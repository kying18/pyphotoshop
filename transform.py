"""
Python Image Manipulation by Kylie Ying (modified from MIT 6.865)

YouTube Kylie Ying: https://www.youtube.com/ycubed 
Twitch KylieYing: https://www.twitch.tv/kylieying 
Twitter @kylieyying: https://twitter.com/kylieyying 
Instagram @kylieyying: https://www.instagram.com/kylieyying/ 
Website: https://www.kylieying.com
Github: https://www.github.com/kying18 
Programmer Beast Mode Spotify playlist: https://open.spotify.com/playlist/4Akns5EUb3gzmlXIdsJkPs?si=qGc4ubKRRYmPHAJAIrCxVQ 
"""

from image import Image
import numpy as np

def brighten(image, factor):
    # when we brighten, we just want to make each channel higher by some amount 
    # factor is a value > 0, how much you want to brighten the image by (< 1 = darken, > 1 = brighten)
    x_pixels, y_pixels, num_channels = image.array.shape  # represents x, y pixels of image, # channels (R, G, B)
    new_im = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)  # making a new array to copy values to!

    # # this is the non vectorized version
    # for x in range(x_pixels):
    #     for y in range(y_pixels):
    #         for c in range(num_channels):
    #             new_im.array[x, y, c] = image.array[x, y, c] * factor

    # faster version that leverages numpy
    new_im.array = image.array * factor

    return new_im

def adjust_contrast(image, factor, mid):
    # adjust the contrast by increasing the difference from the user-defined midpoint by factor amount
    x_pixels, y_pixels, num_channels = image.array.shape  # represents x, y pixels of image, # channels (R, G, B)
    new_im = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)  # making a new array to copy values to!
    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                new_im.array[x, y, c] = (image.array[x, y, c] - mid) * factor + mid

    return new_im

def blur(image, kernel_size):
    # kernel size is the number of pixels to take into account when applying the blur
    # (ie kernel_size = 3 would be neighbors to the left/right, top/bottom, and diagonals)
    # kernel size should always be an *odd* number
    x_pixels, y_pixels, num_channels = image.array.shape  # represents x, y pixels of image, # channels (R, G, B)
    new_im = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)  # making a new array to copy values to!
    neighbor_range = kernel_size // 2  # this is a variable that tells us how many neighbors we actually look at (ie for a kernel of 3, this value should be 1)
    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                # we are going to use a naive implementation of iterating through each neighbor and summing
                # there are faster implementations where you can use memoization, but this is the most straightforward for a beginner to understand
                total = 0
                for x_i in range(max(0,x-neighbor_range), min(new_im.x_pixels-1, x+neighbor_range)+1):
                    for y_i in range(max(0,y-neighbor_range), min(new_im.y_pixels-1, y+neighbor_range)+1):
                        total += image.array[x_i, y_i, c]
                new_im.array[x, y, c] = total / (kernel_size ** 2)
    return new_im

def apply_kernel(image, kernel):
    # the kernel should be a 2D array that represents the kernel we'll use!
    # for the sake of simiplicity of this implementation, let's assume that the kernel is SQUARE
    # for example the sobel x kernel (detecting horizontal edges) is as follows:
    # [1 0 -1]
    # [2 0 -2]
    # [1 0 -1]
    x_pixels, y_pixels, num_channels = image.array.shape  # represents x, y pixels of image, # channels (R, G, B)
    new_im = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)  # making a new array to copy values to!
    neighbor_range = kernel.shape[0] // 2  # this is a variable that tells us how many neighbors we actually look at (ie for a 3x3 kernel, this value should be 1)
    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                total = 0
                for x_i in range(max(0,x-neighbor_range), min(new_im.x_pixels-1, x+neighbor_range)+1):
                    for y_i in range(max(0,y-neighbor_range), min(new_im.y_pixels-1, y+neighbor_range)+1):
                        x_k = x_i + neighbor_range - x
                        y_k = y_i + neighbor_range - y
                        kernel_val = kernel[x_k, y_k]
                        total += image.array[x_i, y_i, c] * kernel_val
                new_im.array[x, y, c] = total
    return new_im

def combine_images(image1, image2):
    # let's combine two images using the squared sum of squares: value = sqrt(value_1**2, value_2**2)
    # size of image1 and image2 MUST be the same
    x_pixels, y_pixels, num_channels = image1.array.shape  # represents x, y pixels of image, # channels (R, G, B)
    new_im = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)  # making a new array to copy values to!
    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                new_im.array[x, y, c] = (image1.array[x, y, c]**2 + image2.array[x, y, c]**2)**0.5
    return new_im
    
#made function accept input from user
if __name__ == '__main__':
    ask = input('What picture you wanna process? : ')
    lake = Image(filename= ask+'.png')
    
    #city = Image(filename='city.png')
  
    print('Choose One Of The Function')
    print('Brighten, Contrast, Blur, Kernel, Combine')
    function = input('Your Choice: ').lower()
    if function == 'brighten':
        name = input('What your new picture name? ')
        add_size3 = float(input('Add your size: '))
        brightened_im = brighten(lake, add_size3)
        brightened_im.write_image(name +'.png')
    elif function == 'contrast':
        name = input('What your new picture name? ')
        add_size1 = float(input('Input first size: '))
        add_size2 = float(input('Input second size: '))
        contrast = adjust_contrast(lake, add_size1, add_size2)
        contrast.write_image(name + '.png')
    elif function == 'blur':
        name = input('What your new picture name? ')
        add_size4 = int(input('Add your size: '))
        blur_3 = blur(lake, add_size4)
        blur_3.write_image(name + '.png')
    elif function == 'kernel':
        name1 = input('What your new x kernel picture name? ')
        name2 = input('What your new y kernel picture name? ')
        sobel_x_kernel = np.array([
            [1,2,1], 
            [0,0,0], 
            [-1,-2,-1]
        ])
        sobel_y_kernel = np.array([
            [1,0,-1],
            [2,0,-2],
            [1,0,-1]
        ])

        sobel_x = apply_kernel(lake, sobel_x_kernel)
        sobel_x.write_image(name1 + '.png')
        sobel_y = apply_kernel(lake, sobel_y_kernel)
        sobel_y.write_image(name2 + '.png')
    elif function == 'combine':
        name1 = input('What your new picture name? ')
        sobel_x_kernel = np.array([
            [1,2,1], 
            [0,0,0], 
            [-1,-2,-1]
        ])
        sobel_y_kernel = np.array([
            [1,0,-1],
            [2,0,-2],
            [1,0,-1]
        ])

        sobel_x = apply_kernel(lake, sobel_x_kernel)
        
        sobel_y = apply_kernel(lake, sobel_y_kernel)
        
        sobel_xy = combine_images(sobel_x, sobel_y)
        sobel_xy.write_image(name1 + '.png')
     else:
        quit()

