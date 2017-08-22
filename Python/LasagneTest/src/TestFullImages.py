# -*- coding: utf-8 -*-

#Usage : python TestFullImages.py TestModel.pkl ../DataSource.txt 1,2,3 12 number of classes

#This code runs the model on each pixel of a test image as a sliding window. On a SPOT images it takes ages to run. Highly inefficient

from __future__ import print_function
from PIL import Image
from osgeo import gdal
from osgeo.gdalconst import GA_ReadOnly
import sys
import os
import pickle
import numpy as np
import pdb
import datetime


#define parameters
modelPath = '../Models/'
outputPath = '../Output/'
TAG = "3Channel_GAUSSIAN_LCN_MAXPOOL_1_2_Removed"

if not os.path.exists(outputPath):
   os.mkdir(outputPath);
if not os.path.exists(modelPath):
   os.mkdir(modelPath);

imageFile = sys.argv[2];
userChannels = [int(i) for i in sys.argv[3].strip().split(',')];
nChannels = len(userChannels);
patchSize = int(sys.argv[4]);
numberOfClasses = int(sys.argv[5])


   
#pdb.set_trace();
net1 = pickle.load(open(modelPath + sys.argv[1],'rb'));

#prepare outputfile name from inputfile
opFile = imageFile.split('/')[-1][0:-5]+'_'+TAG+'.png';
   
if not os.path.exists(imageFile):
    print("%s not found" %imageFile);
    

#Read input data
imageData = gdal.Open(imageFile,GA_ReadOnly);
cols = imageData.RasterXSize;
rows = imageData.RasterYSize
#bands = imageData.RasterCount;
bands = nChannels;
channels = imageData.GetRasterBand(userChannels[0]).ReadAsArray();
print (cols, rows);
newRow = len(range(patchSize/2,rows-patchSize/2));
newCol = len(range(patchSize/2, cols-patchSize/2));
annotationList = [None] * newRow * newCol ;
#pdb.set_trace()


# store row and column index of each patch. This step can be combined with the prediction step below. But it is compputed separately in order to keep things simple. It takes very less time to run. 
for count1, r in enumerate(range(patchSize/2,rows-patchSize/2)):
    for count2, c in enumerate(range(patchSize/2, cols-patchSize/2)):
        annotationList[count1*newCol + count2] = (r,c);

#stack imagedata from each channel
for b in userChannels[1:]:
    channels = np.dstack((channels,imageData.GetRasterBand(b).ReadAsArray()));
channels = np.asarray(channels, dtype = np.float32);   

#define outputlist
outPutList = np.zeros(newRow*newCol);

#sliding window prediction of each patch and store in outputlist
for count3, (x, y) in enumerate(annotationList):
    pass;
    patchData = channels[x-patchSize/2:x+patchSize/2,y-patchSize/2:y+patchSize/2,:];
    patchData = np.rollaxis(patchData,2).reshape((-1, nChannels, patchSize, patchSize));
    outPutList[count3] = net1.predict(patchData)[0];
#reshape outputlist to image shape
opImage = outPutList.reshape(newRow,newCol);
img = Image.fromarray(opImage.astype(np.uint8)*255/(numberOfClasses-1));
img.save(outputPath+opFile);
