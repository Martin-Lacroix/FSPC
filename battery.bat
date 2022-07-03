:: Set input file

set LIST=MarcoLucio SimoneMeduri GuiFourey ZiFeiMeng

:: Clean the output folder

rd /s /q workspace
mkdir workspace

:: Runs the test battery

set MKL_NUM_THREADS=8
set OMP_NUM_THREADS=8
set OMP_PROC_BIND=true

FOR %%A IN (%LIST%) DO (

    echo Run : %%A
    mpiexec -n 2 python main.py -k 1 examples\%%A\input.py
    timeout 5
)

:: Check the results

FOR %%A IN (%LIST%) DO (

    echo Check : %%A
    start python graphs\%%A.py
)