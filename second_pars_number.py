from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import time
import pytesseract
from PIL import Image
import json
from random import randint
import random

def get_random_user_agents():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2564.109 Safari/537.36"
    ]
    return random.sample(user_agents, 5)

def setup_driver():
    chrome_options = webdriver.ChromeOptions()
    user_agents = get_random_user_agents()
    for user_agent in user_agents:
        chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-logging')
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--disable-popup-blocking')
    chrome_options.add_argument('--mute-audio')
    driver = webdriver.Chrome(options=chrome_options) # удаляем service и передаем chrome_options напрямую
    return driver
def main():    
    
    fin_dict = {}
    id_car = 0
    list_href = []
    time_random = randint(2, 5)

    with open('list_hrefs.txt', "r", encoding="utf-8") as file:
        list_href = [line.rstrip('\n') for line in file]

    # driver = setup_driver()

    try:
        for i in list_href[1:5]:
            try:
                driver = setup_driver()
                driver.maximize_window()
                driver.get(i)
                time.sleep(time_random) 
                title = driver.find_element(By.CLASS_NAME, "title-info-title-text").text 
                print(title)
                try:
                    img_element = driver.find_element(By.CLASS_NAME, "desktop-138s7sf")
                    img_element.click()
                    time.sleep(time_random)
                    element_to_save = driver.find_element(By.CLASS_NAME, "item-popup-phoneImage-adVhz")
                    img_url = element_to_save.get_attribute("src")
                    driver.get(img_url)
                    time.sleep(time_random)
                    png = driver.get_screenshot_as_png()
                    with open("image.jpg", "wb") as file:
                        file.write(png)
                    time.sleep(time_random)
                    image = Image.open('image.jpg')
                    text = pytesseract.image_to_string(image).rstrip("\n\f")
                    formatted_text = text.replace(" ", "").replace("-", "")
                    print(formatted_text)

                    fin_dict[id_car] = {
                        "phone": formatted_text,
                        "name_car": title,
                        "href": i
                        }
                    id_car += 1
                    driver.close()
                    
                except Exception as ex:
                    print(ex)
                    
            except Exception as ex:
                print(ex)
    finally:
        
        driver.quit()
    print(fin_dict)
    with open("finaly.json", "w", encoding="utf-8") as file:
        json.dump(fin_dict, file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()