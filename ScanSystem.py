import numpy as np
import matplotlib.pyplot as plt
from const import Scan, Magnification
from OpticalSystem import OpticalSystem

class ScanSystem:
    def __init__(self, optical_system):
        self.optical_system = optical_system
        self.scan_length = Scan.scan_length
        self.scaling_factor = Scan.scaling_factor
        self.sample_distance = Scan.sample_distance
        self.real_sample_distance = Scan.real_sample_distance

    def set_scan_length(self,scan_length):
        self.scan_length = scan_length

    def um_to_voltage(self, x_um, y_um):
        # 실제 길이를 전압으로 변환
        # 설정한 샘플과의 거리로 조정
        x_angle = np.arctan(x_um / (self.sample_distance )) * 180 / np.pi
        y_angle = np.arctan(y_um / (self.sample_distance )) * 180 / np.pi
        
        x_voltage = x_angle * self.scaling_factor
        y_voltage = y_angle * self.scaling_factor
        
        return np.clip(x_voltage, -10, 10), np.clip(y_voltage, -10, 10)

    def voltage_to_um(self, x_voltage, y_voltage):
        # 전압을 실제 길이로 변환
        x_angle = x_voltage / self.scaling_factor
        y_angle = y_voltage / self.scaling_factor
        
        # 실제 샘플과의 거리로 조정
        x_um = np.tan(x_angle * np.pi / 180) * self.real_sample_distance 
        y_um = np.tan(y_angle * np.pi / 180) * self.real_sample_distance 
        
        return x_um, y_um
    
    def read(self,x_v,y_v):
        # 입력된 접압을 이미지의 해당픽셀위치로 변환
        img_x, img_y = self.voltage_to_image_coordinates(x_v, y_v)

        # 픽셀의 경우 실수는 불가능하기 떄문에 정수로 변경
        # 해당 위치의 RGB값이 나옴
        return self.optical_system.img_array[int(img_y), int(img_x),:]


    def write(self,voltage):
        # DAQ 입력 따라하기 
        pass

    def scan(self, num_points=100):
        if not self.check_galvo_parameters(num_points):
            return None
    
        half_length = self.scan_length / 2
        x_positions = np.linspace(-half_length, half_length, num_points)
        y_positions = np.linspace(-half_length, half_length, num_points)
        
        scan_data = np.zeros((num_points, num_points,3))
        
        for i, x in enumerate(x_positions):
            for j, y in enumerate(y_positions):
                x_v, y_v = self.um_to_voltage(x, y)

                # DAQ에 신호 입력
                self.write([x_v,y_v])

                # DAQ로부터 신호 받기
                scan_data[j, i,:] = self.read(x_v,y_v)
                
        
        return scan_data

    def voltage_to_image_coordinates(self, x_v, y_v):
        x_um, y_um = self.voltage_to_um(x_v, y_v)
        img_width, img_height = self.optical_system.img_array.shape[1], self.optical_system.img_array.shape[0]
        x_pixel = ((self.optical_system.real_center[0] + x_um) / self.optical_system.real_width) * img_width
        y_pixel = ((self.optical_system.real_center[1] + y_um) / self.optical_system.real_height) * img_height
        
        return np.clip(x_pixel, 0, img_width), np.clip(y_pixel, 0, img_height)
    
    def check_galvo_parameters(self, num_points):
        # 갈보미터 각도 분해능 (사양에 따라 조정 필요)
        galvo_resolution_deg = 0.0008  # 예: 0.0008도 (15 µrad)

        # 스캔 길이에 해당하는 최대 각도 계산
        max_angle_deg = np.arctan(self.scan_length / (2 * self.sample_distance)) * 180 / np.pi

        # 한 스텝당 각도
        step_angle_deg = 2 * max_angle_deg / (num_points - 1)

        # 한 스텝당 실제 길이 (um)
        step_size_um = self.scan_length / (num_points - 1)

        # num_points의 유효성 검사
        if step_angle_deg < galvo_resolution_deg:
            print(f"Warning: Requested angular step ({step_angle_deg:.6f}°) is smaller than the galvo resolution ({galvo_resolution_deg:.6f}°).")
            max_points = int(2 * max_angle_deg / galvo_resolution_deg) + 1
            print(f"Maximum number of points for this scan length: {max_points}")
            return False

        print(f"Galvo angular resolution: {galvo_resolution_deg:.6f}°")
        print(f"Maximum scan angle: ±{max_angle_deg:.4f}°")
        print(f"Angular step size: {step_angle_deg:.6f}°")
        print(f"Spatial step size: {step_size_um:.4f} µm")
        print(f"Number of points: {num_points}")

        return True
    
    def calculate_max_points(self, scan_length=None):
        if scan_length is None:
            scan_length = self.scan_length

        # 갈보미터 각도 분해능 (사양에 따라 조정 필요)
        galvo_resolution_deg = 0.0008  # 예: 0.0008도 (15 µrad)

        # 스캔 길이에 해당하는 최대 각도 계산
        max_angle_deg = np.arctan(scan_length / (2 * self.real_sample_distance)) * 180 / np.pi

        # 최대 포인트 수 계산
        max_points = int(2 * max_angle_deg / galvo_resolution_deg) + 1

        return max_points

    def display_scan_result(self, scan_data):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # 스캔 영역 계산
        half_length = self.scan_length / 2
        center_x = self.optical_system.real_width / 2
        center_y = self.optical_system.real_height / 2
        
        # 픽셀 단위로 스캔 영역 계산
        pixel_width = self.optical_system.img_array.shape[1]
        pixel_height = self.optical_system.img_array.shape[0]
        pixel_scan_length = int(self.scan_length / self.optical_system.real_width * pixel_width)
        
        start_x = int(center_x / self.optical_system.real_width * pixel_width - pixel_scan_length / 2)
        start_y = int(center_y / self.optical_system.real_height * pixel_height - pixel_scan_length / 2)
        end_x = start_x + pixel_scan_length
        end_y = start_y + pixel_scan_length
        
        # 이미지 크롭
        cropped_img = self.optical_system.img_array[start_y:end_y, start_x:end_x]
        
        # 크롭된 원본 이미지 표시
        ax1.imshow(cropped_img, extent=[center_x - half_length, center_x + half_length,
                                        center_y + half_length, center_y - half_length])
        ax1.set_title("Cropped Original Image")
        
        data_min, data_max = scan_data.min(), scan_data.max()
        # 데이터를 최대값으로 나누어 [0, 1] 범위로 정규화
        normalized_data = scan_data / data_max
        
        # 스캔 결과 표시
        im = ax2.imshow(normalized_data, extent=[0, self.scan_length, self.scan_length, 0])
        ax2.set_title("Scan Result")
        plt.show()

if __name__ == "__main__":
    optical_system = OpticalSystem(Magnification.X50)
    scan_system = ScanSystem(optical_system)
    
    scan_data = scan_system.scan(num_points=100)

    scan_system.display_scan_result(scan_data)