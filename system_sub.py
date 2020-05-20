import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random
import sys
from datetime import datetime

def receiver(sender_IP, Port):
    data = [.5,.6,.4,.8,.7]
    for i in range(len(data)):
        data[i] += random.random()
    return data

def save_data(data, filename):
    file = open(filename, "w") # Be careful here. 'w' will overwrite file. 
    temp = str(datetime.now())+" "+ ', '.join(map(str,data))+'\n'
    file.write(temp)
    file.close()

class plotter(object):
    def __init__(self, sensor_param, sensor_list, data = [], width = 0.8, ymax = 1.5, ymin = 0):
        # input param
        self.sensor_param = sensor_param
        self.sensor_list = sensor_list
        self.data = data
        self.width = width
        self.ymax = ymax
        self.ymin = ymin

        # additional param
        self.color = []
        self.indices = 0
        self.data_list = []
        self.init = 0
        
    def bar_plot(self):
        color = []
        data = []
        for i in range(len(self.data)):
            if float(self.data[i]) > self.sensor_param[self.sensor_list[i]][3] or float(self.data[i]) < self.sensor_param[self.sensor_list[i]][0]:
                color.append('red')
            elif float(self.data[i]) > self.sensor_param[self.sensor_list[i]][2] or float(self.data[i]) < self.sensor_param[self.sensor_list[i]][1]:
                color.append('yellow')
            else:
                color.append('green')
            data.append((self.data[i]-self.sensor_param[self.sensor_list[i]][0])/(self.sensor_param[self.sensor_list[i]][3]-self.sensor_param[self.sensor_list[i]][0]))
        self.color = color
        self.indices = np.arange(len(self.data))
        plt.clf()
        plt.xticks(self.indices,self.sensor_list)
        plt.bar(self.indices, data, width=self.width, alpha = 1, color=self.color)
        plt.ylim(top=self.ymax)
        plt.ylim(bottom=self.ymin)
        plt.pause(1)

    def line_plot(self):
        if len(self.data_list) <= 30:
            self.data_list.append(self.data[0])
        else:
            self.data_list.pop(0)
            self.data_list.append(self.data[0])
        x = []
        for i in range(len(self.data_list)):
            x.append(i-len(self.data_list))
        print(x)
        print(self.data_list)
        print(self.data)
        #if not self.init:
            #self.fig,self.plts = plt.subplots(len(self.data_list))
            #self.init = 1
        #for i in range(len(self.data_list)):
        plt.clf()    
        plt.plot(x,self.data_list, color='blue', linewidth=2)
        plt.pause(0.6)
        #for i in range(len(self.data_list)):
        #plt.plot(x,self.data_list, color='white', linewidth=3)
        #plt.clf()
        
