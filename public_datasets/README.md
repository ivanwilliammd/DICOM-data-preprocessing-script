# Public and private CT scan dataset DICOM Preprocessing Scripts
## Warning: Depecrated version (Apr 2019), Unstable


DICOM Preprocessing script for DICOM conversion of public and private CT scan datasets
Some scripts are adapted from [LIDC-IDRI-preprocessing](https://github.com/MIC-DKFZ/LIDC-IDRI-processing)

## Requirements:
1. OS: Windows
2. Standard python libraries (glob, os, subprocess, xml) and scikit packages (numpy, pandas, scikit package, and xml)
3. SimpleITK Library

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
