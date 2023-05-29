from osgeo import gdal, ogr
import numpy as np
def CreateGeoTiff(self,outRaster, data, geo_transform, projection):
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


ans=readTIF("To_Uday-san_20220926/Area1_M3G20090621T025007_V01_RFL.IMG")
print(ans[2].shape)
