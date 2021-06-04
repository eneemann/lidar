# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 14:38:41 2021
- Simple script to mosaic rasters files using whitebox tools
@author: eneemann
"""

# Import Libraries
import os
import time
from whitebox import WhiteboxTools

# Start timer and print start time in UTC
start_time = time.time()
readable_start = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
print("The script start time is {}".format(readable_start))
today = time.strftime("%Y%m%d")

# Set up whitebox tools
wbt = WhiteboxTools()
wbt.set_verbose_mode(True)
wbt.set_compress_rasters(True)

# Define variables
data_dir = r"C:\Users\eneemann\Desktop\Bountiful Lidar"
os.chdir(data_dir)
wbt.set_working_dir(data_dir)

outfile = 'hh_all.tif'

file_list = []
for file in os.listdir(data_dir):
    if 'hh' in file and file.endswith('.tif'):
        file_list.append(file)

        
print("List of files to mosaic:")
for file in file_list:
    print(file)
    
# Need to convert file list into a string for WBT inputs 
file_string = ", ".join([file for file in file_list])
print(file_string)

print("Mosaicking files ...")    
wbt.mosaic(outfile, inputs=file_string, method="nn")


print("Script shutting down ...")
# Stop timer and print end time in UTC
readable_end = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
print("The script end time is {}".format(readable_end))
print("Time elapsed: {:.2f}s".format(time.time() - start_time))