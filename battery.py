import multiprocessing as mp
import os, shutil, psutil
import numpy as np

# List of test-cases to run in the battery

case_name = ['vertical_container', 'dam_break', 'rubber_gate', 'thermo_square']
base = os.getcwd()

# Set the environment variables (must be removed)

os.environ['PYTHONPATH'] += f'{base}:'
os.environ['PYTHONPATH'] += f'{base}/pyStream/build:'
os.environ['PYTHONPATH'] += f'{base}/../Metafor/oo_meta:'
os.environ['PYTHONPATH'] += f'{base}/../Metafor/oo_metaB/bin:'
os.environ['PYTHONPATH'] += f'{base}/../PFEM3D/build/bin:'

# Make the workspace and clear previous results

if os.path.exists('workspace'): shutil.rmtree('workspace')
os.mkdir('workspace')

def run_test(case_name: str):
    '''
    Run a single test-case on two specific CPU sockets
    '''

    rank = mp.current_process()._identity[0]
    cpu_1, cpu_2 = (rank-1)+(rank-1), rank+(rank-1)

    print(f'Rank {rank} : CPU {cpu_1, cpu_2} - {case_name}')

    # Bind the MPI process to specific CPU sokets

    opt = f'mpiexec --bind-to core --cpu-set {cpu_1},{cpu_2} -n 2'
    run = f'{opt} python3 {base}/examples/2D/{case_name}/main.py'

    # Run the test-case and plot the results

    os.chdir(f'{base}/workspace')
    os.mkdir(case_name)
    os.chdir(case_name)

    os.system(f'{run} 2>&1 | tee workspace.txt > /dev/null')

# Run the battery on all available physical cores

n_proc = psutil.cpu_count(logical = False)
pool = mp.Pool(n_proc//2)
pool.map(run_test, case_name)