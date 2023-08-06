# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 21:30:59 2022

@author: anba
"""

import struct, os, datetime, numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from scipy import ndimage
from processing_tools import processing_tools as ptools 
# import os
# import datetime
# import numpy as np


# import scipy as sp
# import scipy.ndimage as ndimage
# import matplotlib as mpl
# import matplotlib.pyplot as plt
# import cmocean 

#%%######################  Convenience functions ##############################
########## Function to print progress bar in terminal window ##################
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
        
#%%########### functions to read and write binary data ##########################
def _NextBigEndianUnsignedShort(file,n,decode):
    global n_bytes_read,checksum
    """
    Read the next big endian unsigned short

    Args:
        file: file to write to (Buffered Reader)
        n: number of bytes to unpack (int)
        decode: Boolean flag whether to return decoded int (True) or raw bytes (False) 
    Returns:
        value: parsed integer data (int)

    """           
    raw_bytes = file.read(n)
    n_bytes_read += n
    checksum.append(raw_bytes) 
    
    if n > 1:
        fmtstr = f'>{int(n/2)}H' #byte format string for big-endian unsigned short
        out = struct.unpack(fmtstr,raw_bytes)
    else:
        out = raw_bytes
        
    #out = int(bytearray(raw_bytes).hex(),base = 16)
    if decode:    
        return out
    else:
        return raw_bytes
    
    
def _NextLittleEndianUnsignedShort(file,n,decode):
    global n_bytes_read,checksum
    """
    Read the next little endian unsigned short

    Args:
        file: file to write to (Buffered Reader)
        n: number of bytes to unpack (int)
        decode: Boolean flag whether to return decoded int (True) or raw bytes (False) 
    Returns:
        value: parsed integer data (int)

    """           
    raw_bytes = file.read(n)
    n_bytes_read += n
    checksum.append(raw_bytes) 
    
    if n > 1:
        fmtstr = f'<{int(n/2)}H' #byte format string for little-endian unsigned short
        out = struct.unpack(fmtstr,raw_bytes)
    else:
        out = raw_bytes
        
    if decode:    
        return out[0]
    else:
        return raw_bytes

def _NextLittleEndianSignedShort(file,n,decode):
    global n_bytes_read,checksum
    """
    Read the next little endian unsigned short

    Args:
        file: file to write to (Buffered Reader)
        n: number of bytes to unpack (int)
        decode: Boolean flag whether to return decoded int (True) or raw bytes (False) 
        
    Returns:
        value: parsed integer data (int)

    """           
    raw_bytes = file.read(n)
    n_bytes_read += n
    checksum.append(raw_bytes) 
    
    if n > 1:
        fmtstr = f'<{int(n/2)}h' #byte format string for little-endian signed short
        out = struct.unpack(fmtstr,raw_bytes)
    else:
        out = raw_bytes
        
    if decode:    
        return out[0]
    else:
        return raw_bytes
    
#function to convert a byte to a binary bit string     
def get_LE_bit_string(byte): 
    """
    make a bit string from little endian byte
    
    Args:
        byte: a byte
    Returns:
        a string of ones and zeros, the bits in the byte
    """
    # surely there's a better way to do this!!
    bits = ""
    for i in [7, 6, 5, 4, 3, 2, 1, 0]:  # Little Endian
        if (byte >> i) & 1:
            bits += "1"
        else:
            bits += "0"
    return bits

def _WriteLittleEndianUnsignedShort(file,val,n, decoded):
    global n_bytes_written,checksum
    """
    Write little endian unsigned short to file. Update global checksum and byte count.

    Args:
        file: file to write to (Buffered Reader)
        val: value to write (int)
        n: number of bytes to pack (int)
        decoded: Boolean indicating whether the variable was decoded to int (True) or left in byte form (False)
    
    """       
    if decoded:   
        write_bytes = val.to_bytes(n, byteorder='little')
    else:
        write_bytes = val
        
    n_bytes_written += n    
    checksum.append(write_bytes)  
    file.write(write_bytes)
 
def _WriteLittleEndianSignedShort(file,val,n,decoded):
    global n_bytes_written,checksum
    """
    Write little endian signed short to file. Update global checksum and byte count.

    Args:
        file: file to write to (Buffered Reader)
        val: value to write (int)
        n: number of bytes to pack (int)
        decoded: Boolean indicating whether the variable was decoded to int (True) or left in byte form (False)
    """       
    if decoded:   
        fmtstr = f'<{int(n/2)}h' #byte format string for little-endian signed short
        write_bytes = struct.pack(fmtstr,val)
    else:
        write_bytes = val
    

    n_bytes_written += n    
    checksum.append(write_bytes)  
    file.write(write_bytes)
################## Functions to parse ADCP config parameters ##################
#function to parse system config parameters from 2-byte hex
def parse_system_configuration(syscfg):
    """
    determine the system configuration parameters from 2-byte hex
    
    Args:
        syscfg: 2-byte hex string 
    Returns:
        dictionary of system configuration parameters
    """    

    LSB = get_LE_bit_string(syscfg[0])
    MSB = get_LE_bit_string(syscfg[1])
    
    ## determine system configuration
    #key for Beam facing
    beam_facing = {'0':'DOWN',
                '1':'UP'}
    
    #key for XDCR attached
    xdcr_att = {'0':'NOT ATTACHED',
                '1':'ATTACHED'}
    
    # key for sensor configuration
    sensor_cfg = {'00':'#1',
                  '01':'#2',
                  '10':'#3'}
    
    # key for beam pattern
    beam_pat = {'0':'CONCAVE',
                '1':'CONVEX'}
    
    # key for system frequencies
    sys_freq = {'000':'75-kHz',
                '001':'150-kHz',
                '010':'300-kHz',
                '011':'600-kHz',
                '100':'1200-kHz',
                '101':'2400-kHz',} 
    
    ## determine system configuration from MSB
    janus = {'0100':'4-BM',
            '0101': '5-BM (DEMOD)',
            '1111': '5-BM (2 DEMD)'}
    
    beam_angle = {'00': '15E',
                 '01': '20E',
                 '10': '30E',
                 '11': 'OTHER'}
    
    system_configuration = {}
    system_configuration['BEAM FACING']  = beam_facing[LSB[0]]
    system_configuration['XDCR HD']      = xdcr_att[LSB[1]]
    system_configuration['SENSOR CONFIG']= sensor_cfg[LSB[2:4]]
    system_configuration['BEAM PATTERN'] = beam_pat[LSB[4]]
    system_configuration['FREQUENCY']    = sys_freq[LSB[5:]]
    try:
        system_configuration['JANUS CONFIG'] = janus[MSB[:4]]
    except: system_configuration['JANUS CONFIG'] = 'UNKNOWN'
    
    system_configuration['BEAM ANGLE']   = beam_angle[MSB[-2:]]

    return system_configuration   


def parse_EX_command(ex):
    """
    determine the coordinate transformation processing parameters (EX command). parameters from 1-byte hex
    
    Args:
        ex: 1-byte hex string 
    Returns:
        string - coordinate transformation processing parameter 
    """      

    LSB = get_LE_bit_string(ex[0])
    
    coord_sys = {'00': 'BEAM COORDINATES',
                 '01': 'INSTRUMENT COORDINATES',
                 '10': 'SHIP COORDINATES',
                 '11': 'EARTH COORDINATES'}    
    
    coord_system= coord_sys[LSB[3:5]]
    
    return coord_system

def skip_to_next_header(f):
    """
    Skip to the next header (b'\x7f\x7f') in the file. 


    Parameters
    ----------
    f : _io.BufferedReader
    

    Returns
    -------
    None.

    """
    start_byte = f.tell() # byte of current read position in file
    
    
    while True:
        start_byte+=1
        
        b1 = f.read(1) 
        b2 = f.read(1)
        
        #print([b1,b2])
        if b1 == b'\x7f' and b2 == b'\x7f':
            break
        elif b1 == b'' and b2 == b'': # cast to catch end of file
            #print('broke')
            break
        else:
            f.seek(start_byte-1)
    
    f.seek(max(start_byte-2,0))
           
    check = f.read(2) 
    #print(check)  
        
    if check == b'\x7f\x7f':
        
        f.seek(max(start_byte-2,0))
    else:
        f.seek(max(start_byte-1,0))
        
    

############## function to read a TRDI Workhorse ADCP ensemble ################
def read_next_ensemble(file):
    """
    Read the next ensemble from the .000 file

    Args:
        file: file to write to (Buffered Reader)
        
    Returns:
        n_bytes_read: number of bytes read from the file (int)
        ensemble: dictionary containing parsed ensemble data
    """               
    global n_bytes_read,checksum, ensemble_header, fixed_leader
    checksum= []
    n_bytes_read = 0
    
    ensemble_start_byte = file.tell() # absolute byte position of the ensemble in the file
    
    # decode the ensemble header 
    ensemble_header = {}
    for field in ensemble_header_fields:
        ensemble_header[field[0]] = _NextLittleEndianUnsignedShort(file,field[1],decode = field[3])

    ensemble_header['ADDRESS OFFSETS'] = []
    for n in range(ensemble_header['N DATA TYPES']):
        ensemble_header['ADDRESS OFFSETS'].append(_NextLittleEndianUnsignedShort(file,2,decode = True)) 
    
    # Decode the fixed leader (data type 1)
    fixed_leader = {}
    for field in fixed_leader_fields:
        
        if field[2] =='Little Endian':
            fixed_leader[field[0]] = _NextLittleEndianUnsignedShort(file,field[1],decode = field[3])
            
        elif field[2] =='Big Endian':
            fixed_leader[field[0]] = _NextBigEndianUnsignedShort(file,field[1],decode = field[3])
    
    # Decode the variable leader (data type 2)

    #MISTAKE NEAR HERE SOMEWHERE
    ## skip to variable leader header 
    file.seek(ensemble_start_byte+ensemble_header['ADDRESS OFFSETS'][1])
    
    # print(file.tell())
    # file.seek(file.tell()-50) #back up file read position by arbitraty offset 


    
    # start_byte = file.tell() # byte of current read position in file
    # n = 0

    # loop= True
    # while loop:
    #     n+=1
    #     start_byte+=1
        
    #     b1 = file.read(1) 
    #     b2 = file.read(1)
        
    #     #print([b1,b2])
    #     if b1 == b'\x80' and b2 == b'\x00': 
    #         loop= False
    #     else:
    #         file.seek(start_byte-1)
            
    # file.seek(max(start_byte-2,0))
    
    # print(file.tell())
    
    # file.seek(ensemble_header['ADDRESS OFFSETS'][1])
    # print(_NextBigEndianUnsignedShort(file, n=1, decode=True))
    # print(_NextBigEndianUnsignedShort(file, n=1, decode=True))
    # print(_NextBigEndianUnsignedShort(file, n=1, decode=True))
    # print(_NextBigEndianUnsignedShort(file, n=1, decode=True))
    # print(_NextBigEndianUnsignedShort(file, n=1, decode=True))
    # print(_NextBigEndianUnsignedShort(file, n=1, decode=True))
    # print(_NextBigEndianUnsignedShort(file, n=1, decode=True))
    # print(_NextBigEndianUnsignedShort(file, n=1, decode=True))
    
    
    # for i in range(50):
    #     print(_NextBigEndianUnsignedShort(file, n=1, decode=True))
    
    
    
    ## jump to variable leader position
    # print(file.tell())
    #file.seek(ensemble_header['ADDRESS OFFSETS'][2])
    
    #for i in range(7):
    # print(_NextBigEndianUnsignedShort(file, n=2, decode=True))    
    # print(_NextBigEndianUnsignedShort(file, n=2, decode=True))  
    
    # print(file.tell())
    global variable_leader
    variable_leader = {}
    for field in variable_leader_fields:
        variable_leader[field[0]] = _NextLittleEndianUnsignedShort(file,field[1],decode = field[3])
    
    
    file.seek(ensemble_start_byte+ensemble_header['ADDRESS OFFSETS'][2])
    ## Parse data type 3 (velocity)
    ensemble_header['VELOCITY ID'] = _NextLittleEndianUnsignedShort(file,2,decode = True)
    
    #print(ensemble_header['VELOCITY ID'])
    
    velocity_data = []
    for cell in range(fixed_leader['NUMBER OF CELLS {WN}']):
        cell_data = []
        for beam in range(fixed_leader['NUMBER OF BEAMS']):
            cell_data.append( _NextLittleEndianSignedShort(file,2,decode = True))
        velocity_data.append(cell_data)
        
    ## Parse data type 4 (correlation Magnitude)
    ensemble_header['ID CODE 4'] = _NextLittleEndianUnsignedShort(file,2, decode = True)
    corr_mag_data = []
    for cell in range(fixed_leader['NUMBER OF CELLS {WN}']):
        cell_data = []
        for beam in range(fixed_leader['NUMBER OF BEAMS']):
            cell_data.append(_NextLittleEndianUnsignedShort(file,1,decode = field[3]))
        # cell_data.append(np.mean(cell_data))
        corr_mag_data.append(cell_data)
    
    ## Parse data type 5 (echo intensity)
    ensemble_header['ID CODE 5'] = _NextLittleEndianUnsignedShort(file,2,decode = True)
    echo_intensity_data = []
    for cell in range(fixed_leader['NUMBER OF CELLS {WN}']):
        cell_data = []
        for beam in range(fixed_leader['NUMBER OF BEAMS']):
            cell_data.append(_NextLittleEndianUnsignedShort(file,1,decode = field[3]))
        echo_intensity_data.append(cell_data)    
    
    ## Parse data type 6 (percent good)
    ensemble_header['ID CODE 6'] = _NextLittleEndianUnsignedShort(file,2, decode = True)
    pct_good_data = []
    for cell in range(fixed_leader['NUMBER OF CELLS {WN}']):
        cell_data = []
        for beam in range(fixed_leader['NUMBER OF BEAMS']):
            cell_data.append(_NextLittleEndianUnsignedShort(file,1,decode = field[3]))
        pct_good_data.append(cell_data)      
      
        
    # read bottom track data, if recorded
    if ensemble_header['N DATA TYPES'] ==7:
        bottom_track = {}
        for field in bottom_track_fields:  
            bottom_track[field[0]] = _NextLittleEndianUnsignedShort(file,field[1],decode = field[3]) 
    else: bottom_track = None   
    
    #read reserved bit data 
    ensemble_header['RESERVED BIT DATA'] = _NextLittleEndianUnsignedShort(file,2,decode = True)
    
    # read end of ensemble checksum 
    file_checksum = struct.unpack('<H',file.read(2))[0] #chacksum to verify
    n_bytes_read +=2
    
    if sum(bytearray(b''.join(checksum))) - file_checksum != 0:
        
        byte_deficit = sum(bytearray(b''.join(checksum))) - file_checksum
        #Warning('FAILED CHECKSUM')
        #print(f'CHECKSUM FAILED {n_bytes_read}')
        
    ## get system configuration parameters 
    
    global system_configuration
    try:
        system_configuration = parse_system_configuration(fixed_leader['SYSTEM CONFIGURATION'])  
    except: 
        system_configuration = None
        
    coord_sys = parse_EX_command(fixed_leader['COORDINATE TRANSFORM {EX}'])
        
    
    ## package ensemble data into a dictionary 
    ensemble = { 'ENSEMBLE HEADER':ensemble_header,
                  'FIXED LEADER': fixed_leader,
                  'VARIABLE LEADER': variable_leader,
                  'VELOCITY': velocity_data,
                  'CORRELATION MAGNITUDE': corr_mag_data,
                  'ECHO INTENSITY':echo_intensity_data,
                  'PERCENT GOOD':pct_good_data,
                  'BOTTOM TRACK':bottom_track,
                  'CHECKSUM':{'FILE':file_checksum,'PARSED':checksum},
                  'SYSTEM CONFIGURATION':system_configuration,
                  'COORDINATE SYSTEM': coord_sys}    
    
    # # ## package ensemble data into a dictionary 
    # ensemble = { 'ENSEMBLE HEADER':ensemble_header,
    #               'FIXED LEADER': fixed_leader,
    #               'VARIABLE LEADER': variable_leader,
    #               'VELOCITY': velocity_data}    
       
    
    
    #print([ensemble['ENSEMBLE HEADER']['N BYTES IN ENSEMBLE'],f.tell()])
    #print(ensemble['ENSEMBLE HEADER']['N BYTES IN ENSEMBLE'] - f.tell())
    
    #print(ensemble['ENSEMBLE HEADER']['N BYTES IN ENSEMBLE'])
    
    # rel_file_pos = file.tell()% ensemble['ENSEMBLE HEADER']['N BYTES IN ENSEMBLE']
    # #print(rel_file_pos)
    
    # bytes_to_skip = ensemble['ENSEMBLE HEADER']['N BYTES IN ENSEMBLE'] + 2 - rel_file_pos
    
    # #print(bytes_to_skip)
    # file.seek(file.tell() + bytes_to_skip )
    
    #print(checksum)
    #print(file.tell())
    
    #print(file.read(2))
    #skip_to_next_header(raw_file)
    
    return n_bytes_read,ensemble  
    


############## Shell for reading all ensembles in a PD0 file ##################
def read_all_ensembles(filepath,print_progress = True):
    
    """ 
        Successively read read all ensembles in the .000 file. 
        
        Args: 
            filepath: full path to the .000 file (string)
        
        Return: 
            
    """
    global filesize, total_bytes_read,ensemble
    
    filename = filepath.split(os.sep)[-1]
    raw_file = open(filepath,"rb")

    # skip to the header for the first ensemble 
    skip_to_next_header(raw_file)
    
    n_ensembles = 0 # number of ensembles in the file
    ensemble_data = [] # list storing data for each ensemble 
    filesize = os.path.getsize(filepath) # size of input file in bytes
    total_bytes_read = 0 #total number of bytes alread read
    
    
    if  print_progress:
        printProgressBar(total_bytes_read, filesize,taskname = f'Parsing {filename}', prefix= f'Progress  {round(100*total_bytes_read/filesize,0)}%')
    
    
    while True:  
        try:
            
            bytes_read,ensemble = read_next_ensemble(raw_file)
            #skip_to_next_header(raw_file) # skip to next header
            
            total_bytes_read += bytes_read
            ensemble_data.append(ensemble)
            n_ensembles +=1
            
            if print_progress:
                printProgressBar(total_bytes_read, filesize,taskname = f'Parsing {filename}',prefix= f'Progress  {round(100*total_bytes_read/filesize,0)}%') 

        except:
            raw_file.close()
            break     
        
    return ensemble_data, filesize     

def read_all_ensembles_averaged(filepath,averaging_interval,print_progress = True):
    """
    Successively read read all ensembles in the .000 file, taking the average of 
    every intermediate (averaving_interval) ensembles. 

    Parameters
    ----------
    filepath : string
        path to the .000 file
    averaging_interval : int
        number of intermediate ensembles to average

    Returns
    -------
    ensemble_data : list of dictionaries
        list of dictionaries containing data for each avearged ensemble
    filesize : int
        number of bytes in the .000 file that was read

    """
    global filesize, total_bytes_read,ensemble_data
    
    filename = filepath.split(os.sep)[-1]
    raw_file = open(filepath,"rb")
    
    # skip to the header for the first ensemble 
    skip_to_next_header(raw_file)

    
    n_ensembles = 0 # number of ensembles in the file
    ensemble_data = [] # list storing data for each ensemble 
    filesize = os.path.getsize(filepath) # size of input file in bytes
    total_bytes_read = 0 #total number of bytes alread read
    
    if print_progress: printProgressBar(total_bytes_read, filesize,taskname = f'Parsing {filename} (Averaged)', prefix= f'Progress  {round(100*total_bytes_read/filesize,0)}%')
    
    #averaging_interval = 60 # number of ensembles to include in each average 
    #print(filesize)
    
    temp_ensemble_data = [] #list to hold ensembles before they are averaged. 
    while True:   
        try:
            
            bytes_read,ensemble = read_next_ensemble(raw_file)
            #skip_to_next_header(raw_file) # skip to next header
            
            total_bytes_read += bytes_read
            temp_ensemble_data.append(ensemble)
            #print(bytes_read)
            
            
            if n_ensembles%averaging_interval == averaging_interval-1:
                ensemble_data.append(average_ensembles(temp_ensemble_data))
                temp_ensemble_data = []
                
            n_ensembles +=1
            # print(n_ensembles)
            # if n_ensembles>1000:
            #     break
            if print_progress: printProgressBar(total_bytes_read, filesize,taskname = f'Parsing {filename}',prefix= f'Progress  {round(100*total_bytes_read/filesize,0)}%') 
        except:
            #ensemble_data.append(average_ensembles(temp_ensemble_data))
            raw_file.close()
            break
            
            #break  
    return ensemble_data, filesize 

#%%




def average_ensembles(ensembles_to_average):
    """
    Average 'ECHO INTENSITY','CORRELATION MAGNITUDE','VELOCITY', and 
    'PERCENT GOOD' from a list of ensembles and return a single ensemble 

    Parameters
    ----------
    ensembles_to_average : list of dictionaries
        List of dictionaries containing ensemble data

    Returns
    -------
    averaged_ensembles : dictionary
        Dictionary of averaged ensemble data

    """
    fields_to_average = ['ECHO INTENSITY','CORRELATION MAGNITUDE','VELOCITY','PERCENT GOOD']
    averaged_ensembles = ensembles_to_average[0].copy()
    averaged_ensembles['AVERAGED ENSEMBLE NUMBERS'] = [e['VARIABLE LEADER']['ENSEMBLE NUMBER'] for e in ensembles_to_average]
    ensemble_numbers = []
    n_ensembles_to_average = len(ensembles_to_average)
    ensembles_to_average = ensembles_to_average.copy() # copy the input dictionary
    for field in fields_to_average:
        
        field_values = [[] for i in range(n_ensembles_to_average)]
        for e,ensemble in enumerate(ensembles_to_average):
            for item in ensemble[field]:
                for i in range(len(item)):
                    if item[i] == -32768:
                        item[i] = np.nan
                        
                field_values[e].append(item)
        
        
        #field_values[field_values == -32768] = np.nan
        
        #print(int(np.nanmean(field_values,axis = 0).tolist()))
        
        
        avgd_data = np.nanmean(field_values,axis = 0).tolist()
        for i in range(len(avgd_data)):
            
            
            for j in range(len(avgd_data[i])):
                
                try: 
                    avgd_data[i][j] = int(avgd_data[i][j])
                
                except:
                    avgd_data[i][j] = -32768
            # try:
            #     avgd_data[i][j] = 
            # except: None
                
        averaged_ensembles[field] = avgd_data
        
    return averaged_ensembles

###################### Function to write and ensemble #########################
def write_ensemble(file,ensemble,data_type_5 = 'ECHO INTENSITY'):
    global n_bytes_written, checksum 
    n_bytes_written = 0
    checksum = []
    
    fields = []
    # # write the ensemble header 
    for field in ensemble_header_fields:
        fields.append(field[0])
        _WriteLittleEndianUnsignedShort(file, ensemble['ENSEMBLE HEADER'][field[0]], field[1], decoded = field[3])
        
    for n in range(ensemble['ENSEMBLE HEADER']['N DATA TYPES']):
        fields.append('ADDRESS OFFSET')
        _WriteLittleEndianUnsignedShort(file,ensemble['ENSEMBLE HEADER']['ADDRESS OFFSETS'][n],2, decoded = field[3])
    
        
    #Write the fixed leader (data type 1)
    for field in fixed_leader_fields:
        fields.append(field[0])
        _WriteLittleEndianUnsignedShort(file,ensemble['FIXED LEADER'][field[0]],field[1], decoded = field[3])
        
    for field in variable_leader_fields:
        fields.append(field[0])
        _WriteLittleEndianUnsignedShort(file,ensemble['VARIABLE LEADER'][field[0]],field[1], decoded = field[3])
           
        
    ## Write data type 3 (velocity)
    _WriteLittleEndianUnsignedShort(file,ensemble['ENSEMBLE HEADER']['VELOCITY ID'],2,decoded = True)
    for cell in range(ensemble['FIXED LEADER']['NUMBER OF CELLS {WN}']):
        cell_data = []
        for beam in range(ensemble['FIXED LEADER']['NUMBER OF BEAMS']):
            _WriteLittleEndianSignedShort(file,ensemble['VELOCITY'][cell][beam],2,decoded = True)
    
    ## Write data type 4 (correlation Magnitude)
    _WriteLittleEndianUnsignedShort(file,ensemble['ENSEMBLE HEADER']['ID CODE 4'],2,decoded = True)
    for cell in range(ensemble['FIXED LEADER']['NUMBER OF CELLS {WN}']):
        cell_data = []
        for beam in range(ensemble['FIXED LEADER']['NUMBER OF BEAMS']):
            _WriteLittleEndianUnsignedShort(file,ensemble['CORRELATION MAGNITUDE'][cell][beam],1,decoded = True)
            
    ## Write data type 5 (echo intensity)
    _WriteLittleEndianUnsignedShort(file,ensemble['ENSEMBLE HEADER']['ID CODE 5'],2,decoded = True)
    for cell in range(ensemble['FIXED LEADER']['NUMBER OF CELLS {WN}']):
        cell_data = []
        for beam in range(ensemble['FIXED LEADER']['NUMBER OF BEAMS']):
            _WriteLittleEndianUnsignedShort(file,ensemble[data_type_5][cell][beam],1,decoded = True)
    
    ## Write data type 6 (percent good)
    _WriteLittleEndianUnsignedShort(file,ensemble['ENSEMBLE HEADER']['ID CODE 6'],2,decoded = True)
    for cell in range(ensemble['FIXED LEADER']['NUMBER OF CELLS {WN}']):
        cell_data = []
        for beam in range(ensemble['FIXED LEADER']['NUMBER OF BEAMS']):
            _WriteLittleEndianUnsignedShort(file,ensemble['PERCENT GOOD'][cell][beam],1,decoded = True)     
      
        
    # read bottom track data, if recorded
    if ensemble['BOTTOM TRACK']:
        if ensemble['ENSEMBLE HEADER']['N DATA TYPES'] ==7:
            for field in bottom_track_fields:  
                _WriteLittleEndianUnsignedShort(file,ensemble['BOTTOM TRACK'][field[0]],field[1],decoded = field[3]) 
        
    
    #write reserved bit data 
    _WriteLittleEndianUnsignedShort(file,ensemble['ENSEMBLE HEADER']['RESERVED BIT DATA'],2,decoded = True)
    
    # write end of ensemble checksum 
    _WriteLittleEndianUnsignedShort(file,sum(bytearray(b''.join(checksum)))%65536,2,decoded = True) #chacksum to verify
    
    
    
    
    
###################### Postprocessing Functions ###############################
def filter_echo_intensity_array(ensemble_array):
    """
    Generate numpy array of filterd Echo Intensity Data (remove HAIN DVL interference)
        -Two passes of column-wise spike filter, filling nan values inbetween passes by averaging neighbors.
        -Final gaussing smoothing step
    Args:
        ensemble_array: numpy array of echo intensity data with dimensions (nbins,n_ensembles)
    Returns:
        numpy array with dimensions (nbins,n_ensembles)  

    """   
    X = ensemble_array      
    
    def filt(X):
        """
        column-wise spike filter - removes data with a LHS differential exceeding 0.5
        filtered values replaced by nan values. 
        
        Args:
            X: numpy array of echo intensity data with dimensions (nbins,n_ensembles)
        Returns:
            X_new: numpy array with dimensions (nbins,n_ensembles)  
            X_filt: filter mask 
        """
        X_norm = X - np.nanmin(X)
        X_norm = X_norm/np.nanmax(X_norm)
        
        X_dx = np.diff(X_norm,axis = 1) # difference across rows(up/down)
        X_dy = np.diff(X_norm,axis = 0) # difference across columns(left/right)
        
        X_new =X[:,1:].copy()
        X_filt = X_dx 
        X_new[X_filt>0.05] = np.nan
        return X_new,X_filt
    
    def fill_nan(X):
        """
        fill nan values as the average of the all neighboring non-nan values
       
        Args: 
            numpy array of echo intensity data with dimensions (nbins,n_ensembles)
           
        Returns:
            numpy array with dimensions (nbins,n_ensembles)  
        """        
        Xout = X.copy()
        nrow = np.shape(Xout)[0]
        ncol = np.shape(Xout)[1]
        for row in np.arange(0,nrow):
            for col in np.arange(0,ncol):
                curr_val = Xout[row,col]
                if np.isnan(curr_val): 
                    
                    values = []
                    
                    try: values.append(Xout[row-1,col])
                    except: None
                    
                    try:values.append(Xout[row+1,col])
                    except:None
                        
                    try:values.append(Xout[row,col-1])
                    except:None
        
                    try:values.append(Xout[row,col+1])
                    except: None              
        
        
                    if values: Xout[row,col] = np.nanmean(values)
                    else:
                        try:
                            chunk = Xout[row-2:row+2,col-2:col+2]
                            Xout[row,col] = np.nanmean(chunk)
                        except: None
        return Xout  

    X_new,X_filt1 = filt(X) # first pass spike filter
    X_new  = fill_nan(X_new) # fill nan values after first pass
    X_new,X_filt2 = filt(X_new) # second pass of spike filter
    X_new  = fill_nan(X_new)
    X_new = ndimage.gaussian_filter(X_new, sigma=0.25)
    
    #Append first two columns back into data (these were lost during the two passes of spike filter)
    Xout = X.copy()
    Xout[:,2:] = X_new
    
    return Xout

##  Function read RSSI parameters from a PT3 test file
def read_PT3(path):
    """
    Read the High Gain RSSI parameters from a TRDI PT3 calibration test file

    Parameters
    ----------
    path : string
        path to the .txt file containing PT3 test data

    Returns
    -------
    k_c : dict
        dictionary containign the parsed RSSI parameters for each beam 

    """
    file = open(path,'r')
    for i,line in enumerate(file.readlines()):
        L = [i for i in line.split(' ') if i]
    
        if ' '.join(L[:3]) == 'High Gain RSSI:':
            k_c = { 1: float(L[3])/100,# beam 1
                    2: float(L[4])/100,# beam 2
                    3: float(L[5])/100,# beam3
                    4: float(L[6].replace('\n',''))/100}# beam4
            
    file.close()
    return k_c


def rotate(X,theta):
    '''
    Rotates an array of vectors by theta degrees clockwise
    
    Parameters
    ----------
    X : numpy array
        2xn array containing u and v velocity vectors
    theta : rotation angle 
        number of degrees to rotate the vectors.

    Returns
    -------
    2xn numpy array with rotated vectors

    '''
    
    theta = theta*np.pi/180
    R = np.array([[np.cos(theta),-np.sin(theta)],[np.sin(theta),np.cos(theta)]])
    return np.dot(R,X)


def map_unsigned_2byte_integers_to_range(x,minval,maxval, lsd = None):
    """
    Function for converting 2-byte unsigned integers to the a specified range. 
    It is assumed that input values in x are spanned by [0,65535]. The list 
    will be mapped such that 0 is taken to minval, and 65535 is taken to maxval.

    Parameters
    ----------
    x : list or list-like
        values to scale
    maxval : float
        maximum value in scaled range.
    minval : TYPE
        maximum value for scale range.
    lsd : int (optional)
        If supplied, the scaled list will be rounded to the specified least significant digit place (e.g., 0 = 1, 1 = 0.1, 2 = 0.01). 

    Returns
    -------
    x_scl : list or list-like (same as input)
        scaled list of values with range [minval,maxval] 

    """
    
    
    x_scl = (x/65535)*(maxval - minval) + minval
    #scaled = ((x- min(x))/(max(x) - min(x)))*(maxval - minval) + minval
    
    if lsd: 
        x_scl = np.round(x_scl,lsd)
    return x_scl

#%%#####################  formatting information for pd0 fields ###############
 
## fields to parse (NAME, NUMBER OF BYTES TO READ, BYTE CONVENTION, DECODE)
ensemble_header_fields = [('HEADER ID',1,'Little Endian',True),
                          ('DATA SOURCE ID',1,'Little Endian',True),
                          ('N BYTES IN ENSEMBLE',2,'Little Endian',True),
                          ('SPARE',1,'Little Endian',True),
                          ('N DATA TYPES',1,'Little Endian',True)]

fixed_leader_fields = [('FIXED LEADER ID',2,'Little Endian',True),
                       ('CPU F/W VER.',1,'Little Endian',True),
                       ('CPU F/W REV.',1,'Little Endian',True),
                       ('SYSTEM CONFIGURATION',2,'Little Endian',False),
                       ('REAL/SIM FLAG',1,'Little Endian',True),
                       ('LAG LENGTH',1,'Little Endian',True),
                       ('NUMBER OF BEAMS',1,'Little Endian',True),
                       ('NUMBER OF CELLS {WN}',1,'Little Endian',True),
                       ('PINGS PER ENSEMBLE {WP}',2,'Little Endian',True),
                       ('DEPTH CELL LENGTH {WS}',2,'Little Endian',True),
                       ('BLANK AFTER TRANSMIT {WF}',2,'Little Endian',True),
                       ('PROFILING MODE {WM}',1,'Little Endian',True),
                       ('LOW CORR THRESH {WC}',1,'Little Endian',True),
                       ('NO. CODE REPS',1,'Little Endian',True),
                       ('%GD MINIMUM {WG}',1,'Little Endian',True),
                       ('ERROR VELOCITY MAXIMUM {WE}',2,'Little Endian',True),
                       ('TPP MINUTES',1,'Little Endian',True),
                       ('TPP SECONDS',1,'Little Endian',True),
                       ('TPP HUNDREDTHS {TP}',1,'Little Endian',True),
                       ('COORDINATE TRANSFORM {EX}',1,'Little Endian',False),
                       ('HEADING ALIGNMENT {EA}',2,'Little Endian',True),
                       ('HEADING BIAS {EB}',2,'Little Endian',True),
                       ('SENSOR SOURCE {EZ}',1,'Little Endian',True),
                       ('SENSORS AVAILABLE',1,'Little Endian',True),
                       ('BIN 1 DISTANCE',2,'Little Endian',True),
                       ('XMIT PULSE LENGTH BASED ON {WT}',2,'Little Endian',True),
                       ('(starting cell) WP REF LAYER AVERAGE {WL} (ending cell)',2,'Little Endian',True),
                       ('FALSE TARGET THRESH {WA}',1,'Little Endian',True),
                       ('SPARE1',1,'Little Endian',False),
                       ('TRANSMIT LAG DISTANCE',2,'Little Endian',True),
                       ('CPU BOARD SERIAL NUMBER',8,'Big Endian',False),
                       ('SYSTEM BANDWIDTH {WB}',2,'Little Endian',True),
                       ('SYSTEM POWER {CQ}',1,'Little Endian',True),
                       ('SPARE2',1,'Little Endian',False),
                       ('INSTRUMENT SERIAL NUMBER',4,'Little Endian',True),
                       ('BEAM ANGLE',1,'Little Endian',True)]
                       

variable_leader_fields =  [ ('VARIABLE LEADER ID',2,'Little Endian',True),
                            ('ENSEMBLE NUMBER',2,'Little Endian',True),
                            ('RTC YEAR {TS}',1,'Little Endian',True),
                            ('RTC MONTH {TS}',1,'Little Endian',True),
                            ('RTC DAY {TS}',1,'Little Endian',True),
                            ('RTC HOUR {TS}',1,'Little Endian',True),
                            ('RTC MINUTE {TS}',1,'Little Endian',True),
                            ('RTC SECOND {TS}',1,'Little Endian',True),
                            ('RTC HUNDREDTHS {TS}',1,'Little Endian',True),
                            ('ENSEMBLE # MSB',1,'Little Endian',True),
                            ('BIT RESULT',2,'Little Endian',True),
                            ('SPEED OF SOUND {EC}',2,'Little Endian',True),
                            ('DEPTH OF TRANSDUCER {ED}',2,'Little Endian',True),
                            ('HEADING {EH}',2,'Little Endian',True),
                            ('PITCH (TILT 1) {EP}',2,'Little Endian',True),
                            ('ROLL (TILT 2) {ER}',2,'Little Endian',True),
                            ('SALINITY {ES}',2,'Little Endian',True),
                            ('TEMPERATURE {ET}',2,'Little Endian',True),
                            ('MPT MINUTES',1,'Little Endian',True),
                            ('MPT SECONDS',1,'Little Endian',True),
                            ('MPT HUNDREDTHS',1,'Little Endian',True),
                            ('HDG STD DEV',1,'Little Endian',True),
                            ('PITCH STD DEV',1,'Little Endian',True),
                            ('ROLL STD DEV',1,'Little Endian',True),
                            ('ADC CHANNEL 0',1,'Little Endian',True),
                            ('ADC CHANNEL 1',1,'Little Endian',True),
                            ('ADC CHANNEL 2',1,'Little Endian',True),
                            ('ADC CHANNEL 3',1,'Little Endian',True),
                            ('ADC CHANNEL 4',1,'Little Endian',True),
                            ('ADC CHANNEL 5',1,'Little Endian',True),
                            ('ADC CHANNEL 6',1,'Little Endian',True),
                            ('ADC CHANNEL 7',1,'Little Endian',True),
                            ('ERROR STATUS WORD (ESW) {CY}',4,'Little Endian',False),
                            ('SPARE1',2,'Little Endian',False),
                            ('PRESSURE',4,'Little Endian',True),
                            ('PRESSURE SENSOR VARIANCE',4,'Little Endian',True),
                            ('SPARE2',1,'Little Endian',False),
                            ('RTC CENTURY',1,'Little Endian',True),
                            ('RTC YEAR',1,'Little Endian',True),
                            ('RTC MONTH',1,'Little Endian',True),
                            ('RTC DAY',1,'Little Endian',True),
                            ('RTC HOUR',1,'Little Endian',True),
                            ('RTC MINUTE',1,'Little Endian',True),
                            ('RTC SECOND',1,'Little Endian',True),
                            ('RTC HUNDREDTH',1,'Little Endian',True)]

bottom_track_fields = [ ('BOTTOM-TRACK ID',2,'Little Endian',True),
                        ('BT PINGS PER ENSEMBLE {BP}',2,'Little Endian',True),
                        ('BT DELAY BEFORE RE-ACQUIRE {BD}',2,'Little Endian',True),
                        ('BT CORR MAG MIN {BC}',1,'Little Endian',True),
                        ('BT EVAL AMP MIN {BA}',1,'Little Endian',True),
                        ('BT PERCENT GOOD MIN {BG}',1,'Little Endian',True),
                        ('BT MODE {BM}',1,'Little Endian',True),
                        ('BT ERR VEL MAX {BE}',2,'Little Endian',True),
                        ('Reserved',4,'Little Endian',True),
                        ('BEAM#1 BT RANGE',2,'Little Endian',True),
                        ('BEAM#2 BT RANGE',2,'Little Endian',True),
                        ('BEAM#3 BT RANGE',2,'Little Endian',True),
                        ('BEAM#4 BT RANGE',2,'Little Endian',True),
                        ('BEAM#1 BT VEL',2,'Little Endian',True),
                        ('BEAM#2 BT VEL',2,'Little Endian',True),
                        ('BEAM#3 BT VEL',2,'Little Endian',True),
                        ('BEAM#4 BT VEL',2,'Little Endian',True),
                        ('BEAM#1 BT CORR.',1,'Little Endian',True),
                        ('BEAM#2 BT CORR.',1,'Little Endian',True),
                        ('BEAM#3 BT CORR.',1,'Little Endian',True),
                        ('BEAM#4 BT CORR.',1,'Little Endian',True),
                        ('BEAM#1 EVAL AMP',1,'Little Endian',True),
                        ('BEAM#2 EVAL AMP',1,'Little Endian',True),
                        ('BEAM#3 EVAL AMP',1,'Little Endian',True),
                        ('BEAM#4 EVAL AMP',1,'Little Endian',True),
                        ('BEAM#1 BT %GOOD',1,'Little Endian',True),
                        ('BEAM#2 BT %GOOD',1,'Little Endian',True),
                        ('BEAM#3 BT %GOOD',1,'Little Endian',True),
                        ('BEAM#4 BT %GOOD',1,'Little Endian',True),
                        ('REF LAYER MIN {BL}',2,'Little Endian',True),
                        ('REF LAYER NEAR {BL}',2,'Little Endian',True),
                        ('REF LAYER FAR {BL}',2,'Little Endian',True),
                        ('BEAM#1 REF LAYER VEL',2,'Little Endian',True),
                        ('BEAM #2 REF LAYER VEL',2,'Little Endian',True),
                        ('BEAM #3 REF LAYER VEL',2,'Little Endian',True),
                        ('BEAM #4 REF LAYER VEL',2,'Little Endian',True),
                        ('BM#1 REF CORR',1,'Little Endian',True),
                        ('BM#2 REF CORR',1,'Little Endian',True),
                        ('BM#3 REF CORR',1,'Little Endian',True),
                        ('BM#4 REF CORR',1,'Little Endian',True),
                        ('BM#1 REF INT',1,'Little Endian',True),
                        ('BM#2 REF INT',1,'Little Endian',True),
                        ('BM#3 REF INT',1,'Little Endian',True),
                        ('BM#4 REF INT',1,'Little Endian',True),
                        ('BM#1 REF %GOOD',1,'Little Endian',True),
                        ('BM#2 REF %GOOD',1,'Little Endian',True),
                        ('BM#3 REF %GOOD',1,'Little Endian',True),
                        ('BM#4 REF %GOOD',1,'Little Endian',True),
                        ('BT MAX. DEPTH {BX}',2,'Little Endian',True),
                        ('BM#1 RSSI AMP',1,'Little Endian',True),
                        ('BM#2 RSSI AMP',1,'Little Endian',True),
                        ('BM#3 RSSI AMP',1,'Little Endian',True),
                        ('BM#4 RSSI AMP',1,'Little Endian',True),
                        ('GAIN',1,'Little Endian',True),
                        ('(*SEE BYTE 17)',1,'Little Endian',True),
                        ('(*SEE BYTE 19)',1,'Little Endian',True),
                        ('(*SEE BYTE 21)',1,'Little Endian',True),
                        ('(*SEE BYTE 23)',1,'Little Endian',True),
                        ('RESERVED',4,'Little Endian',True)]

###############################################################################
###############################################################################
###############################################################################
#%%
class workhorse_adcp:
    
    """Class to manage PD0 (.000) files created by Teledyne RD Instruments 
    Workhorse ADCP 

    Args:
        filepath: full path to .000 file (string)
        read_averages: if True, average imported ensembles 
        averaging_interval: number of intermediate ensembles to average
        PT3_filepath: path to PT3 test file for instrument. 
    """
    
    def __init__(self, filepath,
                 read_averages = False,
                 averaging_interval = 60,
                 PT3_filepath = None,
                 timezone_correction = 0,
                 magnetic_deviation_correction = 0,
                 instrument_depth = 0,
                 instrument_HAB = 0,
                 verbose = 1):
        
        
        ## check that filepaths exist 
        if not os.path.isfile(filepath):
            raise ValueError('Invalid pd0 filepath')
        if PT3_filepath and not os.path.isfile(PT3_filepath):
            raise ValueError('Invalid PT3 filepath')    
        
        
        
    
        st = datetime.datetime.now()
        self.filepath = filepath
        self.PT3_filepath = PT3_filepath 
        self.timezone_correction = timezone_correction
        self.magnetic_deviation_correction = magnetic_deviation_correction
        self.instrument_depth = instrument_depth
        self.instrument_HAB = instrument_HAB
        
        self.ensemble_fields = ['ECHO INTENSITY','CORRELATION MAGNITUDE','PERCENT GOOD']
        
        if verbose == 1:
            _print = True
        else:
            _print = False
            
            
        if read_averages:
            print('\n############# TRDI Workhorse ADCP PD0 File ####################\n')
            #print('Reading Averaged Ensembles')
            self.ensemble_data, self.filesize = read_all_ensembles_averaged(self.filepath, averaging_interval, print_progress = _print)
        else:
            self.ensemble_data, self.filesize = read_all_ensembles(self.filepath, print_progress = _print) # parse file
        
        
        #retrieve key configuration parameters
        self.get_key_config_parameters(print_output = _print) 

        
        if _print:
            et = datetime.datetime.now()    
            elapsed_time = et - st
            print('\nExecution time:', elapsed_time, 'seconds')
        
        

        
        
#        self.filter_echo_intensity_data()
    

            
            
   
        
    def set_timezone_correction(self,timezone_correction):
        self.timezone_correction = timezone_correction
        self.ensemble_times = self.get_ensemble_datetimes()
        
    def set_magnetic_deviation_correction(self,magnetic_deviation_correction):
        self.magnetic_deviation_correction = magnetic_deviation_correction
        
    def set_instrument_depth(self,instrument_depth):
        self.instrument_depth = instrument_depth
        
    def set_instrument_HAB(self,instrument_HAB):
        self.instrument_HAB = instrument_HAB        
    
    def get_key_config_parameters(self,print_output = False):
        """
        Generate numpy array of datetimes for ensembles. 
        Args:
            print_output: print the config parameters (default = True)
        Returns:
            dictionary containing key configuration parameters  
        """       

        
        self.n_ensembles    = len(self.ensemble_data)
        self.ensemble_times = self.get_ensemble_datetimes()
        self.n_bins         = self.ensemble_data[0]['FIXED LEADER']['NUMBER OF CELLS {WN}']
        self.bin_midpoints  = self.get_bin_midpoints()
        self.bin_size       = self.ensemble_data[0]['FIXED LEADER']['DEPTH CELL LENGTH {WS}']/100
        self.n_bins         = self.ensemble_data[0]['FIXED LEADER']['NUMBER OF CELLS {WN}']
        self.pings_per_ens  = self.ensemble_data[0]['FIXED LEADER']['PINGS PER ENSEMBLE {WP}']
        self.avg_ens_interval = np.mean(np.diff(self.ensemble_times)[1]).total_seconds()
        self.n_beams        = int(self.ensemble_data[0]['FIXED LEADER']['NUMBER OF BEAMS'])
        self.beam_facing = self.ensemble_data[0]['SYSTEM CONFIGURATION']['BEAM FACING']
        
        
        if print_output:
            
            print("\n\033[4m" + 'METADATA' + "\033[0m" )
            #print(f'   {self.filepath}')
            print(f'   File Size {self.filesize:,} bytes') 
            
            try:
                print(f'   System Frequency {self.ensemble_data[0]["SYSTEM CONFIGURATION"]["FREQUENCY"]} ') 
            except: 
                print('   System Frequency {UNABLE TO PARSE} ') 
            print(f'   1st Bin {self.bin_midpoints[0]} m, Bin Size = {self.bin_size} m')
            print(f'   No. Bins {self.n_bins}, Pings/Ens {self.pings_per_ens}')
            print(f'   BB/WH Ensemble Length {self.ensemble_data[0]["ENSEMBLE HEADER"]["N BYTES IN ENSEMBLE"]:,} bytes')
            print(f'   First Ensemble {str(self.ensemble_data[0]["VARIABLE LEADER"]["ENSEMBLE NUMBER"]).zfill(7)} {self.ensemble_times[0].strftime("%d-%B-%Y %H:%M:%S")}')
            print(f'   Last  Ensemble {str(self.ensemble_data[-1]["VARIABLE LEADER"]["ENSEMBLE NUMBER"]).zfill(7)} {self.ensemble_times[-1].strftime("%d-%B-%Y %H:%M:%S")}')
            print(f'   Average Ensemble Interval {self.avg_ens_interval} s')
            print(f'   Timezone Correction {self.timezone_correction} hours')
            print(f'   Magnetic Deviation Correction {self.magnetic_deviation_correction} degrees\n')
    
        out = {'filepath': self.filepath,
               'n_ensembles':self.n_ensembles,
               'ensemble_times': self.ensemble_times,
               'n_bins':self.n_bins,
               'bin_midpoints':self.bin_midpoints,
               'bin_size':self.bin_size,
               'pings_per_ens':self.pings_per_ens,
               'avg_ens_interval':self.avg_ens_interval,
               'n_beams': self.n_beams}
        return out
        
        
    def get_ensemble_datetimes(self):
        """
        Generate numpy array of datetimes for ensembles. 
        Args:
            None
        Returns:
            numpy array with dimensions (n_ensembles)  
        """           
        dtimes =[]
        
        
        for e,ensemble in enumerate(self.ensemble_data):
            
            # century = str(ensemble['VARIABLE LEADER']['RTC CENTURY'])
            # year = int(str(ensemble['VARIABLE LEADER']['RTC CENTURY']) + str(ensemble['VARIABLE LEADER']['RTC YEAR']))
            # month= ensemble['VARIABLE LEADER']['RTC MONTH']
            # day = ensemble['VARIABLE LEADER']['RTC DAY']
            # hour = ensemble['VARIABLE LEADER']['RTC HOUR']
            # minute = ensemble['VARIABLE LEADER']['RTC MINUTE']
            # second = ensemble['VARIABLE LEADER']['RTC SECOND']
            # hundredth = ensemble['VARIABLE LEADER']['RTC HUNDREDTH']
            
            century = str(ensemble['VARIABLE LEADER']['RTC CENTURY'])
            if century == '0': century = '20' #Catch for UNKNOWN bug that occures when parsing DVS instruments
            
            year = int(century + str(ensemble['VARIABLE LEADER']['RTC YEAR {TS}']))
            month= ensemble['VARIABLE LEADER']['RTC MONTH {TS}']
            day = ensemble['VARIABLE LEADER']['RTC DAY {TS}']
            hour = ensemble['VARIABLE LEADER']['RTC HOUR {TS}']
            minute = ensemble['VARIABLE LEADER']['RTC MINUTE {TS}']
            second = ensemble['VARIABLE LEADER']['RTC SECOND {TS}']
            hundredth = ensemble['VARIABLE LEADER']['RTC HUNDREDTHS {TS}']
            
            #print([e,ensemble['VARIABLE LEADER']['ENSEMBLE NUMBER'],year,month,day,hour])
            #dtimes.append(datetime.datetime(year,month,day,hour,minute,second,hundredth*1000))
            
            try:
                
                dtimes.append(datetime.datetime(year,month,day,hour,minute,second,hundredth*1000) + datetime.timedelta(hours = self.timezone_correction))
                
            except: 
                print([e,ensemble['VARIABLE LEADER']['ENSEMBLE NUMBER'],year,month,day,hour])
                dtimes.append(np.nan)
                
                break
                
        return dtimes        
        
    def get_bin_midpoints(self):
        """
        Generate numpy array of bin midpoint distances in meters. 
        Args:
            None
        Returns:
            numpy array with dimensions (n_ensembles)  
        """          
        bin1_dist = self.ensemble_data[0]['FIXED LEADER']['BIN 1 DISTANCE']
        bin_distance = self.ensemble_data[0]['FIXED LEADER']['DEPTH CELL LENGTH {WS}']
        bin_distances = np.linspace(bin1_dist,self.n_bins*bin_distance+bin1_dist,self.n_bins)/100
        return bin_distances 
    
    
    def get_bin_midpoints_depth(self):
        
        if self.beam_facing == 'DOWN':
            bin_midpoints_depth = self.instrument_depth + self.get_bin_midpoints() 
        elif self.beam_facing =='UP':
            bin_midpoints_depth = self.instrument_depth - self.get_bin_midpoints() 
            
        return bin_midpoints_depth
    
    def get_bin_midpoints_HAB(self):
        
        if self.beam_facing == 'DOWN':
            bin_midpoints_HAB = self.instrument_HAB - self.get_bin_midpoints()
        elif self.beam_facing =='UP':
            bin_midpoints_HAB = self.instrument_HAB + self.get_bin_midpoints()
            
        return bin_midpoints_HAB   
    
    def get_sensor_transmit_pulse_lengths(self):
        """
        Get ADCP transmit pulse lengths. Data is from the ensemble variable headers.

        Returns
        -------
        transmit_pulse_lengths : numpy array
            ADCP transmit pule lengths. One value for each ensemble.

        """
        transmit_pulse_lengths = np.empty(self.n_ensembles)
        for c,ensemble in enumerate(self.ensemble_data):
            transmit_pulse_lengths[c] = ensemble['FIXED LEADER']['XMIT PULSE LENGTH BASED ON {WT}']/100
        return transmit_pulse_lengths  
    
    def get_sensor_temperature(self):
        """
        Temperature of the water at the transducer head
        (ET-command). This value may be a manual setting or a
        reading from a temperature sensor.
        Scaling: LSD = 0.01 degree; Range = -5.00 to +40.00 degrees
        
        Returns
        -------
        temperature : numpy array
            ADCP temperature data in degrees C. One value for each ensemble.

        """
        temperature = np.empty(self.n_ensembles)
        
        for c,ensemble in enumerate(self.ensemble_data):
            temperature[c] = ensemble['VARIABLE LEADER']['TEMPERATURE {ET}']/100
        #temperature = map_unsigned_2byte_integers_to_range(temperature,-5,40,lsd = 2)
        return temperature
    
    def get_salinity(self):
        """
        Salinity value of the water at the transducer
        head (ES-command). This value may be a manual setting or
        a reading from a conductivity sensor.
        Scaling: LSD = 1 part per thousand; Range = 0 to 40 ppt
        
        Returns
        -------
        salinity : numpy array
            One value for each ensemble.

        """
        salinity = np.empty(self.n_ensembles)
        
        for c,ensemble in enumerate(self.ensemble_data):
            salinity[c] = ensemble['VARIABLE LEADER']['SALINITY {ES}']
        #salinity = map_unsigned_2byte_integers_to_range(0,40,lsd = 2)
        return salinity
    
    def get_sensor_pitch(self):
        """
        WorkHorse ADCP pitch angle (EP-command).
        This value may be a manual setting or a reading from a tilt
        sensor. Positive values mean that Beam #3 is spatially
        higher than Beam #4.
        Scaling: LSD = 0.01 degree; Range = -20.00 to +20.00 degrees
        Returns
        -------
        pitch : numpy array
            One value for each ensemble.

        """
        pitch = np.empty(self.n_ensembles)
        for c,ensemble in enumerate(self.ensemble_data):
            pitch[c] = ensemble['VARIABLE LEADER']['PITCH (TILT 1) {EP}']/100
        ## per manual - scale from -20 to 20, LSD = 0.01 (2)
        #pitch = map_unsigned_2byte_integers_to_range(pitch,-20,20,lsd = 2)
        return pitch
    
    def get_sensor_roll(self):
        """
        WorkHorse ADCP roll angle (ER-command).
        This value may be a manual setting or a reading from a tilt
        sensor. For up-facing WorkHorse ADCPs, positive values
        mean that Beam #2 is spatially higher than Beam #1. For
        down-facing WorkHorse ADCPs, positive values mean that
        Beam #1 is spatially higher than Beam #2.
        Scaling: LSD = 0.01 degree; Range = -20.00 to +20.00 degrees

        Returns
        -------
        roll : numpy array
            One value for each ensemble.

        """
        roll = np.empty(self.n_ensembles)
        for c,ensemble in enumerate(self.ensemble_data):
            roll[c] = ensemble['VARIABLE LEADER']['ROLL (TILT 2) {ER}']/100
        #roll = map_unsigned_2byte_integers_to_range(roll,-20,20,lsd = 2)
        return roll
    
    def get_sensor_heading(self):
        """
        WorkHorse ADCP heading angle (EHcommand).
        This value may be a manual setting or a reading
        from a heading sensor.
        Scaling: LSD = 0.01 degree; Range = 000.00 to 359.99 degrees
        
        Returns
        -------
        heading : numpy array
             One value for each ensemble.

        """

        heading = np.empty(self.n_ensembles)
        for c,ensemble in enumerate(self.ensemble_data):
            heading[c] = ensemble['VARIABLE LEADER']['HEADING {EH}']/100
        #heading = map_unsigned_2byte_integers_to_range(heading,0,359.99,lsd = 2)
        return heading
    
    def get_sensor_transducer_depth(self):
        """
        Depth of the transducer below the water surface
        (ED-command). This value may be a manual setting or a
        reading from a depth sensor.
        Scaling: LSD = 1 decimeter; Range = 1 to 9999 decimeters
        
        Returns
        -------
        transducer_depth : numpy array
             One value for each ensemble.

        """

        transducer_depth = np.empty(self.n_ensembles)
        for c,ensemble in enumerate(self.ensemble_data):
            transducer_depth[c] = ensemble['VARIABLE LEADER']['HEADING {EH}']
        
        transducer_depth = map_unsigned_2byte_integers_to_range(transducer_depth,0,9999,lsd = 2)
        return heading
    
    def get_velocity(self):
        """
        Retrieve velocity vectors and calculate progressive vectors in m/s. Magnetic deviation correction is applied here. 
    
        Returns
        -------
        u : numpy array
            u velocity
        v : numpy array
            v velocity
        z : numpy array
            z velocity.
        du : numpy array
            displacement in u direction.
        dv : numpy array
            displacement in v direction.
        dz : numpy array
            displacement in z direction.
        err: numpy array
            error velocity
    
        """
        
        global X,u,v
        
        
        u = np.empty((self.n_ensembles,self.n_bins))
        v = np.empty((self.n_ensembles,self.n_bins))
        z = np.empty((self.n_ensembles,self.n_bins))
        ev = np.empty((self.n_ensembles,self.n_bins))
        for e,ensemble in enumerate(self.ensemble_data):
            # cast velocity data as float
            vel_data = np.array(ensemble['VELOCITY']).astype('float')
            # mark nan values 
            vel_data[vel_data==-32768] = np.nan
            
            # convert to m/s
            vel_data = vel_data*.001


            if len(vel_data) == self.n_bins:
                u[e,:] = vel_data[:,0]
                v[e,:] = vel_data[:,1]
                z[e,:] = vel_data[:,2]
                ev[e,:] = vel_data[:,3]
            else:
                u[e,:] = np.nan
                v[e,:] = np.nan
                z[e,:] = np.nan
                ev[e,:] = np.nan
            
        # apply magnetic deviation correction
        if self.magnetic_deviation_correction!=0:
            #print(f'   Correcting for magnetic deviation ({self.magnetic_deviation_correction} degrees)')
            for b in range(self.n_bins): # loop over all bins and calculate rotated velocites for each
                X = np.array([u[:,b],v[:,b]])
                X_rot = rotate(X,theta = self.magnetic_deviation_correction)
                
                # update u and v
                u[:,b] = X_rot[0,:]
                v[:,b] = X_rot[1,:]    
                
        ## gen prog vector components 
        t = self.get_ensemble_datetimes()
        to_sec = np.vectorize(lambda x: x.seconds) # vectorized function to convert datetime delta to total seconds
        dt = np.empty(self.n_ensembles)
        dt[:-1] = to_sec(np.diff(t))
        dt[-1] = dt[-2] #assign last value
        dt = np.outer(dt,np.ones(self.n_bins))
        du = u*dt
        dv = v*dt
        dz = z*dt
        
        return u,v,z,ev     

    def get_bottom_track(self,beam_number):
        """
        

        Parameters
        ----------
        beam_number : int
            beam number to use. if zero the beam average will be returned.

        Returns
        -------
        bottom_track : numpy array
            numpy array of distance to bottom 

        """
        
        
        bottom_track = np.empty(self.n_ensembles)
        if beam_number in [0,1,2,3,4]:
            for e,ensemble in enumerate(self.ensemble_data):
                if beam_number !=0:
                    bottom_track[e] = ensemble['BOTTOM TRACK'][f'BEAM#{beam_number} BT RANGE']/100
                else: 
                    bottom_track[e] = np.mean([ensemble['BOTTOM TRACK']['BEAM#1 BT RANGE'],
                                               ensemble['BOTTOM TRACK']['BEAM#2 BT RANGE'],
                                               ensemble['BOTTOM TRACK']['BEAM#3 BT RANGE'],
                                               ensemble['BOTTOM TRACK']['BEAM#4 BT RANGE']])/100
        else: 
            ValueError('Invalid beam number. Choose integer 0 (avg),1,2,3, or 4. ')
        return bottom_track     

    
    def get_ensemble_array(self,field_name = 'ECHO INTENSITY',beam_number = 0,):
        
        """
        Format ensemble data field into a numpy array
        Args:
            field_name: ensemble data type (string). "ECHO INTENSITY" (default), "CORRELATION MAGNITUDE", "PERCENT GOOD". 
            beam_number: beam number (integer). If no beam number is provided, the beam average (beam_number = 0) will be returned. 
            
        Returns:
            numpy array with dimensions (nbins,n_ensembles)  

        """    
        #check that field name is elegible
        if not field_name in self.ensemble_fields:#["ECHO INTENSITY", "CORRELATION MAGNITUDE", "PERCENT GOOD", 'ABSOLUTE BACKSCATTER','FILTERED ECHO INTENSITY']:
            raise ValueError(f'Invalid field name. Choose one of the following [self.ensemble_fields]')

        #check that beam_number is elegible
        if not beam_number in [0,1,2,3,4]:
            raise ValueError('Invalid beam number. Choose integer 0 (avg),1,2,3, or 4. ')

               
   
        #init empty numpy array to store plotting data 
        X = np.empty((self.n_bins,self.n_ensembles))
        for c,ensemble in enumerate(self.ensemble_data):

            if beam_number!=0:
                column_data = [i[beam_number - 1] for i in ensemble[field_name]]
            else:
                column_data = [np.nanmean(i) for i in ensemble[field_name]]
                
                
            if len(column_data) == self.n_bins:
                X[:,c] = column_data
            else:
                X[:,c] = np.nan
            
        return X    
    
    
    def filter_echo_intensity_data(self):
        """
        Apply column-wise spike filter to echo intensity field of each ensemble, 
        then add to ensemble_data property of the WorkhorseADCP class 
        """
        X = np.empty((self.n_bins,self.n_ensembles,self.n_beams))
        #printProgressBar(0, self.n_beams,prefix = f'Filtering', taskname= f'Filtering 0%')
        for beam in range(self.n_beams):
            #printProgressBar(beam+1, self.n_beams,prefix = f'Filtering {round(100*(beam+1)/self.n_beams,0)}%', taskname= f'Echo Intensity BM{beam+1}')
            X[:,:,beam] = filter_echo_intensity_array(self.get_ensemble_array(field_name = 'ECHO INTENSITY', beam_number = beam+1))     
        self.append_to_ensembles(X,'FILTERED ECHO INTENSITY')
        
        
    def calculate_absolute_backscatter(self,**kwargs):
        """
        Convert numpy array of ensemble data of echo intensity to absolute backscatter then added to ensemble_data property of the WorkhorseADCP class.


        
        Optional Args:
            PT3_filepath - path to the instrument PT3 file
            field_name : ensemble data type (string). "ECHO INTENSITY" (default), "CORRELATION MAGNITUDE", "PERCENT GOOD", or others added by the "append to ensembles" method.  
        
        """
        
        
        
        if self.PT3_filepath:
            self.RSSI = read_PT3(self.PT3_filepath)
        elif kwargs.get('PT3_filepath'):
            self.RSSI = read_PT3(kwargs.get('PT3_filepath'))
        else:
            raise ValueError('PT3 File not specified. Cannot calculate absolute backscatter')
            
            
        if kwargs.get('field_name'): field_name = kwargs.get('field_name')
        else: field_name = 'ECHO INTENSITY'
        
        #self.filter_echo_intensity_data()
        #echo_intensity = self.get_ensemble_array(beam_number = 1)
        temperature = np.outer(self.get_sensor_temperature(),np.ones(self.n_bins)).T
        bin_distances = np.outer(self.get_bin_midpoints(),np.ones(self.n_ensembles))/np.cos(20*np.pi/180)#/100
        transmit_pulse_lengths = np.outer(self.get_sensor_transmit_pulse_lengths(),np.ones(self.n_bins)).T#/100
        
        
        E_r =39 #nominal value provided by ViSea
        
        ## select these based on WB commmand (0 = 25%, 1 = 6.25%)
        
        WB = self.ensemble_data[0]['FIXED LEADER']['SYSTEM BANDWIDTH {WB}']
        
        if WB==0:
            C = -139.09 #for Workhorse 600, 25% 
        else:
            C = -149.14 # for Workhorse 600, 6%
        
        

        k_c = self.RSSI
        
        
        C = -139.09 #for Workhorse 600, 25% 
       

        k_c = {1: 0.3931,# beam 1
               2: 0.4145,# beam 2
               3: 0.416,# beam3
               4: 0.4129}# beam4
    
        alpha = 0.178 
        

        if self.ensemble_data[0]["SYSTEM CONFIGURATION"]["FREQUENCY"] == '300-kHz':
            alpha = 0.068
            P_dbw = 14 #butter supply power for Workhorse 300
            print('300 kHz Unit')
        elif self.ensemble_data[0]["SYSTEM CONFIGURATION"]["FREQUENCY"] == '600-kHz':
            alpha =  0.178 #nominal ocean value for a 600 kHz unit 
            P_dbw = 9 #butter supply power for Workhorse 600
        # else:
        #     P_dbw = 9
        #     alpha = 0.068
            
            
        global StN
        
        X = np.empty((self.n_bins,self.n_ensembles,self.n_beams))
        StN = np.empty((self.n_bins,self.n_ensembles,self.n_beams))
        #printProgressBar(0, self.n_beams,prefix = f'Calculating 0%', taskname= f'Absolute Backscatter 0%')
        for beam in range(self.n_beams):
            #printProgressBar(beam+1, self.n_beams,prefix = f'Calculating {round(100*(beam+1)/self.n_beams,0)}%', taskname= f'Absolute Backscatter BM{beam+1}')
            E = self.get_ensemble_array(field_name = field_name, beam_number = beam+1)
            #E = self.get_ensemble_array(field_name = 'ECHO INTENSITY', beam_number = beam+1)
            
            
            StN[:,:,beam] = (10**(k_c[beam+1]*E/10) - 10**(k_c[beam+1]*E_r/10))/10**(k_c[beam+1]*E_r/10)
            
            X[:,:,beam] = C + 10*np.log10((temperature + 273.16)*(bin_distances**2)) - 10*np.log10(transmit_pulse_lengths) - P_dbw + 2*alpha*bin_distances + 30*np.log10(10**(k_c[beam+1]*(E - E_r)/10)-1)
        
    
        self.append_to_ensembles(X,'ABSOLUTE BACKSCATTER')
        
        self.append_to_ensembles(np.log10(StN),'SIGNAL TO NOISE RATIO')
        
        
        #return abs_bs       
        
        

       
    def append_to_ensembles(self,X,title):
        """
        Format numpy array of ensemble data into a list then add to ensemble_data property of the WorkhorseADCP class.
        Input array must have dimensions of (n_bins,n_ensemles,n_beams). In a typical use case, ensemble data is manipulated in 
        array format, then appended to the ensemble_data property and written to a PD0 file. 
        Args:
            X: numpy array with dimensions (n_bins,n_ensembles,n_beams)
            title: (string) title for the formatted data when appended to the ensemble_data property of the WorkhorseADCP class object. 
        """
        self.ensemble_fields.append(title) # update the list of ensemble field names
        for e in range(self.n_ensembles):
            ensemble_data = [] # data in the current ensemble
            for b in range(self.n_bins):
                bin_data = [] # data in the current bin
                for bm in range(self.n_beams):
                    
                    val = X[b,e,bm]
                    #bin_data.append(int(val))
                    try:
                        bin_data.append(int(val))
                    except:
                        bin_data.append(32768)
                        
                        
                ensemble_data.append(bin_data)
            self.ensemble_data[e][title] = ensemble_data  
            
# set the sensor orientation. 

    def set_sensor_orientation(self,orient_in):#orient_in = None):
        """
        Set the orientation data for the sensor. Accepts input orientation
        timeseries, and assigns instrument position based on the closest position 
        timestamp to each ensemble timestamp. All orientations are in degrees, 
        with pitch and roll ranging[-180,179.99],and heading ranging from [0,359.99] 
        
        
    
        Parameters
        ----------
        orient_in : (optional)pandas dataframe containing a timeseries of roll,pitch,heading 
                data corresponding to the orientation of the instrument. Must have 
                columns named 'pitch', 'roll' and 'heading'. Index must be a pandas 
                timestamp. If not specified, then the onboard gyroscope and compass data 
                (from the variable headers) will be used. 
    
        Returns
        -------
        None.
    
        """
        
        self.orientation = np.full((3,self.n_ensembles),np.nan)
        
        
        if type(orient_in) == type(None):
            self.orientation[0,:] = self.get_sensor_pitch()
            self.orientation[1,:] = self.get_sensor_roll()
            self.orientation[2,:] = self.get_sensor_heading()
        #if kwargs.get('orient_in'):
        else:
            et = self.ensemble_times # ensemble times
            for i,etime in enumerate(et):
                index = orient_in.index.get_indexer([etime], method='nearest')[0] # index of nearest input positon to the ensemble timestamp
          
                self.orientation[0,i] = orient_in.iloc[index].pitch
                self.orientation[1,i] = orient_in.iloc[index].roll
                self.orientation[2,i] = orient_in.iloc[index].heading 
            

        
        
        
    def set_sensor_position(self,pos_in):
        """
        Set the position data for the sensor. Accepts input position timeseries,
        and assigns instrument position based on the closest position timestamp to
        each ensemble timestamp. 
    
        Parameters
        ----------
        pos_in : pandas dataframe
            containing a timeseries of x,y,z data corresponding to the position of 
            the instrument. Must have columns named 'x', 'y' and 'z'. Index must be
            a pandas timestamp. 
            
    
        Returns
        -------
        None.
    
        """
        et = self.ensemble_times # ensemble times
        self.position  = np.full((3,self.n_ensembles),np.nan)
        for i,etime in enumerate(et):
            index = pos_in.index.get_indexer([etime], method='nearest')[0] # index of nearest input positon to the ensembel timestamp
      
            self.position[0,i] = pos_in.iloc[index].x
            self.position[1,i] = pos_in.iloc[index].y
            self.position[2,i] = pos_in.iloc[index].z     
        
                

    def set_beam_relative_geometry(self,rotation = 0,offset = (0,0,0), dr = 0.1):
        """
        Calculate the x,y,z position of each bin in each beam relative to the face 
        of the ADCP. Accounts for 20 degree beam angle in x-z and y-z planes. 
    
        Parameters
        ----------
        rotation : float
            Orientation of the ADCP. This is the number of degrees clockwise from the
            forward direction of the mounting platform. (E.g., the bow of the vessel)
            
            
            
        offset : numpy array
            numpy array containing x,y,z offsets for the instrument. This offset 
            should be the relative distance between the position measuremet
            (e.g., from the vessel GPS) and the center of the ADCP transducer face.
            
        dr : float
            radial distance from the center of the face of the ADCP to the center 
            of the transdecer faces. 
            
        Returns
        -------
        None.
    
        """
    
        # See WorkHorseCommands and Ouput Data Format page 53
        # rotation = 45
        # offset = adcp_offset
        
        # dr = 0.1 # distance from center of the unit to the center of each transducer face
        R = ptools.gen_rot_z(theta = rotation)
        
        if self.beam_facing == 'DOWN':
            self.relative_beam_origin = np.array([(dr,0,0),(-dr,0,0),(0,dr,0),(0,-dr,0)])# position of each beam relative to the center of the face of the instrument
        if self.beam_facing == 'UP':
            self.relative_beam_origin = np.array([(-dr,0,0),(dr,0,0),(0,dr,0),(0,-dr,0)])# position of each beam relative to the center of the face of the instrument
            
        self.relative_beam_origin = np.add(offset,self.relative_beam_origin)  # offset origin to be relative to the center of mass of the position measurement
        self.relative_beam_origin = self.relative_beam_origin.dot(R).T # rotate the origin points - assums that positive y direction is forward (beam 3) 
        
        
        self.relative_beam_midpoint_positions = []
        for b in range(self.n_beams):
            origin = self.relative_beam_origin[:,b]
            beam_midpoints = np.outer(origin,np.ones(self.n_bins))
            if self.beam_facing == 'DOWN':
                beam_midpoints[2] += -self.bin_midpoints
            else: 
                beam_midpoints[2] += self.bin_midpoints
            self.relative_beam_midpoint_positions.append(beam_midpoints)
        
        
        # rotate the beams
        

        theta_beam = self.ensemble_data[0]['FIXED LEADER']['BEAM ANGLE']
        
        
        Ry_cw = ptools.gen_rot_y(-theta_beam)
        Rx_cw = ptools.gen_rot_x(-theta_beam)
        Ry_ccw = ptools.gen_rot_y(theta_beam)
        Rx_ccw = ptools.gen_rot_x(theta_beam)
        self.relative_beam_midpoint_positions[0] = Rx_cw.dot(Ry_cw.dot(self.relative_beam_midpoint_positions[0]))
        self.relative_beam_midpoint_positions[1] = Rx_ccw.dot(Ry_ccw.dot(self.relative_beam_midpoint_positions[1]))
        self.relative_beam_midpoint_positions[2] = Rx_ccw.dot(Ry_cw.dot(self.relative_beam_midpoint_positions[2]))
        self.relative_beam_midpoint_positions[3] = Rx_cw.dot(Ry_ccw.dot(self.relative_beam_midpoint_positions[3]))        
        
        
    
    def write_PD0(self,filename,path = os.getcwd(),data_type_5 = 'ECHO INTENSITY'):
        """
        Write ensemble_data to binary pd0 format. 
        Args:
            filename: name of the .000 file to b0e created
            path: path to directory where .000 file will be written 
            data_type_5: (string) dictionary key of the data type to write as "data type 5" in the PD0 file. See COMMANDS AND OUTPUT DATA FORMAT pdf file for more information. 
        """        
        
        #check that data_type_5 name is elegible
        if not data_type_5 in ["ECHO INTENSITY", "CORRELATION MAGNITUDE", "PERCENT GOOD", "VELOCITY",'ABSOLUTE BACKSCATTER','FILTERED ECHO INTENSITY']:
            raise ValueError('Invalid field name. Choose "ECHO INTENSITY", "CORRELATION MAGNITUDE", "PERCENT GOOD","VELOCITY","ABSOLUTE BACKSCATTER","FILTERED ECHO INTENSITY"')
    
        print(f'Writing {data_type_5} to file')
        file = open(f'{path + os.sep + filename}.000','wb')  
        printProgressBar(0, self.n_ensembles,taskname = f'Writing {filename}.000', prefix = 'Progress  0%') 
        for e,ensemble in enumerate(self.ensemble_data):
            printProgressBar(e+1, self.n_ensembles,taskname = f'Writing {filename}.000', prefix = f'Progress  {round(100*(e+1)/self.n_ensembles,0)}%')
            write_ensemble(file,ensemble, data_type_5 = data_type_5)
        #print(f'Successfully created {path + os.sep + filename}.000')
        file.close()    
        
        
#%% TO DO

# conditional printing of progress bar for paralell imports
# errors parsing system configuration with DVS instruments
# errors parsing century with DVS instruments 
# errors writing DVS data back to pd0 format



#%% testing 

# file = r'\\USDEN1-STOR.DHI.DK\\Projects\\41806502\\Data_from_CSA\\Long_Mooring\\DVS\\Cruise_1\\LM-2000m-DVS-24063\\1-Raw\\DVS_0000_24063.PD0'


# file = r'C:\Users\anba\OneDrive - DHI\Desktop\Projects\NORI Post-Campaign\Long Mooring ADCP Analysis\Data_from_CSA\Long_Mooring\DVS\Cruise_3\LM-DVS-24065\DVS_4065_000000.pd0'
# # file = r'C:\Users\anba\OneDrive - DHI\Desktop\Projects\NORI Post-Campaign\Long Mooring ADCP Analysis\Data_from_CSA\Long_Mooring\DVS\Cruise_2\LM-2008m-DVS-24073\Raw\DVS_LM_24073.PD0'
# adcp_data = WorkhorseADCP(file, instrument_depth = 3280, instrument_HAB=4)

# adcp_data.get_bin_midpoint_HAB()
# adcp_data.get_bin_midpoints()



# file = r'C:\Users\anba\OneDrive - DHI\Desktop\Projects\NORI Post-Campaign\Long Mooring ADCP Analysis\Data_from_CSA\Long_Mooring\ADCP\Cruise_2\LM-4316m-600khz_Dn-24154\Raw\DPL2_600_24154.000'
# adcp_data = WorkhorseADCP(file, instrument_depth = 3280, instrument_HAB=4)