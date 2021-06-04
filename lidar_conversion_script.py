# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 16:32:08 2019

@author: eneemann

- Script to convert all .laz files in a directory to .las

31 Jul 2019: Created initial version of code (EMN).
"""

import os
import time
import subprocess

# Start timer and print start time in UTC
start_time = time.time()
readable_start = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
print("The script start time is {}".format(readable_start))
today = time.strftime("%Y%m%d")


#lidar_dir = r"C:\Users\eneemann\Desktop\Kanab Lidar"
#os.chdir(lidar_dir)
#
#filenumber = 0
#dir_list = os.listdir(lidar_dir)
#total = len(dir_list)
#for filename in dir_list:
#    filenumber += 1
#    print(f"Starting on file {filenumber} of {total}")
#    base = os.path.splitext(filename)[0]
#    command = f"pdal translate {base}.laz {base}.las"
#    print(command)
#    subprocess.check_call(command)
#    print(f"Done with file {filenumber}, moving on to next file ...")
    
    
    
    
lidar_dir = r"C:\Users\eneemann\Desktop\Bountiful Lidar"
os.chdir(lidar_dir)

filenumber = 0
dir_list = os.listdir(lidar_dir)
total = len(dir_list)
for filename in dir_list:
    filenumber += 1
    print(f"Starting on file {filenumber} of {total}")
    base = os.path.splitext(filename)[0]
    command = f"gdal_translate -of GTiff {base}.img {base}.tif"
    print(command)
    subprocess.check_call(command)
    print(f"Done with file {filenumber}, moving on to next file ...")
    
    
    

    
print("Script shutting down ...")
# Stop timer and print end time in UTC
readable_end = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
print("The script end time is {}".format(readable_end))
print("Time elapsed: {:.2f}s".format(time.time() - start_time))