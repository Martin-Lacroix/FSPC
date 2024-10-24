#include "python_stream.h"
#include <Python.h>
#include <stdio.h>

// Convert C++ couts and cerr into python streams

PyCerrCout::PyCerrCout(std::ostream& ostream, bool err):
stream(ostream), errstream(err)
{
    oldbuf = stream.rdbuf();
    stream.rdbuf(this);
}

// Bring back to the normal cout and cerr behaviour 

PyCerrCout::~PyCerrCout()
{
    stream.rdbuf(oldbuf);
}

std::streamsize PyCerrCout::xsputn(const char* input, std::streamsize size)
{
    // Initialize and fix the maximum stream size

    std::string str(input, size);
    static const std::streamsize max_size = 1000;
    std::streamsize written = std::min(size, max_size);

    // Acquire the global interpreter lock using the Python API

    PyGILState_STATE gstate = PyGILState_Ensure();

    // Check the if the stream variable is a stderr or a stdout

    if(errstream) PySys_WriteStderr("%s", str.c_str());
    else PySys_WriteStdout("%s", str.c_str());

    // Release the global interpreter lock and return

    PyGILState_Release(gstate);
    return written;
}

int PyCerrCout::overflow(int input)
{
    if(input != EOF)
    {
        // Acquire the global interpreter lock using the Python API

        PyGILState_STATE gstate = PyGILState_Ensure();

        // Check the if the stream variable is a stderr or a stdout

        if(errstream) PySys_WriteStderr("%c", input);
        else PySys_WriteStdout("%c", input);

        // Release the global interpreter lock and return

        PyGILState_Release(gstate);
    }
    return input;
}

// Actually defines the python stream redirrector class

Redirect::Redirect():
out(std::cout), err(std::cerr, true){}