import math
import os
import tkinter as tk
import socket
import random
import re
import threading

from tkinter import font as tkFont
from PIL import ImageTk, Image
from system_sub import *
from datetime import datetime

def isOpen(ip,port):
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
      s.connect((ip, int(port)))
      s.shutdown(1)
      return True
   except:
      return False


class Button(object):
    def __init__(self,canvas,text,color,command,image="",h=3,w=15):
        self.h=h
        self.w=w
        self.canvas = canvas
        self.image=image
        self.button = tk.Button(master=None,text=text, fg=color,
                                command=command, image=image, compound='center', borderwidth=5)
        self.button.config(height=self.h,width=self.w,bg='grey')
        self.thread = []
        
    def draw(self,x,y):
        self.button.pack(fill='both', expand='yes')
        self.canvas.create_window(x,y,window=self.button)

class GUI_Windows(object):
    def __init__(self, root, canvas):
        self.root = root
        self.canvas = canvas
        self.ip = ""
        self.port = ""
        self.connection_status = ""

        self.sensor_list = [
                       "LOx Pressure",
                       "LCH4 Pressure",
                       "Helium Pressure",
                       "Engine Pressure",
                       "LOx Temp",
                       "LCH4 Temp",
                       "Helium Temp",
                       "Engine Temp"
            ]
        #Pressure unit is psi
        #Temp unit is K
        self.sensor_param = {
            "LOx Pressure"      :[500,520,560,580],
            "LCH4 Pressure"     :[420,445,475,500],
            "Helium Pressure"   :[1500,2000,2500,2750],
            "Engine Pressure"   :[300,325,375,400],
            "LOx Temp"          :[75,85,95,105],
            "LCH4 Temp"         :[100,105,115,125],
            "Helium Temp"       :[70,80,100,110],
            "Engine Temp"       :[70,80,1500,3000]
            }
        
    def exit(self):
        pop = tk.Toplevel()
        text = tk.Label(pop, text="Are you sure you want to EXIT?")
        text.grid(row=1,column=0)
        no = tk.Button(pop, text="NO", command=pop.destroy)
        no.grid(row=2, column=1)
        yes = tk.Button(pop, text="YES", command=self.root.destroy)
        yes.grid(row=2, column=0)

    def connecting_window(self):
        ''' Clear Content and shade background '''
        self.canvas.delete("all")
        self.canvas.config(bg='#12101f')

        ''' Window Content '''
        self.canvas.create_text(750,200,text="Please Enter the IP Address and Port of the Rocket!",
                           fill="white", font="Times 40")
        quit_button = Button(self.canvas,text="EXIT", h=1, w=4,
                     color="Red",command=lambda: self.exit())
        quit_button.button['font'] = tkFont.Font(size=30)
        quit_button.draw(70,70)
        entry = tk.Entry(self.root, font='Times 35')
        self.canvas.create_window(750,400,window=entry,height=100,width=600)
        record_ip_button = Button(self.canvas,text="SET IP", h=1, w=6,
                                  color="Blue",command=lambda: self.set_ip(entry))
        record_ip_button.button['font'] = tkFont.Font(size=15)
        record_ip_button.draw(990,400)

    def set_ip(self,entry_box):
        full_ip = entry_box.get()
        self.ip = full_ip[0:full_ip.find(':')]
        self.port = full_ip[full_ip.find(':')+1:len(full_ip)]
        test_connection_button = Button(self.canvas,text="Test Connection", h=1, w=15,
                     color="Blue",command=lambda: self.test_connection_window())
        test_connection_button.button['font'] = tkFont.Font(size=20)
        test_connection_button.draw(750,550)
        
    def test_connection_window(self):
        self.canvas.delete(self.connection_status)
        self.connection_status = self.canvas.create_text(750,700,text="",
                           fill="white", font="Times 20")
        result = isOpen(self.ip,self.port)
        if result == 1:
            self.canvas.itemconfig(self.connection_status, fill='green', text='Connection Verified to \n%s:%s'%(self.ip,self.port))
            start_plot_button = Button(self.canvas,text="Start Data Transfer", h=1, w=15,
                     color="green",command=lambda: self.show_pnid())
            start_plot_button.draw(750,100)
        else:
            self.canvas.itemconfig(self.connection_status, fill='red', text='Server Not Responding')

    def show_pnid(self):
        self.canvas.delete("all")
        bkg = "pics/PnID.png"
        img = Image.open(bkg)
        img = img.resize((1280,800), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        
        self.root.geometry("%dx%d"%(img.width(),img.height()))
        self.canvas.config(bg='#f8f8ff',width=img.width(),height=img.height())
        self.canvas.pack()
        self.canvas.create_image(math.ceil(img.width()/2),
                                   math.ceil(img.height()/2),
                                   image=img)
        display_bar = Button(self.canvas,text="Bar Chart", h=1, w=7,
                                  color="Blue",
                             command=lambda: threading.Thread(target=self.show_bar()).start())
        display_bar.draw(1250,20)
        display_line = Button(self.canvas,text="Line Chart", h=1, w=7,
                                  color="Blue",
                              command=lambda: threading.Thread(target=self.show_line()).start())
        display_line.draw(1250,50)
        quit_button = Button(self.canvas,text="EXIT",h=1,w=7,
                     color="Red",command=lambda: self.exit())
        quit_button.draw(1250,80)
        self.root.mainloop()

    def get_data(self):
        # Replace the following code to get data from the rocket
        data = [530,440,2250,380,110,110,90,1100]
        #data = [0.5,.3,.2,.9,1,1.2,.4,.9]
        for i in range(len(data)):
            data[i] += random.random()

        #store data to txt file
        file = open("Result.txt", "w") # Be careful here. 'w' will overwrite file. 
        temp = '\n'+str(datetime.now())+" "+ ', '.join(map(str,data))
        file.write(temp)
        file.close()        

    def show_bar(self):
        plot = plotter(self.sensor_param,self.sensor_list)
        while True:
            self.get_data();
            with open("Result.txt","rb") as file:
                file.seek(-1, os.SEEK_END)
                while file.read(1) != b'\n':
                    file.seek(-2, os.SEEK_CUR)
                data = file.readline().decode()
            data = re.split(r'[;,\s]\s*',data)[2:10]
            for i in range(len(data)):
                data[i]=float(data[i])
            plot.data = data
            plot.bar_plot()
            plt.pause(.5)

    def show_line(self):
        plot = plotter(self.sensor_param,self.sensor_list)
        while True:
            self.get_data();
            with open("Result.txt","rb") as file:
                file.seek(-1, os.SEEK_END)
                while file.read(1) != b'\n':
                    file.seek(-2, os.SEEK_CUR)
                data = file.readline().decode()
            data = re.split(r'[;,\s]\s*',data)[2:10]
            for i in range(len(data)):
                data[i]=float(data[i])
            plot.data = data
            plot.line_plot()
            plt.pause(.5)
