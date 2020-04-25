import ee
import numpy

def earthengine2images(
    data_source,
    date_range,
    cloud_cover,
    bands,
    region_coords,
    enhance=True
):
    ee.Initialize()
    
    start_date, end_date = date_range
    # region geometry from coordinates
    region = ee.Geometry.Rectangle(
        region_coords
    )
    # select ImageCollection
    img_series = ee.ImageCollection(
        data_source
    ).filterDate(
        start_date, end_date
    ).filterBounds(
        region
    ).filter(
        ee.Filter.lt("CLOUD_COVER", cloud_cover)
    ).select(
        list(bands.values())
    )
     
    img_series = img_series.toList(img_series.size())
    series_length = img_series.size().getInfo()
    # convert to image arrays
    img_arrays = []
    for i in range(series_length):
        band_arrays = [
            numpy.array(
                ee.Image(
                    img_series.get(i)
                ).sampleRectangle(
                    region=region,
                    defaultValue=0
                ).get(
                    bands[color]
                ).getInfo() 
            )
            for color in ("R", "G", "B")
        ]
        band_arrays = [numpy.expand_dims(band_array, 2) for band_array in band_arrays]
        img = numpy.concatenate(band_arrays, 2)
        img_arrays.append(img)
        
    if enhance:
        
        def normalize(data):
            '''
            Normalize the data from 0->1
            '''
            norm = (data-data.min())/(data.max()-data.min())
            return norm
        
        img_arrays = [normalize(img_array) for img_array in img_arrays]
    return img_arrays