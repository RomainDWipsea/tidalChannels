# -*- coding: utf-8 -*-

import numpy as np
import sys
import pdb
from osgeo import gdal
from osgeo.gdalconst import GA_ReadOnly, GDT_Float32
import pickle
#from sklearn import svm, grid_search, datasets
import random

#usage python Master.py full_path_for_annotation_text_file full_path_of_image_file XYZ.pkl patchsize
def chunkIt(seq, num):
  avg = len(seq) / float(num)
  out = []
  last = 0.0

  while last < len(seq):
    out.append(seq[int(last):int(last + avg)])
    last += avg

  return out

annotationFile = sys.argv[1];
imageFile = sys.argv[2];
opfile = sys.argv[3];
patchSize = int(sys.argv[4]);
annotationList = []
dataSet = [];
labels =[];
userChannels = raw_input("Please enter channels to extract separated by commas index starting from 1: ");
userChannels  = [int(i) for i in userChannels.strip().split(',')];
with open(annotationFile, 'rb') as f:
    for count,line in enumerate(f):
        if count == 0:
            classLabels = line.strip().split();
            classList = dict((key, value) for (value,key) in enumerate(classLabels));
        else:
            (x, y, label) = line.strip().split();
            #pdb.set_trace();
            annotationList.append((int(float(x)), int(float(y)), classList[label]));

   
imageData = gdal.Open(imageFile,GA_ReadOnly);
cols = imageData.RasterXSize;
rows = imageData.RasterYSize
#bands = imageData.RasterCount
bands = len(userChannels);
channels = imageData.GetRasterBand(userChannels[0]).ReadAsArray();
#pdb.set_trace(); 
for b in userChannels[1:]:
    channels = np.dstack((channels,imageData.GetRasterBand(b).ReadAsArray()));


channels = np.asarray(channels, dtype = 'float32');    

'''for c in range(channels.shape[2]):
    channels[:,:,c] = channels[:,:,c]/float(np.amax(channels[:,:,c]));'''

dataSet = np.zeros((1,bands*patchSize*patchSize));
print channels.shape;
for (y, x, label) in annotationList:
    patchData = channels[x-patchSize/2:x+patchSize/2,y-patchSize/2:y+patchSize/2,:];
    patchData = np.rollaxis(patchData,2);
    patchDataFlat = np.transpose(patchData.flatten('C'));
    if patchDataFlat.shape[0] != bands*patchSize*patchSize:
        #pdb.set_trace();
        continue;
    #pdb.set_trace();
    #print x,y,patchData.shape;
    dataSet = np.vstack((dataSet,patchDataFlat));
    labels.append(label);
dataSet = np.delete(dataSet,0,0);
#pdb.set_trace(); 
tempList = list(zip(dataSet,labels));
random.shuffle(tempList);
dataSet,labels = zip(*tempList);
#pdb.set_trace();
labels = np.asarray(labels);
dataSet = np.asarray(dataSet);
#dataSet = dataSet/np.amax(dataSet);
'''dataSetSize = len(dataSet);
finalDataSet = (tuple(dataSet[0:dataSetSize/3]),
                tuple(dataSet[dataSetSize/3:2*dataSetSize/3),tuple(dataSet[2*dataSetSize/3:dataSetSize]));'''
dataPartitions = np.asarray(chunkIt(dataSet,3));
labelPartitions = np.asarray(chunkIt(labels,3));

finalDataSet = tuple(zip(dataPartitions,labelPartitions));
pickle.dump(finalDataSet,open('../../Data/'+opfile,'wb'));
'''parameters = {'kernel':('linear', 'rbf'), 'C':[1, 10]};
svr = svm.SVC()
clf = grid_search.GridSearchCV(svr, parameters, verbose = 5)
clf.fit(dataSet,labels)
pdb.set_trace();'''
