#include <iostream>
#include <streambuf>

// |-----------------------------------------------|
// | Convert couts and cerr into python streams    |
// |-----------------------------------------------|

class PyCerrCout: public std::basic_streambuf<char>
{
    public:

    ~PyCerrCout();
    PyCerrCout(std::ostream &ostream, bool err=false);

    private:

    std::ostream &stream;
    std:: streambuf *oldbuf;
    bool errstream;

    protected:

    virtual std:: streamsize xsputn(const char* input, std:: streamsize size);
    virtual std::char_traits<char>:: int_type overflow(int input);
};

// |-----------------------------------------------|
// | Redirect all cpp terminal prints to Python    |
// |-----------------------------------------------|

class Redirect
{
    public: Redirect();
    private:

    PyCerrCout out;
    PyCerrCout err;
};