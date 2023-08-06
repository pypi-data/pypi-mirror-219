# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 11:01:11 2023

@author: Administrator
"""

import configparser
from scipy.signal import find_peaks

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import glob 
import os
import logging

from scipy.ndimage.filters import uniform_filter1d

from scipy.signal import convolve2d
from scipy.interpolate import interp1d


from skimage.transform import rescale, resize 

from pyproj import Geod
geod = Geod(ellps="WGS84")

import sys
import matplotlib

from PyQt5 import QtCore, QtGui, QtWidgets

from matplotlib.gridspec import GridSpec
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import qdarktheme
import time

from matplotlib.path import Path as MPL_Path

from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from matplotlib.colors import ListedColormap
import re
import traceback
import zipfile

import xarray as xr
import matplotlib.dates as mdates
#%% inspection GUI

class MplCanvas(FigureCanvasQTAgg ):

    def __init__(self, parent=None, dpi=150):
        self.fig = Figure(figsize=None, dpi=dpi,facecolor='gray')
        super(MplCanvas, self).__init__(self.fig)

        
class MainWindow(QtWidgets.QMainWindow):
    

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.canvas =  MplCanvas(self, dpi=150)
                
        self.echodata=dict()
        self.echodata_swarm=dict()
        self.df_nasc=pd.DataFrame([])

        
        self.filecounter=-1
        self.filenames = None
        self.df_files = pd.DataFrame([])

        self.folder_source=''
        self.statusBar().setStyleSheet("background-color : k")


        menuBar = self.menuBar()

        # Creating menus using a title
        openMenu = menuBar.addAction("Select echogram files")
        openMenu.triggered.connect(self.openfiles_fun)

        
        self.showfolderbutton =  menuBar.addAction('Show data folder')
        # self.showfolderbutton.setEnabled(False)
        self.showfolderbutton.triggered.connect(self.showfoldefunc)     

        
        self.showfolderbutton =  menuBar.addAction('Undo mask change')
        # self.showfolderbutton.setEnabled(False)
        self.showfolderbutton.triggered.connect(self.undo_mask)     
  
        quitMenu = menuBar.addAction("Quit")
        quitMenu.triggered.connect(self.func_quit)     
    

        toolbar = QtWidgets.QToolBar()

        self.checkbox_mask=QtWidgets.QCheckBox('Save changes')
        self.checkbox_mask.setChecked(False)            
        toolbar.addWidget(self.checkbox_mask)
        
        self.checkbox_raw=QtWidgets.QCheckBox('Raw')
        self.checkbox_raw.setChecked(False)           
        self.checkbox_raw.clicked.connect(self.choose_raw_changed)          
        toolbar.addWidget(self.checkbox_raw)

        toolbar.addWidget(QtWidgets.QLabel('Freq.:'))        
        self.choose_freq = QtWidgets.QComboBox()
        self.choose_freq.addItem('38')
        self.choose_freq.addItem('120')
        self.choose_freq.addItem('200')
        self.choose_freq.setCurrentIndex(1)
        toolbar.addWidget(  self.choose_freq)
        toolbar.addWidget(QtWidgets.QLabel('kHz'))            
        self.choose_freq.activated[str].connect(self.choose_freq_changed) 

        toolbar.addWidget(QtWidgets.QLabel('Color:'))        
        self.choose_color = QtWidgets.QComboBox()
        self.choose_color.addItem('viridis')
        self.choose_color.addItem('plasma')
        self.choose_color.addItem('jet')
        self.choose_color.setCurrentIndex(2)
        toolbar.addWidget(  self.choose_color)
        self.choose_color.activated[str].connect(self.choose_color_changed) 
        
        

        toolbar.addWidget(QtWidgets.QLabel('Min. depth:'))        
        self.excl_depth_spin = QtWidgets.QSpinBox()
        self.excl_depth_spin.setMinimum(0)
        self.excl_depth_spin.setMaximum(8000)
        self.excl_depth_spin.setValue(20)
        toolbar.addWidget(  self.excl_depth_spin)
        toolbar.addWidget(QtWidgets.QLabel('m'))        

        toolbar.addWidget(QtWidgets.QLabel('Max. depth:'))        
        self.max_depth_spin = QtWidgets.QSpinBox()
        self.max_depth_spin.setMinimum(0)
        self.max_depth_spin.setMaximum(8000)
        self.max_depth_spin.setValue(500)

        toolbar.addWidget(  self.max_depth_spin)
        toolbar.addWidget(QtWidgets.QLabel('m'))              
        
        self.butt_prev=QtWidgets.QPushButton('<-- previous')
        self.butt_prev.clicked.connect(self.plot_prev)        
        toolbar.addWidget(self.butt_prev)

        self.butt_next=QtWidgets.QPushButton('Next -->')
        self.butt_next.clicked.connect(self.plot_next)        
        toolbar.addWidget(self.butt_next)
        
                #### hotkeys
        self.msgSc1 = QtWidgets.QShortcut(QtCore.Qt.Key_Right, self)
        self.msgSc1.activated.connect(self.plot_next)
        self.msgSc2 = QtWidgets.QShortcut(QtCore.Qt.Key_Left, self)
        self.msgSc2.activated.connect(self.plot_prev)        


        self.butt_removearea=QtWidgets.QPushButton('Remove area')
        self.butt_removearea.clicked.connect(self.mask_removearea)        
        toolbar.addWidget(self.butt_removearea)
        
        self.butt_addarea=QtWidgets.QPushButton('Add area')
        self.butt_addarea.clicked.connect(self.mask_addarea)        
        toolbar.addWidget(self.butt_addarea)
        
        toolbar.addSeparator()

         
        tnav = NavigationToolbar( self.canvas, self)       
        toolbar.addWidget(tnav)
       
        outer_layout = QtWidgets.QVBoxLayout()
        outer_layout.addWidget(toolbar)
        outer_layout.addWidget(self.canvas)
    
        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QtWidgets.QWidget()
        widget.setLayout(outer_layout)
        self.setCentralWidget(widget)
        
        
        self.show()  
   

        self.cmap_mask = ListedColormap( np.array([[1,0,0, 1. ]] ) )
        
        
        self.t=[-1,-1]
        self.plotwindow_startsecond=0
        self.plotwindow_length=0
  
        
    def settings_edit(self):
        os.startfile(self.ini_file)    
   
                  
    def showfoldefunc(self):    
         os.startfile(self.workpath)
         
    def openfiles_fun(self):
        
        fname_canidates, ok = QtWidgets.QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()",'',"Echogram Files (*_echogram.nc)")
         
        if len( fname_canidates ) >0:
            
            self.filenames = np.array( fname_canidates )   
            print(  fname_canidates )
            
            self.workpath = os.path.dirname( fname_canidates[0])
        
            self.filecounter=-1
               
            self.plot_next()
            
    def choose_color_changed(self):
        if self.filecounter>=0:        
            self.plot_echogram()

    def choose_raw_changed(self):
        if self.filecounter>=0:        
            self.plot_echogram()
            
    def plot_echogram(self):    
        
                
        # breakpoint()
        
        ix_f = self.xr_sv.coords['frequency']== int(self.choose_freq.currentText()) *1000
        sv = np.squeeze( self.xr_sv[ix_f,:,:])
        

            
                
        # sv = sv.interpolate_na( dim='time', method="linear")
        
        # sv = sv.interpolate_na(  'depth',max_gap=3,method="linear")
        # sv = sv.interpolate_na(  'time' ,max_gap=pd.Timedelta(seconds=5))
        
        # sv = sv.interp(time=sv.time , depth=sv.depth, method="linear")
        
        

        sv_mask=sv.copy()
        sv_mask.values [~self.mask_manual.values]=np.nan

        
        cell_thickness=np.abs(np.mean(np.diff( self.xr_sv.coords['depth']) ))        
        
        track= pd.DataFrame([])
        track.index= self.xr_sv.coords['time']      
        track['nasc_swarm'] =4*np.pi*1852**2 * np.nansum( np.power(10, sv_mask /10)*cell_thickness ,axis=0)   
          
        # peak filter
        x = track['nasc_swarm'].values.copy()
        peaks, peak_meta = find_peaks(x,prominence=10000,width=[0,2] )
        # x[peaks]=np.nan
        
        ix1 = np.round( peak_meta['left_ips']).astype(int)-1
        ix2 = np.round( peak_meta['right_ips']).astype(int)+1
        
        ix1[ix1<0]=0
        ix2[ix2>len(x)-1]=len(x)-1
        
        for i1,i2 in zip(ix1,ix2):
            x[i1:i2]=np.nan

        track['nasc_swarm']=x
        track['nasc_swarm']=track['nasc_swarm'].interpolate()
        
        # duration =     ( self.xr_sv.coords['time'][-1] - self.xr_sv.coords['time'][0]).data  / np.timedelta64(1, 's')
        # dm=self.xr_sv.coords['depth'][-1].data
        
        
        self.canvas.fig.clf() 
                
        self.ax = self.canvas.fig.subplots(2, 1, gridspec_kw={'height_ratios': [1, 3]},sharex=True)
        ax=self.ax
        
        ax[0].plot( track['nasc_swarm'] , '-k')
        ax[0].plot( track['nasc_swarm'].resample('1min').mean(), '.-b')
        
        
        ax[0].grid()
        # ax[0].set_xlim( self.xr_sv.coords['time'].min() , self.xr_sv.coords['time'].max())
        ax[0].set_ylabel('NASC')
        
        # plt.gca=ax[1]
        
        x_lims = mdates.date2num( [  self.xr_sv.coords['time'].min().values , self.xr_sv.coords['time'].max().values ])
        range_max = self.xr_sv.coords['depth'].max()
        ext=[x_lims[0] ,x_lims[1],-range_max ,0 ]
        
        if self.checkbox_raw.isChecked():
            fname= self.filenames[self.filecounter]
            self.xr_sv_raw = xr.open_dataarray(fname[:-12] + '_rawechogram.nc')
            sv_raw = np.squeeze( self.xr_sv_raw[ix_f,:,:])
            im = ax[1].imshow( sv_raw,cmap= self.choose_color.currentText()   ,aspect='auto',vmin=-90,vmax=-30,extent=ext)
            
        else:    
            im = ax[1].imshow( sv,cmap= self.choose_color.currentText()   ,aspect='auto',vmin=-90,vmax=-30,extent=ext)
        
        masked_data = np.ma.masked_where(self.mask_manual == 1, self.mask_manual)
        
        
        ax[1].imshow( masked_data  ,aspect='auto',extent=ext,cmap=self.cmap_mask,alpha=0.3)
        
        # cbar3 = plt.colorbar(im)
        ax[1].xaxis_date()
        ax[1].grid()
        ax[1].set_ylabel('Depth in m')
        ax[1].set_ylim(-self.max_depth_spin.value(),0)

        ax[1].plot(x_lims,[-self.excl_depth_spin.value(),-self.excl_depth_spin.value()] ,'-r' )
        
        

        cbaxes = inset_axes(ax[1], width="15%", height="3%", loc='lower left',  bbox_to_anchor=(0.05, 0.15, 1, 1) ,bbox_transform= ax[1].transAxes) 
        self.canvas.fig.colorbar(im,cax=cbaxes,label='$s_v$', orientation='horizontal')        
            
        
            #         cbaxes = inset_axes(self.canvas.axes4, width="100%", height="100%", loc=3,bbox_to_anchor=(.05, .15, .4, .04),bbox_transform=self.canvas.axes4.transAxes) 
            # cbar=self.canvas.fig.colorbar(sc,cax=cbaxes, orientation='horizontal')
            
            

        self.canvas.fig.tight_layout()
        self.canvas.draw()

   
    def choose_freq_changed(self):
        if self.filecounter>=0:   
            self.plot_echogram()

        
    def read_file_and_mask(self):    
        if self.filecounter>=0:        
            fname= self.filenames[self.filecounter]
            
            # if fname.split('.')[-1]=='nc':
            
            
            self.xr_sv = xr.open_dataarray(fname)
            
            # breakpoint()
            
            f_list = (self.xr_sv.coords['frequency'].values / 1000).astype(int).astype(str)
            self.choose_freq.clear()
            if isinstance(f_list, str):
                f_list=[f_list]
            self.choose_freq.addItems(f_list)
            
            try:
                ix_120 = np.where( self.xr_sv.coords['frequency'].values==120000)[0][0] 
            except:
                ix_120 = np.argmax( self.xr_sv.coords['frequency'].values)
                
            
            self.choose_freq.setCurrentIndex( ix_120 )
            # self.choose_freq.setCurrentIndex( np.argmax(self.xr_sv.coords['frequency'].values) )

            if os.path.isfile(fname[:-12] + '_mask_manual.h5' ):     
                self.mask_manual= np.transpose(  pd.read_hdf( fname[:-12] + '_mask_manual.h5',key='df' ) )
            else:
                if os.path.isfile(fname[:-12] + '_mask_swarm.h5' ):     
                    self.mask_swarm= np.transpose(  pd.read_hdf( fname[:-12] + '_mask_swarm.h5',key='df' ) )
                    self.mask_manual = self.mask_swarm.copy()
                    ixdepthvalid= ( self.xr_sv.coords['depth'] >= self.excl_depth_spin.value() ) & ( self.xr_sv.coords['depth']  <= self.max_depth_spin.value())
                    self.mask_manual.values[~ixdepthvalid,:]=False  
                else:
                    
                    s2=len( self.xr_sv.coords['time'])
                    s1=len( self.xr_sv.coords['depth'])
                    self.mask_manual=pd.DataFrame( np.ones([s1,s2]).astype(bool)   )
                    self.mask_manual.columns=self.xr_sv.coords['time']
                    self.mask_manual.index=self.xr_sv.coords['depth']
                    ixdepthvalid= ( self.xr_sv.coords['depth'] >= self.excl_depth_spin.value() ) & ( self.xr_sv.coords['depth']  <= self.max_depth_spin.value())
                    self.mask_manual.values[~ixdepthvalid,:]=False                  
          
            self.mask_manual_old=self.mask_manual.copy() 
  
                
            # self.mask_dbdiff= np.transpose( pd.read_hdf( fname[:-12] + '_mask_dbdiff.h5',key='df' ) )
            

            
    def undo_mask(self):
        self.mask_manual=self.mask_manual_old.copy() 
        self.plot_echogram()            

                
    def onclick_draw(self,event):
            # print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
            #       ('double' if event.dblclick else 'single', event.button,
            #        event.x, event.y, event.xdata, event.ydata))
            if event.button==1 & event.dblclick:
                self.draw_x=self.draw_x.append( pd.Series(event.xdata) ,ignore_index=True )
                self.draw_y=self.draw_y.append( pd.Series(event.ydata) ,ignore_index=True )
                # self.f_limits=self.canvas.axes.get_ylim()
                # self.t_limits=self.canvas.axes.get_xlim()   
                
                line = self.line_2.pop(0)
                line.remove()        
                self.line_2 =self.ax[1].plot(self.draw_x,self.draw_y,'.-r')      
                self.canvas.draw()    
                         
                # func_draw_shape_plot()   
              
            if event.button==3:
                self.draw_x=self.draw_x.head(-1)
                self.draw_y=self.draw_y.head(-1)
                # self.f_limits=self.canvas.axes.get_ylim()
                # self.t_limits=self.canvas.axes.get_xlim()
                # func_draw_shape_plot()              
                line = self.line_2.pop(0)
                line.remove()        
                self.line_2 =self.ax[1].plot(self.draw_x,self.draw_y,'.-r')     
                self.canvas.draw()                   
 
    def mask_removearea(self):
            
        # msg = QtWidgets.QMessageBox()
        # msg.setIcon(QtWidgets.QMessageBox.Information)   
        # msg.setText("Add points with double left click.\nRemove latest point with single right click. \nExit draw mode by pushing enter")
        # msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        # returnValue = msg.exec()    
        # if returnValue == QtWidgets.QMessageBox.Ok:
            self.butt_removearea.setEnabled(False)   
            print('drawing')  
            self.draw_x=pd.Series(dtype='float')
            self.draw_y=pd.Series(dtype='float')
            self.d_limits=self.ax[1].get_ylim()
            self.t_limits=self.ax[1].get_xlim()
            self.plot_echogram()
            
            # self.canvas.fig.canvas.mpl_disconnect(self.cid1)    
            self.cid2=self.canvas.fig.canvas.mpl_connect('button_press_event', self.onclick_draw)
            self.line_2 =self.ax[1].plot(self.draw_x,self.draw_y,'.-r')        
            # self.plot_echogram()   
            self.drawexitm = QtWidgets.QShortcut(QtCore.Qt.Key_Return, self)
            self.drawexitm.activated.connect(self.func_draw_shape_exit_remove)  
         
    def func_draw_shape_exit_remove(self):
        # print('save shape' + str(self.draw_x.shape))
        self.canvas.fig.canvas.mpl_disconnect(self.cid2)
        ## deactive shortcut
        self.drawexitm.setEnabled(False)  

        if self.draw_x.shape[0]>2:

            
            # breakpoint()
            
            m = np.transpose( self.mask_manual )
            t = mdates.date2num( m.index )
            d = -m.columns 
            

            kk_t,kk_d=np.meshgrid( t,d)   
            # kernel=np.zeros( [ k_f.shape[0] ,k_t.shape[0] ] )
            x, y = kk_t.flatten(), kk_d.flatten()
            points = np.vstack((x,y)).T 
            
            p = MPL_Path(list(zip( self.draw_x.values , self.draw_y.values))) # make a polygon
            grid = p.contains_points(points)
            m_shapemask = grid.reshape(kk_t.shape) # now you have a mask with points inside a polygon  
            self.mask_manual_old=self.mask_manual.copy() 
            self.mask_manual.values[ m_shapemask ] = False
                  
        self.plot_echogram()
        self.butt_removearea.setEnabled(True)   

         
    def func_draw_shape_exit_add(self):
        # print('save shape' + str(self.draw_x.shape))
        self.canvas.fig.canvas.mpl_disconnect(self.cid2)
        ## deactive shortcut
        self.drawexitm.setEnabled(False)  

        if self.draw_x.shape[0]>2:

            # breakpoint()
            
            m = np.transpose( self.mask_manual )
            t = mdates.date2num( m.index )
            d = -m.columns 
            

            kk_t,kk_d=np.meshgrid( t,d)   
            # kernel=np.zeros( [ k_f.shape[0] ,k_t.shape[0] ] )
            x, y = kk_t.flatten(), kk_d.flatten()
            points = np.vstack((x,y)).T 
            
            p = MPL_Path(list(zip( self.draw_x.values , self.draw_y.values))) # make a polygon
            grid = p.contains_points(points)
            m_shapemask = grid.reshape(kk_t.shape) # now you have a mask with points inside a polygon  
            self.mask_manual_old=self.mask_manual.copy() 
            self.mask_manual.values[ m_shapemask ] = True
                  
        self.plot_echogram()   
        self.butt_addarea.setEnabled(True)     
         


    def mask_addarea(self):
        # msg = QtWidgets.QMessageBox()
        # msg.setIcon(QtWidgets.QMessageBox.Information)   
        # msg.setText("Add points with double left click.\nRemove latest point with single right click. \nExit draw mode by pushing enter")
        # msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        # returnValue = msg.exec()    
        # if returnValue == QtWidgets.QMessageBox.Ok:
            self.butt_addarea.setEnabled(False)     

            print('drawing')  
            self.draw_x=pd.Series(dtype='float')
            self.draw_y=pd.Series(dtype='float')
            self.d_limits=self.ax[1].get_ylim()
            self.t_limits=self.ax[1].get_xlim()
            self.plot_echogram()
            
            # self.canvas.fig.canvas.mpl_disconnect(self.cid1)    
            self.cid2=self.canvas.fig.canvas.mpl_connect('button_press_event', self.onclick_draw)
            self.line_2 =self.ax[1].plot(self.draw_x,self.draw_y,'.-g')        
            # self.plot_echogram()   
            self.drawexitm = QtWidgets.QShortcut(QtCore.Qt.Key_Return, self)
            self.drawexitm.activated.connect(self.func_draw_shape_exit_add)  
        
        
        
    def save_changes(self):
       
        
        m = np.transpose( self.mask_manual )
        fname= self.filenames[self.filecounter]
        m.to_hdf( fname[:-12] + '_mask_manual.h5',key='df' )
        
        # calc nasc
        ix_f = self.xr_sv.coords['frequency']== int(self.choose_freq.currentText()) *1000
        sv_mask = np.squeeze( self.xr_sv[ix_f,:,:]).copy()
        sv_mask.values [~self.mask_manual.values]=np.nan

        cell_thickness=np.abs(np.mean(np.diff( self.xr_sv.coords['depth']) ))        
        nasc = 4*np.pi*1852**2 * np.nansum( np.power(10, sv_mask /10)*cell_thickness ,axis=0)   

        # peak filter
        x = nasc.copy()
        peaks, peak_meta = find_peaks(x,prominence=10000,width=[0,2] )
        # x[peaks]=np.nan
       
        ix1 = np.floor( peak_meta['left_ips']).astype(int)-1
        ix2 = np.ceil( peak_meta['right_ips']).astype(int)+1         
        ix1[ix1<0]=0
        ix2[ix2>len(x)-1]=len(x)-1
         
        for i1,i2 in zip(ix1,ix2):
             x[i1:i2]=np.nan
        
        track=  pd.read_hdf( fname[:-12] + '_nasctable.h5',key='df' ) 

        track['nasc_manual']=x
        track['nasc_manual']=track['nasc_manual'].interpolate()


        # track['nasc_manual'] =nasc
        track.to_hdf( fname[:-12] + '_nasctable.h5',key='df'  )
        track.to_csv( fname[:-12] + '_nasctable.csv' )
        
        
        
    def plot_next(self):
         if len(self.filenames)>0:
            print('old filecounter is: '+str(self.filecounter))
            
            if self.checkbox_mask.isChecked():
                self.save_changes()
                
           
            self.filecounter=self.filecounter+1
            if self.filecounter>len(self.filenames)-1:
                self.filecounter=len(self.filenames)-1
                print('That was it')
            self.read_file_and_mask()
            self.plot_echogram()
            
            

    def plot_prev(self):
         if len(self.filenames)>0:   
            print('old filecounter is: '+str(self.filecounter))
            
            if self.checkbox_mask.isChecked():
                self.save_changes()

         
            self.filecounter=self.filecounter-1
            if self.filecounter<0:
                self.filecounter=0
                print('That was it')
            # new file    
            # self.filecounter=self.filecounter+1
            self.read_file_and_mask()
            self.plot_echogram()
                
         
     
######
             

    def func_quit(self):
        self.statusBar().setStyleSheet("background-color : k")
        # self.statusBar().removeWidget(self.label_1)   
        # self.startautoMenu.setEnabled(True)
        # self.exitautoMenu.setEnabled(False)     
        QtWidgets.QApplication.instance().quit()     
        # QCoreApplication.quit()
        self.close()    
        

class gui():
    def __init__(self, *args, **kwargs):
        app = QtWidgets.QApplication(sys.argv)
        app.setApplicationName("Krillscan")    
        app.setStyleSheet(qdarktheme.load_stylesheet())
        w = MainWindow()
        sys.exit(app.exec_())

# inspect=ks()

# app = QtWidgets.QApplication(sys.argv)
# app.setApplicationName("Krillscan")    
# app.setStyleSheet(qdarktheme.load_stylesheet())
# w = MainWindow()
# sys.exit(app.exec_())
     
    
        
