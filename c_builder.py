from cffi import FFI

builder = FFI()

builder.set_source("library", """
                    #include "clib/library.h"
                    
                    """,
                   sources = ['clib/library.c'])

builder.cdef("""
             void cube_vertices(float* buffer, int x, int y, int z, float n, int fill);
             void cube_vertices_x(float* buffer, int x, int y, int z, float n);
            """)


if __name__ == '__main__':
    builder.compile(verbose = True)
