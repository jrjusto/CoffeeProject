import cv2
import numpy as np
from picamera2 import Picamera2
from tkinter import *
from libcamera import controls
from PIL import Image, ImageTk
import time
import pandas as pd
from ultralytics import YOLO
import cvzone
model=YOLO('best.pt')
#model.export(format="ncnn")
my_file = open("classes.txt", "r")
data = my_file.read()
class_list = data.split("\n")
leafTypes = ['Elliptic','Lanceolate','Ovate']
branchTypes = ['Drooping','Semi-erect','Horizontal']
im = None
root = Tk()
root.geometry("480x320")   #480x320
selectedItem = "Leaf"
foundLeaf = False
foundBranch = False
root.attributes('-fullscreen',True)
imgLF = LabelFrame(root)
#imgLF.geometry("320x320")
imgLF.grid(column=0,row=0)
secondFrame = LabelFrame(root)
secondFrame.grid(column=1,row=0)
buttonFrame = LabelFrame(secondFrame)
buttonFrame.pack()
def clearText():
    treeOutputL.config(text="Tree:     ")

def printTree():
    global branchType
    global leafType
    global treeType
    if branchType == branchTypes[0] and leafType == leafTypes[0]:
        treeType = "Robusta"
    elif branchType == branchTypes[1] and leafType == leafTypes[1]:
        treeType = "Liberica"
    elif branchType == branchTypes[2] and leafType == leafTypes[2]:
        treeType = "Excelsa"
    else:
        treeType = "Not found"
    print(treeType)
    treeOutputL.config(text="Tree: "+str(treeType))

def retakePic():
    global stopFrame
    stopFrame = False

def capturePic():
    global stopFrame
    global leafType
    global selectedItem
    global branchType
    global treeType
    global foundLeaf
    global foundBranch
    global L1
    im = None
    
    im= picam2.capture_array()
    im=cv2.flip(im,-1)
    #im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

    results=model.predict(im)
    
    a=results[0].boxes.data
    px=pd.DataFrame(a).astype("float")
    
    for index,row in px.iterrows():
#        print(row)
 
        x1=int(row[0])
        y1=int(row[1])
        x2=int(row[2])
        y2=int(row[3])
        d=int(row[5])
        c=class_list[d]
        
        if selectedItem == 'Leaf':
            
            if c in leafTypes:
                cv2.rectangle(im,(x1,y1),(x2,y2),(0,0,255),2)
                #cvzone.putTextRect(im,f'{c}',(x1,y1),1,1)
                leafType = c
                selectedItem = 'Branch'
                selectedL.config(text='Branch')
                foundLeaf = True
                print("passf")
                finish = True

                
      
        elif selectedItem == 'Branch':
            if c in branchTypes:
                cv2.rectangle(im,(x1,y1),(x2,y2),(0,0,255),2)
                #cvzone.putTextRect(im,f'{c}',(x1,y1),1,1)
                branchType = c
                selectedItem = 'Leaf'
                selectedL.config(text='Leaf')
                foundBranch = True
                finish = True
    
    if foundLeaf and foundBranch:
        if branchType == branchTypes[0] and leafType == leafTypes[0]:
            treeType = "Robusta"
        elif branchType == branchTypes[1] and leafType == leafTypes[1]:
            treeType = "Liberica"
        elif branchType == branchTypes[2] and leafType == leafTypes[2]:
            treeType = "Excelsa"
        else:
            treeType = "Not found"
        print(treeType)
        treeOutputL.config(text="Found: "+str(treeType))
        foundLeaf = False
        foundBranch = False
             
        

    #im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    im = Image.fromarray(im)
    im = ImageTk.PhotoImage(im)
    L1.configure(image=im)
    L1.image = im
    stopFrame =  True




takePicB = Button(buttonFrame,text = "Take Picture",command=capturePic,height = 4,width=11)
takePicB.pack()
retakePicB = Button(buttonFrame,text = "Retake Picture",command=retakePic,height = 4,width=11)
retakePicB.pack()

selectedL = Label(buttonFrame,text = selectedItem)
selectedL.pack()

L1 = Label(imgLF)
L1.pack()
stopFrame = False




outputFrame = LabelFrame(secondFrame)


outputFrame.pack()
findTreeB = Button(outputFrame,text = "Find tree",command=printTree)
#findTreeB.pack()

treeOutputL = Label(outputFrame,text = "Tree:     ")
treeOutputL.pack()

clearB = Button(outputFrame,text = "Clear",command=clearText,height = 4,width=11)
clearB.pack()





def update_frame():
    global im
    global stopFrame
    if stopFrame == False:
        im= picam2.capture_array()
        im=cv2.flip(im,-1)
        #im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(im)
        im = ImageTk.PhotoImage(im)
        L1.configure(image=im)
        L1.image = im
        
    root.after(1,update_frame)
    

picam2 = Picamera2()

picam2.configure(picam2.create_video_configuration(main={"size": (350, 320),"format":"BGR888"},lores={"size": (100, 100)}, raw={"size": (640,640)},encode = "lores"))

picam2.start()
#picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
update_frame()

root.mainloop()

    