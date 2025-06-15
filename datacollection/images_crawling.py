from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import urllib.request
import os

def find_imgs(key_word, count):
    search_query = key_word + ' 영양정보표'
    save_dir = './dataset/images/train'
    os.makedirs(save_dir, exist_ok=True)

    driver = webdriver.Chrome()
    driver.set_window_size(1920, 1080)
    driver.get(f'https://www.google.com/search?q={search_query}&tbm=isch')

    time.sleep(2)

    # 1. 충분히 스크롤해서 이미지 많이 로드
    for _ in range(10):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

    # 2. 썸네일 한 번만 모두 수집
    thumbnails = driver.find_elements(By.CSS_SELECTOR, 'img.YQ4gaf')
    downloaded = set()

    for idx, thumbnail in enumerate(thumbnails):
        try:
            if thumbnail.get_attribute('class') == 'YQ4gaf zr758c wA1Bge' or thumbnail.get_attribute('class') == 'YQ4gaf zr758c':
                continue
            # 썸네일이 화면에 보이도록 스크롤
            driver.execute_script("arguments[0].scrollIntoView(true);", thumbnail)
            time.sleep(0.5)

            # 팝업이 열려 있으면 닫기
            try:
                close_btn = driver.find_element(By.CSS_SELECTOR, 'button.uj1Jfd.wv9iH.iM6qI')
                close_btn.click()
                time.sleep(0.5)
            except Exception:
                pass

            # 썸네일 클릭
            driver.execute_script("arguments[0].click();", thumbnail)
            time.sleep(1.5)

            # 고해상도 이미지 추출
            images = driver.find_elements(By.CSS_SELECTOR, 'img.sFlh5c.FyHeAf.iPVvYb')
            for image in images:
                src = image.get_attribute('src')
                if src and src.startswith('http') and src not in downloaded:
                    urllib.request.urlretrieve(src, f'{save_dir}/{count}.jpg')
                    downloaded.add(src)
                    count += 1
                    print(f"Downloaded: {src}")
                    break
            time.sleep(0.5)
            # 팝업 닫기
            try:
                close_btn = driver.find_element(By.CSS_SELECTOR, 'button.uj1Jfd.wv9iH.iM6qI')
                close_btn.click()
                time.sleep(0.5)
            except Exception:
                pass


        except Exception as e:
            print(f"Error at index {idx}: {e}")
            continue

    driver.quit()
    return count

if __name__ == "__main__":
    count = 3315
    foods = ['삼각김밥 ', '믹스커피 ', '젤리 ', '아이스크림 ', '3분짜장 ', '과자 ', '신라면 ', '카레 ', '3분짜장 ']
    for keyWord in foods:
        count = find_imgs(keyWord, count)
