from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import smtplib
import os

THRESHOLD_PRICE = 40
my_email = os.environ.get("EMAIL")
my_password = os.environ.get("PASSWORD")
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
#chrome_driver_path = Service("C:\SeleniumDrivers\chromedriver.exe") # local driver
chrome_driver_path = Service("/usr/local/bin/chromedriver") # circleci driver.
driver = webdriver.Chrome(service= chrome_driver_path, chrome_options=options)

driver.maximize_window()
driver.get(url="https://www.amazon.com/Horizon-Forbidden-West-Launch-PlayStation-5/dp/B09FBL24D5/ref=sr_1_1?keywords=forbidden+west+ps5&qid=1647360494&sprefix=forbi%2Caps%2C141&sr=8-1")
#price = driver.find_element_by_id("priceblock_ourprice")
time.sleep(2)
price = driver.find_element(by="id", value="priceblock_ourprice")
#price = driver.find_element(By.XPATH, value='//*[@id="priceblock_ourprice"]')
# print(price.text)
game_price_float = float(price.text.split("$")[1])
print(game_price_float)
search_bar = driver.find_element(by="id",value="twotabsearchtextbox")
print(search_bar.get_attribute("value"))
time.sleep(3)


if game_price_float <= THRESHOLD_PRICE:
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(from_addr=my_email,
                            to_addrs="fahad.ahsan@gmail.com",
                            msg=f"Subject: Forbidden West Amazon Deal!!\n\n"
                                f"Horizon Forbidden West deal for ${game_price_float} now!")

    print("Email Sent")
# driver.find_element(By.CSS_SELECTOR, '#landingImage').click()
# time.sleep(2)
# driver.find_element(By.CSS_SELECTOR, '#a-popover-5 > div > header > button > i').click()
# time.sleep(2)
# driver.find_element(By.CSS_SELECTOR, '#a-autoid-12-announce > div > div.twisterTextDiv.text > p').click()
# time.sleep(2)
# driver.find_element(By.CSS_SELECTOR, '.a-button-input').click()
# time.sleep(2)
# item_added = driver.find_element(By.CSS_SELECTOR, "#sw-atc-details-single-container > div.a-section.a-padding-medium.sw-atc-message-section > div.a-section.a-spacing-none.a-padding-none > span")
# print(item_added.text)

driver.close()


