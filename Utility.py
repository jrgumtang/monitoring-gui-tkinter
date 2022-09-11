"""
Module: Utility Class
Description: Handles log file creation
            Serial data validation
            Appending data to log file
"""
from datetime import datetime
import csv
import math
import numpy as np
import serial as sr
import os

import Config

class FileUtility:
    
    def createFile():
        global currentFile
        dir_path = os.path.dirname(os.path.realpath(__file__))
        FILE_LOCATION = dir_path + "/logs/"

        timestamp = (datetime.now()).strftime("%y%m%d%H%M%S")
        filename = "lokalte_log_" + timestamp +".csv"
        currentFile = FILE_LOCATION + filename 
        print("csv_path: ", currentFile)
        return currentFile

    def createCSV():
        with open(FileUtility.createFile(), 'w', encoding='UTF8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=Config.FIELDNAMES)
            writer.writeheader()

class DataUtility:
    data = np.array([])
    error_count = 0
    vswr_value = 0
    fwd_pwr =0
    rev_pwr =0
    temp_value = 0
    vswr_temp = 0
    vswr_status = 0

    serial_port = sr.Serial(Config.USB_PORT, 9600) # MAC port

    def validate_raw_data(data):
        for i in data:
            try:
                value = float(i)
                if (math.isinf(value)):
                    DataUtility.error_count += 1
                    print("error_count_INF", DataUtility.error_count)
                    return 0
            except:
                DataUtility.error_count += 1
                print("error_count_NAN", DataUtility.error_count)
                return 0
        return 1

    def getSerialData():
        while(1):
            serial_data = DataUtility.serial_port.readline()
            serial_raw_data = serial_data.decode('utf').rstrip('\r\n').split(",")
            #print("raw_data", len(serial_raw_data))
            check_data = DataUtility.validate_raw_data(serial_raw_data)
    
            if (check_data and (len(serial_raw_data)==7)):
                DataUtility.fwd_pwr = serial_raw_data[0] # Forward Power
                DataUtility.rev_pwr = serial_raw_data[1] # Reverse Power
                DataUtility.vswr_value = serial_raw_data[2] # VSWR value
                DataUtility.temp_value = serial_raw_data[4] # System temp
                DataUtility.vswr_temp = serial_raw_data[5] # VSWR temp
                DataUtility.vswr_status = serial_raw_data[6] #VSWR Status
            else:
                DataUtility.getSerialData()

            DataUtility.appendData(serial_raw_data)
            
    def appendData(raw_data):
        timestamp = (datetime.now()).strftime("%H%M%S")
        with open(currentFile, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, 
                            raw_data[0], 
                            raw_data[1], 
                            raw_data[2], 
                            raw_data[3], 
                            raw_data[4], 
                            raw_data[5], 
                            raw_data[6]])