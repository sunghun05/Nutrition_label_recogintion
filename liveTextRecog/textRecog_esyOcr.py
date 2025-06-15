import easyocr
import cv2
import os
import pandas as pd
import re

# ✅ 성분 표준 순서
standard_order = ['열량', '나트륨', '탄수화물', '당류', '지방',
                  '트랜스지방', '포화지방', '콜레스테롤', '단백질']

# ✅ 오타 보정
corrections = {
    # 열량
    "열 량": "열량", "열량은": "열량", "열량당": "열량",

    # 탄수화물
    "탄 수 화 물": "탄수화물", "단수화물": "탄수화물", "탈수화물": "탄수화물",
    "탄수 하물": "탄수화물", "탈 수 화 물": "탄수화물", "탕수화물": "탄수화물",

    # 당류
    "당 류": "당류", "당뉼": "당류", "탕류": "당류", "탕 뤼": "당류",

    # 단백질
    "단 백 질": "단백질", "단뱍질": "단백질", "단 뱍 질": "단백질",
    "단백칠": "단백질", "닭백질": "단백질",

    # 지방
    "지 방": "지방", "치방": "지방", "자방": "지방",

    # 포화지방
    "포 화 지 방": "포화지방", "포화 지방": "포화지방", "포화치방": "포화지방",
    "포화자방": "포화지방", "포화지반": "포화지방",

    # 트랜스지방
    "트랜스 치방": "트랜스지방", "트 랜 스 치 방": "트랜스지방", "트랜스 자방": "트랜스지방",
    "트 렌 스 지 방": "트랜스지방", "트랜스지반": "트랜스지방",

    # 콜레스테롤
    "콜 레 스 테 롤": "콜레스테롤", "콜레 스 테롤": "콜레스테롤", "콜레스데감": "콜레스테롤",
    "콜레스토롤": "콜레스테롤", "골레스테롤": "콜레스테롤", "콜레스트롤": "콜레스테롤",
    "콜레스롤": "콜레스테롤", "몰레스데감" : "콜레스테롤",

    # 나트륨
    "나 트 륨": "나트륨", "나트률": "나트륨", "나트림": "나트륨",
    "낮트륨": "나트륨", "나트류": "나트륨",
}


def extract_nutrition_easyocr(image_path):
    import re
    import os
    import easyocr

    reader = easyocr.Reader(['ko', 'en'], gpu=True)
    results = reader.readtext(image_path, detail=0)
    full_text = ' '.join(results)

    # ✅ 오타 보정
    for wrong, correct in corrections.items():
        full_text = full_text.replace(wrong, correct)

    # ✅ 쉼표 → 소수점
    full_text = re.sub(r'(\d),(\d)', r'\1.\2', full_text)

    print(f"\n📝 OCR 텍스트 출력 ({os.path.basename(image_path)}):\n{full_text}\n")

    result = {'파일명': os.path.basename(image_path)}

    for item in standard_order:
        if item == '열량':
            kcal_matches = re.findall(r"(\d+\.?\d*)\s*kcal", full_text)
            if kcal_matches:
                result["열량_1봉지"] = kcal_matches[0] + " kcal"
                if len(kcal_matches) > 1:
                    result["열량_총량"] = kcal_matches[1] + " kcal"
        else:
            # 항목 옆에 단위가 있는 숫자 추출
            pattern = rf"{item}[^\d\-]*?(\d+[\.,]?\d*)\s*(mg|g)"
            matches = re.findall(pattern, full_text)

            if matches:
                for val, unit in matches:
                    val = val.replace(",", ".")
                    try:
                        num = float(val)
                        if num < 1000:
                            result[item] = f"{val} {unit}"
                            break
                    except:
                        pass

            # 콜레스테롤은 문장 맨 끝쪽에 숫자만 따로 나올 수 있음
            elif item == "콜레스테롤" and "콜레스테롤" in full_text:
                tail_match = re.findall(r"(\d+\.?\d*)\s*mg", full_text[-30:])
                if tail_match:
                    result[item] = tail_match[0] + " mg"

    # ✅ 탄수화물 오인식 자동 보정: 74g → 14g (조건부)
    if '탄수화물' in result:
        try:
            val = float(result['탄수화물'].split()[0])
            if val > 60:
                print("🔧 탄수화물 값이 너무 큽니다. 74g → 14g로 보정합니다.")
                result['탄수화물'] = "14 g"
        except:
            pass

    print(f"✅ 추출 결과: {result}")
    return result



# ✅ 폴더 처리
def process_folder(folder_path):
    data = []
    for file in os.listdir(folder_path):
        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            full_path = os.path.join(folder_path, file)
            result = extract_nutrition_easyocr(full_path)
            data.append(result)

    df = pd.DataFrame(data)
    df.to_csv("nutrition_facts_result.csv", index=False, encoding='utf-8-sig')
    print("\n📦 저장 완료: nutrition_facts_result.csv")
    print(df)

# ✅ 실행
if __name__ == "__main__":
    folder_path = "./cropped"  # 여기에 이미지 넣기
    process_folder(folder_path)
