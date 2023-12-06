

import math
import os, sys
import numpy as np
import cv2
from osgeo import gdal, osr
import matplotlib.pyplot as plt
#precondition:list must have latitute as index 0 and longitute at index 1
#returns the average elevation height of the 30m x 30m area around the 
#given gps coordinates
def getElevationHeight(gpsList, pathToData):
    latitude = gpsList[0]
    longitude = gpsList[1]
    
    #setting block letter
    long_letter = "E" if (longitude >= 0 and longitude < 180) else "W"
    lat_letter = "N" if latitude >= 0 else "S"
    
    
    
    #setting latitude block string
    if(lat_letter == "N"):
        if(math.floor(abs(latitude)) > 10):
            latitude_block_str = str(math.floor(abs(latitude)))
        else:
            latitude_block_str = "0" + str(math.floor(abs(latitude)))
    else: #lat_letter = "S"
        if(math.ceil(abs(latitude)) > 10):
            latitude_block_str = str(math.ceil(abs(latitude)))
        else:
            latitude_block_str = "0" + str(math.ceil(abs(latitude)))
    
    #setting longitude block string
    if(long_letter == "W"):
        if(math.ceil(abs(longitude)) > 100):
            longitude_block_str = str(math.ceil(abs(longitude)))
        elif(math.ceil(abs(longitude)) > 10):
            longitude_block_str = "0" + str(math.ceil(abs(longitude)))
        else:
            longitude_block_str = "00" + str(math.ceil(abs(longitude)))
    else: #long_letter = "E"
        if(math.floor(abs(longitude)) > 100):
            longitude_block_str = str(math.floor(abs(longitude)))
        elif(math.floor(abs(longitude)) > 10):
            longitude_block_str = "0" + str(math.floor(abs(longitude)))
        else:
            longitude_block_str = "00" + str(math.floor(abs(longitude)))
    
    
    #gets name of FABDEM 1 x 1 degree block tif FIXME
    blockNameStr = pathToData + lat_letter + latitude_block_str + long_letter + longitude_block_str + "_FABDEM_V1-2.tif"
    
    
    ##########################################################
    
    # # block folder name
    # block_folder_lat_north = ((int(latitude_block_str) // 10) * 10)
    # block_folder_lat_south = (int(math.ceil(int(latitude_block_str) / 10)) * 10)
    # block_folder_long_east = ((int(longitude_block_str) // 10) * 10)
    # block_folder_long_west = (int(math.ceil(int(longitude_block_str) / 10)) * 10)
    # #TODO account for east and west, already accounted for north and south
    # if(lat_letter == "N"):
    #     block_folder_lat_north = str(block_folder_lat_north) if latitude > 10 else "0" + str(block_folder_lat_north)
        
    #     if(math.ceil(abs(longitude)) > 100):
    #         block_folder_long_east = str(block_folder_long_east)
    #     elif(math.ceil(abs(longitude)) > 10):
    #         block_folder_long_east = "0" + str(block_folder_long_east)
    #     else:
    #         block_folder_long_east = "00" + str(block_folder_long_east)
    # else:
    #     block_folder_lat_south = str(block_folder_lat_south) if abs(latitude) > 10 else "0" + str(block_folder_lat_south)
        
    #     if(math.ceil(abs(longitude)) > 100):
    #         block_folder_long_east = str(block_folder_long_east)
    #     elif(math.ceil(abs(longitude)) > 10):
    #         block_folder_long_east = "0" + str(block_folder_long_east)
    #     else:
    #         block_folder_long_east = "00" + str(block_folder_long_east)
        
    # blockFolderName = lat_letter + block_folder_lat + long_letter + "-" + 
    # (lat_letter if int(block_folder_lat_north) < 90 else )
        
    # Load the tif file
    
    fpath = (blockNameStr)
    inRas = gdal.Open(fpath)
    if inRas is None:
        print ('Could not open image file')
        sys.exit(1)
    band1 = inRas.GetRasterBand(1)
    rows = inRas.RasterYSize
    cols = inRas.RasterXSize
    
    cropData = band1.ReadAsArray(0, 0, cols, rows)
    
    numrows = len(cropData)
    numcols = len(cropData[0])
    
    
    if(lat_letter == "N"):
        lat_scalar = 1 - abs(latitude - math.floor(abs(latitude)))
        if(long_letter == "E"):
            long_scalar = abs(longitude) - math.floor(abs(longitude))
        else:
            long_scalar = math.ceil(abs(longitude)) - abs(longitude)
    else:
        lat_scalar = abs(latitude - math.floor(abs(latitude)))
        if(long_letter == "E"):
            long_scalar = abs(longitude) - math.floor(abs(longitude))
        else:
            long_scalar = math.ceil(abs(longitude)) - abs(longitude)
            
    
    # plt.imshow(cropData, cmap='gray')
    # plt.show()
    return cropData[int(numrows * lat_scalar), int(numcols * long_scalar)]

        


print(getElevationHeight([-.951, 8.858], "/Users/mihirsharma/Library/CloudStorage/OneDrive-NorthAlleghenySchoolDistrict/AirLab/"))
# print(int(math.ceil(int("11") / 10)) * 10)