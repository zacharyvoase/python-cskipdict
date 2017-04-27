from ._skiplist import ffi, lib


_undefined = object()


class ObjectRef(object):

    def __init__(self):
        self.__alloc = ffi.new('uintptr_t **')
        self.ref = ffi.cast('void **', self.__alloc)

    @property
    def deref(self):
        return ffi.from_handle(ffi.cast('void *', self.ref[0]))


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
            self.__pointers.discard(prev.deref)

    def __delitem__(self, k):
        prev = ObjectRef()
        did_remove = lib.skiplist_remove(self.__list, k, prev.ref)
        if not did_remove:
            raise KeyError(k)
        self.__pointers.discard(prev.deref)

    def pop(self, k, default=_undefined):
        prev = ObjectRef()
        did_remove = lib.skiplist_remove(self.__list, k, prev.ref)
        if not did_remove:
            if default is _undefined:
                raise KeyError(k)
            return default
        popped = prev.deref
        self.__pointers.discard(prev)
        return popped

    def __iter__(self):
        for k, v in self.iteritems():
            yield k

    def iteritems(self):
        node = self.__list.head.next[0]
        while node:
            yield (node.key, ffi.from_handle(node.val))
            node = node.next[0]


def main():
    skipdict = SkipDict()
    skipdict[1] = 'a'
    skipdict[2] = 'b'
    assert len(skipdict) == 2
    assert skipdict[1] == 'a'
    assert skipdict[2] == 'b'
    assert 1 in skipdict
    assert 2 in skipdict
    assert 3 not in skipdict
    for k, v in skipdict.iteritems():
        print '({}, {})'.format(k, v)
    skipdict[0] = 'c'
    print ''
    for k, v in skipdict.iteritems():
        print '({}, {})'.format(k, v)
    print ''
    print 'd.pop(0) == {!r}'.format(skipdict.pop(0))
    print 'd.pop(1) == {!r}'.format(skipdict.pop(1))
    assert len(skipdict) == 1


if __name__ == '__main__':
    main()
