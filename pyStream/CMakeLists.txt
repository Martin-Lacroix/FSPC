cmake_minimum_required(VERSION 3.15)
project(PythonStream)

# Name the Swig module and setup the compilation flags

set(SWIG_MODULE python_stream)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC")

# Compile a static library with the C++ code

add_library(${PROJECT_NAME} STATIC ${SWIG_MODULE}.cpp)
include_directories(${PROJECT_SOURCE_DIR})

# Find the Swig and the Python libraries

find_package(SWIG REQUIRED)
include(${SWIG_USE_FILE})

find_package(PythonLibs REQUIRED)
include_directories(${PYTHON_INCLUDE_PATH})

# Provide the language and link the Swig module with the library

set_source_files_properties(${SWIG_MODULE}.i PROPERTIES CPLUSPLUS ON)
swig_add_library(${SWIG_MODULE} LANGUAGE python SOURCES ${SWIG_MODULE}.i)
swig_link_libraries(${SWIG_MODULE} ${PROJECT_NAME} ${PYTHON_LIBRARIES})
