# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 14:56:11 2023

@author: anba
"""

import time
import multiprocessing as mp
import progressbar
import pickle
import cloudpickle    

import numpy as np

class processing_tools:
    
        
        
    def pickle_obj(obj,fname):
        """
        Pickle an object
    
        Parameters
        ----------
        obj : Object to pickle
        fname : string
            filename for pickled object
    
        Returns
        -------
        None.
    
        """

        
        with open(fname,"wb") as f:
            
            try:
                pickle.dump(obj,f)
            except:
                cloudpickle.dump(obj,f)
            
    def unpickle_obj(fname):
        """
        Unpickle an object
    
        Parameters
        ----------
        fname : string
            Path to pickled object.
    
        Returns
        -------
        out : unpickled object.
    
        """
    
        with open(fname,"rb") as f:
            
            try:
                out = pickle.load(f) 
            except:
                out = cloudpickle.load(f) 
        return out
    
    def flatten_list(l): # flatten a list of lists
        """
        Parameters
        ----------
        l : list
            List to flatten
    
        Returns
        -------
        out : flattened list
    
        """
        
        out = [item for sublist in l for item in sublist]
        return out
    
    def printProgressBar (iteration, total,taskname = '', prefix = 'Progress', decimals = 1, length = 25, fill = '█', printEnd = "\r"):
        """
        Terminal progress bar
        Args:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            taskname    - Optional  : task description (Str)
            prefix      - Optional  : prefix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
       
        
        taskname = taskname.ljust(100)
        print(f'\r{prefix} |{bar}|{taskname}', end = printEnd)
        # Print New Line on Complete
        if iteration == total: 
            print()  
            
            
    def paralell_fcn(f,iterable,taskname = 'Processing'):
        
        
        """
        Run a function in paralell
    
        Parameters
        ----------
        f : function to run 
        iterable: inpute argument to interate over
        taskname: task label on progress bar
        Returns
        -------
        list of task results
    
        """

        st = time.time()
        cpu_count = min(mp.cpu_count(),len(iterable))
        varname = 'Task'# '_'.join(taskname.split(' '))
        widgets = [progressbar.GranularBar(markers=" ░▒▓█", left='', right='|'),
                    progressbar.widgets.Variable(varname)]
        bar = progressbar.ProgressBar(widgets = widgets, max_value = len(iterable))
        bar.variables[varname] = str(taskname) 
        bar.update(1)
        results = []
        
        #printProgressBar(0, len(iterable),prefix = f'Filtering', taskname= f'Filtering 0%')
            
        with mp.Pool(cpu_count) as pool:
            
            
            #results= pool.map(f,iterable)
            tasks = pool.imap_unordered(f,iterable) 
    
            for r,result in enumerate(tasks):
                bar.update(r+1)
                results.append(result)
                time.sleep(0.1)
                
                #print(r)
        bar.update(r+1)
        #bar.update(len(iterable)) # force bar to 100%
                
        print('\r','\n')
        print(f'Execution Time: {round((time.time() - st)/60,2)} min')
        print('\r','\n')
        return results
    
    
    def gen_rot_y(theta):
        """
        Generate a 3*3 matrix that rotates a vector by angle theta about the y-axis
    
        Parameters
        ----------
        theta : float
            angle to rotate by.
    
        Returns
        -------
        numpy array
            Rotation matrix (Ry).
    
        """
        theta = theta*np.pi/180
        return np.array([(np.cos(theta),0,np.sin(theta)),
                         (0,1,0),
                         (-np.sin(theta),0,np.cos(theta))])
    
    def gen_rot_z(theta):
        """
        Generate a 3*3 matrix that rotates a vector by angle theta about the z-axis
    
        Parameters
        ----------
        theta : float
            angle to rotate by.
    
        Returns
        -------
        numpy array
            Rotation matrix (Rz).
    
        """
        theta = theta*np.pi/180
        return np.array([(np.cos(theta),-np.sin(theta),0),
                         (np.sin(theta),np.cos(theta),0),
                         (0,0,1)])
                         
    def gen_rot_x(theta):
        """
        Generate a 3*3 matrix that rotates a vector by angle theta about the x-axis
    
        Parameters
        ----------
        theta : float
            angle to rotate by.
    
        Returns
        -------
        numpy array
            Rotation matrix (Rx).
    
        """
        theta = theta*np.pi/180
        return np.array([(1,0,0),
                         (0,np.cos(theta),-np.sin(theta)),
                         (0,np.sin(theta),np.cos(theta))])