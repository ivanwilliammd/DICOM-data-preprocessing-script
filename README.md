# Public and private CT scan dataset DICOM Preprocessing Scripts
## Warning: Depecrated version for academic usage (Apr 2019), Unstable

DICOM Preprocessing script for DICOM conversion of public and private CT scan datasets
Some scripts are adapted from [LIDC-IDRI-preprocessing](https://github.com/MIC-DKFZ/LIDC-IDRI-processing)

## Requirements:
1. OS: Windows
2. Standard python libraries (glob, os, subprocess, xml), jupyter notebook, and scikit packages (numpy, pandas, scikit package, and xml)
3. SimpleITK Library

## See more information related to DICOM Preprocessing:
1. [MITK phenotyping](http://mitk.org/wiki/Phenotyping)
2. [3D slicer](https://www.slicer.org/)

## For public datasets
* Download data from the [LIDC-IDRI website](https://wiki.cancerimagingarchive.net/display/Public/LIDC-IDRI) --> Download DICOM files and XML annotations using the "NBIA Data Retrriever" and choose "Classic Directory Name" option instead of "Descriptive Directory Name".
* Change the paths in "lidc_data_to_nifti.py"
	* path_to_executables : Path where the command line tool from MITK Phenotyping can be found
	* path_to_dicoms : Folder which contains the DICOM image files (not the segmentation dicoms)
	* path_to_xmls : Folder that contains the XML which describes the nodules Following output paths needs to be defined:
	* path_to_nrrds : Folder that will contain the created Nrrd / Nifti Files
	* path_to_planars :Folder that will contain the Planar figure for each subject
	* path_to_characteristics : Path to a CSV File, where the characteristic of a nodule will be stored. If the file exists, the new content will be appended.
	* path_to_error_file : Path to an error file where error messages are written to. Existing files will be appended.
* Run the script "lidc_data_to_nifti.py"

## For private datasets
* Run the folder in numbered sequence and adapt it to your private datasets annotation
	1. Match_CSV annotation
	2. Read_Metadata_from_DICOM
	3. Convert_XML
	4. DICOM_to_NRRD
* If you have some problem related to automatic script preprocessing, please use 3rd party apps mentioned above (MITK Phenotyping/3D Slicer) to manually convert your datasets to NRRD files

## Output files on Subfolders:
1. NRRD-Files (Whole DICOM series)
2. Planar Figures (pixel-wise masking of nodules in single plane)
3. Nifti file/nii.gz (segmentation of nodule)

------------------------------------------------------------------------------
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

```http://www.apache.org/licenses/LICENSE-2.0```

------------------------------------------------------------------------------
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
******************************************************************************
