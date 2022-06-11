from PIL import Image
import numpy as np
import os
import math
import argparse

#Author: Braeden Ellershaw (braeden.ellershaw@gmail.com)
#Description: Generates an ascii .txt file from an image using python
#Usage: python image-to-ascii.py -i [input file location] -o [output file location]
#Date of Creation: June 11, 2022
#Last Updated June 11, 2022

def main():

    #get arguments from command line
    parser = argparse.ArgumentParser(description='Generates an ascii .txt file from an image.')
    parser.add_argument("-i","--img", help = "The file path of the image to convert.",required = True,  default="", type = str)
    parser.add_argument("-o","--out", help = "Output file location.", default="", required = True, type = str)
    parser.add_argument("-x","--x_px", help = "The x-axis pixel size for each chunk ", default="32", required = False, type = int)
    parser.add_argument("-y","--y_px", help = "The y-axis pixel size for each chunk ", default="32", required = False, type = int)
    args = parser.parse_args()

    #set variables to corresponding argument values
    img_loc = args.img #the location of the input image
    out_loc = args.out #the location of the output file
    x_px = args.x_px #the x-axis pixel size for each chunk 
    y_px = args.y_px #the y-axis pixel size for each chunk 

    #load image and convert it to grayscale
    img = Image.open(img_loc) # open image as img
    img = img.convert('L') #convert img to grayscale 
    np_img = np.asarray(img) #create numpy array from img
    ascii_arr = np.empty( (math.ceil(np_img.shape[0]/x_px),(math.ceil(np_img.shape[1]/y_px))), dtype=str) #numpy array that holds numpy values

    #create chunks and process image
    for x in range(0,np_img.shape[0],x_px):
        for y in range(0,np_img.shape[1],y_px):

            img_chunk = np_img[x:(x+x_px),y:(y+y_px)] #create chunk from imput image
            color_avg = 255 - np.average(img_chunk) #average brightness of the chunk
            ascii_char = get_ascii(color_avg) #create ascii character from average brightness
            ascii_arr[int(x/x_px), int(y/y_px)] = ascii_char #assign character to location in output array

    np.savetxt(X = ascii_arr, fname = out_loc, fmt = "%s") #save to file location 
    print("ASCII image saved to:", os.path.abspath(out_loc))

#convert sections to ascii characters with same average
def get_ascii(color_avg):
    if color_avg >= 230:
        return "$"
    elif color_avg >= 200:
        return "A"
    elif color_avg >= 180:
        return "V"
    elif color_avg >= 150:
        return "0"
    elif color_avg >= 100:
        return "$" 
    elif color_avg >= 50:
        return "I" 
    elif color_avg >= 25:
        return "1"      
    else:
        return "-"
main()