# -*- coding: utf-8 -*-
"""
Created on Sun Dec 18 10:08:43 2022

@author: anba
"""

import pandas as pd
import numpy as np
import os,sys

from scipy.ndimage import gaussian_filter1d
import argparse
import matplotlib.cm as cm
import cmocean
import vispy 


from vispy.app import use_app, Timer
from vispy import app, visuals, scene
from vispy.io import imread, load_data_file, read_mesh, read_png


from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import * 
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
#%% Global Simulation Parameters 
script_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
z_factor = 5
timestep = 1

datetimes = pd.date_range(pd.to_datetime('15 Sept 22'),pd.to_datetime('15 Nov 22'),freq = '1min') ##NUMPTY DONT CHANGE THIS

# set initial timestep 
start_date = pd.to_datetime('25 SEPT 22')
end_date = pd.to_datetime('15 Nov 22')
t = datetimes.get_indexer([start_date], method ='nearest')[0]
#%%

# ######################### Load company logos ##################################
# path = os.sep.join([script_dir,'Logos','Logos.png'])
# logos = scene.visuals.Image(read_png(path))



#%%#############################################################################
#######################  INITIALIZE VISUALIZATION  ############################
###############################################################################

class CanvasWrapper:
    def __init__(self):
        self.canvas = scene.SceneCanvas(keys='interactive',
                                        title='NORI-D Data Viewer',
                                        show=True,
                                        bgcolor = 'black',
                                        size=(1800, 1000))
        
        self.grid =  self.canvas.central_widget.add_grid()
        self.main_view =  self.grid.add_view(row=0,
                                             col=0,
                                             row_span=10,
                                             col_span = 10) # main viewer window
        
        #window for displaying company logos
        self.icon_view = self.grid.add_view(row=9,
                                            col=1,
                                            col_span = 4,
                                            row_span = 1,
                                            margin = 1,
                                            padding = 1) 
        
        #window for displaying company logos
        self.time_view = self.grid.add_view(row=8,
                                            col=7,
                                            col_span = 3,
                                            row_span =2,
                                            margin = 1,
                                            padding = 1) 


        self.init()

    def init(self):
        
        
        #self.icon_view.add(logos)
        
        self.time_display = scene.visuals.Text(datetimes[0].strftime("%d-%b-%y %H:%M"),
                                          color='white',
                                          rotation=0,
                                          font_size = 15,
                                          pos = (380,130),
                                          parent=self.time_view.scene) 
        
        

         # self.FBCT1_velocity_line = scene.visuals.Line(pos = np.array([[0,0,0],[1,1,1]]), width = 1, parent  = self.main_view.scene)
         # self.FBCT1_backscat_line = scene.visuals.Line(pos = gen_ADCP_linepos(FBCT1_backscat_df,'FBCT_001'), width = 10, parent  = self.main_view.scene)
          
        
        self.main_view.camera = 'turntable' 
        
        
        



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, canvas_wrapper: CanvasWrapper, *args, **kwargs):
        super().__init__(*args, **kwargs)

        central_widget = QtWidgets.QWidget()
        main_layout = QtWidgets.QHBoxLayout()

        self.setWindowTitle("DOVE")
        # self.setWidth(1800)
        # self.setFixedHeight(1000)

        self.setGeometry(25, 25, 1800, 1000)
        # self._controls = Controls()
        # main_layout.addWidget(self._controls)
        
        self._canvas_wrapper = canvas_wrapper
        main_layout.addWidget(self._canvas_wrapper.canvas.native)
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)   
        
        
        quit = QtWidgets.QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)
        
        self.paused = False
        # self.sp = QtWidgets.QSlider(QtCore.Qt.Horizontal)
       
        
        
        
        
        # creating a QWidget object
        widget = QtWidgets.QWidget(self)
 
        # creating a vertical box layout
        layout = QtWidgets.QVBoxLayout(self)
 
        # push button 1
        self.PausePlayButton = QtWidgets.QPushButton("Pause", self)
        self.PausePlayButton.clicked.connect(self.pause_play)
        #self.StartButton.valueChanged[int].connect(self.pause_play)
        
        # time slider 
        self.TimeSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.TimeSlider.setRange(0,len(datetimes))
        self.TimeSlider.valueChanged[int].connect(self.update_time)
        
        # timestep dial
        self.TimestepDial = QtWidgets.QDial()
        self.TimestepDial.valueChanged.connect(self.update_timestep)
        self.TimestepDial.setRange(-10,10)
        self.TimestepDial.setNotchesVisible(True)
        self.TimestepDial.setGeometry(220, 125, 200, 60)
        
        self.DialLabel = QtWidgets.QLabel(f"dt = {timestep} min", self)
        self.DialLabel.setAlignment(Qt.AlignCenter)
        # setting geometry to the label
        self.DialLabel.setGeometry(400, 125, 200, 60)
        
        # adding these buttons to the layout
        layout.addWidget(self.PausePlayButton)
        layout.addWidget(self.TimeSlider)
        layout.addWidget(self.DialLabel)
        layout.addWidget(self.TimestepDial)
        
        # setting the layout to the widget
        
        
        widget.setLayout(layout)
        widget.setAutoFillBackground(True)
        # adding widget to the layout
        self.PlaybackDock=QtWidgets.QDockWidget('Playback',self)
        self.PlaybackDock.setFixedSize(200, 300)
        self.PlaybackDock.setWidget(widget)        
        self.PlaybackDock.setGeometry(100, 0, 200, 30)
        #self.PlaybackDock.setFeatures(QtWidgets.QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.PlaybackDock.setAllowedAreas(Qt.NoDockWidgetArea)
        #self.PlaybackDock.setFeatures(QtWidgets.QDockWidget.DockWidgetMovable)
        
        
        # self.TimeSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        # self.TimeSlider.setRange(0,len(datetimes))
        # self.TimeSlider.valueChanged[int].connect(self.update_time)
        
        # self.TimeStepDial = QtWidgets.QDial()
        
        # self.PlaybackDock.setWidget(self.TimeSlider)
        # self.PlaybackDock.setWidget(self.TimeStepDial)
        
    def update_timestep(self):
        global timestep
        timestep = self.TimestepDial.value()
        
        self.DialLabel.setText(f"dt = {timestep} min")
        
        
    def update_time(self):
        global t
        t = self.TimeSlider.value()
        
        canvas.main_view.update()
        
    def pause_play(self):
        if not self.paused:
            timer.stop()
            self.paused = True
            self.PausePlayButton.setText('Play')
        else:
            timer.start()
            self.paused = False
            self.PausePlayButton.setText('Pause')
        
        
    def closeEvent(self, event):
        close = QtWidgets.QMessageBox()
        close.setText("You sure?")
        close.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
        close = close.exec()

        if close == QtWidgets.QMessageBox.Yes:
            event.accept()
            timer.stop()
        else:
            event.ignore()
        




# main_view.camera = 'turntable' 

#%% MAIN LOOP





def update_data(ev):
    
    global t
    t = (t+timestep)%(len(datetimes))
    time = datetimes[t]
    
    
    win.TimeSlider.setValue(t)
 
    canvas.time_display.text = time.strftime("%d-%b-%y %H:%M")
    

     
     
    # pos = calculate_progv(FBCT1_velocity_df,t-lagdist,t,'FBCT_001')
    # fbct1_ctd_colors = gen_CTD_colors(np.flip(FBCT1_CTD_df['Turbidity'][t-lagdist:t].to_numpy()))
    # fbct1_backscat_colors = vispy.color.color_array.ColorArray(color=backscat_cmap(FBCT1_backscat_df.iloc[t].to_numpy()), alpha=None, clip=False, color_space='rgb')
    # canvas.FBCT1_velocity_line.set_data(pos = pos, width = 3,color = fbct1_ctd_colors)
    # canvas.FBCT1_backscat_line.set_data(color = fbct1_backscat_colors )
    


global timer,canvas
if __name__ == '__main__':
    
    
    app = use_app("pyqt5")
    app.create()
    
    
    canvas = CanvasWrapper()
    # load_Tree()
    win = MainWindow(canvas)
    
    
    timer = Timer("auto", connect=update_data, start=True, app = app)
    win.destroyed.connect(timer.stop)

    win.show()
    app.run()    

