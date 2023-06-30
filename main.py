import random
import time
import warnings
import re

import chromedriver_autoinstaller
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
)
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

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
word_num = len(word_dict)

while 1:
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
		for i in range(1, word_num + 1):
			time.sleep(2)
			try:
				driver.find_element(
				    by=By.CSS_SELECTOR,
				    value="#wrapper-learn > div > div > div.study-bottom > div.btn-text.btn-down-cover-box",
				).click()
				time.sleep(0.5)
				driver.find_element(
				    by=By.CSS_SELECTOR,
				    value="#wrapper-learn > div > div > div.study-bottom.down > div.btn-text.btn-know-box",
				).click()
			except:
				break
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
		time.sleep(2)

		try:
			for i in range(1, word_num + 1):
				cash_idx = driver.find_element(
				    by=By.XPATH,
				    value=f"//*[@id='wrapper-learn']/div[1]/div/div[2]/div[2]/div[{i}]",
				).get_attribute("data-idx")

				for j in range(1, 5):
					ans_mean = driver.find_element(
					    By.XPATH,
					    value=f"//*[@id='wrapper-learn']/div[1]/div/div[2]/div[2]/div[{i}]/div[3]/div[{j}]/div[2]/div",
					).text
					if word_dict[cash_idx]["mean"] == ans_mean:
						driver.find_element(
						    by=By.XPATH,
						    value=
						    f"//*[@id='wrapper-learn']/div[1]/div/div[2]/div[2]/div[{i}]/div[3]/div[{j}]/div[2]/div",
						).click()
						break
					if j == 4:
						driver.find_element(
						    by=By.XPATH,
						    value=
						    f"//*[@id='wrapper-learn']/div[1]/div/div[2]/div[2]/div[{i}]/div[3]/div[{j}]/div[2]/div",
						).click()
						time.sleep(1)
						driver.find_element(
						    by=By.XPATH,
						    value="//*[@id='wrapper-learn']/div[1]/div/div[3]/div[2]/a",
						)
						break
				time.sleep(2.5)
		except Exception as e:
			pass

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
		try:
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
		except NoSuchElementException:
			pass
	elif ch_d == 4:
		driver.find_element(by=By.XPATH, value="/html/body/div[2]/div/div[2]/div[2]/div").click()
		time.sleep(0.5)
		driver.find_element(by=By.XPATH, value="//*[@id='wrapper-test']/div/div[1]/div[1]/div[4]/a").click()
		time.sleep(0.5)
		driver.find_element(by=By.XPATH, value="//*[@id='wrapper-test']/div/div[1]/div[3]/div[3]/a").click()
		time.sleep(1.5)

		## 여기까지 함
		try:
			driver.find_element(by=By.XPATH, value="/html/body/div[26]/div[2]/div/div[3]/a").click()

			driver.get(class_site)

			driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[4]/div/div/div[3]/a[1]").click()

			time.sleep(1)
		except:
			pass

		driver.find_element(by=By.XPATH, value="/html/body/div[2]/div/div[1]/div[1]/div[4]/a").click()

		driver.find_element(by=By.XPATH, value="/html/body/div[2]/div/div[1]/div[3]/div[3]/a").click()

		time.sleep(2)
		for i in range(1, 21):
			cash_d = driver.find_element(
			    by=By.XPATH,
			    value=f"/html/body/div[2]/div/div[2]/div[1]/form/div[{i}]/div/div[1]/div[2]/div/div/div",
			).text

			element = driver.find_element(
			    by=By.XPATH,
			    value=f"/html/body/div[2]/div/div[2]/div[1]/form/div[{i}]/div/div[1]/div[2]",
			)
			driver.execute_script("arguments[0].click();", element)

			cash_dby = [0, 0, 0, 0]

			for j in range(0, 4):
				cash_dby[j] = driver.find_element(
				    by=By.XPATH,
				    value=
				    f"/html/body/div[2]/div/div[2]/div[1]/form/div[{i}]/div/div[2]/div/div[1]/div[{j+1}]/label/div/div",
				).text

			time.sleep(2)
			ck = False
			if cash_d.upper() != cash_d.lower():
				for j in range(0, 4):
					if word.index(cash_d) == mean.index(cash_dby[j]):
						element = driver.find_element(
						    by=By.XPATH,
						    value=
						    f"/html/body/div[2]/div/div[2]/div[1]/form/div[{i}]/div/div[2]/div/div[1]/div[{j+1}]/label/div/div",
						)
						driver.execute_script("arguments[0].click();", element)
						ck = True
						break
			else:
				for j in range(0, 4):
					if mean.index(cash_d) == word.index(cash_dby[j]):
						element = driver.find_element(
						    by=By.XPATH,
						    value=
						    f"/html/body/div[2]/div/div[2]/div[1]/form/div[{i}]/div/div[2]/div/div[1]/div[{j+1}]/label/div/div",
						)
						driver.execute_script("arguments[0].click();", element)
						ck = True
						break
			if ck != True:
				print("\n찾을수없는 단어 감지로 랜덤으로 찍기발동!!\n")
				driver.find_element(
				    by=By.XPATH,
				    value=
				    f"/html/body/div[2]/div/div[2]/div[1]/form/div[{i}]/div/div[2]/div/div[1]/div[{random.randint(1, 4)}]/label/div/div",
				).click()
				time.sleep(2)
			time.sleep(3)
	if ch_d == 5:
		print("Ctrl + C 를 눌러 강제 종료")
		##매칭 게임
		driver.find_element(by=By.CSS_SELECTOR, value="a.w-120:nth-child(2) > div:nth-child(1)").click()
		time.sleep(1)

		# 단어 1000개 이상
		try:
			driver.find_element(by=By.XPATH, value="/html/body/div[53]/div[2]/div/div[2]/a[3]").click()
			time.sleep(1)
		except Exception as e:
			pass
		driver.find_element(by=By.XPATH, value="/html/body/div[5]/div[2]/div/div/div[1]/div[4]/a[1]").click()
		# 매칭 게임 시작
		time.sleep(2.5)
		past_cards = ""
		while True:
			try:
				html = BeautifulSoup(driver.page_source, "html.parser")
				# 점수 순으로 정렬
				unsorted_cards = dict()
				cards = html.find("div", class_="match-body").get_text(strip=True)
				# 이전 카드와 같으면 다시
				if past_cards == cards:
					raise NotImplementedError
				for i in range(4):
					left_card = html.find("div", id="left_card_{}".format(i))
					score = int(left_card.find("span", class_="card-score").get_text(strip=True))
					left_card.find("span", class_="card-score").decompose()
					question = left_card.get_text(strip=True)
					unsorted_cards["{}_{}".format(question, str(i))] = score
					# 점수 높은 순서로 배열
					sorted_lists = {k: v for k, v in sorted(unsorted_cards.items(), key=lambda item: item[1])}.keys()
				for k in sorted_lists:
					word = k.split("_")[0]
					order = k.split("_")[1]
					# answer = list[word]
					answer = mean[word.index(word)]

					for j in range(4):
						right_card = html.find("div", id="right_card_{}".format(j)).get_text(strip=True)
						if right_card == answer:
							left_element = driver.find_element_by_id("left_card_{}".format(order))
							right_element = driver.find_element_by_id("right_card_{}".format(j))
							try:
								left_element.click()
								right_element.click()
							except ElementClickInterceptedException:
								action = ActionChains(driver)
								action.click(on_element=left_element)
								action.click(on_element=right_element)
								action.perform()
								action.reset_actions()
							raise NotImplementedError
						else:
							continue
			except NotImplementedError:
				if driver.find_element_by_class_name("rank-info").size["height"] > 0:
					print("완료되었습니다")
					driver.find_element(by=By.CSS_SELECTOR, value=".btn-default").click()
					time.sleep(1)
					break
				else:
					past_cards = cards
			except KeyboardInterrupt:
				break

	driver.get(class_site)
	ch_d = chd_wh()
