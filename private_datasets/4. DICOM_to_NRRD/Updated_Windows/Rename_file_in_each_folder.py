import glob
import os
import subprocess
import numpy as np
import IPython
import sys, os

# Input path to NRRD file
path_to_nrrd = r"D:\Moscow_NRRD_Output\nrrd_file"

all_dirs = os.listdir(path_to_nrrd)
tot_dirs = len(all_dirs)
dir_it=0

for dir_it in range(tot_dirs):
    file_path = os.path.join(path_to_nrrd, all_dirs[dir_it])
    percentage= 100*(dir_it+1)/tot_dirs
    print('Opening %s \t\t\t\t\t\t\t\t\t\t\t %d out of %d folder (%d percent)' % (all_dirs[dir_it], dir_it+1, tot_dirs, percentage))
    for root, dirs, files in os.walk(file_path):

        fileName = sorted(files, key=str)
        N_file = len(fileName)
        
        i=0
        k = 0
        if i in range(N_file):
            for fileName in sorted (files, key=str):
                file_path_dcm = os.path.join(root, fileName)
                
                patient_id=all_dirs[dir_it]
                target_name = os.path.join(root, patient_id+"_ct_scan.nrrd")
                os.rename(file_path_dcm, target_name)
                print('\tFile with name: '+str(fileName)+' converted to '+str(patient_id)+"_ct_scan.nrrd")
                
        else:
        	print("Next folder ......")