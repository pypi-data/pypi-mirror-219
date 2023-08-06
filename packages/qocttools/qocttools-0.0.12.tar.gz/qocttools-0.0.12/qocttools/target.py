## Copyright 2019-present The qocttools developing team
##
## This file is part of qocttools.
##
## qocttools is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## qocttools is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with qocttools.  If not, see <https://www.gnu.org/licenses/>.

"""This module contains the Target class, and associated procedures.

"""

import jax; jax.config.update('jax_platform_name', 'cpu')
import jax.numpy as jnp
from jax import grad
import numpy as np
import qocttools.math_extra as math_extra
import qocttools.floquet as floquet
import qutip as qt


class Target:
    """The class that holds the definition of the target

    Parameters
    ----------
    targettype: string
        The code admits the following types of characters:

        1. generic

           The user may input any function as target, defined by
           the driver program, using the `Fyu` parameter (see below).

        2. expectationvalue

           The target is the expectation value of some operator:

           .. math::

              F(y, u) = \\langle \\Psi(T)\\vert O \\vert \\Psi(T)\\rangle

           or, if the multitarget option is used,

           .. math::

              F(y, u) = \\frac{1}{Q} \\sum_i \\langle \\Psi_i(T)\\vert O_i \\vert \\Psi_i(T)\\rangle

           Here, :math:`Q` is the number of targets. The operator(s) should be provided 
           using the `operator` argument (below).

        3. evolutionoperator

           The goal now is to find a set of control parameters that leads to an evolution of
           the system characterized by a fixed target evolution operator. This target evolution
           operator (or operators, if a multitarget setup is used), is provided by the argument
           `Utarget`. The target definition is:

           .. math::

              F(U, u) = \\frac{1}{Q} \\sum_i \\vert U(T) \\cdot U^{(i)}_{\\rm target} \\vert^2

        4. floquet

    Fyu: function

        If `targettype == "generic"`, the user should pass the function used to 
        define the target. The interface should be:

        .. code-block:: python

           def Fyu(y: qutip.Qobj or list of qutip.Qobj, u: ndarray) -> float:

        The function `Fyu` should receive as argument a system state (be it a Hilbert
        state, evolution operator, or density matrix), that is supposed to be the state
        at the end of the propagation, and a control parameters set. It should output
        the target functional value. It may also take as argument a list of states, if
        one is running the optimizaion in *multitarget* mode.

    dFdy: function

        If `targettype == "generic"`, the user should pass the function used to 
        define the target (`Fyu`), **and** the derivative of that function with respect to
        the state, which would be given by this `dFdy` parameter. The interface should be:

        .. code-block:: python

           def dFdy(y: qutip.Qobj or list of qutip.Qobj, u: ndarray) -> list of float:

    dFdu: function

        If `targettype == "generic"`, the user should pass the function used to 
        define the target (`Fyu`), **and, if it is not zero**, the derivative of that function with respect to
        the control parameters, which would be given by this `dFdu` parameter. The interface should be:

        .. code-block:: python

           def dFdu(u: ndarray, m: int) -> float:

    """
    def __init__(self, targettype, 
                 Fyu = None,
                 dFdy = None,
                 dFdu = None,
                 operator = None,
                 Utarget = None,
                 alpha = None,
                 S = None,
                 targeteps = None,
                 T = None,
                 fepsilon = None,
                 dfdepsilon = None):
        self.targettype = targettype
        if targettype == 'generic':
            self.Fyu_ = Fyu
            self.dFdy_ = dFdy
            self.operator = operator
        elif targettype == 'expectationvalue':
            if isinstance(operator, list):
                self.operator = []
                for i in range(len(operator)):
                    self.operator.append(operator[i].copy())
            else:
                self.operator = [operator.copy()]
        elif targettype == 'evolutionoperator':
            if isinstance(Utarget, list):
                self.Utarget = []
                for i in range(len(Utarget)):
                    self.Utarget.append(Utarget[i].copy())
            else:
                self.Utarget = [Utarget.copy()]
            self.operator = operator
        elif targettype == 'floquet':
            if targeteps is not None:
                self.targeteps = targeteps.copy()
            else:
                self.targeteps = None
            self.T = T
            self.operator = operator
            self.fepsilon_ = fepsilon
            self.dfdepsilon_ = dfdepsilon
        self.dFdu = dFdu
        self.alpha = alpha
        if S == None:
            self.S = lambda x: 1
        else:
            self.S = S


    def Fyu(self, y, u):
        """The functional F of the trayectory y that is to be maximized
        
        It may also be an explicit function of the control parameters u.

        Parameters
        ----------
        y : qutip.result 
            The trajectory of the quantum system
        u : ndarray
            The control parameters that were used to generate the trajectory.

        Returns
        -------
        float:
            The value of the target functional.
        """
        if self.targettype == 'generic':
            if self.dFdy_ == 'ad':
                return float(self.Fyu_(jnp.array(y.full()), u))
            else:
                return self.Fyu_(y, u)

        if self.targettype == 'floquet':
            Fval = 1.0
            if not isinstance(y, list):
                UTset_ = [y]
            else:
                UTset_ = y
            nst = len(UTset_)
            dim = UTset_[0].dims[0][0]
            epsilon = np.zeros([nst, dim])
            for k in range(len(UTset_)):
                epsilon[k, :] = floquet.epsi(UTset_[k].full(), self.T)
            return self.f(epsilon)

        elif self.targettype == 'expectationvalue':
            if isinstance(y, list):
                ntgs = len(y)
                x = 0.0
                for j in range(len(y)):
                    x = x + qt.expect(self.operator[j], y[j])
            else:
                ntgs = 1
                x = qt.expect(self.operator[0], y)
            return x / ntgs

        elif self.targettype == 'evolutionoperator':
            if isinstance(y, list):
                ntgs = len(y)
                x = 0.0
                for j in range(ntgs):
                    dim = y[j].shape[0]
                    x = x + (1/dim**2) * (np.absolute(math_extra.frobenius_product(self.Utarget[j], y[j])))**2
                x = x / ntgs
                return x
            else:
                dim = y.shape[0]
                return (1/dim**2)*(np.absolute(math_extra.frobenius_product(self.Utarget[0], y)))**2

    def dFdy(self, y, u):
        """Derivative of the target functional wrt the quantum trajectory.

        Right now, it in fact assumes that the functional only depends on the final
        state of the quantum trajectory. This functional derivative is used to determine
        the boundary condition used in the definition of the costate.

        Parameters
        ----------
        y: qutip.Qobj or list of qutip.Qobj
           The state of the system at the final time of the propagation
        u: ndarray
           The control parameters

        Returns
        -------
        qutip.Qobj or list of qutip.Qobj
           The derivative of F with respect to the quantum state.
        """
        if self.targettype == 'generic':
            if self.dFdy_ == 'ad':
                shape = np.array(y.full().shape)
                d = shape.prod()
                def Fyureal(yr, u):
                    yreal = yr[0:d]
                    yimag = yr[d:]
                    y = yreal + 1j*yimag
                    y = y.reshape(shape)
                    res = self.Fyu_(y, u)
                    return res
                dFdyureal = grad(Fyureal, argnums = 0)
                # This should put first the real parts, and then the imaginary parts (check!)
                yreal = jnp.hstack([y.full().real.flatten(), y.full().imag.flatten()])
                gf = dFdyureal(yreal, u)
                gfr = gf[:d]
                gfi = gf[d:]
                gfw = (1.0/2.0) * (gfr + 1j * gfi)
                gfw = gfw.reshape(shape)
                gfw = np.array(gfw)
                res = qt.Qobj(gfw)
                return res
            else:
                return self.dFdy_(y, u)

        if self.targettype == 'floquet':
            if not isinstance(y, list):
                UTset_ = [y]
            else:
                UTset_ = y
            nst = len(UTset_)
            dim = UTset_[0].dims[0][0]
            epsilon = np.zeros([nst, dim])
            dfdy = []
            for k in range(len(UTset_)):
                dfdy.append(np.zeros([dim, dim], dtype = complex))
                UT = UTset_[k].full()
                epsilon[k, :] = floquet.epsi(UT, self.T)
                depsi = floquet.depsi(UT, self.T)
                for m in range(dim):
                    dfdy[k][:, :] += self.dfdepsilon(epsilon)[k, m] * depsi[m, :, :]
                dfdy[k] = qt.Qobj(dfdy[k])
            return dfdy

        elif self.targettype == 'expectationvalue':
            if isinstance(y, list):
                dF = []
                ntgs = len(y)
                for j in range(len(y)):
                    if y[j].isket:
                        dF.append(self.operator[j] * y[j] / ntgs)
                    else:
                        dF.append(0.5 * self.operator[j] / ntgs)
                return dF
            else:
                if y.isket:
                    return self.operator[0]*y
                else:
                    return 0.5 * self.operator[0]

        elif self.targettype == 'evolutionoperator':
            if isinstance(y, list):
                dF = []
                ntgs = len(y)
                for j in range(ntgs):
                    dim = y[j].shape[0]
                    dF.append( (1/dim**2) * math_extra.frobenius_product(self.Utarget[j], y[j])*self.Utarget[j] / ntgs)
                return dF
            else:
                dim = y.shape[0]
                return (1/dim**2) * math_extra.frobenius_product(self.Utarget[0], y)*self.Utarget[0]


    def f(self, eps):
        if self.fepsilon_ is not None:
            return self.fepsilon_(eps)
        cte = 1.0
        fval = 0.0
        nkpoints = eps.shape[0]
        targete = self.targeteps
        dim = eps.shape[1]
        fval = 0.0
        for k in range(nkpoints):
            for alpha in range(dim):
                fval = fval - cte * (eps[k, alpha] - targete[k, alpha])**2
        return fval


    def dfdepsilon(self, eps):
        if self.dfdepsilon_ is not None:
            return self.dfdepsilon_(eps)
        cte = 1.0
        nkpoints = eps.shape[0]
        targete = self.targeteps
        dim = eps.shape[1]
        dfval = np.zeros((nkpoints, dim))
        for k in range(nkpoints):
            for alpha in range(dim):
                dfval[k, alpha] = - 2.0 * cte * (eps[k, alpha]-targete[k, alpha])
        return dfval
