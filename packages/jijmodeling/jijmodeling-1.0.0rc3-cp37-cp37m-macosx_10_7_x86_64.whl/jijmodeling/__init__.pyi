import typing, enum

@typing.final
class AbsOp:
    """
    A class for representing the absolute value
    
    The AbsOp class is used to represent the absolute value.
    The number of dimensions of the operand is zero.
    
    Attributes:
        operand: The operand.
    
    Note:
        The AbsOp class does not have a constructor.
    """
    def __new__(cls):
        pass

    def __add__(self, value, /):
        """
        Return self+value.
        """
        pass


    def __mod__(self, value, /):
        """
        Return self%value.
        """
        pass


    def __mul__(self, value, /):
        """
        Return self*value.
        """
        pass


    def __neg__(self, /):
        """
        -self
        """
        pass


    def __pow__(self, value, mod=None, /):
        """
        Return pow(self, value, mod).
        """
        pass


    def __radd__(self, value, /):
        """
        Return value+self.
        """
        pass


    def __rmod__(self, value, /):
        """
        Return value%self.
        """
        pass


    def __rmul__(self, value, /):
        """
        Return value*self.
        """
        pass


    def __rpow__(self, value, mod=None, /):
        """
        Return pow(value, self, mod).
        """
        pass


    def __rsub__(self, value, /):
        """
        Return value-self.
        """
        pass


    def __rtruediv__(self, value, /):
        """
        Return value/self.
        """
        pass


    def __sub__(self, value, /):
        """
        Return self-value.
        """
        pass


    def __truediv__(self, value, /):
        """
        Return self/value.
        """
        pass


    def _repr_latex_(self, /):
        """
        
        """
        pass


    operand: typing.Any
    def set_latex(self, /, latex=None):
        """
        Set the LaTeX representation of the object.
        If the LaTeX representation is not set, the default representation is set.
        
        Args:
            latex (str, optional): LaTeX representation of the object. Defaults to None.
        """
        pass


@typing.final
class AddOp:
    """
    A class for representing addition
    
    The AddOp class is used to represent addition (`+`) of an arbitrary number of operands.
    For example `a + b + c + d` would be one AddOp object.
    The number of dimensions of each operand is zero.
    
    Attributes:
        terms: A sequence of operands to be added.
    
    Note:
        The AddOp class does not have a constructor. Its intended
        instantiation method is by calling the addition operation on other
        expressions.
    """
    def __new__(cls):
        pass

    def __add__(self, value, /):
        """
        Return self+value.
        """
        pass


    def __mod__(self, value, /):
        """
        Return self%value.
        """
        pass


    def __mul__(self, value, /):
        """
        Return self*value.
        """
        pass


    def __neg__(self, /):
        """
        -self
        """
        pass


    def __pow__(self, value, mod=None, /):
        """
        Return pow(self, value, mod).
        """
        pass


    def __radd__(self, value, /):
        """
        Return value+self.
        """
        pass


    def __rmod__(self, value, /):
        """
        Return value%self.
        """
        pass


    def __rmul__(self, value, /):
        """
        Return value*self.
        """
        pass


    def __rpow__(self, value, mod=None, /):
        """
        Return pow(value, self, mod).
        """
        pass


    def __rsub__(self, value, /):
        """
        Return value-self.
        """
        pass


    def __rtruediv__(self, value, /):
        """
        Return value/self.
        """
        pass


    def __sub__(self, value, /):
        """
        Return self-value.
        """
        pass


    def __truediv__(self, value, /):
        """
        Return self/value.
        """
        pass


    def _repr_latex_(self, /):
        """
        
        """
        pass


    def set_latex(self, /, latex=None):
        """
        Set the LaTeX representation of the object.
        If the LaTeX representation is not set, the default representation is set.
        
        Args:
            latex (str, optional): LaTeX representation of the object. Defaults to None.
        """
        pass


    terms: typing.Any
@typing.final
class AndOp:
    """
    A class for representing logical AND
    
    The AndOp class is used to represent logical AND (`&`) of an arbitrary number of operands.
    For example `a & b & c & d` would be one AndOp object.
    The number of dimensions of each operand is zero.
    
    Attributes:
        terms: A sequence of operands to apply the AND operation.
    
    Note:
        The AndOp class does not have a constructor.
    """
    def __new__(cls):
        pass

    def __and__(self, value, /):
        """
        Return self&value.
        """
        pass


    def __or__(self, value, /):
        """
        Return self|value.
        """
        pass


    def __rand__(self, value, /):
        """
        Return value&self.
        """
        pass


    def __ror__(self, value, /):
        """
        Return value|self.
        """
        pass


    def __rxor__(self, value, /):
        """
        Return value^self.
        """
        pass


    def __xor__(self, value, /):
        """
        Return self^value.
        """
        pass


    def _repr_latex_(self, /):
        """
        
        """
        pass


    def set_latex(self, /, latex=None):
        """
        Set the LaTeX representation of the object.
        If the LaTeX representation is not set, the default representation is set.
        
        Args:
            latex (str, optional): LaTeX representation of the object. Defaults to None.
        """
        pass


    terms: typing.Any
@typing.final
class ArrayLength:
    """
    A class for referring to the length of an array at a given axis.
    
    The ArrayLength class is to refer to the number of elements of an axis in an array.
    
    This class is not intended to be instantiated directly. Instead, you can use
    the `len_at` method in of `Placeholder`, `Element` or `Subscript`.
    
    Attributes:
        array: A variable with `ndim >= 1`.
        axis: An axis index. A $n$-dimensional variable has $n$ axes. Axis 0 is the array's outermost axis and $n-1$ is the innermost.
        description (str, optional): A description of the ArrayLength instance.
    
    Raises:
        ModelingError: Raises if `axis` >= `array.ndim`.
    
    Examples:
        Create a length of axis 0 in a 2-dimensional placeholder.
    
        >>> import jijmodeling as jm
        >>> a = jm.Placeholder("a", ndim=2)
        >>> N = a.len_at(0, latex="N")
    """
    def __new__(cls):
        pass

    def __add__(self, value, /):
        """
        Return self+value.
        """
        pass


    def __mod__(self, value, /):
        """
        Return self%value.
        """
        pass


    def __mul__(self, value, /):
        """
        Return self*value.
        """
        pass


    def __neg__(self, /):
        """
        -self
        """
        pass


    def __pow__(self, value, mod=None, /):
        """
        Return pow(self, value, mod).
        """
        pass


    def __radd__(self, value, /):
        """
        Return value+self.
        """
        pass


    def __rmod__(self, value, /):
        """
        Return value%self.
        """
        pass


    def __rmul__(self, value, /):
        """
        Return value*self.
        """
        pass


    def __rpow__(self, value, mod=None, /):
        """
        Return pow(value, self, mod).
        """
        pass


    def __rsub__(self, value, /):
        """
        Return value-self.
        """
        pass


    def __rtruediv__(self, value, /):
        """
        Return value/self.
        """
        pass


    def __sub__(self, value, /):
        """
        Return self-value.
        """
        pass


    def __truediv__(self, value, /):
        """
        Return self/value.
        """
        pass


    def _repr_latex_(self, /):
        """
        
        """
        pass


    array: typing.Any
    axis: typing.Any
    description: str
    def set_latex(self, /, latex=None):
        """
        Set the LaTeX representation of the object.
        If the LaTeX representation is not set, the default representation is set.
        
        Args:
            latex (str, optional): LaTeX representation of the object. Defaults to None.
        """
        pass


@typing.final
class BinaryVar:
    """
    A class for creating a binary variable
    
    The BinaryVar class is used to create a binary variable.
    
    The index operator (`[]`) of a binary variable with `ndim >= 1` returns a :obj:`Subscript` object.
    
    Attributes:
        name (str): A name of the binary variable.
        shape (tuple): A tuple with the size of each dimension of the binary variable. Empty if the variable is not multi-dimensional.
        description (str): A description of the binary variable.
    
    Args:
        name (str): A name of the binary variable.
        shape (list/tuple): A sequence with the size of each dimension of the binary variable. Defaults to an empty tuple (a scalar value).
            Each item in :obj:`shape` must be a valid expression evaluating to a non-negative scalar.
        latex (str, optional): A LaTeX-name of the binary variable to be represented in Jupyter notebook.
            It is set to :obj:`name` by default.
        description (str, optional): A description of the binary variable.
    
    Examples:
        Create a scalar binary variable whose name is "z".
    
        >>> import jijmodeling as jm
        >>> z = jm.BinaryVar("z")
    
        Create a 2-dimensional binary variable whose name is "x" and has a 2x2 shape.
    
        >>> import jijmodeling as jm
        >>> x = jm.BinaryVar("x", shape=[2, 2])
    
        Create a 1-dimensional binary variable with the index of `123`.
    
        >>> import jijmodeling as jm
        >>> x = jm.BinaryVar("x", shape=[124])
        >>> x[123]
        BinaryVar(name='x', shape=[NumberLit(value=124)])[NumberLit(value=123)]
    """
    def __new__(cls, name: str, *, shape=None, latex=None, description=None):
        pass

    def __add__(self, value, /):
        """
        Return self+value.
        """
        pass


    def __getitem__(self, key, /):
        """
        Return self[key].
        """
        pass


    def __mul__(self, value, /):
        """
        Return self*value.
        """
        pass


    def __neg__(self, /):
        """
        -self
        """
        pass


    def __pow__(self, value, mod=None, /):
        """
        Return pow(self, value, mod).
        """
        pass


    def __radd__(self, value, /):
        """
        Return value+self.
        """
        pass


    def __rmul__(self, value, /):
        """
        Return value*self.
        """
        pass


    def __rpow__(self, value, mod=None, /):
        """
        Return pow(value, self, mod).
        """
        pass


    def __rsub__(self, value, /):
        """
        Return value-self.
        """
        pass


    def __sub__(self, value, /):
        """
        Return self-value.
        """
        pass


    def _repr_latex_(self, /):
        """
        
        """
        pass


    description: str
    name: str
    ndim: int
    def set_latex(self, /, latex=None):
        """
        Set the LaTeX representation of the object.
        If the LaTeX representation is not set, the default representation is set.
        
        Args:
            latex (str, optional): LaTeX representation of the object. Defaults to None.
        """
        pass


    shape: tuple
@typing.final
class CeilOp:
    """
    A class for representing the ceil operator
    
    The CeilOp class is used to represent the ceil operator.
    The number of dimensions of the operand is zero.
    
    Attributes:
        operand: The operand.
    
    Note:
        The CeilOp class does not have a constructor.
    """
    def __new__(cls):
        pass

    def __add__(self, value, /):
        """
        Return self+value.
        """
        pass


    def __mod__(self, value, /):
        """
        Return self%value.
        """
        pass


    def __mul__(self, value, /):
        """
        Return self*value.
        """
        pass


    def __neg__(self, /):
        """
        -self
        """
        pass


    def __pow__(self, value, mod=None, /):
        """
        Return pow(self, value, mod).
        """
        pass


    def __radd__(self, value, /):
        """
        Return value+self.
        """
        pass


    def __rmod__(self, value, /):
        """
        Return value%self.
        """
        pass


    def __rmul__(self, value, /):
        """
        Return value*self.
        """
        pass


    def __rpow__(self, value, mod=None, /):
        """
        Return pow(value, self, mod).
        """
        pass


    def __rsub__(self, value, /):
        """
        Return value-self.
        """
        pass


    def __rtruediv__(self, value, /):
        """
        Return value/self.
        """
        pass


    def __sub__(self, value, /):
        """
        Return self-value.
        """
        pass


    def __truediv__(self, value, /):
        """
        Return self/value.
        """
        pass


    def _repr_latex_(self, /):
        """
        
        """
        pass


    operand: typing.Any
    def set_latex(self, /, latex=None):
        """
        Set the LaTeX representation of the object.
        If the LaTeX representation is not set, the default representation is set.
        
        Args:
            latex (str, optional): LaTeX representation of the object. Defaults to None.
        """
        pass


@typing.final
class Constraint:
    """
    A class for creating a constraint
    
    The Constraint class is used to create a constraint.
    
    Attributes:
        name (str): A name of the constraint.
        sense: equal sign (=) or inequality sign (>= or <=) included in the expression.
        expression: The (in)equality equation of the constraint.
        forall (list): A list that stores forall indices.
    
    Args:
        name (str): A name of the constraint.
        expression: The (in)equality equation of the constraint.
        forall: A list that stores forall indices. Defaults to None.
    
    Raises:
        ModelingError: Raises if `expression` does not contain any decision variable.
    
    Expression:
        Create an equality constraint that the sum of $N$ binary variables is equal to one.
    
        >>> import jijmodeling as jm
        >>> N = jm.Placeholder("N")
        >>> i = jm.Element("i", belong_to=N)
        >>> x = jm.BinaryVar("x", shape=(N,))
        >>> jm.Constraint("constraint", jm.sum(i, x[i]) == 1)
        {'expression': sum(i in [0..N), x[i]) == 1}
    
        Create an inequality constraint with forall.
    
        >>> import jijmodeling as jm
        >>> N = jm.Placeholder("N")
        >>> i = jm.Element("i", belong_to=N)
        >>> j = jm.Element("j", belong_to=N)
        >>> x = jm.BinaryVar("x", shape=(N, N))
        >>> jm.Constraint("constraint", jm.sum(i, x[i,j]) == 1, forall=j)
        {'expression': sum(i in [0..N), x[i, j]) == 1, 'forall': [j]}
    
        Create an inequality constraint with conditional forall.
    
        >>> import jijmodeling as jm
        >>> N = jm.Placeholder("N")
        >>> i = jm.Element("i", belong_to=N)
        >>> j = jm.Element("j", belong_to=N)
        >>> x = jm.BinaryVar("x", shape=(N, N))
        >>> jm.Constraint("constraint", x[i,j] <= 2, forall=[i, (j, j != i)])
        {'expression': x[i, j] <= 2, 'forall': [i, (j, j != i)]}
        
    """
    def __new__(cls, name: str, expression, *, forall=None):
        pass

    def _repr_latex_(self, /):
        """
        
        """
        pass


    expression: typing.Any
    forall: typing.Any
    def is_equality(self, /):
        """
        Returns true if the constraint is an equality constraint.
        
        Returns:
            bool: True if the constraint is an equality constraint. Otherwise, False.
        
        Examples:
            >>> import jijmodeling as jm
            >>> N = jm.Placeholder("N")
            >>> i = jm.Element("i", belong_to=N)
            >>> x = jm.BinaryVar("x", shape=(N,))
            >>> constraint = jm.Constraint("constraint", jm.sum(i, x[i]) == 1)
            >>> assert constraint.is_equality()
        """
        pass


    def is_inequality(self, /):
        """
        Returns true if the constraint is an inequality constraint.
        
        Returns:
            bool: True if the constraint is an inequality constraint. Otherwise, False.
        
        Examples:
            >>> import jijmodeling as jm
            >>> N = jm.Placeholder("N")
            >>> i = jm.Element("i", belong_to=N)
            >>> x = jm.BinaryVar("x", shape=(N,))
            >>> constraint = jm.Constraint("constraint", jm.sum(i, x[i]) <= 1)
            >>> assert constraint.is_inequality()
        """
        pass


    left: typing.Any
    name: str
    right: typing.Any
    sense: typing.Any
@typing.final
class ConstraintSense:
    """
    Equality of a constraint
    """
    def __new__(cls):
        pass

    EQUAL: ConstraintSense
    GREATER_THAN_EQUAL: ConstraintSense
    LESS_THAN_EQUAL: ConstraintSense
@typing.final
class ContinuousVar:
    """
    A class for creating a continuous variable
    
    The ContinuousVar class is used to create a continuous variable.
    The lower and upper bounds of the variable can be specified by:
    - an integer value
    - a float value
    - a scalar expression that does not contains any decision variable
    - a Placeholder object whose dimensionality is equal to that of this variable.
    - a subscripted variable whose dimensionality is equal to that of this variable.
    
    The index operator (`[]`) of a variable with `ndim >= 1` returns a :obj:`Subscript` object.
    
    Attributes:
        name (str): A name of the continuous variable.
        shape (tuple): A tuple with the size of each dimension of the integer variable. Empty if the variable is not multi-dimensional.
        lower_bound: The lower bound of the variable.
        upper_bound: The upper bound of the variable.
        description (str): A description of the continuous variable.
    
    Args:
        name (str): A name of the continuous variable.
        shape (list/tuple): A sequence with the size of each dimension of the continuous variable. Defaults to an empty tuple (a scalar value).
            Each item in :obj:`shape` must be a valid expression evaluating to a non-negative scalar.
        lower_bound: The lower bound of the variable.
        upper_bound: The upper bound of the variable.
        latex (str, optional): A LaTeX-name of the continuous variable to be represented in Jupyter notebook.
            It is set to :obj:`name` by default.
        description (str, optional): A description of the continuous variable.
    
    Raises:
        ModelingError: Raises if a bound is a `Placeholder` or `Subscript` object whose `ndim` is neither `0` nor the same value as `ndim` of the continuous variable.
    
    Examples:
        Create a scalar continuous variable whose name is "z" and domain is [-1, 1].
    
        >>> import jijmodeling as jm
        >>> z = jm.ContinuousVar("z", lower_bound=-1, upper_bound=1)
    
        Create a 2-dimensional continuous variable...
        - whose name is "x".
        - whose domain is [0, 2].
        - where each dimension has length 2 (making this a 2x2 matrix).
    
        >>> import jijmodeling as jm
        >>> x = jm.ContinuousVar("x", shape=[2, 2], lower_bound=0, upper_bound=2)
    
        Create a 1-dimensional continuous variable with the index of `123`.
    
        >>> import jijmodeling as jm
        >>> x = jm.ContinuousVar("x", shape=[124], lower_bound=0, upper_bound=2)
        >>> x[123]
        ContinuousVar(name='x', shape=[NumberLit(value=124)], lower_bound=NumberLit(value=0), upper_bound=NumberLit(value=2))[NumberLit(value=123)]
    """
    def __new__(cls, name: str, *, shape=None, lower_bound, upper_bound, latex=None, description=None):
        pass

    def __add__(self, value, /):
        """
        Return self+value.
        """
        pass


    def __getitem__(self, key, /):
        """
        Return self[key].
        """
        pass


    def __mul__(self, value, /):
        """
        Return self*value.
        """
        pass


    def __neg__(self, /):
        """
        -self
        """
        pass


    def __pow__(self, value, mod=None, /):
        """
        Return pow(self, value, mod).
        """
        pass


    def __radd__(self, value, /):
        """
        Return value+self.
        """
        pass


    def __rmul__(self, value, /):
        """
        Return value*self.
        """
        pass


    def __rpow__(self, value, mod=None, /):
        """
        Return pow(value, self, mod).
        """
        pass


    def __rsub__(self, value, /):
        """
        Return value-self.
        """
        pass


    def __sub__(self, value, /):
        """
        Return self-value.
        """
        pass


    def _repr_latex_(self, /):
        """
        
        """
        pass


    description: str
    lower_bound: typing.Any
    name: str
    ndim: int
    def set_latex(self, /, latex=None):
        """
        Set the LaTeX representation of the object.
        If the LaTeX representation is not set, the default representation is set.
        
        Args:
            latex (str, optional): LaTeX representation of the object. Defaults to None.
        """
        pass


    shape: tuple
    upper_bound: typing.Any
@typing.final
class CustomPenaltyTerm:
    """
    A class for creating a custom penalty term
    
    The CustomPenaltyTerm class is used to create a custom penalty term.
    
    Attributes:
        name (str): A name of the custom penalty term.
        expression: The expression of the custom penalty term.
        forall (list): A list that stores forall indices.
    
    Args:
        name (str): A name of the custom penalty term.
        expression: The expression of the custom penalty term.
        forall: A list that stores forall indices. Defaults to None.
    
    Raises:
        ModelingError: Raises if `expression` does not contain any decision variable.
    
    Expression:
        Create a custom penalty term.
    
        >>> import jijmodeling as jm
        >>> N = jm.Placeholder("N")
        >>> i = jm.Element("i", belong_to=N)
        >>> x = jm.BinaryVar("x", shape=(N,))
        >>> jm.CustomPenaltyTerm("custom penalty term", (jm.sum(i, x[i]) - 1)**2)  # doctest: +ELLIPSIS
        <jijmodeling.CustomPenaltyTerm object at 0x...>
    
        Create a custom penalty term with forall.
    
        >>> import jijmodeling as jm
        >>> N = jm.Placeholder("N")
        >>> i = jm.Element("i", belong_to=N)
        >>> j = jm.Element("j", belong_to=N)
        >>> x = jm.BinaryVar("x", shape=(N, N))
        >>> jm.CustomPenaltyTerm("custom penalty term", (jm.sum(i, x[i,j]) - 1)**2, forall=j)  # doctest: +ELLIPSIS
        <jijmodeling.CustomPenaltyTerm object at 0x...>
    
        Create a custom penalty term with conditional forall.
    
        >>> import jijmodeling as jm
        >>> N = jm.Placeholder("N")
        >>> i = jm.Element("i", belong_to=N)
        >>> j = jm.Element("j", belong_to=N)
        >>> x = jm.BinaryVar("x", shape=(N, N))
        >>> jm.CustomPenaltyTerm("custom penalty term", (x[i,j] - 2)**2, forall=[i, (j, j != i)])  # doctest: +ELLIPSIS
        <jijmodeling.CustomPenaltyTerm object at 0x...>
    """
    def __new__(cls, name: str, expression, *, forall=None):
        pass

    def _repr_latex_(self, /):
        """
        
        """
        pass


    expression: typing.Any
    forall: typing.Any
    name: str
@typing.final
class DataType:
    """
    
    """
    def __new__(cls):
        pass

    FLOAT: DataType
    INTEGER: DataType
@typing.final
class DummyIndexedVar:
    """
    A class for representing a subscripted variable with dummy indices
    
    The DummyIndexedVar class is an intermediate representation to support syntactic sugar of sum/prod with slices.
    
    Note:
        The DummyIndexedVar class does not have a constructor.
    """
    def __new__(cls):
        pass

    def prod(self, /):
        """
        Take a prod of the decision variable over the elements for which the slice is given and return a ProdOp object.
        
        Returns:
            ProdOp: A ProdOp object taken a prod of the decision variable over the elements for which the slice is given.
        
        Note:
            An automatically created dummy index
            - has a name of the form `__dummy_{decision_var.name}_{axis}` where `axis` is the axis of the slice.
            - belongs to a range whose start defaults to 0 and end defaults to the length of the axis.
            - has description of the form `dummy index at {axis} for {decision_var.name}`.
            - has latex string of the form `\\ast_{axis}`.
        
        Examples:
            Create a prodOp object taken a prod of the 2-dim binary variable over the 0-th elements for which the slice is given.
        
            >>> import jijmodeling as jm
            >>> n = jm.Placeholder("n")
            >>> x = jm.BinaryVar("x", shape=(n, n))
            >>> i = jm.Element("__dummy_x_0", belong_to=n)
            >>> j = jm.Element("j", belong_to=n)
            >>> assert jm.is_same(x[:, j].prod(), jm.prod(i, x[i, j]))
        """
        pass


    def sum(self, /):
        """
        Take a sum of the decision variable over the elements for which the slice is given and return a SumOp object.
        
        Returns:
            SumOp: A SumOp object taken a sum of the decision variable over the elements for which the slice is given.
        
        Note:
            An automatically created dummy index
            - has a name of the form `__dummy_{decision_var.name}_{axis}` where `axis` is the axis of the slice.
            - belongs to a range whose start defaults to 0 and end defaults to the length of the axis.
            - has description of the form `dummy index at {axis} for {decision_var.name}`.
            - has latex string of the form `\\ast_{axis}`.
        
        Examples:
            Create a SumOp object taken a sum of the 2-dim binary variable over the 0-th elements for which the slice is given.
        
            >>> import jijmodeling as jm
            >>> n = jm.Placeholder("n")
            >>> x = jm.BinaryVar("x", shape=(n, n))
            >>> i = jm.Element("__dummy_x_0", belong_to=n)
            >>> j = jm.Element("j", belong_to=n)
            >>> assert jm.is_same(x[:, j].sum(), jm.sum(i, x[i, j]))
        """
        pass


@typing.final
class Element:
    """
    A class for creating an element
    
    The Element class is used to create an element.
    It is used in the following cases:
    - an index of summation $\displaystyle \sum$ (:obj:`SumOp`)
    - an index of product $\displaystyle \prod$ (:obj:`ProdOp`)
    - a bound variable of the universal quantifier $\forall$ (:obj:`Forall`)
    
    It has a set that it belongs to.
    There are two options for this set:
    1. A half-open range, where the lower bound is included and the upper bound is excluded
    2. A `Placeholder`, `Element`, or `Subscript` variable with `ndim` >= 1
    
    The index operator (`[]`) of an element with `ndim >= 1` returns a :obj:`Subscript` object.
    
    Attributes:
        name (str): A name of the element.
        ndim (int): The number of dimensions of the element. The value is one less than the value of `belong_to.ndim`.
        description (str): A description of the element.
        belong_to: A set the element belongs to.
    
    Args:
        name (str): A name of the element.
        belong_to: A set the element belongs to.
        latex (str, optional): A LaTeX-name of the element to be represented in Jupyter notebook.
            It is set to :obj:`name` by default.
        description (str, optional): A description of the element.
    
    Examples:
        Create an element that belongs to a half-open range.
    
        >>> import jijmodeling as jm
        >>> i = jm.Element("i", belong_to=(0,10))
    
        If you pass an object with `ndim` as the `belong_to` argument, the set that the element belongs to is a range with a start of 0 and an end of the object.
    
        >>> import jijmodeling as jm
        >>> i = jm.Element("i", belong_to=10)
        >>> assert jm.is_same(i, jm.Element("i", belong_to=(0,10)))
    
        Create an element that belongs to a 1-dimensional placeholder.
    
        >>> import jijmodeling as jm
        >>> E = jm.Placeholder("E", ndim=1)
        >>> e = jm.Element("e", belong_to=E)
    
        Create a 1-dimensional element with the index of `123`.
    
        >>> import jijmodeling as jm
        >>> a = jm.Placeholder("a", ndim=2)
        >>> e = jm.Element("e", belong_to=a)
        >>> e[123]
        Element(name='e', belong_to=Placeholder(name='a', ndim=2))[NumberLit(value=123)]
    """
    def __new__(cls, name: str, *, belong_to, latex=None, description=None):
        pass

    def __add__(self, value, /):
        """
        Return self+value.
        """
        pass


    def __getitem__(self, key, /):
        """
        Return self[key].
        """
        pass


    def __mod__(self, value, /):
        """
        Return self%value.
        """
        pass


    def __mul__(self, value, /):
        """
        Return self*value.
        """
        pass


    def __neg__(self, /):
        """
        -self
        """
        pass


    def __pow__(self, value, mod=None, /):
        """
        Return pow(self, value, mod).
        """
        pass


    def __radd__(self, value, /):
        """
        Return value+self.
        """
        pass


    def __rmod__(self, value, /):
        """
        Return value%self.
        """
        pass


    def __rmul__(self, value, /):
        """
        Return value*self.
        """
        pass


    def __rpow__(self, value, mod=None, /):
        """
        Return pow(value, self, mod).
        """
        pass


    def __rsub__(self, value, /):
        """
        Return value-self.
        """
        pass


    def __rtruediv__(self, value, /):
        """
        Return value/self.
        """
        pass


    def __sub__(self, value, /):
        """
        Return self-value.
        """
        pass


    def __truediv__(self, value, /):
        """
        Return self/value.
        """
        pass


    def _repr_latex_(self, /):
        """
        
        """
        pass


    belong_to: typing.Any
    description: str
    def len_at(self, /, axis, *, latex=None, description=None):
        """
        
        """
        pass


    name: str
    ndim: int
    def set_latex(self, /, latex=None):
        """
        Set the LaTeX representation of the object.
        If the LaTeX representation is not set, the default representation is set.
        
        Args:
            latex (str, optional): LaTeX representation of the object. Defaults to None.
        """
        pass


    shape: tuple
@typing.final
class EqualOp:
    """
    A class for representing the equal operator
    
    The EqualOp class is used to represent the equal operator (`==`).
    The number of dimensions of each operand is zero.
    
    Attributes:
        left: The left-hand operand.
        right: The right-hand operand.
    
    Note:
        The EqualOp class does not have a constructor.
    """
    def __new__(cls):
        pass

    def __and__(self, value, /):
        """
        Return self&value.
        """
        pass


    def __or__(self, value, /):
        """
        Return self|value.
        """
        pass


    def __rand__(self, value, /):
        """
        Return value&self.
        """
        pass


    def __ror__(self, value, /):
        """
        Return value|self.
        """
        pass


    def __rxor__(self, value, /):
        """
        Return value^self.
        """
        pass


    def __xor__(self, value, /):
        """
        Return self^value.
        """
        pass


    def _repr_latex_(self, /):
        """
        
        """
        pass


    left: typing.Any
    right: typing.Any
    def set_latex(self, /, latex=None):
        """
        Set the LaTeX representation of the object.
        If the LaTeX representation is not set, the default representation is set.
        
        Args:
            latex (str, optional): LaTeX representation of the object. Defaults to None.
        """
        pass


@typing.final
class Evaluation:
    """
    A class for evaluation.
    
    The Evaluation class is to represent the result of evaluating a model.
    
    Attributes:
        energy (numpy.ndarray): The value of energy of each sample.
        objective (numpy.ndarray): The value of an objective function of each sample.
        constraint_violations (dict[str, numpy.ndarray]): The constraint violation of each sample.
        constraint_forall (dict[str, numpy.ndarray]): The constraint forall of each sample.
        constraint_values (numpy.ndarray): The constraint value of each sample.
        penalty (dict[str, numpy.ndarray]): The penalty of each sample.
    """
    def __new__(cls, energy=Ellipsis, objective=Ellipsis, constraint_violations=Ellipsis, constraint_forall=Ellipsis, constraint_values=Ellipsis, penalty=Ellipsis):
        pass

    constraint_expr_values: typing.Any
    constraint_forall: typing.Any
    constraint_values: typing.Any
    constraint_violations: typing.Any
    energy: typing.Any
    @staticmethod
    def from_dict(dict):
        """
        Create a Evaluation object from the given dict.
        
        If a key is not the name of the Evaluation fields, the value value is ignored.
        
        Args:
            dict: A dict whose keys are name of the Evaluation fields.
        """
        pass


    @staticmethod
    def from_json(json):
        """
        Create a Evaluation object from the JSON string.
        
        Args:
            json (str): A JSON string.
        
        Returns:
            Evaluation: An Evaluation object.
        """
        pass


    objective: typing.Any
    penalty: typing.Any
    def to_dict(self, /):
        """
        Convert into a dict.
        
        Returns:
            dict: A dict whose keys are name of the Evaluation's fields.
        """
        pass


    def to_json(self, /):
        """
        Serialize the Evaluation object into a JSON string.
        
        Returns:
            str: A JSON string.
        
        Note:
            A numpy array is converted into a list.
        """
        pass


    def to_pandas(self, /):
        """
        Convert into a pandas DataFrame.
        
        Returns:
            pandas.DataFrame: A pandas DataFrame.
        """
        pass


@typing.final
class FloorOp:
    """
    A class for representing the floor operator
    
    The FloorOp class is used to represent the floor operator.
    The number of dimensions of the operand is zero.
    
    Attributes:
        operand: The operand.
    
    Note:
        The FloorOp class does not have a constructor.
    """
    def __new__(cls):
        pass

    def __add__(self, value, /):
        """
        Return self+value.
        """
        pass


    def __mod__(self, value, /):
        """
        Return self%value.
        """
        pass


    def __mul__(self, value, /):
        """
        Return self*value.
        """
        pass


    def __neg__(self, /):
        """
        -self
        """
        pass


    def __pow__(self, value, mod=None, /):
        """
        Return pow(self, value, mod).
        """
        pass


    def __radd__(self, value, /):
        """
        Return value+self.
        """
        pass


    def __rmod__(self, value, /):
        """
        Return value%self.
        """
        pass


    def __rmul__(self, value, /):
        """
        Return value*self.
        """
        pass


    def __rpow__(self, value, mod=None, /):
        """
        Return pow(value, self, mod).
        """
        pass


    def __rsub__(self, value, /):
        """
        Return value-self.
        """
        pass


    def __rtruediv__(self, value, /):
        """
        Return value/self.
        """
        pass


    def __sub__(self, value, /):
        """
        Return self-value.
        """
        pass


    def __truediv__(self, value, /):
        """
        Return self/value.
        """
        pass


    def _repr_latex_(self, /):
        """
        
        """
        pass


    operand: typing.Any
    def set_latex(self, /, latex=None):
        """
        Set the LaTeX representation of the object.
        If the LaTeX representation is not set, the default representation is set.
        
        Args:
            latex (str, optional): LaTeX representation of the object. Defaults to None.
        """
        pass


@typing.final
class GreaterThanEqualOp:
    """
    A class for representing the greater than equal operator
    
    The GreaterThanEqualOp class is used to represent the greater than equal operator (`>=`).
    The number of dimensions of each operand is zero.
    
    Attributes:
        left: The left-hand operand.
        right: The right-hand operand.
    
    Note:
        The GreaterThanEqualOp class does not have a constructor.
    """
    def __new__(cls):
        pass

    def __and__(self, value, /):
        """
        Return self&value.
        """
        pass


    def __or__(self, value, /):
        """
        Return self|value.
        """
        pass


    def __rand__(self, value, /):
        """
        Return value&self.
        """
        pass


    def __ror__(self, value, /):
        """
        Return value|self.
        """
        pass


    def __rxor__(self, value, /):
        """
        Return value^self.
        """
        pass


    def __xor__(self, value, /):
        """
        Return self^value.
        """
        pass


    def _repr_latex_(self, /):
        """
        
        """
        pass


    left: typing.Any
    right: typing.Any
    def set_latex(self, /, latex=None):
        """
        Set the LaTeX representation of the object.
        If the LaTeX representation is not set, the default representation is set.
        
        Args:
            latex (str, optional): LaTeX representation of the object. Defaults to None.
        """
        pass


@typing.final
class GreaterThanOp:
    """
    A class for representing the greater than operator
    
    The GreaterThanOp class is used to represent the greater than operator (`>`).
    The number of dimensions of each operand is zero.
    
    Attributes:
        left: The left-hand operand.
        right: The right-hand operand.
    
    Note:
        The GreaterThanOp class does not have a constructor.
    """
    def __new__(cls):
        pass

    def __and__(self, value, /):
        """
        Return self&value.
        """
        pass


    def __or__(self, value, /):
        """
        Return self|value.
        """
        pass


    def __rand__(self, value, /):
        """
        Return value&self.
        """
        pass


    def __ror__(self, value, /):
        """
        Return value|self.
        """
        pass


    def __rxor__(self, value, /):
        """
        Return value^self.
        """
        pass


    def __xor__(self, value, /):
        """
        Return self^value.
        """
        pass


    def _repr_latex_(self, /):
        """
        
        """
        pass


    left: typing.Any
    right: typing.Any
    def set_latex(self, /, latex=None):
        """
        Set the LaTeX representation of the object.
        If the LaTeX representation is not set, the default representation is set.
        
        Args:
            latex (str, optional): LaTeX representation of the object. Defaults to None.
        """
        pass


@typing.final
class IntegerVar:
    """
    A class for creating an integer variable
    
    The IntegerVar class is used to create an integer variable.
    The lower and upper bounds of the variable can be specified by:
    - an integer value
    - a float value
    - a scalar expression that does not contains any decision variable
    - a Placeholder object whose dimensionality is equal to that of this variable.
    - a subscripted variable whose dimensionality is equal to that of this variable.
    
    The index operator (`[]`) of a variable with `ndim >= 1` returns a :obj:`Subscript` object.
    
    Attributes:
        name (str): A name of the integer variable.
        shape (tuple): A tuple with the size of each dimension of the integer variable. Empty if the variable is not multi-dimensional.
        lower_bound: The lower bound of the variable.
        upper_bound: The upper bound of the variable.
        description (str): A description of the integer variable.
    
    Args:
        name (str): A name of the integer variable.
        shape (list/tuple): A sequence with the size of each dimension of the integer variable. Defaults to an empty tuple (a scalar value).
            Each item in :obj:`shape` must be a valid expression evaluating to a non-negative scalar.
        lower_bound: The lower bound of the variable.
        upper_bound: The upper bound of the variable.
        latex (str, optional): A LaTeX-name of the integer variable to be represented in Jupyter notebook.
            It is set to :obj:`name` by default.
        description (str, optional): A description of the integer variable.
    
    Raises:
        ModelingError: Raises if a bound is a `Placeholder` or `Subscript` object whose `ndim` is neither `0` nor the same value as `ndim` of the integer variable.
    
    Examples:
        Create a scalar integer variable whose name is "z" and domain is [-1, 1].
    
        >>> import jijmodeling as jm
        >>> z = jm.IntegerVar("z", lower_bound=-1, upper_bound=1)
    
        Create a 2-dimensional integer variable...
        - whose name is "x".
        - whose domain is [0, 2].
        - where each dimension has length 2 (making this a 2x2 matrix).
    
        >>> import jijmodeling as jm
        >>> x = jm.IntegerVar("x", shape=[2, 2], lower_bound=0, upper_bound=2)
    
        Create a 1-dimensional integer variable with the index of `123`.
    
        >>> import jijmodeling as jm
        >>> x = jm.IntegerVar("x", shape=[124], lower_bound=0, upper_bound=2)
        >>> x[123]
        IntegerVar(name='x', shape=[NumberLit(value=124)], lower_bound=NumberLit(value=0), upper_bound=NumberLit(value=2))[NumberLit(value=123)]
    """
    def __new__(cls, name: str, *, shape=None, lower_bound, upper_bound, latex=None, description=None):
        pass

    def __add__(self, value, /):
        """
        Return self+value.
        """
        pass


    def __getitem__(self, key, /):
        """
        Return self[key].
        """
        pass


    def __mul__(self, value, /):
        """
        Return self*value.
        """
        pass


    def __neg__(self, /):
        """
        -self
        """
        pass


    def __pow__(self, value, mod=None, /):
        """
        Return pow(self, value, mod).
        """
        pass


    def __radd__(self, value, /):
        """
        Return value+self.
        """
        pass


    def __rmul__(self, value, /):
        """
        Return value*self.
        """
        pass


    def __rpow__(self, value, mod=None, /):
        """
        Return pow(value, self, mod).
        """
        pass


    def __rsub__(self, value, /):
        """
        Return value-self.
        """
        pass


    def __sub__(self, value, /):
        """
        Return self-value.
        """
        pass


    def _repr_latex_(self, /):
        """
        
        """
        pass


    description: str
    lower_bound: typing.Any
    name: str
    ndim: int
    def set_latex(self, /, latex=None):
        """
        Set the LaTeX representation of the object.
        If the LaTeX representation is not set, the default representation is set.
        
        Args:
            latex (str, optional): LaTeX representation of the object. Defaults to None.
        """
        pass


    shape: tuple
    upper_bound: typing.Any
@typing.final
class LessThanEqualOp:
    """
    A class for representing the less than equal operator
    
    The LessThanEqualOp class is used to represent the less than equal operator (`<=`).
    The number of dimensions of each operand is zero.
    
    Attributes:
        left: The left-hand operand.
        right: The right-hand operand.
    
    Note:
        The LessThanEqualOp class does not have a constructor.
    """
    def __new__(cls):
        pass

    def __and__(self, value, /):
        """
        Return self&value.
        """
        pass


    def __or__(self, value, /):
        """
        Return self|value.
        """
        pass


    def __rand__(self, value, /):
        """
        Return value&self.
        """
        pass


    def __ror__(self, value, /):
        """
        Return value|self.
        """
        pass


    def __rxor__(self, value, /):
        """
        Return value^self.
        """
        pass


    def __xor__(self, value, /):
        """
        Return self^value.
        """
        pass


    def _repr_latex_(self, /):
        """
        
        """
        pass


    left: typing.Any
    right: typing.Any
    def set_latex(self, /, latex=None):
        """
        Set the LaTeX representation of the object.
        If the LaTeX representation is not set, the default representation is set.
        
        Args:
            latex (str, optional): LaTeX representation of the object. Defaults to None.
        """
        pass


@typing.final
class LessThanOp:
    """
    A class for representing the less than operator
    
    The LessThanOp class is used to represent the less than operator (`<`).
    The number of dimensions of each operand is zero.
    
    Attributes:
        left: The left-hand operand.
        right: The right-hand operand.
    
    Note:
        The LessThanOp class does not have a constructor.
    """
    def __new__(cls):
        pass

    def __and__(self, value, /):
        """
        Return self&value.
        """
        pass


    def __or__(self, value, /):
        """
        Return self|value.
        """
        pass


    def __rand__(self, value, /):
        """
        Return value&self.
        """
        pass


    def __ror__(self, value, /):
        """
        Return value|self.
        """
        pass


    def __rxor__(self, value, /):
        """
        Return value^self.
        """
        pass


    def __xor__(self, value, /):
        """
        Return self^value.
        """
        pass


    def _repr_latex_(self, /):
        """
        
        """
        pass


    left: typing.Any
    right: typing.Any
    def set_latex(self, /, latex=None):
        """
        Set the LaTeX representation of the object.
        If the LaTeX representation is not set, the default representation is set.
        
        Args:
            latex (str, optional): LaTeX representation of the object. Defaults to None.
        """
        pass


@typing.final
class LnOp:
    """
    A class for representing the natural logarithm
    
    The LnOp class is used to represent the natural logarithm.
    The number of dimensions of the operand is zero.
    
    Attributes:
        operand: The operand.
    
    Note:
        The LnOp class does not have a constructor.
    """
    def __new__(cls):
        pass

    def __add__(self, value, /):
        """
        Return self+value.
        """
        pass


    def __mod__(self, value, /):
        """
        Return self%value.
        """
        pass


    def __mul__(self, value, /):
        """
        Return self*value.
        """
        pass


    def __neg__(self, /):
        """
        -self
        """
        pass


    def __pow__(self, value, mod=None, /):
        """
        Return pow(self, value, mod).
        """
        pass


    def __radd__(self, value, /):
        """
        Return value+self.
        """
        pass


    def __rmod__(self, value, /):
        """
        Return value%self.
        """
        pass


    def __rmul__(self, value, /):
        """
        Return value*self.
        """
        pass


    def __rpow__(self, value, mod=None, /):
        """
        Return pow(value, self, mod).
        """
        pass


    def __rsub__(self, value, /):
        """
        Return value-self.
        """
        pass


    def __rtruediv__(self, value, /):
        """
        Return value/self.
        """
        pass


    def __sub__(self, value, /):
        """
        Return self-value.
        """
        pass


    def __truediv__(self, value, /):
        """
        Return self/value.
        """
        pass


    def _repr_latex_(self, /):
        """
        
        """
        pass


    operand: typing.Any
    def set_latex(self, /, latex=None):
        """
        Set the LaTeX representation of the object.
        If the LaTeX representation is not set, the default representation is set.
        
        Args:
            latex (str, optional): LaTeX representation of the object. Defaults to None.
        """
        pass


@typing.final
class Log10Op:
    """
    A class for representing the base 10 logarithm
    
    The Log10Op class is used to represent the base 10 logarithm.
    The number of dimensions of the operand is zero.
    
    Attributes:
        operand: The operand.
    
    Note:
        The Log10Op class does not have a constructor.
    """
    def __new__(cls):
        pass

    def __add__(self, value, /):
        """
        Return self+value.
        """
        pass


    def __mod__(self, value, /):
        """
        Return self%value.
        """
        pass


    def __mul__(self, value, /):
        """
        Return self*value.
        """
        pass


    def __neg__(self, /):
        """
        -self
        """
        pass


    def __pow__(self, value, mod=None, /):
        """
        Return pow(self, value, mod).
        """
        pass


    def __radd__(self, value, /):
        """
        Return value+self.
        """
        pass


    def __rmod__(self, value, /):
        """
        Return value%self.
        """
        pass


    def __rmul__(self, value, /):
        """
        Return value*self.
        """
        pass


    def __rpow__(self, value, mod=None, /):
        """
        Return pow(value, self, mod).
        """
        pass


    def __rsub__(self, value, /):
        """
        Return value-self.
        """
        pass


    def __rtruediv__(self, value, /):
        """
        Return value/self.
        """
        pass


    def __sub__(self, value, /):
        """
        Return self-value.
        """
        pass


    def __truediv__(self, value, /):
        """
        Return self/value.
        """
        pass


    def _repr_latex_(self, /):
        """
        
        """
        pass


    operand: typing.Any
    def set_latex(self, /, latex=None):
        """
        Set the LaTeX representation of the object.
        If the LaTeX representation is not set, the default representation is set.
        
        Args:
            latex (str, optional): LaTeX representation of the object. Defaults to None.
        """
        pass


@typing.final
class Log2Op:
    """
    A class for representing the base 2 logarithm
    
    The Log2Op class is used to represent the base 2 logarithm.
    The number of dimensions of the operand is zero.
    
    Attributes:
        operand: The operand.
    
    Note:
        The Log2Op class does not have a constructor.
    """
    def __new__(cls):
        pass

    def __add__(self, value, /):
        """
        Return self+value.
        """
        pass


    def __mod__(self, value, /):
        """
        Return self%value.
        """
        pass


    def __mul__(self, value, /):
        """
        Return self*value.
        """
        pass


    def __neg__(self, /):
        """
        -self
        """
        pass


    def __pow__(self, value, mod=None, /):
        """
        Return pow(self, value, mod).
        """
        pass


    def __radd__(self, value, /):
        """
        Return value+self.
        """
        pass


    def __rmod__(self, value, /):
        """
        Return value%self.
        """
        pass


    def __rmul__(self, value, /):
        """
        Return value*self.
        """
        pass


    def __rpow__(self, value, mod=None, /):
        """
        Return pow(value, self, mod).
        """
        pass


    def __rsub__(self, value, /):
        """
        Return value-self.
        """
        pass


    def __rtruediv__(self, value, /):
        """
        Return value/self.
        """
        pass


    def __sub__(self, value, /):
        """
        Return self-value.
        """
        pass


    def __truediv__(self, value, /):
        """
        Return self/value.
        """
        pass


    def _repr_latex_(self, /):
        """
        
        """
        pass


    operand: typing.Any
    def set_latex(self, /, latex=None):
        """
        Set the LaTeX representation of the object.
        If the LaTeX representation is not set, the default representation is set.
        
        Args:
            latex (str, optional): LaTeX representation of the object. Defaults to None.
        """
        pass


@typing.final
class MaxOp:
    """
    A class for representing the maximum value.
    
    The MaxOp class is used to represent the minimum value of operands.
    The number of dimensions of each operand is zero.
    
    Attributes:
        terms: A sequence of operands.
    
    Note:
        The MaxOp class does not have a constructor. Its intended
        instantiation method is by calling the `max` function.
    """
    def __new__(cls):
        pass

    def __add__(self, value, /):
        """
        Return self+value.
        """
        pass


    def __mod__(self, value, /):
        """
        Return self%value.
        """
        pass


    def __mul__(self, value, /):
        """
        Return self*value.
        """
        pass


    def __neg__(self, /):
        """
        -self
        """
        pass


    def __pow__(self, value, mod=None, /):
        """
        Return pow(self, value, mod).
        """
        pass


    def __radd__(self, value, /):
        """
        Return value+self.
        """
        pass


    def __rmod__(self, value, /):
        """
        Return value%self.
        """
        pass


    def __rmul__(self, value, /):
        """
        Return value*self.
        """
        pass


    def __rpow__(self, value, mod=None, /):
        """
        Return pow(value, self, mod).
        """
        pass


    def __rsub__(self, value, /):
        """
        Return value-self.
        """
        pass


    def __rtruediv__(self, value, /):
        """
        Return value/self.
        """
        pass


    def __sub__(self, value, /):
        """
        Return self-value.
        """
        pass


    def __truediv__(self, value, /):
        """
        Return self/value.
        """
        pass


    def _repr_latex_(self, /):
        """
        
        """
        pass


    def set_latex(self, /, latex=None):
        """
        Set the LaTeX representation of the object.
        If the LaTeX representation is not set, the default representation is set.
        
        Args:
            latex (str, optional): LaTeX representation of the object. Defaults to None.
        """
        pass


    terms: typing.Any
@typing.final
class MeasuringTime:
    """
    A class for storing time to be measured.
    
    Attributes:
        solve (SolvingTime): Time to solve the problem.
        system (SystemTime): Time to measure system time.
        total (float, optional): Total time to solve the problem. Defaults to None.
    """
    def __new__(cls, solve=Ellipsis, system=Ellipsis, total=None):
        pass

    @staticmethod
    def from_dict(dict):
        """
        Create a MeasuringTime object from the given dict.
        
        If a key is not the name of the MeasuringTime fields, the value value is ignored.
        
        Args:
            dict (dict): A dict.
        
        Returns:
            A MeasuringTime object.
        """
        pass


    @staticmethod
    def from_json(json):
        """
        Create a MeasuringTime object from the JSON string.
        
        Args:
            json (str): A JSON string.
        
        Returns:
            MeasuringTime: A MeasuringTime object.
        """
        pass


    solve: typing.Any
    system: typing.Any
    def to_dict(self, /):
        """
        Convert into a dict.
        
        Returns:
            dict: A dict whose keys are name of the MeasuringTime's fields.
        """
        pass


    def to_json(self, /):
        """
        Serialize the MeasuringTime object into a JSON string.
        
        Returns:
            str: A JSON string.
        
        Note:
            A numpy array is serialized into a list.
        """
        pass


    total: typing.Any
@typing.final
class MinOp:
    """
    A class for representing the minimum value.
    
    The MinOp class is used to represent the minimum value of operands.
    The number of dimensions of each operand is zero.
    
    Attributes:
        terms: A sequence of operands.
    
    Note:
        The MinOp class does not have a constructor. Its intended
        instantiation method is by calling the `min` function.
    """
    def __new__(cls):
        pass

    def __add__(self, value, /):
        """
        Return self+value.
        """
        pass


    def __mod__(self, value, /):
        """
        Return self%value.
        """
        pass


    def __mul__(self, value, /):
        """
        Return self*value.
        """
        pass


    def __neg__(self, /):
        """
        -self
        """
        pass


    def __pow__(self, value, mod=None, /):
        """
        Return pow(self, value, mod).
        """
        pass


    def __radd__(self, value, /):
        """
        Return value+self.
        """
        pass


    def __rmod__(self, value, /):
        """
        Return value%self.
        """
        pass


    def __rmul__(self, value, /):
        """
        Return value*self.
        """
        pass


    def __rpow__(self, value, mod=None, /):
        """
        Return pow(value, self, mod).
        """
        pass


    def __rsub__(self, value, /):
        """
        Return value-self.
        """
        pass


    def __rtruediv__(self, value, /):
        """
        Return value/self.
        """
        pass


    def __sub__(self, value, /):
        """
        Return self-value.
        """
        pass


    def __truediv__(self, value, /):
        """
        Return self/value.
        """
        pass


    def _repr_latex_(self, /):
        """
        
        """
        pass


    def set_latex(self, /, latex=None):
        """
        Set the LaTeX representation of the object.
        If the LaTeX representation is not set, the default representation is set.
        
        Args:
            latex (str, optional): LaTeX representation of the object. Defaults to None.
        """
        pass


    terms: typing.Any
@typing.final
class ModOp:
    """
    A class for representing modulo
    
    The ModOp class is used to represent modulo (or remainder) (`%`).
    The number of dimensions of each operand is zero.
    
    Attributes:
        left: The left-hand operand.
        right: The right-hand operand.
    
    Note:
        The ModOp class does not have a constructor.
    """
    def __new__(cls):
        pass

    def __add__(self, value, /):
        """
        Return self+value.
        """
        pass


    def __mod__(self, value, /):
        """
        Return self%value.
        """
        pass


    def __mul__(self, value, /):
        """
        Return self*value.
        """
        pass


    def __neg__(self, /):
        """
        -self
        """
        pass


    def __pow__(self, value, mod=None, /):
        """
        Return pow(self, value, mod).
        """
        pass


    def __radd__(self, value, /):
        """
        Return value+self.
        """
        pass


    def __rmod__(self, value, /):
        """
        Return value%self.
        """
        pass


    def __rmul__(self, value, /):
        """
        Return value*self.
        """
        pass


    def __rpow__(self, value, mod=None, /):
        """
        Return pow(value, self, mod).
        """
        pass


    def __rsub__(self, value, /):
        """
        Return value-self.
        """
        pass


    def __rtruediv__(self, value, /):
        """
        Return value/self.
        """
        pass


    def __sub__(self, value, /):
        """
        Return self-value.
        """
        pass


    def __truediv__(self, value, /):
        """
        Return self/value.
        """
        pass


    def _repr_latex_(self, /):
        """
        
        """
        pass


    left: typing.Any
    right: typing.Any
    def set_latex(self, /, latex=None):
        """
        Set the LaTeX representation of the object.
        If the LaTeX representation is not set, the default representation is set.
        
        Args:
            latex (str, optional): LaTeX representation of the object. Defaults to None.
        """
        pass


@typing.final
class ModelingError(BaseException):
    """
    Common base class for all non-exit exceptions.
    """
    def __new__(cls):
        pass

    args: typing.Any
    def with_traceback():
        """
        Exception.with_traceback(tb) --
        set self.__traceback__ to tb and return self.
        """
        pass


@typing.final
class MulOp:
    """
    A class for representing multiplication
    
    The MulOp class is used to represent multiplication (`*`) of an arbitrary number of operands.
    For example `a * b * c * d` would be one AddOp object.
    The number of dimensions of each operand is zero.
    
    Attributes:
        terms: A sequence of operands to be multiplied.
    
    Note:
        The MulOp class does not have a constructor. Its intended
        instantiation method is by calling the multiplication operation on other
        expressions.
    """
    def __new__(cls):
        pass

    def __add__(self, value, /):
        """
        Return self+value.
        """
        pass


    def __mod__(self, value, /):
        """
        Return self%value.
        """
        pass


    def __mul__(self, value, /):
        """
        Return self*value.
        """
        pass


    def __neg__(self, /):
        """
        -self
        """
        pass


    def __pow__(self, value, mod=None, /):
        """
        Return pow(self, value, mod).
        """
        pass


    def __radd__(self, value, /):
        """
        Return value+self.
        """
        pass


    def __rmod__(self, value, /):
        """
        Return value%self.
        """
        pass


    def __rmul__(self, value, /):
        """
        Return value*self.
        """
        pass


    def __rpow__(self, value, mod=None, /):
        """
        Return pow(value, self, mod).
        """
        pass


    def __rsub__(self, value, /):
        """
        Return value-self.
        """
        pass


    def __rtruediv__(self, value, /):
        """
        Return value/self.
        """
        pass


    def __sub__(self, value, /):
        """
        Return self-value.
        """
        pass


    def __truediv__(self, value, /):
        """
        Return self/value.
        """
        pass


    def _repr_latex_(self, /):
        """
        
        """
        pass


    def set_latex(self, /, latex=None):
        """
        Set the LaTeX representation of the object.
        If the LaTeX representation is not set, the default representation is set.
        
        Args:
            latex (str, optional): LaTeX representation of the object. Defaults to None.
        """
        pass


    terms: typing.Any
@typing.final
class NotEqualOp:
    """
    A class for representing the not equal operator
    
    The NotEqualOp class is used to represent the not equal operator (`!=`).
    The number of dimensions of each operand is zero.
    
    Attributes:
        left: The left-hand operand.
        right: The right-hand operand.
    
    Note:
        The NotEqualOp class does not have a constructor.
    """
    def __new__(cls):
        pass

    def __and__(self, value, /):
        """
        Return self&value.
        """
        pass


    def __or__(self, value, /):
        """
        Return self|value.
        """
        pass


    def __rand__(self, value, /):
        """
        Return value&self.
        """
        pass


    def __ror__(self, value, /):
        """
        Return value|self.
        """
        pass


    def __rxor__(self, value, /):
        """
        Return value^self.
        """
        pass


    def __xor__(self, value, /):
        """
        Return self^value.
        """
        pass


    def _repr_latex_(self, /):
        """
        
        """
        pass


    left: typing.Any
    right: typing.Any
    def set_latex(self, /, latex=None):
        """
        Set the LaTeX representation of the object.
        If the LaTeX representation is not set, the default representation is set.
        
        Args:
            latex (str, optional): LaTeX representation of the object. Defaults to None.
        """
        pass


@typing.final
class NumberLit:
    """
    A class for creating a number literal
    
    The NumberLit class is used to create a number literal.
    Its instance is automatically generated by the return value of
    arithmetic or mathematical functions taking a number literal and
    an object defined by jijmodeling as arguments.
    
    Attributes:
        value (int | float): A numeric value.
        dtype (:obj:`DataType`): A type of the value.
            `dtype` is `DataType.INTEGER` if the type of the value is integer else `dtype` is `DataType.FLOAT`.
    
    Args:
        value (int | float): A numeric value.
    
    Examples:
        Create a number literal with a integer value `123`.
    
        >>> import jijmodeling as jm
        >>> v = jm.NumberLit(123)
        >>> assert v.value == 123
        >>> assert v.dtype == jm.DataType.INTEGER
    
        Create a number literal with a float value `1.23`.
    
        >>> import jijmodeling as jm
        >>> v = jm.NumberLit(1.23)
        >>> assert v.value == 1.23
        >>> assert v.dtype == jm.DataType.FLOAT
    """
    def __new__(cls, value):
        pass

    def __add__(self, value, /):
        """
        Return self+value.
        """
        pass


    def __mod__(self, value, /):
        """
        Return self%value.
        """
        pass


    def __mul__(self, value, /):
        """
        Return self*value.
        """
        pass


    def __neg__(self, /):
        """
        -self
        """
        pass


    def __pow__(self, value, mod=None, /):
        """
        Return pow(self, value, mod).
        """
        pass


    def __radd__(self, value, /):
        """
        Return value+self.
        """
        pass


    def __rmod__(self, value, /):
        """
        Return value%self.
        """
        pass


    def __rmul__(self, value, /):
        """
        Return value*self.
        """
        pass


    def __rpow__(self, value, mod=None, /):
        """
        Return pow(value, self, mod).
        """
        pass


    def __rsub__(self, value, /):
        """
        Return value-self.
        """
        pass


    def __rtruediv__(self, value, /):
        """
        Return value/self.
        """
        pass


    def __sub__(self, value, /):
        """
        Return self-value.
        """
        pass


    def __truediv__(self, value, /):
        """
        Return self/value.
        """
        pass


    def _repr_latex_(self, /):
        """
        
        """
        pass


    dtype: typing.Any
    value: typing.Any
@typing.final
class OrOp:
    """
    A class for representing logical OR
    
    The OrOp class is used to represent logical OR (`|`) of an arbitrary number of operands.
    For example `a | b | c | d` would be one OrOp object.
    The number of dimensions of each operand is zero.
    
    Attributes:
        terms: A sequence of operands to apply the OR operation.
    
    Note:
        The OrOp class does not have a constructor.
    """
    def __new__(cls):
        pass

    def __and__(self, value, /):
        """
        Return self&value.
        """
        pass


    def __or__(self, value, /):
        """
        Return self|value.
        """
        pass


    def __rand__(self, value, /):
        """
        Return value&self.
        """
        pass


    def __ror__(self, value, /):
        """
        Return value|self.
        """
        pass


    def __rxor__(self, value, /):
        """
        Return value^self.
        """
        pass


    def __xor__(self, value, /):
        """
        Return self^value.
        """
        pass


    def _repr_latex_(self, /):
        """
        
        """
        pass


    def set_latex(self, /, latex=None):
        """
        Set the LaTeX representation of the object.
        If the LaTeX representation is not set, the default representation is set.
        
        Args:
            latex (str, optional): LaTeX representation of the object. Defaults to None.
        """
        pass


    terms: typing.Any
@typing.final
class Placeholder:
    """
    A class for creating a placeholder
    
    The Placeholder class is used to create a placeholder.
    It is a symbol to be replaced by a numerical value when you solve an optimization problem.
    
    The index operator (`[]`) of a placeholder with `ndim >= 1` returns a :obj:`Subscript` object.
    
    Attributes:
        name (str): A name of the placeholder.
        ndim (int): The number of dimensions of the placeholder.
        description (str, optional): A description of the placeholder.
    
    Args:
        name (str): A name of the placeholder.
        ndim (int): The number of dimensions of the placeholder. Defaults to `0`.
            The :obj:`ndim` must be set to a non-negative value.
        latex (str, optional): A LaTeX-name of the placeholder to be represented in Jupyter notebook.
            It is set to :obj:`name` by default.
        description (str, optional): A description of the placeholder.
    
    Raises:
        TypeError: Raises if set a float value to `ndim`.
        OverflowError: Raises if set a negative value to `ndim`.
    
    Examples:
        Create a scalar (or ndim is 0) placeholder whose name is "a".
    
        >>> import jijmodeling as jm
        >>> a = jm.Placeholder("a")
    
        Create a 2-dimensional placeholder whose name is "m".
    
        >>> import jijmodeling as jm
        >>> m = jm.Placeholder("m", ndim=2)
    
        Create a 1-dimensional placeholder with the index of `123`.
    
        >>> import jijmodeling as jm
        >>> a = jm.Placeholder("a", ndim=2)
        >>> a[123]
        Placeholder(name='a', ndim=2)[NumberLit(value=123)]
    """
    def __new__(cls, name: str, *, ndim=0, latex=None, description=None):
        pass

    def __add__(self, value, /):
        """
        Return self+value.
        """
        pass


    def __getitem__(self, key, /):
        """
        Return self[key].
        """
        pass


    def __mod__(self, value, /):
        """
        Return self%value.
        """
        pass


    def __mul__(self, value, /):
        """
        Return self*value.
        """
        pass


    def __neg__(self, /):
        """
        -self
        """
        pass


    def __pow__(self, value, mod=None, /):
        """
        Return pow(self, value, mod).
        """
        pass


    def __radd__(self, value, /):
        """
        Return value+self.
        """
        pass


    def __rmod__(self, value, /):
        """
        Return value%self.
        """
        pass


    def __rmul__(self, value, /):
        """
        Return value*self.
        """
        pass


    def __rpow__(self, value, mod=None, /):
        """
        Return pow(value, self, mod).
        """
        pass


    def __rsub__(self, value, /):
        """
        Return value-self.
        """
        pass


    def __rtruediv__(self, value, /):
        """
        Return value/self.
        """
        pass


    def __sub__(self, value, /):
        """
        Return self-value.
        """
        pass


    def __truediv__(self, value, /):
        """
        Return self/value.
        """
        pass


    def _repr_latex_(self, /):
        """
        
        """
        pass


    description: str
    def len_at(self, /, axis, *, latex=None, description=None):
        """
        
        """
        pass


    name: str
    ndim: int
    def set_latex(self, /, latex=None):
        """
        Set the LaTeX representation of the object.
        If the LaTeX representation is not set, the default representation is set.
        
        Args:
            latex (str, optional): LaTeX representation of the object. Defaults to None.
        """
        pass


    shape: tuple
@typing.final
class PowOp:
    """
    A class for representing the power operator
    
    The ModOp class is used to represent the power operator(`**`).
    The number of dimensions of each operand is zero.
    
    Attributes:
        base: The base operand.
        exponent: The exponent operand.
    
    Note:
        The PowOp class does not have a constructor.
    """
    def __new__(cls):
        pass

    def __add__(self, value, /):
        """
        Return self+value.
        """
        pass


    def __mod__(self, value, /):
        """
        Return self%value.
        """
        pass


    def __mul__(self, value, /):
        """
        Return self*value.
        """
        pass


    def __neg__(self, /):
        """
        -self
        """
        pass


    def __pow__(self, value, mod=None, /):
        """
        Return pow(self, value, mod).
        """
        pass


    def __radd__(self, value, /):
        """
        Return value+self.
        """
        pass


    def __rmod__(self, value, /):
        """
        Return value%self.
        """
        pass


    def __rmul__(self, value, /):
        """
        Return value*self.
        """
        pass


    def __rpow__(self, value, mod=None, /):
        """
        Return pow(value, self, mod).
        """
        pass


    def __rsub__(self, value, /):
        """
        Return value-self.
        """
        pass


    def __rtruediv__(self, value, /):
        """
        Return value/self.
        """
        pass


    def __sub__(self, value, /):
        """
        Return self-value.
        """
        pass


    def __truediv__(self, value, /):
        """
        Return self/value.
        """
        pass


    def _repr_latex_(self, /):
        """
        
        """
        pass


    base: typing.Any
    exponent: typing.Any
    def set_latex(self, /, latex=None):
        """
        Set the LaTeX representation of the object.
        If the LaTeX representation is not set, the default representation is set.
        
        Args:
            latex (str, optional): LaTeX representation of the object. Defaults to None.
        """
        pass


@typing.final
class Problem:
    """
    A class for creating an optimization problem
    
    The Problem class is used to create an optimization problem.
    
    Attributes:
        name (str): A name of the optimization problem.
        sense: Sense of the optimization problem.
        objective: The objective function of the optimization problem.
        constraints (dict): A dictionary that stores constraints.
            A key is the name of a constraint and the value is the constraint object.
        custom_penalty_terms (dict): A dictionary that stores custom penalty terms.
            A key is the name of a custom penalty and the value is the custom penalty object.
    
    Args:
        name (str): A name of the optimization problem.
        sense (optional): Sense of the optimization problem. Defaults to :obj:`ProblemSense.MINIMIZE`.
    """
    def __new__(cls, name: str, *, sense=Ellipsis):
        pass

    def _repr_latex_(self, /):
        """
        
        """
        pass


    constraints: typing.Any
    custom_penalty_terms: typing.Any
    name: str
    objective: typing.Any
    sense: typing.Any
@typing.final
class ProblemSense:
    """
    An optimization sense
    """
    def __new__(cls):
        pass

    MAXIMIZE: ProblemSense
    MINIMIZE: ProblemSense
@typing.final
class ProdOp:
    """
    A class for representing product
    
    The ProdOp class is used to represent product.
    The number of dimensions of the opreand is zero.
    
    Attributes:
        index: The index of product.
        condition: The condition for the product index.
        operand: The opreand.
    
    Note:
        The ProdOp class does not have a constructor.
    """
    def __new__(cls):
        pass

    def __add__(self, value, /):
        """
        Return self+value.
        """
        pass


    def __mod__(self, value, /):
        """
        Return self%value.
        """
        pass


    def __mul__(self, value, /):
        """
        Return self*value.
        """
        pass


    def __neg__(self, /):
        """
        -self
        """
        pass


    def __pow__(self, value, mod=None, /):
        """
        Return pow(self, value, mod).
        """
        pass


    def __radd__(self, value, /):
        """
        Return value+self.
        """
        pass


    def __rmod__(self, value, /):
        """
        Return value%self.
        """
        pass


    def __rmul__(self, value, /):
        """
        Return value*self.
        """
        pass


    def __rpow__(self, value, mod=None, /):
        """
        Return pow(value, self, mod).
        """
        pass


    def __rsub__(self, value, /):
        """
        Return value-self.
        """
        pass


    def __rtruediv__(self, value, /):
        """
        Return value/self.
        """
        pass


    def __sub__(self, value, /):
        """
        Return self-value.
        """
        pass


    def __truediv__(self, value, /):
        """
        Return self/value.
        """
        pass


    def _repr_latex_(self, /):
        """
        
        """
        pass


    condition: typing.Any
    index: typing.Any
    operand: typing.Any
    def set_latex(self, /, latex=None):
        """
        Set the LaTeX representation of the object.
        If the LaTeX representation is not set, the default representation is set.
        
        Args:
            latex (str, optional): LaTeX representation of the object. Defaults to None.
        """
        pass


@typing.final
class ProtobufDeserializationError(BaseException):
    """
    Common base class for all non-exit exceptions.
    """
    def __new__(cls):
        pass

    args: typing.Any
    def with_traceback():
        """
        Exception.with_traceback(tb) --
        set self.__traceback__ to tb and return self.
        """
        pass


@typing.final
class ProtobufSerializationError(BaseException):
    """
    Common base class for all non-exit exceptions.
    """
    def __new__(cls):
        pass

    args: typing.Any
    def with_traceback():
        """
        Exception.with_traceback(tb) --
        set self.__traceback__ to tb and return self.
        """
        pass


@typing.final
class Range:
    """
    A class representing a half-open interval.
    
    The `Range` class is used to represent a half-open interval [start, end).
    This class does not have a constructor because it should be created by the Element class.
    
    Attributes:
        start: The lower bound of the range (inclusive).
        end: The upper bound of the range (exclusive).
    
    Note:
        This class does not contain any decision variable.
    """
    def __new__(cls):
        pass

    end: typing.Any
    start: typing.Any
@typing.final
class Record:
    """
    A class for representing a record.
    
    There are two types of solutions that can be given; dense solutions and sparse solutions.
    A dense solution is a dict whose key is a variable name and the value is a list of numpy.ndarray.
    A sparse solution is a dict whose key is a variable name and the value is a list of tuples with three elements,
    where the first element is a list of indices, the second element is a list of non-zero values, and the third element is a shape of the array.
    The length of the list of solutions must be the same as the length of the list of num_occurrences.
    Each index of the list of solutions corresponds to the same index of the list of non-zero values.
    
    As an example, consider the following solutions:
    
    ```python
    {
        "x": [np.array([[0.0, 1.0, 0.0], [2.0, 0.0, 3.0]]), np.array([[1.0, 0.0, 0.0], [2.0, 3.0, 4.0]])],
        "y": [np.array([0.0, 0.0, 1.0]), np.array([0.0, 1.0, 0.0])]
    }
    ```
    
    This is a dense solution. The corresponding sparse solution is as follows:
    
    ```python
    {
        "x": [(([0, 1, 1], [1, 0, 2]), [1.0, 2.0, 3.0], (2, 3)), (([0, 1, 1, 1], [0, 0, 1, 2]), [1.0, 2.0, 3.0, 4.0], (2, 3))],
        "y": [(([2],), [1.0], (3,)), (([1],), [1.0], (3,))]
    }
    ```
    
    Attributes:
        solution (Union[Dict[str, List[numpy.ndarray]], Dict[str, List[Tuple[List[int], List[float], Tuple[int, ...]]]]]): A solution.
        num_occurrences (List[int]): A list of the number of occurrences in which the solution is observed.
    """
    def __new__(cls, solution, num_occurrences):
        pass

    @staticmethod
    def from_dict(dict):
        """
        Create a Record object from the given dict.
        
        If a key is not one of "solution" or "num_occurrences", the value is ignored.
        
        Args:
            dict: A dict of str to a list of dense solutions or sparse solutions.
        
        Returns:
            A Record object.
        """
        pass


    @staticmethod
    def from_json(json):
        """
        Create a Record object from the JSON string.
        
        Args:
            json (str): A JSON string.
        
        Returns:
            Record: A Record object.
        """
        pass


    def is_dense(self, /):
        """
        Return true if the solution is dense.
        
        Returns:
            bool: True if the solution is dense.
        """
        pass


    def is_sparse(self, /):
        """
        Return true if the solution is sparse.
        
        Returns:
            bool: True if the solution is sparse.
        """
        pass


    num_occurrences: typing.Any
    solution: typing.Any
    def to_dense(self, /):
        """
        Return a Record object whose solution is dense.
        If the solution is already dense, the solution is not converted.
        Otherwise, the solution is converted into a dense solution.
        
        Returns:
            Record: A Record object whose solution is dense.
        """
        pass


    def to_dict(self, /):
        """
        Convert into a dict.
        
        Returns:
            dict: A dict whose keys are "solution" and "num_occurrences".
        """
        pass


    def to_json(self, /):
        """
        Serialize the Record object into a JSON string.
        
        Returns:
            str: A JSON string.
        
        Note:
            A numpy array is serialized into a list.
        """
        pass


    def to_pandas(self, /):
        """
        Convert into a pandas DataFrame.
        
        Returns:
            pandas.DataFrame: A pandas DataFrame.
        """
        pass


    def to_sparse(self, /):
        """
        Return a Record object whose solution is sparse.
        If the solution is already sparse, the solution is not converted.
        Otherwise, the solution is converted into a sparse solution.
        
        Returns:
            Record: A Record object whose solution is sparse.
        """
        pass


@typing.final
class SampleSet:
    """
    A class for storing time of jijzept running.
    
    Attributes:
        post_problem_and_instance_data (float, optional): Time to upload problem and instance_data to blob. Defaults to None.
        request_queue (float, optional): Time to send request to queue. Defaults to None.
        fetch_problem_and_instance_data (float, optional): Time to fetch problme and instance_data from blob. Defaults to None.
        fetch_result (float, optional): Time to fetch result. Defaults to None.
        deserialize_solution (float, optional): Time to deserialize json object. Defaults to None.
    """
    def __new__(cls, record, evaluation, measuring_time, metadata=None):
        pass

    evaluation: typing.Any
    def feasible(self, /, rtol=1e-05, atol=1e-08):
        """
        Return a Sampleset with only feasible solutions.
        If there is no feasible solution, the record and evaluation are empty.
        
        Args:
            rtol (float): The relative tolerance parameter. Defaults to 1e-5.
            atol (float): The absolute tolerance parameter. Defaults to 1e-8.
        
        Returns:
            SampleSet: A SampleSet object with only feasible solutions or empty.
        
        Note:
            The feasible solutions are determined by the following condition:
            $$ |0 - v| \\leq \\mathrm{atol} + \\mathrm{rtol} \\cdot |v| $$
        """
        pass


    @staticmethod
    def from_dict(dict):
        """
        Create a SampleSet object from the given dict.
        
        If a key is not the name of the SampleSet fields, the value value is ignored.
        
        Args:
            dict (dict): A dict.
        
        Returns:
            A SampleSet object.
        """
        pass


    @staticmethod
    def from_json(json):
        """
        Create a SampleSet object from the JSON string.
        
        Args:
            json (str): A JSON string.
        
        Returns:
            SampleSet: A SampleSet object.
        """
        pass


    def get_backend_calculation_time(self, /):
        """
        Return report of the calculation time of the JijZept backends.
        
        Returns:
            dict: A dictionary of the calculation time of the JijZept backends.
        """
        pass


    def infeasible(self, /, rtol=1e-05, atol=1e-08):
        """
        Return a Sampleset with only infeasible solutions.
        If there is no infeasible solution, the record and evaluation are empty.
        
        Args:
            rtol (float): The relative tolerance parameter. Defaults to 1e-5.
            atol (float): The absolute tolerance parameter. Defaults to 1e-8.
        
        Returns:
            SampleSet: A SampleSet object with only infeasible solutions or empty.
        
        Note:
            The feasible solutions are determined by the following condition:
            $$ |0 - v| > \\mathrm{atol} + \\mathrm{rtol} \\cdot |v| $$
        """
        pass


    def is_dense(self, /):
        """
        Return true if the solution is dense.
        
        Returns:
            bool: True if the solution is dense.
        """
        pass


    def is_sparse(self, /):
        """
        Return true if the solution is sparse.
        
        Returns:
            bool: True if the solution is sparse.
        """
        pass


    def lowest(self, /, rtol=1e-05, atol=1e-08):
        """
        Return a Sampleset with feasible solutions which has the lowest objective.
        If there is no feasible solution, the record and evaluation are empty.
        
        Args:
            rtol (float): The relative tolerance parameter. Defaults to 1e-5.
            atol (float): The absolute tolerance parameter. Defaults to 1e-8.
        
        Returns:
            SampleSet: A SampleSet object with feasible solutions or empty.
        
        Note:
            The feasible solutions are determined by the following condition:
            $$ |0 - v| \\leq \\mathrm{atol} + \\mathrm{rtol} \\cdot |v| $$
        """
        pass


    measuring_time: typing.Any
    metadata: typing.Any
    record: typing.Any
    def to_dense(self, /):
        """
        Return a Sampleset whose record is converted into a dense solution format.
        If the record is already a dense solution format, return itself.
        
        Returns:
            SampleSet: A SampleSet object.
        """
        pass


    def to_dict(self, /):
        """
        Convert into a dict.
        
        Returns:
            dict: A dict whose keys are name of the SampleSet's fields.
        """
        pass


    def to_json(self, /):
        """
        Serialize the SampleSet object into a JSON string.
        
        Returns:
            str: A JSON string.
        
        Note:
            A numpy array is converted into a list.
        """
        pass


    def to_pandas(self, /):
        """
        Convert into a pandas DataFrame.
        
        Returns:
            pandas.DataFrame: A pandas DataFrame.
        """
        pass


@typing.final
class SemiContinuousVar:
    """
    A class for creating a semi-continuous variable
    
    The SemiContinuousVar class is used to create a semi-continuous variable.
    Either the lower bound or the upper bound is set by the following object:
    - an integer value
    - a float value
    - a scalar expression that does not contains any decision variable
    - a Placeholder object whose dimensionality is equal to that of this variable.
    - a subscripted variable whose dimensionality is equal to that of this variable.
    
    The index operator (`[]`) of a semi-continuous variable with `ndim >= 1` returns a :obj:`Subscript` object.
    
    Attributes:
        name (str): A name of the semi-continuous variable.
        shape (tuple): A tuple with the size of each dimension of the semi-continuous variable. Empty if the variable is not multi-dimensional.
        lower_bound: The lower bound of the variable.
        upper_bound: The upper bound of the variable.
        description (str): A description of the semi-continuous variable.
    
    Args:
        name (str): A name of the semi-continuous variable.
        shape (list/tuple): A sequence with the size of each dimension of the binary variable. Defaults to an empty tuple (a scalar value).
            Each item in :obj:`shape` must be a valid expression evaluating to a non-negative scalar.
        lower_bound: The lower bound of the variable.
        upper_bound: The upper bound of the variable.
        latex (str, optional): A LaTeX-name of the semi-continuous variable to be represented in Jupyter notebook.
            It is set to :obj:`name` by default.
        description (str, optional): A description of the semi-continuous variable.
    
    Raises:
        ModelingError: Raises if a bound is a `Placeholder` or `Subscript` object whose `ndim` is neither `0` nor the same value as `ndim` of the semi-continuous variable.
    
    Examples:
        Create a scalar semi-continuous variable whose name is "z" and domain is [-1, 1].
    
        >>> import jijmodeling as jm
        >>> z = jm.SemiContinuousVar("z", lower_bound=-1, upper_bound=1)
    
        Create a 2-dimensional semi-continuous variable...
        - whose name is "x".
        - whose domain is [0, 2].
        - where each dimension has length 2 (making this a 2x2 matrix).
    
        >>> import jijmodeling as jm
        >>> x = jm.SemiContinuousVar("x", shape=[2, 2], lower_bound=0, upper_bound=2)
    
        Create a 1-dimensional semi-continuous variable with the index of `123`.
    
        >>> import jijmodeling as jm
        >>> x = jm.SemiContinuousVar("x", shape=[124], lower_bound=0, upper_bound=2)
        >>> x[123]
        SemiContinuousVar(name='x', shape=[NumberLit(value=124)], lower_bound=NumberLit(value=0), upper_bound=NumberLit(value=2))[NumberLit(value=123)]
    """
    def __new__(cls, name: str, *, shape=None, lower_bound, upper_bound, latex=None, description=None):
        pass

    def __add__(self, value, /):
        """
        Return self+value.
        """
        pass


    def __getitem__(self, key, /):
        """
        Return self[key].
        """
        pass


    def __mul__(self, value, /):
        """
        Return self*value.
        """
        pass


    def __neg__(self, /):
        """
        -self
        """
        pass


    def __pow__(self, value, mod=None, /):
        """
        Return pow(self, value, mod).
        """
        pass


    def __radd__(self, value, /):
        """
        Return value+self.
        """
        pass


    def __rmul__(self, value, /):
        """
        Return value*self.
        """
        pass


    def __rpow__(self, value, mod=None, /):
        """
        Return pow(value, self, mod).
        """
        pass


    def __rsub__(self, value, /):
        """
        Return value-self.
        """
        pass


    def __sub__(self, value, /):
        """
        Return self-value.
        """
        pass


    def _repr_latex_(self, /):
        """
        
        """
        pass


    description: str
    lower_bound: typing.Any
    name: str
    ndim: int
    def set_latex(self, /, latex=None):
        """
        Set the LaTeX representation of the object.
        If the LaTeX representation is not set, the default representation is set.
        
        Args:
            latex (str, optional): LaTeX representation of the object. Defaults to None.
        """
        pass


    shape: tuple
    upper_bound: typing.Any
@typing.final
class SemiIntegerVar:
    """
    A class for creating a semi-integer variable
    
    The SemiIntegerVar class is used to create a semi-integer variable.
    The lower and upper bounds of the variable can be specified by:
    - an integer value
    - a float value
    - a scalar expression that does not contains any decision variable
    - a Placeholder object whose dimensionality is equal to that of this variable.
    - a subscripted variable whose dimensionality is equal to that of this variable.
    
    The index operator (`[]`) of a semi-integer variable with `ndim >= 1` returns a :obj:`Subscript` object.
    
    Attributes:
        name (str): A name of the semi-integer variable.
        shape (tuple): A tuple with the size of each dimension of the integer variable. Empty if the variable is not multi-dimensional.
        lower_bound: The lower bound of the variable.
        upper_bound: The upper bound of the variable.
        description (str): A description of the semi-integer variable.
    
    Args:
        name (str): A name of the semi-integer variable.
        shape (list/tuple): A sequence with the size of each dimension of the integer variable. Defaults to an empty tuple (a scalar value).
            Each item in :obj:`shape` must be a valid expression evaluating to a non-negative scalar.
        lower_bound: The lower bound of the variable.
        upper_bound: The upper bound of the variable.
        latex (str, optional): A LaTeX-name of the semi-integer variable to be represented in Jupyter notebook.
            It is set to :obj:`name` by default.
        description (str, optional): A description of the semi-integer variable.
    
    Raises:
        ModelingError: Raises if a bound is a `Placeholder` or `Subscript` object whose `ndim` is neither `0` nor the same value as `ndim` of the semi-integer variable.
    
    Examples:
        Create a scalar semi-integer variable whose name is "z" and domain is [-1, 1].
    
        >>> import jijmodeling as jm
        >>> z = jm.SemiIntegerVar("z", lower_bound=-1, upper_bound=1)
    
        Create a 2-dimensional semi-integer variable...
        - whose name is "x".
        - whose domain is [0, 2].
        - where each dimension has length 2 (making this a 2x2 matrix).
    
        >>> import jijmodeling as jm
        >>> x = jm.SemiIntegerVar("x", shape=[2, 2], lower_bound=0, upper_bound=2)
    
        Create a 1-dimensional semi-integer variable with the index of `123`.
    
        >>> import jijmodeling as jm
        >>> x = jm.SemiIntegerVar("x", shape=[124], lower_bound=0, upper_bound=2)
        >>> x[123]
        SemiIntegerVar(name='x', shape=[NumberLit(value=124)], lower_bound=NumberLit(value=0), upper_bound=NumberLit(value=2))[NumberLit(value=123)]
    """
    def __new__(cls, name: str, *, shape=None, lower_bound, upper_bound, latex=None, description=None):
        pass

    def __add__(self, value, /):
        """
        Return self+value.
        """
        pass


    def __getitem__(self, key, /):
        """
        Return self[key].
        """
        pass


    def __mul__(self, value, /):
        """
        Return self*value.
        """
        pass


    def __neg__(self, /):
        """
        -self
        """
        pass


    def __pow__(self, value, mod=None, /):
        """
        Return pow(self, value, mod).
        """
        pass


    def __radd__(self, value, /):
        """
        Return value+self.
        """
        pass


    def __rmul__(self, value, /):
        """
        Return value*self.
        """
        pass


    def __rpow__(self, value, mod=None, /):
        """
        Return pow(value, self, mod).
        """
        pass


    def __rsub__(self, value, /):
        """
        Return value-self.
        """
        pass


    def __sub__(self, value, /):
        """
        Return self-value.
        """
        pass


    def _repr_latex_(self, /):
        """
        
        """
        pass


    description: str
    lower_bound: typing.Any
    name: str
    ndim: int
    def set_latex(self, /, latex=None):
        """
        Set the LaTeX representation of the object.
        If the LaTeX representation is not set, the default representation is set.
        
        Args:
            latex (str, optional): LaTeX representation of the object. Defaults to None.
        """
        pass


    shape: tuple
    upper_bound: typing.Any
@typing.final
class SolvingTime:
    """
    A class for storing time to solve a problem.
    
    Attributes:
        preprocess (float, optional): Time to preprocess the problem. Defaults to None.
        solve (float, optional): Time to solve the problem. Defaults to None.
        postprocess (float, optional): Time to postprocess the problem. Defaults to None.
    """
    def __new__(cls, preprocess=None, solve=None, postprocess=None):
        pass

    @staticmethod
    def from_dict(dict):
        """
        Create a SolvingTime object from the given dict.
        
        If a key is not one of "preprocess", "solve", or "postprocess", the value is ignored.
        
        Args:
            dict (dict): A dict.
        
        Returns:
            A SolvingTime object.
        """
        pass


    @staticmethod
    def from_json(json):
        """
        Create a SolvingTime object from the JSON string.
        
        Args:
            json (str): A JSON string.
        
        Returns:
            SolvingTime: A SolvingTime object.
        """
        pass


    postprocess: typing.Any
    preprocess: typing.Any
    solve: typing.Any
    def to_dict(self, /):
        """
        Convert into a dict.
        
        Returns:
            dict: A dict with keys "preprocess", "solve", and "postprocess".
        """
        pass


    def to_json(self, /):
        """
        Serialize the SolvingTime object into a JSON string.
        
        Returns:
            str: A JSON string.
        
        Note:
            A numpy array is serialized into a list.
        """
        pass


@typing.final
class Subscript:
    """
    A class for representing a subscripted variable
    
    The Subscript class is used to represent a variable with subscriptions.
    
    Attributes:
        variable: A variable that has subscripts.
        subscripts (list): A list of subscripts.
        ndim (int): The number of dimensions of the subscripted variable.
    
    Note:
        The Subscript class does not have a constructor.
    """
    def __new__(cls):
        pass

    def __add__(self, value, /):
        """
        Return self+value.
        """
        pass


    def __getitem__(self, key, /):
        """
        Return self[key].
        """
        pass


    def __mod__(self, value, /):
        """
        Return self%value.
        """
        pass


    def __mul__(self, value, /):
        """
        Return self*value.
        """
        pass


    def __neg__(self, /):
        """
        -self
        """
        pass


    def __pow__(self, value, mod=None, /):
        """
        Return pow(self, value, mod).
        """
        pass


    def __radd__(self, value, /):
        """
        Return value+self.
        """
        pass


    def __rmod__(self, value, /):
        """
        Return value%self.
        """
        pass


    def __rmul__(self, value, /):
        """
        Return value*self.
        """
        pass


    def __rpow__(self, value, mod=None, /):
        """
        Return pow(value, self, mod).
        """
        pass


    def __rsub__(self, value, /):
        """
        Return value-self.
        """
        pass


    def __rtruediv__(self, value, /):
        """
        Return value/self.
        """
        pass


    def __sub__(self, value, /):
        """
        Return self-value.
        """
        pass


    def __truediv__(self, value, /):
        """
        Return self/value.
        """
        pass


    def _repr_latex_(self, /):
        """
        
        """
        pass


    def len_at(self, /, axis, *, latex=None, description=None):
        """
        
        """
        pass


    ndim: int
    shape: tuple
    subscripts: typing.Any
    variable: typing.Any
@typing.final
class SumOp:
    """
    A class for representing summation
    
    The SumOp class is used to represent summation.
    The number of dimensions of the opreand is zero.
    
    Attributes:
        index: The index of summation.
        condition: The condition for the summation index.
        operand: The opreand.
    
    Note:
        The SumOp class does not have a constructor.
    """
    def __new__(cls):
        pass

    def __add__(self, value, /):
        """
        Return self+value.
        """
        pass


    def __mod__(self, value, /):
        """
        Return self%value.
        """
        pass


    def __mul__(self, value, /):
        """
        Return self*value.
        """
        pass


    def __neg__(self, /):
        """
        -self
        """
        pass


    def __pow__(self, value, mod=None, /):
        """
        Return pow(self, value, mod).
        """
        pass


    def __radd__(self, value, /):
        """
        Return value+self.
        """
        pass


    def __rmod__(self, value, /):
        """
        Return value%self.
        """
        pass


    def __rmul__(self, value, /):
        """
        Return value*self.
        """
        pass


    def __rpow__(self, value, mod=None, /):
        """
        Return pow(value, self, mod).
        """
        pass


    def __rsub__(self, value, /):
        """
        Return value-self.
        """
        pass


    def __rtruediv__(self, value, /):
        """
        Return value/self.
        """
        pass


    def __sub__(self, value, /):
        """
        Return self-value.
        """
        pass


    def __truediv__(self, value, /):
        """
        Return self/value.
        """
        pass


    def _repr_latex_(self, /):
        """
        
        """
        pass


    condition: typing.Any
    index: typing.Any
    operand: typing.Any
    def set_latex(self, /, latex=None):
        """
        Set the LaTeX representation of the object.
        If the LaTeX representation is not set, the default representation is set.
        
        Args:
            latex (str, optional): LaTeX representation of the object. Defaults to None.
        """
        pass


@typing.final
class SystemTime:
    """
    A class for storing time of jijzept running.
    
    Attributes:
        post_problem_and_instance_data (float, optional): Time to upload problem and instance_data to blob. Defaults to None.
        request_queue (float, optional): Time to send request to queue. Defaults to None.
        fetch_problem_and_instance_data (float, optional): Time to fetch problme and instance_data from blob. Defaults to None.
        fetch_result (float, optional): Time to fetch result. Defaults to None.
        deserialize_solution (float, optional): Time to deserialize json object. Defaults to None.
    """
    def __new__(cls, post_problem_and_instance_data=None, request_queue=None, fetch_problem_and_instance_data=None, fetch_result=None, deserialize_solution=None):
        pass

    deserialize_solution: typing.Any
    fetch_problem_and_instance_data: typing.Any
    fetch_result: typing.Any
    @staticmethod
    def from_dict(dict):
        """
        Create a SystemTime object from the given dict.
        
        If a key is not the name of the SystemTime fields, the value value is ignored.
        
        Args:
            dict (dict): A dict.
        
        Returns:
            A SystemTime object.
        """
        pass


    @staticmethod
    def from_json(json):
        """
        Create a SystemTime object from the JSON string.
        
        Args:
            json (str): A JSON string.
        
        Returns:
            SystemTime: A SystemTime object.
        """
        pass


    post_problem_and_instance_data: typing.Any
    request_queue: typing.Any
    def to_dict(self, /):
        """
        Convert into a dict.
        
        Returns:
            dict: A dict whose keys are name of the SystemTime's fields.
        """
        pass


    def to_json(self, /):
        """
        Serialize the SystemTime object into a JSON string.
        
        Returns:
            str: A JSON string.
        
        Note:
            A numpy array is serialized into a list.
        """
        pass


@typing.final
class XorOp:
    """
    A class for representing logical XOR
    
    The XorOp class is used to represent logical XOR (`^`) of an arbitrary number of operands.
    For example `a ^ b ^ c ^ d` would be one AndOp object.
    The number of dimensions of each operand is zero.
    
    Attributes:
        terms: A sequence of operands to apply the XOR operation.
    
    Note:
        The XorOp class does not have a constructor.
    """
    def __new__(cls):
        pass

    def __and__(self, value, /):
        """
        Return self&value.
        """
        pass


    def __or__(self, value, /):
        """
        Return self|value.
        """
        pass


    def __rand__(self, value, /):
        """
        Return value&self.
        """
        pass


    def __ror__(self, value, /):
        """
        Return value|self.
        """
        pass


    def __rxor__(self, value, /):
        """
        Return value^self.
        """
        pass


    def __xor__(self, value, /):
        """
        Return self^value.
        """
        pass


    def _repr_latex_(self, /):
        """
        
        """
        pass


    def set_latex(self, /, latex=None):
        """
        Set the LaTeX representation of the object.
        If the LaTeX representation is not set, the default representation is set.
        
        Args:
            latex (str, optional): LaTeX representation of the object. Defaults to None.
        """
        pass


    terms: typing.Any
def abs(operand):
    """
    Create the `AbsOp` object from the expression.
    
    Args:
        operand: An operand of the abs operator.
    
    Returns:
        obj: The `AbsOp` object whose operand is the input.
    
    Examples:
        Create the `AbsOp` object whose operand is a placeholder.
    
        >>> import jijmodeling as jm
        >>> a = jm.Placeholder("a")
        >>> jm.abs(a)
    
    Raises:
        ModelingError: Raises if the input contains a decision variable.
    """
    pass


def ceil(operand):
    """
    Create the `CeilOp` object from the expression.
    
    Args:
        operand: An operand of the ceil operator.
    
    Returns:
        obj: The `CeilOp` object whose operand is the input.
    
    Examples:
        Create the `CeilOp` object whose operand is a placeholder.
    
        >>> import jijmodeling as jm
        >>> a = jm.Placeholder("a")
        >>> jm.ceil(a)
    
    Raises:
        ModelingError: Raises if the input contains a decision variable.
    """
    pass


def extract_nodes(obj, type):
    """
    Extract all nodes from the given object.
    
    Args:
        obj: An expression defined by JijModeling's module, or a `Problem`, `Constraint`, `CustomPenaltyTerm`, or a list of forall object.
        type: A type of node to extract.
    
    Returns:
        list: A list of nodes whose type is `type`.
    
    Examples:
        Extract all placeholders from the given expression.
    
        ```python
        >>> from itertools import zip_longest
        >>> import jijmodeling as jm
        >>> a = jm.Placeholder("a")
        >>> b = jm.Placeholder("b")
        >>> expr = jm.Placeholder("a") + jm.Placeholder("b")
        >>> for actual, expect in zip_longest(jm.extract_nodes(expr, jm.Placeholder), [a, b]):
        >>>     assert jm.is_same(actual, expect)
        ```
    """
    pass


def extract_variables(obj):
    """
    Extract all variables from the given object without duplication.
    
    This function returns a list of variables present within the given object.
    The variables are stored in the list according to their visit order in a depth-first traversal of the tree.
    Even if the same variable appears more than twice in the expression tree, the variable is only stored in the list upon its first appearance.
    Consequently, the list returned by this function contains only the unique variables present in the expression.
    
    Args:
        obj: An expression defined by JijModeling's module, or a `Problem`, `Constraint`, `CustomPenaltyTerm`, or a list of forall object.
    
    Returns:
        list: A list of variables, which are `Placeholder`, `Element`, `ArrayLength`, `BinaryVar`, `IntegerVar`, `ContinuousVar`, `SemiIntegerVar`, or `SemiContinuousVar`.
    
    Examples:
        Extract all variables from a problem without duplication.
    
        ```python
        >>> n = jm.Placeholder("n")
        >>> i = jm.Element("i", belong_to=n)
        >>> x = jm.BinaryVar("x", shape=[10])
        >>> y = jm.IntegerVar("y", shape=[10], lower_bound=0, upper_bound=1)
        >>> z = jm.ContinuousVar("z", shape=[10], lower_bound=0, upper_bound=1)
        >>> problem = jm.Problem("problem")
        >>> problem += jm.sum(i, x[i])
        >>> problem += jm.Constraint("constraint", y[i] == 1, forall=i)
        >>> problem += jm.CustomPenaltyTerm("penalty", z[i], forall=i)
        >>> actual = jm.extract_variables(problem)
        >>> expect = [i, n, x, y, z]
        >>> assert len(actual) == len(expect)
        >>> for actual_node, expect_node in zip(actual, expect):
        >>>     assert jm.is_same(actual_node, expect_node)
        ```
    """
    pass


def floor(operand):
    """
    Create the `FloorOp` object from the expression.
    
    Args:
        operand: An operand of the floor operator.
    
    Returns:
        obj: The `FloorOp` object whose operand is the input.
    
    Examples:
        Create the `FloorOp` object whose operand is a placeholder.
    
        >>> import jijmodeling as jm
        >>> a = jm.Placeholder("a")
        >>> jm.floor(a)
    
    Raises:
        ModelingError: Raises if the input contains a decision variable.
    """
    pass


def from_protobuf(buf):
    """
    
    """
    pass


def is_dynamic_degree(expr):
    """
    Return true if degree of the expression is not determined statically.
    
    Args:
        expr: A math expression to be checked.
    
    Returns:
        bool: True if degree of the expression is determined dynamically.
    
    Examples:
        Check if the degree of the following expression is determined dynamically.
    
        ```python
        a = jm.Placeholder("a", ndim=1)
        i = jm.Element("i", belong_to=a)
        x = jm.BinaryVar("x", shape=(a.len_at(0),))
        # The number of multiplication is not determined until the value of a is given.
        expr = jm.prod(i, x[i])
        assert jm.is_dynamic_degree(expr)
        ```
    """
    pass


def is_higher_order(expr):
    """
    Return true if the degree of the given expression is higher than 2.
    
    Args:
        expr: A math expression to be checked.
    
    Returns:
        bool: True if the degree of the given expression is higher than 2.
    """
    pass


def is_linear(expr):
    """
    Return true if the given expression is linear.
    
    Args:
        expr: A math expression to be checked.
    
    Returns:
        bool: True if the given expression is linear.
    """
    pass


def is_quadratic(expr):
    """
    Return true if the given expression is quadratic.
    
    Args:
        expr: A math expression to be checked.
    
    Returns:
        bool: True if the given expression is quadratic.
    """
    pass


def is_same(src, dst):
    """
    Return `true` if `src` and `dst` are the same object defined by Jijmodeling.
    
    Args:
        src: An object defined by Jijmodeling module.
        dst: An object defined by Jijmodeling module.
    
    Returns:
        bool: `true` if `src` and `dst` is the same object. Otherwise `false`.
    
    Examples:
        Check if the two placeholders are the same.
    
        >>> import jijmodeling as jm
        >>> a = jm.Placeholder("name")
        >>> b = jm.Placeholder("name")
        >>> assert jm.is_same(a, b)
        >>> c = jm.Placeholder("name", ndim=2)
        >>> assert not jm.is_same(a, c) # the value of `ndim` is different
    
    Raises:
        TypeError: Raises if the type of `src` is different from the type of `dst`, or one of them is not an object defined by Jijmodeling module (e.g. `str`).
    
    Note:
        This function does not check the following attributes:
        - `description`
        - `latex`
    
        For example,
    
        >>> import jijmodeling as jm
        >>> src = jm.Placeholder("placeholder", latex="src")
        >>> dst = jm.Placeholder("placeholder", latex="dst")
        >>> assert jm.is_same(src, dst)
    
        this code works without any exception.
    """
    pass


def ln(operand):
    """
    Create the `LnOp` object from the expression.
    
    Args:
        operand: An operand of the natural logarithm.
    
    Returns:
        obj: The `LnOp` object whose operand is the input.
    
    Examples:
        Create the `LnOp` object whose operand is a placeholder.
    
        >>> import jijmodeling as jm
        >>> a = jm.Placeholder("a")
        >>> jm.ln(a)
    
    Raises:
        ModelingError: Raises if the input contains a decision variable.
    """
    pass


def log10(operand):
    """
    Create the `Log10Op` object from the expression.
    
    Args:
        operand: An operand of the log10 operator.
    
    Returns:
        obj: The `Log10Op` object whose operand is the input.
    
    Examples:
        Create the `Log10Op` object whose operand is a placeholder.
    
        >>> import jijmodeling as jm
        >>> a = jm.Placeholder("a")
        >>> jm.log10(a)
    
    Raises:
        ModelingError: Raises if the input contains a decision variable.
    """
    pass


def log2(operand):
    """
    Create the `Log2Op` object from the expression.
    
    Args:
        operand: An operand of the log2 operator.
    
    Returns:
        obj: The `Log2Op` object whose operand is the input.
    
    Examples:
        Create the `Log2Op` object whose operand is a placeholder.
    
        >>> import jijmodeling as jm
        >>> a = jm.Placeholder("a")
        >>> jm.log2(a)
    
    Raises:
        ModelingError: Raises if the input contains a decision variable.
    """
    pass


def max(*operands):
    """
    Create the `MaxOp` object from the expression.
    
    Args:
        operands: A sequence of operands.
    
    Returns:
        obj: The `MaxOp` object whose operands are the inputs.
    
    Examples:
        Create the `MaxOp` object whose operands are three placeholders.
    
        ```python
        >>> import jijmodeling as jm
        >>> a = jm.Placeholder("a")
        >>> b = jm.Placeholder("b")
        >>> c = jm.Placeholder("c")
        >>> jm.max(a, b, c)
        ```
    
    Raises:
        ModelingError: Raises if the input contains a decision variable.
    """
    pass


def min(*operands):
    """
    Create the `MinOp` object from the expression.
    
    Args:
        operands: A sequence of operands.
    
    Returns:
        obj: The `MinOp` object whose operands are the inputs.
    
    Examples:
        Create the `MinOp` object whose operands are three placeholders.
    
        ```python
        >>> import jijmodeling as jm
        >>> a = jm.Placeholder("a")
        >>> b = jm.Placeholder("b")
        >>> c = jm.Placeholder("c")
        >>> jm.min(a, b, c)
        ```
    
    Raises:
        ModelingError: Raises if the input contains a decision variable.
    """
    pass


def prod(index, operand):
    """
    Create the `ProdOp` object.
    
    Args:
        index: An index of product.
        operand: The operand of product.
    
    Returns:
        obj: The `ProdOp` object.
    
    Examples:
        Create product of an indexed placeholder $a_{i}$ from $i=0$ to $N-1$.
    
        >>> import jijmodeling as jm
        >>> a = jm.Placeholder("a", ndim=1)
        >>> N = jm.Placeholder("N")
        >>> i = jm.Element("i", belong_to=(0, N))
        >>> jm.prod(i, a[i])
    
        Create product of an indexed binary variable $x_{e}$ over all elements $e$ in the set $E$.
    
        >>> import jijmodeling as jm
        >>> x = jm.BinaryVar("x", ndim=1)
        >>> E = jm.Placeholder("E", ndim=1)
        >>> e = jm.Element("e", belong_to=E)
        >>> jm.prod(e, x[e])
    
        By passing a tuple containing two elements to the index of product, a conditional index can be constructed.
        The left element of the tuple should be an instance of the `Element` class, while the right element should be the conditional expression for that index.
    
        >>> import jijmodeling as jm
        >>> a = jm.Placeholder("a", ndim=1)
        >>> i = jm.Element("i", belong_to=(0, 10))
        >>> jm.prod((i, i != 2), a[i])
    
        This code creates product of an indexed placeholder $a_{i}$ from $i=0$ to $9$ subject to the condition $i\neq2$.
    """
    pass


def replace(expr, replacer):
    """
    Replace the expression node with the result of calling the replacer.
    
    Args:
       expr: A target math expression.
       replacer: A callable object that takes an expression node and returns a new expression node.
    
    Examples:
        Replace a placeholder with a binary variable.
    
        ```python
        >>> import jijmodeling as jm
        >>> ph = jm.Placeholder("placeholder")
        >>> var = jm.BinaryVar("x")
        >>> replaced = jm.replace(ph, lambda x: var if isinstance(x, jm.Placeholder) else x)
        >>> assert jm.is_same(replaced, var)
        ```
    
        Replace a subscripted variable with a binary variable if it is a placeholder.
    
        ```python
        >>> import jijmodeling as jm
        >>> ph = jm.Placeholder("ph", ndim=2)
        >>> x = jm.BinaryVar("x", shape=(1000, 1000))
        >>> elt = jm.Element("elt", belong_to=ph)
        >>> expr = ph[123, 456] + elt[123]
        >>> replacer = (
            lambda node: x[node.subscripts]
            if isinstance(node, jm.Subscript) and isinstance(node.variable, jm.Placeholder)
            else node
        )
        >>> replaced = jm.replace(expr, replacer)
        >>> assert jm.is_same(replaced, x[123, 456] + elt[123])
        ```
    
    Raises:
        TypeError: Raises if the type of `replacer` is not callable.
    
    Note:
        The replacer must satisfy the following conditions:
    
        - The replacer must be a callable object.
        - The number of arguments of the replacer must be one.
        - The replacer must take an expression node as the argument.
        - The replacer must return an expression node.
    """
    pass


def sum(index, operand):
    """
    Create the `SumOp` object.
    
    Args:
        index: An index of summation.
        operand: The operand of summation.
    
    Returns:
        obj: The `SumOp` object.
    
    Examples:
        Create summation of an indexed placeholder $a_{i}$ from $i=0$ to $N-1$.
    
        >>> import jijmodeling as jm
        >>> a = jm.Placeholder("a", ndim=1)
        >>> N = jm.Placeholder("N")
        >>> i = jm.Element("i", belong_to=(0, N))
        >>> jm.sum(i, a[i])
    
        Create summation of an indexed binary variable $x_{e}$ over all elements $e$ in the set $E$.
    
        >>> import jijmodeling as jm
        >>> x = jm.BinaryVar("x", ndim=1)
        >>> E = jm.Placeholder("E", ndim=1)
        >>> e = jm.Element("e", belong_to=E)
        >>> jm.sum(e, x[e])
    
        By passing a tuple containing two elements to the index of summation, a conditional index can be constructed.
        The left element of the tuple should be an instance of the `Element` class, while the right element should be the conditional expression for that index.
    
        >>> import jijmodeling as jm
        >>> a = jm.Placeholder("a", ndim=1)
        >>> i = jm.Element("i", belong_to=(0, 10))
        >>> jm.sum((i, i != 2), a[i])
    
        This code creates summation of an indexed placeholder $a_{i}$ from $i=0$ to $9$ subject to the condition $i\neq2$.
    """
    pass


def to_protobuf(obj):
    """
    
    """
    pass


