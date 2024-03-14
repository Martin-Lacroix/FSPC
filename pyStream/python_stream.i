%include std_streambuf.i

// Add necessary symbols to generated header

%module python_stream %{
    #include "python_stream.h"
%}
%include "python_stream.h"
