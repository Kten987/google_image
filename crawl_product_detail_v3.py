from botasaurus.request import request, Request
from botasaurus.soupify import soupify
from bs4 import BeautifulSoup
import pandas as pd
import json

@request
def get_product_detail(request: Request, Link):
    clean_link = Link.replace(" ", "%20")
    # Create a URL
    url = "https://www.sephora.com" + clean_link
    # Navigate to the Omkar Cloud website
    response = request.get(url)

    rows = {}
    # Create a BeautifulSoup object    
    soup = soupify(response)
    #Lưu ra file để xem cấu trúc html
    # with open('sephora_product_v3_2.html', 'w', encoding='utf-8') as file:
    #     file.write(soup.prettify())

    # price = soup.find("span", class_="css-18jtttk").text.strip()
        
    # element_type = soup.find("div", class_="css-0", attrs={"data-at": "sku_name_label"})
    # if element_type is not None:
    #     type = element_type.text.strip()
    # else:
    #     type = "Not found"

    # element_volume = soup.find("span", class_="css-xm4yxq eanm77i0", attrs={"data-at": "sku_size_label"})
    # if element_volume is not None:
    #     volume = element_volume.text.strip()
    # else:
    #     volume = "Not found"

    
    # element_description = soup.find("div", class_="css-32uy52 eanm77i0")
    # if element_description is not None:
    #     description = element_description.text.strip()
    # else:
    #     description = "Not found"

    # ingredients_element = soup.find("div", id="ingredients")
    # if ingredients_element is not None:
    #     ingredients = ingredients_element.text.strip()
    # else:
    #     ingredients = "Not found"

    try:
        # Tìm đoạn script chứa thông tin sản phẩm
        json_str = soup.find(type='text/json').string
        # Chuyển đổi chuỗi JSON thành đối tượng Python
        data = json.loads(json_str)
        try: 
            ingredients_raw = data["page"]["product"]["currentSku"]["ingredientDesc"]
     
            ingredients = ingredients_raw.replace("<br>", "\n")
        except:
            ingredients = "Not found"
        
        try:
            description_raw = data["page"]["product"]["productDetails"]["longDescription"]

            description = description_raw.replace("<br>", "\n").replace("</b>", " ").replace("<b>", " ")
        except:
            description = "Not found"

        try:
            price = data["page"]["product"]["currentSku"]["listPrice"]
        except:
            price = "Not found"

        try:
            volume = data["page"]["product"]["currentSku"]["size"]
        except:
            volume = "Not found"

        rows = {
            'Link': Link,
            'price': price,
            #'type': type, # 'type' is the 'sku_name_label' in the html code, but it is not present in the html code of the product page I am scraping, so I am using 'type' as a placeholder for 'sku_name_label
            'volume': volume,
            'description_raw': description_raw,
            'description': description,
            'ingredients_raw': ingredients_raw, # 'ingredients_raw' is the 'ingredientDesc' in the html code, but it is not present in the html code of the product page I am scraping, so I am using 'ingredients_raw' as a placeholder for 'ingredientDesc
            'ingredients': ingredients
        }

    except:
        rows = {
            'Link': Link,
            'price': "Error",
            'volume': "Error",
            'description_raw': "Error",
            'description': "Error",
            'ingredients_raw': "Error",
            'ingredients': "Error"
        }


    df = pd.DataFrame(rows, index=[0], columns=['Link','price','volume', 'description_raw' ,'description', 'ingredients_raw' ,'ingredients'])
    df.to_csv('test_product_2.csv', index=False)
    # Save the data as a JSON file in output/scrape_heading_task.json
    return rows  

if __name__ == "__main__":
    get_product_detail("/product/glowmotions-P442821?skuId=2205359&icid2=products grid:p442821:product")

