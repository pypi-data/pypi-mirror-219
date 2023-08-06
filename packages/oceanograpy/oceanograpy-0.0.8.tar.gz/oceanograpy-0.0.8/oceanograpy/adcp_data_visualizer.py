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

#%%
from workhorse_adcp import workhorse_adcp as wh_adcp 
from seabird_ctd import seabird_ctd as sb_ctd 
from processing_tools import processing_tools as ptools 
from matplotlib_dhi import subplots 
import adcp_plot_tools

import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd, numpy as np

#%%
pt3_filepath = r'\\USDEN1-STOR.DHI.DK\Projects\41806287\41806287 NORI-D Data\Data\ROV\Island Pride HD14\ADCP\Config\ROV_ADCP_20161_PT3.txt'
#adcp_filepath = r'\\USDEN1-STOR.DHI.DK\Projects\41806287\41806287 NORI-D Data\Data\ROV\Island Pride HD14\ADCP\Raw\ADCP_24142_600kHz\ROV_ADCP_12102022\_RDI_005.000'
adcp_filepath = r'\\USDEN1-STOR.DHI.DK\Projects\41806287\41806287 NORI-D Data\Data\ROV\Island Pride HD14\ADCP\Raw\ADCP_24142_600kHz\ROV_ADCP_17102022\_RDI_005.000'


adcp_data = wh_adcp(filepath = adcp_filepath, PT3_filepath = pt3_filepath, verbose = 1)



USBL = pd.read_csv(r'\\USDEN1-STOR.DHI.DK\Projects\41806287\41806287 NORI-D Data\Data\ROV\Island Pride HD14\Position\Processed\01 Merge\USBL_data_all_dives.csv', index_col = [0], parse_dates = True)
HAIN = pd.read_csv(r'\\USDEN1-STOR.DHI.DK\Projects\41806287\41806287 NORI-D Data\Data\ROV\Island Pride HD14\Position\Processed\01 Merge\HAIN_data_all_dives.csv', index_col = [0], parse_dates = True)


pos_in = HAIN[['Easting','Northing','Depth']].copy(deep = True)
pos_in.columns = ['x','y','z']
pos_in['z'] = -pos_in['z']
adcp_data.set_sensor_position(pos_in)


orient_in = HAIN[['Pitch','Roll','Heading']]
orient_in.columns = ['pitch','roll','heading']
adcp_data.set_sensor_orientation(orient_in)


#%% Global Simulation Parameters 
script_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
z_factor = 5
timestep = 1

datetimes = adcp_data.ensemble_times #pd.date_range(pd.to_datetime('15 Sept 22'),pd.to_datetime('15 Nov 22'),freq = '1min') ##NUMPTY DONT CHANGE THIS

# # set initial timestep 
# start_date = pd.to_datetime('25 SEPT 22')
# end_date = pd.to_datetime('15 Nov 22')
# t = datetimes.get_indexer([start_date], method ='nearest')[0]
t = 0
#%%

# ######################### Load company logos ##################################
# path = os.sep.join([script_dir,'Logos','Logos.png'])
# logos = scene.visuals.Image(read_png(path))



#%%#############################################################################
#######################  INITIALIZE VISUALIZATION  ############################
###############################################################################

class CanvasWrapper:
    def __init__(self, adcp_data):
        
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
        
        self.adcp_data = adcp_data


        self.init()

    def init(self):
        
        
        #self.icon_view.add(logos)
        
        
        
        self.time_display = scene.visuals.Text(datetimes[0].strftime("%d-%b-%y %H:%M"),
                                          color='white',
                                          rotation=0,
                                          font_size = 15,
                                          pos = (380,130),
                                          parent=self.time_view.scene) 
        
        
        # self.line = scene.visuals.Markers(pos = adcp_data.position.T,
        #                                     size = 15,
        #                                     spherical = True,
        #                                     scaling = True,
        #                                     parent =self.main_view.scene)
        
        
        self.plane_verts = 30*np.array([[-.5,-.5,0],
                                        [-.5,.5,0],
                                        [.5,.5,0],
                                        [.5,-.5,0],
                                        [-.5,-.5,0]])
        self.plane = scene.visuals.Line(pos = np.add(self.plane_verts , adcp_data.position[:,0]), width = 5, parent  = self.main_view.scene)
        
        
        # self.beam_vec = [(0,0,1),(0,0,1),(0,0,1),(0,0,1)]
        theta_beam = 20
        
        
        # self.beam_vec[0] = np.dot(self.beam_vec[0],ptools.gen_rot_x(theta_beam))
        # self.beam_vec[1] = np.dot(self.beam_vec[1],ptools.gen_rot_x(-theta_beam))
        # self.beam_vec[2] = np.dot(self.beam_vec[2],ptools.gen_rot_y(-theta_beam))
        # self.beam_vec[3] = np.dot(self.beam_vec[3],ptools.gen_rot_y(theta_beam))
        
        
        self.beams = []
        for i in range(adcp_data.n_beams):
            
            beam_pos = np.full((self.adcp_data.n_bins,3),0)
            beam_pos[:,2] = self.adcp_data.bin_midpoints
            self.beams.append(beam_pos)
            
            
        self.beams[0] = np.dot(self.beams[0],ptools.gen_rot_x(theta_beam))
        self.beams[1] = np.dot(self.beams[1],ptools.gen_rot_x(-theta_beam))
        self.beams[2] = np.dot(self.beams[2],ptools.gen_rot_y(-theta_beam))
        self.beams[3] = np.dot(self.beams[3],ptools.gen_rot_y(theta_beam))
        
        #self.beams[2] = adcp_data.get_bin_midpoints

        self.beam_lines = []
        
        for i in range(self.adcp_data.n_beams):
            # self.beam_lines.append(scene.visuals.Markers(pos = np.add(self.beams[i],adcp_data.position[:,0]),
            #                                     size = 5,
            #                                     spherical = False,
            #                                     scaling = True,
            #                                     parent =self.main_view.scene))           
        
            self.beam_lines.append(scene.visuals.Line(pos = np.add(self.beams[i],self.adcp_data.position[:,0]),
                                                width = 1,
                                                parent =self.main_view.scene))         
        
        self.main_view.camera = 'turntable' 
        
        
        
#canvas = CanvasWrapper()
        
        
#%%

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
        # close = QtWidgets.QMessageBox()
        # close.setText("You sure?")
        # close.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
        #close = close.exec()
        timer.stop()
        # if close == QtWidgets.QMessageBox.Yes:
        #     event.accept()
        #     timer.stop()
        # else:
        #     event.ignore()
        


def update_data(ev):
    
    global t,X,Xr,roll,pitch,yaw
    t = (t+timestep)%(len(datetimes))
    time = datetimes[t]
    
    
    win.TimeSlider.setValue(t)
 
    canvas.time_display.text = time.strftime("%d-%b-%y %H:%M")
    
    
    
    #canvas.line.set_data(pos=adcp_data.position[:,t:t+1].T)#,
    
    
    yaw   = canvas.adcp_data.orientation[2][t]
    pitch = canvas.adcp_data.orientation[0][t]
    roll  = canvas.adcp_data.orientation[1][t]
    
    X = canvas.plane_verts 
    R = np.dot(ptools.gen_rot_x(roll),ptools.gen_rot_z(yaw).dot(ptools.gen_rot_y(pitch)))
    X = X.dot(R)
    X = np.add(X , canvas.adcp_data.position[:,t])
    canvas.plane.set_data(pos= X, width = 1)
    
    
  
    
    #,
    #                                 size = 20,
    #                                 face_color = 'green',
    #                                 edge_color = 'yellow',)    

#canvas = CanvasWrapper()

#% MAIN LOOP






     
     
    # pos = calculate_progv(FBCT1_velocity_df,t-lagdist,t,'FBCT_001')
    # fbct1_ctd_colors = gen_CTD_colors(np.flip(FBCT1_CTD_df['Turbidity'][t-lagdist:t].to_numpy()))
    # fbct1_backscat_colors = vispy.color.color_array.ColorArray(color=backscat_cmap(FBCT1_backscat_df.iloc[t].to_numpy()), alpha=None, clip=False, color_space='rgb')
    # canvas.FBCT1_velocity_line.set_data(pos = pos, width = 3,color = fbct1_ctd_colors)
    # canvas.FBCT1_backscat_line.set_data(color = fbct1_backscat_colors )
    


global timer,canvas
if __name__ == '__main__':
    
    
    app = use_app("pyqt5")
    app.create()
    
    
    canvas = CanvasWrapper(adcp_data)
    # load_Tree()
    win = MainWindow(canvas)
    
    
    timer = Timer("auto", connect=update_data, start=True, app = app)
    win.destroyed.connect(timer.stop)

    win.show()
    app.run()    

