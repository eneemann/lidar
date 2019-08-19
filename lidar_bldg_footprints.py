# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 15:08:08 2019

@author: eneemann

- Script to generate building footprints from .las files

16 Aug 2019: Created initial version of code (EMN), started from ESRI script.
"""

import os
import time
import arcpy
import tempfile
import math

# Start timer and print start time in UTC
start_time = time.time()
readable_start = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
print("The script start time is {}".format(readable_start))
today = time.strftime("%Y%m%d")

lidar_dir = r'C:\Users\eneemann\Desktop\small lidar'
os.chdir(lidar_dir)
in_las = os.listdir(lidar_dir)
print(in_las)
out_folder = r'C:\Users\eneemann\Desktop\small lidar'
basename = 'test'  # basename for output files
# final_lasd = 'small_lidar_dataset'  # output LAS dataset

# First pass, create a las dataset
my_lasd = 'small_lidar.lasd'
# arcpy.management.CreateLasDataset(in_las, my_lasd)

lasd = my_lasd
dem = os.path.join(lidar_dir, 'small_dem.tif')
footprint = os.path.join(lidar_dir, 'small_footprints.shp')

# try:
desc = arcpy.Describe(lasd)
if desc.spatialReference.linearUnitName in ['Foot_US', 'Foot']:
    unit = 'Feet'
else:
    unit = 'Meters'
ptSpacing = desc.pointSpacing * 2.25
print(f"the units are: {unit}, the point spacing is: {ptSpacing}")
sampling = '{0} {1}'.format(ptSpacing, unit)
print(f"the sampling distance is: {sampling}")
# Classify overlap points
print("Classifying overlap points ...")
arcpy.ddd.ClassifyLasOverlap(lasd, sampling)

# Classify ground points
print("Classifying ground points ...")
arcpy.ddd.ClassifyLasGround(lasd)

# Filter for ground points
print("Filtering to ground points and generating DEM ...")
arcpy.management.MakeLasDatasetLayer(lasd, 'ground', class_code=[2])

# Generate DEM
# arcpy.conversion.LasDatasetToRaster('ground', dem, 'ELEVATION',
#                                     'BINNING NEAREST NATURAL_NEIGHBOR',
#                                     sampling_type='CELLSIZE',
#                                     sampling_value=desc.pointSpacing)
arcpy.conversion.LasDatasetToRaster(lasd, dem, "ELEVATION",
                                    "BINNING NEAREST NATURAL_NEIGHBOR", "FLOAT",
                                    "CELLSIZE", 0.5, 1)

# Classify noise points
print("Classifying noise points ...")
arcpy.ddd.ClassifyLasNoise(lasd, method='ISOLATION', edit_las='CLASSIFY',
                           withheld='WITHHELD', ground=dem,
                           low_z='-2 feet', high_z='300 feet',
                           max_neighbors=ptSpacing, step_width=ptSpacing,
                           step_height='10 feet')
# Classify buildings
print("Classifying building points ...")
arcpy.ddd.ClassifyLasBuilding(lasd, '9 feet', '100 Square Feet')

#Classify vegetation
print("Classifying vegetation by height ...")
arcpy.ddd.ClassifyLasByHeight(lasd, 'GROUND', [5, 20, 50],
                              compute_stats='COMPUTE_STATS')

# Filter LAS dataset for building points
print("Filtering to building points and exporting to raster ...")
lasd_layer = 'building points'
arcpy.management.MakeLasDatasetLayer(lasd, lasd_layer, class_code=[6])
# Export raster from lidar using only building points
temp_raster = 'in_memory/bldg_raster'
arcpy.management.LasPointStatsAsRaster(lasd_layer, temp_raster,
                                       'PREDOMINANT_CLASS', 'CELLSIZE', 2.5)

# Convert building raster to polygon
print("Converting raster to polygon feature class ...")
temp_footprint = 'in_memory/footprint'
arcpy.conversion.RasterToPolygon(temp_raster, temp_footprint)

# Regularize building footprints
print("Regularizing building footprints ...")
arcpy.ddd.RegularizeBuildingFootprint(temp_footprint, footprint,
                                      method='RIGHT_ANGLES')

# except arcpy.ExecuteError:
print(arcpy.GetMessages())


print("Script shutting down ...")
# Stop timer and print end time in UTC
readable_end = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
print("The script end time is {}".format(readable_end))
print("Time elapsed: {:.2f}s".format(time.time() - start_time))