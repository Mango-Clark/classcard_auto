import time
import warnings
import re
import traceback

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
)
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# 함수불러오기
from utility import chd_wh, get_id, word_get, change_url

warnings.filterwarnings("ignore", category=DeprecationWarning)

account = get_id()

class_site = change_url()

ch_d = chd_wh()

print("크롬 드라이브를 불러오고 있습니다 잠시만 기다려주세요!")

# 장치 동작하지않음 방지
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=Service(chromedriver_autoinstaller.install()), options=options)

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
	driver.get(class_site)
	driver.get(class_site)
	driver.find_elements(By.XPATH, "//div[@class='p-b-sm']")
except:
	print("\n입력한 URL이 잘못되어 프로그램을 종료합니다\n")
	input("종료하려면 아무 키나 누르세요...")
	quit()
time.sleep(1)

word_dict = word_get(driver)
word_num = word_dict['word_num']

while True:
	if ch_d == 1:
		driver.find_element(
		    by=By.CSS_SELECTOR,
		    value=
		    "body > div.bottom-fixed > div > div.cc-table.fill-parent.m-t > div.font-0.pos-relative > div:nth-child(1)",
		).click()
		time.sleep(2)
		driver.find_element(
		    by=By.CSS_SELECTOR,
		    value="#wrapper-learn > div.start-opt-body > div > div > div > div.m-t > a",
		).click()

		unknown_count = word_num

		while unknown_count > 1:
			time.sleep(3)
			driver.find_element(
			    by=By.XPATH,
			    value='//*[@id="wrapper-learn"]/div[1]/div/div[3]/div[1]/a',
			).click()
			time.sleep(0.5)
			driver.find_element(
			    by=By.XPATH,
			    value='//*[@id="wrapper-learn"]/div[1]/div/div[3]/div[2]/a',
			).click()
			unknown_count = int(
			    driver.find_element(
			        by=By.XPATH,
			        value='//*[@id="wrapper-learn"]/div[1]/div/div[1]/span[3]/span',
			    ).get_attribute('innerText'))
			print(f"남은 단어 수: {unknown_count}")
		time.sleep(1)
		driver.find_element(
		    by=By.CSS_SELECTOR,
		    value="body > div.study-header-body > div > div:nth-child(1) > div:nth-child(1) > a",
		).click()
		print("암기가 끝났습니다.")
	elif ch_d == 2:
		driver.find_element(
		    by=By.CSS_SELECTOR,
		    value=
		    "body > div.bottom-fixed > div > div.cc-table.fill-parent.m-t > div.font-0.pos-relative > div:nth-child(2)",
		).click()

		time.sleep(2)
		driver.find_element(
		    by=By.CSS_SELECTOR,
		    value="#wrapper-learn > div.start-opt-body > div > div > div > div.m-t > a",
		).click()
		time.sleep(2.5)

		unknown_count = word_num
		while unknown_count > 1:
			cash_idx = driver.find_element(
			    by=By.CSS_SELECTOR,
			    value=
			    "#wrapper-learn > div.cc-table.fill-parent-h.middle.m-center > div > div.study-content.cc-table.middle > div.study-body.fade.in > div.CardItem.current.showing",
			).get_attribute("data-idx")
			for i in range(1, 5):
				ans_mean = driver.find_element(
				    By.CSS_SELECTOR,
				    value=
				    f'#wrapper-learn > div.cc-table.fill-parent-h.middle.m-center > div > div.study-content.cc-table.middle > div.study-body.fade.in > div.CardItem.current.showing > div.card-quest.card-quest-front > div:nth-child({i}) > div.card-quest-list > div',
				).get_attribute('innerText')
				ans_mean = ' '.join(re.split("[\n]", ans_mean))
				if word_dict[cash_idx]["mean"] == ans_mean:
					driver.find_element(
					    by=By.CSS_SELECTOR,
					    value=
					    f'#wrapper-learn > div.cc-table.fill-parent-h.middle.m-center > div > div.study-content.cc-table.middle > div.study-body.fade.in > div.CardItem.current.showing > div.card-quest.card-quest-front > div:nth-child({i})',
					).click()
					break
				if i == 4:
					driver.find_element(
					    by=By.CSS_SELECTOR,
					    value=
					    f'#wrapper-learn > div.cc-table.fill-parent-h.middle.m-center > div > div.study-content.cc-table.middle > div.study-body.fade.in > div.CardItem.current.showing > div.card-quest.card-quest-front > div:nth-child({i})',
					).click()
					time.sleep(1)
					driver.find_element(
					    by=By.XPATH,
					    value="//*[@id='wrapper-learn']/div[1]/div/div[3]/div[2]/a",
					)
					break
			unknown_count = int(
			    driver.find_element(
			        by=By.XPATH,
			        value='//*[@id="wrapper-learn"]/div[1]/div/div[1]/span[3]/span',
			    ).get_attribute('innerText'))
			print(f"남은 단어 수: {unknown_count}")
			time.sleep(2.5)

		print("리콜 학습 종료")
	elif ch_d == 3:
		driver.find_element(
		    by=By.CSS_SELECTOR,
		    value="#tab_set_all > div.card-list-title > div > div.text-right > a:nth-child(3)",
		).click()

		driver.find_element(
		    by=By.XPATH,
		    value="//*[@id='wrapper-learn']/div[2]/div/div/div/div[4]/a",
		).click()

		time.sleep(2)
		for i in range(1, word_num + 1):
			cash_d = driver.find_element(
			    by=By.XPATH,
			    value=f"//*[@id='wrapper-learn']/div[1]/div/div[2]/div[2]/div[{i}]",
			).get_attribute('data-idx')
			in_tag = driver.find_element(
			    by=By.CSS_SELECTOR,
			    value=
			    "#wrapper-learn > div > div > div.study-content.cc-table.middle > div.study-body.fade.in > div.CardItem.current.showing > div.card-bottom > div > div > div > div.text-normal.spell-input > input",
			)
			in_tag.click()
			in_tag.send_keys(word_dict[cash_d]["word"])
			driver.find_element(by=By.XPATH, value="//*[@id='wrapper-learn']/div/div/div[3]").click()
			time.sleep(1.5)
			try:
				driver.find_element(
				    by=By.XPATH,
				    value="//*[@id='wrapper-learn']/div/div/div[3]/div[2]",
				).click()
			except:
				pass
			i += 1
			time.sleep(1)
	elif ch_d == 4:
		print("Ctrl + C 를 눌러 강제 종료")
		##매칭 게임
		driver.find_element(
		    by=By.XPATH,
		    value="/html/body/div[2]/div/div[2]/div[1]/div[5]",
		).click()
		time.sleep(1)

		driver.find_element(
		    by=By.XPATH,
		    value="//*[@id='wrapper-learn']/div[1]/div[1]/div/div/div[2]/div[4]/a",
		).click()

		# 매칭 게임 시작
		time.sleep(3)
		while True:
			try:
				left_card = []
				for i in range(0, 4):
					cash_idx = driver.find_element(
					    by=By.XPATH,
					    value=f'//*[@id="left_card_{i}"]/div/div[1]/div/a/i',
					).get_attribute('data-idx')
					left_card.append(cash_idx)
				for i in range(0, 4):
					cash_answer = driver.find_element(
					    by=By.XPATH,
					    value=f"//*[@id='right_card_{i}']/div/div/div/div",
					).get_attribute('innerText')
					cash_answer = " ".join(re.split("[\n]", cash_answer))
					flag = False
					for j in range(0, 4):
						if cash_answer == word_dict[left_card[j]]["mean"]:
							flag = True
							driver.find_element(
							    by=By.XPATH,
							    value=f'//*[@id="left_card_{j}"]',
							).click()
							driver.find_element(
							    by=By.XPATH,
							    value=f"//*[@id='right_card_{i}']",
							).click()
							break
					if flag:
						break
				score = int(
				    driver.find_element(
				        by=By.XPATH, value='//*[@id="match-wrapper"]/div[1]/div[2]/span[2]').get_attribute('innerText'))
				time.sleep(2)
			except KeyboardInterrupt:
				driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div[1]/div[1]/a').click()
				driver.find_element(by=By.XPATH, value='//*[@id="confirmModal"]/div[2]/div/div[2]/a[3]').click()
				break
	if ch_d == 5:
		driver.find_element(by=By.XPATH, value="/html/body/div[2]/div/div[2]/div[2]/div").click()
		time.sleep(0.5)
		driver.find_element(by=By.XPATH, value="//*[@id='wrapper-test']/div/div[1]/div[1]/div[4]/a").click()
		time.sleep(0.5)
		question_number = driver.find_element(
		    by=By.XPATH, value="//*[@id='wrapper-test']/div/div[1]/div[3]/div[1]/div/div[2]/div[2]/span").text
		question_number = int(re.split("[ |문항]", question_number)[2])
		driver.find_element(by=By.XPATH, value="//*[@id='wrapper-test']/div/div[1]/div[3]/div[3]/a").click()
		time.sleep(2)
		for i in range(1, question_number + 1):
			time.sleep(0.5)
			cash_given = driver.find_element(
			    by=By.XPATH,
			    value=f"//*[@id='testForm']/div[{i}]/div/div[1]/div[2]/div[2]/div/div",
			).text
			cash_given = " ".join(re.split("[\n]", cash_given))
			driver.find_element(
			    by=By.XPATH,
			    value=f'//*[@id="testForm"]/div[{i}]/div/div[1]/div[2]/div[2]/div',
			).click()
			time.sleep(0.5)
			for j in range(1, 7):
				cash_answer = driver.find_element(
				    by=By.XPATH,
				    value=f'//*[@id="testForm"]/div[{i}]/div/div[2]/div/div[1]/div[{j}]/label/div',
				).get_attribute('innerText')
				cash_answer = ' '.join(re.split("[\n]", cash_answer))
				if cash_answer == word_dict[cash_given]:
					driver.find_element(
					    by=By.XPATH,
					    value=f'//*[@id="testForm"]/div[{i}]/div/div[2]/div/div[1]/div[{j}]/label/div',
					).click()
					break
			time.sleep(3)
	driver.get(class_site)
	ch_d = chd_wh()
