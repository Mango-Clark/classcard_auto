import json
import time

import requests

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver


def word_get(driver: WebDriver):
	html = BeautifulSoup(driver.page_source, "html.parser")
	cards = html.find("div", class_="flip-body")
	word_num = len(cards.find_all("div", class_="flip-card"))

	idx = [0 for _ in range(word_num + 1)]
	word = [0 for _ in range(word_num + 1)]
	mean = [0 for _ in range(word_num + 1)]

	retdict = {'word_num': word_num}

	for i in range(1, word_num + 1):
		idx[i] = driver.find_element(
		    by=By.XPATH,
		    value=f"//*[@id='tab_set_all']/div[2]/div[{i}]",
		).get_attribute("data-idx")

		word[i] = driver.find_element(
		    by=By.XPATH,
		    value=f'//*[@id="tab_set_all"]/div[2]/div[{i}]/div[1]',
		).get_attribute("innerText")

		mean[i] = driver.find_element(
		    by=By.XPATH,
		    value=f'//*[@id="tab_set_all"]/div[2]/div[{i}]/div[2]',
		).get_attribute("innerText")

		mean[i] = mean[i].replace('\n', ' ').replace('  ', ' ')

		retdict.update({idx[i]: {"word": word[i], "mean": mean[i]}})
		retdict.update({word[i]: mean[i]})
		retdict.update({mean[i]: word[i]})
	return retdict


def get_study_type():
	print("""
학습유형을 선택해주세요.
Ctrl + C 를 눌러 종료
[1] 암기학습
[2] 리콜학습
[3] 스펠학습
[4] 매칭게임
[5] 테스트
	""")
	while 1:
		try:
			study_type = int(input(">>> "))
			if study_type >= 1 and study_type <= 5:
				break
			else:
				raise ValueError
		except ValueError:
			print("학습유형을 다시 입력해주세요.")
		except KeyboardInterrupt:
			quit()
	return study_type


def check_id(id: str, pw: str):
	print("계정 정보를 확인하고 있습니다 잠시만 기다려주세요!")
	headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
	data = {"login_id": id, "login_pwd": pw}
	res = requests.post("https://www.classcard.net/LoginProc", headers=headers, data=data)
	status = res.json()
	if status["result"] == "ok":
		return True
	else:
		return False


def save_id():
	while True:
		id = input("아이디를 입력하세요 : ")
		password = input("비밀번호를 입력하세요 : ")
		if check_id(id, password):
			data = {"id": id, "pw": password}
			with open("config.json", "w", encoding="utf-8") as f:
				json.dump(data, f, ensure_ascii=False, indent=4)
			print("아이디 비밀번호가 저장되었습니다.\n")
			return data
		else:
			print("아이디 또는 비밀번호가 잘못되었습니다.\n")
			continue


def get_id():
	try:
		with open("config.json", "r", encoding="utf-8") as f:
			return json.load(f)
	except:
		return save_id()


def save_url():
	while True:
		url = input("학습할 세트URL을 입력하세요 : ")
		account = get_id()
		data = {"id": account["id"], "pw": account["pw"], "url": url}
		with open("config.json", "w", encoding="utf-8") as f:
			json.dump(data, f, ensure_ascii=False, indent=4)
		print("학습할 세트URL이 저장되었습니다.\n")
		return data


def get_url():
	try:
		with open("config.json", "r", encoding="utf-8") as f:
			json_data = json.load(f)
			return json_data["url"]
	except:
		return save_url()


def change_url():
	print("""
학습할 세트URL을 변경하겠습니까? Y/N
Ctrl + C 를 눌러 종료
	""")
	while 1:
		try:
			ch_d = input(">>> ")
			if ch_d.casefold() == "N".casefold() or ch_d.casefold() == "NO".casefold():
				return get_url()
			elif ch_d.casefold() == "Y".casefold() or ch_d.casefold() == "YES".casefold():
				return save_url()
			else:
				raise ValueError
		except ValueError:
			print("다시 입력해주세요.")
		except KeyboardInterrupt:
			quit()


def log_header() -> str:
	return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ' | '
