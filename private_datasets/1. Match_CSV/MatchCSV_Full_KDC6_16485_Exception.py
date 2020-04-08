"""
Last updated Apr 2019
by @ivanwilliammd
"""

import glob
import os
import numpy as np
import h5py
import IPython 
import pandas as pd
import csv 
import IPython
import math

    ## Path to original DICOM_Metadata CSV file   --> change to # for full
# path_to_dicom_csv="D:\CSV\Metadata_DICOM_Moscow_Sample.csv"
path_to_dicom_csv="D:\CSV\Metadata_DICOM_Moscow_full.csv"
name_to_dicom_csv=path_to_dicom_csv.split("\\")


    ## Path to original CSV with XYZ positive axis --> change to # for full
# path_to_ori_csv="D:\CSV\lung_annotation_raw_Final_Sample.csv"
path_to_ori_csv="D:\CSV\lung_annotation_raw_Final_KDC6_16485.csv"
name_to_ori_csv=path_to_ori_csv.split("\\")

    ## Path to output CSV with                     --> change to # for full
# path_to_output="D:\CSV\Combined_Sample.csv"
path_to_output="D:\CSV\Combined_KDC6_16485.csv"

    ## Open output CSV file and adding header
csv_file=open(path_to_output, mode='w+')
csv_file.write('Nomor,Namafolder,Subfolder,Namafile,Xpix,Ypix,Zdown,Spacing,Size_mm,Xbound,Ybound,Zorigin,TipeNodul\n')
print('Matching metadata info from %s with %s table........... \n   Adding header .................. \n' % (name_to_ori_csv[-1], name_to_dicom_csv[-1]))


    ## Extract DICOM_Metadata CSV header
df_dicom = pd.read_csv(path_to_dicom_csv)
df_dicom_select = df_dicom[['Namafolder','Subfolder','Namafile','OriginX','OriginY','OriginZ','Spacing','Slice_Location']]
df_dicom_select

    ## Extract original CSV header
df_ori = pd.read_csv(path_to_ori_csv)
df_ori_select = df_ori[['Acc_Num','X_coor','Y_coor','Zdown_coor','Size_mm','Type']]
df_ori_select

total_ori_data=df_ori_select.shape[0]
print('  There are %d total data need to be matched' % (total_ori_data))

def xy_bound (Xpix, Ypix, bound_addition):
    num_bound_addition=len(bound_addition)
    Xbound_list=[]
    Ybound_list=[]
    #left side border
    for p in range(num_bound_addition):
        Xbound = Xpix+bound_addition[0]
        Ybound = Ypix+bound_addition[p]
        Xbound_list.append(Xbound)
        Ybound_list.append(Ybound)
        
    #Right side border
    for p in range(num_bound_addition):
        Xbound = Xpix+bound_addition[-1]
        Ybound = Ypix+bound_addition[p]
        Xbound_list.append(Xbound)
        Ybound_list.append(Ybound)
    
    #Lower border
    for p in range(num_bound_addition-2):
        Xbound = Xpix+bound_addition[p+1]
        Ybound = Ypix+bound_addition[0]
        Xbound_list.append(Xbound)
        Ybound_list.append(Ybound)
    
    #Upper border
    for p in range(num_bound_addition-2):
        Xbound = Xpix+bound_addition[p+1]
        Ybound = Ypix+bound_addition[-1]
        Xbound_list.append(Xbound)
        Ybound_list.append(Ybound)
    return [Xbound_list, Ybound_list]

def Z_slice(Zdown, num_slice):
    ## Get information from sorted OriginZ
    pos=int(Zdown)-1
    slice_dev=int(num_slice/2)
    
    Namafolder = dfSortMatch.iloc[[pos]].Namafolder.values[0]
    Subfolder = dfSortMatch.iloc[[pos]].Subfolder.values[0]
    Spacing = dfSortMatch.iloc[[pos]].Spacing.values[0]
    totalZ = dfSortMatch.shape[0]
    Zorigin_list=[]
    Namafile_list=[]

    for x in range(num_slice):
        j = int(pos)-int(slice_dev)+x
        if j>0 and j<totalZ:
        	j=j
        else:
        	if j<0:
        		j=0
        	else:
        		j=totalZ-2

        Zorigin = dfSortMatch.iloc[[j]].OriginZ.values[0]
        Namafile = dfSortMatch.iloc[[j]].Namafile.values[0]
            
        Zorigin_list.append(Zorigin)
        Namafile_list.append(Namafile)
    return [Zorigin_list, Namafolder, Subfolder, Namafile_list, Spacing]

def find_thickness(k):
    if '0.5' in Unique_Subfolder[k]:
            slice_thick = 0.5
    else:
        if '1.0' in Unique_Subfolder[k]:
            slice_thick = 1.0
        else:
            if '5.0' in Unique_Subfolder[k]:
                slice_thick = 5.0
    print('    Slice thickness : %s ' % slice_thick)
    return slice_thick

def getRatio(z, num_slice):
    medZ=num_slice/2
    if z==medZ or (z>(0.45*medZ) and z<(0.55*medZ)):
        ratio = 1
    else:
        ratio=1-math.exp(-medZ/abs(z-medZ))
#         print('Edge slice, ratio adjusted to %f' % ratio)
    return ratio

k=2956

dfSortMatch=pd.DataFrame()

for i in range(total_ori_data):
    print('    Progress: %d out of %d ' % (i+1, total_ori_data))
    Acc_Num = df_ori_select.iloc[[i]].Acc_Num.values[0]
    Xpix = df_ori_select.iloc[[i]].X_coor.values[0]
    Ypix = df_ori_select.iloc[[i]].Y_coor.values[0]
    Zdown = df_ori_select.iloc[[i]].Zdown_coor.values[0]
    Size_mm = df_ori_select.iloc[[i]].Size_mm.values[0]
    TipeNodul = df_ori_select.iloc[[i]].Type.values[0]
    Nomor = i+1+k
    RoI_Num = 0
    
    print('    Finding match using keyword %s ' % Acc_Num)
    dfMatch=df_dicom_select[df_dicom_select['Namafolder'].str.match(Acc_Num)]
    total_match=dfMatch.shape[0]
    Unique_Subfolder=dfMatch.Subfolder.unique()
    count_typeSubs= len(Unique_Subfolder)
     
    ## If directory type only have one folder/type of CT scan for example LungOnly or Body Only
    if count_typeSubs==1:
        dfSortMatch=dfMatch.copy()
        dfSortMatch.sort_values("OriginZ", axis=0, ascending=True, inplace=True)
        
        k=0
        slice_thick = find_thickness(k)

        # Feeding number of slice to find Z information
        num_slice = int(Size_mm/slice_thick)
        Zorigin_list, Namafolder, Subfolder, Namafile_list, Spacing = Z_slice(Zdown, num_slice)
        num_slice = len(Zorigin_list)
        
        # Getting box_coor in 2D images at each Z
        pixel_box = int((Size_mm/Spacing)/2)
        bound_addition=np.arange(-pixel_box, pixel_box+1)
        Xbound_list, Ybound_list = xy_bound(Xpix, Ypix, bound_addition)
        
        for z in range(num_slice):
            #scaling the bounding boxes at the bordering 10 slice (latest 10 slice)
            ratio = getRatio(z, num_slice)
            num_of_pix_box = len(Xbound_list)*ratio
            for p in range(int(num_of_pix_box)):
                RoI_Num=RoI_Num+1
                
                diffX=Xbound_list[p]-Xpix
                diffY=Ybound_list[p]-Ypix
                            
                Xbound=int(Xpix + ratio*diffX)
                Ybound=int(Ypix + ratio*diffY)
                csv_file.write(str(Nomor)+','+str(Namafolder)+','+str(Subfolder)+','+str(Namafile_list[z])+','+str(Xpix)+','+str(Ypix)+','+str(Zdown)+','+str(slice_thick)+','+str(Size_mm)+','+str(Xbound)+','+str(Ybound)+','+str(Zorigin_list[z])+','+str(TipeNodul)+'\n')
#                 print('    Writing '+str(Namafolder)+','+str(Subfolder)+','+str(Namafile_list[z])+','+str(Xpix)+','+str(Ypix)+','+str(Zdown)+','+str(slice_thick)+','+str(Size_mm)+','+str(Xbound)+','+str(Ybound)+','+str(Zorigin_list[z])+','+str(TipeNodul))
                
                RoI_Num=RoI_Num+1
        print('Total RoI made = %d' % RoI_Num)
        
    ## If directory have two folder/type of CT scan Lung and Body
    else:
        for k in range(count_typeSubs):
            keySubs=Unique_Subfolder[k]
            dfSortMatch=dfMatch[dfMatch['Subfolder'].str.contains(keySubs[3:7])]
            dfSortMatch.sort_values("OriginZ", axis=0, ascending=True, inplace=True)
            slice_thick = find_thickness(k)

            # Feeding number of slice to find Z information
            num_slice = int(Size_mm/slice_thick)
            Zorigin_list, Namafolder, Subfolder, Namafile_list, Spacing = Z_slice(Zdown, num_slice)
            num_slice = len(Zorigin_list)

            # Getting box_coor in 2D images at each Z
            pixel_box = int((Size_mm/Spacing)/2)
            bound_addition=np.arange(-pixel_box, pixel_box+1)
            Xbound_list, Ybound_list = xy_bound(Xpix, Ypix, bound_addition)

            for z in range(num_slice):
                #scaling the bounding boxes at the bordering 10 slice (latest 10 slice)
                ratio = getRatio(z, num_slice)
                num_of_pix_box = len(Xbound_list)*ratio
                for p in range(int(num_of_pix_box)):
                    RoI_Num=RoI_Num+1

                    diffX=Xbound_list[p]-Xpix
                    diffY=Ybound_list[p]-Ypix

                    Xbound=int(Xpix + ratio*diffX)
                    Ybound=int(Ypix + ratio*diffY)
                    csv_file.write(str(Nomor)+','+str(Namafolder)+','+str(Subfolder)+','+str(Namafile_list[z])+','+str(Xpix)+','+str(Ypix)+','+str(Zdown)+','+str(slice_thick)+','+str(Size_mm)+','+str(Xbound)+','+str(Ybound)+','+str(Zorigin_list[z])+','+str(TipeNodul)+'\n')
#                     print('    Writing '+str(Namafolder)+','+str(Subfolder)+','+str(Namafile_list[z])+','+str(Xpix)+','+str(Ypix)+','+str(Zdown)+','+str(slice_thick)+','+str(Size_mm)+','+str(Xbound)+','+str(Ybound)+','+str(Zorigin_list[z])+','+str(TipeNodul))
                    RoI_Num=RoI_Num+1
        print('Total RoI made = %d' % RoI_Num)
        
csv_file.close()
print('Finish, csv_file Closed')