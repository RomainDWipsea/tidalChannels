# -*- coding: utf-8 -*-

# Author : Koustav Ghosal
# Date :  August 2016
# Summary : This code creates a simple interactive user interface for annotating multi-spectral images. The user can
#           select the input image and the channels to be displayed. The canvas can be dragged using mouse and annotated by 
#           double clicking the pixel. Output is saved in ../Output/ folder. A snapshot of the canvas can be saved at ../Output folder.


from __future__ import print_function
import Tkinter as tk
import auxil.auxil as auxil
import numpy as np
from osgeo import gdal
from osgeo.gdalconst import GA_ReadOnly, GDT_Float32
import pdb
import scipy as sp
from PIL import Image, ImageTk
import sys
import datetime
import random
import tkFont

opDir = "../Output/"
imagePath = '';
opFileName = '';

class MenuBar(tk.Frame):
        global opFileName, imagePanel, opDir, imagePath, sidePanel;
        def __init__(self, parent):
            self.frame = tk.Frame.__init__(self, parent);
            self.menubar = tk.Menu(parent, bg = "#CA4A2F", relief = tk.FLAT, activebackground = "#D6BF86", tearoff = 0.0);
            filemenu = tk.Menu(self.menubar, bg = "#FFCC99",relief = tk.FLAT, activebackground = "#D6BF86")
            filemenu.add_command(label="New", command=self.openNewFile);
            filemenu.add_command(label="Open", command=None);
            filemenu.add_command(label="Save", command=self.saveButton);
            filemenu.add_command(label="Snapshot", command=self.takeSnapShot);
            filemenu.add_separator()
            filemenu.add_command(label="Exit", command=root.quit)
            self.menubar.add_cascade(label="File", menu=filemenu)

            helpmenu = tk.Menu(self.menubar, bg = "#FFCC99",relief = tk.FLAT, activebackground = "#D6BF86")
            helpmenu.add_command(label="Help Index", command=None)
            helpmenu.add_command(label="About...", command=None)
            self.menubar.add_cascade(label="Help", menu=helpmenu)

            parent.config(menu = self.menubar);
            
        def openNewFile(self):
            imagePath = auxil.select_infile(title='Choose Image.');
            imagePanel.updateImage(imagePath);
            imagePanel.listOfids = [];
            imagePanel.listOfCoordinates = [];
        
        def saveButton(self):
            #pdb.set_trace();
            opFileName = (opDir+sidePanel.userId.get()+"_"+str(datetime.datetime.now().microsecond)+imagePath.split('/')[-1].split('.')[0]);
            #pdb.set_trace();
            with open(opFileName+'.txt',"wb") as f:
                for i in sidePanel.listOfClasses:
                    print (i, file = f, end = " ");
                print ("\n",end = "\n");
                for c in imagePanel.listOfCoordinates:
                    print (c[0], c[1], c[2], file = f);
                    
        def takeSnapShot(self):
            opFileName = (opDir+sidePanel.userId.get()+"_"+
                    str(datetime.datetime.now().microsecond)+imagePath.split('/')[-1].split('.')[0]);              
            imagePanel.canvas.postscript(file = opFileName+'.ps',colormode='color');
            
class Header(tk.Frame):
    def __init__(self, parent):
        self.frame = tk.Frame.__init__(self, parent);
        self.classLabel = tk.StringVar(root);
        self.choices = [""];
        self.option = tk.OptionMenu(self.frame, self.classLabel, *self.choices);
        self.classLabel.set('Select');
        self.option.grid(row = 0, column = 1, sticky = tk.E, padx = 25, pady = 10);
        self.option.config(bg = "#C4AC48");
        self.option.config(activebackground = "#D6BF86");
        self.option.config(relief = tk.RAISED);
        self.option.config(highlightthickness = 0);
        self.option["menu"].config(bg = "#FFCC99");
        self.option["menu"].config(activebackground = "#D6BF86");
        
class SidePanel(tk.Frame):
    global header;
    def __init__(self, parent):
        #pdb.set_trace();
        self.frame = tk.Frame.__init__(self, parent);
        self.userId = tk.StringVar();
        self.nClasses = tk.StringVar();
        self.classNames = tk.StringVar();
        
        self.uIdEntry = tk.Entry(self.frame, textvariable = self.userId);
        self.uIdEntry.insert(0, "User_Id");
        self.uIdEntry.grid(row = 2, column = 0, pady = 10);
        
        self.nClassesEntry = tk.Entry(self.frame, textvariable = self.nClasses);
        self.nClassesEntry.insert(0, "Enter number of Classes");
        self.nClassesEntry.grid(row = 3, column = 0, pady = 10);
        
        self.classList = tk.Entry(self.frame, textvariable = self.classNames);
        self.classList.insert(0, "Class 1, Class 2,..., Class N");
        self.classList.grid(row = 4, column = 0, pady = 10);
        
        self.assignValues = tk.Button(self.frame, text="Start",
                                      command = self.assignValues, bg = "#C4AC48", activebackground = "#D6BF86").grid(row = 5, column = 0, pady = 10);
        
        self.ClassCounterBox = tk.Listbox(self.frame, width = 25, height = 10,background = "#FFCC99",
                               relief = tk.FLAT, highlightthickness = 0, font = tkFont.Font(size=15));
        self.ClassCounterBox.grid(row = 6, column = 0,rowspan = 2, padx=10, pady=10, sticky  = tk.N);
        
    def assignValues(self):
        self.numberOfClasses = int(self.nClasses.get());
        self.listOfClasses = self.classNames.get().strip().split(',');
        self.ClassColor =  dict((key, value) for (key, value) in zip(self.listOfClasses,self.gen_hex_colour_code(self.numberOfClasses)));
        self.ClassCounter  = dict((key, value) for (key, value) in zip(self.listOfClasses,list([0]*self.numberOfClasses)));
        self.updateValues();       
        '''for count, key in enumerate(self.ClassCounter):
            self.ClassCounterBox.insert(tk.END, '{}:    {}'.format(key, self.ClassCounter[key]));
            self.ClassCounterBox.itemconfig(count, {'bg':self.ClassColor[key]});'''
        header.choices =  self.ClassCounter;
        header.classLabel.set('Select');
        header.option['menu'].delete(0, 'end');
        for choice in header.choices:
            header.option['menu'].add_command(label=choice, command=tk._setit(header.classLabel, choice));
            
            
    def updateValues(self):
        self.ClassCounterBox.delete(0, tk.END);
        for count,key in enumerate(self.ClassCounter):
            self.ClassCounterBox.insert(tk.END, '{}:    {}'.format(key, self.ClassCounter[key]));
            self.ClassCounterBox.itemconfig(count, {'bg':self.ClassColor[key]});
            
    def resetValues(self):
        self.ClassCounter  = dict((key, value) for (key, value) in zip(self.listOfClasses,list([0]*self.numberOfClasses)));
        self.updateValues();
            
    def gen_hex_colour_code(self,n):
        colors = [];
        for i in range(n):
            colors.append('#'+''.join([random.choice('0123456789ABCDEF') for x in range(6)]));
        return colors;
    

class ImagePanel(tk.Frame):
    global sidePanel, header;    
    def __init__(self, parent):
        self.frame = tk.Frame.__init__(self, parent);
        self.listOfids = []; self.listOfCoordinates = []; self.listOfLabels = [];
        self.oldX = 0;
        self.oldY = 0;
        self.selectId = None;
        #self.canvas = tk.Canvas(self.frame, width=1600, height=800);
        self.canvas = tk.Canvas(self.frame, relief = tk.RAISED, bg = '#FFFFFF');
        self.canvas.grid(row = 1, column = 1, rowspan = 7, padx=25, pady = 5, sticky = "nsew" );
        self.rgb = ImageTk.PhotoImage(Image.open("../images/StartUpBackground.jpg"));
        self.imageId = self.canvas.create_image((0,0), image=self.rgb, anchor= tk.NW);
        
        
        #self.xsb = tk.Scrollbar(self.frame, orient="horizontal", command=self.canvas.xview, bg = "#D6BF86")
        #self.ysb = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview, bg = "#D6BF86")
        #self.canvas.configure(yscrollcommand=self.ysb.set, xscrollcommand=self.xsb.set)
        #self.canvas.configure(scrollregion=(0,0,5000,5000));
        #self.xsb.grid(row = 4, columnspan = 2, sticky="ew");
        #self.ysb.grid(row = 3, column = 3, sticky="ns");
        
        #linux scroll
        #self.canvas.bind("<Button-4>", self.zoomerP)
        #self.canvas.bind("<Button-5>", self.zoomerM)

        #windows scroll
        #self.canvas.bind("<MouseWheel>",self.zoomer)


        self.canvas.bind("<Button-1>", self.move_start)
        self.canvas.bind("<B1-Motion>", self.move_move)
        self.canvas.bind("<Double-Button-1>", self.selectPixel)
        self.canvas.bind("<Double-Button-3>", self.removePixel)
        self.canvas.bind("<Shift-Button-1>", self.move_start)
        self.canvas.bind("<Shift-B1-Motion>", self.move_select)
        self.canvas.bind("<Shift-ButtonRelease>", self.bulk_select)

    #move
    def move_start(self, event):
        self.canvas.scan_mark(event.x, event.y)
        self.oldX = self.canvas.canvasx(event.x);
        self.oldY = self.canvas.canvasy(event.y);
        
    def move_select(self, event):
        if self.selectId:
            self.canvas.delete(self.selectId);
        self.selectId = self.canvas.create_rectangle(self.oldX, self.oldY, self.canvas.canvasx(event.x), self.canvas.canvasy(event.y), outline = "cyan");
        
    def move_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    #windows zoom
    def zoomer(self,event):
        if (event.delta > 0):
            self.canvas.scale("all", event.x, event.y, 1.5, 1.5)
        elif (event.delta < 0):
            self.canvas.scale("all", event.x, event.y, 0.5, 0.5)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))

    #linux zoom
    def zoomerP(self,event):
        self.canvas.scale("all", self.canvas.canvasx(event.x), self.canvas.canvasx(event.y), 1.5, 1.5)        
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))
        self.canvas.update_idletasks();
        
    def zoomerM(self,event):
        self.canvas.scale("all", self.canvas.canvasx(event.x), self.canvas.canvasx(event.y), .5, .5)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))
        self.canvas.update_idletasks();
        
    def bulk_select(self, event):
        #print ("BP 1");
        #Next line deletes the rectangle for selection
        self.canvas.delete(self.selectId);
        curLabel = header.classLabel.get();
        #pdb.set_trace();
        nPoints = int(np.amin([self.canvas.canvasx(event.x) - self.oldX, self.canvas.canvasy(event.y) - self.oldY]));
        xCoordinates = random.sample(range(int(self.oldX), int(self.canvas.canvasx(event.x))),nPoints);
        yCoordinates = random.sample(range(int(self.oldY), int(self.canvas.canvasy(event.y))),nPoints);
        if curLabel != '':
            sidePanel.ClassCounter[curLabel] +=nPoints;
            sidePanel.updateValues();
            for i in range(nPoints):
                cx = xCoordinates[i];
                cy = yCoordinates[i];          
                idOfPixel = self.canvas.create_oval(cx-3, cy-3, cx+3, cy+3, fill=sidePanel.ClassColor[curLabel]);
                self.listOfids.append(idOfPixel);
                self.listOfCoordinates.append(tuple((cx,cy,curLabel)));
                self.listOfLabels.append(curLabel);            
        else:
            print("Please select a class label");
        self.canvas.update_idletasks();

    def selectPixel(self,event):
        curLabel = header.classLabel.get();
        cx = int(self.canvas.canvasx(event.x));
        cy = int(self.canvas.canvasy(event.y));
        if curLabel != 'Select':
            sidePanel.ClassCounter[curLabel] +=1;
            sidePanel.updateValues();
            idOfPixel = self.canvas.create_oval(cx-3, cy-3, cx+3, cy+3, fill=sidePanel.ClassColor[curLabel]);
            self.listOfids.append(idOfPixel);
            self.listOfCoordinates.append(tuple((cx,cy,curLabel)));
            self.listOfLabels.append(curLabel); 
        else:
            print("Please select a class label");
        self.canvas.update_idletasks();

    def removePixel(self, event):
        chosenId, = self.canvas.find_withtag(tk.CURRENT);
        if chosenId and chosenId != self.imageId:
            self.canvas.delete(chosenId);
            indexOfDeletion = self.listOfids.index(chosenId);
            self.listOfids.pop(indexOfDeletion);
            self.listOfCoordinates.pop(indexOfDeletion);
            sidePanel.ClassCounter[self.listOfLabels[indexOfDeletion]]-=1;
            sidePanel.updateValues();
            self.listOfLabels.pop(indexOfDeletion);
        self.canvas.update_idletasks();

    def updateImage(self, imagePath):
        if imagePath:
            self.imageData = gdal.Open(imagePath,GA_ReadOnly);
            self.cols = self.imageData.RasterXSize;
            self.rows = self.imageData.RasterYSize
            self.bands = self.imageData.RasterCount
            self.channels = self.imageData.GetRasterBand(1).ReadAsArray();
            for b in range(2,self.bands+1):
                self.channels = np.dstack((self.channels,self.imageData.GetRasterBand(b).ReadAsArray()));
            self.setChannels();
            self.getImage();
        self.imageId = imagePanel.canvas.create_image((0,0), image=self.rgb, anchor= tk.NW);
        self.canvas.update_idletasks();

    def setChannels(self):
        self.displayChannelIndices = list(auxil.select_dims("Select the Channels to Visualize the Image"));
        #self.displayChannelIndices = [0, 1, 2];

    def getImage(self):
        im =  np.asarray(self.channels).take(self.displayChannelIndices,2);
        #imPIL = sp.misc.toimage(im);
        #imBright = sp.misc.toimage(im).point(lambda p: p * 2.0)
        #pdb.set_trace();        
        self.rgb = ImageTk.PhotoImage(sp.misc.toimage(im).point(lambda p: p * 2));
        

class FooterButtons(tk.Frame):
    global sidePanel, imagePanel;
    def __init__(self, parent):
        self.frame = tk.Frame.__init__(self, parent);
        self.clearButton = tk.Button(self.frame, text = "Clear", command = self.clearPanel, bg = "#C4AC48", activebackground = "#D6BF86").grid(row = 8, column = 1, padx=5, pady=5);

    def clearPanel(self):
        for i in imagePanel.listOfids:
            imagePanel.canvas.delete(i);
        imagePanel.listOfids = [];
        imagePanel.listOfCoordinates = [];
        sidePanel.resetValues();           
        imagePanel.canvas.update_idletasks();


class AnnotationTool(tk.Frame):
    def __init__(self, root):
        global header, imagePanel, footer, sidePanel, menubar;
        self.frame = tk.Frame.__init__(self, root, background = "#ffffff");
        sidePanel  = SidePanel(self);
        imagePanel = ImagePanel(self);
        header = Header(self);
        footer = FooterButtons(self);
        menubar = MenuBar(root);

if __name__ == "__main__":
    root = tk.Tk();
    root.title('Annotation Tool');
    root.configure(background = "#FFCC99")
    application = AnnotationTool(root).grid(row = 0);
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=5)
    root.columnconfigure(2, weight=0)
    root.rowconfigure(0, weight=0)
    root.rowconfigure(1, weight=0)
    root.rowconfigure(2, weight=0)
    root.rowconfigure(3, weight=0)
    root.rowconfigure(4, weight=0)
    root.rowconfigure(5, weight=0)
    root.rowconfigure(6, weight=0)
    root.rowconfigure(7, weight=5)    
    root.rowconfigure(8, weight=0)
    root.mainloop();
