from tkinter import Tk, Text, BOTH, W, N, E, S
from tkinter.ttk import Frame, Button, Label, Style
from PIL import ImageTk, Image


class App(Frame):
    def __init__(self):
        super().__init__()   
         
        self.initUI()
        
        
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
        
        # ItemList
        itemList = Text(self)
        itemList.grid(row=1, column=3, rowspan=4, 
            padx=5, sticky=E+W+S+N)

        #Buttons
        abtn = Button(self, text="Activate", command = lambda :pNUM(3))
        abtn.grid(row=1, column=0)

        cbtn = Button(self, text="Close")
        cbtn.grid(row=2, column=0, pady=4)
        
        hbtn = Button(self, text="Help")
        hbtn.grid(row=5, column=0, padx=5)

        obtn = Button(self, text="OK")
        obtn.grid(row=5, column=3)

        #Pictures
        path = "result.jpg"
        pil_img = Image.open(path)

       	#Pictures : Resize to Show
       	w_box = 202
       	h_box = 360
       	w, h = pil_img.size
       	resizedImg = resize(w, h, w_box, h_box, pil_img)

       	img = ImageTk.PhotoImage(resizedImg)

       	pannel = Label(self, image = img)
       	pannel.image = img
       	pannel.grid(row=1, column = 1, columnspan = 2, rowspan = 4, sticky = E+W+S+N, padx = 5)

def resize(w, h, w_box, h_box, pil_image):
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

def main():
    root = Tk()
    root.geometry("500x420")
    app = App()
    root.mainloop()

def aClick(self):
    self.config(text = "False")
    print ("Hello")
def pNUM(k):
    print (k)

if __name__ == '__main__':
    main()  
