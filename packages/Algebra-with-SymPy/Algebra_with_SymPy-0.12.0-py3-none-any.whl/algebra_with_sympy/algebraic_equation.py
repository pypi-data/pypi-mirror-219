"""
Algebraic Equations with SymPy
==============================

These tools define relations that all high school and college students would
recognize as mathematical equations. They consist of a left hand side (lhs)
and a right hand side (rhs) connected by a relation operator such as "=". At
present the "=" relation operator is the only option. The relation operator may
not be set.

This class should not be confused with the Boolean class ``Equality``
(abbreviated ``Eq``) which specifies that the equality of two objects is
``True``.

This tool applies operations to both sides of the equation simultaneously, just
as students are taught to do when attempting to isolate (solve for) a
variable. Thus the statement ``Equation/b`` yields a new equation
``Equation.lhs/b = Equation.rhs/b``

The intent is to allow using the mathematical tools in SymPy to rearrange
equations and perform algebra in a stepwise fashion. In this way more people
can successfully perform algebraic rearrangements without stumbling over
missed details such as a negative sign. This mimics the capabilities available
in [SageMath](https://www.sagemath.org/) and
[Maxima](http://maxima.sourceforge.net/).
"""
import sys

import sympy
from sympy.core.add import _unevaluated_Add
from sympy.core.expr import Expr
from sympy.core.basic import Basic
from sympy.core.evalf import EvalfMixin
from sympy.core.sympify import _sympify
from algebra_with_sympy.preparser import integers_as_exact
import functools
from sympy import *

class algwsym_config():

    def __init__(self):
        """
        This is a class to hold parameters that control behavior of
        the algebra_with_sympy package.

        Settings
        ========
        Printing
        --------
        In interactive environments the default output of an equation is a
        human readable string with the two sides connected by an equals
        sign or a typeset equation with the two sides connected by an equals sign.
        `print(Eqn)` or `str(Eqn)` will return this human readable text version of
        the equation as well. This is consistent with python standards, but not
        sympy, where `str()` is supposed to return something that can be
        copy-pasted into code. If the equation has a declared name as in `eq1 =
        Eqn(a,b/c)` the name will be displayed to the right of the equation in
        parentheses (eg. `a = b/c    (eq1)`). Use `print(repr(Eqn))` instead of
        `print(Eqn)` or `repr(Eqn)` instead of `str(Eqn)` to get a code
        compatible version of the equation.

        You can adjust this behvior using some flags that impact output:
        * `algwsym_config.output.show_code` default is `False`.
        * `algwsym_config.output.human_text` default is `True`.
        * `algwsym_config.output.label` default is `True`.

        In interactive environments you can get both types of output by setting
        the `algwsym_config.output.show_code` flag. If this flag is true
        calls to `latex` and `str` will also print an additional line "code
        version: `repr(Eqn)`". Thus in Jupyter you will get a line of typeset
        mathematics output preceded by the code version that can be copy-pasted.
        Default is `False`.

        A second flag `algwsym_config.output.human_text` is useful in
        text-based interactive environments such as command line python or
        ipython. If this flag is true `repr` will return `str`. Thus the human
        readable text will be printed as the output of a line that is an
        expression containing an equation.
        Default is `True`.

        Setting both of these flags to true in a command line or ipython
        environment will show both the code version and the human readable text.
        These flags impact the behavior of the `print(Eqn)` statement.

        The third flag `algwsym_config.output.label` has a default value of
        `True`. Setting this to `False` suppresses the labeling of an equation
        with its python name off to the right of the equation.
        """
        pass

    class output():

        def __init__(self):
            """This holds settings that impact output.
            """
            pass

        @property
        def show_code(self):
            """
            If `True` code versions of the equation expression will be
            output in interactive environments. Default = `False`.
            """
            return self.show_code

        @property
        def human_text(self):
            """
            If `True` the human readable equation expression will be
            output in text interactive environments. Default = `False`.
            """
            return self.human_text

        @property
        def solve_to_list(self):
            """
            If `True` the results of a call to `solve(...)` will return a
            Python `list` rather than a Sympy `FiniteSet`. This recovers
            behavior for versions before 0.11.0.

            Note: setting this `True` means that expressions within the
            returned solutions will not be pretty-printed in Jupyter and
            IPython.
            """
            return self.solve_to_list

    class numerics():

        def __init__(self):
            """This class holds settings for how numerical computation and
            inputs are handled.
            """
            pass

        def integers_as_exact(self):
            """**This is a flag for informational purposes and interface
            consistency. Changing the value will not change the behavior.**

            To change the behavior call:
            * `unset_integers_as_exact()` to turn this feature off.
            * `set_integers_as_exact()` to turn this feature on (on by
            default).

            If set to `True` (the default) and if running in an
            IPython/Jupyter environment any number input without a decimal
            will be interpreted as a sympy integer. Thus, fractions and
            related expressions will not evalute to floating point numbers,
            but be maintained as exact expressions (e.g. 2/3 -> 2/3 not the
            float 0.6666...).
            """
            return self.integers_as_exact

def __latex_override__(expr, *arg):
    from IPython import get_ipython
    show_code = False
    if get_ipython():
        algwsym_config = get_ipython().user_ns.get("algwsym_config", False)
    else:
        algwsym_config = globals()['algwsym_config']
    if algwsym_config:
        show_code = algwsym_config.output.show_code
    if show_code:
        print("Code version: " + repr(expr))
    return '$'+latex(expr) + '$'

def __command_line_printing__(expr, *arg):
    # print('Entering __command_line_printing__')
    human_text = True
    show_code = False
    if algwsym_config:
        human_text = algwsym_config.output.human_text
        show_code = algwsym_config.output.show_code
    tempstr = ''
    if show_code:
        tempstr += "Code version: " + repr(expr) + '\n'
    if not human_text:
        return print(tempstr + repr(expr))
    else:
        return print(tempstr + str(expr))

# Now we inject the formatting override(s)
from IPython import get_ipython
ip = get_ipython()
formatter = None
if ip:
    # In an environment that can display typeset latex
    formatter = ip.display_formatter
    old = formatter.formatters['text/latex'].for_type(Basic,
                                                      __latex_override__)
    # print("For type Basic overriding latex formatter = " + str(old))

    # For the terminal based IPython
    if "text/latex" not in formatter.active_types:
        old = formatter.formatters['text/plain'].for_type(tuple,
                                                    __command_line_printing__)
        # print("For type tuple overriding plain text formatter = " + str(old))
        for k in sympy.__all__:
            if k in globals() and not "Printer" in k:
                if isinstance(globals()[k], type):
                    old = formatter.formatters['text/plain'].\
                        for_type(globals()[k], __command_line_printing__)
                    # print("For type "+str(k)+
                    # " overriding plain text formatter = " + str(old))
else:
    # command line
    # print("Overriding command line printing of python.")
    sys.displayhook = __command_line_printing__

# Numerics controls
def set_integers_as_exact():
    """This operation uses `sympy.interactive.session.int_to_Integer`, which
    causes any number input without a decimal to be interpreted as a sympy
    integer, to pre-parse input cells. It also sets the flag
    `algwsym_config.numerics.integers_as_exact = True` This is the default
    mode of algebra_with_sympy. To turn this off call
    `unset_integers_as_exact()`.
    """
    from IPython import get_ipython
    if get_ipython():
        get_ipython().input_transformers_post.append(integers_as_exact)
        algwsym_config = get_ipython().user_ns.get("algwsym_config", False)
        if algwsym_config:
            algwsym_config.numerics.integers_as_exact = True
        else:
            raise ValueError("The algwsym_config object does not exist.")
    return

def unset_integers_as_exact():
    """This operation disables forcing of numbers input without
    decimals being interpreted as sympy integers. Numbers input without a
    decimal may be interpreted as floating point if they are part of an
    expression that undergoes python evaluation (e.g. 2/3 -> 0.6666...). It
    also sets the flag `algwsym_config.numerics.integers_as_exact = False`.
    Call `set_integers_as_exact()` to avoid this conversion of rational
    fractions and related expressions to floating point. Algebra_with_sympy
    starts with `set_integers_as_exact()` enabled (
    `algwsym_config.numerics.integers_as_exact = True`).
    """
    from IPython import get_ipython
    if get_ipython():
        pre = get_ipython().input_transformers_post
        # The below looks excessively complicated, but more reliably finds the
        # transformer to remove across varying IPython environments.
        for k in pre:
            if "integers_as_exact" in k.__name__:
                pre.remove(k)
        algwsym_config = get_ipython().user_ns.get("algwsym_config", False)
        if algwsym_config:
            algwsym_config.numerics.integers_as_exact = False
        else:
            raise ValueError("The algwsym_config object does not exist.")

    return

class Equation(Basic, EvalfMixin):
    """
    This class defines an equation with a left-hand-side (tlhs) and a right-
    hand-side (rhs) connected by the "=" operator (e.g. `p*V = n*R*T`).

    Explanation
    ===========
    This class defines relations that all high school and college students
    would recognize as mathematical equations. At present only the "=" relation
    operator is recognized.

    This class is intended to allow using the mathematical tools in SymPy to
    rearrange equations and perform algebra in a stepwise fashion. In this
    way more people can successfully perform algebraic rearrangements without
    stumbling over missed details such as a negative sign.

    Create an equation with the call ``Equation(lhs,rhs)``, where ``lhs`` and
    ``rhs`` are any valid Sympy expression. ``Eqn(...)`` is a synonym for
    ``Equation(...)``.

    Parameters
    ==========
    lhs: sympy expression, ``class Expr``.
    rhs: sympy expression, ``class Expr``.
    kwargs:

    Examples
    ========
    NOTE: All the examples below are in vanilla python. You can get human
    readable eqautions "lhs = rhs" in vanilla python by adjusting the settings
    in `algwsym_config` (see it's documentation). Output is human readable by
    default in IPython and Jupyter environments.
    >>> from algebra_with_sympy import *
    >>> a, b, c, x = var('a b c x')
    >>> Equation(a,b/c)
    Equation(a, b/c)
    >>> t=Eqn(a,b/c)
    >>> t
    Equation(a, b/c)
    >>> t*c
    Equation(a*c, b)
    >>> c*t
    Equation(a*c, b)
    >>> exp(t)
    Equation(exp(a), exp(b/c))
    >>> exp(log(t))
    Equation(a, b/c)

    Simplification and Expansion
    >>> f = Eqn(x**2 - 1, c)
    >>> f
    Equation(x**2 - 1, c)
    >>> f/(x+1)
    Equation((x**2 - 1)/(x + 1), c/(x + 1))
    >>> (f/(x+1)).simplify()
    Equation(x - 1, c/(x + 1))
    >>> simplify(f/(x+1))
    Equation(x - 1, c/(x + 1))
    >>> (f/(x+1)).expand()
    Equation(x**2/(x + 1) - 1/(x + 1), c/(x + 1))
    >>> expand(f/(x+1))
    Equation(x**2/(x + 1) - 1/(x + 1), c/(x + 1))
    >>> factor(f)
    Equation((x - 1)*(x + 1), c)
    >>> f.factor()
    Equation((x - 1)*(x + 1), c)
    >>> f2 = f+a*x**2+b*x +c
    >>> f2
    Equation(a*x**2 + b*x + c + x**2 - 1, a*x**2 + b*x + 2*c)
    >>> collect(f2,x)
    Equation(b*x + c + x**2*(a + 1) - 1, a*x**2 + b*x + 2*c)

    Apply operation to only one side
    >>> poly = Eqn(a*x**2 + b*x + c*x**2, a*x**3 + b*x**3 + c*x)
    >>> poly.applyrhs(factor,x)
    Equation(a*x**2 + b*x + c*x**2, x*(c + x**2*(a + b)))
    >>> poly.applylhs(factor)
    Equation(x*(a*x + b + c*x), a*x**3 + b*x**3 + c*x)
    >>> poly.applylhs(collect,x)
    Equation(b*x + x**2*(a + c), a*x**3 + b*x**3 + c*x)

    ``.apply...`` also works with user defined python functions
    >>> def addsquare(eqn):
    ...     return eqn+eqn**2
    ...
    >>> t.apply(addsquare)
    Equation(a**2 + a, b**2/c**2 + b/c)
    >>> t.applyrhs(addsquare)
    Equation(a, b**2/c**2 + b/c)
    >>> t.apply(addsquare, side = 'rhs')
    Equation(a, b**2/c**2 + b/c)
    >>> t.applylhs(addsquare)
    Equation(a**2 + a, b/c)
    >>> addsquare(t)
    Equation(a**2 + a, b**2/c**2 + b/c)

    Inaddition to ``.apply...`` there is also the less general ``.do``,
    ``.dolhs``, ``.dorhs``, which only works for operations defined on the
    ``Expr`` class (e.g.``.collect(), .factor(), .expand()``, etc...).
    >>> poly.dolhs.collect(x)
    Equation(b*x + x**2*(a + c), a*x**3 + b*x**3 + c*x)
    >>> poly.dorhs.collect(x)
    Equation(a*x**2 + b*x + c*x**2, c*x + x**3*(a + b))
    >>> poly.do.collect(x)
    Equation(b*x + x**2*(a + c), c*x + x**3*(a + b))
    >>> poly.dorhs.factor()
    Equation(a*x**2 + b*x + c*x**2, x*(a*x**2 + b*x**2 + c))

    ``poly.do.exp()`` or other sympy math functions will raise an error.

    Rearranging an equation (simple example made complicated as illustration)
    >>> p, V, n, R, T = var('p V n R T')
    >>> eq1=Eqn(p*V,n*R*T)
    >>> eq1
    Equation(V*p, R*T*n)
    >>> eq2 =eq1/V
    >>> eq2
    Equation(p, R*T*n/V)
    >>> eq3 = eq2/R/T
    >>> eq3
    Equation(p/(R*T), n/V)
    >>> eq4 = eq3*R/p
    >>> eq4
    Equation(1/T, R*n/(V*p))
    >>> 1/eq4
    Equation(T, V*p/(R*n))
    >>> eq5 = 1/eq4 - T
    >>> eq5
    Equation(0, -T + V*p/(R*n))

    Substitution (#'s and units)
    >>> L, atm, mol, K = var('L atm mol K', positive=True, real=True) # units
    >>> eq2.subs({R:0.08206*L*atm/mol/K,T:273*K,n:1.00*mol,V:24.0*L})
    Equation(p, 0.9334325*atm)
    >>> eq2.subs({R:0.08206*L*atm/mol/K,T:273*K,n:1.00*mol,V:24.0*L}).evalf(4)
    Equation(p, 0.9334*atm)

    Substituting an equation into another equation:
    >>> P, P1, P2, A1, A2, E1, E2 = symbols("P, P1, P2, A1, A2, E1, E2")
    >>> eq1 = Eqn(P, P1 + P2)
    >>> eq2 = Eqn(P1 / (A1 * E1), P2 / (A2 * E2))
    >>> P1_val = (eq1 - P2).swap
    >>> P1_val
    Equation(P1, P - P2)
    >>> eq2 = eq2.subs(P1_val)
    >>> eq2
    Equation((P - P2)/(A1*E1), P2/(A2*E2))
    >>> P2_val = solve(eq2.subs(P1_val), P2).args[0]
    >>> P2_val
    Equation(P2, A2*E2*P/(A1*E1 + A2*E2))

    Combining equations (Math with equations: lhs with lhs and rhs with rhs)
    >>> q = Eqn(a*c, b/c**2)
    >>> q
    Equation(a*c, b/c**2)
    >>> t
    Equation(a, b/c)
    >>> q+t
    Equation(a*c + a, b/c + b/c**2)
    >>> q/t
    Equation(c, 1/c)
    >>> t**q
    Equation(a**(a*c), (b/c)**(b/c**2))

    Utility operations
    >>> t.reversed
    Equation(b/c, a)
    >>> t.swap
    Equation(b/c, a)
    >>> t.lhs
    a
    >>> t.rhs
    b/c
    >>> t.as_Boolean()
    Eq(a, b/c)

    `.check()` convenience method for `.as_Boolean().simplify()`
    >>> from sympy import I, pi
    >>> Equation(pi*(I+2), pi*I+2*pi).check()
    True
    >>> Eqn(a,a+1).check()
    False

    Differentiation
    Differentiation is applied to both sides if the wrt variable appears on
    both sides.
    >>> q=Eqn(a*c, b/c**2)
    >>> q
    Equation(a*c, b/c**2)
    >>> diff(q,b)
    Equation(Derivative(a*c, b), c**(-2))
    >>> diff(q,c)
    Equation(a, -2*b/c**3)
    >>> diff(log(q),b)
    Equation(Derivative(log(a*c), b), 1/b)
    >>> diff(q,c,2)
    Equation(Derivative(a, c), 6*b/c**4)

    If you specify multiple differentiation all at once the assumption
    is order of differentiation matters and the lhs will not be
    evaluated.
    >>> diff(q,c,b)
    Equation(Derivative(a*c, b, c), -2/c**3)

    To overcome this specify the order of operations.
    >>> diff(diff(q,c),b)
    Equation(Derivative(a, b), -2/c**3)

    But the reverse order returns an unevaulated lhs (a may depend on b).
    >>> diff(diff(q,b),c)
    Equation(Derivative(a*c, b, c), -2/c**3)

    Integration can only be performed on one side at a time.
    >>> q=Eqn(a*c,b/c)
    >>> integrate(q,b,side='rhs')
    b**2/(2*c)
    >>> integrate(q,b,side='lhs')
    a*b*c

    Make a pretty statement of integration from an equation
    >>> Eqn(Integral(q.lhs,b),integrate(q,b,side='rhs'))
    Equation(Integral(a*c, b), b**2/(2*c))

    Integration of each side with respect to different variables
    >>> q.dorhs.integrate(b).dolhs.integrate(a)
    Equation(a**2*c/2, b**2/(2*c))

    Automatic solutions using sympy solvers. THIS IS EXPERIMENTAL. Please
    report issues at https://github.com/gutow/Algebra_with_Sympy/issues.
    >>> tosolv = Eqn(a - b, c/a)
    >>> solve(tosolv,a)
    FiniteSet(Equation(a, b/2 - sqrt(b**2 + 4*c)/2), Equation(a, b/2 + sqrt(b**2 + 4*c)/2))
    >>> solve(tosolv, b)
    FiniteSet(Equation(b, (a**2 - c)/a))
    >>> solve(tosolv, c)
    FiniteSet(Equation(c, a**2 - a*b))
    """

    def __new__(cls, lhs, rhs, **kwargs):
        lhs = _sympify(lhs)
        rhs = _sympify(rhs)
        if not isinstance(lhs, Expr) or not isinstance(rhs, Expr):
            raise TypeError('lhs and rhs must be valid sympy expressions.')
        return super().__new__(cls, lhs, rhs)

    def _get_eqn_name(self):
        """
        Tries to find the python string name that refers to the equation. In
        IPython environments (IPython, Jupyter, etc...) looks in the user_ns.
        If not in an IPython environment looks in __main__.
        :return: string value if found or empty string.
        """
        human_text = algwsym_config.output.human_text
        algwsym_config.output.human_text=False
        import __main__ as shell
        for k in dir(shell):
            item = getattr(shell,k)
            if isinstance(item,Equation):
                if item.__repr__()==self.__repr__() and not \
                        k.startswith('_'):
                    algwsym_config.output.human_text=human_text
                    return k
        algwsym_config.output.human_text = human_text
        return ''

    @property
    def lhs(self):
        """
        Returns the lhs of the equation.
        """
        return self.args[0]

    @property
    def rhs(self):
        """
        Returns the rhs of the equation.
        """
        return self.args[1]

    def as_Boolean(self):
        """
        Converts the equation to an Equality.
        """
        return Equality(self.lhs, self.rhs)

    def check(self, **kwargs):
        """
        Forces simplification and casts as `Equality` to check validity.
        Parameters
        ----------
        kwargs any appropriate for `Equality`.

        Returns
        -------
        True, False or an unevaluated `Equality` if truth cannot be determined.
        """
        return Equality(self.lhs, self.rhs, **kwargs).simplify()

    @property
    def reversed(self):
        """
        Swaps the lhs and the rhs.
        """
        return Equation(self.rhs, self.lhs)

    @property
    def swap(self):
        """
        Synonym for `.reversed`
        """
        return self.reversed

    def _applytoexpr(self, expr, func, *args, **kwargs):
        # Applies a function to an expression checking whether there
        # is a specialized version associated with the particular type of
        # expression. Errors will be raised if the function cannot be
        # applied to an expression.
        funcname = getattr(func, '__name__', None)
        if funcname is not None:
            localfunc = getattr(expr, funcname, None)
            if localfunc is not None:
                return localfunc(*args, **kwargs)
        return func(expr, *args, **kwargs)

    def apply(self, func, *args, side='both', **kwargs):
        """
        Apply an operation/function/method to the equation returning the
        resulting equation.

        Parameters
        ==========

        func: object
            object to apply usually a function

        args: as necessary for the function

        side: 'both', 'lhs', 'rhs', optional
            Specifies which side of the equation the operation will be applied
            to. Default is 'both'.

        kwargs: as necessary for the function
         """
        lhs = self.lhs
        rhs = self.rhs
        if side in ('both', 'lhs'):
            lhs = self._applytoexpr(self.lhs, func, *args, **kwargs)
        if side in ('both', 'rhs'):
            rhs = self._applytoexpr(self.rhs, func, *args, **kwargs)
        return Equation(lhs, rhs)

    def applylhs(self, func, *args, **kwargs):
        """
        If lhs side of the equation has a defined subfunction (attribute) of
        name ``func``, that will be applied instead of the global function.
        The operation is applied to only the lhs.
        """
        return self.apply(func, *args, **kwargs, side='lhs')

    def applyrhs(self, func, *args, **kwargs):
        """
        If rhs side of the equation has a defined subfunction (attribute) of
        name ``func``, that will be applied instead of the global function.
        The operation is applied to only the rhs.
        """
        return self.apply(func, *args, **kwargs, side='rhs')

    class _sides:
        """
        Helper class for the `.do.`, `.dolhs.`, `.dorhs.` syntax for applying
        submethods of expressions.
        """

        def __init__(self, eqn, side='both'):
            self.eqn = eqn
            self.side = side

        def __getattr__(self, name):
            func = None
            if self.side in ('rhs', 'both'):
                func = getattr(self.eqn.rhs, name, None)
            else:
                func = getattr(self.eqn.lhs, name, None)
            if func is None:
                raise AttributeError('Expressions in the equation have no '
                                     'attribute `' + str(
                    name) + '`. Try `.apply('
                                     + str(name) + ', *args)` or '
                                                   'pass the equation as a parameter to `'
                                     + str(name) + '()`.')
            return functools.partial(self.eqn.apply, func, side=self.side)

    @property
    def do(self):
        return self._sides(self, side='both')

    @property
    def dolhs(self):
        return self._sides(self, side='lhs')

    @property
    def dorhs(self):
        return self._sides(self, side='rhs')
    
    def _eval_rewrite(self, rule, args, **kwargs):
        """Return Equation(L, R) as Equation(L - R, 0) or as L - R.

        Parameters
        ==========

        evaluate : bool, optional
            Control the evaluation of the result. If `evaluate=None` then
            terms in L and R will not cancel but they will be listed in
            canonical order; otherwise non-canonical args will be returned.
            Default to True.
        
        eqn : bool, optional
            Control the returned type. If `eqn=True`, then Equation(L - R, 0)
            is returned. Otherwise, the L - R symbolic expression is returned.
            Default to True.

        Examples
        ========
        >>> from sympy import Add
        >>> from sympy.abc import b, x
        >>> from algebra_with_sympy import Equation
        >>> eq = Equation(x + b, x - b)
        >>> eq.rewrite(Add)
        Equation(2*b, 0)
        >>> eq.rewrite(Add, evaluate=None).lhs.args
        (b, b, x, -x)
        >>> eq.rewrite(Add, evaluate=False).lhs.args
        (b, x, b, -x)
        >>> eq.rewrite(Add, eqn=False)
        2*b
        >>> eq.rewrite(Add, eqn=False, evaluate=False).args
        (b, x, b, -x)
        """
        if rule == Add:
            # NOTE: the code about `evaluate` is very similar to
            # sympy.core.relational.Equality._eval_rewrite_as_Add
            eqn = kwargs.pop("eqn", True)
            evaluate = kwargs.get('evaluate', True)
            L, R = args
            if evaluate:
                # allow cancellation of args
                expr = L - R
            else:
                args = Add.make_args(L) + Add.make_args(-R)
                if evaluate is None:
                    # no cancellation, but canonical
                    expr = _unevaluated_Add(*args)
                else:
                    # no cancellation, not canonical
                    expr = Add._from_args(args)
            if eqn:
                return self.func(expr, 0)
            return expr

    def subs(self, *args, **kwargs):
        """Substitutes old for new in an equation after sympifying args.
    
        `args` is either:

        * one or more arguments of type `Equation(old, new)`.
        * two arguments, e.g. foo.subs(old, new)
        * one iterable argument, e.g. foo.subs(iterable). The iterable may be:

            - an iterable container with (old, new) pairs. In this case the
              replacements are processed in the order given with successive
              patterns possibly affecting replacements already made.
            - a dict or set whose key/value items correspond to old/new pairs.
              In this case the old/new pairs will be sorted by op count and in
              case of a tie, by number of args and the default_sort_key. The
              resulting sorted list is then processed as an iterable container
              (see previous).
        
        If the keyword ``simultaneous`` is True, the subexpressions will not be
        evaluated until all the substitutions have been made.

        Please, read ``help(Expr.subs)`` for more examples.

        Examples
        ========

        >>> from sympy.abc import a, b, c, x
        >>> from algebra_with_sympy import Equation
        >>> eq = Equation(x + a, b * c)

        Substitute a single value:

        >>> eq.subs(b, 4)
        Equation(a + x, 4*c)

        Substitute a multiple values:

        >>> eq.subs([(a, 2), (b, 4)])
        Equation(x + 2, 4*c)
        >>> eq.subs({a: 2, b: 4})
        Equation(x + 2, 4*c)

        Substitute an equation into another equation:

        >>> eq2 = Equation(x + a, 4)
        >>> eq.subs(eq2)
        Equation(4, b*c)

        Substitute multiple equations into another equation:

        >>> eq1 = Equation(x + a + b + c, x * a * b * c)
        >>> eq2 = Equation(x + a, 4)
        >>> eq3 = Equation(b, 5)
        >>> eq1.subs(eq2, eq3)
        Equation(c + 9, 5*a*c*x)

        """
        new_args = args
        if all(isinstance(a, self.func) for a in args):
            new_args = [{a.args[0]: a.args[1] for a in args}]
        elif (len(args) == 1) and all(isinstance(a, self.func) for a in
                                      args[0]):
            raise TypeError("You passed into `subs` a list of elements of "
                "type `Equation`, but this is not supported. Please, consider "
                "unpacking the list with `.subs(*eq_list)` or select your "
                "equations from the list and use `.subs(eq_list[0], eq_list["
                "2], ...)`.")
        elif any(isinstance(a, self.func) for a in args):
            raise ValueError("`args` contains one or more Equation and some "
                "other data type. This mode of operation is not supported. "
                "Please, read `subs` documentation to understand how to "
                "use it.")
        return super().subs(*new_args, **kwargs)

    #####
    # Overrides of binary math operations
    #####

    @classmethod
    def _binary_op(cls, a, b, opfunc_ab):
        if isinstance(a, Equation) and not isinstance(b, Equation):
            return Equation(opfunc_ab(a.lhs, b), opfunc_ab(a.rhs, b))
        elif isinstance(b, Equation) and not isinstance(a, Equation):
            return Equation(opfunc_ab(a, b.lhs), opfunc_ab(a, b.rhs))
        elif isinstance(a, Equation) and isinstance(b, Equation):
            return Equation(opfunc_ab(a.lhs, b.lhs), opfunc_ab(a.rhs, b.rhs))
        else:
            return NotImplemented

    def __add__(self, other):
        return self._binary_op(self, other, lambda a, b: a + b)

    def __radd__(self, other):
        return self._binary_op(other, self, lambda a, b: a + b)

    def __mul__(self, other):
        return self._binary_op(self, other, lambda a, b: a * b)

    def __rmul__(self, other):
        return self._binary_op(other, self, lambda a, b: a * b)

    def __sub__(self, other):
        return self._binary_op(self, other, lambda a, b: a - b)

    def __rsub__(self, other):
        return self._binary_op(other, self, lambda a, b: a - b)

    def __truediv__(self, other):
        return self._binary_op(self, other, lambda a, b: a / b)

    def __rtruediv__(self, other):
        return self._binary_op(other, self, lambda a, b: a / b)

    def __mod__(self, other):
        return self._binary_op(self, other, lambda a, b: a % b)

    def __rmod__(self, other):
        return self._binary_op(other, self, lambda a, b: a % b)

    def __pow__(self, other):
        return self._binary_op(self, other, lambda a, b: a ** b)

    def __rpow__(self, other):
        return self._binary_op(other, self, lambda a, b: a ** b)

    def _eval_power(self, other):
        return self.__pow__(other)

    #####
    # Operation helper functions
    #####
    def expand(self, *args, **kwargs):
        return Equation(self.lhs.expand(*args, **kwargs), self.rhs.expand(
            *args, **kwargs))

    def simplify(self, *args, **kwargs):
        return self._eval_simplify(*args, **kwargs)

    def _eval_simplify(self, *args, **kwargs):
        return Equation(self.lhs.simplify(*args, **kwargs), self.rhs.simplify(
            *args, **kwargs))

    def _eval_factor(self, *args, **kwargs):
        # TODO: cancel out factors common to both sides.
        return Equation(self.lhs.factor(*args, **kwargs), self.rhs.factor(
            *args, **kwargs))

    def factor(self, *args, **kwargs):
        return self._eval_factor(*args, **kwargs)

    def _eval_collect(self, *args, **kwargs):
        from sympy.simplify.radsimp import collect
        return Equation(collect(self.lhs, *args, **kwargs),
                        collect(self.rhs, *args, **kwargs))

    def collect(self, *args, **kwargs):
        return self._eval_collect(*args, **kwargs)

    def evalf(self, *args, **kwargs):
        return Equation(self.lhs.evalf(*args, **kwargs),
                        self.rhs.evalf(*args, **kwargs))

    n = evalf

    def _eval_derivative(self, *args, **kwargs):
        # TODO Find why diff and Derivative do not appear to pass through
        #  kwargs to this. Since we cannot set evaluation of lhs manually
        #  try to be intelligent about when to do it.
        from sympy.core.function import Derivative
        eval_lhs = False
        if not (isinstance(self.lhs, Derivative)):
            for sym in args:
                if sym in self.lhs.free_symbols and not (
                        _sympify(sym).is_number):
                    eval_lhs = True
        return Equation(self.lhs.diff(*args, **kwargs, evaluate=eval_lhs),
                        self.rhs.diff(*args, **kwargs))

    def _eval_Integral(self, *args, **kwargs):
        side = kwargs.pop('side', None)  # Could not seem to pass values for
        # `evaluate` through to here.
        if side is None:
            raise ValueError('You must specify `side="lhs"` or `side="rhs"` '
                             'when integrating an Equation')
        else:
            try:
                return (getattr(self, side).integrate(*args, **kwargs))
            except AttributeError:
                raise AttributeError('`side` must equal "lhs" or "rhs".')

    #####
    # Output helper functions
    #####
    def __repr__(self):
        repstr = 'Equation(%s, %s)' %(self.lhs.__repr__(), self.rhs.__repr__())
        # if algwsym_config.output.human_text:
        #     return self.__str__()
        return repstr

    def _latex(self, printer):
        tempstr = ''
        """
        if algwsym_config.output.show_code and not \
            algwsym_config.output.human_text:
            print('code version: '+ self.__repr__())
        """
        tempstr += printer._print(self.lhs)
        tempstr += '='
        tempstr += printer._print(self.rhs)
        namestr = self._get_eqn_name()
        if namestr !='' and algwsym_config.output.label:
            tempstr += '\\,\\,\\,\\,\\,\\,\\,\\,\\,\\,'
            tempstr += '(\\text{'+namestr+'})'
        return tempstr

    def __str__(self):
        tempstr = ''
        # if algwsym_config.output.show_code:
        #     human_text = algwsym_config.output.human_text
        #     algwsym_config.output.human_text=False
        #     tempstr += '\ncode version: '+self.__repr__() +'\n'
        #     algwsym_config.output.human_text=human_text
        tempstr += str(self.lhs) + ' = ' + str(self.rhs)
        namestr = self._get_eqn_name()
        if namestr != '' and algwsym_config.output.label:
            tempstr += '          (' + namestr + ')'
        return tempstr


Eqn = Equation
if ip and "text/latex" not in formatter.active_types:
    old = formatter.formatters['text/plain'].for_type(Eqn,
                                                __command_line_printing__)
    # print("For type Equation overriding plain text formatter = " + str(old))

def solve(f, *symbols, **flags):
    """
    Override of sympy `solve()`.

    If passed an expression and variable(s) to solve for it behaves
    almost the same as normal solve with `dict = True`, except that solutions
    are wrapped in a FiniteSet() to guarantee that the output will be pretty
    printed in Jupyter like environments.

    If passed an equation or equations it returns solutions as a
    `FiniteSet()` of solutions, where each solution is represented by an
    equation or set of equations.

    To get a Python `list` of solutions (pre-0.11.0 behavior) rather than a
    `FiniteSet` issue the command `algwsym_config.output.solve_to_list = True`.
    This also prevents pretty-printing in IPython and Jupyter.

    Examples
    --------
    >>> a, b, c, x, y = symbols('a b c x y', real = True)
    >>> import sys
    >>> sys.displayhook = __command_line_printing__ # set by default on normal initialization.
    >>> eq1 = Eqn(abs(2*x+y),3)
    >>> eq2 = Eqn(abs(x + 2*y),3)
    >>> B = solve((eq1,eq2))

    Default human readable output on command line
    >>> B
    {{x = -3, y = 3}, {x = -1, y = -1}, {x = 1, y = 1}, {x = 3, y = -3}}

    To get raw output turn off by setting
    >>> algwsym_config.output.human_text=False
    >>> B
    FiniteSet(FiniteSet(Equation(x, -3), Equation(y, 3)), FiniteSet(Equation(x, -1), Equation(y, -1)), FiniteSet(Equation(x, 1), Equation(y, 1)), FiniteSet(Equation(x, 3), Equation(y, -3)))

    Pre-0.11.0 behavior where a python list of solutions is returned
    >>> algwsym_config.output.solve_to_list = True
    >>> solve((eq1,eq2))
    [[Equation(x, -3), Equation(y, 3)], [Equation(x, -1), Equation(y, -1)], [Equation(x, 1), Equation(y, 1)], [Equation(x, 3), Equation(y, -3)]]
    >>> algwsym_config.output.solve_to_list = False # reset to default

    `algwsym_config.output.human_text = True` with
    `algwsym_config.output.how_code=True` shows both.
    In Jupyter-like environments `show_code=True` yields the Raw output and
    a typeset version. If `show_code=False` (the default) only the
    typeset version is shown in Jupyter.
    >>> algwsym_config.output.show_code=True
    >>> algwsym_config.output.human_text=True
    >>> B
    Code version: FiniteSet(FiniteSet(Equation(x, -3), Equation(y, 3)), FiniteSet(Equation(x, -1), Equation(y, -1)), FiniteSet(Equation(x, 1), Equation(y, 1)), FiniteSet(Equation(x, 3), Equation(y, -3)))
    {{x = -3, y = 3}, {x = -1, y = -1}, {x = 1, y = 1}, {x = 3, y = -3}}
    """
    from sympy.solvers.solvers import solve
    from sympy.sets.sets import FiniteSet
    from IPython.display import display
    newf =[]
    solns = []
    displaysolns = []
    contains_eqn = False
    if hasattr(f,'__iter__'):
        for k in f:
            if isinstance(k, Equation):
                newf.append(k.lhs-k.rhs)
                contains_eqn = True
            else:
                newf.append(k)
    else:
        if isinstance(f, Equation):
            newf.append(f.lhs - f.rhs)
            contains_eqn = True
        else:
            newf.append(f)
    flags['dict'] = True
    result = solve(newf, *symbols, **flags)
    if contains_eqn:
        if len(result[0]) == 1:
            for k in result:
                for key in k.keys():
                    val = k[key]
                    tempeqn = Eqn(key, val)
                    solns.append(tempeqn)
        else:
            for k in result:
                solnset = []
                for key in k.keys():
                    val = k[key]
                    tempeqn = Eqn(key, val)
                    solnset.append(tempeqn)
                if not algwsym_config.output.solve_to_list:
                    solnset = FiniteSet(*solnset)
                solns.append(solnset)
    else:
        solns = result
    if algwsym_config.output.solve_to_list:
        return list(solns)
    else:
        return FiniteSet(*solns)

def solveset(f, symbols, domain=sympy.Complexes):
    """
    Very experimental override of sympy solveset, which we hope will replace
    solve. Much is not working. It is not clear how to input a system of
    equations unless you directly select `linsolve`, etc...
    """
    from sympy.solvers import solveset as solve
    from IPython.display import display
    newf = []
    solns = []
    displaysolns = []
    contains_eqn = False
    if hasattr(f, '__iter__'):
        for k in f:
            if isinstance(k, Equation):
                newf.append(k.lhs - k.rhs)
                contains_eqn = True
            else:
                newf.append(k)
    else:
        if isinstance(f, Equation):
            newf.append(f.lhs - f.rhs)
            contains_eqn = True
        else:
            newf.append(f)
    result = solve(*newf, symbols, domain=domain)
    # if contains_eqn:
    #     if len(result[0]) == 1:
    #         for k in result:
    #             for key in k.keys():
    #                 val = k[key]
    #                 tempeqn = Eqn(key, val)
    #                 solns.append(tempeqn)
    #         display(*solns)
    #     else:
    #         for k in result:
    #             solnset = []
    #             displayset = []
    #             for key in k.keys():
    #                 val = k[key]
    #                 tempeqn = Eqn(key, val)
    #                 solnset.append(tempeqn)
    #                 if algwsym_config.output.show_solve_output:
    #                     displayset.append(tempeqn)
    #             if algwsym_config.output.show_solve_output:
    #                 displayset.append('-----')
    #             solns.append(solnset)
    #             if algwsym_config.output.show_solve_output:
    #                 for k in displayset:
    #                     displaysolns.append(k)
    #         if algwsym_config.output.show_solve_output:
    #             display(*displaysolns)
    # else:
    solns = result
    return solns

def sqrt(arg, evaluate = None):
    """
    Override of sympy convenience function `sqrt`. Simply divides equations
    into two sides if `arg` is an instance of `Equation`. This avoids an
    issue with the way sympy is delaying specialized applications of _Pow_ on
    objects that are not basic sympy expressions.
    """
    from sympy.functions.elementary.miscellaneous import sqrt as symsqrt
    if isinstance(arg, Equation):
        return Equation(symsqrt(arg.lhs, evaluate), symsqrt(arg.rhs, evaluate))
    else:
        return symsqrt(arg,evaluate)

# Pick up the docstring for sqrt from sympy
from sympy.functions.elementary.miscellaneous import sqrt as symsqrt
sqrt.__doc__+=symsqrt.__doc__
del symsqrt

def root(arg, n, k = 0, evaluate = None):
    """
    Override of sympy convenience function `root`. Simply divides equations
    into two sides if `arg`  or `n` is an instance of `Equation`. This
    avoids an issue with the way sympy is delaying specialized applications
    of _Pow_ on objects that are not basic sympy expressions.
    """
    from sympy.functions.elementary.miscellaneous import root as symroot
    if isinstance(arg, Equation):
        return Equation(symroot(arg.lhs, n, k, evaluate),
                        symroot(arg.rhs, n, k, evaluate))
    if isinstance(n, Equation):
        return Equation(symroot(arg, n.lhs, k, evaluate),
                        symroot(arg, n.rhs, k, evaluate))
    else:
        return symroot(arg, n, k, evaluate)

# pick up the docstring for root from sympy
from sympy.functions.elementary.miscellaneous import root as symroot
root.__doc__+=symroot.__doc__
del symroot

def Heaviside(arg, **kwargs):
    """
    Overide of the Heaviside function as implemented in Sympy. Get a recursion
    error if use the normal class extension of a function to do this.

    """
    from sympy.functions.special.delta_functions import Heaviside as symHeav
    if isinstance(arg, Equation):
        return Equation(symHeav((arg.lhs), **kwargs),symHeav((arg.rhs),
                                                             **kwargs))
    else:
        return symHeav(arg, **kwargs)
# Pick up the docstring for Heaviside from Sympy.
from sympy.functions.special.delta_functions import Heaviside as symHeav
Heaviside.__doc__ += symHeav.__doc__
del symHeav

def collect(expr, syms, func=None, evaluate=None, exact=False,
            distribute_order_term=True):
    """
    Override of sympy `collect()`.
    """
    from sympy.simplify.radsimp import collect
    _eval_collect = getattr(expr, '_eval_collect', None)
    if _eval_collect is not None:
        return _eval_collect(syms, func, evaluate,
                             exact, distribute_order_term)
    else:
        return collect(expr, syms, func, evaluate, exact,
                       distribute_order_term)

class Equality(Equality):
    """
    Extension of Equality class to include the ability to convert it to an
    Equation.
    """
    def to_Equation(self):
        """
        Return: recasts the Equality as an Equation.
        """
        return Equation(self.lhs,self.rhs)

    def to_Eqn(self):
        """
        Synonym for to_Equation.
        Return: recasts the Equality as an Equation.
        """
        return self.to_Equation()

Eq = Equality

def __FiniteSet__repr__override__(self):
    """Override of the `FiniteSet.__repr__(self)` to overcome sympy's
    inconsistent wrapping of Finite Sets which prevents reliable use of
    copy and paste of the code representation.
    """
    insidestr = ""
    for k in self.args:
        insidestr += k.__repr__() +', '
    insidestr = insidestr[:-2]
    reprstr = "FiniteSet("+ insidestr + ")"
    return reprstr

sympy.sets.FiniteSet.__repr__ = __FiniteSet__repr__override__

def __FiniteSet__str__override__(self):
    """Override of the `FiniteSet.__str__(self)` to overcome sympy's
    inconsistent wrapping of Finite Sets which prevents reliable use of
    copy and paste of the code representation.
    """
    insidestr = ""
    for k in self.args:
        insidestr += str(k) + ', '
    insidestr = insidestr[:-2]
    strrep = "{"+ insidestr + "}"
    return strrep

sympy.sets.FiniteSet.__str__ = __FiniteSet__str__override__

#####
# Extension of the Function class. For incorporation into SymPy this should
# become part of the class
#####
class EqnFunction(Function):
    """
    Extension of the sympy Function class to understand equations. Each
    sympy function impacted by this extension is listed in the documentation
    that follows.
    """
    def __new__(cls, *args, **kwargs):
        n = len(args)
        eqnloc = None
        neqns = 0
        newargs = []
        for k in args:
            newargs.append(k)
        if (n > 0):
            for i in range(n):
                if isinstance(args[i], Equation):
                    neqns += 1
                    eqnloc = i
            if neqns > 1:
                raise NotImplementedError('Function calls with more than one '
                                          'Equation as a parameter are not '
                                          'supported. You may be able to get '
                                          'your desired outcome using .applyrhs'
                                          ' and .applylhs.')
            if neqns == 1:
                newargs[eqnloc] = args[eqnloc].lhs
                lhs = super().__new__(cls, *newargs, **kwargs)
                newargs[eqnloc] = args[eqnloc].rhs
                rhs = super().__new__(cls, *newargs, **kwargs)
                return Equation(lhs,rhs)
        return super().__new__(cls, *args, **kwargs)

def str_to_extend_sympy_func(func:str):
    """
    Generates the string command to execute for a sympy function to
    gain the properties of the extended EqnFunction class.
    """
    execstr = 'class ' + str(func) + '(' + str(
        func) + ',EqnFunction):\n    ' \
                'pass\n'
    return execstr

# TODO: Below will not be needed when incorporated into SymPy.
# This is hacky, but I have not been able to come up with another way
# of extending the functions programmatically, if this is separate package
# from sympy that extends it after loading sympy.
#  Functions listed in `skip` are not applicable to equations or cannot be
#  extended because of `mro` error or `metaclass conflict`. This reflects
#  that some of these are not members of the Sympy Function class.

# Overridden elsewhere
_extended_ = ('sqrt', 'root', 'Heaviside')

# Either not applicable to equations or have not yet figured out a way
# to systematically apply to an equation.
# TODO examine these more carefully (top priority: real_root, cbrt, Ynm_c).
_not_applicable_to_equations_ = ('Min', 'Max', 'Id', 'real_root', 'cbrt',
        'unbranched_argument', 'polarify', 'unpolarify',
        'piecewise_fold', 'E1', 'Eijk', 'bspline_basis',
        'bspline_basis_set', 'interpolating_spline', 'jn_zeros',
        'jacobi_normalized', 'Ynm_c', 'piecewise_exclusive', 'Piecewise',
        'motzkin', 'hyper','meijerg', 'chebyshevu_root', 'chebyshevt_root',
        'betainc_regularized')
_skip_ = _extended_ + _not_applicable_to_equations_

for func in functions.__all__:

    if func not in _skip_:
        try:
            exec(str_to_extend_sympy_func(func), globals(), locals())
        except TypeError:
            from warnings import warn
            warn('SymPy function/operation ' + str(func) + ' may not work ' \
                'properly with Equations. If you use it with Equations, ' \
                'validate its behavior. We are working to address this ' \
                'issue.')

# Redirect python abs() to Abs()
abs = Abs