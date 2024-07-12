%include std_streambuf.i

// Add the necessary symbols to the generated header

%module python_stream %{
    #include "python_stream.h"
%}

// We also need to include the python_stream header here

%include "python_stream.h"
