# Python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests
import os

# Cài đặt đường dẫn đến ChromeDriver
driver_path = 'path/to/chromedriver'
driver = webdriver.Chrome(driver_path)

# Mở trang Google Images với từ khóa tìm kiếm
search_query = 'skin1004 madagascar centella tone brightening cleansing gel foam'
driver.get(f'https://www.google.com/search?tbm=isch&q={search_query}')

# Tạo thư mục để lưu ảnh
if not os.path.exists('images'):
    os.makedirs('images')

# Tìm và nhấp vào từng ảnh để mở popup
thumbnails = driver.find_elements(By.CSS_SELECTOR, 'img.Q4LuWd')
for index, thumbnail in enumerate(thumbnails):
    try:
        thumbnail.click()
        time.sleep(2)  # Đợi popup mở

        # Lấy URL của ảnh chất lượng cao từ popup
        img_url = driver.find_element(By.CSS_SELECTOR, 'img.n3VNCb').get_attribute('src')

        # Tải ảnh về máy
        img_data = requests.get(img_url).content
        with open(f'images/image_{index}.jpg', 'wb') as handler:
            handler.write(img_data)
    except Exception as e:
        print(f'Error downloading image {index}: {e}')

# Đóng trình duyệt
driver.quit()