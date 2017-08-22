#!/bin/bash

for sourceImage in `cat ../DataSource.txt`
do
time python TestFullImages.py NN_S6_6_6_13_Sep_15_MaxPool_1_AND_2_Removed.pkl $sourceImage 1,2,3 12 &
done

