cmake_minimum_required(VERSION 3.15)
project(PythonStream)

# Setup the compilation options

set(CMAKE_SWIG_FLAGS "")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC")

# Create a static library for the Cpp code

add_library(${PROJECT_NAME} STATIC ${PROJECT_NAME}.cpp)
include_directories(${PROJECT_SOURCE_DIR})

# Find Swig and Python libraries

find_package(SWIG REQUIRED)
include(${SWIG_USE_FILE})

find_package(PythonLibs REQUIRED)
include_directories(${PYTHON_INCLUDE_PATH})

# Link the Swig module with thye Cpp code

set_source_files_properties(${PROJECT_NAME}.i PROPERTIES CPLUSPLUS ON)
swig_add_library(python_stream LANGUAGE python SOURCES ${PROJECT_NAME}.i)
swig_link_libraries(python_stream ${PROJECT_NAME} ${PYTHON_LIBRARIES})
