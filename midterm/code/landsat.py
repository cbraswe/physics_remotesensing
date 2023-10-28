import rasterio

class Band():
    def __init__(self, number, file, mtl):
        self.number = number
        self.file = file
        band = rasterio.open(self.file)
        self.array = band.select(1)
        self.profile = band.profile
        self.mtl = mtl

    def convert_to_reflectance(self):
        return None
    
    def convert_to_radiance(self):
        return None
    