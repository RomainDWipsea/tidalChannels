#!/usr/bin/env python

# Usage : python Master.py xyz.pkl xyz.model number_of_channels patchSize number_of_classes
# This code trains a model on the annotated data.




from __future__ import print_function
import lasagne
from lasagne import layers
from lasagne.updates import nesterov_momentum
from nolearn.lasagne import NeuralNet
from nolearn.lasagne import visualize
import matplotlib.pyplot as plt
from PIL import Image
import sys
import os
import gzip
import pickle
import numpy as np
import numpy
import pdb



PY2 = sys.version_info[0] == 2

# Define parameters
inputPath = '../../Data/';
outputPath = '../Output';
modelPath = '../Models/'
nChannels = 0;
patchSize = int(sys.argv[4]);
nOutPutClasses =  int(sys.argv[5]);


#defines pickle load function depending on the size of the data
if PY2:
    from urllib import urlretrieve

    def pickle_load(f, encoding):
        return pickle.load(f)
else:
    from urllib.request import urlretrieve

    def pickle_load(f, encoding):
        return pickle.load(f, encoding=encoding)
        

#loads and reshapes data according to CNN input format
def load_data():
    global nChannels;
    nChannels = int(sys.argv[3]);
    filename = inputPath + sys.argv[1];
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    #pdb.set_trace();
    X_train, y_train = data[0]
    X_val, y_val = data[1]
    X_test, y_test = data[2]
    X_train = X_train.reshape((-1, nChannels, patchSize, patchSize))
    X_val = X_val.reshape((-1, nChannels, patchSize, patchSize))
    X_test = X_test.reshape((-1, nChannels, patchSize, patchSize))
    y_train = y_train.astype(np.uint8)
    y_val = y_val.astype(np.uint8)
    y_test = y_test.astype(np.uint8)
    X_train = X_train.astype(np.float32)
    X_val = X_val.astype(np.float32)
    X_test = X_test.astype(np.float32)
    return X_train, y_train, X_val, y_val, X_test, y_test


#defines the layers of the CNN and set parameters
def nn_example():
    global nChannels;
    X_train, y_train, X_val, y_val, X_test, y_test = load_data()
    net1 = NeuralNet(
    layers=[('input', layers.InputLayer),
            ('aug1',layers.LocalResponseNormalization2DLayer),
            ('aug2',layers.GaussianNoiseLayer),
            ('bn1', layers.BatchNormLayer),
            ('conv2d1', layers.Conv2DLayer),
            ('bn2', layers.BatchNormLayer),
            ('maxpool1', layers.MaxPool2DLayer),
            ('conv2d2', layers.Conv2DLayer),
            ('bn3', layers.BatchNormLayer),
            ('maxpool2', layers.MaxPool2DLayer),
            ('dropout1', layers.DropoutLayer),
            ('dense', layers.DenseLayer),
            ('bn4', layers.BatchNormLayer),
            ('dropout2', layers.DropoutLayer),
            ('output', layers.DenseLayer),
            ],
    # input layer
    input_shape=(None, nChannels, patchSize, patchSize),
    # layer conv2d1
    conv2d1_num_filters=32,
    conv2d1_filter_size=(3, 3),
    conv2d1_nonlinearity=lasagne.nonlinearities.rectify,
    conv2d1_W=lasagne.init.GlorotUniform(),  
    # layer maxpool1
    maxpool1_pool_size=(2, 2),    
    # layer conv2d2
    conv2d2_num_filters=32,
    conv2d2_filter_size=(3, 3),
    conv2d2_nonlinearity=lasagne.nonlinearities.rectify,
    # layer maxpool2
    maxpool2_pool_size=(2, 2),
    # dropout1
    dropout1_p=0.5,    
    # dense
    dense_num_units=256,
    dense_nonlinearity=lasagne.nonlinearities.rectify,    
    # dropout2
    dropout2_p=0.5,    
    # output
    output_nonlinearity=lasagne.nonlinearities.softmax,
    output_num_units= nOutPutClasses,
    # optimization method params
    update=nesterov_momentum,
    update_learning_rate=0.01,
    update_momentum=0.9,
    max_epochs=100,
    verbose=2,
    )

    nn = net1.fit(X_train, y_train)
    print("Test Accuracy : %s" % str(1- np.mean(np.abs(net1.predict(X_test) - y_test))));
    sys.setrecursionlimit(6000);
    pickle.dump(net1, open(modelPath + sys.argv[2],'wb'));
    #visualize.plot_conv_weights(net1.layers_['conv2d1']);
    #get_full_image_response(net1);


def main():
    if not os.path.exists(inputPath):
        print('Input file not found at %s' %inputPath);
        exit();
    if not os.path.exists(outputPath):
        os.mkdir(outputPath);
    if not os.path.exists(modelPath):
        os.mkdir(modelPath);
    nn_example();
if __name__ == '__main__':
    main()
