from fileinput import filename
import cv2
import sys
import random
import os
import numpy as np
import math
from PIL import Image
# import skimage
import matplotlib.pyplot as plt
# from rasterio.plot import show
from osgeo import gdal, ogr


window_name = 'Image'
color = (0, 0, 0)

class ImagePreprocessor:

    def __init__(self):
        self.freq = []
        pass

    def incFreq(self, x):
        self.freq[x[0]] += 1
        print(sum(self.freq))

    def CreateGeoTiff(self,outRaster, data, geo_transform, projection):
        driver = gdal.GetDriverByName('GTiff')
        no_bands,rows,cols = data.shape
        # print(geo_transform,projection)
        DataSet = driver.Create(outRaster, cols, rows, no_bands, gdal.GDT_Float32)
        DataSet.SetGeoTransform(geo_transform)
        DataSet.SetProjection(projection)

        data1 = np.moveaxis(data, -1, 0)
        print(data1.shape,"******")

        for i, image in enumerate(data, 1):
            # print(i,image)
            DataSet.GetRasterBand(i).WriteArray(image)
        DataSet.FlushCache()
        DataSet = None

    def fit(self, images):
        self.images = []
        self.projection=[]
        self.geotrans=[]
        self.read_images(images)

    def drawLines(self, image,projection,geotrans,linetype):
        if(linetype=="h_line"):
            image=np.rot90(image,axes=(1,2))
            # print(image.shape,image1.shape)
        #     image=cv2.rotate(image,cv2.ROTATE_90_CLOCKWISE)
        self.height=image.shape[1]
        self.width=image.shape[2]
        print(self.height,self.width,"********")
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
        gap=max(1,int(1/100* self.width))
        # print(gap)
        iter=0
        dummy=np.zeros((image.shape))
        # print(image.shape,"##############################")
        # print(image)

        while(temp<num_pixels):
            iter+=1
            if(iter==10):
                break
            for i in range(0,self.width,gap):
                j = 0
                if(total > self.height*self.width or temp > num_pixels):
                    break
                thickness = random.randint(1, ((1/100)*self.width)//1)
                while (j < self.height):
                    if(vis[(i*self.height+j)//5]):
                        j += 1
                        total += 1
                        init_prob = ((num_pixels-temp) /
                                    (self.height*self.width-total))
                        continue
                    height = random.randint(
                        min_h, min(self.height-j, max_h)+min_h)
                    # print(height,"________")
                    prob = random.uniform(0, 1)
                    if(prob <= init_prob):
                        s.append((i, j, min(self.height, j+height), thickness))
                        vis[i*self.height+j] = height
                        temp = temp+height*thickness
                        total += height*thickness
                    else:
                        total += height
                    if(total >= self.height*self.width or temp > num_pixels):
                        break

                    init_prob = ((num_pixels-temp) /
                                (self.height*self.width-total))
                    j += height
        print(num_pixels,temp,"*******")

        for i in range(len(s)):
            # print("-----------",image.shape,"******************")
            dummy[:,s[i][1]:s[i][2],s[i][0]:(s[i][0]+s[i][-1])]=image[:,s[i][1]:s[i][2],s[i][0]:(s[i][0]+s[i][-1])]
            image[:,s[i][1]:s[i][2],s[i][0]:(s[i][0]+s[i][-1])]=0
            # image = cv2.line(
                # image, (s[i][0], s[i][1]), (s[i][0], s[i][2]), color, s[i][-1])
        # if(linetype=="h_line"):
            # image=cv2.rotate(image,cv2.ROTATE_90_CLOCKWISE)
        if(linetype=="h_line"):
            image=np.rot90(image,axes=(1,2))
            dummy=np.rot90(dummy,axis=(1,2))
        self.height=image.shape[1]
        self.width=image.shape[2]
        # print("***********")
        # print(image)
        return (image,dummy)



    
    def read_images(self,paths):
        self.images=[]
        self.paths=paths
        for i in range(len(paths)):

            dataset = gdal.Open(os.path.join(paths[i]))
            print(dataset.RasterCount)
            geotrans=dataset.GetGeoTransform()
            proj=dataset.GetProjection()
            image=dataset.ReadAsArray()
            self.geotrans.append(geotrans)
            self.projection.append(proj)
            # image = cv2.imread(os.path.join(paths[i]))
            self.images.append(image)
            

        self.images=np.array(self.images)
        print(self.images.shape)



    def CorruptImages(self, percent=2, linetype="v_line"):
        try:
            # print(self.images.ndim,"*******",self.images)
            if(self.images.ndim == 4):
                pass
        except:
            self.images = np.array(self.images)

        # try:
        #     if(self.images.ndim == 1):
        #         raise ValueError
        # except:
        #     print(" Dimensional array (An array of images)")
        # else:

        try:
            if(percent < 0 or percent > 100):
                raise ValueError
        except:
            print("Invalid Percentage (percent should be an int >=0 and <=100)")
        else:
            self.width = self.images[0].shape[2]
            self.height = self.images[0].shape[1]
            num_pixels = int((percent/100)*(self.width*self.height))
            avg_corrupt = math.ceil(num_pixels/self.width)
            self.num_pixels = num_pixels
            self.avg_corrupt = avg_corrupt
            
            corrupted_images=list(map(lambda x:self.drawLines(self.images[x],self.projection[x],self.geotrans[x],linetype),list(range(self.images.shape[0]))))
            dummy_images=np.array(list(map(lambda x: x[1],corrupted_images)))
            corrupted_images=np.array(list(map(lambda x: x[0],corrupted_images)))
            for i in range(len(corrupted_images)):
                if("/" in self.paths[i]):
                    filename=self.paths[i].split("/")[-1]
                else:
                    filename=self.paths[i]
                
                self.CreateGeoTiff("original_images/new_"+filename,corrupted_images[i]+dummy_images[i],self.geotrans[i],self.projection[i])
                self.CreateGeoTiff("striped_images/new_"+filename,corrupted_images[i],self.geotrans[i],self.projection[i])
                self.CreateGeoTiff("dummy_images/new_"+filename,dummy_images[i],self.geotrans[i],self.projection[i])
                # cv2.imwrite("striped_images/striped_"+filename,corrupted_images[i])
                # cv2.imshow(window_name, corrupted_images[i])
                # cv2.waitKey(0)
            return corrupted_images
        



"""
    Inputs are array of paths of image files 

    Output will be present in same directory of input with _new attached to the filename
    eg: if input is craters/moon1.png , then outut will be present in craters/moon1_new.png


"""



"paths could be relative paths or absolute paths"
dir_path="cropped_images"
# image_paths=[]
"********************* GIVE THE INPUT OF THE FILENAME/PATH HERE ****************************"
image_paths=["cropped_images/cropped_0000_Area1_MI_MAP_03_N22E196N21E197SC.tif"]
# for filename in sorted(os.listdir(dir_path)):
    # if(filename.endswith(".tif")):
        # image_paths.append(dir_path+"/"+filename)
    
print(image_paths)

# image_paths = ["cropped_images/cropped_image_0000.png","cropped_images/cropped_image_0001.png"]
preprocessor = ImagePreprocessor()
preprocessor.fit(image_paths)

"""
    The first argumen is percent between 0 to 100 , as of no the algorithtm works
    well for percent between 0 to 50% but can try giving 50% above as well.
    The second argument is v_line for vertical lines and h_line for horizontal line

"""
corrupted=preprocessor.CorruptImages(2, linetype="v_line")

