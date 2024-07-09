import numpy as np
import matplotlib.pyplot as plt
from const import Magnification, Scan
from OpticalSystem import OpticalSystem
from ScanSystem import ScanSystem

def main():
    # 사용자 입력
    print("갈바노미터 스캐닝 시뮬레이션")
    print("사용 가능한 배율: 20X, 50X, 100X")
    mag_input = input("사용할 배율을 선택하세요 (20, 50, 100): ")
    
    # 배율 선택
    mag_dict = {'20': Magnification.X20, '50': Magnification.X50, '100': Magnification.X100}
    magnification = mag_dict.get(mag_input)
    if not magnification:
        print("잘못된 배율을 선택했습니다. 20X로 설정합니다.")
        magnification = Magnification.X20

    # 광학 시스템 및 스캔 시스템 초기화
    optical_system = OpticalSystem(magnification)
    scan_system = ScanSystem(optical_system)

    # 스캔 범위 설정
    scan_length = float(input(f"스캔 범위를 입력하세요 (µm, 최대 {int(optical_system.real_height)}): "))
    scan_length = min(scan_length, Scan.scan_length)
    scan_system.set_scan_length(scan_length)

    # 스캔 포인트 수 설정
    num_points = int(input(f"스캔 포인트 수를 입력하세요 (예: 100, 최대{scan_system.calculate_max_points()}): "))

    # 원본 이미지 표시
    optical_system.display_image(square_size_um=scan_length, show_square=True)

    # 스캔 수행
    print("스캔 중...")
    scan_data = scan_system.scan(num_points)

    # 스캔 결과 표시
    scan_system.display_scan_result(scan_data)

    # 스캔 데이터 저장
    # save_option = input("스캔 데이터를 저장하시겠습니까? (y/n): ")
    # if save_option.lower() == 'y':
    #     filename = input("저장할 파일 이름을 입력하세요 (확장자 제외): ")
    #     np.save(f"{filename}.npy", scan_data)
    #     print(f"스캔 데이터가 {filename}.npy로 저장되었습니다.")

if __name__ == "__main__":
    main()
