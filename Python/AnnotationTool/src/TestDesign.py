# -*- coding: utf-8 -*-
import Tkinter as tk
from PIL import Image, ImageTk

class HeaderButtons(tk.Frame):
    def __init__(self, parent):
        self.frame = tk.Frame.__init__(self, parent);
        self.fileOpenButton = tk.Button(self.frame, text="Open", command=None).grid(row = 0, column = 0, sticky = tk.E);
        self.saveButton = tk.Button(self.frame, text="Save", command=None).grid(row = 0, column = 1, sticky = tk.W);
        
class SelectLabelPanel(tk.Frame):
    def __init__(self, parent):
        self.frame = tk.Frame.__init__(self, parent);
        x = tk.StringVar();
        r1 = tk.Radiobutton(self.frame, text="Foreground", padx=50, variable=x, value='FG', command=None); 	# the 1st radiobox
        r2 = tk.Radiobutton(self.frame, text="Background", padx=50, variable=x, value='BG', command=None);	# the 2nd radiobox
        r1.grid(row = 1, column = 0);
        r2.grid(row = 1, column = 1);
        
class ImagePanel(tk.Frame):
    def __init__(self, parent):
        self.frame = tk.Frame.__init__(self, parent);
        self.canvas = tk.Canvas(self.frame, width=1000, height=800);
        self.canvas.grid(row = 2, columnspan = 2);
        self.rgb = ImageTk.PhotoImage(Image.open("../images/oldMap.jpeg"));
        self.imageId = self.canvas.create_image((0,0), image=self.rgb, anchor= tk.NW);
        
class FooterButtons(tk.Frame):
        def __init__(self, parent):
            self.frame = tk.Frame.__init__(self, parent);
            self.clearButton = tk.Button(self.frame, text="Clear", command=None).grid(row = 3, column = 0, sticky = tk.E);
            self.exitButton = tk.Button(self.frame, text="Quit", command=None).grid(row = 3, column = 1, sticky = tk.W);
        
class TestDesign(tk.Frame):
    def __init__(self, root):
        #self.frame1 = tk.Frame();
        global header, imagePanel, classLabels, footer;
        self.frame1 = tk.Frame.__init__(self, root);
        header = HeaderButtons(self);
        imagePanel = ImagePanel(self);
        classLabels = SelectLabelPanel(self);
        footer = FooterButtons(self);
        

if __name__ == "__main__":
    root = tk.Tk();
    root.title('Annotation Tool');
    application = TestDesign(root);
    root.mainloop();