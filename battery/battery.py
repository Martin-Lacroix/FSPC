import multiprocessing as mp
import os, shutil

base = os.getcwd()
case_name = ['dam_break', 'mooney_hyper', 'thermo_square', 'vertical_container']

os.environ['PYTHONPATH'] += base+'/../FSPC:'
os.environ['PYTHONPATH'] += base+'/../FSPC/pyStream/build:'
os.environ['PYTHONPATH'] += base+'/../Metafor/oo_meta:'
os.environ['PYTHONPATH'] += base+'/../Metafor/oo_metaB/bin:'
os.environ['PYTHONPATH'] += base+'/../PFEM3D/build/bin:'

if os.path.exists('workspace'): shutil.rmtree('workspace')
os.mkdir('workspace')

def run_test(case_name: str):

    os.chdir(base+'/workspace')
    rank = str(mp.current_process()._identity[0])

    print('Rank',rank, '-', case_name)
    
    run = '-rf '+base+'/battery/rank_files/rankfile_'+rank+'.txt '
    run += '-n 2 python3 '+base+'/examples/2D/'+case_name+'/main.py'

    os.mkdir(case_name)
    os.chdir(case_name)

    os.system('mpiexec '+run+' 2>&1 | tee workspace.txt > /dev/null')
    os.system('python3 '+base+'/battery/'+case_name+'.py')

pool = mp.Pool(4)
pool.map(run_test, case_name)