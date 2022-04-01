from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import smtplib
import os

THRESHOLD_PRICE = 40
PRICE = 100
shop_name = ''
shop_link= ''
my_email = os.environ.get('EMAIL')
my_password = os.environ.get('PASSWORD')
url_list = [{'name':'Amazon',
             'url':'https://www.amazon.com/Horizon-Forbidden-West-Launch-PlayStation-5/dp/B09FBL24D5/ref=sr_1_1?keywords=forbidden+west+ps5&qid=1647360494&sprefix=forbi%2Caps%2C141&sr=8-1',
             'search_by': 'id',
             'element_value':'priceblock_ourprice'},
            {'name':'Target',
             'url':'https://www.target.com/p/horizon-forbidden-west-launch-edition-playstation-5/-/A-84290221?ref=tgt_adv_XS000000&AFID=google_pla_df&fndsrc=tgtao&DFA=71700000014844932&CPNG=PLA_Video%2BGames%2BShopping_Brand%7CVideo%2BGames_Ecomm_Hardlines&adgroup=SC_Video%2BGames&LID=700000001170770pgs&LNM=PRODUCT_GROUP&network=g&device=c&location=9033288&targetid=aud-1453399007976:pla-64523595581&ds_rl=1246978&ds_rl=1248099&gclid=Cj0KCQjw_4-SBhCgARIsAAlegrVEDAIbsz_0IVX0iFG0PFqLEepiV6VoTM08moUQKn6G4SdYdfdWP7kaAmlgEALw_wcB&gclsrc=aw.ds',
             'search_by':'class name',
             'element_value':'style__PriceFontSize-sc-1o3i6gc-0'},
            {'name':'Best_Buy',
             'url':'https://www.bestbuy.com/site/horizon-forbidden-west-launch-edition-playstation-5/6479468.p?skuId=6479468',
             'search_by':'xpath',
             'element_value':'/html/body/div[3]/main/div[2]/div[3]/div[2]/div/div/div[1]/div/div/div/div/div/div[1]/div/div/div/span[1]'}
            ]

for url in url_list:
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    # chrome_driver_path = Service("C:\SeleniumDrivers\chromedriver.exe") # local driver
    chrome_driver_path = Service("/usr/local/bin/chromedriver") # circleci driver.
    driver = webdriver.Chrome(service= chrome_driver_path, options=options)

    driver.maximize_window()
    driver.get(url=url['url'])
    #price = driver.find_element_by_id("priceblock_ourprice")
    time.sleep(4)
    ##### FOR BESTBUY ONLY#########
    # search_key= driver.find_element(By.CLASS_NAME, value='search-input').send_keys("forwhat its worth")
    # time.sleep(2)
    # click_item= driver.find_element(By.CSS_SELECTOR, value='#SignInToastCloseButton > svg').click()
    # time.sleep(2)
    ##############################
    try:
        price = driver.find_element(by= url['search_by'], value= url['element_value'])
    except NoSuchElementException:
        print(f'Element not found for {url["name"]}')
    else:
        game_price_float = float(price.text.split("$")[1])
        print(url['name'])
        print(game_price_float)
        time.sleep(3)
        if game_price_float < PRICE:
            PRICE = game_price_float
            shop_name = url['name']
            shop_link = url['url']
        driver.close()




if PRICE <= THRESHOLD_PRICE:
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(from_addr=my_email,
                            to_addrs="fahad.ahsan@gmail.com",
                            msg=f"Subject: Forbidden West Amazon Deal!!\n\n"
                                f"Horizon Forbidden West deal at {shop_name} for ${PRICE} now!\n"
                                f"{shop_link}")

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


