import numpy as np
import regex as re
from typing import List, Optional, Union

class Spectrometer():
    """This is a class for spectrometer information. 
    """
    def __init__(self, 
                 spectrometer_code: str,
                 wavelength_min: float, 
                 wavelength_max: float,
                 bandpass_descrip: Optional[str] = None,
                 model_descrip: Optional[str] = None):
        self.spectrometer_code = spectrometer_code
        self.wavelength_min = wavelength_min
        self.wavelength_max = wavelength_max
        self.bandpass_descrip = bandpass_descrip
        self.model_descrip = model_descrip
    
    def __repr__(self):
        return repr(f'{self.__class__.__name__}(spectrometer_code={self.spectrometer_code}, wavelength_min={self.wavelength_min},wavelength_max={self.wavelength_max},bandpass_descrip={self.bandpass_descrip},model_descrip={self.model_descrip})')

    def get_band_center(self): # unclear full direction this will take, so not calculating this upfront
        return self.wavelength_min/self.wavelength_max

class Sample():
    def __init__(self, 
                 data: np.array,
                 name: Optional[str] = None,
                 sample_id: Optional[str] = None,
                 record: Optional[int] = None, # unclear if this is always an int or a string or if there are multiple - recommend ignoring
                 purity: Optional[str] = None,
                 library: Optional[str] = None,
                 spectrometer: Optional[Spectrometer] = None):
        self.data = data
        self.name = name # not extracted in from_txt_file yet
        self.sample_id = sample_id # not extracted in from_txt_file yet
        self.record = record 
        self.purity = purity
        self.library = library 
        self.spectrometer = spectrometer

    @classmethod
    def from_txt_file(cls, aref_file: str, microns_file: str, spectrometers: Union[Spectrometer, List[Spectrometer]]):
        params = {}
        sample = open(aref_file).read().split('\n') 
        header = sample[0] # extract spectrometer info from the header 
        lib = header.strip().split(' ')[0] # the first info is the Spectral Library
        params['library'] = lib[:-1] 
        params['purity'] = lib[-1] # the last digit is the purity
        record = re.search('(?<=Record=)\d+', header).group() 
        params['record'] = int(record) if record else None
        data = np.array([float(x) for x in sample[1:] if x])

        if isinstance(spectrometers, list):
            spectrometer = next((spec for spec in spectrometers if spec.spectrometer_code in header)) # only one match
        else:
            spectrometer = spectrometers # a single spectrometer provided
        
        wavelengths = sample = open(microns_file).read().split('\n') 
        wavelengths = np.array([float(x) for x in wavelengths[1:] if x])
        data = np.vstack((wavelengths, data))
        bad_data = -1.2300000e+34 # this is a known
        data = data[:, np.all(data != bad_data, axis=0)]
        return cls(data=data, 
                   spectrometer=spectrometer if spectrometer else None,
                   **params)

    def __repr__(self):
        # maybe we go back and add in some minimal representation of the data array
        return repr(f'{self.__class__.__name__}(data=truncd{self.data[:2, :2]},name={self.name},sample_id={self.sample_id},record={self.record},purity={self.purity},library={self.library},spectrometer={self.spectrometer})')

        