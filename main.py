"""
Module: Main module
Description: Contains main GUI
            Reference for GUI code taken from Stackoverflow
"""
import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from AppThreads import SerialThread
from Utility import DataUtility

import VersionLog

#-----Main GUI code-----
class MonitoringApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, 'REIINN Housekeeping GUI' + VersionLog.GUI_VERSION)
        container = tk.Frame(self, background='light blue')
        container.pack(side="top", fill="both", expand=True, ipady=0, pady=0) #
        #Graph Display
        graphFrame = GraphVSWR(container, self)
        graphFrame.place(x=10, y=10, width=500, height=520, ) 
        #Values Display
        valuesFrame = getValues(container, self)
        valuesFrame.place(x=10, y=530, width=500, height=110) 

class GraphVSWR(tk.Frame):

    def __init__(self, parent, controller, nb_points=100):
        tk.Frame.__init__(self, parent)
        # Plot for VSWR
        self.graphFigure = Figure(figsize=(2, 1), dpi=100)
        self.ax = self.graphFigure.add_subplot(2, 1, 1)
        self.ax.set_title('VSWR and Temperature Monitoring')
        self.ax.set_ylabel('VSWR')
        self.x_data = list(range(0, nb_points))
        self.y_data = [0 for i in range(nb_points)]
        
        self.plot = self.ax.plot(self.x_data, self.y_data, label='Time')[0]
        self.ax.set_ylim(0, 5)
        self.ax.set_xlim(0, nb_points)
        self.ax.grid(visible=True, which='major', color='#666666', linestyle='-')
        self.ax.minorticks_on()
        self.ax.grid(visible=True, which='minor', color='#666666', linestyle='-', alpha=0.2)   
        self.graphCanvas = FigureCanvasTkAgg(self.graphFigure, self)
        
        # Plot for Temp
        self.ax1 = self.graphFigure.add_subplot(2, 1, 2, sharex=self.ax)
        self.ax1.set_ylabel('System Temp')
        
        self.x_data1 = list(range(0, nb_points))
        self.y_data1 = [0 for i in range(nb_points)]
        # create the plot
        self.plot1 = self.ax1.plot(self.x_data1, self.y_data1, label='Time')[0]
        self.ax1.set_ylim(0, 80)
        self.ax1.set_xlim(0, nb_points)
        self.ax1.grid(visible=True, which='major', color='#666666', linestyle='-')
        self.ax1.minorticks_on()
        self.ax1.grid(visible=True, which='minor', color='#666666', linestyle='-', alpha=0.2)   
        self.graphCanvas = FigureCanvasTkAgg(self.graphFigure, self)
        toolbar = NavigationToolbar2Tk(self.graphCanvas, self)
        toolbar.update()

        self.graphCanvas.get_tk_widget().place(width=500, height=500)
        self.plotVSWR()

    #-----plot data-----
    def plotVSWR(self):
        self.vswr_value = float(DataUtility.vswr_value)
        self.vswr_status = DataUtility.vswr_status
        self.temp_data = float(DataUtility.temp_value)
        # append new data point to the x and y data
        self.y_data.append(self.vswr_value)
        self.y_data1.append(self.temp_data)
        # remove oldest data point
        self.y_data = self.y_data[1:]
        self.y_data1 = self.y_data1[1:]
        #  update plot data
        self.plot.set_xdata(self.x_data)
        self.plot.set_ydata(self.y_data)
        self.plot1.set_xdata(self.x_data1)
        self.plot1.set_ydata(self.y_data1)
        # redraw plot
        self.graphCanvas.draw_idle()
        # repeat after 1s
        self.after(1000, self.plotVSWR)

class getValues(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #tk.Tk.configure(self, bg='blue')
        self.displayValues()
    
    def displayValues(self):

        vswr = DataUtility.vswr_value
        forwardPower = DataUtility.fwd_pwr
        reversePower = DataUtility.rev_pwr
        tempMCP9700 = DataUtility.temp_value
        tempAD8364 = DataUtility.vswr_temp
        vswr_status = DataUtility.vswr_status

        vswr_bg_color = 'gray' #(0 > VSWR < 20)
        vswr_label = 'DISCONNECTED'

        if (vswr_status == '1'): #(1 > VSWR < 1.5)
            vswr_bg_color = 'green'
            vswr_label = 'NORMAL'

        if (vswr_status == '2'): #(1.5 > VSWR < 2.8)
            vswr_bg_color = '#cccc00'
            vswr_label = 'LOW WARNING'

        if (vswr_status == '3'): #(2.8 > VSWR < 20)
            vswr_bg_color = 'orange'
            vswr_label = 'HIGH WARNING'

        if (vswr_status == '4'): #(2.8 > VSWR < 20)
            vswr_bg_color = 'red'
            vswr_label = 'DANGER'

        tk.Label(self, height=2, width=20, bg='#404040', text='RF Power(dBm)').grid(row=1,column=1)
        tk.Label(self, height=2, width=20, bg='#737373', text='Forward: %s'%(forwardPower)).grid(row=2,column=1)
        tk.Label(self, height=2, width=20, bg='#737373', text='Reverse: %s'%(reversePower)).grid(row=3,column=1)

        tk.Label(self, height=2, width=20, bg='#404040', text='VSWR Status').grid(row=1,column=2)
        
        vswr_value = tk.Label(self, height=2, width=20, text='VSWR: %s'%(vswr)) #bg= vswr_bg_color,
        vswr_value.config(bg=vswr_bg_color)
        vswr_value.grid(row=2,column=2)
        
        vswr_label = tk.Label(self, height=2, width=20, text='%s'%(vswr_label))
        vswr_label.config(bg=vswr_bg_color)
        vswr_label.grid(row=3,column=2)

        tk.Label(self, height=2, width=20, bg='#404040', text='Temperature(\xb07C)').grid(row=1,column=3)
        tk.Label(self, height=2, width=20, bg='#737373', text='System: %s'%(tempMCP9700)).grid(row=2,column=3)
        tk.Label(self, height=2, width=20, bg='#737373', text='Chip: %s'%(tempAD8364)).grid(row=3,column=3)

        self.after(1000, self.displayValues)  # repeat after 1s

#Run serial read on separate thread
SerialThread()
#Run Python GUI
app = MonitoringApp()
app.geometry('520x655')
app.mainloop()
