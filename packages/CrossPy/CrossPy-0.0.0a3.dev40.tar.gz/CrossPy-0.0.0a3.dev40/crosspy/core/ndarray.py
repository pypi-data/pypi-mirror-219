import numpy
from crosspy import cupy

from typing import Any, Optional, Tuple, Union, Iterable, Sequence
from numbers import Number
from collections import defaultdict
from warnings import warn

from ..device import Device, cpu
from ..utils.array import ArrayType, register_array_type, get_array_module, is_array

from crosspy.context import context
from crosspy.transfer.cache import fetch

__all__ = ['CrossPyArray', 'BasicIndexType', 'IndexType']

import logging
logger = logging.getLogger(__name__)

BasicIndexType = Union[int, slice, Iterable[int]]  # non-recursive
IndexType = Union[BasicIndexType, Tuple[BasicIndexType, ...]]  # recursive

ShapeType=Union[Tuple[()], Tuple[int, ...]]

def _cross_apply(func, arg0, *args, **kwargs):
    if hasattr(arg0, 'device'):
        with arg0.device:
            return func(arg0, *tuple(cupy.asarray(x) for x in args), **kwargs)
    return func(arg0, *(cupy.asnumpy(x) for x in args), **kwargs)

def normalize_slice(slice_: slice, len_: int):
    def _wrap_to_positive(i):
        return i and int(i + len_ if i < 0 else i)  # convert numpy int to python int; TODO step?
    return slice(_wrap_to_positive(slice_.start or 0), _wrap_to_positive(slice_.stop if slice_.stop is not None else len_), slice_.step if slice_.step is not None else 1)

def shape_of_slice(normalized_slice_: slice):
    """Assume normalized slice"""
    return (normalized_slice_.stop - normalized_slice_.start) // normalized_slice_.step


def _local_assignment(target, local_indices, source, source_indices: Optional[tuple]=None):
    if source_indices is None:
        src = source
    else:
        src = source[tuple(source_indices)
                        ] if len(source_indices) else source.item()
    if hasattr(target, 'device'):  # target is cupy array
        if isinstance(src, self.__class__):
            src = src.all_to(target.device)
        with target.device:
            target[tuple(local_indices)] = cupy.asarray(src)
    elif hasattr(source, 'devices'): # ??? <= crosspy
        mapping = source.plan_index_mapping(source_indices, local_indices)
        for t, s in mapping:
            target[tuple(t)] = cupy.asnumpy(s)
    elif hasattr(source, 'device'):  # numpy <= cupy
        target[tuple(local_indices)] = cupy.asnumpy(src)
    else:  # numpy <= numpy
        target[tuple(local_indices)] = src

def _check_concat_axis(shapes, expected) -> Optional[int]:
    def are_all_values_same(l):
        return len(set(l)) == 1
    # a boolean list of size # dimensions, true for dimension where all parts share same size
    is_same_size_mask = [are_all_values_same(d) for d in zip(*shapes)]
    assert len(is_same_size_mask) > 0, "zero-dimensional arrays cannot be concatenated"
    if all(is_same_size_mask):  # can be concat by any dim
        assert expected < len(is_same_size_mask), "axis %d is out of bounds for array of dimension %d" % (expected, len(is_same_size_mask))
        return expected

    def all_except_one(bool_array):
        return sum(bool_array) == len(bool_array) - 1
    if all_except_one(is_same_size_mask):
        _concatable = is_same_size_mask.index(False)
        if expected != _concatable:
            raise ValueError(
                "Cannot concat on axis %s, but %s is feasible" % (expected, _concatable)
            )
        return _concatable

    raise ValueError(
        "Incompatible shapes with %s different dims" % (len(is_same_size_mask) - sum(is_same_size_mask))
    )

HANDLED_FUNCTIONS = {}


def implements(np_function):
    "Register an __array_function__ implementation."
    def decorator(func):
        HANDLED_FUNCTIONS[np_function] = func
        return func

    return decorator

def get_shape(obj, *, reg_by_id=None):
    if hasattr(obj, 'shape'):
        return getattr(obj, 'shape')
    elif hasattr(obj, '__len__'):
        return len(obj)
    elif reg_by_id and id(obj) in reg_by_id:
        return reg_by_id[id(obj)]
    raise Exception("Unknown shape of %s" % obj)

from .x1darray import Vocabulary, _Metadata, _pinned_memory_empty, get_device

class Initializer:
    """TODO make it a classmethod"""
    def __init__(self, obj, axis: Optional[int] = None, **kwargs) -> None:
        # super().__init__()
        # try:
        #     if dim is None:
        #         self._original_data = numpy.asarray(obj) # TODO: hinted by placement
        #     else:
        #         self._original_data = numpy.concatenate(obj, axis=dim)
        # except:
        self._original_data = obj  # NOTE this holds reference to the original data, which may or may not be expected

        # metainfo caches
        self._device_to_indices = defaultdict(list)
        self._lazy_movement = defaultdict(list)

        initial_shapes = kwargs.get('initial_shapes', None)
        initial_devices = kwargs.get('initial_devices', None)
        _get_shape = lambda x: get_shape(x, reg_by_id=initial_shapes)
        _get_device = lambda x: get_device(x, reg_by_id=initial_devices)

        def _record_device(obj):
            device = _get_device(obj)
            if not isinstance(device, (Device, str)):  # TODO remove string
                warn(f"{type(device)} is not a known device type to CrossPy", RuntimeWarning)

        if not isinstance(obj, (list, tuple)):
            assert axis is None, "assumption: no concat for non-list objs"
            self._shape = _get_shape(obj) # TODO shortcut other attribute computation
            self._dtype = getattr(obj, 'dtype', type(obj))
            self._metadata = None
            self.device_array = None
            self._concat_axis = None
            self._device_to_indices = None
            _record_device(obj)
            return

        list_obj = obj
        if len(list_obj) == 0:
            assert axis is None, ValueError("need at least one array to concatenate")
            self._concat_axis = None
            self._dtype = None
            self._shape = (0,)
            self._metadata = None
            self.device_array = None
            return

        self._dtype = list_obj[0].dtype
        assert all(a.dtype == self._dtype for a in list_obj[1:]), "dtype mismatched: %s" % (a.dtype for a in list_obj)

        shapes: tuple[ShapeType, ...] = tuple(_get_shape(a) for a in list_obj)
        # Check concatenation dimension
        self._concat_axis = axis if axis is None else _check_concat_axis(shapes, axis)
        if self._concat_axis is not None:
            assert self._concat_axis == 0, NotImplementedError("axis > 0 not implemented")
            self._bounds = numpy.cumsum(shapes, dtype=numpy.uint64)

        self._shape = getattr(self._original_data, 'shape', self._init_shape(shapes))

        for i, obj in enumerate(list_obj):
            if self._concat_axis is not None:
                device = _get_device(obj)
                self._device_to_indices[
                    repr(device)].append(
                    slice(self._bounds[i-1] if i else 0, self._bounds[i]))
            _record_device(obj)

        ########
        # new scheme
        ########
        objs = list_obj
        device_vocab = Vocabulary()
        self._metadata = _Metadata(len(objs), alloc=_pinned_memory_empty)

        # delay actuall concatenation
        block_idx = defaultdict(list)
        per_device_size = defaultdict(int)
        global_size = 0
        for i, block in enumerate(objs):
            did = device_vocab.index(_get_device(block))
            self._metadata.device_idx[i] = did
            if axis is None:
                raise NotImplementedError
            size = block.shape[axis]
            self._metadata.device_offset[i] = global_size - per_device_size[did]
            per_device_size[did] += size
            self._metadata.block_offset[i] = global_size + size
            global_size = self._metadata.block_offset[i]
            block_idx[did].append(i)
        # concatenate once to avoid reallocation overhead
        # device id (int) -> grouped array
        self.device_array = {}
        for did, bids in block_idx.items():
            with device_vocab[did]:
                # FIXME discrepency of view vs copy
                # TODO check module has concatenate
                self.device_array[did] = objs[bids[0]] if len(bids) == 1 else get_array_module(objs[bids[0]]).concatenate([objs[i] for i in bids], axis=axis)

    def _init_shape(self, shapes: Sequence[ShapeType]) -> ShapeType:
        """
        :param shapes: shapes of each subarray
        :return: shape of the aggregated array
        """
        if len(shapes) == 1:
            return (1,) + shapes[0] if self._concat_axis is None else shapes[0]
        if not all([len(s) == len(shapes[0]) for s in shapes[1:]]):
            # TODO: optionally add 1 dimension to align
            raise ValueError("Array dimensions mismatch")
        logger.debug(shapes)

        if self._concat_axis is None:
            return (len(shapes),) + shapes[0]
        assert self._concat_axis == 0, NotImplementedError("only support concat along axis 0")
        # merge shapes
        logger.debug("Concat over dim ", self._concat_axis)
        shape = list(shapes[0])
        shape[self._concat_axis] = sum([s[self._concat_axis] for s in shapes])
        final_shape: ShapeType = tuple(shape)
        return final_shape

    def finish(self):
        return CrossPyArray(
            self._shape,
            self._dtype,
            self._metadata,
            self.device_array,
            axis=self._concat_axis,
            original_data=self._original_data,
            device_to_indices=self._device_to_indices,
        )

class CrossPyArray(numpy.lib.mixins.NDArrayOperatorsMixin):
    """
    Heterougeneous N-dimensional array compatible with the numpy API with custom implementations of numpy functionality.

    https://numpy.org/doc/stable/user/basics.dispatch.html#basics-dispatch
    """
    fromobject = Initializer

    def __init__(
        self,
        shape,
        dtype,
        metadata,
        device_array,
        axis: Optional[int] = None,
        original_data = None,
        device_to_indices = None,
        device_to_blocks = None,
        **kwargs
    ) -> None:
        # super().__init__()
        # try:
        #     if dim is None:
        #         self._original_data = numpy.asarray(obj) # TODO: hinted by placement
        #     else:
        #         self._original_data = numpy.concatenate(obj, axis=dim)
        # except:

        self._shape = shape
        self._dtype = dtype
        self._concat_axis = axis

        self._metadata: _Metadata = metadata
        self.device_array = device_array

        self._original_data = original_data  # NOTE this holds reference to the original data, which may or may not be expected

        # metainfo caches
        self._device_to_indices = device_to_indices

        self._lazy_movement = defaultdict(list)


    @property
    def data_map(self):
        """
        :param shapes: 
        """
        if not isinstance(self._original_data, (list, tuple)):
            assert self._concat_axis is None
            return {tuple((0, s) for s in self.shape): self._original_data}

        if len(self._original_data) == 0:
            return {}

        subshape = self._original_data[0].shape
        if self._concat_axis is None:
            return {((i, i+1), (*([0] * len(subshape)), *subshape)): self._original_data[i] for i in range(len(self._original_data))}
        if len(self._original_data) == 1:
            return {tuple((0, s) for s in subshape): self._original_data[0]}
        assert self._concat_axis == 0, NotImplementedError
        bounds = numpy.cumsum([0] + [x.shape[self._concat_axis] for x in self._original_data])
        return {(*((0, s) for s in subshape[:self._concat_axis]), (bounds[i], bounds[i+1]), *((0, s) for s in subshape[self._concat_axis+1:])): self._original_data[i] for i in range(len(self._original_data))}

    # @classmethod
    # def from_shapes(cls, shapes: Sequence[ShapeType], block_gen, dim=None) -> 'CrossPyArray':
    #     """
    #     :param block_gen: i -> array
    #     """
    #     return CrossPyArray(*init_from_shapes_builder(shapes, block_gen, dim=dim))

    @property
    def nparts(self) -> int:
        if self._metadata is None:
            return 1
        return len(self._metadata.block_offset)

    @property
    def ndevices(self) -> int:
        return len(self._device_to_indices)

    @property
    def dtype(self) -> type:
        return self._dtype

    @property
    def shape(self) -> tuple[int, ...]:
        return tuple(self._shape)

    @property
    def boundaries(self):
        if self._concat_axis is not None:
            return self._metadata.block_offset
        return numpy.array(self._shape)

    @property
    def heteroaxis(self):
        return self._concat_axis

    @property
    def device_map(self):
        return {
            k: getattr(v, 'device', 'cpu')
            for k, v in self.data_map.items()
        }

    @property
    def device(self) -> list:
        return [getattr(x, 'device', -1) for x in self._original_data]

    def monolithic(self) -> bool:
        return self._concat_axis is None

    def on(self, device) -> list:
        if isinstance(device, (Device, str)):
            return self._device_to_indices.get(repr(device), [])
        return []

    def block_at(self, i: int):
        loc = self._global_index_to_block_id(i)
        return self._original_data[loc]

    def device_at(self, i: int):
        return getattr(self.block_at(i), 'device', -1)

    @property
    def type_map(self):
        return {k: type(v) for k, v in self.data_map.items()}

    def to_dict(self):
        return self.data_map

    def values(self):
        return list(self.data_map.values())

    def keys(self):
        return list(self.data_map.keys())

    def item(self):
        if self._shape != ():
            raise IndexError("cannot get item from non-scalars")
        return self.data_map.get(())

    def __bool__(self) -> bool:
        return bool(self._original_data)

    def __len__(self) -> int:
        if len(self.shape):
            return self.shape[0]
        raise TypeError("len() of unsized object")

    def __repr__(self) -> str:
        return '; '.join(
            repr(
                self.device_array[self._metadata.device_idx[i]]
                [(self._metadata.block_offset[i - 1] if i else 0) - self.
                 _metadata.device_offset[i]:self._metadata.block_offset[i] -
                 self._metadata.device_offset[i]]
            ) if self._metadata is not None else "array([])"
            for i in range(self.nparts)
        )

    def debug_print(self):
        print("DEBUG", id(self))
        print("  shape=%s" % repr(self._shape))
        print("  origin=%s" % repr(self._original_data))
        if isinstance(self._original_data, (list, tuple)):
            print("  otypes=%s" % [type(x) for x in self._original_data])
            print("  odevices=%s" % [x.device if hasattr(x, 'device') else None for x in self._original_data])
        else:
            print("  otypes=%s" % type(self._original_data))
            print("  odevices=%s" % self._original_data.device if hasattr(self._original_data, 'device') else None)

    def _index_intersection(
        self, part_range: tuple[int, int], target: BasicIndexType
    ) -> Union[BasicIndexType, None]:
        '''On one dimension, given the source range and target index, return

        TODO move to utils
        '''
        l, r = part_range
        if isinstance(
            target, int
        ) and l <= target < r:  # TODO negative indexing
            return (target - l)  # global to local
        elif isinstance(target, Iterable):
            in_range = [
                (i - l) for i in target if l <= i < r
            ]  # TODO negative indexing
            return in_range if len(in_range) else None
        elif isinstance(target, slice):
            # trivial case: target == part_range
            if target.start in (None, l) and target.stop in (None, r) and target.step in (None, 1):
                return slice(0, r-l)
            # trivial case: target and part_range are not overlapped
            if target.start and r <= target.start or target.stop and target.stop <= l:
                return None
            # long path
            new_start = None
            new_stop = None
            for i in range(
                target.start or 0, target.stop or r, target.step or 1
            ):
                if new_start is None and l <= i:
                    new_start = i
                if i < r:
                    new_stop = i + 1
            return slice(
                new_start - l, new_stop -
                l if new_stop is not None else None, target.step
            ) if new_start is not None else None
        elif isinstance(target, self.__class__):
            return target.to_dict()[((l, r),)] # TODO handle general bool mask
        return None

    def _global_index_to_block_id(self, i, out=None, stream=None):
        """
        Computes which block the referred element resides in

        Return shape and device is same to input indices unless out is given
        """
        lib = get_array_module(i)
        assert hasattr(lib, 'searchsorted'), TypeError("Indices can only be numpy.ndarray or cupy.ndarray, not %s" % type(i))
        with get_device(i) as here:
            local_block_offset = fetch(self._metadata.block_offset, here, stream)
        blk_id = lib.searchsorted(local_block_offset, i, side='right')
        if out is not None:
            out[...] = blk_id
        return blk_id


    def _indexing_check(self, index: IndexType):
        """Check before set and get item"""
        if self._shape == ():
            raise IndexError("scalar is not subscriptable")

        assert isinstance(index, (int, slice)) or (
            isinstance(index, list) and all(isinstance(i, (int, slice)) for i in index)
        ) or (
            is_array(index) and len(getattr(index, 'shape', (len(index), ))) == 1
        ), NotImplementedError(
            "Only support 1-D indexing by integers, slices, and/or arrays"
        )

        if isinstance(index, slice):
            index = normalize_slice(index, len(self))

        # unify the form to list of slices
        if not isinstance(index, tuple):
            index = (index, )

        # allow optional ellipsis [d0, d1, ...]
        if len(index) - len(self.shape) == 1 and index[-1] is Ellipsis:
            index = index[:-1]

        return index

    def _LEGACY_SLOW_check_index(self, index: Tuple[BasicIndexType]):
        def _meta_check(target, max):
            if isinstance(target,
                          int) and (0 <= target < max or 0 > target >= -max):
                return True
            elif isinstance(target, Iterable):
                return all([(0 <= i < max or 0 > i >= -max) for i in target])
            elif isinstance(target, slice):
                return all(
                    [
                        i < max for i in range(
                            target.start or 0, target.stop or max,
                            target.step or 1
                        )
                    ]
                )
            raise TypeError("index out of range", target, "vs", max)

        if not all(
            [_meta_check(i, self._shape[d]) for d, i in enumerate(index)]
        ):
            raise TypeError("index out of range")


    def get_raw_item_by_slice(self, slice_):
        left, head_start = self._locate(slice_.start)
        right, tail_stop = self._locate(slice_.stop)
        # right is not on boundary -> trailing partial block
        relevant_blocks = self._original_data[left:right + 1 if slice_.stop not in self._metadata.block_offset else right]
        assert len(relevant_blocks), "Invalid slicing: empty array not supported yet"

        assert slice_.step in [None, 1], NotImplementedError("stepping not implemented")
        # trimming
        is_partial_head = slice_.start > 0 and slice_.start not in self._metadata.block_offset
        is_partial_tail = slice_.stop < len(self) and slice_.stop not in self._metadata.block_offset
        assert is_partial_head == bool(left < len(self._original_data) and head_start)
        assert is_partial_tail == bool(right < len(self._original_data) and tail_stop) # partial tail <-> tail stop != 0

        if len(relevant_blocks) == 1:
            relevant_blocks[0] = relevant_blocks[0][is_partial_head and head_start or None: is_partial_tail and tail_stop or None]
        else:
            if is_partial_head:
                relevant_blocks[0] = relevant_blocks[0][head_start:]
            if is_partial_tail:
                relevant_blocks[-1] = relevant_blocks[-1][:tail_stop]

        return relevant_blocks

    def get_raw_item(self, index: IndexType):
        if isinstance(index, slice):
            return self.get_raw_item_by_slice(index)
        raise NotImplementedError(type(index))

    def __getitem__(self, index: IndexType):  # -> Union[Array, List[Array]]
        """
        Note
            CuPy handles out-of-bounds indices differently from NumPy: NumPy
            handles them by raising an error, but CuPy wraps them around.
            We currently raise an error.
        """
        if isinstance(index, (Device, str)):
            slices = self.on(index)
            return CrossPyArray([self.block_at(slice_.start) for slice_ in slices], axis=0)

        # FIXME: ad hoc, should deal with negative indices
        if self._concat_axis == 0 and isinstance(index, int) and index == -1:
            return self._original_data[-1][-1]

        index = self._indexing_check(index)

        if len(self._lazy_movement):
            raise NotImplementedError("implementing movement operator...")
            self._lazy_movement = defaultdict(list)

        # FIXME: ad hoc for 1-D
        if self._concat_axis == 0 and len(index) == 1:
            if isinstance(index[0], slice):
                slice_ = index[0]
                if slice_.stop == 0 or slice_.start >= len(self):
                    return Initializer([]).finish() # TODO no early return when step < 0
                blkid = self._global_index_to_block_id([slice_.start, slice_.stop - 1])
                nblocks = blkid[1] - blkid[0] + 1
                if nblocks == 0:
                    return Initializer([]).finish() # TODO empty array
                metadata = _Metadata(nblocks, alloc=_pinned_memory_empty)
                if nblocks == 1:
                    metadata.block_offset[0] = slice_.stop - slice_.start
                    metadata.device_idx[0] = self._metadata.device_idx[blkid[0]]
                    metadata.device_offset[0] = 0
                    did = metadata.device_idx[0]
                    device_offset = self._metadata.device_offset[blkid[0]]
                    singleton = self.device_array[did][slice_.start - device_offset:slice_.stop - device_offset]
                    if hasattr(singleton, '__verify__'):
                        singleton.__verify__()
                    device_array = {did: singleton}
                    return CrossPyArray((metadata.block_offset[-1],), self._dtype, metadata, device_array, axis=self._concat_axis)
                # TODO inplace subtract
                # block_offset
                metadata.block_offset[:] = self._metadata.block_offset[blkid[0]:blkid[1] + 1]
                metadata.block_offset -= slice_.start
                metadata.block_offset[-1] = slice_.stop - slice_.start  # TODO step must be 1
                # device_idx
                metadata.device_idx[:] = self._metadata.device_idx[blkid[0]:blkid[1] + 1]
                # device_offset
                metadata.device_offset[:] = self._metadata.device_offset[blkid[0]:blkid[1] + 1]
                metadata.device_offset[:] = self._metadata.block_offset[blkid[0]:blkid[1] + 1] - metadata.device_offset  # accumulated sizes
                accum_sizes = self._metadata.block_offset[:blkid[0]] - self._metadata.device_offset[:blkid[0]]
                # device_array

                perm = metadata.device_idx.argsort(kind='stable')
                aux = metadata.device_idx[perm]
                mask = numpy.empty(aux.shape, dtype=numpy.bool_)
                mask[:1] = True  # first occurence
                mask[1:] = aux[1:] != aux[:-1]
                dids = aux[mask]
                first_blkid = perm[mask] + blkid[0]
                mask[:-1] = mask[1:]
                mask[-1:] = True  # last occurence
                last_blkid = perm[mask] + blkid[0]
                res_blk_to_chk = len(accum_sizes)  # counter for device_offset of prior blocks
                if res_blk_to_chk:
                    trunc_dids = self._metadata.device_idx[:blkid[0]]
                device_array = {}
                for did, bstart, bstop in zip(dids, first_blkid, last_blkid):
                    device_array[did] = self.device_array[did][
                        slice_.start if bstart == 0 else (max(
                            slice_.start,
                            self._metadata.block_offset[bstart - 1]
                        ) - self._metadata.device_offset[bstart]):
                        min(slice_.stop, self._metadata.block_offset[bstop]) -
                        self._metadata.device_offset[bstop]]
                    if res_blk_to_chk or (did == metadata.device_idx[0] and slice_.start) or did == metadata.device_idx[-1]:
                        mask = (metadata.device_idx == did)
                        if res_blk_to_chk:
                            acc_sz_d = accum_sizes[trunc_dids == did]
                            if len(acc_sz_d):
                                metadata.device_offset[mask] -= acc_sz_d[-1]
                                res_blk_to_chk -= len(acc_sz_d)
                        if mask[0]:  # adjustment from first block residual
                            residule = (slice_.start - self._metadata.block_offset[blkid[0] - 1]) if blkid[0] else slice_.start
                            metadata.device_offset[mask] -= residule
                        if mask[-1]:
                            residule = self._metadata.block_offset[blkid[1]] - slice_.stop
                            if residule:
                                metadata.device_offset[-1] -= residule
                metadata.device_offset = metadata.block_offset - metadata.device_offset
                assert metadata.device_offset[0] == 0, metadata.device_offset[0]
                return CrossPyArray((metadata.block_offset[-1],), self._dtype, metadata, device_array, axis=self._concat_axis)
            if isinstance(index[0], int):
                int_ = index[0]
                blkid = self._global_index_to_block_id(int_)
                selection = self.device_array[self._metadata.device_idx[blkid]][int_ - self._metadata.device_offset[blkid]]
                return selection if self._concat_axis == 0 else Initializer(selection, axis = None).finish()
            if isinstance(index[0], list) and all(isinstance(i, bool) for i in index[0]) or is_array(index[0]) and index[0].dtype.kind == 'b':
                bools = index[0]
                assert len(bools) == len(self), IndexError("boolean index did not match indexed array along dimension 0; dimension is %d but corresponding boolean dimension is %d" % (len(self), len(bools)))
                # TODO: assert any(bools)
                if isinstance(bools, CrossPyArray):
                    assert numpy.allclose(self.boundaries, bools.boundaries), NotImplementedError("boolean index array structure mismatch")
                    per_device_result = [_cross_apply((lambda a, b: a[b]), self.device_array[did], bools.device_array[did]) for did in bools.device_array]
                    per_block_result = [x for x in per_device_result if len(x)]  # FIXME device and block may not be 1v1
                else:
                    start = 0
                    per_block_result = []
                    for i,stop in enumerate(self._metadata.block_offset):
                        local_bools = bools[start:stop]
                        if numpy.any(local_bools):
                            per_block_result.append(self._original_data[i][local_bools])
                        start = stop
                return CrossPyArray.fromobject(per_block_result, axis=self._concat_axis if len(per_block_result) else None).finish()
            if isinstance(index[0], (list, tuple)) and all(isinstance(i, int) for i in index[0]) or is_array(index[0]):  # and index[0].dtype != bool:
                global_ints = index[0]
                if isinstance(global_ints, (list, tuple)):
                    global_ints = numpy.asarray(global_ints)
                block_ids = self._global_index_to_block_id(global_ints)
                assert len(block_ids) == len(global_ints)

                obj = []
                for i, block in enumerate(self._original_data):
                    in_range_mask = (block_ids == i)
                    local_ints = global_ints[in_range_mask] - (self.boundaries[i - 1] if i else 0)
                    obj.append(block[local_ints])

                if len(obj) == 1:
                    return CrossPyArray(obj[0], axis=None)
                return CrossPyArray(obj, axis=0)
            raise NotImplementedError("this way of indexing is not supported")
        raise NotImplementedError("Only implemented for 1-D")

        # def _parse_bool_mask(mask):
        #     # assume mask is 1-D
        #     assert len(mask.shape) == 1
        #     return [i for i in range(mask.shape[0]) if mask[i].item()]
        # index = [(_parse_bool_mask(i) if isinstance(i, self.__class__) else i) for i in index]

        # 1. build a new index to data mapping
        # 2. build a new index to device mapping
        # ret = []
        # for k, v in self._index_to_data.items():
        #     local_indices = [
        #         self._index_intersection(
        #             k[d], i if i is not Ellipsis else slice(None)
        #         ) for d, i in enumerate(index)
        #     ]
        #     if all([i is not None for i in local_indices]):
        #         try:
        #             with v.device:
        #                 ret.append(v[tuple(local_indices)])
        #         except:
        #             ret.append(v[tuple(local_indices)])
        # # TODO check out of range in advance
        # if len(ret) == 0:
        #     raise IndexError("Index out of range")
        # # FIXME: shape may change!!!
        # return CrossPyArray.from_array_list(ret)

    def __setitem__(self, index: IndexType, value):
        """
        Assign :param:`value` to a partition which may not on the current device.

        :param index: index of the target partition(s)

        .. todo:
            Assignment of different values to multiple partitions (ndarrays) are currently NOT supported. The :param:`value` is assigned as a whole to each of the target partition(s).
        """
        index = self._indexing_check(index)

        if self._concat_axis == 0 and len(index) == 1:
            if isinstance(index[0], slice):
                slice_ = index[0]
                # check shape
                assert shape_of_slice(index[0]) == len(value), "shape mismatch; broadcasting not implemented"
                assert slice_.step in [None, 1], NotImplementedError("stepping not implemented")

                assert isinstance(value, CrossPyArray), "TODO: np/cp arrays"
                if slice_.start == 0 and slice_.stop == len(self):
                    # TODO check same topology
                    for dst_blk, src_blk in zip(self.device_array.values(), value.device_array.values()):
                        dst_blk[:] = src_blk
                    return

                interal_bounds = self._metadata.block_offset[(slice_.start < self._metadata.block_offset) & (self._metadata.block_offset <= slice_.stop)] - slice_.start
                external_bounds = value._metadata.block_offset
                assert slice_.start + external_bounds[-1] == slice_.stop, "shape mismatch; broadcasting not implemented"
                bounds = numpy.unique(numpy.concatenate((external_bounds, interal_bounds)))
                assert bounds[-1] == external_bounds[-1], f"{bounds[-1]=} {external_bounds[-1]=}"

                start = 0
                for stop in bounds:
                    source_block_id, source_local_slice = value._locate(slice(start, stop))
                    target_block_id, target_local_slice = self._locate(slice(slice_.start + start, slice_.start + stop))
                    src_array = value.device_array[value._metadata.device_idx[source_block_id]]
                    dst_array = self.device_array[self._metadata.device_idx[target_block_id]]
                    from_device = get_device(src_array)
                    to_device = get_device(dst_array)
                    with to_device as here:
                        if from_device == to_device:
                            dst_array[target_local_slice] = src_array[source_local_slice]
                        else:
                            src_buf = src_array[source_local_slice]
                            local_src = fetch(src_buf, here)
                            dst_array[target_local_slice] = local_src
                        # self._lazy_movement[(from_device, to_device)].append((source_obj, source_local_slice, target_obj, target_local_slice))
                    start = stop
                return
            elif isinstance(index[0], int):
                int_ = index[0]
                loc = self._global_index_to_block_id(int_)
                dev_id, dev_offset = self._metadata.device_idx[loc], self._metadata.device_offset[loc]
                block = self.device_array[dev_id]
                # Parla-specific
                if hasattr(block, '_get_compute_device_for_crosspy'):
                    with block._get_compute_device_for_crosspy([block in al for al in self.device_view()].index(True)):
                        block[int(int_ - dev_offset)] = value
                    return
                with get_device(block):
                    block[int(int_ - dev_offset)] = value
                return
            raise NotImplementedError(f"this way of indexing is not supported {index[0]}")
        raise NotImplementedError("Only implemented for 1-D")

        # TODO set is much slower than get

        if self.nparts == 1: # short path
            _local_assignment(self.values()[0], index, value)
            return

        # propagate trivial slice (:)
        if index[0] == slice(None) and isinstance(value, self.__class__) and all(
            ok == ik[:len(ok)] for ok,ik in zip(value.keys(), self.keys())
        ):
            # TODO assuming keys/values ordered
            for src,dst in zip(value.values(), self.values()):
                _local_assignment(dst, index, src)
            return

        def _target_shape(index, caps: list[int]):
            """
            :return: The shape of target region defined by index
            """
            def _per_dim_size(target: BasicIndexType, max: int):
                if isinstance(target, int):
                    return 1
                elif isinstance(target, Iterable):
                    try:
                        return len(target) # len might not be available
                    except:
                        try:
                            return target.shape[0]
                        except:
                            # TODO slow!
                            return sum(
                                [1 for _ in target]
                            )
                elif isinstance(target, slice):
                    if target.step in (None, 1):
                        return (target.stop or max) - (target.start or 0)
                    # TODO slow
                    return sum(
                        [
                            1 for _ in range(
                                target.start or 0, target.stop or max,
                                target.step or 1
                            )
                        ]
                    )
                raise TypeError("unknown index type")

            return [_per_dim_size(i, caps[d]) for d, i in enumerate(index)]

        source_shape_start = [0 for _ in range(len(value.shape))]
        for k, v in self.data_map.items():
            local_indices = [
                self._index_intersection(k[d], i) for d, i in enumerate(index)
            ]
            if all([i is not None for i in local_indices]):
                target_shape = _target_shape(local_indices, [r[1] for r in k])
                for i in range(len(target_shape), len(k)):
                    target_shape.append(k[i][1] - k[i][0]) # fill up remaining dims
                target_shape = [x for x in target_shape if x > 1] # squeeze
                assert len(target_shape) == len(value.shape)
                source_shape_end = [
                    a + b for a, b in
                    zip(source_shape_start, target_shape)
                ]
                source_indices = [
                    slice(start, stop) for start, stop in
                    zip(source_shape_start, source_shape_end)
                ]
                source_shape_start = source_shape_end
                _local_assignment(v, local_indices, value, source_indices)

    def __getattr__(self, name):
        if self._concat_axis is None and self._metadata is not None:
            obj = self._original_data
        elif self.nparts == 1:
            assert len(self.device_array) == 1
            obj = next(iter(self.device_array.values()))
        else:
            raise AttributeError("'%s' object has no attribute '%s'" % (type(self).__name__, name))
        try:
            return getattr(obj, name)
        except AttributeError as e:
            e_obj = e
        try:
            from crosspy.utils.array import get_array_module
            libfunc = getattr(get_array_module(obj), name)
            return lambda *a, **kw: libfunc(obj, *a, **kw)
        except AttributeError as e_lib:
            e_lib.args = (e_obj.args[0] + '; ' + e_lib.args[0],)
            raise e_lib
        raise AttributeError("'%s' object has no attribute '%s'" % (type(self).__name__, name))

    def _locate(self, global_index):
        """
        Returns block id and block-local index.
        Note
            Assume the slice is NOT crossing blocks.
        """
        l2g_offset = lambda block_id: self._metadata.device_offset[block_id]
        if isinstance(global_index, slice):
            global_slice = global_index
            block_id = self._global_index_to_block_id(global_slice.start)
            # TODO check assumption
            dofs = self._metadata.device_offset[block_id]
            local_start = global_slice.start - dofs
            local_stop = global_slice.stop - dofs
            return block_id, slice(local_start, local_stop, global_slice.step)
        # int, numpy.uint64, etc.
        global_int = global_index
        block_id = self._global_index_to_block_id(global_int)
        local_int = global_int - type(global_int)(l2g_offset(block_id))  # int - np.uint64 = np.float64
        return block_id, local_int

    def plan_index_mapping(self, my_indices, other_indices):
        mapping = []
        other_start = [other_indices[d].start for d in range(len(other_indices))]
        for k, v in self.data_map.items():
            local_indices = [
                self._index_intersection(k[d], i)
                for d, i in enumerate(my_indices)
            ]
            other_end = [
                a + b for a, b in zip(other_start, v[local_indices].shape)
            ]
            other_index = [
                slice(start, stop)
                for start, stop in zip(other_start, other_end)
            ]
            mapping.append((other_index, v[local_indices]))
            other_start = other_end
        return mapping

    # TODO unify attr
    def sum(self, axis=None, *args, **kwargs):
        # TODO: assuming 1-D
        new_map = {}
        v0 = None
        vv = None
        reduce = axis in self.distributed_dims or axis is None
        # TODO axis=None
        for k,v in self.data_map.items():
            try:
                with v.device:
                    if reduce and vv is not None:
                        v0 = get_array_module(vv).asarray(vv)
                    vv = get_array_module(v).sum(v, axis=axis)
                    if reduce and v0 is not None:
                        vv += v0
            except:
                if reduce and vv is not None:
                    v0 = get_array_module(vv).asarray(vv)
                vv = get_array_module(v).sum(v, axis=axis)
                if reduce and v0 is not None:
                    vv += v0
            new_map[k] = vv
        return CrossPyArray.from_array_list([vv] if reduce else list(new_map.values()))

    # TODO unify attr
    def argmin(self, axis=None, *args, **kwargs):
        new_map = {}
        for k,v in self.data_map.items():
            try:
                with v.device:
                    vv = get_array_module(v).argmin(v, axis=axis)
            except:
                vv = get_array_module(v).argmin(v, axis=axis)
            new_map[k] = vv
        return CrossPyArray.from_array_list(list(new_map.values()))

    def tobuffer(self, buffer, **ctx_params):
        """Complexity: O(#blocks)"""
        assert len(buffer) >= len(self), f"Buffer is too small ({len(buffer)} < ({len(self)})"
        ctx_params.setdefault('stream', {'non_blocking': True})
        start = 0
        for stop, did, dofs in zip(self._metadata.block_offset, self._metadata.device_idx, self._metadata.device_offset):
            with context(buffer, **ctx_params) as ctx:
                array = self.device_array[did]
                ctx.copy(buffer, slice(start, stop), array, slice(start - dofs, stop - dofs))
                start = stop

    def to(self, placement):
        if isinstance(placement, Iterable):
            return self._to_multidevice(placement)
        else:
            return self.all_to(placement)

    def _to_multidevice(self, placement):
        from ..partition.ldevice import LDeviceSequenceBlocked
        Partitioner = LDeviceSequenceBlocked
        mapper = Partitioner(len(placement), placement=placement)
        arr_p = mapper.partition_tensor(self)
        return CrossPyArray.from_array_list(arr_p)

    def all_to(self, device):
        def _aggregate(concat, pull_op):
            output = None
            # ad hoc
            if not isinstance(self._original_data, list):
                return pull_op(self._original_data)
            output = concat([pull_op(x) for x in self._original_data])
            # legacy
            # for k, v in sorted(self._index_to_data.items()):
            #     pulled = pull_op(v)
            #     if output is None:
            #         output = pulled
            #     else:
            #         diff_dim = -1
            #         shape = [(0, s) for s in output.shape]
            #         assert len(shape) == len(k)
            #         for i, (range1, range2) in enumerate(zip(shape, k)):
            #             if range1 != range2:
            #                 diff_dim = i
            #                 break
            #         output = concat((output, pulled), axis=diff_dim)
            return output

        if (
            isinstance(device, Device) and
            device.__class__.__name__ == "_CPUDevice"
        ) or (isinstance(device, int) and device < 0):
            return _aggregate(numpy.concatenate, cupy.asnumpy)

        try:
            device = getattr(device, "cupy_device")
        except AttributeError:
            device = cupy.cuda.Device(device)
        with device:
            return _aggregate(cupy.concatenate, cupy.asarray)

    def __array__(self, dtype=None):
        """
        `numpy.array` or `numpy.asarray` that converts this array to a numpy array
        will call this __array__ method to obtain a standard numpy.ndarray.
        """
        logger.debug("ALL TO CPU!")
        return self.all_to(-1)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        """
        :param ufunc:   A function like numpy.multiply
        :param method:  A string, differentiating between numpy.multiply(...) and
                        variants like numpy.multiply.outer, numpy.multiply.accumulate,
                        and so on. For the common case, numpy.multiply(...), method == '__call__'.
        :param inputs:  A mixture of different types
        :param kwargs:  Keyword arguments passed to the function
        """
        # One might also consider adding the built-in list type to this
        # list, to support operations like np.add(array_like, list)
        _HANDLED_TYPES = (numpy.ndarray, Number, cupy._core.core.ndarray)
        out = kwargs.get('out', ())
        for x in inputs + out:
            # Only support operations with instances of _HANDLED_TYPES.
            # Use ArrayLike instead of type(self) for isinstance to
            # allow subclasses that don't override __array_ufunc__ to
            # handle ArrayLike objects.
            if not isinstance(x, _HANDLED_TYPES + (CrossPyArray, )):
                logger.debug("not handling", type(x))
                return NotImplemented

        assert method == '__call__', NotImplemented
        assert 0 < len(inputs) < 3, NotImplemented
        assert inputs[0] is self, NotImplemented
        left = inputs[0]
        assert isinstance(left, CrossPyArray)
        per_device_result = {did: _cross_apply(ufunc, block, *inputs[1:]) for did, block in left.device_array.items()}
        return CrossPyArray(left._shape, next(iter(per_device_result.values())).dtype, left._metadata, per_device_result, left._concat_axis)  # TODO ...

        try:
            per_block_result = left.block_view(lambda block: _cross_apply(ufunc, block, *inputs[1:]))
        except ValueError:
            if len(inputs) == 2:
                right = inputs[1]
                if isinstance(right, CrossPyArray):
                    per_block_result = [ufunc(l, r) for l, r in zip(left.block_view(), right.block_view())]
                else:
                    raise NotImplementedError("%s has not been implemented yet" % ufunc)
            else:
                raise NotImplementedError("%s has not been implemented yet" % ufunc)
        return CrossPyArray.fromobject(per_block_result, axis=left.heteroaxis).finish()


        ########
        # LEGACY
        ########

        # Defer to the implementation of the ufunc on unwrapped values.
        # inputs = tuple(x.values() if isinstance(x, CrossPyArray) else x
        #                for x in inputs)
        if out:
            kwargs['out'] = tuple(
                x.values() if isinstance(x, CrossPyArray) else x for x in out
            )

        unwrapped_inputs = []
        last_mapping = None
        for input in inputs:
            if isinstance(input, Number):
                unwrapped_inputs.append([input])
            elif isinstance(input, CrossPyArray):
                try:
                    unwrapped_inputs.append(input.values())
                except:
                    unwrapped_inputs.append(numpy.asarray(input))
                this_mapping = input.keys()
                if last_mapping is None or last_mapping == [()]:
                    last_mapping = this_mapping
                if this_mapping != [()] and not (
                    this_mapping == last_mapping or all(r in n for m in this_mapping for r in m for n in last_mapping)):
                    raise TypeError("inconsistent mappings not supported")
            else:
                return NotImplemented

        # broadcast inputs
        if last_mapping is not None:
            for input in unwrapped_inputs:
                while len(input) < len(last_mapping):
                    input.append(input[0]) # often just 2 inputs
            assert all(len(unwrapped_inputs[0]) == len(i) for i in unwrapped_inputs[1:])
        # result = getattr(ufunc, method)(*inputs, **kwargs)
        result = []
        for fine_inputs in zip(*unwrapped_inputs):
            has_device = [hasattr(i, 'device') for i in fine_inputs]
            if any(has_device):
                with fine_inputs[has_device.index(True)].device: # on lhs device by default
                    fine_inputs = [cupy.asarray(i) for i in fine_inputs]
                    fine_result = getattr(ufunc,
                    method)(*fine_inputs, **kwargs)
            else:
                fine_result = getattr(ufunc,
                    method)(*fine_inputs, **kwargs)
            result.append(fine_result)

        if type(result) is tuple:
            # multiple return values
            return tuple(type(self).from_array_list(x) for x in result)
        elif method == 'at':
            # no return value
            return None
        else:
            # one return value
            return type(self)(result)  # self.__class__(result)

        return NotImplemented

    def __array_function__(self, func, types, args, kwargs):
        if func not in HANDLED_FUNCTIONS:
            return NotImplemented
        # Note: this allows subclasses that don't override
        # __array_function__ to handle DiagonalArray objects.
        if not all(issubclass(t, self.__class__) for t in types):
            return NotImplemented
        return HANDLED_FUNCTIONS[func](*args, **kwargs)

    def device_view(self, *, split=True, return_slices=False):
        """Coarse-grained view per device.
        If `return_slices` is True, `split` is ignored as if it's True
        """
        if not split and not return_slices:
            yield from self.device_array.items()
            return
        for did, array in self.device_array.items():
            res = []
            if self._metadata.device_idx[0] == did:
                slice_ = slice(0, self._metadata.block_offset[0])
                res.append(slice_ if return_slices else array[slice_])
            if len(self._metadata.device_idx) == 1:
                assert len(self.device_array) == 1
                yield res
                return
            mask = (self._metadata.device_idx[1:] == did)
            dofs = self._metadata.device_offset[1:][mask]
            starts = self._metadata.block_offset[:-1][mask] - dofs
            stops = self._metadata.block_offset[1:][mask] - dofs
            for start, stop in zip(starts, stops):
                slice_ = slice(start, stop)
                res.append(slice_ if return_slices else array[slice_])
            yield res


    def block_view(self, apply=None):
        start = 0
        for stop, did, dofs in zip(self._metadata.block_offset, self._metadata.device_idx, self._metadata.device_offset):
            if apply is not None:
                yield apply(self.device_array[did][start - dofs:stop - dofs])
            else:
                yield self.device_array[did][start - dofs:stop - dofs]
            start = stop

    @property
    def blockview(self):
        return CrossPyArray.BlockView(self)

    class BlockView:
        def __init__(self, xpa: 'CrossPyArray'):
            self.array = xpa

        def __getitem__(self, index):
            assert index >= 0, "Negative index not supported"
            # very ad hoc; assuming ordered keys
            dview = self.array.to_dict()
            for k in dview:
                if index == 0:
                    return dview[k]
                index -= 1
            raise Exception("Oops, it's so fragile right now...")

@implements(numpy.sum)
def _sum(a, axis=None):
    "Implementation of np.sum for CrossPyArray objects"
    return a.sum(axis)


class _CrossPyArrayType(ArrayType):
    def can_assign_from(self, a, b):
        # TODO: We should be able to do direct copies from numpy to cupy arrays, but it doesn't seem to be working.
        # return isinstance(b, (cupy.ndarray, numpy.ndarray))
        raise NotImplementedError
        return isinstance(b, _Array)

    def get_memory(self, a):
        raise NotImplementedError
        return gpu(a.device.id).memory()

    def get_array_module(self, a):
        import sys
        return sys.modules[__name__]


register_array_type(CrossPyArray)(_CrossPyArrayType())
