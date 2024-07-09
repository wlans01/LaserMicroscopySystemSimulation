import numpy as np
import matplotlib.pyplot as plt
from const import Magnification, Camera

class OpticalSystem:
    def __init__(self, magnification):
        self.magnification = magnification
        self.img_array = self.load_image()
        self.real_width, self.real_height = self.calculate_real_dimensions()
        self.real_center = (self.real_width/2 , self.real_height/2)

    def load_image(self):
        array_file_path = self.magnification.value.file_name
        return np.load(array_file_path)

    def calculate_real_dimensions(self):
        width, height = Camera.Sensor_Size
        real_width = width * Camera.Pixel_Size / self.magnification.value.mag
        real_height = height * Camera.Pixel_Size / self.magnification.value.mag
        return real_width, real_height

    def draw_center_square(self, ax, size_um, show_coordinates=True):
        # 마이크로미터를 픽셀로 변환
        size_pixels = size_um * self.magnification.value.mag / Camera.Pixel_Size
        
        # 이미지 중심 계산
        center_x = self.real_width / 2
        center_y = self.real_height / 2
        
        # 정사각형의 좌표 계산
        half_size = size_um / 2
        left = center_x - half_size
        right = center_x + half_size
        top = center_y - half_size
        bottom = center_y + half_size
        
        # 정사각형 그리기
        square = plt.Rectangle((left, top), size_um, size_um, 
                               fill=False, edgecolor='red', linewidth=1)
        ax.add_patch(square)
        
        if show_coordinates:
            # 꼭짓점 좌표 표시
            corners = [(left, top), (right, top), (right, bottom), (left, bottom)]
            for i, (x, y) in enumerate(corners):
                ax.text(x, y, f'({x:.2f}, {y:.2f})', color='red', fontsize=8, 
                        ha='right' if i in [0, 3] else 'left', 
                        va='bottom' if i in [0, 1] else 'top')
        
        # 실제 크기 표시
        ax.text(right + 5, center_y, f'{size_um} µm', color='red', fontsize=10, 
                rotation=270, va='center')

    def display_image(self, square_size_um=10 ,show_square = False):
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.imshow(self.img_array, extent=[0, self.real_width, self.real_height, 0])
        if show_square:
            self.draw_center_square(ax, square_size_um)
        plt.show()

# 사용 예시
if __name__ == "__main__":
    optical_system = OpticalSystem(Magnification.X50)
    optical_system.display_image(show_square= True)


    

