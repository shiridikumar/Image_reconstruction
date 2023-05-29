import tensorflow.compat.v1 as tf
import scipy
from scipy.ndimage import rotate
tf.disable_v2_behavior()
import os
from osgeo import gdal, ogr
import numpy as np
import random
global images ,geotrans,proj
images=[]
geotrans=[]
proj=[]
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

def readTIF(path):
    dataset = gdal.Open(path)
    print(dataset.RasterCount)
    geotrans=dataset.GetGeoTransform()
    proj=dataset.GetProjection()
    image=dataset.ReadAsArray()
    return (geotrans,proj,image)

"*** flip code "

def flip_image(path,image,geotrans,proj,dir="h"):
    if(dir=="h"):
        new_img=np.fliplr(image)
    else:
        new_img=image[:,::-1,:]
    dest_path=path
    if("/" in path):
        dest_path=path.split("/")[-1]
    dest_path="flipped_"+dir+"_"+dest_path
    return new_img
    # CreateGeoTiff(dest_path,new_img,geotrans,proj)


def rotateit(image, theta, isseg=False):
    order = 0 if isseg == True else 5
    return rotate(image, float(theta), reshape=False, order=order, mode='nearest')

def rotate_image(path,image,geotrans,proj,angle):
    image=np.transpose(image)
    new_img=rotateit(image,angle)
    new_img=np.transpose(new_img)
    dest_path=path
    if("/" in path):
        dest_path=path.split("/")[-1]
    dest_path="rotated_"+"_"+dest_path
    return new_img
    # CreateGeoTiff(dest_path,new_img,geotrans,proj)

def intensify_image(path,image,geotrans,proj,factor):
    new_img=image
    for i in range(image.shape[0]):
        prob=random.uniform(0,1)
        if(prob<0.5):
            new_img[i,:,:]=new_img[i,:,:]*float(factor)
    dest_path=path
    if("/" in path):
        dest_path=path.split("/")[-1]
    dest_path="intensity_"+dest_path
    return new_img
    # CreateGeoTiff(dest_path,new_img,geotrans,proj)


def translateit(image, offset, isseg=False):
    order = 0 if isseg == True else 5

    return scipy.ndimage.interpolation.shift(image, (int(offset[0]), int(offset[1]), 0), order=order, mode='nearest')


def translate_image(path,image,geotrans,proj,offset):
    image=np.transpose(image)
    new_img=translateit(image,offset)
    new_img=np.transpose(new_img)
    dest_path=path
    if("/" in path):
        dest_path=path.split("/")[-1]
    dest_path="translate_"+dest_path
    return new_img
    # CreateGeoTiff(dest_path,new_img,geotrans,proj)


def load_tif(dir_path):
    image_list = []
    y_list = []
    global images,geotrans,proj
    num=0
    for filename in sorted(os.listdir(dir_path)):
        print(filename)
        # if(num==5):
        #     break
        if filename.endswith(".tif"):
            filename=os.path.join(dir_path)+"/"+filename
            dataset = gdal.Open(filename)
            geotran=dataset.GetGeoTransform()
            pro=dataset.GetProjection()
            image=dataset.ReadAsArray()
            geotrans.append(geotran)
            proj.append(pro)
            print(image.shape,"***********")
            images.append(image)
            num+=1



path="cropped_images"

# geotrans,proj,image=readTIF(path)
# translate_image(path,image,geotrans,proj,[20,50])

load_tif(path)
ind=0
for i in range(len(images)):
    for j in range(5):
        prob=random.uniform(0,1)
        if(prob<0.75):
            dirp=random.uniform(0,1)
            if(dirp<0.5):
                dir="v"
            else:
                dir="h"
            images[i]=flip_image(path,images[i],geotrans[i],proj[i],dir)
        prob=random.uniform(0,1)
        if(prob<0.75):
            angle=random.randint(5,15)
            images[i]=rotate_image(path,images[i],geotrans[i],proj[i],angle)
        
        prob=random.uniform(0,1)
        if(prob<0.75):
            factor=random.uniform(0.001,0.003)
            images[i]=intensify_image(path,images[i],geotrans[i],proj[i],factor)
        prob=random.uniform(0,1)
        if(prob<0.75):
            vert=0
            vp=random.uniform(0,1)
            if(vp<0.5):
                vert=random.randint(int((2/100)*images[i].shape[1]),int((7/100)*images[i].shape[1]))
            hp=random.uniform(0,1)
            horz=0
            if(hp<0.5):
                horz=random.randint(int((2/100)*images[i].shape[2]),int((7/100)*images[i].shape[2]))
            images[i]=translate_image(path,images[i],geotrans[i],proj[i],[vert,horz])
        new_path="augmented_images/image_"
        num=str(ind).zfill(4)

        new_path=new_path+num+".tif"
        ind+=1
        CreateGeoTiff(new_path,images[i],geotrans[i],proj[i])
        print(ind,"********")

    

        



