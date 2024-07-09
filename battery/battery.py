import multiprocessing as mp
import os, shutil, psutil
import numpy as np

# List of test-cases to run in the battery

case_name = ['vertical_container', 'dam_break', 'rubber_gate', 'thermo_square']
base = os.getcwd()

# Set the environment variables (must be removed)

os.environ['PYTHONPATH'] += base+'/../FSPC:'
os.environ['PYTHONPATH'] += base+'/../FSPC/pyStream/build:'
os.environ['PYTHONPATH'] += base+'/../Metafor/oo_meta:'
os.environ['PYTHONPATH'] += base+'/../Metafor/oo_metaB/bin:'
os.environ['PYTHONPATH'] += base+'/../PFEM3D/build/bin:'

# Make the workspace and clear previous results

if os.path.exists('workspace'): shutil.rmtree('workspace')
os.mkdir('workspace')

def run_test(case_name: str):
    '''
    Run a single test-case on two specific CPU sockets
    '''

    rank = mp.current_process()._identity[0]
    cpu_bind = [(rank-1)+(rank-1), rank+(rank-1)]

    print('Rank', rank, '- CPU', cpu_bind, '-', case_name)

    # Bind the MPI process to specific CPU sokets

    os.sched_setaffinity(0, cpu_bind)
    opt = 'mpiexec --bind-to core --cpu-set {},{} -n 2'.format(*cpu_bind)
    run = '{} python3 {}/examples/2D/{}/main.py'.format(opt, base, case_name)

    # Run the test-case and plot the results

    os.chdir('{}/workspace'.format(base))
    os.mkdir(case_name)
    os.chdir(case_name)

    os.system('{} 2>&1 | tee workspace.txt > /dev/null'.format(run))
    os.system('python3 {}/battery/{}.py'.format(base, case_name))

# Run the battery on all available physical cores

n_proc = psutil.cpu_count(logical = False)
pool = mp.Pool(n_proc//2)
pool.map(run_test, case_name)