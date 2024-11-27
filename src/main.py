from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from datetime import datetime
import json


def merge_dicts(data_dicts):
    merged_dict = {"web-of-science": {}}
    for current_dict in data_dicts:
        for year, values in current_dict.items():
            merged_dict["web-of-science"][year] = values
    return merged_dict


def parse_data(year):
    url = 'https://science.nsu.ru/publication-analytics?action=web-of-science&years={}%2C{}'.format(year, year)
    driver = webdriver.Chrome()
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="tree"]')))
    except Exception as e:
        print('Failed to load page: {}'.format(e))
        driver.quit()
        return {}

    d = {year: {}}
    for n in range(1, 61):
        xpath_il1 = '//*[@id="tree"]/div[{}]'.format(n)
        try:
            item_level_1 = driver.find_element(By.XPATH, xpath_il1)
            department = (item_level_1.find_element(By.TAG_NAME, 'a')).text
            number = (item_level_1.find_element(By.TAG_NAME, 'span')).text
            d[year][department] = number
        except Exception as e:
            print('An error occurred: {}'.format(e))
            driver.quit()
            return {}
    driver.quit()
    return d


if __name__ == '__main__':
    data_dicts = []
    for year in range(2020, 2025):
        data_dicts.append(parse_data(year))
    data = merge_dicts(data_dicts)

    print('Please enter the path to the directory where the the resulting file will be saved.')
    dr = input()
    file_path = dr.strip() + '\\' + ((datetime.today()).isoformat()).replace(':', '-') + '.json'
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)
