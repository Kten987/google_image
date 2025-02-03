from botasaurus.request import request, Request
from botasaurus.browser import browser, Driver
from botasaurus.soupify import soupify
from bs4 import BeautifulSoup
import pandas as pd
# import json
import unidecode
import re


# convert product name sang dạng từ khóa, ví dụ: Pyunkang Yul Cleansing Foam -> Pyunkang+Yul+Cleansing+Foam 
def convert_productname(product_name):
    product_name = 'customer images ' + product_name.lower() 
    product_name = unidecode.unidecode(product_name)
    product_name = product_name.replace(" ", "+")
    return product_name

@browser(
    block_images_and_css=True,
    close_on_crash=True,
    max_retry=3,
    reuse_driver=True,
    headless=True,
    output=None,
    parallel=10
)

def google_search(driver: Driver, product_name):

    url = "https://www.google.com/search?q=" + product_name + "&dpr=1&udm=2" 
    print(url)
    #response = requests.get(url, headers=headers, proxies=proxy_dict)
    response = driver.google_get(url)
    html_content = driver.page_html
    # ## Lưu ra file để xem cấu trúc html
    # with open("search_image_review_3.html", "w", encoding="utf-8") as file:
    #     file.write(str(html_content))

    soup = BeautifulSoup(html_content, "html.parser")
    # Chuyển html sang dạng text
    matches = soup.find_all(class_="mNsIhb")

    list_output = []
    for match in matches[:5]:
        match = match.find('img').get('src')
        list_output.append(match)

    df_output = pd.DataFrame([list_output], columns=[f'link_{i+1}' for i in range(5)])
    # df_output.to_csv("output.csv", index=False)
    return df_output
        

if __name__ == "__main__":
    product_name = "Adaferin Adapalene Gel 0.1%"
    product_name = convert_productname(product_name)
    google_search(product_name)
    # print(product_name)

