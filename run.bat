:: Set input file

set INPUT=examples\damNcomp\input.py

:: Clean output folder

rd /s /q workspace
mkdir workspace

:: Runs the code

set MKL_NUM_THREADS=8
set OMP_NUM_THREADS=8
set OMP_PROC_BIND=true

:: python main.py -k 8 %INPUT%


mpiexec -n 2 python main.py -k 8 %INPUT%