from __future__ import annotations

from ._dtypes import (
    _floating_dtypes,
    _numeric_dtypes,
    float32,
    complex64,
    complex128,
)
from ._data_type_functions import finfo
from ._manipulation_functions import reshape
from ._elementwise_functions import conj
from ._array_object import Array
from ._flags import requires_extension, get_array_api_strict_flags

try:
    from numpy._core.numeric import normalize_axis_tuple
except ImportError:
    from numpy.core.numeric import normalize_axis_tuple

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ._typing import Literal, Optional, Sequence, Tuple, Union, Dtype

from typing import NamedTuple

import numpy.linalg
import numpy as np

class EighResult(NamedTuple):
    eigenvalues: Array
    eigenvectors: Array

class QRResult(NamedTuple):
    Q: Array
    R: Array

class SlogdetResult(NamedTuple):
    sign: Array
    logabsdet: Array

class SVDResult(NamedTuple):
    U: Array
    S: Array
    Vh: Array

# Note: the inclusion of the upper keyword is different from
# np.linalg.cholesky, which does not have it.
@requires_extension('linalg')
def cholesky(x: Array, /, *, upper: bool = False) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.linalg.cholesky <numpy.linalg.cholesky>`.

    See its docstring for more information.
    """
    # Note: the restriction to floating-point dtypes only is different from
    # np.linalg.cholesky.
    if x.dtype not in _floating_dtypes:
        raise TypeError('Only floating-point dtypes are allowed in cholesky')
    L = np.linalg.cholesky(x._array)
    if upper:
        U = Array._new(L).mT
        if U.dtype in [complex64, complex128]:
            U = conj(U)
        return U
    return Array._new(L)

# Note: cross is the numpy top-level namespace, not np.linalg
@requires_extension('linalg')
def cross(x1: Array, x2: Array, /, *, axis: int = -1) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.cross <numpy.cross>`.

    See its docstring for more information.
    """
    if x1.dtype not in _numeric_dtypes or x2.dtype not in _numeric_dtypes:
        raise TypeError('Only numeric dtypes are allowed in cross')
    if x1.ndim == 0:
        raise ValueError('cross() requires arrays of dimension at least 1')
    # Note: this is different from np.cross(), which allows dimension 2
    if x1.shape[axis] != 3:
        raise ValueError('cross() dimension must equal 3')
    return Array._new(np.cross(x1._array, x2._array, axis=axis))

@requires_extension('linalg')
def det(x: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.linalg.det <numpy.linalg.det>`.

    See its docstring for more information.
    """
    # Note: the restriction to floating-point dtypes only is different from
    # np.linalg.det.
    if x.dtype not in _floating_dtypes:
        raise TypeError('Only floating-point dtypes are allowed in det')
    return Array._new(np.linalg.det(x._array))

# Note: diagonal is the numpy top-level namespace, not np.linalg
@requires_extension('linalg')
def diagonal(x: Array, /, *, offset: int = 0) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.diagonal <numpy.diagonal>`.

    See its docstring for more information.
    """
    # Note: diagonal always operates on the last two axes, whereas np.diagonal
    # operates on the first two axes by default
    return Array._new(np.diagonal(x._array, offset=offset, axis1=-2, axis2=-1))

@requires_extension('linalg')
def eigh(x: Array, /) -> EighResult:
    """
    Array API compatible wrapper for :py:func:`np.linalg.eigh <numpy.linalg.eigh>`.

    See its docstring for more information.
    """
    # Note: the restriction to floating-point dtypes only is different from
    # np.linalg.eigh.
    if x.dtype not in _floating_dtypes:
        raise TypeError('Only floating-point dtypes are allowed in eigh')

    # Note: the return type here is a namedtuple, which is different from
    # np.eigh, which only returns a tuple.
    return EighResult(*map(Array._new, np.linalg.eigh(x._array)))


@requires_extension('linalg')
def eigvalsh(x: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.linalg.eigvalsh <numpy.linalg.eigvalsh>`.

    See its docstring for more information.
    """
    # Note: the restriction to floating-point dtypes only is different from
    # np.linalg.eigvalsh.
    if x.dtype not in _floating_dtypes:
        raise TypeError('Only floating-point dtypes are allowed in eigvalsh')

    return Array._new(np.linalg.eigvalsh(x._array))

@requires_extension('linalg')
def inv(x: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.linalg.inv <numpy.linalg.inv>`.

    See its docstring for more information.
    """
    # Note: the restriction to floating-point dtypes only is different from
    # np.linalg.inv.
    if x.dtype not in _floating_dtypes:
        raise TypeError('Only floating-point dtypes are allowed in inv')

    return Array._new(np.linalg.inv(x._array))

# Note: the name here is different from norm(). The array API norm is split
# into matrix_norm and vector_norm().

# The type for ord should be Optional[Union[int, float, Literal[np.inf,
# -np.inf, 'fro', 'nuc']]], but Literal does not support floating-point
# literals.
@requires_extension('linalg')
def matrix_norm(x: Array, /, *, keepdims: bool = False, ord: Optional[Union[int, float, Literal['fro', 'nuc']]] = 'fro') -> Array:  # noqa: F821
    """
    Array API compatible wrapper for :py:func:`np.linalg.norm <numpy.linalg.norm>`.

    See its docstring for more information.
    """
    # Note: the restriction to floating-point dtypes only is different from
    # np.linalg.norm.
    if x.dtype not in _floating_dtypes:
        raise TypeError('Only floating-point dtypes are allowed in matrix_norm')

    return Array._new(np.linalg.norm(x._array, axis=(-2, -1), keepdims=keepdims, ord=ord))


@requires_extension('linalg')
def matrix_power(x: Array, n: int, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.matrix_power <numpy.matrix_power>`.

    See its docstring for more information.
    """
    # Note: the restriction to floating-point dtypes only is different from
    # np.linalg.matrix_power.
    if x.dtype not in _floating_dtypes:
        raise TypeError('Only floating-point dtypes are allowed for the first argument of matrix_power')

    # np.matrix_power already checks if n is an integer
    return Array._new(np.linalg.matrix_power(x._array, n))

# Note: the keyword argument name rtol is different from np.linalg.matrix_rank
@requires_extension('linalg')
def matrix_rank(x: Array, /, *, rtol: Optional[Union[float, Array]] = None) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.matrix_rank <numpy.matrix_rank>`.

    See its docstring for more information.
    """
    # Note: this is different from np.linalg.matrix_rank, which supports 1
    # dimensional arrays.
    if x.ndim < 2:
        raise np.linalg.LinAlgError("1-dimensional array given. Array must be at least two-dimensional")
    S = np.linalg.svd(x._array, compute_uv=False)
    if rtol is None:
        tol = S.max(axis=-1, keepdims=True) * max(x.shape[-2:]) * finfo(S.dtype).eps
    else:
        if isinstance(rtol, Array):
            rtol = rtol._array
        # Note: this is different from np.linalg.matrix_rank, which does not multiply
        # the tolerance by the largest singular value.
        tol = S.max(axis=-1, keepdims=True)*np.asarray(rtol)[..., np.newaxis]
    return Array._new(np.count_nonzero(S > tol, axis=-1))


# Note: outer is the numpy top-level namespace, not np.linalg
@requires_extension('linalg')
def outer(x1: Array, x2: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.outer <numpy.outer>`.

    See its docstring for more information.
    """
    # Note: the restriction to numeric dtypes only is different from
    # np.outer.
    if x1.dtype not in _numeric_dtypes or x2.dtype not in _numeric_dtypes:
        raise TypeError('Only numeric dtypes are allowed in outer')

    # Note: the restriction to only 1-dim arrays is different from np.outer
    if x1.ndim != 1 or x2.ndim != 1:
        raise ValueError('The input arrays to outer must be 1-dimensional')

    return Array._new(np.outer(x1._array, x2._array))

# Note: the keyword argument name rtol is different from np.linalg.pinv
@requires_extension('linalg')
def pinv(x: Array, /, *, rtol: Optional[Union[float, Array]] = None) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.linalg.pinv <numpy.linalg.pinv>`.

    See its docstring for more information.
    """
    # Note: the restriction to floating-point dtypes only is different from
    # np.linalg.pinv.
    if x.dtype not in _floating_dtypes:
        raise TypeError('Only floating-point dtypes are allowed in pinv')

    # Note: this is different from np.linalg.pinv, which does not multiply the
    # default tolerance by max(M, N).
    if rtol is None:
        rtol = max(x.shape[-2:]) * finfo(x.dtype).eps
    return Array._new(np.linalg.pinv(x._array, rcond=rtol))

@requires_extension('linalg')
def qr(x: Array, /, *, mode: Literal['reduced', 'complete'] = 'reduced') -> QRResult:  # noqa: F821
    """
    Array API compatible wrapper for :py:func:`np.linalg.qr <numpy.linalg.qr>`.

    See its docstring for more information.
    """
    # Note: the restriction to floating-point dtypes only is different from
    # np.linalg.qr.
    if x.dtype not in _floating_dtypes:
        raise TypeError('Only floating-point dtypes are allowed in qr')

    # Note: the return type here is a namedtuple, which is different from
    # np.linalg.qr, which only returns a tuple.
    return QRResult(*map(Array._new, np.linalg.qr(x._array, mode=mode)))

@requires_extension('linalg')
def slogdet(x: Array, /) -> SlogdetResult:
    """
    Array API compatible wrapper for :py:func:`np.linalg.slogdet <numpy.linalg.slogdet>`.

    See its docstring for more information.
    """
    # Note: the restriction to floating-point dtypes only is different from
    # np.linalg.slogdet.
    if x.dtype not in _floating_dtypes:
        raise TypeError('Only floating-point dtypes are allowed in slogdet')

    # Note: the return type here is a namedtuple, which is different from
    # np.linalg.slogdet, which only returns a tuple.
    return SlogdetResult(*map(Array._new, np.linalg.slogdet(x._array)))

# Note: unlike np.linalg.solve, the array API solve() only accepts x2 as a
# vector when it is exactly 1-dimensional. All other cases treat x2 as a stack
# of matrices. The np.linalg.solve behavior of allowing stacks of both
# matrices and vectors is ambiguous c.f.
# https://github.com/numpy/numpy/issues/15349 and
# https://github.com/data-apis/array-api/issues/285.

# To workaround this, the below is the code from np.linalg.solve except
# only calling solve1 in the exactly 1D case.
def _solve(a, b):
    try:
        from numpy.linalg._linalg import (
        _makearray, _assert_stacked_2d, _assert_stacked_square,
        _commonType, isComplexType, _raise_linalgerror_singular
        )
    except ImportError:
        from numpy.linalg.linalg import (
        _makearray, _assert_stacked_2d, _assert_stacked_square,
        _commonType, isComplexType, _raise_linalgerror_singular
        )
    from numpy.linalg import _umath_linalg

    a, _ = _makearray(a)
    _assert_stacked_2d(a)
    _assert_stacked_square(a)
    b, wrap = _makearray(b)
    t, result_t = _commonType(a, b)

    # This part is different from np.linalg.solve
    if b.ndim == 1:
        gufunc = _umath_linalg.solve1
    else:
        gufunc = _umath_linalg.solve

    # This does nothing currently but is left in because it will be relevant
    # when complex dtype support is added to the spec in 2022.
    signature = 'DD->D' if isComplexType(t) else 'dd->d'
    with np.errstate(call=_raise_linalgerror_singular, invalid='call',
                     over='ignore', divide='ignore', under='ignore'):
        r = gufunc(a, b, signature=signature)

    return wrap(r.astype(result_t, copy=False))

@requires_extension('linalg')
def solve(x1: Array, x2: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.linalg.solve <numpy.linalg.solve>`.

    See its docstring for more information.
    """
    # Note: the restriction to floating-point dtypes only is different from
    # np.linalg.solve.
    if x1.dtype not in _floating_dtypes or x2.dtype not in _floating_dtypes:
        raise TypeError('Only floating-point dtypes are allowed in solve')

    return Array._new(_solve(x1._array, x2._array))

@requires_extension('linalg')
def svd(x: Array, /, *, full_matrices: bool = True) -> SVDResult:
    """
    Array API compatible wrapper for :py:func:`np.linalg.svd <numpy.linalg.svd>`.

    See its docstring for more information.
    """
    # Note: the restriction to floating-point dtypes only is different from
    # np.linalg.svd.
    if x.dtype not in _floating_dtypes:
        raise TypeError('Only floating-point dtypes are allowed in svd')

    # Note: the return type here is a namedtuple, which is different from
    # np.svd, which only returns a tuple.
    return SVDResult(*map(Array._new, np.linalg.svd(x._array, full_matrices=full_matrices)))

# Note: svdvals is not in NumPy (but it is in SciPy). It is equivalent to
# np.linalg.svd(compute_uv=False).
@requires_extension('linalg')
def svdvals(x: Array, /) -> Union[Array, Tuple[Array, ...]]:
    if x.dtype not in _floating_dtypes:
        raise TypeError('Only floating-point dtypes are allowed in svdvals')
    return Array._new(np.linalg.svd(x._array, compute_uv=False))

# Note: trace is the numpy top-level namespace, not np.linalg
@requires_extension('linalg')
def trace(x: Array, /, *, offset: int = 0, dtype: Optional[Dtype] = None) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.trace <numpy.trace>`.

    See its docstring for more information.
    """
    if x.dtype not in _numeric_dtypes:
        raise TypeError('Only numeric dtypes are allowed in trace')

    # Note: trace() works the same as sum() and prod() (see
    # _statistical_functions.py)
    if dtype is None:
        if get_array_api_strict_flags()['api_version'] < '2023.12':
            if x.dtype == float32:
                dtype = np.float64
            elif x.dtype == complex64:
                dtype = np.complex128
    else:
        dtype = dtype._np_dtype
    # Note: trace always operates on the last two axes, whereas np.trace
    # operates on the first two axes by default
    return Array._new(np.asarray(np.trace(x._array, offset=offset, axis1=-2, axis2=-1, dtype=dtype)))

# Note: the name here is different from norm(). The array API norm is split
# into matrix_norm and vector_norm().

# The type for ord should be Optional[Union[int, float, Literal[np.inf,
# -np.inf]]] but Literal does not support floating-point literals.
@requires_extension('linalg')
def vector_norm(x: Array, /, *, axis: Optional[Union[int, Tuple[int, ...]]] = None, keepdims: bool = False, ord: Optional[Union[int, float]] = 2) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.linalg.norm <numpy.linalg.norm>`.

    See its docstring for more information.
    """
    # Note: the restriction to floating-point dtypes only is different from
    # np.linalg.norm.
    if x.dtype not in _floating_dtypes:
        raise TypeError('Only floating-point dtypes are allowed in norm')

    # np.linalg.norm tries to do a matrix norm whenever axis is a 2-tuple or
    # when axis=None and the input is 2-D, so to force a vector norm, we make
    # it so the input is 1-D (for axis=None), or reshape so that norm is done
    # on a single dimension.
    a = x._array
    if axis is None:
        # Note: np.linalg.norm() doesn't handle 0-D arrays
        a = a.ravel()
        _axis = 0
    elif isinstance(axis, tuple):
        # Note: The axis argument supports any number of axes, whereas
        # np.linalg.norm() only supports a single axis for vector norm.
        normalized_axis = normalize_axis_tuple(axis, x.ndim)
        rest = tuple(i for i in range(a.ndim) if i not in normalized_axis)
        newshape = axis + rest
        a = np.transpose(a, newshape).reshape(
            (np.prod([a.shape[i] for i in axis], dtype=int), *[a.shape[i] for i in rest]))
        _axis = 0
    else:
        _axis = axis

    res = Array._new(np.linalg.norm(a, axis=_axis, ord=ord))

    if keepdims:
        # We can't reuse np.linalg.norm(keepdims) because of the reshape hacks
        # above to avoid matrix norm logic.
        shape = list(x.shape)
        _axis = normalize_axis_tuple(range(x.ndim) if axis is None else axis, x.ndim)
        for i in _axis:
            shape[i] = 1
        res = reshape(res, tuple(shape))

    return res

# These functions are also in the main namespace. We define them here as
# wrappers so that they can still be disabled when the linalg extension is
# disabled without disabling the versions in the main namespace.

# Note: matmul is the numpy top-level namespace but not in np.linalg
@requires_extension('linalg')
def matmul(x1: Array, x2: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.matmul <numpy.matmul>`.

    See its docstring for more information.
    """
    from ._linear_algebra_functions import matmul
    return matmul(x1, x2)

# Note: tensordot is the numpy top-level namespace but not in np.linalg
@requires_extension('linalg')
def tensordot(x1: Array, x2: Array, /, *, axes: Union[int, Tuple[Sequence[int], Sequence[int]]] = 2) -> Array:
    from ._linear_algebra_functions import tensordot
    return tensordot(x1, x2, axes=axes)

@requires_extension('linalg')
def matrix_transpose(x: Array, /) -> Array:
    from ._linear_algebra_functions import matrix_transpose
    return matrix_transpose(x)

@requires_extension('linalg')
def vecdot(x1: Array, x2: Array, /, *, axis: int = -1) -> Array:
    from ._linear_algebra_functions import vecdot
    return vecdot(x1, x2, axis=axis)

__all__ = ['cholesky', 'cross', 'det', 'diagonal', 'eigh', 'eigvalsh', 'inv', 'matmul', 'matrix_norm', 'matrix_power', 'matrix_rank', 'matrix_transpose', 'outer', 'pinv', 'qr', 'slogdet', 'solve', 'svd', 'svdvals', 'tensordot', 'trace', 'vecdot', 'vector_norm']
