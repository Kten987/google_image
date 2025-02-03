from crawl_image import convert_productname, google_search
import pandas as pd
import time

def get_output(file_csv):
    input = pd.read_csv(file_csv)
    input = input[99:]
    i = 99
    for product in input["productName"]:
        product_name = convert_productname(product)
        output = google_search(product_name)
        output.to_csv(f"out_put_main_2/output_{i}.csv", index=False)
        i += 1
        time.sleep(3)

if __name__ == "__main__":
    get_output("image_review - basic routine - productName.csv")