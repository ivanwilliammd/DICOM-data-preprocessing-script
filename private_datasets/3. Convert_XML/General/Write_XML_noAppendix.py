"""
Last updated Apr 2019
by @ivanwilliammd
"""

import glob
import os
import numpy as np
import IPython 
import pandas as pd
import csv 
import IPython
from decimal import Decimal


    ## Path of input CSV                     --> change to # for full
path_to_combined_csv="D:\\CSV\\Combined_full.csv"
    ## Extract combined CSV header
df_combined = pd.read_csv(path_to_combined_csv)
df_combined_select = df_combined[['Nomor','Namafolder','Subfolder','Namafile','Xpix','Ypix','Zdown','Spacing','Size_mm','Xbound','Ybound','Zorigin','TipeNodul']]
df_combined_select

total_combined_data=df_combined_select.shape[0]

Namafolder_Previous='first'
Nomor_Previous=99999
Zorigin_Previous=99999.999
Total_entries=df_combined_select.Nomor.unique()
Last_entries= Total_entries[-1]
Total_patient=df_combined_select.Namafolder.unique()
Num_total_patient=len(Total_patient)

print ('There are %s nodules annotation at %s' % (Last_entries, Num_total_patient))


########################################################################################################################################################################

def write_XML_annotation_header(Namafolder, Subfolder, Namafile, Nomor, ClassSphericity, ClassNodul, ClassMargin, Zorigin, Xbound, Ybound):

	## Path to output XML
	path_to_output_xml="D:\\XML\\"+str(Namafolder)+".xml"
	f = open(path_to_output_xml, "w+")

	f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
	f.write('<LidcReadMessage uid="%s" xmlns="http://www.nih.gov" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nih.gov  http://troll.rad.med.umich.edu/lidc/LidcReadMessage.xsd">\n' %Namafolder)
	f.write('<ResponseHeader>\n')
	f.write('<Version>1.8.1</Version>\n')
	f.write('<MessageId>00000</MessageId>\n')
	f.write('<DateRequest>1900-01-01</DateRequest>\n')
	f.write('<TimeRequest>00:00:00</TimeRequest>\n')
	f.write('<RequestingSite>removed</RequestingSite>\n')
	f.write('<ServicingSite>removed</ServicingSite>\n')
	f.write('<TaskDescription>Second unblinded read</TaskDescription>\n')
	f.write('<CtImageFile>removed</CtImageFile>\n')
	f.write('<SeriesInstanceUid>%s</SeriesInstanceUid>\n' % Subfolder)
	f.write('<DateService>1900-01-01</DateService>\n')
	f.write('<TimeService>00:00:00</TimeService>\n')
	f.write('<ResponseDescription>1 - Reading complete</ResponseDescription>\n')
	f.write('<StudyInstanceUID>%s</StudyInstanceUID></ResponseHeader>\n' % Namafolder)
	f.write('<readingSession>\n')
	f.write('    <annotationVersion>3.12</annotationVersion>\n')
	f.write('    <servicingRadiologistID>anonymous</servicingRadiologistID>\n')
	f.write('    <unblindedReadNodule>\n')
	f.write('      <noduleID>Nodule %0*d</noduleID>\n' % (4, Nomor))
	f.write('      <characteristics>\n')
	f.write('        <subtlety>5</subtlety>\n')
	f.write('        <internalStructure>1</internalStructure>\n')
	f.write('        <calcification>5</calcification>\n')
	f.write('        <sphericity>%d</sphericity>\n' % ClassSphericity)
	f.write('        <margin>%d</margin>\n' % ClassMargin)
	f.write('        <lobulation>2</lobulation>\n')
	f.write('        <spiculation>2</spiculation>\n')
	f.write('        <texture>%d</texture>\n' % ClassNodul)
	f.write('        <malignancy>%d</malignancy>\n' % ClassNodul)
	f.write('      </characteristics>\n')
	f.write('      <roi>\n')
	f.write('        <imageZposition>%f </imageZposition>\n' % Zorigin)
	f.write('        <imageSOP_UID>%s</imageSOP_UID>\n' % Namafile)
	f.write('        <inclusion>TRUE</inclusion>\n')
	f.write('        <edgeMap>\n')
	f.write('          <xCoord>%d</xCoord>\n' % Xbound)
	f.write('          <yCoord>%d</yCoord>\n' % Ybound)
	f.write('        </edgeMap>\n')


	return[]

def write_edgemap(Xbound, Ybound):
	## Path to output XML
	path_to_output_xml="D:\\XML\\"+str(Namafolder)+".xml"
	f = open(path_to_output_xml, "a")

	f.write('        <edgeMap>\n')
	f.write('          <xCoord>%d</xCoord>\n' % Xbound)
	f.write('          <yCoord>%d</yCoord>\n' % Ybound)
	f.write('        </edgeMap>\n')
	return[]

def write_new_roi(Zorigin, Namafile, Xbound, Ybound):
	## Path to output XML
	path_to_output_xml="D:\\XML\\"+str(Namafolder)+".xml"
	f = open(path_to_output_xml, "a")
	
	f.write('      </roi>\n')
	f.write('      <roi>\n')
	f.write('        <imageZposition>%f </imageZposition>\n' % Zorigin)
	f.write('        <imageSOP_UID>%s</imageSOP_UID>\n' % Namafile)
	f.write('        <inclusion>TRUE</inclusion>\n')
	f.write('        <edgeMap>\n')
	f.write('          <xCoord>%d</xCoord>\n' % Xbound)
	f.write('          <yCoord>%d</yCoord>\n' % Ybound)
	f.write('        </edgeMap>\n')
	return[]

def write_new_nodule(Nomor, ClassSphericity, ClassNodul, ClassMargin, Zorigin, Xbound, Ybound):
	## Path to output XML
	path_to_output_xml="D:\\XML\\"+str(Namafolder)+".xml"
	f = open(path_to_output_xml, "a")
	f.write('      </roi>\n')

	f.write('    </unblindedReadNodule>\n')
	f.write('    <unblindedReadNodule>\n')
	f.write('      <noduleID>Nodule %0*d</noduleID>\n' % (4, Nomor))
	f.write('      <characteristics>\n')
	f.write('        <subtlety>5</subtlety>\n')
	f.write('        <internalStructure>1</internalStructure>\n')
	f.write('        <calcification>5</calcification>\n')
	f.write('        <sphericity>%d</sphericity>\n' % ClassSphericity)
	f.write('        <margin>%d</margin>\n' % ClassMargin)
	f.write('        <lobulation>2</lobulation>\n')
	f.write('        <spiculation>2</spiculation>\n')
	f.write('        <texture>%d</texture>\n' % ClassNodul)
	f.write('        <malignancy>%d</malignancy>\n' % ClassNodul)
	f.write('      </characteristics>\n')
	f.write('      <roi>\n')
	f.write('        <imageZposition>%f </imageZposition>\n' % Zorigin)
	f.write('        <imageSOP_UID>%s</imageSOP_UID>\n' % Namafile)
	f.write('        <inclusion>TRUE</inclusion>\n')
	f.write('        <edgeMap>\n')
	f.write('          <xCoord>%d</xCoord>\n' % Xbound)
	f.write('          <yCoord>%d</yCoord>\n' % Ybound)
	f.write('        </edgeMap>\n')
	return[]

def close_current_XML_file(Namafolder_Previous):
	## Path to output XML
	path_to_output_xml="D:\\XML\\"+str(Namafolder_Previous)+".xml"
	f = open(path_to_output_xml, "a")

	f.write('      </roi>\n')
	f.write('    </unblindedReadNodule>\n')
	f.write('</readingSession>\n')
	f.write('</LidcReadMessage>')	
	print("D:\\XML\\"+str(Namafolder_Previous)+".xml successfuly created")
	f.close()
	# import IPython;IPython.embed()
	return []

########################################################################################################################################################################

## Reading CSV Data recursively
for i in range(total_combined_data):
	percentage = 100*(i+1)/total_combined_data
	print('    Progress: %d out of %d         (%.2f percent)' % (i+1, total_combined_data, percentage))

	Nomor = df_combined_select.iloc[[i]].Nomor.values[0]
	Namafolder = df_combined_select.iloc[[i]].Namafolder.values[0]
	Subfolder = df_combined_select.iloc[[i]].Subfolder.values[0]
	Namafile = df_combined_select.iloc[[i]].Namafile.values[0]
	Xbound = df_combined_select.iloc[[i]].Xbound.values[0]
	Ybound = df_combined_select.iloc[[i]].Ybound.values[0]
	Zorigin = df_combined_select.iloc[[i]].Zorigin.values[0]
	TipeNodul = df_combined_select.iloc[[i]].TipeNodul.values[0]
	Size_mm = df_combined_select.iloc[[i]].Size_mm.values[0]

    ## Create ClassNodul & ClassMargin
	if TipeNodul=="solid":
		ClassNodul=5
		ClassMargin=5
	else:
		if TipeNodul=="subsolid":
			ClassNodul=3
			ClassMargin=3
		else:
			if TipeNodul=="groundglass":
				ClassNodul=1
				ClassMargin=1
			else:
				#Consider it solid
				ClassNodul=5
				ClassMargin=5

	## Create ClassSphericity
	if Size_mm<10:
		ClassSphericity=3
	else:
		ClassSphericity=5

    ## Structuring XML Tree
	if Namafolder_Previous==Namafolder:
		if Nomor_Previous==Nomor:
			if Zorigin_Previous==Zorigin.copy():
				write_edgemap(Xbound,Ybound)
			else:
				write_new_roi(Zorigin, Namafile, Xbound, Ybound)
		else:
			write_new_nodule(Nomor, ClassSphericity, ClassNodul, ClassMargin, Zorigin, Xbound, Ybound)
	else:
		if Nomor_Previous==99999:
			write_XML_annotation_header(Namafolder, Subfolder, Namafile, Nomor, ClassSphericity, ClassNodul, ClassMargin, Zorigin, Xbound, Ybound)
		else:
			close_current_XML_file(Namafolder_Previous)
			write_XML_annotation_header(Namafolder, Subfolder, Namafile, Nomor, ClassSphericity, ClassNodul, ClassMargin, Zorigin, Xbound, Ybound)

	#For last file to input close_XML_file
	if i+1==total_combined_data:
		close_current_XML_file(Namafolder_Previous)
		print ('Finishing converting %s annotation rows for %s' % (total_combined_data, Num_total_patient))
	else:
		print()

    ## Store parameter to prevent doubling
	Namafolder_Previous=Namafolder
	Nomor_Previous=Nomor
	Zorigin_Previous=Zorigin