from botasaurus.request import request, Request
from botasaurus.soupify import soupify
from bs4 import BeautifulSoup
# import pandas as pd
# import json
import unidecode


# convert product name sang dạng từ khóa, ví dụ: Pyunkang Yul Cleansing Foam -> Pyunkang+Yul+Cleansing+Foam 
def convert_productname(product_name):
    product_name = unidecode.unidecode(product_name)
    product_name = product_name.replace(" ", "+")
    return product_name

@request
def google_search(request: Request, url):
    #url = "https://www.google.com/search?q=" + product_name + "&dpr=1&udm=2" + "#vhid=" + id + "&vssid=mosaic"
    # url = "https://www.google.com/search?q=9+Wishes+Amazing+Pine+Ampule+Serum&dpr=1&udm=2#vhid=hNWTX7gDx19p1M&vssid=mosaic"
    print(url)
    response = request.get(url)
    
    soup = BeautifulSoup(response.text, "html.parser")
    ## Lưu ra file để xem cấu trúc html
    with open("search_image_detail.html", "w", encoding="utf-8") as file:
        file.write(str(soup))
    # Tìm tất cả các phần tử có thuộc tính data-docid
    # data_docid_elements = soup.find_all(attrs={"data-docid": True})

    # # Lấy giá trị của thuộc tính data-docid đầu tiên
    # if data_docid_elements:
    #     first_data_docid = data_docid_elements[0]['data-docid']
    #     print(f'Giá trị của data-docid đầu tiên: {first_data_docid}')
    # else:
    #     print('Không tìm thấy thuộc tính data-docid nào.')


if __name__ == "__main__":
    url = "https://www.google.com/search?q=9+Wishes+Amazing+Pine+Ampule+Serum&dpr=1&udm=2#vhid=hNWTX7gDx19p1M&vssid=mosaic"
    google_search(url)
    # print(product_name)

