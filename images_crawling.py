from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import urllib.request
import os

search_query = 'nutrition labels on food'
save_dir = './dataset/images/train'
# os.makedirs(save_dir, exist_ok=True)

driver = webdriver.Chrome()
driver.set_window_size(1920, 1080)
driver.get(f'https://www.google.com/search?q={search_query}&tbm=isch')

time.sleep(2)
for _ in range(10):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

thumbnails = driver.find_elements(By.CSS_SELECTOR, 'img.YQ4gaf')
count = 0
for idx, thumbnail in enumerate(thumbnails):
    try:
        thumbnail.click()
        time.sleep(3)
        # 고해상도 이미지의 src 추출
        images = driver.find_elements(By.TAG_NAME, 'img')
        for image in images:
            src = image.get_attribute('src')
            if src and 'http' in src:
                urllib.request.urlretrieve(src, f'{save_dir}/{count}.jpg')
                count += 1
                break  # 한 번만 저장
        if count >= 100:  # 원하는 개수만큼 저장
            break
    except Exception as e:
        print(e)
        continue
driver.quit()