import cv2
import sys
import random
import os
import numpy as np
import math
window_name = 'Image'
color = (0, 0, 0)

class ImagePreprocessor:

    def __init__(self):
        self.freq = []
        pass

    def incFreq(self, x):
        self.freq[x[0]] += 1
        print(sum(self.freq))

    def fit(self, images):
        self.images = []
        self.read_images(images)

    def drawLines(self, image,linetype):
        # print(image.shape,"***********")
        if(linetype=="h_line"):
            image=cv2.rotate(image,cv2.ROTATE_90_CLOCKWISE)
        self.height=image.shape[1]
        self.width=image.shape[0]
        num_pixels = self.num_pixels
        avg_corrupt = self.avg_corrupt
        min_h = 10/100*(self.height)//1
        max_h = 30/100*(self.height)//1
        init_prob = avg_corrupt/self.height
        # cv2.imshow(window_name, image)
        # cv2.waitKey(0)

        s = []
        temp = 0
        total = 0
        vis = [0 for j in range(self.height*self.width)]
        for i in range(self.width):
            j = 0
            if(total > self.height*self.width or temp > num_pixels):
                break
            thickness = random.randint(1, ((1/100)*self.width)//1)
            while (j < self.height):
                if(vis[(i*self.width+j)//5]):
                    j += 1
                    total += 1
                    init_prob = ((num_pixels-temp) /
                                 (self.height*self.width-total))
                    continue
                height = random.randint(
                    min_h, min(self.height-j, max_h)+min_h)
                prob = random.uniform(0, 1)
                if(prob <= init_prob):
                    s.append((i, j, min(self.height, j+height), thickness))
                    vis[i*self.width+j] = height
                    temp = temp+height*thickness
                    total += height*thickness
                else:
                    total += height
                if(total > self.height*self.width or temp > num_pixels):
                    break

                init_prob = ((num_pixels-temp) /
                             (self.height*self.width-total))
                j += height

        for i in range(len(s)):
            image = cv2.line(
                image, (s[i][0], s[i][1]), (s[i][0], s[i][2]), color, s[i][-1])
        if(linetype=="h_line"):
            image=cv2.rotate(image,cv2.ROTATE_90_CLOCKWISE)
        self.height=image.shape[1]
        self.width=image.shape[0]
        return image



    
    def read_images(self,paths):
        self.images=[]
        for i in range(len(paths)):
            image = cv2.imread(os.path.join("craters/moon1.png"))
            self.images.append(image)
        self.images=np.array(self.images)


    def CorruptImages(self, percent=2, linetype="v_line"):
        try:
            if(self.images.ndim == 4):
                pass
        except:
            self.images = np.array(self.images)

        try:
            if(self.images.ndim != 4):
                raise ValueError
        except:
            print("Expected a 4 Dimensional array (An array of images)")
        else:

            try:
                if(percent < 0 or percent > 100):
                    raise ValueError
            except:
                print("Invalid Percentage (percent should be an int >=0 and <=100)")
            else:
                self.width = self.images[0].shape[0]
                self.height = self.images[0].shape[1]
                num_pixels = int((percent/100)*(self.width*self.height))
                avg_corrupt = math.ceil(num_pixels/self.width)
                self.num_pixels = num_pixels
                self.avg_corrupt = avg_corrupt
                

                # corrupt_function =np.vectorize(self.drawLines)
                # print(self.images.shape[0])
                corrupted_images=np.array(list(map(lambda x:self.drawLines(self.images[x],linetype),list(range(self.images.shape[0])))))
                # print(corrupted_images.shape)
                for i in range(len(corrupted_images)):
                    cv2.imshow(window_name, corrupted_images[i])
                    cv2.waitKey(0)
                return corrupted_images
        





image_paths = ["craters/moon1.png","craters/moon1.png"]
preprocessor = ImagePreprocessor()
preprocessor.fit(image_paths)
corrupted=preprocessor.CorruptImages(2, linetype="v_line")