#from tkinter import Tk, Text, BOTH, W, N, E, S
from tkinter import *
from tkinter.ttk import Frame, Button, Label, Style

import tkinter
from PIL import ImageTk, Image

import easycheckout


class App(Frame):
    # Fields
    root = None

    itemList = None
    statusLabel = None

    image_width = 202
    image_height = 360

    imageLabel = None

    def __init__(self, root):
        super().__init__()
        self.initUI()
        self.root = root
        
    def initUI(self):
      	
      	# TitleBar
        self.master.title("Easy Checkout")
        self.pack(fill=BOTH, expand=True)

        # Stretch
        self.columnconfigure(3, weight=1)
        self.columnconfigure(0, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)
        
        # Row0 : Labels for Sections
        cmd = Label(self, text="Commands")
        cmd.grid(sticky=W, pady=4, padx=5, row = 0, column = 0)

        pic = Label(self, text="Picture")
        pic.grid(sticky=W, pady=4, padx=5, row = 0, column = 1)

        items = Label(self, text="Items")
        items.grid(sticky=W, pady=4, padx=5, row = 0, column = 3)
        
        self.statusLabel = Label(self, text= "Hello!\nThis is\nEasyCheckout\n\nPress Activate\nto Start")
        self.statusLabel.grid(sticky=W, pady=4, padx=5, row = 3, column = 0)
        
        self.itemList = Listbox(self)
        self.itemList.grid(row=1, column=3, rowspan=4,
                      padx=5, sticky=E+W+S+N)
                      
        #Buttons
        abtn = Button(self, text="Activate", command = lambda: easycheckout.run(self))
        abtn.grid(row=1, column=0)

        qbtn = Button(self, text="Quit", command = self.quit)
        qbtn.grid(row=2, column=0, pady=4)
        
        clearbtn = Button(self, text="Clear", command = self.clearItem )
        clearbtn.grid(row=5, column=0, padx=5)

        obtn = Button(self, text="OK", command = self.changeImage)
        obtn.grid(row=5, column=3)

        #Pictures
        path = "result.jpg"
        pil_img = Image.open(path)

       	#Pictures : Resize to Show
       	w, h = pil_img.size
       	resizedImg = self.resize(w, h, self.image_width, self.image_height, pil_img)

       	img = ImageTk.PhotoImage(resizedImg)

       	self.imageLabel = Label(self, image = img)
       	self.imageLabel.image = img
       	self.imageLabel.grid(row=1, column = 1, columnspan = 2, rowspan = 4, sticky = E+W+S+N, padx = 5)
    
    # METHODS
    def resize(self, w, h, w_box, h_box, pil_image):
        '''
        resize a pil_image object so it will fit into
        a box of size w_box times h_box, but retain aspect ratio
        '''
        f1 = 1.0*w_box/w  # 1.0 forces float division in Python2
        f2 = 1.0*h_box/h
        factor = min([f1, f2])
        #print(f1, f2, factor)  # test
        # use best down-sizing filter
        width = int(w*factor)
        height = int(h*factor)
        return pil_image.resize((width, height), Image.ANTIALIAS)

    # changeImage NEEDTOBE IMPLEMENTED
    def changeImage(self, path = 'test.png', resize = True):
        pil_img = Image.open(path)

        if(resize):
            #Pictures : Resize to Show
            w, h = pil_img.size
            resizedImg = self.resize(w, h, self.image_width, self.image_height, pil_img)
        else:
            resizedImg = pil_img

        img = ImageTk.PhotoImage(resizedImg)

        self.imageLabel.config(image = img)
        self.imageLabel.image = img


    
    # Insert Item in the ListBox
    def insertItem(self, item):
        self.itemList.insert(END,item)
    
    # Delete Item(s) in the ListBox
    def clearItem(self):
        selection = self.itemList.curselection()
        if (len(selection)==0):
            self.itemList.delete(0,self.itemList.size())
        else:
            idx = selection[0]
            self.itemList.delete(idx)
    # Quit Window
    def quit(self):
        self.root.quit();
    
    # ChangeStatus Text
    def changeStatus(self, status):
        self.statusLabel.config(text = status)

    # Update TK
    def update(self):
        self.root.update()


def main():
    root = Tk()
    root.geometry("500x420")
    app = App(root)
    root.mainloop()

if __name__ == '__main__':
    main()  
