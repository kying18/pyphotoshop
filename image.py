import numpy as np
import png

class Image:
    def __init__(self, filename):
        self.input_path = 'input/'
        self.output_path = 'output/'
        self.filename = filename
        self.path_to_file = self.input_path + filename
        self.image = self.read_image()  # initializing the image

    def read_image(self, gamma=2.2):
        '''
        read PNG RGB image, return 3D numpy array organized along Y, X, channel
        values are float, gamma is decoded
        '''
        image = png.Reader(self.path_to_file).asFloat()
        resized_image = np.vstack(list(image[2]))
        resized_image.resize(image[1], image[0], 3)
        resized_image = resized_image ** gamma
        return resized_image

    def write_image(self, output_file_name, gamma=2.2):
        '''
        3D numpy array (Y, X, channel) of values between 0 and 1 -> write to png
        '''
        image = np.clip(self.image, 0, 1)
        y, x = self.image.shape[0], self.image.shape[1]
        image = image.reshape(y, x*3)
        writer = png.Writer(x, y)
        with open(self.output_path + output_file_name, 'wb') as f:
            writer.write(f, 255*(image**(1/gamma)))

        self.image.resize(y, x, 3)  # we mutated the method in the first step of the function
        

if __name__ == '__main__':
    im = Image('lake.png')
    im.write_image('test.png')