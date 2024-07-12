# Re-create the output folders

rm -rf build
mkdir build
cd build

# Compile the code in release with CMake

cmake -DCMAKE_BUILD_TYPE=Release ..
make -j8
