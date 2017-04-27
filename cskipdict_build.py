import os

from cffi import FFI


skiplist_header_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build', 'skiplist.h')
include_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'c')

ffibuilder = FFI()

with open(skiplist_header_file) as header_file:
    ffibuilder.cdef(header_file.read())

ffibuilder.set_source('cskipdict._skiplist', '''
#define SKIPLIST_IMPLEMENTATION
#include "skiplist-config.h"
#include "skiplist-template.h"
int skiplist_uint64_cmp(uint64_t a, uint64_t b, void *userdata);

int skiplist_uint64_cmp(uint64_t a, uint64_t b, void *userdata) {
  return (a > b) - (a < b);
}
''', include_dirs=[include_dir])


if __name__ == '__main__':
    ffibuilder.compile(verbose=True)
