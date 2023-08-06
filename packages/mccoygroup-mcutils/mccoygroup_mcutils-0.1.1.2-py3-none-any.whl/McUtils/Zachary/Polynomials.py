import abc, numpy as np, scipy.signal
import itertools as it
from ..Combinatorics import UniquePermutations

__all__ = [
    "AbstractPolynomial",
    "DensePolynomial",
    "SparsePolynomial",
    "PureMonicPolynomial",
    "TensorCoefficientPoly"
]

class AbstractPolynomial(metaclass=abc.ABCMeta):
    """
    Provides the general interface an abstract polynomial needs ot support, including
    multiplication, addition, shifting, access of coefficients, and evaluation
    """

    @property
    @abc.abstractmethod
    def scaling(self):
        raise NotImplementedError("abstract base class")

    @abc.abstractmethod
    def __mul__(self, other)->'AbstractPolynomial':
        raise NotImplementedError("abstract base class")
    @abc.abstractmethod
    def __add__(self, other)->'AbstractPolynomial':
        raise NotImplementedError("abstract base class")

    @abc.abstractmethod
    def shift(self, shift)->'AbstractPolynomial':
        raise NotImplementedError("abstract base class")

    def __rmul__(self, other)->'AbstractPolynomial':
        return self * other
    def __radd__(self, other)->'AbstractPolynomial':
        return self + other
    def __truediv__(self, other)->'AbstractPolynomial':
        return self * (1/other)
    def __neg__(self):
        return -1*self
    def __sub__(self, other):
        return self + (-other)
    def __rsub__(self, other):
        return (-self)+other


    # def __rtruediv__(self, other):
    #     return other * (1/self)


class DensePolynomial(AbstractPolynomial):
    """
    A straightforward dense n-dimensional polynomial data structure with
    multiplications and shifts
    """
    def __init__(self,
                 coeffs,
                 prefactor=None,
                 shift=None
                 ):
        self._scaling = prefactor
        self._shift = shift
        self._poly_coeffs = np.asanyarray(coeffs)
        self._coeff_tensors = None
        self._uc_tensors = None
    def __repr__(self):
        return "{}({}, {})".format(type(self).__name__, self.coeffs.shape, self.scaling)
    @classmethod
    def from_tensors(cls, tensors, prefactor=None, shift=None, rescale=True):
        coeffs = cls.condense_tensors(tensors, rescale=rescale)
        new = cls(coeffs, prefactor=prefactor, shift=shift)
        return new


    @property
    def shape(self):
        return self._poly_coeffs.shape

    @property
    def scaling(self):
        return 1 if self._scaling is None else self._scaling
    @scaling.setter
    def scaling(self, s):
        self._scaling = s

    @property
    def coeffs(self):
        if self._shift is not None:
            self._poly_coeffs = self._compute_shifted_coeffs(self._poly_coeffs, self._shift)
            self._shift = None
        if self._scaling is not None:
            self._poly_coeffs = self._poly_coeffs * self._scaling
            self.scaling = None
        return self._poly_coeffs
    @coeffs.setter
    def coeffs(self, cs):
        self._poly_coeffs = cs

    def __mul__(self, other)->'DensePolynomial':
        if isinstance(other, (int, float, np.integer, np.floating)):
            if other == 1:
                return self
            elif other == 0:
                return 0
        if isinstance(other, DensePolynomial):
            # print(self.coeffs.shape, other.coeffs.shape)
            new_coeffs = scipy.signal.convolve(
                self.coeffs,
                other.coeffs
            )
            return DensePolynomial(
                new_coeffs,
                shift=None,
                prefactor=self.scaling * other.scaling
            )
        else:
            return DensePolynomial(
                self._poly_coeffs,
                shift=self._shift,
                prefactor=self.scaling * other
            )

    def __add__(self, other)->'DensePolynomial':
        if isinstance(other, DensePolynomial):
            if self.shape != other.shape:  # need to cast to consistent shape
                consistent_shape = [
                    max(s1, s2)
                    for s1, s2 in zip(
                        self.shape,
                        other.shape
                    )
                ]
                fcs = np.pad(self.coeffs,
                             [[0, c-s] for c,s in zip(consistent_shape, self.shape)]
                             )
                ocs = np.pad(other.coeffs,
                             [[0, c-s] for c,s in zip(consistent_shape, other.shape)]
                             )
            else:
                fcs = self.coeffs
                ocs = other.coeffs
            return DensePolynomial(
                fcs*self.scaling + ocs*other.scaling,
                shift=None
            )
        else:
            if self.scaling != 1:
                other = other / self.scaling
            new = self._poly_coeffs.copy().flatten()
            new[0] += other
            new = new.reshape(self._poly_coeffs.shape)
            return DensePolynomial(
                new,
                shift=self._shift,
                prefactor=self.scaling
            )

    def shift(self, shift)->'DensePolynomial':
        if not isinstance(shift, (int, np.integer, float, np.floating)):
            shift = np.asanyarray(shift)
        return DensePolynomial(
            self._poly_coeffs,
            shift=(0 if self._shift is None else self._shift) + shift,
            prefactor=self._scaling
        )
    @classmethod
    def _compute_shifted_coeffs(cls, poly_coeffs, shift):
        # if fourier_coeffs is None:
        #     raise ValueError("need fourier coeffs for shifted coeff calc")
        if poly_coeffs.ndim == 1:
            shift = [shift]

        # factorial outer product
        factorial_terms = np.array([np.math.factorial(x) for x in range(poly_coeffs.shape[0])])
        for s in poly_coeffs.shape[1:]:
            factorial_terms = np.expand_dims(factorial_terms, -1) * np.reshape(
                np.array([np.math.factorial(x) for x in range(s)]),
                [1]*factorial_terms.ndim + [s]
            )
        # shift outer product
        shift_terms = np.power(shift[0], np.arange(poly_coeffs.shape[0]))
        for f,s in zip(shift[1:], poly_coeffs.shape[1:]):
            shift_terms = np.expand_dims(shift_terms, -1) * np.reshape(
                np.power(f, np.arange(s)),
                [1]*shift_terms.ndim + [s]
            )

        # build shifted polynomial coefficients
        rev_fac = factorial_terms
        for i in range(factorial_terms.ndim):
            rev_fac = np.flip(rev_fac, axis=i)
            shift_terms = np.flip(shift_terms, axis=i)

        poly_terms = poly_coeffs * factorial_terms
        shift_terms = shift_terms / rev_fac

        new = scipy.signal.convolve(
            poly_terms,
            shift_terms
        )

        for s in reversed(poly_terms.shape):
            new = np.moveaxis(new, -1, 0)
            new = new[-s:]
        new = new / factorial_terms

        return new

    @classmethod
    def extract_tensors(cls, coeffs, rescale=True):
        nz_pos = np.where(coeffs != 0)
        if len(nz_pos) == 0 or len(nz_pos[0]) == 0:
            return [0]
        max_order = np.max(np.sum(nz_pos, axis=0, dtype=int))
        # raise Exception(max_order)
        # max_order = sum(c-1 for c in coeffs.shape)
        num_dims = len(coeffs.shape)
        tensors = [
            np.zeros((num_dims,)*i)
            for i in range(1, max_order+1)
        ]
        tensors = [0] + tensors # include ref
        for idx in zip(*nz_pos):
            # we compute the order of the index, compute the number of
            # permutations of the index, and then set all of the permutations
            # equal to the value divided by the number of perms
            order = sum(idx)
            value = coeffs[idx]
            if order == 0:
                tensors[0] = value
            else:
                new_idx = sum(
                    ([i]*n for i,n in enumerate(idx)),
                    []
                ) # we figure out which coords are affected and by how much
                final_perms = UniquePermutations(new_idx).permutations()
                # print(final_perms)
                if rescale:
                    subvalue = value / len(final_perms)
                else:
                    subvalue = value
                fp_inds = tuple(final_perms.T)
                tensors[order][fp_inds] = subvalue
        return tensors
    @classmethod
    def condense_tensors(cls, tensors, rescale=True):
        # we'll be a bit slower here in constructing so we can make sure
        # we get the smallest tensor

        # order = len(tensors)
        ncoord = len(tensors[1])
        tensor_elems = {} #
        shape = [1] * ncoord
        # we could be more efficient through where tricks if we wanted
        for o,t in enumerate(tensors):
            if o == 0:
                idx = (0,)*ncoord
                tensor_elems[idx] = t
            else:
                for upos in it.combinations_with_replacement(range(ncoord), r=o):
                    val = t[upos]
                    if val != 0:
                        idx = tuple(np.bincount(upos, minlength=ncoord))
                        if rescale:
                            val = val * UniquePermutations.count_permutations(idx)
                        tensor_elems[idx] = val
                        for n,i in enumerate(idx):
                            shape[n] = max(i+1, shape[n])
        # raise Exception(shape)
        condensed_tensor = np.zeros(shape)
        for idx,val in tensor_elems.items():
            condensed_tensor[idx] = val
        return condensed_tensor

    @property
    def coefficient_tensors(self):
        if self._coeff_tensors is None:
            self._coeff_tensors = self.extract_tensors(self.coeffs)
        return self._coeff_tensors
    @property
    def unscaled_coefficient_tensors(self):
        if self._uc_tensors is None:
            self._uc_tensors = self.extract_tensors(self.coeffs, rescale=False)
        return self._uc_tensors
    def transform(self, lin_transf):
        """
        Applies (for now) a linear transformation to the polynomial
        """
        tensors = self.coefficient_tensors
        transf_tensors = []
        for n,t in enumerate(tensors):
            for ax in range(n):
                t = np.tensordot(lin_transf, t, axes=[1, n-1])
            transf_tensors.append(t)
        new = self.condense_tensors(transf_tensors)
        return DensePolynomial(new)

    def outer(self, other):
        return DensePolynomial(
            np.multiply.outer(self.coeffs, other),
            prefactor=self.scaling*other.scaling
        )

    def deriv(self, coord):
        if self._poly_coeffs.shape[coord] == 1:
            return 0
        new_coeffs = self.coeffs.copy()
        new_coeffs = np.moveaxis(new_coeffs, coord, 0)
        scaling = np.arange(1, new_coeffs.shape[0])
        for _ in range(new_coeffs.ndim-1):
            scaling = np.expand_dims(scaling, -1)
        new_coeffs = scaling * new_coeffs[1:]
        new_coeffs = np.moveaxis(new_coeffs, 0, coord)
        return DensePolynomial(
            new_coeffs,
            prefactor=self.scaling
        )

    def clip(self, threshold=1e-15):
        clipped_inds = np.where(np.abs(self.coeffs * self.scaling) > threshold)
        if len(clipped_inds) == 0 or len(clipped_inds[0]) == 0:
            return 0
        new_shape = tuple(max(x) + 1 for x in clipped_inds)
        coeffs = np.zeros(new_shape)
        coeffs[clipped_inds] = self.coeffs[clipped_inds]
        return DensePolynomial(
            coeffs,
            prefactor=self._scaling
        )
    
class SparsePolynomial(AbstractPolynomial):
    """
    A semi-symbolic representation of a polynomial of tensor
    coefficients
    """
    def __init__(self, terms:dict, prefactor=1):
        self.terms = terms
        self.prefactor = prefactor
        self._shape = None

    @property
    def scaling(self):
        return 1 if self.prefactor is None else self.prefactor
    @scaling.setter
    def scaling(self, s):
        self.prefactor = s

    def expand(self):
        if self.prefactor == 1:
            return self
        else:
            return type(self)({k:self.prefactor*v for k,v in self.terms.items()}, prefactor=1)
    @classmethod
    def monomial(cls, idx, value=1):
        return cls({idx:value})
    def __repr__(self):
        return "{}({},{})".format(type(self).__name__, self.terms,self.prefactor)

    def __mul__(self, other):
        if isinstance(other, (int, float, np.integer, np.floating)):
            if other == 1:
                return self
            elif other == 0:
                return SparsePolynomial({})
        if isinstance(other, SparsePolynomial):
            new_terms = {}
            for k,v in other.terms.items():
                for k2,v2 in self.terms.items():
                    t = tuple(sorted(k + k2))
                    new_terms[t] = new_terms.get(t, 0) + v * v2
                    if new_terms[t] == 0:
                        del new_terms[t]
            return type(self)(new_terms, prefactor=self.prefactor*other.prefactor)
        else:
            return type(self)(self.terms, prefactor=self.prefactor*other)
            # new_terms = {}
            # for k,v in self.terms.items():
            #     new_terms[k] = self.prefactor*other*v
            # return SparsePolynomial(new_terms)
    def __add__(self, other):
        if isinstance(other, (int, float, np.integer, np.floating)):
            if other == 0:
                return self
            else:
                return self + type(self)({():other})
        else:
            self = self.expand()
            new_terms = {}
            if isinstance(other, SparsePolynomial):
                other = other.expand()
                for s in other.terms.keys() & self.terms.keys():
                    v = other.terms[s]
                    v2 = self.terms[s]
                    new = v + v2
                    if new != 0:
                        new_terms[s] = new
                for o in other.terms.keys() - self.terms.keys():
                    new_terms[o] = other.terms[o]
                for o in self.terms.keys() - other.terms.keys():
                    new_terms[o] = self.terms[o]
            else:
                for k2, v2 in self.terms.items():
                    new = v2 + other
                    if new != 0:
                        new_terms[k2] = new
            if len(new_terms) == 0:
                return 0
            return type(self)(new_terms)

    @classmethod
    def _to_tensor_idx(cls, idx):
        idx_terms = {}
        m = 0
        for t in idx:
            m = max(m, t)
            idx_terms[t] = idx_terms.get(t, 0) + 1
        return tuple(idx_terms[t] for t in range(m))
    @property
    def shape(self):
        if self._shape is None:
            self._shape = np.max(np.array(list(self.terms.keys())), axis=0)
        return self._shape
    def as_dense(self)->DensePolynomial:
        new_coeffs = np.zeros(self.shape)
        for idx, val in self.terms.items():
            self._to_tensor_idx(idx)
            new_coeffs[idx] = val
        return DensePolynomial(
            new_coeffs,
            prefactor=self.prefactor
        )
    def shift(self, shift)->DensePolynomial:
        return self.as_dense().shift(shift)

class PureMonicPolynomial(SparsePolynomial):
    def __init__(self, terms: dict, prefactor=1, canonicalize=True):
        if canonicalize:
            terms = {self.canonical_key(k):v for k,v in terms.items()}
        super().__init__(terms, prefactor)

    @property
    def shape(self):
        raise ValueError("{} doesn't have a dense counterpart".format(type(self).__name__))
    def as_dense(self):
        raise ValueError("{} doesn't have a dense counterpart".format(type(self).__name__))
    def shift(self, shift) -> DensePolynomial:
        raise ValueError("{} doesn't have a dense counterpart".format(type(self).__name__))

    @classmethod
    def monomial(cls, idx, value=1):
        return cls({(idx,): value})

    @classmethod
    def key_hash(cls, monomial_tuple):
        # hashes tuples of indices to give a fast check that the tuples
        # are the same independent of ordering
        return sum(hash(x) for x in monomial_tuple)

    @classmethod
    @abc.abstractmethod
    def canonical_key(cls, monomial_tuple):
        raise NotImplementedError("{} is abstract".format(cls.__name__))

    def __mul__(self, other):
        if isinstance(other, (int, float, np.integer, np.floating)):
            if other == 1:
                return self
            elif other == 0:
                return 0
                # return type(self)({})
        if isinstance(other, PureMonicPolynomial):
            new_terms = {}
            term_hashes = {}
            for k,v in other.terms.items():
                for k2,v2 in self.terms.items():
                    new_hash = self.key_hash(k) + self.key_hash(k2)
                    if new_hash in term_hashes:
                        t = term_hashes[new_hash]
                    else:
                        t = self.canonical_key(k + k2) # construct new tuple and canonicalize
                        term_hashes[new_hash] = t
                    new_terms[t] = new_terms.get(t, 0) + v * v2
                    if new_terms[t] == 0:
                        del new_terms[t]
            return type(self)(new_terms, prefactor=self.prefactor*other.prefactor, canonicalize=False)
        else:
            return type(self)(self.terms, prefactor=self.prefactor*other, canonicalize=False)
class TensorCoefficientPoly(PureMonicPolynomial):
    """
    Represents a polynomial constructed using tensor elements as monomials
    by tracking sets of indices
    """

    @classmethod
    def canonical_key(cls, monomial_tuple):
        # we need a way to sort indices, which we do by grouping by key length,
        # doing a standard sort for each length, and reconcatenating
        s_groups = {}
        for index_tuple in monomial_tuple:
            l = len(index_tuple)
            grp = s_groups.get(l, [])
            s_groups[l] = grp
            grp.append(index_tuple)
        t = tuple(
            grp
            for l in sorted(s_groups.keys())
            for grp in sorted(s_groups[l])
        )
        return t

# class TensorCoeffPoly(AbstractPolynomial):
#     """
#     A semi-symbolic representation of a polynomial of tensor
#     coefficients
#     """
#
#     def __init__(self, terms:dict, prefactor=1):
#         self.terms = terms
#         self.prefactor = prefactor
#     def expand(self):
#         if self.prefactor == 1:
#             return self
#         else:
#             return TensorCoeffPoly({k:self.prefactor*v for k,v in self.terms.items()}, prefactor=1)
#     @classmethod
#     def monomial(cls, idx, value=1):
#         return cls({(idx,):value})
#     def __repr__(self):
#         return "{}({},{})".format(type(self).__name__, self.terms,self.prefactor)