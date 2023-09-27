import json
import re
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver

from utility import log_header


def do_memorize(driver: WebDriver, word_dict: dict, do_logging: bool):
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

	if do_logging:
		with open('.log', 'a', encoding='utf-8') as log:
			log.write(f'{log_header()}암기를 시작합니다\n\n')

	unknown_count = word_dict['word_num']

	while unknown_count > 1:
		time.sleep(3)
		driver.find_element(
		    by=By.XPATH,
		    value='//*[@id="wrapper-learn"]/div[1]/div/div[3]/div[1]/a',
		).click()

		unknown_count = int(
		    driver.find_element(
		        by=By.XPATH,
		        value='//*[@id="wrapper-learn"]/div[1]/div/div[1]/span[3]/span',
		    ).get_attribute('innerText'))
		print(f"{log_header()}남은 단어 수: {unknown_count}")

		if do_logging:
			with open('.log', 'a', encoding='utf-8') as log:
				data_idx = driver.find_element(
				    by=By.CSS_SELECTOR,
				    value=
				    '#wrapper-learn > div.cc-table.fill-parent-h.middle.m-center > div > div.study-content.cc-table.middle.pos-relative > div.study-body.fade.in > div.CardItem.current.showing',
				).get_attribute('data-idx')
				log.write(f'{log_header()}외우는 중: {str(word_dict[data_idx])}\n')
				log.write(f"{log_header()}남은 단어 수: {unknown_count}\n")

		time.sleep(0.5)
		driver.find_element(
		    by=By.XPATH,
		    value='//*[@id="wrapper-learn"]/div[1]/div/div[3]/div[2]/a',
		).click()
	time.sleep(1)
	driver.find_element(
	    by=By.CSS_SELECTOR,
	    value="body > div.study-header-body > div > div:nth-child(1) > div:nth-child(1) > a",
	).click()
	print("암기가 끝났습니다.")
	if do_logging:
		with open('.log', 'a', encoding='utf-8') as log:
			log.write(f'{log_header()}암기가 끝났습니다\n\n\n')


def do_recall(driver: WebDriver, word_dict: dict, do_logging: bool):
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

	if do_logging:
		with open('.log', 'a', encoding='utf-8') as log:
			log.write(f'{log_header()}리콜 학습 시작합니다\n\n\n')

	unknown_count = word_dict['word_num']
	while unknown_count > 1:
		cash_idx = driver.find_element(
		    by=By.CSS_SELECTOR,
		    value=
		    "#wrapper-learn > div.cc-table.fill-parent-h.middle.m-center > div > div.study-content.cc-table.middle > div.study-body.fade.in > div.CardItem.current.showing",
		).get_attribute("data-idx")

		if do_logging:
			with open('.log', 'a', encoding='utf-8') as log:
				log.write(f'{log_header()}리콜 중: {str(word_dict[cash_idx])}\n')

		for i in range(1, 4):
			ans_mean = driver.find_element(
			    By.CSS_SELECTOR,
			    value=
			    f'#wrapper-learn > div.cc-table.fill-parent-h.middle.m-center > div > div.study-content.cc-table.middle > div.study-body.fade.in > div.CardItem.current.showing > div.card-quest.card-quest-front > div:nth-child({i}) > div.card-quest-list > div',
			).get_attribute('innerText')
			ans_mean = ans_mean.replace('  ', ' ').replace('\n', ' ')
			if do_logging:
				with open('.log', 'a', encoding='utf-8') as log:
					log.write(f'{log_header()}____탐색 중: {ans_mean}\n')
			if word_dict[cash_idx]["mean"] == ans_mean:
				driver.find_element(
				    by=By.CSS_SELECTOR,
				    value=
				    f'#wrapper-learn > div.cc-table.fill-parent-h.middle.m-center > div > div.study-content.cc-table.middle > div.study-body.fade.in > div.CardItem.current.showing > div.card-quest.card-quest-front > div:nth-child({i})',
				).click()
				break
		else:
			driver.find_element(
			    by=By.CSS_SELECTOR,
			    value=
			    f'#wrapper-learn > div.cc-table.fill-parent-h.middle.m-center > div > div.study-content.cc-table.middle > div.study-body.fade.in > div.CardItem.current.showing > div.card-quest.card-quest-front > div:nth-child(4)',
			).click()
			if do_logging:
				with open('.log', 'a', encoding='utf-8') as log:
					log.write(f'{log_header()}____탐색 실패: {word_dict[cash_idx]["mean"]}\n')
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
		print(f"남은 단어 수: {unknown_count}")
		if do_logging:
			with open('.log', 'a', encoding='utf-8') as log:
				log.write(f'{log_header()}남은 단어 수: {unknown_count}\n\n')
		time.sleep(2.5)

	print("리콜 학습 종료")
	if do_logging:
		with open('.log', 'a', encoding='utf-8') as log:
			log.write(f'{log_header()}리콜 학습 종료\n\n\n')


def do_spell(driver: WebDriver, word_dict: dict, do_logging: bool):
	driver.find_element(
	    by=By.CSS_SELECTOR,
	    value="#tab_set_all > div.card-list-title > div > div.text-right > a:nth-child(3)",
	).click()

	driver.find_element(
	    by=By.XPATH,
	    value="//*[@id='wrapper-learn']/div[2]/div/div/div/div[4]/a",
	).click()

	time.sleep(2)

	unknown_count = word_dict['word_num']
	while unknown_count > 1:
		data_idx = driver.find_element(
		    by=By.XPATH,
		    value=
		    '#wrapper-learn > div.cc-table.fill-parent-h.middle.m-center > div > div.study-content.cc-table.middle > div.study-body.fade.in > div.CardItem.showing.current',
		).get_attribute('data-idx')

		answer_box = driver.find_element(
		    by=By.CSS_SELECTOR,
		    value=
		    "#wrapper-learn > div.cc-table.fill-parent-h.middle.m-center > div > div.study-content.cc-table.middle > div.study-body.fade.in > div.CardItem.showing.current > div.card-bottom > div > div > div > div.text-normal.spell-input > input",
		)
		answer_box.clear()
		answer_box.send_keys(word_dict[data_idx]["word"])

		driver.find_element(
		    by=By.XPATH,
		    value="//*[@id='wrapper-learn']/div/div/div[3]",
		).click()

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

		print(f'남은 문제 수: {unknown_count}')

		time.sleep(1)


def do_matching(driver: WebDriver, word_dict: dict, do_logging: bool):
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
				cash_answer = cash_answer.replace('  ', ' ').replace('\n', ' ')

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
						break
				else:
					continue
				break
			score = driver.find_element(
			    by=By.XPATH,
			    value='//*[@id="match-wrapper"]/div[1]/div[2]/span[2]',
			).get_attribute('innerText')
			print(f'현재 점수: {score}점')
			time.sleep(2)
		except KeyboardInterrupt:
			driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div[1]/div[1]/a').click()
			driver.find_element(by=By.XPATH, value='//*[@id="confirmModal"]/div[2]/div/div[2]/a[3]').click()
			break
		except:
			with open('config.json', 'r') as f:
				json_data = json.load(f)
				driver.get(json_data["url"])


def do_test(driver: WebDriver, word_dict: dict, do_logging: bool):
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

	driver.find_element(
	    by=By.XPATH,
	    value="//*[@id='wrapper-test']/div/div[1]/div[3]/div[3]/a",
	).click()
	time.sleep(2)
	for i in range(1, question_count):
		time.sleep(0.5)
		cash_given = driver.find_element(
		    by=By.XPATH,
		    value=f"//*[@id='testForm']/div[{i}]/div/div[1]/div[2]/div[2]/div/div",
		).text
		cash_given = cash_given.replace('  ', ' ').replace('\n', ' ')
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
			cash_answer = cash_answer.replace('  ', ' ').replace('\n', ' ')
			if cash_answer == word_dict[cash_given]:
				driver.find_element(
				    by=By.XPATH,
				    value=f'//*[@id="testForm"]/div[{i}]/div/div[2]/div/div[1]/div[{j}]/label/div',
				).click()
				break
		currunt_question = int(
		    driver.find_element(
		        by=By.XPATH,
		        value='//*[@id="wrapper-test"]/div/div[2]/div[1]/div/span[1]',
		    ).get_attribute('innerText'))
		print(f'남은 문제 수: {question_count - currunt_question}')
		time.sleep(3)


def do_stduy(study_type: int, driver: WebDriver, word_dict: dict, do_logging: bool):
	if study_type == 1:
		do_memorize(driver, word_dict, do_logging)
	elif study_type == 2:
		do_recall(driver, word_dict, do_logging)
	elif study_type == 3:
		do_spell(driver, word_dict, do_logging)
	elif study_type == 4:
		do_matching(driver, word_dict, do_logging)
	elif study_type == 5:
		do_test(driver, word_dict, do_logging)
