import time
import warnings

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from utility import get_study_type, get_id, word_get, change_url
from utility import logmessage
from study import do_stduy

lm = logmessage("\n프로그램 시작")

account = get_id()
lm.log_message("ID/PW 불러오기 완료")

class_url = change_url()
lm.log_message("URL 불러오기 완료")

lm.log_message("크롬 드라이브를 불러오는 중...")
# 장치 동작하지않음 방지
options = webdriver.ChromeOptions()
options.add_argument("--mute-audio")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(
    service=Service(chromedriver_autoinstaller.install()), options=options)

lm.log_message("크롬 드라이브 불러오기 완료")

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
	lm.log_message("입력한 URL이 잘못되어 프로그램을 종료합니다")
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

lm.log_message('단어장 불러오는 중...')
word_dict = word_get(driver)
word_num = len(word_dict)
lm.log_message(f"word_dict: {word_dict}\n단어장 불러오기 완료")

while True:
	do_stduy(get_study_type(), driver, word_dict)
	driver.get(class_url)
	driver.get(class_url)
