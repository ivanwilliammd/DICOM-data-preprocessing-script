#### Ivan William Harsono-Converting Private database with x, y, z coordinate to LIDC format XML ####
#### Convention of x, y, z --> x, y = (0,0) at upper left, z counted from the lowest point"


import glob
import os
import subprocess
import SimpleITK as sitk
import numpy as np
import csv 
import IPython
# import lidcXmlHelper as xmlHelperfrom __future__ import print_function
import SimpleITK as sitk
import sys, os


# Input path to DICOMS file
path_to_dicoms = r"D:\THESIS\Private_DB_Moscow_ORInConverted\CT Scan RAW\DICOM" ###full database site
# path_to_dicoms = r"D:\DICOM_Moscow"

# Output path to Metadata file
path_to_metadata_info = r"D:\Metadata_DICOM_Moscow_full.csv"
# Open the csv file --> append
csv_file=open(path_to_metadata_info, mode='w+') # ganti ke mode='a' kalau sdh ada isinya
csv_file.write('Namafolder,Subfolder,Namafile,OriginX,OriginY,OriginZ,Spacing,Slice_Location,pixel_type\n')
print('Create CSV containing metadata info %s ........... \n   Adding header .................. ' % path_to_metadata_info)


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
                selected_image = sitk.ReadImage(file_path_dcm)
                print('\n\tFound %d out of %d DICOM: %s \n' % (i, N_file, file_path_dcm))
                i=i+1
                print('\tMetadata info:')
                
                origin = selected_image.GetOrigin() #0020/0032
                size = selected_image.GetSize()
                spacing = selected_image.GetSpacing()
                direction = selected_image.GetDirection()
                location = selected_image.GetDepth()
                pixel_type = selected_image.GetPixelIDTypeAsString()
                
                for k in selected_image.GetMetaDataKeys():
                    v = selected_image.GetMetaData(k)
                    if k=='0020|1041':
                        slice_location = v
#                     if k=='0020|0032':
#                         extract = v
#                         tuplet = extract.split("\\")
#                         z_val = tuplet[2]
                                            
                
#                 print('origin: ' + str(origin))
#                 print('size: ' + str(size))
#                 print('spacing: ' + str(spacing[0]))
#                 print('direction: ' + str(direction))
#                 print('slice location: ' + str(slice_location))
# #                 print('image_z_position_value: ' + str(z_val)) # sama dengan origin[2]
#                 print('pixel type: ' + str(pixel_type))
#                 print('\t')
    
                if 'AGFA' in file_path_dcm:
                    Nama_folder=all_dirs[dir_it][1:17]
                else:
                    if 'KDC6' in file_path_dcm:
                        Nama_folder=all_dirs[dir_it][1:11]
                
                dir_split = root.split('\\')
                subs=dir_split[-1]                                
                                    
                print('\t'+str(Nama_folder)+','+str(subs)+','+str(fileName)+','+str(origin[0])+','+str(origin[1])+','+str(origin[2])+','+str(spacing[0])+','+str(slice_location)+','+str(pixel_type)+'\n')
                csv_file.write(str(Nama_folder)+','+str(subs)+','+str(fileName)+','+str(origin[0])+','+str(origin[1])+','+str(origin[2])+','+str(spacing[0])+','+str(slice_location)+','+str(pixel_type)+'\n')
csv_file.close()
print('CSV File close')