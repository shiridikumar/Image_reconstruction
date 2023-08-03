from osgeo import gdal, ogr
import numpy as np
import pandas as pd
import math
import os
def CreateGeoTiff(outRaster, data, geo_transform, projection):
        driver = gdal.GetDriverByName('GTiff')
        no_bands,rows,cols = data.shape
        DataSet = driver.Create(outRaster, cols, rows, no_bands, gdal.GDT_Float32)
        DataSet.SetGeoTransform(geo_transform)
        DataSet.SetProjection(projection)
        for i, image in enumerate(data, 1):
            # print(i,image)
            DataSet.GetRasterBand(i).WriteArray(image)
        DataSet.FlushCache()
        DataSet = None

def readTIF(path):
    dataset = gdal.Open(path)
    geotrans=dataset.GetGeoTransform()
    proj=dataset.GetProjection()
    image=dataset.ReadAsArray()
    return (geotrans,proj,image)

def calculate_rmse(original,dup):
    diff=(original-dup)**2
    return math.sqrt(np.sum(diff))




    
def interpolate(image):
    for i in range(image.shape[0]):
        df=pd.DataFrame(np.transpose(image[i,:,:]))
        print(sum(df.isnull().sum()))
        print(df.shape)
        df=df.interpolate(method='linear', limit_direction='both', axis=0)
        nan_in_df = df.isnull().sum()
        print(sum(nan_in_df))
        image[i,:,:]=np.transpose(df.values)
    return image


dir_path="striped_images"
try:
    os.system("rm -rf neighbhour_interpolated")
except:
    pass
os.system("mkdir neighbhour_interpolated")


for filename in sorted(os.listdir(dir_path)):
    if(not(filename.endswith(".tif"))):
        continue
    path=os.path.join(dir_path)+"/"+filename
    geo,proj,image=readTIF(path)
    image=interpolate(image)

    CreateGeoTiff("neighbhour_interpolated"+"/"+filename+"_interpolated.tif",image,geo,proj)



original="cropped_images"

def calculate_error(original,constructed):
    orig=sorted(os.listdir(original))
    dup=sorted(os.listdir(constructed))
    rmse=[]
    orig=list(filter(lambda x:x.endswith(".tif"), orig))
    dup=list(filter(lambda x:x.endswith(".tif"), dup))

    for x,y in zip(orig,dup):

        _,_,orig=readTIF(os.path.join(original)+"/"+x)
        _,_,cons=readTIF(os.path.join(constructed)+"/"+y)
        rmse.append(calculate_rmse(orig,cons))

    print(sum(rmse)/len(rmse),rmse)

calculate_error(original,"neighbhour_interpolated")


