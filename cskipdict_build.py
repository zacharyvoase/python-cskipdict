import os

from cffi import FFI


src_root = os.path.join(os.path.dirname(__file__), 'cskipdict', 'headers')
skiplist_header_file = os.path.join(src_root, 'skiplist.cdef')

ffibuilder = FFI()

with open(skiplist_header_file) as header_file:
    ffibuilder.cdef(header_file.read())

ffibuilder.set_source('cskipdict._skiplist', '''
extern "C" {
    #define SKIPLIST_IMPLEMENTATION
    #include "skiplist-config.h"
    #include "skiplist-template.h"
    int skiplist_int64_cmp(int64_t a, int64_t b, void *userdata);

    int skiplist_int64_cmp(int64_t a, int64_t b, void *userdata) {
    return (a > b) - (a < b);
    }
}
''',
include_dirs=[src_root],
sources=[os.path.join(src_root, 'random_uniform.cpp')],
extra_compile_args=['-std=c++11'],
source_extension='.cpp')


if __name__ == '__main__':
    ffibuilder.compile(verbose=True)
