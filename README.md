# 가상 피팅 SAMPLE - 202101951 김승연
## 기본 설명
> 2025.12.5일에 API키 소멸 예정!
* Gemini-nanobanana의 평균 출력속도 40s에 비해 월등히 상회. (첫 번째 cold start 이후 평균 10초)
* 상/하의 전부 가상 피팅 지원.
* 복잡한 배경에서도 무리 없이 가상 피팅 가능.
* AES 암호화를 통한 보호.
* API 지원

## Sample_output
* 남자 앉아있는 사진 의류 변경
<p align="center">
<img src="./sample_image/남자앉아있는사진.jpg" alt="남자 앉아있는 사진" width="20%" />
<img src="./sample_output/남자앉은사진_후드.webp" alt="남자 후드티 사진" width="20%" />
<img src="./sample_output/남자앉은사진_청바지.webp" alt="남자 청바지 사진" width="20%" />
<img src="./sample_output/남자앉은사진_빨간상의.webp" alt="남자 빨간상의 사진" width="20%" />
</p>

* 여성 의류 변경
<p align="center">
<img src="./sample_image/여자사진1.jpeg" alt="여성1 원본 사진" width="20%" />
<img src="./sample_output/여자1_치마.webp" alt="여성1 치마 변경" width="20%" />
<img src="./sample_image/여자사진2.jpeg" alt="여성2 원본 사진" width="20%" />
<img src="./sample_output/여자2__청바지.webp" alt="여성2 바지 변경" width="20%" />
</p>

## Usage
1. requirements.txt 설치  
    ```python
    pip install -r requirements.txt

2. sample_vto.py 설정 변경
    ```python
    class SampleVto:
    def __init__(self):
        self.api_key = "rpa_AB~~~"

        self.person_image_path = r"사람 사진의 경로를 입력해주세요 !!"
        self.clothes_image_path = r"옷 사진의 경로를 입력해주세요!"
        ...

3. 실행
    * 최상위 패키지에 "result.webp"로 저장됩니다.