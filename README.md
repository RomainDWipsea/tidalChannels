# Installing Dependencies #

## System Requirements ##
1. Ubuntu (Preferably 14+ 64-bit)
2. Python2.7




## Install virtualenv ##

```
#!bash

sudo apt-get install virtualenv
```


## Download CRC and GDAL ##

```
#!bash

git clone https://github.com/mortcanty/CRCPython.git
wget http://download.osgeo.org/gdal/2.1.0/gdal-2.1.0.tar.gz
```



## Create and Activate Virtual Environment ##

```
#!bash

virtualenv irisa_venv -p /usr/bin/python2.7
source irisa_venv/bin/activate
pip install matplotlib
pip install numpy
pip install scipy
```



## Installation ##

### 1. Install auxil ###

move to CRCPython/src/

run:

```
#!bash

python setup.py install
sudo cp ../provmeans/linux\ 64bit/libprov_means.so /usr/local/lib/libprov_means.so
```



### 2. Install GDAL ###
change directory to where gdal was downloaded


```
#!bash

tar -xvf gdal-2.1.0.tar.gz
cd gdal-2.1.0/
./configure --prefix=/usr/
make -j`nproc`
sudo make install
cd swig/python/
python setup.py install
```


### 3. Install PIL ###

```
#!bash

pip install Pillow

```


### 4. Install Theano, Lasagne, Nolearn ###

```
#!bash

pip install --upgrade https://github.com/Theano/Theano/archive/master.zip
pip install --upgrade https://github.com/Lasagne/Lasagne/archive/master.zip
pip install -r https://raw.githubusercontent.com/dnouri/nolearn/master/requirements.txt
pip install git+https://github.com/dnouri/nolearn.git@master#egg=nolearn==0.7.git


```

# Running the code #

## Annotation Tool ##
move to AnnotationTool/src

```
#!bash

python Master.py
```

The output is saved as a text file in AnnotationTool/Output.

**There is a bug in Output. Open the output and in the first line, put a newline after the class names.**  
## Process data to CNN input format ##
Move to ProcessData/src


```
#!python

python Master.py full_path_for_annotation_text_file full_path_of_image_file output_file_name_to_be_created.pkl patchsize
```

The output is stored in irisa_codes/Python/Data.

## CNN Training and Testing ##
Move to LasagneTest/src/

### Training ###

**GPU is not used since training takes less time**
```
#!bash

THEANO_FLAGS='device=cpu,floatX=float32' python Master.py just_name_of_input_data_file_created_from_ProcessData.pkl name_for_model_file_to_be_created.model number_of_channels patchSize number_of_classes
```

Model is saved in LasagneTest/Models/

### Testing ###

Set the TAG variable within the code accordingly

```
#!bash

THEANO_FLAGS='device=cpu,floatX=float32' python TestFullImages.py just_name_of_model_file_created_by_CNN full_image_path channels_seperated_by_commas patchsize number_of_classes
For example
THEANO_FLAGS='device=cpu,floatX=float32' python TestFullImages.py TestOP.model /home/koustav/Desktop/irisa/ILSVRC2010_val_00000001.JPEG 1,2,3 12 4

```

Output is saved in LasagneTest/Output.
