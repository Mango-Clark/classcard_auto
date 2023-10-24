import time
import warnings

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from utility import get_study_type, get_id, word_get, change_url, log_header
from study import do_stduy

DO_LOGGING = True

warnings.filterwarnings("ignore", category=DeprecationWarning)

account = get_id()

if DO_LOGGING:
	with open('.log', 'a', encoding='utf-8') as log:
		log.write(f'\n\n\n{log_header()}프로그램 시작\n{log_header()}ID/PW 불러오기 완료\n')

class_url = change_url()

if DO_LOGGING:
	with open('.log', 'a', encoding='utf-8') as log:
		log.write(f'{log_header()}URL 불러오기 완료\n')

print("크롬 드라이브를 불러오고 있습니다 잠시만 기다려주세요!")

if DO_LOGGING:
	with open('.log', 'a', encoding='utf-8') as log:
		log.write(f'{log_header()}크롬 드라이브를 불러오는 중\n')

# 장치 동작하지않음 방지
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=Service(chromedriver_autoinstaller.install()), options=options)

# Login
if DO_LOGGING:
	with open('.log', 'a', encoding='utf-8') as log:
		log.write(f'{log_header()}크롬 드라이브 불러오기 완료\n')

driver.get("https://www.classcard.net/Login")
tag_id = driver.find_element(by=By.ID, value="login_id")
tag_pw = driver.find_element(by=By.ID, value="login_pwd")
tag_id.clear()
tag_id.send_keys(account["id"])
tag_pw.send_keys(account["pw"])
driver.find_element(
    by=By.CSS_SELECTOR,
    value="#loginForm > div.checkbox.primary.text-primary.text-center.m-t-md > button",
).click()

try:
	time.sleep(1)
	driver.get(class_url)
	driver.get(class_url)
	driver.find_elements(By.XPATH, "//div[@class='p-b-sm']")
except:
	print("\n입력한 URL이 잘못되어 프로그램을 종료합니다\n")
	input("종료하려면 아무 키나 누르세요...")
	quit()
time.sleep(1)

driver.find_element(
    by=By.XPATH,
    value='/html/body/div[1]/div[4]/div[3]/div[2]/div',
).click()
time.sleep(0.1)
driver.find_element(
    by=By.XPATH,
    value='/html/body/div[1]/div[4]/div[3]/div[2]/div/ul/li[1]/a',
).click()

word_dict = word_get(driver)
word_num = word_dict['word_num']
if DO_LOGGING:
	with open('.log', 'a', encoding='utf-8') as log:
		log.write(f'{log_header()}word_dict: ')
		log.write(str(word_dict))
		log.write('\n')

while True:
	do_stduy(get_study_type(), driver, word_dict, DO_LOGGING)
	driver.get(class_url)
	driver.get(class_url)
