#Silhouette
#Project 1.4.7 Image Artist
#by Aviram Bhalla-Levine and Rebecca Griffin
#Note: Takes longer than three and a half minutes to run, be patient.
#Also, to run call the function 'silhouette' in the 'Version #' directory and
#specify the original image and modified image directories as arguments.

from __future__ import print_function
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os.path
import PIL
import PIL.ImageDraw
import numpy as np

def main(dir_in='Images', dir_out='Modified Images'):
    change_in = raw_input('The current input directory is the subdirectory \
\'' + dir_in + '\'. Would you like to change the input directory? Type \'y\' \
for yes and anything else for no.\n')
    if (change_in == 'y') or (change_in == 'Y'):
        dir_in = raw_input('What should the new input directory be?\n')
        print('The new input subdiretory is now \'' + dir_in + '\'.\n')
    change_out = raw_input('The current output directory is the subdirectory \
\'' + dir_out + '\'. Would you like to change the output directory? Type \'y\' \
for yes and anything else for no.\n')
    if (change_out == 'y') or (change_out == 'Y'):
        dir_out = raw_input('What should the new output directory be?\n')
        print('The new output subdiretory is now \'' + dir_out + '\'.\n')
    images = pull_images(dir_in)[0]
    filenames = pull_images(dir_in)[1]
    for index in range(len(images)):
        print('Modifying Image ' + str(index + 1) + ' of ' + str(len(images))
        + '.')
        color = pick_color(filenames[index])
        modified_image = silhouette(images[index], color)
        print('Saving Image ' + str(index + 1) + ' of ' + str(len(images))
        + '.')
        place_images(modified_image, filenames[index], dir_out)
        
def pick_color(filename):
    color = raw_input('Would you like a colored or transparent background on \
the modified version of\'' + filename + '\'?\nType \'c\' for color or anything \
else for transparent.\n')
    if (color == 'c') or (color == 'C'):
        red = raw_input('What would you like your red value to be? Please use \
an appropriate integer or the value will be recoreded as 0.\n')
        try:
            red = int(red)
        except ValueError:
            red = 0
        if (red < 0) or (red > 255):
            red = 0
        green = raw_input('What would you like your green value to be? Please \
use an appropriate integer or the value will be recoreded as 0.\n')
        try:
            green = int(green)
        except ValueError:
            green = 0
        if (green < 0) or (green > 255):
            green = 0
        blue = raw_input('What would you like your blue value to be? Please use\
 an appropriate integer or the value will be recoreded as 0.\n')
        try:
            blue = int(blue)
        except ValueError:
            blue = 0
        if (blue < 0) or (blue > 255):
            blue = 0
    else:
        red = 0
        green = 0
        blue = 0
    return (red, green, blue)

def silhouette(raw, color=(0, 0, 0)):
    raw_a = np.array(raw)
    img = PIL.Image.new('RGBA', (raw.size[0]-1, raw.size[1]-1))
    img_a = np.array(img)
    progress = 0
    total_brightness = 0
    valid_pixels = 0
    for col in range(1, (raw.size[0]-1)):
        for row in range(1, (raw.size[1]-1)):
            img_a[row][col][0] = int((raw_a[row][col][0]-
            raw_a[row+1][col][0])+(raw_a[row][col][0]-
            raw_a[row][col+1][0])+(raw_a[row][col][0]-
            raw_a[row-1][col][0])+(raw_a[row][col][0]-
            raw_a[row][col-1][0]))
            img_a[row][col][1] = int((raw_a[row][col][1]-
            raw_a[row+1][col][1])+(raw_a[row][col][1]-
            raw_a[row][col+1][1])+(raw_a[row][col][1]-
            raw_a[row-1][col][1])+(raw_a[row][col][1]-
            raw_a[row][col-1][1]))
            img_a[row][col][2] = int((raw_a[row][col][2]-
            raw_a[row+1][col][2])+(raw_a[row][col][2]-
            raw_a[row][col+1][2])+(raw_a[row][col][2]-
            raw_a[row-1][col][2])+(raw_a[row][col][2]-
            raw_a[row][col-1][2]))
            img_a[row][col][3] = raw_a[row][col][3]
            if img_a[row][col][3] != 0:
                total_brightness = (total_brightness + img_a[row][col][0] + 
                img_a[row][col][1] + img_a[row][col][2])
                valid_pixels = valid_pixels + 1
            progress = progress + 1
            if progress % 100000 == 0:
                print(str(progress) + ' iterations out of about ' + 
                str(5*(raw.size[0]-1)*(raw.size[1]-1)) + ' iterations.')
    average_brightness = total_brightness/(10*valid_pixels)
    for col in range(1, (raw.size[0]-1)):
        for row in range(1, (raw.size[1]-1)):
            if ((3*img_a[row][col][0] <= average_brightness) or
            (3*img_a[row][col][1] <= average_brightness) or
            (3*img_a[row][col][2] <= average_brightness)
            or ((img_a[row][col][0]+img_a[row][col][1]+img_a[row][col][2])
            <= average_brightness)):
                img_a[row][col][0] = 0
                img_a[row][col][1] = 0
                img_a[row][col][2] = 0
                img_a[row][col][3] = 0
            else:
                img_a[row][col][3] = 255
            progress = progress + 1
            if progress % 100000 == 0:
                print(str(progress) + ' iterations out of about ' + 
                str(5*(raw.size[0]-1)*(raw.size[1]-1)) + ' iterations.')
    for col in range(1, (raw.size[0]-2)):
        for row in range(1, (raw.size[1]-2)):
            if img_a[row-1][col][3] == 0:
                break
            elif img_a[row][col-1][3] == 0:
                break
            elif img_a[row+1][col][3] == 0:
                break
            elif img_a[row][col+1][3] == 0:
                break
            elif img_a[row-1][col-1][3] == 0:
                break
            elif img_a[row+1][col-1][3] == 0:
                break
            elif img_a[row-1][col+1][3] == 0:
                break
            elif img_a[row+1][col+1][3] == 0:
                break
            else:
                img_a[row][col][3] = 255
            progress = progress + 1
            if (((progress % 100000) == 0) or 
            (progress == (4*(raw.size[0]-2)*(raw.size[1]-2)))):
                print(str(progress) + ' iterations out of about ' + 
                str(5*(raw.size[0]-1)*(raw.size[1]-1)) + ' iterations.')
    for col in range(1, (raw.size[0]-1)):
        for row in range(1, (raw.size[1]-1)):
            if ((img_a[row][col][0] >= 240) and
            (img_a[row][col][1] >= 240) and
            (img_a[row][col][2] >= 240)):
                img_a[row][col][0] = 0
                img_a[row][col][1] = 0
                img_a[row][col][2] = 0
                img_a[row][col][3] = 0
            progress = progress + 1
            if progress % 100000 == 0:
                print(str(progress) + ' iterations out of about ' + 
                str(5*(raw.size[0]-1)*(raw.size[1]-1)) + ' iterations.')
    for col in range(1, (raw.size[0]-1)):
        for row in range(1, (raw.size[1]-1)):
            if (img_a[row][col][3] >= 15):
                img_a[row][col][0] = 0
                img_a[row][col][1] = 0
                img_a[row][col][2] = 0
                img_a[row][col][3] = 255
            progress = progress + 1
            if progress % 100000 == 0:
                print(str(progress) + ' iterations out of about ' + 
                str(5*(raw.size[0]-1)*(raw.size[1]-1)) + ' iterations.')
    if color != (0, 0, 0):
        for col in range(1, (raw.size[0]-1)):
            for row in range(1, (raw.size[1]-1)):
                if (img_a[row][col][3] < 15):
                    img_a[row][col][0] = color[0]
                    img_a[row][col][1] = color[1]
                    img_a[row][col][2] = color[2]
                    img_a[row][col][3] = 255
                progress = progress + 1
                if progress % 100000 == 0:
                    print(str(progress) + ' iterations out of about ' + 
                    str(5*(raw.size[0]-1)*(raw.size[1]-1)) + ' iterations.')
    else:
        progress = progress + (raw.size[0]-1)*(raw.size[1]-1)
        print(str(progress) + ' iterations out of about ' + 
        str(4*(raw.size[0]-1)*(raw.size[1]-1)) + ' iterations.')
    image = PIL.Image.fromstring('RGBA', (raw.size[0]-1, raw.size[1]-1), 
    img_a)
    return image

def pull_images(directory):
    image_list = [] # Initialize aggregaotrs
    file_list = []
    directory_list = os.listdir(directory) # Get list of files
    for entry in directory_list:
        absolute_filename = os.path.join(directory, entry)
        try:
            raw = PIL.Image.open(absolute_filename)
            if (raw.mode != 'RGBA'):
                raw = raw.convert('RGBA')
            file_list += [entry]
            image_list += [raw]
        except IOError:
            pass # do nothing with errors tying to open non-images
    return image_list, file_list

def place_images(new_image, old_filename, directory):
    # Create a new directory 'Modified Images'
    new_directory = os.path.join(directory)
    try:
        os.mkdir(new_directory)
    except OSError:
        pass # if the directory already exists, proceed
    # Parse the filename
    filename, filetype = old_filename.split('.')
    #save the altered image, using PNG to retain transparency
    new_image_filename = os.path.join(new_directory, filename + '.png')
    new_image.save(new_image_filename)

main()