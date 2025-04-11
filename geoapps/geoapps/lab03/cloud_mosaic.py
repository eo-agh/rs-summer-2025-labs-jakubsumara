def create_cloud_free_mosaic(aoi, start_date, end_date):
    def mask_qa60(image):
        qa = image.select('QA60')
        cloud_bit_mask = 1 << 10
        shadow_bit_mask = 1 << 11
        mask = qa.bitwiseAnd(cloud_bit_mask).eq(0).And(
               qa.bitwiseAnd(shadow_bit_mask).eq(0))
        return image.updateMask(mask).copyProperties(image, ["system:time_start"])

    s2 = (
        ee.ImageCollection('COPERNICUS/S2_SR')
        .filterBounds(aoi)
        .filterDate(start_date, end_date)
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
        .map(mask_qa60)
        .map(lambda img: img.clip(aoi))
    )

    mosaic = s2.median().clip(aoi)
    return mosaic