from osgeo import gdal, ogr
import numpy as np
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
    print(dataset.RasterCount)
    geotrans=dataset.GetGeoTransform()
    proj=dataset.GetProjection()
    image=dataset.ReadAsArray()
    return (geotrans,proj,image)


ans=readTIF("To_Uday-san_20220926/Area1_MI_MAP_03_N22E196N21E197SC.tif")
# print(np.max(ans[2]),2**32-1)
# print(ans[2].shape)
# pixel=0
# for i in range(ans[2].shape[1]):
    # for j in range(ans[2].shape[2]):
        # if(np.sum(ans[2][:,i,j])!=0):
            # pixel+=1
print(ans[2].shape)
new=ans[2][:4,:,:]
CreateGeoTiff("temp.tif",new,ans[0],ans[1])
# print(2/100*(ans[2].shape[1]*ans[2].shape[2]),pixel)