# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 10:25:12 2019

@author: GAjmera121451
"""
import numpy as np
import pandas as pd
from PIL import Image
#%% Get Defect List from KLARF file
klarfpath = r"\\amat.com\folders\Israel\PL_Storage\BF\Users\Girish@PLStorage\For Marcelo\FullMapKLARF_NL_V1_2.001"
klarfpath = r"C:\Users\GAjmera121451\Desktop\Field Support\LETI Accuracy\UV_Acc_test\ADR_NO_GDR.001"
klarfpath = r"C:\Users\GAjmera121451\Desktop\Field Support\LETI Accuracy\UV_Acc_test\ADR_with_GDR.001"

def KLARF_to_DF(klarfpath):

  lines = []
  count = 0
  defectdatastartline = 0
  defectdataendline = 0
  multitifffilepath = 0
  testplans = 0

  with open(klarfpath,"rt") as klarffileid:
      for line in klarffileid:

        if line.find("TiffFileName")!=-1:
          TiffFileName = line[14:-3]
          multitifffilepath=1

        if line.find("InspectionTest")!=-1:
          testplans = testplans+1

        if line.find("DefectRecordSpec")!=-1:
          columnheader = line[20:-2].split(" ")
          defectdatastartline = count+2

        if line.find("SummarySpec")!=-1:
          defectdataendline = count-1
          line = line.replace(";","")

        if line.find("SummaryList")!=-1:
          summaryliststartline = count+1

        lines.append(line.rstrip("\n"))
        count=count+1


      defectlist = lines[defectdatastartline:defectdataendline+1]
      defectlist[-1] =defectlist[-1].replace(';','')
      summarylist = [i.replace(';','').split(" ") for i in lines[summaryliststartline:summaryliststartline+testplans]]

      if summarylist[0][0] == "":
        temp_summary_start = 1
      else:
        temp_summary_start = 0



  defectheader = columnheader
  otfheader = ['DEFECTID', 'IMAGEID', 'IMAGECODE']

  for index,row in enumerate(defectlist):
      if len(defectlist[index].split(" ")) > 3: # Defect Row
        if defectlist[index].split(" ")[0] == "":
          temp_defect_start = 1
        else:
          temp_defect_start = 0
      else: # OTF Row
        if defectlist[index].split(" ")[0] == "":
          temp_otf_start = 1
          break
        else:
          temp_otf_start = 0
          break

  noofdefectcolumn = len(defectheader)
  noofdefects = 0
  for k in summarylist:
    noofdefects = noofdefects + int(k[temp_summary_start+1])
  defectlocation_np = np.zeros((noofdefects,len(columnheader)))

  # noofotfcolumn = len(otfheader)
  # noofotfimages = len(defectlist)-noofdefects
  # otflocation_np = np.zeros((noofotfimages,len(otfheader)))

  index_defect = -1
  index_otf = -1

  for index,row in enumerate(defectlist):
      if len(defectlist[index].split(" ")) > 3:
        index_defect = index_defect + 1
        defectlocation_np[index_defect,range(noofdefectcolumn)] = row.split(" ")[temp_defect_start:(noofdefectcolumn+temp_defect_start)]
      # else:
      #   index_otf = index_otf+1
      #   otflocation_np[index_otf,0] = defectlocation_np[index_defect,0]
      #   otflocation_np[index_otf,1:3] = row.split(" ")[temp_otf_start:(noofotfcolumn-1+temp_otf_start)]

  defectlocation_df = pd.DataFrame(defectlocation_np,columns = columnheader)
  # otflocation_df = pd.DataFrame(otflocation_np,columns = otfheader)

  # OTFImageType_dict = {300:'BF Current',310:'BF Previous',320:'BF Next',330:'BF Diff',
  #                    301:'GF Current',311:'GF Previous',321:'GF Next',331:'GF Diff'}

  # otflocation_df = otflocation_df.replace({"IMAGECODE" : OTFImageType_dict})

  return defectlocation_df,#otflocation_df


#%% Load Image from Multi Tiff File for a specifc Image ID
def load_img_multitiff(path,target_size=None,ImageID = 1):

    img = Image.open(path)
    img.seek(ImageID)
    if img.mode != 'RGB':
      img = img.convert('RGB')

#    if target_size is not None and img._size is not target_size:
#        width_height_tuple = (target_size[1], target_size[0])
#        if img.size != width_height_tuple:
#            img = img.resize(width_height_tuple, Image.NEAREST)

    return img

#%% For Testing the Function
k = KLARF_to_DF(klarfpath)
DefectList = k[0]
DefectList = DefectList.loc[(DefectList!=0).any(axis=1)]
DefectList.to_csv('WithGDR.csv')
#import os
#from PIL import Image
#import matplotlib.pyplot as plt
#
#klarfpath = r"\\amat.com\folders\Israel\PL_Storage\BF\DEMOS\YMTC_CH_Sept_19\YMTC_CH_FullWafer_Unified.001"
#defectlocation_df,otflocation_df = KLARF_to_DF(klarfpath)
#
#folderpath, klarffilename = os.path.split(klarfpath)
#TiffFileName = folderpath + "//" + klarffilename[:-3] +"I01"
#
#
#
#otfimage = Image.open(TiffFileName,"r")
#otfimage_np = np.zeros((len(otflocation_df),otfimage.width,otfimage.height),dtype = np.uint8)
#
## Access a specific Image
#DefectID = 345
#ImageType = 'GF Previous'
#ImageID = int(otflocation_df.loc[(otflocation_df['DEFECTID'] == DefectID) & (otflocation_df['IMAGECODE'] == ImageType),'IMAGEID'].values[0])
#
#otfimage.seek(ImageID)
#otfimage_np[ImageID,:,:] = np.asarray(otfimage)
#plt.imshow(otfimage_np[ImageID,:,:])

#






