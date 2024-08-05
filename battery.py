import multiprocessing as mp
import os, psutil

# Multiple instances of this function are spawn

def run_test(test_case: str):
    '''
    Run a single test-case on two specific CPU sockets
    '''

    case_name = test_case.replace('/', '_')

    # Compute the dedicated CPU sockets based on the MPI rank

    rank = mp.current_process()._identity[0]
    cpu_1, cpu_2 = (rank-1)+(rank-1), rank+(rank-1)

    print(f'Rank {rank} : CPU {cpu_1, cpu_2} - {case_name}')

    # Bind the MPI process to specific CPU sokets

    opt = f'mpiexec --bind-to core --cpu-set {cpu_1},{cpu_2} -n 2'
    run = f'{opt} python3 {base}/examples/{test_case}/main.py'

    # Run the test-case and plot the results

    os.mkdir(case_name)
    os.chdir(case_name)

    os.system(f'{run} 2>&1 | tee workspace.txt > /dev/null')
    os.chdir('..')

# Get the base folder and total number of physical cores

base = os.path.dirname(__file__)
n_proc = psutil.cpu_count(logical = False)

# List of test cases to run in the battery

test_list = list()

test_list.append('2D/dam_break')
test_list.append('2D/rubber_gate')
test_list.append('2D/thermo_square')
test_list.append('2D/vertical_container')
test_list.append('3D/clamped_plate')

# Run the battery on all available physical cores

pool = mp.Pool(n_proc//2)
pool.map(run_test, test_list)
