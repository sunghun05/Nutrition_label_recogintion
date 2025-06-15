import cv2
import pytesseract
import re
import os
import pandas as pd
from difflib import get_close_matches

# 🛠️ Windows용 Tesseract 설치 경로
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 🎯 추출 대상 키워드
keywords = [
    '나트륨', '탄수화물', '당류', '지방', '트랜스지방', '포화지방', '콜레스테롤', '단백질', '열량',
    'Total Fat', 'Saturated Fat', 'Trans Fat', 'Cholesterol', 'Sodium',
    'Total Carbohydrate', 'Sugars', 'Added Sugars', 'Protein', 'Calories', 'Dietary Fiber'
]

# 🧠 OCR 오탈자 보정 사전
corrections = {
    # 지방 계열
    "지 방": "지방",
    "트 랜 스 지 방": "트랜스지방",
    "트 랜 스 치 방": "트랜스지방",
    "포 화 지 방": "포화지방",
    "포 화 치 방": "포화지방",
    "포화지 방": "포화지방",
    "포화 치 방": "포화지방",

    # 콜레스테롤
    "콜 레 스 테 롤": "콜레스테롤",
    "콜 레 스 터 롤": "콜레스테롤",
    "콜레스 터롤": "콜레스테롤",

    # 나트륨
    "나 트 륨": "나트륨",
    "나 트륨": "나트륨",
    "나 트륨": "나트륨",

    # 탄수화물
    "탄 수 화 물": "탄수화물",
    "탄수 화물": "탄수화물",
    "총 탄 수 화 물": "탄수화물",
    "탄수화 물": "탄수화물",

    # 당류
    "당 뉼": "당류",
    "총 당 류": "당류",
    "총당 류": "당류",
    "당 류": "당류",
    "당율": "당류",

    # 단백질
    "단 뱍 질": "단백질",
    "단 백 칠": "단백질",
    "단 백 질": "단백질",
    "단백 칠": "단백질",

    # 열량 (칼로리)
    "칼 로 리": "열량",
    "총 칼 로 리": "열량",
    "열 량": "열량",
    "열향": "열량",

    # 영문 키워드 (대체)
    "Total Fat": "지방",
    "Trans Fat": "트랜스지방",
    "Saturated Fat": "포화지방",
    "Cholesterol": "콜레스테롤",
    "Sodium": "나트륨",
    "Total Carbohydrate": "탄수화물",
    "Sugars": "당류",
    "Added Sugars": "당류",
    "Dietary Fiber": "식이섬유",
    "Protein": "단백질",
    "Calories": "열량"
}


# 🔍 OCR 키워드 유사 보정 (선택사항)
def correct_keyword(word, keywords):
    matches = get_close_matches(word, keywords, n=1, cutoff=0.8)
    return matches[0] if matches else word

# 📦 이미지 한 장 분석
def extract_nutrition_from_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print(f"❌ 이미지 로딩 실패: {image_path}")
        return {}

    # 전처리
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 9, 75, 75)
    thresh = cv2.adaptiveThreshold(gray, 255,
                                   cv2.ADAPTIVE_THRESH_MEAN_C,
                                   cv2.THRESH_BINARY_INV, 15, 10)

    # OCR 수행
    text = pytesseract.image_to_string(thresh, lang='kor+eng')

    # 오타 보정
    for wrong, correct in corrections.items():
        text = text.replace(wrong, correct)

    print(f"\n📝 OCR 전체 텍스트 ({os.path.basename(image_path)}):\n{text}\n")

    result = {'파일명': os.path.basename(image_path)}

    # 텍스트 줄 단위 분석
    for line in text.split('\n'):
        lowered_line = line.lower()
        for key in keywords:
            if key.lower() in lowered_line:
                pattern = rf"{key}[^0-9\-]*(\d+\.?\d*)\s*(mg|g|kcal|%|mcg)?"
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    value = match.group(1)
                    unit = match.group(2) if match.group(2) else ''
                    result[key] = f"{value} {unit}".strip()

    print(f"✅ 추출 결과: {result}")
    return result

# 📁 폴더 내 이미지 일괄 처리
def process_folder(image_folder):
    data = []
    for file in os.listdir(image_folder):
        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            full_path = os.path.join(image_folder, file)
            info = extract_nutrition_from_image(full_path)
            data.append(info)

    df = pd.DataFrame(data)
    df.to_csv("nutrition_facts_result.csv", index=False, encoding='utf-8-sig')
    print("\n📦 CSV 저장 완료: nutrition_facts_result.csv")
    return df

# 🚀 메인
if __name__ == "__main__":
    folder_path = "./images"  # 여기에 이미지들 넣기
    df_result = process_folder(folder_path)
    print("\n📊 최종 데이터프레임:\n")
    print(df_result)
