%include std_streambuf.i

// Add necessary symbols to generated header

%module pyStream %{
    #include "PythonStream.h"
%}
%include "PythonStream.h"
