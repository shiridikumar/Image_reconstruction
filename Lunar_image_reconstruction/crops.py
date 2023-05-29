import random
import cv2
import os
import numpy as np
from osgeo import gdal, ogr
import numpy as np
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import ImageDataGenerator

global images
images=[]
global ind
ind=0

datagen = ImageDataGenerator(width_shift_range=0.2,
                             height_shift_range=0.2,
                             horizontal_flip=True,
                             rotation_range=45,
                             brightness_range=[0.5,2.0],
                             zoom_range=[1.2,0.8]
                            )


def CreateGeoTiff(outRaster, data, geo_transform, projection):
    driver = gdal.GetDriverByName('GTiff')
    no_bands,rows,cols = data.shape
    DataSet = driver.Create(outRaster, cols, rows, no_bands, gdal.GDT_Float32)
    DataSet.SetGeoTransform(geo_transform)
    DataSet.SetProjection(projection)
    for i, image in enumerate(data, 1):
        DataSet.GetRasterBand(i).WriteArray(image)
    

    DataSet.FlushCache()
    DataSet = None


def make_crops(filename):
    global ind
    dataset = gdal.Open(filename)
    geotrans=dataset.GetGeoTransform()
    proj=dataset.GetProjection()
    image=dataset.ReadAsArray()
    stx=0;sty=0
    mw,mh=image.shape[1],image.shape[2]
    while(stx<mw-256):
        sty=0

        while(sty<mh-256):
            crop_image = image[:,stx:stx+256, sty:sty+256]
            sty+=256
            num=str(ind).zfill(4)
            fname=filename
            if("/" in filename):
                fname=filename.split("/")[-1]
            fname="cropped_"+str(num)+"_"+fname
            CreateGeoTiff("cropped_images/"+fname,crop_image,geotrans,proj)
            # cv2.imwrite("cropped_images/"+filename, crop_image)
            ind+=1
        stx+=256

    for i in range(25):
        y=random.randint(0,mh-257)
        x=random.randint(0,mw-257)
        h=y+256
        w=x+256
        crop_image = image[:,x:w, y:h]
        num=str(ind).zfill(4)
        fname=filename
        if("/" in filename):
            fname=filename.split("/")[-1]
        fname="cropped_"+str(num)+"_"+fname
        CreateGeoTiff("cropped_images/"+fname,crop_image,geotrans,proj)
        ind+=1
    

    return (geotrans,proj,image)


def load_data(dir_path):
    image_list = []
    y_list = []
    for filename in sorted(os.listdir(dir_path)):
        if (filename.endswith(".tif")):
            make_crops(os.path.join(dir_path)+"/"+filename)
        



def load_tif(dir_path):
    image_list = []
    y_list = []
    global images
    num=0
    for filename in sorted(os.listdir(dir_path)):
        print(filename)
        if(num==5):
            break
        if filename.endswith(".tif"):
            filename=os.path.join(dir_path)+"/"+filename
            dataset = gdal.Open(filename)
            geotrans=dataset.GetGeoTransform()
            proj=dataset.GetProjection()
            image=dataset.ReadAsArray()
            print(image.shape,"***********")
            images.append(np.transpose(image))
            num+=1



dir_path="To_Uday-san_20220926"
load_data(dir_path)

# print(images.shape)




# new_dir="cropped_images"

# load_tif(new_dir)
# images=np.array(images)
# print(images.shape)
# train_generator = datagen.flow(images, batch_size=1)

# for i in range(2):
#     image_batch = train_generator.next()
#     image = image_batch[0].astype('uint8')
#     print(image)

# for img in images: 
#     stx=0;sty=0
#     image = cv2.imread(img)
#     print(image.shape)
#     mw,mh=image.shape[0],image.shape[1]
#     while(stx<mw-256):
#         sty=0
#         while(sty<mh-256):
#             crop_image = image[stx:stx+256, sty:sty+256]
#             sty+=256
#             num=str(ind).zfill(4)
#             filename="cropped_image_"+num+".png"
#             cv2.imwrite("cropped_images/"+filename, crop_image)
#             ind+=1
#             # cv2.waitKey(0)
#         stx+=256
    
#     rang=25
#     if(img=="data6.png"):
#         rang=200
#     for i in range(rang):
#         y=random.randint(0,mh-257)
#         x=random.randint(0,mw-257)
#         h=y+256
#         w=x+256
#         crop_image = image[x:w, y:h]
#         num=str(ind).zfill(4)
#         filename="cropped_image_"+num+".png"
#         cv2.imwrite("cropped_images/"+filename, crop_image)
#         ind+=1

# print(ind)