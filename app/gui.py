"""
Tkinter application for handling the visualization
"""
#Constants
IMGS_DIR     = "../data/imgs/"
MIXED4A_IMGS = IMGS_DIR + "mixed4a_imgs.npy"

import numpy as np
import tkinter as tk
import pickle 
from PIL import Image, ImageTk
from lucid.misc.io.serialize_array import _normalize_array as gen_img

class NeuronWindow(tk.Button):
    def __init__(self, master, node_id):
        tk.Button.__init__(self, master)
        self.node_id = node_id


class DeepTopoWindow(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.__init_window()
        self.__visualize_layer()
    
    def __init_window(self):
        self.master.title("Topological analysis of Neural Networks")
        
        #Expand to fill
        self.pack(fill=tk.BOTH, expand=1)

        # creating a button instance
        quitButton = tk.Button(self, text="Quit", command=self.__client_exit)

        # placing the button on my window
        quitButton.place(x=0, y=0)
    
    def __visualize_layer(self):
        imgs = np.load(MIXED4A_IMGS)
        imgs = imgs.reshape(imgs.shape[0], 64, 64, 3)
        self.__layer_buttons = []
        self.__imgs_tk = []
        print(imgs.shape)
        row = -1
        for i in range(imgs.shape[0]):
            if i % 64 == 0:
                row+=1
            img = imgs[i]
            img = gen_img(img)
            img_tk = ImageTk.PhotoImage(Image.fromarray(img))
            self.__imgs_tk.append(img_tk)
            self.__layer_buttons.append(NeuronWindow(self, i))
            self.__layer_buttons[i].config(image=self.__imgs_tk[i])
            self.__layer_buttons[i].bind("<Button-1>", self.__node_event)
            self.__layer_buttons[i].pack()
#            self.__layer_buttons[i].grid(sticky=tk.N+tk.E+tk.W+tk.S)#.pack()#grid(row=row, column=i)#pack(side=tk.LEFT)
#            self.__layer_buttons[i].place(x=i*64,y=i*64)
        self.pack(fill=tk.BOTH, expand=True)

    @staticmethod
    def __node_event(event):
        print("Got clicked!x=%d y=%d" %(event.x, event.y))
        print("Node id: %d" % event.widget.node_id)
    
    def __client_exit(self):
        exit()
