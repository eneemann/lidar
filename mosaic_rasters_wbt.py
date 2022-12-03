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
data_dir = r"C:\Users\eneemann\Desktop\Zion Lidar"
os.chdir(data_dir)
wbt.set_working_dir(data_dir)

outfile = 'Zion_all.tif'

file_list = []
for file in os.listdir(data_dir):
    if 'NED' in file and file.endswith('.img'):
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


## Need license to use
#wbt.shadow_animation(
#    "clipped_DSM.tif", 
#    'shadows.html', 
#    palette="atlas", 
#    max_dist="", 
#    date="21/06/2021", 
#    interval=15, 
#    location="40.865459/-111.873929/-6", 
#    height=600, 
#    delay=250, 
#    label="")


#wbt.horizon_angle(
#    "clipped_DSM.tif", 
#    'horizon_angle.tif', 
#    azimuth=180.0, 
#    max_dist=100.0)
#
#wbt.time_in_daylight(
#    "clipped_DSM.tif", 
#    'time_in_daylight.tif', 
#    40.865459, 
#    -111.873929, 
#    az_fraction=10.0, 
#    max_dist=100.0, 
#    utc_offset="-06:00", 
#    start_day=1, 
#    end_day=365, 
#    start_time="00:00:00", 
#    end_time="23:59:59")

