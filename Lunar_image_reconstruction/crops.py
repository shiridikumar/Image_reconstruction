import random
import cv2
import os
import numpy as np
from osgeo import gdal, ogr
import numpy as np
# from tensorflow.keras.preprocessing.image import load_img
# from tensorflow.keras.preprocessing.image import img_to_array
# from tensorflow.keras.preprocessing.image import ImageDataGenerator

try:
    os.system("rm -rf cropped_images")
except:
    pass
os.system("mkdir cropped_images")


global images
images=[]
global ind
ind=0


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
        



# def load_tif(dir_path):
#     image_list = []
#     y_list = []
#     global images
#     num=0
#     for filename in sorted(os.listdir(dir_path)):
#         print(filename)
#         if(num==5):
#             break
#         if filename.endswith(".tif"):
#             filename=os.path.join(dir_path)+"/"+filename
#             dataset = gdal.Open(filename)
#             geotrans=dataset.GetGeoTransform()
#             proj=dataset.GetProjection()
#             image=dataset.ReadAsArray()
#             print(image.shape,"***********")
#             images.append(np.transpose(image))
#             num+=1



dir_path="To_Uday-san_20220926"
load_data(dir_path)


