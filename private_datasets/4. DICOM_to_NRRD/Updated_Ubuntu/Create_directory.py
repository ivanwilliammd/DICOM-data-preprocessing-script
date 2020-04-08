# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 12:28:19 2018

@author: Michael Goetz (m.goetz@dkfz-heidelberg.de)
"""

import glob
import os
import subprocess
import SimpleITK as sitk
import numpy as np
import lidcXmlHelper as xmlHelper
import IPython

# Path to the command lines tools of MITK Phenotyping

# Path to the folder that contains the LIDC-IDRI DICOM files
path_to_dicoms = "/media/ivanwilliam/BINUS_DATA/THESIS/Private_DB_Moscow_ORInConverted/CT Scan RAW/DICOM"

# Path to the folder that contains the LIDC-IDRI XML files
path_to_xmls= "/media/ivanwilliam/BINUS_DATA/XML_Results_Full"
path_to_nrrds =  "/media/ivanwilliam/BINUS_DATA/Moscow_NRRD_Output/nrrd_file"
path_to_error_file="/media/ivanwilliam/BINUS_DATA/Moscow_NRRD_Output/conversion_error_log.txt"

planar_template=r"template.pf"



def write_error(msg, errorfile=path_to_error_file):
    """ 
    A simple error logging method. Errors should be reported using this functions.
    All errors are then logged in the file specified with the global variable
    'path_to_error_file' if no other file is specified.
    
    The error message is also printed in the main text. 
    """
    a=open(errorfile,'a')
    a.write(str(msg) + "\n")
    a.close()
    print("ERROR:",msg)

def get_dicom_from_study_uid(study_uid, series_uid):
    """
    Find the folder containing the dicoms that corresponds to a given study id
    or an study id and a series id.
    
    Returns:
        The path to the DICOMs matching the given IDs
        The number of DICOMs that had been found.
    """
    # if series_uid is not None:
    all_dirs = os.listdir(path_to_dicoms)
    matching = [s for s in all_dirs if study_uid in s]


    search_path=os.path.join(path_to_dicoms, matching[0], series_uid)
    dicoms_file=os.listdir(search_path)
    num_dicoms=len(dicoms_file)

    if num_dicoms > 0:
        return search_path, num_dicoms
    else:
        return [], 0
    
def create_nrrd_from_dicoms(image, patient_id):
    """
    Reads a folder that contains multiple DICOM files and 
    converts the input into a single nrrd file using a command line 
    app from MITK or MITK Phenotyping. 
    
    Input:
        * path to one dicom (other are automatically found.)
        * Patient ID
    
    Output:
        Creates a single nrrd file with the path: $target_path / patient_id + '_ct_scan.nrrd'
    
    """
    target_path = os.path.join(path_to_nrrds, patient_id)
    target_name = os.path.join(target_path, patient_id+"_ct_scan.nrrd")
    os.makedirs(target_path, exist_ok=True)
    # file = open(target_name, 'w+')
    # file.close()
    
    return target_name


def parse_xml_file(file):
    # Create an XML Tree, use own method to remove namespaces 
    root=xmlHelper.create_xml_tree(file)
    
    # IPython.embed()

    # Find the Study and Series IDs if possible
    study_uid=xmlHelper.get_study_uid(root)
    series_uid=xmlHelper.get_series_uid(root)
    print("Parsing %s" % file)
    print("Get study_uid %s and series_uid %s" % (study_uid, series_uid))
    if study_uid is None:
        write_error("Failed to find Study UID: " + file)
        return
    
    # Find the DICOMS matching the study and series ID. 
    # Assuming that all DICOMS to a study/series ID are in one folder. 
    dicom_path, no_of_dicoms=get_dicom_from_study_uid(study_uid, series_uid)
    if no_of_dicoms < 10:
        print(dicom_path)
        print("No DICOM's found for file:",file)
        return
    print(dicom_path)

    # Files are saved in a folder with the structure $PatientID/$StudyID/$SeriesID/$DicomName
    # Removing StudyID, SeriesID and DICOM-Name gives a patient ID --> StudyUID
    # long_patient_id=os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(dicom_path))))
    patient_id=study_uid
    
    # For some patients, more than one scan is provided (for example due to multiple
    # time points). To ensure that each time point is only scanned one, an appendix
    # is added to the patient_id, ensuring that multiple time points can be selected. 
    appendix=file[-5]
    patient_id =patient_id+appendix
    print(patient_id)
            # break
    
    # Create Nrrd files from DICOMS and reading spacing and orgiin. 
    nrrd_file=create_nrrd_from_dicoms(dicom_path, patient_id)
    # spacing, origin = get_spacing_and_origin(nrrd_file)

xml_dirs = os.listdir(path_to_xmls)
tot_xml = len(xml_dirs)
xml_dirs= sorted(xml_dirs, key=str)
dir_it=0
for dir_it in range(tot_xml):
    xml_file = os.path.join(path_to_xmls, xml_dirs[dir_it])
    print('    Opening %d out of %d XML' % (dir_it+1, tot_xml))
    print(xml_file)
    parse_xml_file(xml_file)