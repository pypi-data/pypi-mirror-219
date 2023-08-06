# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 19:27:56 2023

@author: anba
"""




import matplotlib.pyplot as plt
import numpy as np
#from matplotlib_dhi import subplots
import time



class easter_egg:
    
    
    def __init__(self):
        # Define the characters for each letter
        letters = {
            'c': np.array([
                [1, 1, 1],
                [1, 0, 0],
                [1, 0, 0],
                [1, 0, 0],
                [1, 1, 1]
            ]),
            'u': np.array([
                [1, 0, 1],
                [1, 0, 1],
                [1, 0, 1],
                [1, 0, 1],
                [1, 1, 1]
            ]),
            'n': np.array([
                [1, 0, 0],
                [1, 1, 0],
                [1, 0, 1],
                [1, 0, 1],
                [1, 0, 1]
            ]),
            't': np.array([
                [1, 1, 1],
                [0, 1, 0],
                [0, 1, 0],
                [0, 1, 0],
                [0, 1, 0]
            ])
        }
        
        # Create an empty canvas
        canvas = np.zeros((7, 19))
        
        # Set the positions for each letter
        positions = {
            'c': (1, 1),
            'u': (1, 6),
            'n': (1, 11),
            't': (1, 15)
        }
        
        # Place each letter on the canvas
        for char in 'cunt':
            letter_matrix = letters[char]
            x, y = positions[char]
            canvas[x:x+letter_matrix.shape[0], y:y+letter_matrix.shape[1]] = letter_matrix
        
        # Add black border by padding the canvas with zeros
        padded_canvas = np.pad(canvas, pad_width=1, mode='constant', constant_values=1)
        
        # Create the plot
        fig = plt.figure()
        ax= fig.gca()
        ax.imshow(padded_canvas, cmap='gray')
        ax.axis('off')
        plt.show(block=False)
        plt.pause(10)
        plt.close()
        
        i = 1
        back = False
        while True: 
            thresh= 5
            if back:
                i+=1  
            else:
                i-=1
                
            
            if i >= thresh:
                back = False
            if i <=0:
                back = True
            #time.sleep(0.05)
            print((i)*' '+'get back to work dude!!!')     


 
#easter_egg()
 
# # create a thread
# thread1 = Thread(target=task1)
# # run the thread
# thread1.start()
# # wait for the thread to finish
# print('Waiting for the thread...')
# thread1.join()


# # create a thread
# thread2 = Thread(target=task2)
# # run the thread
# thread2.start()
# # wait for the thread to finish
# print('Waiting for the thread...')
# thread2.join()


