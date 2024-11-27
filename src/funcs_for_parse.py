from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time
from datetime import datetime
import json


def driver_setup(path_to_driver):
    service = Service(path_to_driver)
    options = Options()
    options.add_argument('--headless') #работа драйвера в фоновом режиме
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def merge_dicts(data_dicts):
    merged_dict = {"web-of-science": {}}
    for current_dict in data_dicts:
        for year, values in current_dict.items():
            merged_dict["web-of-science"][year] = values
    return merged_dict


def writing_answer(name_of_dir, data):
    file_path = name_of_dir.strip() + '\\parse_NGU_' + ((datetime.today()).isoformat()).replace(':', '-') + '.json'
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)


def get_department_number(item_level):
    department = item_level.find_element(By.TAG_NAME, 'a').text
    number = item_level.find_element(By.TAG_NAME, 'span').text
    if department and number:
        return department, number
    else:
        return None, None



def parse_data(year, driver):
    url = 'https://science.nsu.ru/publication-analytics?action=web-of-science&years={}%2C{}'.format(year, year)
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="tree"]')))
    except Exception as e:
        print('Failed to load page: {}'.format(e))
        driver.quit()
        return {}

    d = {year: {}}
    for n in range(1, 61):
        xpath_il1 = '//*[@id="tree"]/div[{}]'.format(n)
        item_level_1 = WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.XPATH, xpath_il1)))
        department, number = get_department_number(item_level_1)
        if (department == None) and (number == None):
            item_level_1 = driver.find_element(By.XPATH, xpath_il1)
            time.sleep(1)
            department, number = get_department_number(item_level_1)
        d[year][department] = number
    return d
