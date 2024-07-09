# const.py
# 상수 값들 저장
from enum import Enum
from typing import NamedTuple

class Camera:
    Pixel_Size = 2.2
    Sensor_Size = (1792, 1024)

class MagInfo(NamedTuple):
    mag: int
    file_name: str

class Magnification(Enum):
    X20 = MagInfo(20, "image_array.npy")
    X50 = MagInfo(50, "image_array2.5.npy")
    X100 = MagInfo(100, "image_array5.npy")

    @classmethod
    def get_image_path(cls, mag):
        for m in cls:
            if m.value.mag == mag:
                return m.value.file_name
        raise ValueError(f"Unsupported magnification: {mag}")
    

class Scan:
    scaling_factor = 0.8
    sample_distance = 1000  
    real_sample_distance = 1000  
    scan_length = 10