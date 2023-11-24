import json
import re
import sys
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver

from utility import logmessage


def do_memorize(driver: WebDriver, word_dict: dict) -> None:
	lm = logmessage("암기 학습 준비 중")
	driver.find_element(
	    by=By.CSS_SELECTOR,
	    value="body > div.bottom-fixed > div > div.cc-table.fill-parent.m-t > div.font-0.pos-relative > div:nth-child(1)",
	).click()

	time.sleep(1)

	driver.find_element(
	    by=By.CSS_SELECTOR,
	    value="#wrapper-learn > div.start-opt-body > div > div > div > div.m-t > a",
	).click()

	lm.log_message("암기 학습을 시작합니다")

	unknown_count = len(word_dict)

	time.sleep(2)

	while unknown_count > 1:
		unknown_count = int(
		    driver.find_element(
		        by=By.XPATH,
		        value='//*[@id="wrapper-learn"]/div[1]/div/div[1]/span[3]/span',
		    ).get_attribute('innerText'))
		lm.log_message(f"남은 단어 수: {unknown_count}")

		driver.find_element(
		    by=By.CSS_SELECTOR,
		    value='#wrapper-learn > div.cc-table.fill-parent-h.middle.m-center > div > div.study-bottom > div.btn-text.btn-down-cover-box > a',
		).click()
		time.sleep(0.5)

		data_idx = driver.find_element(
		    by=By.CSS_SELECTOR,
		    value='#wrapper-learn > div.cc-table.fill-parent-h.middle.m-center > div > div.study-content.cc-table.middle.pos-relative > div.study-body.fade.in > div.CardItem.showing.current',
		).get_attribute('data-idx')
		lm.log_message(f"암기 중: {str(word_dict[data_idx])}")

		driver.find_element(
		    by=By.CSS_SELECTOR,
		    value='#wrapper-learn > div.cc-table.fill-parent-h.middle.m-center > div > div.study-bottom > div.btn-text.btn-know-box > a',
		).click()
		time.sleep(3)

	driver.find_element(
	    by=By.CSS_SELECTOR,
	    value="body > div.study-header-body > div > div:nth-child(1) > div:nth-child(1) > a",
	).click()
	lm.log_message("암기 학습이 끝났습니다")


def do_recall(driver: WebDriver, word_dict: dict):
	lm = logmessage('리콜 학습 준비 중')

	driver.find_element(
	    by=By.CSS_SELECTOR,
	    value="body > div.bottom-fixed > div > div.cc-table.fill-parent.m-t > div.font-0.pos-relative > div:nth-child(2)",
	).click()

	time.sleep(2)
	driver.find_element(
	    by=By.CSS_SELECTOR,
	    value="#wrapper-learn > div.start-opt-body > div > div > div > div.m-t > a",
	).click()
	time.sleep(2.5)
	lm.log_message('리콜 학습을 시작합니다')

	unknown_count = len(word_dict)
	while unknown_count > 1:
		cash_idx = driver.find_element(
		    by=By.CSS_SELECTOR,
		    value="#wrapper-learn > div.cc-table.fill-parent-h.middle.m-center > div > div.study-content.cc-table.middle > div.study-body.fade.in > div.CardItem.current.showing",
		).get_attribute("data-idx")
		lm.log_message(f'리콜 중: {str(word_dict[cash_idx])}')

		for i in range(1, 4):
			ans_mean = driver.find_element(
			    By.CSS_SELECTOR,
			    value=f'#wrapper-learn > div.cc-table.fill-parent-h.middle.m-center > div > div.study-content.cc-table.middle > div.study-body.fade.in > div.CardItem.current.showing > div.card-quest.card-quest-front > div:nth-child({i}) > div.card-quest-list > div',
			).get_attribute('innerText')
			ans_mean = ans_mean.replace('  ', ' ').replace('\n', ' ')
			lm.log_message(f'____탐색 중: {ans_mean}')
			if word_dict[cash_idx]["mean"] == ans_mean:
				driver.find_element(
				    by=By.CSS_SELECTOR,
				    value=f'#wrapper-learn > div.cc-table.fill-parent-h.middle.m-center > div > div.study-content.cc-table.middle > div.study-body.fade.in > div.CardItem.current.showing > div.card-quest.card-quest-front > div:nth-child({i})',
				).click()
				break
		else:
			driver.find_element(
			    by=By.CSS_SELECTOR,
			    value=f'#wrapper-learn > div.cc-table.fill-parent-h.middle.m-center > div > div.study-content.cc-table.middle > div.study-body.fade.in > div.CardItem.current.showing > div.card-quest.card-quest-front > div:nth-child(4)',
			).click()
			lm.log_message(f'____탐색 실패: {word_dict[cash_idx]["mean"]}')

			time.sleep(1)
			driver.find_element(
			    by=By.XPATH,
			    value="//*[@id='wrapper-learn']/div[1]/div/div[3]/div[2]/a",
			)

		unknown_count = int(
		    driver.find_element(
		        by=By.XPATH,
		        value='//*[@id="wrapper-learn"]/div[1]/div/div[1]/span[3]/span',
		    ).get_attribute('innerText'))
		lm.log_message(f"남은 단어 수: {unknown_count}")
		time.sleep(2.5)

	lm.log_message('리콜 학습이 끝났습니다')


def do_spell(driver: WebDriver, word_dict: dict):
	lm = logmessage('스펠 학습 준비 중')
	driver.find_element(
	    by=By.CSS_SELECTOR,
	    value="#tab_set_all > div.card-list-title > div > div.text-right > a:nth-child(3)",
	).click()

	driver.find_element(
	    by=By.XPATH,
	    value="//*[@id='wrapper-learn']/div[2]/div/div/div/div[4]/a",
	).click()

	time.sleep(2)
	lm.log_message('스펠 학습을 시작합니다')

	unknown_count = len(word_dict)
	while unknown_count > 1:
		data_idx = driver.find_element(
		    by=By.CSS_SELECTOR,
		    value='#wrapper-learn > div.cc-table.fill-parent-h.middle.m-center > div > div.study-content.cc-table.middle > div.study-body.fade.in > div.CardItem.showing.current',
		).get_attribute('data-idx')

		answer_box = driver.find_element(
		    by=By.CSS_SELECTOR,
		    value="#wrapper-learn > div.cc-table.fill-parent-h.middle.m-center > div > div.study-content.cc-table.middle > div.study-body.fade.in > div.CardItem.showing.current > div.card-bottom > div > div > div > div.text-normal.spell-input > input",
		)
		answer_box.clear()
		answer_box.send_keys(word_dict[data_idx]["word"])

		driver.find_element(
		    by=By.XPATH,
		    value="//*[@id='wrapper-learn']/div/div/div[3]",
		).click()
		lm.log_message(f'스펠 중: {str(word_dict[data_idx])}')

		time.sleep(1.5)

		driver.find_element(
		    by=By.XPATH,
		    value="//*[@id='wrapper-learn']/div/div/div[3]/div[2]",
		).click()

		unknown_count = int(
		    driver.find_element(
		        by=By.XPATH,
		        value='//*[@id="wrapper-learn"]/div[1]/div/div[1]/span[3]/span',
		    ).get_attribute('innerText'))
		lm.log_message(f'남은 문제 수: {unknown_count}')

		time.sleep(1)

	lm.log_message('스펠 학습이 끝났습니다')


def do_matching(driver: WebDriver, word_dict: dict):
	lm = logmessage("매칭 학습 준비중\n____목표 점수 입력중...")
	while True:
		goal_score = input("목표 점수를 입력하세요\n____0을 입력하면 제한 시간동안 무제한으로 합니다.\n>>> ")
		lm.log_message(f'___입력 값: {goal_score}')
		try:
			goal_score = int(goal_score)
			if goal_score < 0:
				lm.log_message('____음이 아닌 정수를 입력해 주세요')
				continue
			if goal_score == 0:
				goal_score = sys.maxint
			break
		except ValueError:
			lm.log_message('____정수를 입력해주세요')

	lm.log_message(f'목표 점수가 {goal_score}점으로 설정되었습니다')

	driver.find_element(
	    by=By.XPATH,
	    value="/html/body/div[2]/div/div[2]/div[1]/div[5]",
	).click()
	time.sleep(1)

	driver.find_element(
	    by=By.XPATH,
	    value="//*[@id='wrapper-learn']/div[1]/div[1]/div/div/div[2]/div[4]/a",
	).click()
	time.sleep(3)

	lm.log_message('매칭 학습을 시작합니다')
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
				cash_answer = cash_answer.replace('\n', ' ').replace('  ', ' ')

				for j in range(0, 4):
					if cash_answer == word_dict[left_card[j]]["mean"]:
						driver.find_element(
						    by=By.XPATH,
						    value=f'//*[@id="left_card_{j}"]',
						).click()
						driver.find_element(
						    by=By.XPATH,
						    value=f"//*[@id='right_card_{i}']",
						).click()
						lm.log_message(f'매칭 중: {str(word_dict[left_card[j]])}')
						break
				else:
					continue
				break
			score = int(
			    driver.find_element(
			        by=By.XPATH,
			        value='//*[@id="match-wrapper"]/div[1]/div[2]/span[2]',
			    ).get_attribute('innerText'))
			lm.log_message(f'현재 점수: {score}점')

			if score >= goal_score:
				lm.log_message(f'목표 점수 {goal_score}점에 도달하여 매칭 학습을 종료합니다')
				return

			time.sleep(2)
		except KeyboardInterrupt:
			return
		except:
			lm.log_message('시간 제한에 의해서 매칭 학습이 종료됩니다')


def do_test(driver: WebDriver, word_dict: dict):
	lm = logmessage('테스트 준비 중')
	driver.find_element(
	    by=By.XPATH,
	    value="/html/body/div[2]/div/div[2]/div[2]/div",
	).click()
	time.sleep(0.5)

	driver.find_element(
	    by=By.XPATH,
	    value="//*[@id='wrapper-test']/div/div[1]/div[1]/div[4]/a",
	).click()
	time.sleep(0.5)

	question_count = driver.find_element(
	    by=By.XPATH,
	    value="//*[@id='wrapper-test']/div/div[1]/div[3]/div[1]/div/div[2]/div[2]/span",
	).text
	question_count = int(re.split("[ |문항]", question_count)[2])
	lm.log_message(f'테스트 총 문제 수: {question_count}')

	driver.find_element(
	    by=By.XPATH,
	    value="//*[@id='wrapper-test']/div/div[1]/div[3]/div[3]/a",
	).click()
	time.sleep(2)

	lm.log_message('테스트를 시작합니다')
	for i in range(1, question_count + 1):
		time.sleep(0.5)
		cash_given = driver.find_element(
		    by=By.XPATH,
		    value=f"//*[@id='testForm']/div[{i}]/div/div[1]/div[2]/div[2]/div/div",
		).text.replace('\n', ' ').replace('  ', ' ')

		for idx, d in word_dict.items():
			if d["word"] == cash_given:
				cash_idx: str = idx
				cash_answer_type = "mean"
				break
			if d["mean"] == cash_given:
				cash_idx: str = idx
				cash_answer_type = "word"
				break

		driver.find_element(
		    by=By.XPATH,
		    value=f'//*[@id="testForm"]/div[{i}]/div/div[1]/div[2]/div[2]/div',
		).click()
		time.sleep(0.2)

		for j in range(1, 7):
			cash_option = driver.find_element(
			    by=By.XPATH,
			    value=f'//*[@id="testForm"]/div[{i}]/div/div[2]/div/div[1]/div[{j}]/label/div',
			).get_attribute('innerText').replace('\n', ' ').replace('  ', ' ')

			if cash_option == word_dict[cash_idx][cash_answer_type]:
				driver.find_element(
				    by=By.XPATH,
				    value=f'//*[@id="testForm"]/div[{i}]/div/div[2]/div/div[1]/div[{j}]/label/div',
				).click()
				lm.log_message(f'테스트 중: {str(word_dict[cash_idx])}')
				break

		currunt_question = int(
		    driver.find_element(
		        by=By.XPATH,
		        value='//*[@id="wrapper-test"]/div/div[2]/div[1]/div/span[1]',
		    ).get_attribute('innerText'))
		lm.log_message(f'남은 문제 수: {question_count - currunt_question}')
		time.sleep(0.2)
	lm.log_message('테스트가 끝났습니다')


def do_stduy(study_type: int, driver: WebDriver, word_dict: dict):
	if study_type == 1:
		do_memorize(driver, word_dict)
	elif study_type == 2:
		do_recall(driver, word_dict)
	elif study_type == 3:
		do_spell(driver, word_dict)
	elif study_type == 4:
		do_matching(driver, word_dict)
	elif study_type == 5:
		do_test(driver, word_dict)
