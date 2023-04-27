import ctypes

# g++ -fPic -shared -o nomefile.so nomefile.cpp
# clibrary = ctypes.CDLL('/home/jean/MEGA/PYTHON-T/lang2/Clibrary/sorting.so',mode=ctypes.RTLD_GLOBAL)
clibrary = ctypes.CDLL('Clibrary/sorting.so')
