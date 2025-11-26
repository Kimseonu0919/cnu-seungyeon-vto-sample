import os
import io
import time
import base64

import requests
from PIL import Image, ImageOps

class SampleVto:
    def __init__(self):
        #################### || 설정 항목 - 나머지는 건드릴 필요 없습니다|| ##########################
        self.api_key = "API_KEY값을 입력하세요!"

        self.person_image_path = r"사람 이미지의 경로를 입력하세요!"
        self.clothes_image_path = r"옷 이미지의 경로를 입력하세요!"
        ###########################################################################################
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_yaml_path = os.path.join(base_dir, 'config', 'config.yaml')
    
    def __encode_image_optimized(self, image_path, max_size=1024):
        """ 
        이미지를 EXIF 회전 후, 긴 변 기준 1280px로 리사이징하여 Lossless WebP로 변환 
        (가상 피팅용 의류 디테일 보존 최적화)
        """
        if not os.path.exists(image_path):
            print(f"[ERROR] 파일 없음: {image_path}")
            return None
            
        try:
            with Image.open(image_path) as img:
                # EXIF 정보 기반 회전
                img = ImageOps.exif_transpose(img)
                
                # 투명 배경(RGBA) 처리 로직 추가
                if img.mode == 'RGBA':
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[3]) # Alpha channel을 마스크로 사용
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert("RGB")

                # 스마트 리사이징 (AI 모델 친화적 크기 계산)
                width, height = img.size
                if max(width, height) > max_size:
                    scale_ratio = max_size / max(width, height)
                    new_width = int(width * scale_ratio)
                    new_height = int(height * scale_ratio)
                    
                    # 너비/높이를 16의 배수로 맞추면 VAE 인코딩 속도/품질이 미세하게 향상됨 (선택사항)
                    new_width = new_width - (new_width % 16)
                    new_height = new_height - (new_height % 16)

                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                buffer = io.BytesIO()
                img.save(buffer, format="WEBP", lossless=True)
                
                return base64.b64encode(buffer.getvalue()).decode('utf-8')

        except Exception as e:
            print(f"[ERROR] 이미지 인코딩 실패: {e}")
            return None
    
    def run(self):
        "모델 구동하는 함수"
        url = f"https://api.runpod.ai/v2/rinftbo7n36eg8/runsync"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        print("WEBP 변환 중...")
        img1_b64 = self.__encode_image_optimized(self.person_image_path)
        img2_b64 = self.__encode_image_optimized(self.clothes_image_path)

        if not img1_b64 or not img2_b64:
            print("이미지 변환 실패")
            exit()

        payload = {
            "input": {
                "image_1": img1_b64,
                "image_2": img2_b64
            }
        }

        print(f"모델 구동 시작...")
        start_req = time.time()

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=120)
            response.raise_for_status()
            result = response.json()
            end_req = time.time()
            
            status = result.get('status')
            if status == 'COMPLETED':
                total_time = end_req - start_req
                print(f"성공! || 총 소요 시간: {total_time:.2f}초")
                
                output_b64 = result['output']['result_image']
                output_filename = "result.webp"
                
                with open(output_filename, "wb") as f:
                    f.write(base64.b64decode(output_b64))
                print(f"결과 저장 완료: {output_filename}")
            elif status == 'FAILED':
                print("실패:", result.get('error'))
            else:
                print(f"상태: {status}")
            
        except Exception as e:
            print(f"에러: {e}")

if __name__ == "__main__":
    sample_vto = SampleVto()
    sample_vto.run()
