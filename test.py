from processing import *
from detection import *

from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
import ntpath
import cv2
import numpy as np
import math

import matplotlib
import matplotlib.pyplot as plt
import skimage.io as io
from skimage.filters import threshold_otsu
from skimage import img_as_ubyte
#"load image data"

class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)   

        self.controller = Processing()
        self.detection = Detection()


        self.fullImageL = None
        self.fullImageR = None
     
        #reference to the master widget, which is the tk window                 
        self.master = master
        self.panelA = None
        self.panelB = None
        self.panelZ = None

        self.valClickX = self.valClickY = None

        self.slider = []
        self.checkVal = []

        self.init_window()

###################################################### 	  v	

    def run(self):
        if self.checkVal[0].get() == 1:
            self.fullImageL = self.controller.blackWhite(self.fullImageL)
            self.fullImageR = self.fullImageL
        if self.checkVal[1].get() == 1:
            a = self.slider[0].get()
            self.fullImageL = self.controller.binarizare(self.fullImageL,a)
            self.fullImageR = self.fullImageL
        if self.checkVal[2].get() == 1:
            self.fullImageL = self.detection.detection(self.fullImageL)
            self.fullImageR = self.fullImageL

        print([x.get() for x in self.slider])
        print([x.get() for x in self.checkVal])
        self.updatePanelR()

        


######################################################    v	GUI 
    
    def openImage(self):
        event = 1
        filename = filedialog.askopenfilename(title='open')
        
        img = cv2.imread(filename)
        self.fullImageL = img

        self.updatePanelL()
           

    # update the left panel with self.imageRL
    # transform cv2 image to tkinter image and show
    def updatePanelL(self):
        img = cv2.resize(self.fullImageL,(500,400))

        im = Image.fromarray(img)      
        imgtk = ImageTk.PhotoImage(image = im)
        
        self.panelA = Label(self.master, image=imgtk)
        self.panelA.image = imgtk
        self.panelA.place(x=300, y=100)

    # update the right panel with self.imageR 
    # transform cv2 image to tkinter image and show
    def updatePanelR(self):
        img = cv2.resize(self.fullImageR,(500,400))

        im = Image.fromarray(img)      
        imgtk = ImageTk.PhotoImage(image = im)
        
        self.panelB = Label(self.master, image=imgtk)
        self.panelB.image = imgtk
        self.panelB.place(x=850, y=100)

        # bind mouse events to window
        self.panelB.bind( "<Button-1>", self.clickZoom)

    def updatePanelZ(self):
        img = cv2.resize(self.fullImageR,(500,400))
        img =img[self.valClickY-25:self.valClickY+25, self.valClickX-25:self.valClickX+25,:]
        img = cv2.resize(img,None,fx=2, fy=2, interpolation = cv2.INTER_CUBIC)

        im = Image.fromarray(img)      
        imgtk = ImageTk.PhotoImage(image = im)
        
        self.panelZ = Label(self.master, image=imgtk)
        self.panelZ.image = imgtk
        self.panelZ.place(x=1352, y=50)


    # swap self.imageL <-> self.imageR
    # to make quickly operation on imageR
    def swapImage(self):
        self.fullImageL = self.fullImageR
        self.updatePanelL()


     # get postion of mouse click in imageL 
    def clickZoom( self, event ):
        self.valClickX = event.x
        self.valClickY = event.y
        print(self.valClickX, self.valClickY)
        self.updatePanelZ()


    #Creation of init_window
    def init_window(self):

        # changing the title of our master widget      
        self.master.title("ObservatorP")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        menubar = Menu(self.master)
        # create a pulldown menu, and add it to the menu bar
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.openImage)
        filemenu.add_command(label="Save", command=self.openImage)
        filemenu.add_command(label="Swap", command=self.swapImage)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command= self.master.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        # display the menu
        self.master.config(menu=menubar)


        #Left Menu
        self.checkVal.append(IntVar())
        self.checkVal.append(IntVar())
        self.checkVal.append(IntVar())

        ck1 = Checkbutton(self.master, text="BlackWhite", variable=self.checkVal[0])
        ck2 = Checkbutton(self.master, text="Binarizare", variable=self.checkVal[1])
        ck3 = Checkbutton(self.master, text="Detection", variable=self.checkVal[2])
        ck1.place(x=20, y=40)
        ck2.place(x=20, y=80)
        ck3.place(x=20, y=120)

        self.slider.append(Scale(self.master, from_=0, to=255, orient=HORIZONTAL))
        self.slider[0].set(36)
        self.slider[0].place(x=120, y=62)


        but = Button(self.master, text='Run', command=self.run)
        but.place(x=20, y=150)
######################################################     ^
    

root = Tk()

root.geometry("1500x600")

#creation of an instance
app = Window(root)

#mainloop 
root.mainloop()  