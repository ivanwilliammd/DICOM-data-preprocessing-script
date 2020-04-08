import glob
import os
import subprocess
import SimpleITK as sitk
import numpy as np
import csv 
import IPython
import SimpleITK as sitk
import sys, os

# Input path to DICOMS file
# path_to_dicoms = r"D:\THESIS\Private_DB_Moscow_ORInConverted\CT Scan RAW\DICOM" ###full database site
path_to_dicoms = r"D:\DICOM_Moscow"

all_dirs = os.listdir(path_to_dicoms)
tot_dirs = len(all_dirs)
dir_it=0

for dir_it in range(tot_dirs):
    file_path = os.path.join(path_to_dicoms, all_dirs[dir_it])
    print('    Opening %d out of %d folder' % (dir_it+1, tot_dirs))
    for root, dirs, files in os.walk(file_path):

        fileName = sorted(files, key=str)
        N_file = len(fileName)
        
        i = 1
        k = 0
        if i in range(N_file):
            for fileName in sorted (files, key=str):
                file_path_dcm = os.path.join(root, fileName)
                renamed_file = str(fileName)+".dcm"
                file_rename_result = os.path.join(root, renamed_file)
                os.rename(file_path_dcm, file_rename_result)
                # file_path_dcm = os.path.join(root, fileName)
                # selected_image = sitk.ReadImage(file_path_dcm)
                # print('\n\tFound %d out of %d DICOM: %s \n' % (i, N_file, file_path_dcm))
                # i=i+1
                # print('\tMetadata info:')
        else:
        	print("Next folder ......")