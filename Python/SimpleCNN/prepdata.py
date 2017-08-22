# -*- coding: utf-8 -*-
import numpy as np
import pickle
import gzip
'''data = np.random.rand(28,28,4);
data = np.rollaxis(data,2);
dataFlat = data.flatten('C');'''

import numpy as np
import pickle
import gzip
trainData =  np.random.rand(500,3456);
testData =  np.random.rand(5000,3456);
valData =  np.random.rand(5000,3456);
trainLab = np.concatenate((np.zeros((250,)),np.ones((250,))),0);
testLab = np.concatenate((np.zeros((2500,)),np.ones((2500,))),0);
valLab = np.concatenate((np.zeros((2500,)),np.ones((2500,))),0);
dataSet = ((trainData,trainLab),(testData, testLab),(valData,valLab));

pickle.dump(dataSet,open('/home/koustav/Desktop/Tidal_Channels/Code/Python/data/SampleData.pkl','wb'));

trainData[0:250,:] = trainData[0:250,:] * .09;
testData[0:250,:] = testData[0:250,:] * .09;
valData[0:250,:] = valData[0:250,:] * .09;