import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from unidecode import unidecode

def get_data():
    browser = webdriver.Edge()
    browser.get("https://www.alza.sk/najpredavanejsie-najlepsie-notebooky/18842920.htm")
    desired_class = "name browsinglink"
    data = []
    for item in browser.find_elements(By.CLASS_NAME, "browsingitemcontainer"):
        products = item.find_elements(By.CLASS_NAME, desired_class.replace(" ", "."))
        prices = item.find_elements(By.CLASS_NAME, "price-box__price-text")

        for product, price in zip(products, prices):
            data.append({"Názov": product.text, "Cena": price.text})

    browser.quit()
    return data

def clean_data(df):
    df["Názov"] = df["Názov"].apply(lambda x: re.sub(r'\([^)]*\)', '', x))
    df["Názov"] = df["Názov"].apply(lambda x: x.split('+')[0].strip())
    df["Názov"] = df["Názov"].apply(lambda x: x.replace('"',""))
    df["Cena"] = df["Cena"].str.replace('"',"")

def create_and_export_dataframe(data, filename="output.csv"):
    df = pd.DataFrame(data)
    clean_data(df)
    df.sort_values(by="Názov", inplace=True)
    df.to_csv(filename, index=False, encoding="utf-8")

def main():
    data = get_data()
    create_and_export_dataframe(data)

if __name__ == "__main__":
    main()
