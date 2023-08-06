# -*- coding: utf-8 -*-
"""
Created on Mon May 15 15:35:53 2023

@author: sndn
"""
###############################################################################

import os
import warnings
import numpy as np
import pandas as pd
import xml.etree.ElementTree as ET

###############################################################################

class seabird_ctd:
    
    
    def __init__(self, filepath_hex, filepath_xml):
        
        self.filepath_hex = filepath_hex
        self.filepath_xml = filepath_xml
        
        self.data = {}
        
        self.detect_sensors()
        self.parse_xml()
        self.parse_hex()
        
        self.print_metadata()   # Comment out to mute metadata
        
        self.get_xml_coefficients()
        self.get_hex_coefficients()
        self.compare_coefficients()
        
        self.hex2temperature()
        self.hex2pressure()
        self.hex2conductivity()
        self.conductivity2salinity()
        
        if 'TurbidityMeter' in self.sensors:
            self.hex2turbidity()
            
        if 'WET_LabsCStar' in self.sensors:
            self.hex2transmission()
            
        if 'OxygenSensor' in self.sensors:
            self.hex2oxygen()


    def detect_sensors(self):
        
        """
        
        Detects all instruments found in the xml configuration file (.xmlcon) and stores their names in self.sensors
        
        """
        
        self.sensors = []
        
        tree = ET.parse(self.filepath_xml)
        root = tree.getroot()

        sensors = root.findall('Instrument/SensorArray/Sensor')
        
        for sensor in sensors:
            for child in sensor:
                if child.tag != 'NotInUse':
                    self.sensors.append(child.tag)
                    
                    
    def print_metadata(self):
        
        """
        
        Prints file metadata to standard output (terminal)
        
        """
        
        print('\n#################### Seabird CTD Hex File ####################\n')
        print("\033[4m" + 'METADATA' + "\033[0m" + '\n')
        print('    ' + "\033[4m" + 'Instrument name' + "\033[0m" + f': {self.xmlcon["Name"]}')
        print('    ' + "\033[4m" + 'File name' + "\033[0m" + f': {os.path.basename(self.filepath_hex)}')
        print('    ' + "\033[4m" + 'File size' + "\033[0m" + f': {os.path.getsize(self.filepath_hex):,} bytes')
        print('    ' + "\033[4m" + 'Number samples' + "\033[0m" + f': {self.number_samples:,}')
        
        print('    ' + "\033[4m" + 'Attached sensors'+ "\033[0m" + ':')
        for sensor in self.sensors:
            print(f'        {sensor}')
        
        
    def parse_xml(self):
        
        """
        
        Extracts information from the xml configuration file (.xmlcon) and stores it in self.xmlcon dictionary
        
        """
        
        self.xmlcon = {}
        
        tree = ET.parse(self.filepath_xml)
        root = tree.getroot()
        
        self.xmlcon['Name'] = root.find('Instrument/Name').text
    
    
    def parse_hex(self):
        
        """
        
        Extracts information from SBE16/19 hex files such as hexadecimal strings (stored in self.hex_samples)
        and number of samples.
        
        Constructs timestamps for each sample and stores them in self.data['DateTime']
        
        """
        
        hex_file = open(self.filepath_hex, 'r')
        hex_data = hex_file.read()
        hex_file.close()
        
        self.hex_samples = hex_data.split('*END*')[1].strip().split('\n')
        
        hex_header = hex_data.split('*END*')[0].strip().split('\n')
        
        time_start = []         # Array to store start times for each sampling period in the file 
        number_samples = []     # Array to store number of samples for each sampling period in the file
        for line in hex_header:
            if '* hdr' in line or '* cast' in line:
                time_start.append(pd.to_datetime(line.split('samples')[0][-21:]))
                sample_range = [int(i) for i in line.split('samples')[1].split(',')[0].split('to')]
                n_samples = (sample_range[1] - sample_range[0]) + 1
                number_samples.append(n_samples)
                
        if self.xmlcon['Name'] == 'SBE 16plus V2 Seacat CTD':
            sampling_freq = 1
        elif self.xmlcon['Name'] == 'SBE 19plus V2 Seacat CTD':
            sampling_freq = 4
        
        timestep = pd.Timedelta(value=1/sampling_freq, unit='seconds')

        date_time = pd.date_range(start=time_start[0], periods=0, freq=timestep) # Create empty DatetimeIndex 
        for i in range(len(time_start)):
            daterange = pd.date_range(start=time_start[i], periods=number_samples[i], freq=timestep)
            date_time = date_time.append(daterange)
        
        self.number_samples = sum(number_samples)
        self.data['DateTime'] = date_time
    
        ''' Procedure for parsing DeckSamplingSBE hex headers
        n_samples = len(self.hex_measurements)

        hex_header = hex_data.split('*END*')[0]
        time_start = pd.to_datetime(hex_header.split('* System UTC = ')[1])
        time_step = float(hex_header.split('* Real-Time Sample Interval = ')[1].split('seconds')[0])
        time_step = pd.Timedelta(value=time_step, unit='seconds')
        
        self.data['DateTime'] = pd.date_range(start=time_start, periods=n_samples, freq=time_step)
        '''
        
    def get_xml_coefficients(self):
        
        """
        
        Retrieves calibration coefficients for sensors detected in xml configuration file (.xmlcon) and
        stores them in self.coefficients_xml.
        
        """
        
        # Dictionary of all possible sensors (as they appear in xml) and their calibration coefficients (the ones you want).
        sensor_coefficients = \
        {
        'TemperatureSensor': ['A0','A1','A2','A3'],
        'ConductivitySensor': ['G','H','I','J','CPcor','CTcor'],
        'PressureSensor': ['PA0','PA1','PA2','PTEMPA0','PTEMPA1','PTEMPA2','PTCA0','PTCA1','PTCA2','PTCB0','PTCB1','PTCB2'],
        'WET_LabsCStar': ['M','B', 'PathLength'],
        'OxygenSensor': ['A','B','C','D0','D1','D2','E','Tau20','H1','H2','H3','Soc','offset'],
        'TurbidityMeter': ['ScaleFactor','DarkVoltage']
        }
        
        tree = ET.parse(self.filepath_xml)
        root = tree.getroot()
        
        self.coefficients_xml = {}
        
        for sensor in self.sensors:
            
            self.coefficients_xml[sensor] = {}
            
            if sensor == 'ConductivitySensor':
                child = root.findall('Instrument/SensorArray/Sensor/ConductivitySensor/Coefficients')[1]
            
            elif sensor == 'OxygenSensor' and self.xmlcon['Name'] == 'SBE 19plus V2 Seacat CTD':
                child = root.findall('Instrument/SensorArray/Sensor/OxygenSensor/CalibrationCoefficients')[1]
                
            elif sensor == 'OxygenSensor' and self.xmlcon['Name'] == 'SBE 16plus V2 Seacat CTD':
                # Overwrite OxygenSensor coefficients if SBE16 (uses different DO sensor and calibration)
                sensor_coefficients['OxygenSensor'] = ['A0','A1','A2','B0','B1','C0','C1','C2', 'pcor']
                child = root.find('Instrument/SensorArray/Sensor/OxygenSensor')
            
            else:
                child = root.find(f'Instrument/SensorArray/Sensor/{sensor}')
            
            for coefficient in sensor_coefficients[sensor]:
                self.coefficients_xml[sensor][coefficient] = float(child.find(coefficient).text)


    def get_hex_coefficients(self):
        
        """
        
        Retrieves calibration coefficients from SBE16/19 hex file (.hex) and stores them in self.coefficients_hex.
        
        """
        
        hex_file = open(self.filepath_hex, 'r')
        hex_header = hex_file.read()
        hex_file.close()

        hex_header = hex_header.split('*END*')[0]

        self.coefficients_hex = {
                                 'TemperatureSensor': {},
                                 'ConductivitySensor': {},
                                 'PressureSensor': {}
                                }

        self.coefficients_hex['TemperatureSensor']['A0'] = float(hex_header.split('<TA0>')[1].split('</TA0>')[0])
        self.coefficients_hex['TemperatureSensor']['A1'] = float(hex_header.split('<TA1>')[1].split('</TA1>')[0])
        self.coefficients_hex['TemperatureSensor']['A2'] = float(hex_header.split('<TA2>')[1].split('</TA2>')[0])
        self.coefficients_hex['TemperatureSensor']['A3'] = float(hex_header.split('<TA3>')[1].split('</TA3>')[0])

        self.coefficients_hex['ConductivitySensor']['G'] = float(hex_header.split('<G>')[1].split('</G>')[0])
        self.coefficients_hex['ConductivitySensor']['H'] = float(hex_header.split('<H>')[1].split('</H>')[0])
        self.coefficients_hex['ConductivitySensor']['I'] = float(hex_header.split('<I>')[1].split('</I>')[0])
        self.coefficients_hex['ConductivitySensor']['J'] = float(hex_header.split('<J>')[1].split('</J>')[0])
        self.coefficients_hex['ConductivitySensor']['CPcor'] = float(hex_header.split('<CPCOR>')[1].split('</CPCOR>')[0])
        self.coefficients_hex['ConductivitySensor']['CTcor'] = float(hex_header.split('<CTCOR>')[1].split('</CTCOR>')[0])

        self.coefficients_hex['PressureSensor']['PA0'] = float(hex_header.split('<PA0>')[1].split('</PA0>')[0])
        self.coefficients_hex['PressureSensor']['PA1'] = float(hex_header.split('<PA1>')[1].split('</PA1>')[0])
        self.coefficients_hex['PressureSensor']['PA2'] = float(hex_header.split('<PA2>')[1].split('</PA2>')[0])
        self.coefficients_hex['PressureSensor']['PTEMPA0'] = float(hex_header.split('<PTEMPA0>')[1].split('</PTEMPA0>')[0])
        self.coefficients_hex['PressureSensor']['PTEMPA1'] = float(hex_header.split('<PTEMPA1>')[1].split('</PTEMPA1>')[0])
        self.coefficients_hex['PressureSensor']['PTEMPA2'] = float(hex_header.split('<PTEMPA2>')[1].split('</PTEMPA2>')[0])
        self.coefficients_hex['PressureSensor']['PTCA0'] = float(hex_header.split('<PTCA0>')[1].split('</PTCA0>')[0])
        self.coefficients_hex['PressureSensor']['PTCA1'] = float(hex_header.split('<PTCA1>')[1].split('</PTCA1>')[0])
        self.coefficients_hex['PressureSensor']['PTCA2'] = float(hex_header.split('<PTCA2>')[1].split('</PTCA2>')[0])
        self.coefficients_hex['PressureSensor']['PTCB0'] = float(hex_header.split('<PTCB0>')[1].split('</PTCB0>')[0])
        self.coefficients_hex['PressureSensor']['PTCB1'] = float(hex_header.split('<PTCB1>')[1].split('</PTCB1>')[0])
        self.coefficients_hex['PressureSensor']['PTCB2'] = float(hex_header.split('<PTCB2>')[1].split('</PTCB2>')[0])
        
        
    def compare_coefficients(self):

        """
        
        Compares calibration coefficients extracted from xml and hex file and warns user if they do not match.
        
        """
        
        for sensor in self.coefficients_hex:
            for coefficient in self.coefficients_hex[sensor]:
                rtol = abs(self.coefficients_xml[sensor][coefficient] * 0.001)
                if not np.isclose(self.coefficients_xml[sensor][coefficient], self.coefficients_hex[sensor][coefficient], rtol=rtol):
                    warnings.warn(f'*** WARNING *** : {sensor} calibration coefficient {coefficient} in xmlcon does not match corresponding value in hex file... Proceeding with value from xmlcon.')

    
    def get_hex_samples(self):
        
        """
        
        Extracts hexadecimal measurements from SBE16/19 hex file.
        
        """
        
        file_hex = open(self.filepath_hex, 'r')
        data_hex = file_hex.read()
        file_hex.close()
        
        self.hex_samples = data_hex.split('*END*')[1].strip().split('\n')
        
        
    def hex2temperature(self):
        
        """
        
        Calculates temperature (degrees Celcius, C) from hexadecimal string.
        
        """
        
        A0 = self.coefficients_xml['TemperatureSensor']['A0']
        A1 = self.coefficients_xml['TemperatureSensor']['A1']
        A2 = self.coefficients_xml['TemperatureSensor']['A2']
        A3 = self.coefficients_xml['TemperatureSensor']['A3']
        
        temperature_decimal = np.array([int(x[:6], base=16) for x in self.hex_samples])
        MV = (temperature_decimal - 524288)/1.6e7
        R = ((MV*2.900e9) + 1.024e8) / (2.048e4 - (MV*2.0e5))
        temperature_degrees = 1/(A0 + A1*np.log(R) + A2*np.log(R)**2 + A3*np.log(R)**3) - 273.15
        
        self.data['Temperature (C)'] = temperature_degrees


    def hex2conductivity(self):

        """
        
        Calculates conductivity (Simiens/meter, S/m) from hexadecimal string.
        
        """

        G = self.coefficients_xml['ConductivitySensor']['G']
        H = self.coefficients_xml['ConductivitySensor']['H']
        I = self.coefficients_xml['ConductivitySensor']['I']
        J = self.coefficients_xml['ConductivitySensor']['J']
        CPcor = self.coefficients_xml['ConductivitySensor']['CPcor']
        CTcor = self.coefficients_xml['ConductivitySensor']['CTcor']

        conductivity_decimal = np.array([int(x[6:12], base=16) for x in self.hex_samples])
        f = conductivity_decimal / 256 / 1000
        conductivity_spm = (G + H*(f**2)+ I*(f**3) + J*(f**4)) / (1 + CTcor*self.data['Temperature (C)'] + CPcor*self.data['Pressure (dbar)'])
        
        self.data['Conductivity (S/m)'] = conductivity_spm


    def hex2pressure(self):

        """
        
        Calculates pressure (decibars, dbar) from hexadecimal string.
        
        """

        PA0 = self.coefficients_xml['PressureSensor']['PA0']
        PA1 = self.coefficients_xml['PressureSensor']['PA1']
        PA2 = self.coefficients_xml['PressureSensor']['PA2']
        PTEMPA0 = self.coefficients_xml['PressureSensor']['PTEMPA0']
        PTEMPA1 = self.coefficients_xml['PressureSensor']['PTEMPA1']
        PTEMPA2 = self.coefficients_xml['PressureSensor']['PTEMPA2']
        PTCA0 = self.coefficients_xml['PressureSensor']['PTCA0']
        PTCA1 = self.coefficients_xml['PressureSensor']['PTCA1']
        PTCA2 = self.coefficients_xml['PressureSensor']['PTCA2']
        PTCB0 = self.coefficients_xml['PressureSensor']['PTCB0']
        PTCB1 = self.coefficients_xml['PressureSensor']['PTCB1']
        PTCB2 = self.coefficients_xml['PressureSensor']['PTCB2']
        
        pressure_decimal = np.array([int(x[12:18], base=16) for x in self.hex_samples])
        ptcv_decimal = np.array([int(x[18:22], base=16) for x in self.hex_samples])
        
        y = ptcv_decimal / 13107
        t = PTEMPA0 + PTEMPA1*(y) + PTEMPA2*(y**2)
        x = pressure_decimal - PTCA0 - PTCA1*t - PTCA2*(t**2)
        n = (x*PTCB0) / (PTCB0 + PTCB1*t + PTCB2*(t**2))
        
        pressure_dbar = PA0 + PA1*n + PA2*(n**2)
        pressure_dbar = (pressure_dbar - 14.7) * 0.689476
        
        self.data['Pressure (dbar)'] = pressure_dbar


    def hex2turbidity(self):
        
        """
        
        Calculates turbidity (Nephelometric turbidity, NTU) from hexadecimal string measured 
        by WET Labs ECO NTU turbidity sensor.
        
        """
        
        scale_factor = self.coefficients_xml['TurbidityMeter']['ScaleFactor']
        dark_voltage = self.coefficients_xml['TurbidityMeter']['DarkVoltage']
        
        if self.xmlcon['Name'] == 'SBE 16plus V2 Seacat CTD':
            
            turbidity_decimal = np.array([int(x[26:30], base=16) for x in self.hex_samples])
            
        elif self.xmlcon['Name'] == 'SBE 19plus V2 Seacat CTD':
            
            turbidity_decimal = np.array([int(x[30:34], base=16) for x in self.hex_samples])
        
        turbidity_volt = turbidity_decimal / 13107
        turbidity_ntu = scale_factor * (turbidity_volt - dark_voltage)
        
        self.data['Turbidity (NTU)'] = turbidity_ntu
        
        
    def hex2transmission(self):
        
        """
        
        Calculates light transmission (%) and beam attenuation coefficients from hexadecimal string measured 
        by WET Labs C-Star transmissometer.
        
        """
        
        M = self.coefficients_xml['WET_LabsCStar']['M']
        B = self.coefficients_xml['WET_LabsCStar']['B']
        z = self.coefficients_xml['WET_LabsCStar']['PathLength']
        
        transmission_decimal = np.array([int(x[22:26], base=16) for x in self.hex_samples])
        transmission_volt = transmission_decimal / 13107
        
        beam_transmission = (M*transmission_volt) + B
        beam_attenuation = -(1/z)*np.log(beam_transmission/100)
        
        self.data['Light Transmission (%)'] = beam_transmission
        self.data['Beam Attenuation Coefficient'] = beam_attenuation
    
    
    def hex2oxygen(self):
        
        """
        
        Calculates oxygen concentration (milliliters/Liter, mL/L) from hexadecimal string.
        For details on calculation of salinity correction factor (Scorr) see Appendix I of:
        https://www.seabird.com/asset-get.download.jsa?id=54627862513
        
        """
        
        # SBE 63 Dissolved Oxygen Sensor calculations
        if self.xmlcon['Name'] == 'SBE 16plus V2 Seacat CTD':
            
            A0 = self.coefficients_xml['OxygenSensor']['A0']
            A1 = self.coefficients_xml['OxygenSensor']['A1']
            A2 = self.coefficients_xml['OxygenSensor']['A2']
            B0 = self.coefficients_xml['OxygenSensor']['B0']
            B1 = self.coefficients_xml['OxygenSensor']['B1']
            C0 = self.coefficients_xml['OxygenSensor']['C0']
            C1 = self.coefficients_xml['OxygenSensor']['C1']
            C2 = self.coefficients_xml['OxygenSensor']['C2']
            E = self.coefficients_xml['OxygenSensor']['pcor']
            
            T = self.data['Temperature (C)']
            P = self.data['Pressure (dbar)']
            S = self.data['Salinity (PSU)']
            
            # Coefficients for salinity correction factor (Scorr)
            solB0 = -6.24523e-3; solB1 = -7.37614e-3; solB2 = -1.03410e-2; solB3 = -8.17083e-3
            solC0 = -4.88682e-7
            
            Ts = np.log((298.15-T)/(273.15+T))
            
            Scorr = np.exp(S*(solB0+(solB1*Ts)+(solB2*(Ts**2))+(solB3*(Ts**3))) + (solC0*(S**2)))
            
            oxygen_decimal = np.array([int(x[30:36], base=16) for x in self.hex_samples])
            
            V = ((oxygen_decimal/100000)-10) / 39.457071 

            eqpt1 = ((A0+(A1*T)+(A2*(V**2))) / (B0+(B1*V))) - 1
            eqpt2 = C0+(C1*T)+(C2*(T**2))
            eqpt3 = np.exp(E*P/(T+273.15))
            
            oxygen_conc = (eqpt1/eqpt2)*eqpt3*Scorr
            
            self.data['Oxygen (ml/l)'] = oxygen_conc
        
        # SBE 43 Dissolved Oxygen Sensor calculations
        elif self.xmlcon['Name'] == 'SBE 19plus V2 Seacat CTD':
            
            A = self.coefficients_xml['OxygenSensor']['A']
            B = self.coefficients_xml['OxygenSensor']['B']
            C = self.coefficients_xml['OxygenSensor']['C']
            #D0 = self.coefficients_xml['OxygenSensor']['D0']
            #D1 = self.coefficients_xml['OxygenSensor']['D1']
            #D2 = self.coefficients_xml['OxygenSensor']['D2']
            E = self.coefficients_xml['OxygenSensor']['E']
            #Tau20 = self.coefficients_xml['OxygenSensor']['Tau20']
            #H1 = self.coefficients_xml['OxygenSensor']['H1']
            #H2 = self.coefficients_xml['OxygenSensor']['H2']
            #H3 = self.coefficients_xml['OxygenSensor']['H3']
            Soc = self.coefficients_xml['OxygenSensor']['Soc']
            Voffset = self.coefficients_xml['OxygenSensor']['offset']
            
            T = self.data['Temperature (C)']
            P = self.data['Pressure (dbar)']
            
            oxygen_decimal = np.array([int(x[26:30], base=16) for x in self.hex_samples])
            V = oxygen_decimal / 13107
            
            eqpt1 = Soc*(V+Voffset)*(1+(A*T)+(B*(T**2))+(C*(T**3)))
            eqpt2 = np.exp(E*P/(T+273.15))
            oxysat = self.oxygen_saturation()
            
            oxygen_conc = eqpt1*eqpt2*oxysat
            
            self.data['Oxygen (ml/l)'] = oxygen_conc
    
    
    def conductivity2salinity(self):
        
        """
        
        Calculates salinity (PSU) from conductivity following the standards of the Practical Salinity Scale - 1978 (PSS-78)
        For details on calculation see:
        https://salinometry.com/pss-78/
        https://www.seabird.com/asset-get.download.jsa?id=54627861526
        
        """
        
        a = [0.008, -0.1692, 25.3851, 14.0941, -7.0261, 2.7081]
        b = [0.0005, -0.0056, -0.0066, -0.0375, 0.0636, -0.0144]
        k = 0.0162
        
        A1 = 2.07e-5; A2 = -6.37e-10; A3 = 3.989e-15
        B1 = 3.426e-2; B2 = 4.464e-4; B3 = 4.215e-1; B4 = -3.107e-3
        C0 = 6.766097e-1; C1 = 2.00564e-2; C2 = 1.104259e-4; C3 = -6.9698e-7; C4 = 1.0031e-9
        
        T = self.data['Temperature (C)'] * 1.00024      # Temperature IPTS-68, C
        P = self.data['Pressure (dbar)']                # Pressure, dbars
        R = self.data['Conductivity (S/m)'] / 4.2914    # Conductivity ratio (C of water at 35 PSU and 15C @ sea-level = 4.2914 S/m)
        
        Rp = 1 + (((A1*P)+(A2*(P**2))+(A3*(P**3)))/(1+(B1*T)+(B2*(T**2))+(B3*R)+(B4*T*R)))
        rT = C0 + (C1*T) + (C2*(T**2)) + (C3*(T**3)) + (C4*(T**4))
        RT = R/(Rp*rT)
        
        S1 = 0; S2 = 0
        for i in range(6):
            S1 += a[i] * np.power(RT,(i/2))
            S2 += b[i] * np.power(RT,(i/2))
        
        S = S1 + (((T-15)/(1+(k*(T-15))))*S2)
        
        self.data['Salinity (PSU)'] = S
       
        
    def oxygen_saturation(self):
        
        """
        
        Calculates the oxygen saturation limit (mL/L) as a function of temperature and salinity 
        For details see Appendix A of:
        http://www.argodatamgt.org/content/download/26535/181243/file/SBE43_ApplicationNote64_RevJun2013.pdf
        
        Returns:
            oxysat (np.array): oxygen saturation limit (mL/L)
        
        """
        
        A0 = 2.00907; A1 = 3.22014; A2 = 4.0501; A3 = 4.94457; A4 = -0.256847; A5 = 3.88767
        B0 = -0.00624523; B1 = -0.00737614; B2 = -0.010341; B3 = -0.00817083
        C0 = -4.88682e-7
        
        T = self.data['Temperature (C)']
        S = self.data['Salinity (PSU)']
        
        Ts = np.log((298.15-T)/(273.15+T))
        
        eqpt1 = A0+(A1*Ts)+(A2*(Ts**2))+(A3*(Ts**3))+(A4*(Ts**4))+(A5*(Ts**5))
        eqpt2 = (S*(B0+(B1*Ts)+(B2*(Ts**2))+(B3*(Ts**3)))) + (C0*(S**2))
        
        oxysat = np.exp(eqpt1+eqpt2)
        
        return oxysat
        
            
    def dataframe2csv(self):
        
        df = pd.DataFrame.from_dict(self.data)
        
        filename_hex = os.path.basename(self.filepath_hex)
        filename_csv = os.path.splitext(filename_hex)[0] + '.csv'
        
        df.to_csv(filename_csv)


###############################################################################

def main():     
    
    scriptpath = os.path.abspath('.')
    
    relpath_xml = 'ROV CTD/Config/SBE19-7947_DO-1900_CStar-1917_NTU-5874_xmiss_DO_swap.xmlcon'
    #relpath_xml = 'FBCT1 CTD/Config/16-50406.xmlcon'
    #relpath_xml = 'DeckSamplingSBE/DECKSMPL_RETURN03.XMLCON'

    relpath_hex = 'ROV CTD/Raw/SBE19plus_01907947_2022_10_19_0001.hex'
    #relpath_hex = 'FBCT1 CTD/Raw/SBE16plus_01650406_2022_10_04.hex'
    #relpath_hex = 'DeckSamplingSBE/decksmpl_return03.hex'
    
    filepath_xml = os.path.join(scriptpath,relpath_xml)
    filepath_hex = os.path.join(scriptpath,relpath_hex)
    
    test = SeabirdCTD(filepath_hex, filepath_xml)
    
    #print(test.number_samples)
    #print(test.data)
    #print(test.coefficients_xml)
    #test.dataframe2csv()
    
###############################################################################

if __name__ == '__main__':
    main()
    
###############################################################################
