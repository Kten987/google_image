from botasaurus.request import request, Request
from botasaurus.soupify import soupify
from bs4 import BeautifulSoup
# import pandas as pd
# import json
import unidecode
import re


# convert product name sang dạng từ khóa, ví dụ: Pyunkang Yul Cleansing Foam -> Pyunkang+Yul+Cleansing+Foam 
def convert_productname(product_name):
    product_name = unidecode.unidecode(product_name)
    product_name = product_name.replace(" ", "+")
    return product_name

@request
def google_search(request: Request, product_name):
    url = "https://www.google.com/search?q=" + product_name + "&dpr=1&udm=2" 
    print(url)
    response = request.get(url)
    
    soup = BeautifulSoup(response.text, "html.parser")
    # ## Lưu ra file để xem cấu trúc html
    # with open("search_image_2.html", "w", encoding="utf-8") as file:
    #     file.write(str(soup))
    # Tìm tất cả các phần tử có thuộc tính data-docid
    data_docid_elements = soup.find_all(attrs={"data-docid": True})

    # Lấy giá trị của thuộc tính data-docid đầu tiên
    if data_docid_elements:
        first_data_docid = data_docid_elements[0]['data-docid']
        print(f'Giá trị của data-docid đầu tiên: {first_data_docid}')
    else:
        print('Không tìm thấy thuộc tính data-docid nào.')

    # Tìm tất cả các thẻ <script>
    scripts = soup.find_all('script')
    # Chuyển biến scripts sang string
    scripts_string = str(scripts)

    # # Lưu biến result ra file txt
    # with open("scripts_string.txt", "w", encoding="utf-8") as file:
    #     file.write(scripts_string)

    match = re.search(r'"hNWTX7gDx19p1M",\[([^]]+)\],\[([^]]+)\]', scripts_string)

    if match:
        values = match.group(2)
        result = values.split(',')[0].replace('"', '')
        print(result)
    else:
        print('Không tìm thấy nội dung trong hNWTX7gDx19p1M')
    
    # # Duyệt qua nội dung của các thẻ <script> để tìm đoạn chứa AWxQ3Y: [ ... ]
    # for script in scripts:
    #     if script.string:       
    #         match = re.search(r'AWxQ3Y:\s*\[(.*?)\]', script.string, re.DOTALL)
    #         if match:
    #             awxq3y_content = match.group(1)
    #             print(f'Nội dung trong AWxQ3Y: [{awxq3y_content}]')
    #             break
    # else:
    #     print('Không tìm thấy nội dung trong AWxQ3Y: [ ... ]')

    


if __name__ == "__main__":
    product_name = "9 Wishes Amazing Pine Ampule Serum"
    product_name = convert_productname(product_name)
    google_search(product_name)
    # print(product_name)

