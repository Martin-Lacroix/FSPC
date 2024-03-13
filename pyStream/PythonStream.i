%include std_streambuf.i

// Add necessary symbols to generated header

%module python_stream %{
    #include "PythonStream.h"
%}
%include "PythonStream.h"
