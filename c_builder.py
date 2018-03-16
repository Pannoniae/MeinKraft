from cffi import FFI

builder = FFI()

builder.set_source("library", """
                    #include "clib/library.h"
                    
                    """,
                   sources = ['clib/library.c'])

builder.cdef("""
             int main();
            """)


if __name__ == '__main__':
    builder.compile(verbose = True)
