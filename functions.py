"""
functions.py
"""
import numpy as np
from sympy import lambdify, abc, latex, diff, integrate
from sympy.parsing.sympy_parser import parse_expr
from sympy.core import basic
from typing import Dict, List, Union


class VariableNotFoundError(Exception):
    """Variable not found error.
    """
    def __str__(self) -> None:
        """Print this exception.
        """
        return "Variable not found"

def zero(*args):
    return args[0]*0


def rect(x: np.ndarray) -> np.ndarray:
    """
    Rectangle function.
    """
    return np.array(
        [
            1.0 if (0.5 > x_i > -0.5) else 0.
            for x_i in x
        ]
        )


def noise(x: np.ndarray) -> np.ndarray:
    """
    This is the noise function.
    """
    return np.array([2.0*np.random.rand() - 1.0 for _ in range(len(x))])


def multiplies_var(main_var: basic.Basic, arb_var: basic.Basic,
                   expr: basic.Basic) -> bool:
    """
    This function takes in the following parameters:
    main_var [sympy.core.basic.Basic]: the main variable
    arb_var [sympy.core.basic.Basic]: an arbitrary variable
    expr [sympy.core.basic.Basic]: an algebraic expression
    Check to see if an arbitrary variable multiplies
    a sub expression that contains the main variable.
    If it does, return True else False.

    The following examples should clarify what this function does:

    >>> expr = parse_expr("a*sinh(k*x) + c")
    >>> multiplies_var(abc.x, abc.a, expr)
    True
    >>> multiplies_var(abc.x, abc.k, expr)
    True
    >>> multiplies_var(abc.x, abc.b, expr)
    False

    >>> expr = parse_expr("w*a**pi*sin(k**10*tan(y*x)*z) + d + e**10*tan(f)")
    >>> multiplies_var(abc.x, abc.w, expr)
    True
    >>> multiplies_var(abc.x, abc.a, expr)
    True
    >>> multiplies_var(abc.x, abc.k, expr)
    True
    >>> multiplies_var(abc.x, abc.z, expr)
    True
    >>> multiplies_var(abc.x, abc.y, expr)
    True
    >>> multiplies_var(abc.x, abc.d, expr)
    False
    >>> multiplies_var(abc.x, abc.e, expr)
    False
    >>> multiplies_var(abc.x, abc.f, expr)
    False
    """
    arg_list = []
    for arg1 in expr.args:
        if arg1.has(main_var):
            arg_list.append(arg1)
            for arg2 in expr.args:
                if ((arg2 is arb_var or (arg2.is_Pow and arg2.has(arb_var)))
                   and expr.has(arg1*arg2)):
                    return True
    return any([multiplies_var(main_var, arb_var, arg)
                for arg in arg_list if
                (arg is not main_var)])


class FunctionR2toR:
    """
    A callable function class that maps two variables,
    as well as any number of parameters, into a single variable.

    Attributes:
    latex_repr [str]: The function as a LaTeX string.
    symbols [sympy.Symbol]: All variables used in this function.
    domain_variables [sympy.Symbol]: The variables in the domain.
    parameters [sympy.Symbol]: All scalar parameters used in the function.
    """

    # Private Attributes:
    # _symbolic_func [sympy.basic.Basic]: symbol function
    # _lambda_func [sympy.Function]: lamba function

    def __init__(self, function_name: str,
                 main_variables:
                 List[basic.Basic]
                 = None) -> None:
        """
        The initializer. The parameter must be a
        string representation of a function.

        >>> f = FunctionR2toR("a*x*cos(x*y) + b")
        >>> f(2, 3.141592653589793, 1.0, 1.0)
        3.0
        >>> a = abc.a
        >>> b = abc.b
        >>> c = abc.c
        >>> f.get_default_values() == {a: 1.0, b: 0.0}
        True
        >>> g = FunctionR2toR("a**2*sin(x) + b*y + c", [abc.x, abc.y])
        >>> g.get_default_values() == {a: 1.0, b: 1.0, c: 0.0}
        True
        >>> g = FunctionR2toR("a**2*sin(x) + c", [abc.x, abc.y])
        >>> g.get_default_values() == {a: 1.0, c: 0.0}
        True
        >>> g = FunctionR2toR("b*sinh(y) + c", [abc.x, abc.y])
        >>> g.get_default_values() == {b: 1.0, c: 0.0}
        True
        """
        self._SINGLE_VARIABLE = 1
        self._DOUBLE_VARIABLE = 2
        self._domain_type = 0
        if main_variables is None:
            param1, param2 = abc.x, abc.y
            main_variables = [param1, param2]
        else:
            param1, param2 = main_variables
        self.domain_variables = main_variables
        # Dictionary of modules and user defined functions.
        # Used for lambdify from sympy to parse input.
        def zero(*args):
            return args[0]*0
        module_list = ["numpy", {"rect": rect, "noise": noise, "zero": zero}]
        self._symbolic_func = parse_expr(function_name)
        symbol_set = self._symbolic_func.free_symbols
        symbol_list = list(symbol_set)
        self.latex_repr = latex(self._symbolic_func)
        if self._symbolic_func.has(param1) and self._symbolic_func.has(param2):
            self._domain_type = self._DOUBLE_VARIABLE
            self.domain_variables = [param1, param2]
            symbol_list.remove(param1)
            symbol_list.remove(param2)
            self.parameters = symbol_list
            main_variables.extend(symbol_list)
            self.symbols = main_variables
            self._lambda_func = lambdify(
                self.symbols, self._symbolic_func, modules=module_list)
        elif (self._symbolic_func.has(param1)
              and not self._symbolic_func.has(param2)):
            self._domain_type = self._SINGLE_VARIABLE
            self.domain_variables = [param1]
            symbols = [param1]
            symbol_list.remove(param1)
            self.parameters = symbol_list
            symbols.extend(symbol_list)
            self.symbols = symbols
            self._lambda_func = lambdify(
                self.symbols, self._symbolic_func, modules=module_list)
        elif (not self._symbolic_func.has(param1)
              and self._symbolic_func.has(param2)):
            self._domain_type = self._SINGLE_VARIABLE
            self.domain_variables = [param2]
            symbols = [param2]
            symbol_list.remove(param2)
            self.parameters = symbol_list
            symbols.extend(symbol_list)
            self.symbols = symbols
            self._lambda_func = lambdify(
                self.symbols, self._symbolic_func, modules=module_list)
        else:
            zero = parse_expr("zero(x, y)")
            self._symbolic_func += zero
            self._domain_type = self._DOUBLE_VARIABLE
            self.domain_variables = [param1, param2]
            self.parameters = symbol_list
            main_variables.extend(symbol_list)
            self.symbols = main_variables
            self._lambda_func = lambdify(
                self.symbols, self._symbolic_func, modules=module_list)
            # raise VariableNotFoundError

    def __call__(self,
                 param1: Union[np.array, float],
                 *args: Union[np.array, float],
                 **kwargs: Union[np.array, float]) -> np.array:
        """
        Call this class as if it were a function.

        >>> f = FunctionR2toR("a**2*sin(x) + b*y", [abc.x, abc.y])
        >>> f(0.0, 1.0, 2.0, 2.0)
        2.0
        >>> f = FunctionR2toR("a**2*(x**2 + 1)", [abc.x, abc.y])
        >>> f(1.0, 1.0)
        2.0
        """
        if self._domain_type == self._DOUBLE_VARIABLE:
            param2, *args = args
            return self._lambda_func(param1, param2, *args, **kwargs)
        elif self._domain_type == self._SINGLE_VARIABLE:
            return self._lambda_func(param1, *args, **kwargs)
        else:
            pass

    def get_default_values(self) -> Dict[basic.Basic, float]:
        """
        Get a dict of the suggested default values for each parameter
        used in this function.
        """
        default_values_dict = {}
        for s in self.parameters:
            value = float(multiplies_var(
                self.symbols[0], s, self._symbolic_func)
                          or multiplies_var(
                              self.symbols[1], s, self._symbolic_func))
            default_values_dict[s] = value
        return default_values_dict


if __name__ == "__main__":
    import doctest
    from time import perf_counter
    t1 = perf_counter()
    doctest.testmod()
    t2 = perf_counter()
    print(t2 - t1)
