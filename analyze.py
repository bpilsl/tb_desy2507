import re
import os
import sys
import argparse
from glob import glob

def runCorry(config, files, log, additional=None):
    # cmd = f'corry -c {config} -o EventLoaderEUDAQ2.file_name={files[0]} -o EventLoaderEUDAQ2:TLU_0.file_name={files[1]} -o EventLoaderEUDAQ2:RD50_MPWx_0.file_name={files[2]}   -o EventLoaderMuPixTelescope.input_file={files[3]} -l {log} '
    cmd = f'corry -c {config} -o EventLoaderEUDAQ2.file_name={files[0]} -o EventLoaderEUDAQ2:TLU_0.file_name={files[1]} -o EventLoaderEUDAQ2:RD50_MPWx_0.file_name={files[2]} -l {log} '
    if additional:
        cmd += additional
    print(cmd)  
    os.system(cmd)  

runs = sys.argv[1]
geo = sys.argv[2]

telDir = 'data/adenium'
tluDir = 'data/tlu'
telepixDir = 'data/telepix2'
dutDir = 'data/mpw4'

dirs = [telDir, tluDir, telepixDir, dutDir]


first = last = 0

if '-' in runs:
    splitted = runs.split('-')
    first = int(splitted[0])
    last = int(splitted[1])
else:
    first = last = int(runs)

for runNmb in range(first, last + 1):
    files = []
    for d in dirs:
        files.append(glob(f'{d}/*run{runNmb:06}.*')[0])
        
    # files.append(os.path.basename(glob(f'telepix/rawData/single_run_{runNmb:06}.blck')[0]))

    runCorry('analysis.cfg', files, f'logs/log_ana{runNmb:06}.txt', f'-o histogram_file=analysis_{runNmb:06}.root -o detectors_file={geo}')
