import re
import os
import sys
import argparse
from glob import glob

def runCorry(config, files, log, additional=None):
    """
    Function to execute the Corry software with the given parameters.
    Args:
        config: The configuration file to use.
        files: A list of files required by Corry.
        log: Log file where the output will be saved.
        additional: Optional string with additional arguments to pass to Corry.
    """
    cmd = f'corry -c {config} -o EventLoaderEUDAQ2.file_name={files[0]} -o EventLoaderEUDAQ2:TLU_0.file_name={files[1]} -o EventLoaderEUDAQ2:RD50_MPWx_0.file_name={files[2]}   -o EventLoaderMuPixTelescope.input_file={files[3]} -l {log} '
    # cmd = f'corry -c {config} -o EventLoaderEUDAQ2.file_name={files[0]} -o EventLoaderEUDAQ2:TLU_0.file_name={files[1]} -o EventLoaderEUDAQ2:RD50_MPWx_0.file_name={files[2]} -l {log} '
    if additional:
        cmd += additional
    print('\n\n ####### RUNNING: ', cmd,'\n\n')  
    os.system(cmd)

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Run Corry software with specific configurations and data files.')
    
    # Define the arguments the script expects
    parser.add_argument('runNmb', type=int, nargs='+', help='List of run numbers used to align.')
    parser.add_argument('initialGeo', type=str, help='Path to the initial geometry file.')
    # parser.add_argument('finalGeo', type=str, help='Path to the final geometry file.')

    # Parse the arguments
    args = parser.parse_args()


    print('aligning run(s) %s' %args.runNmb)
    for runNmb in args.runNmb:
        initialGeo = args.initialGeo
        finalGeo = f'geo/aligned/full-run{runNmb:06}.geo'


        telDir = 'data/adenium'
        tluDir = 'data/tlu' 
        telepixDir = 'data/telepix'       
        dutDir = 'data/mpw4'        

        dirs = [telDir, tluDir, dutDir]        

        files = []

        # Globbing the telescope and TLU data files based on the run number
        # We use globbing to find files matching the specific run number pattern
        for d in dirs:
            print(f'Globbing for files in directory {d} with run number {runNmb:06}')
            files_found = glob(f'{d}/*run*{runNmb:06}*')
            if files_found:
                files.append(files_found[0])  # Append the first matched file
            else:
                print(f"No files found for run {runNmb:06} in {d}")
                continue
                # sys.exit(1)  # Exit if no matching files are found
        
        tpData = glob(f'{telepixDir}/*run*{runNmb}*.blck')
        tpData = tpData[0].split('/')[-1]
        files.append(tpData)

        print('found ', files)

        # # Globbing the telepix2 block file for the given run number
        # print(f'Globbing for telepix2 block file for run {runNmb:06}')
        # telepix_file_found = glob(f'data/telepix2/single_run_{runNmb:06}.blck')
        # if telepix_file_found:
        #     files.append(os.path.basename(telepix_file_found[0]))  # Append the block file
        # else:
        #     print(f"No telepix2 block file found for run {runNmb:06}")
        #     continue
        #     # sys.exit(1)                  

        # Running the Corry software with different configuration files
        runCorry('prealign.conf', files, 'logs/log_prealign.txt', f'-o detectors_file={initialGeo}')# -g RD50_MPWx_0.mask_file={mask_file[0]}')
        runCorry('align_mille.conf', files, 'logs/log_align_mille.txt', f'-o detectors_file_updated={finalGeo}')

if __name__ == "__main__":
    main()
