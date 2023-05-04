from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

list_hrefs = []

def main():
    global list_hrefs
    coll_page = 100
    coll = 1
    while coll != coll_page:
      url=f"https://www.avito.ru/all/gruzoviki_i_spetstehnika/gruzoviki/new/samosval-ASgBAgICA0RUkAKIuw2sijTiwQ3gnDo?cd=1&p={coll}"
      get_sourse_url(url=url)
      coll += 1
      # print(url)
    with open("list_hrefs.txt", "w", encoding="utf-8") as file:
        for item in list_hrefs:
            file.write(item + "\n") 

def get_sourse_url(url):
    global list_hrefs
    s = Service("chromedriver/chromedriver")
    driver = webdriver.Chrome(service=s)
    driver.maximize_window()
   

    try:
        driver.get(url=url)
        time.sleep(1)
        element = driver.find_elements(By.CLASS_NAME, "iva-item-titleStep-pdebR")
        # element = driver.find_element(By.CLASS_NAME, "iva-item-titleStep-pdebR").find_element(By.CSS_SELECTOR, "a").get_attribute("href")
        for i in element:
            href = i.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            list_hrefs.append(href)
            # print(str(href))

    except Exception as _ex:
        print(_ex)
    finally:
        driver.close()
        driver.quit()
# with open("list_hrefs.txt", "w", encoding="utf-8") as file:
#         for item in list_hrefs:
#             file.write(item + "\n")
if __name__ == "__main__":
    main()