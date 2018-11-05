from tkinter import *
from tkinter import filedialog
from PIL import Image,ImageTk,ImageFilter,ImageOps
import PIL
import os
import py8Bit

class mainMenu :


    def __init__(self,a):
        self.a = a
        self.w = 300
        self.h = 200
        self.file_name_open="insert_image.gif"

        self.image_frame = Frame(a,  width=self.w, height=self.h)
        self.image_frame.pack(pady=20)

        # correct size image
        img = Image.open(self.file_name_open)
        img=self.resize(img)
        # prepare image for the label
        self.icon_1 = ImageTk.PhotoImage(img)
        # create the container (frame)
        self.frame_1 = Frame(self.image_frame, width=self.w, height=self.h)
        self.frame_1.pack(side='left', padx=10, pady =10)#_propagate(0)
        # set the label that contains the image
        self.label_1 = Label(self.frame_1, image=self.icon_1)
        self.label_1.config(height=self.h, width=self.w)
        self.label_1.pack(side="bottom", fill="both", expand="yes")


        # correct size image
        img = Image.open(self.file_name_open)
        img=self.resize(img)
        self.icon_2 = ImageTk.PhotoImage(img)
        # create the container (frame)
        self.frame_2 = Frame(self.image_frame, width=self.w, height=self.h)
        self.frame_2.pack(side=RIGHT, padx=10, pady =10)#_propagate(0)
        # set the label that contains the image
        self.label_2 = Label(self.frame_2, image=self.icon_2)
        self.label_2.config(height=self.h, width=self.w)
        self.label_2.pack(side="bottom", fill="both", expand="yes")

        self.edited_image = None

        self.button_sel_image    = Button(text="Select the image",  width=30, command=self.mfileopen)
        self.button_sel_image.pack(pady=5)
        self.button_save_image   = Button(text="Save the image"  ,  width=30, command=self.mfilesave)
        self.button_save_image.pack(pady=5)
        self.button_8_bit_effect = Button(text="8 Bit", width=30,  command=self.BitEffect)
        self.button_8_bit_effect.pack(pady=5)

    # function to make the image fill the container
    def resize(self,img):
        baseH = self.h
        # the image size with respect to container space
        hpercent = ( float(img.size[1]) / baseH )
        baseW = self.w
        wpercent = ( float(img.size[0]) / baseW  )

        if (hpercent < 1 and wpercent < 1):
            # the image is smaller than the space so it is correct
            return img

        # to understand if the image as to be reduce
        if hpercent > 1 and wpercent > 1 :
            hpercent = ( float( baseH / img.size[1]) )
            wpercent = ( float( baseW / img.size[0]) )

        # only the smallest scale is needed to make the image contained into the container
        if ( hpercent < wpercent):
            wpercent = hpercent
        else:
            hpercent = wpercent

        hsize = int((float(img.size[1]) * float(hpercent)))
        wsize = int((float(img.size[0]) * float(wpercent)))

        img = img.resize((wsize , hsize), PIL.Image.ANTIALIAS)
        return img


    # save the file button call
    # it passes the name of the image to save it
    def mfilesave(self):
        file_name_save = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Select file", filetypes=(("PNG", "*.png"), ("all files", "*.*")))
        self.edited_image.save(fp=file_name_save)

    # open the file button call
    # it passes the name of the image to the updatePhoto function
    def mfileopen(self):
        file_name_open = filedialog.askopenfile()
        self.updatePhoto(file_name_open.name) # .name to access to the name of the _io.TextIOWrapper

    def updatePhoto(self,file_name_open):
        print(file_name_open)
        self.file_name_open = file_name_open
        img = Image.open(self.file_name_open)
        img=self.resize(img)
        self.icon_1 = ImageTk.PhotoImage(img)
        self.frame_1.pack()#_propagate(0)
        self.label_1.config( image=self.icon_1)
        self.label_1.pack(side="bottom", fill="both", expand="yes")



    def BitEffect(self):
        # disble the button
        self.button_8_bit_effect.config(state="disabled")
        self.edited_image = py8Bit.bit_effect(self.file_name_open,0.2,self.a)
        img = self.resize(self.edited_image)
        #self.icon_2 = ImageTk.PhotoImage(self.edited_image)
        self.icon_2 = ImageTk.PhotoImage(img)
        self.frame_2.pack()#_propagate(0)
        self.label_2.configure(image=self.icon_2)
        #self.label_2.image = self.icon_2
        self.label_2.pack(side = "bottom", fill = "both", expand = "yes")
        # enable the button
        self.button_8_bit_effect.config(state="normal")




a = Tk()
my_gui = mainMenu(a)
a.mainloop()
