from ._skiplist import ffi, lib


_undefined = object()


class ObjectRef(object):

    def __init__(self):
        self.__alloc = ffi.new('uintptr_t **')
        self.ref = ffi.cast('void **', self.__alloc)

    @property
    def handle(self):
        return ffi.cast('void *', self.ref[0])

    @property
    def deref(self):
        return ffi.from_handle(self.handle)


class SkipDict(object):

    __slots__ = ('__list', '__pointers')

    def __init__(self):
        self.__list = ffi.new('skiplist_skiplist *')
        self.__pointers = set()
        init_err = lib.skiplist_init(
            self.__list,
            ffi.addressof(lib, 'skiplist_uint64_cmp'),
            # Null `void *userdata` for cmp, iter, and alloc functions
            ffi.NULL,
            ffi.NULL,
            ffi.NULL)
        if init_err:
            raise RuntimeError("Error initializing skiplist")

    def __del__(self):
        lib.skiplist_free(self.__list)

    def __repr__(self):
        return 'SkipDict({' + ', '.join('{!r}: {!r}'.format(k, v) for k, v in self.iteritems()) + '})'

    def __len__(self):
        return lib.skiplist_size(self.__list)

    def __contains__(self, k):
        return bool(lib.skiplist_find(self.__list, k, ffi.NULL))

    def __nonzero__(self):
        return len(self) > 0

    def __getitem__(self, k):
        result = lib.skiplist_get(self.__list, k, ffi.NULL)
        if result == ffi.NULL:
            raise KeyError(k)
        return ffi.from_handle(result)

    def get(self, k, default=None):
        result = lib.skiplist_get(self.__list, k, ffi.NULL)
        if result == ffi.NULL:
            return default
        return ffi.from_handle(result)

    def __setitem__(self, k, value):
        handle = ffi.new_handle(value)
        self.__pointers.add(handle)
        prev = ObjectRef()
        did_overwrite = lib.skiplist_insert(self.__list, k, handle, prev.ref)
        if did_overwrite:
            self.__pointers.discard(prev.handle)

    def __delitem__(self, k):
        prev = ObjectRef()
        did_remove = lib.skiplist_remove(self.__list, k, prev.ref)
        if not did_remove:
            raise KeyError(k)
        self.__pointers.discard(prev.handle)

    def pop(self, k, default=_undefined):
        prev = ObjectRef()
        did_remove = lib.skiplist_remove(self.__list, k, prev.ref)
        if not did_remove:
            if default is _undefined:
                raise KeyError(k)
            return default
        popped = prev.deref
        self.__pointers.discard(prev.handle)
        return popped

    def __iter__(self):
        for k, v in self.iteritems():
            yield k

    def iteritems(self):
        node = self.__list.head
        while node.next[0]:
            yield (node.next[0].key, ffi.from_handle(node.next[0].val))
            node = node.next[0]

    def minimum(self):
        key_pointer = ffi.new('uint64_t *')
        val_ref = ObjectRef()
        has_result = lib.skiplist_min(self.__list, key_pointer, val_ref.ref)
        if not has_result:
            return None
        return (key_pointer[0], val_ref.deref)

    def maximum(self):
        key_pointer = ffi.new('uint64_t *')
        val_ref = ObjectRef()
        has_result = lib.skiplist_max(self.__list, key_pointer, val_ref.ref)
        if not has_result:
            return None
        return (key_pointer[0], val_ref.deref)

    def pop_minimum(self):
        key_pointer = ffi.new('uint64_t *')
        val_ref = ObjectRef()
        has_result = lib.skiplist_pop(self.__list, key_pointer, val_ref.ref)
        if not has_result:
            return None
        output = (key_pointer[0], val_ref.deref)
        self.__pointers.discard(val_ref.handle)
        return output

    def pop_maximum(self):
        key_pointer = ffi.new('uint64_t *')
        val_ref = ObjectRef()
        has_result = lib.skiplist_shift(self.__list, key_pointer, val_ref.ref)
        if not has_result:
            return None
        output = (key_pointer[0], val_ref.deref)
        self.__pointers.discard(val_ref.handle)
        return output
