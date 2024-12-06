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
    """
        Настраивает и инициализирует экземпляр веб-драйвера Chrome.
        Args:
            path_to_driver (str): Путь к исполняемому файлу драйвера Chrome.
        Returns:
            webdriver.Chrome: Экземпляр веб-драйвера Chrome с заданными параметрами.
        """
    service = Service(path_to_driver)
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def merge_dicts(data_dicts, search_parameter):
    """
        Объединяет несколько словарей в один, используя заданный параметр поиска в качестве ключа.
        Args:
            data_dicts (list): Список словарей, которые нужно объединить.
            search_parameter (str): Параметр, который будет использоваться в качестве ключа в объединенном словаре.
        Returns:
            dict: Объединенный словарь с данными.
        """
    merged_dict = {search_parameter: {}}
    for current_dict in data_dicts:
        for year, values in current_dict.items():
            merged_dict[search_parameter][year] = values
    return merged_dict


def writing_answer(name_of_dir, search_parameter, data):
    """
        Записывает данные в JSON файл в указанной директории.
        Args:
            name_of_dir (str): Название директории, в которую будет сохранен файл.
            search_parameter (str): Параметр, который будет частью имени файла.
            data (dict): Данные, которые нужно сохранить в файл.
        """
    file_path = name_of_dir.strip() + '/' + search_parameter + '_' + ((datetime.today()).isoformat()).replace(':', '-') + '.json'
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)
    return


def get_department_number(item_level):
    """
        Извлекает название подразделения и число из элемента уровня.
        Args:
            item_level (WebElement): Элемент, из которого нужно извлечь данные.
        Returns:
            Кортеж, содержащий название отдела и соответствующее ему число, или (None, None) если данные не найдены.
        """
    department = item_level.find_element(By.TAG_NAME, 'a').text
    number = item_level.find_element(By.TAG_NAME, 'span').text
    if department and number:
        return department, number
    else:
        return None, None


def get_arrow(item_level):
    """
        Находит в коде стрелку, которая может быть использована для раскрывания дополнительных данных.
        Args:
            item_level (WebElement): Элемент, в котором нужно найти стрелку.
        Returns:
            WebElement or None: Элемент стрелки, если найден, иначе None.
        """
    try:
        arrow = item_level.find_element(By.CLASS_NAME, 'arrow')
        if arrow:
            return arrow
        else:
            return None
    except Exception:
        return None


def get_items(item_level, item_level_number):
    """
        Извлекает элементы заданного уровня из элемента уровня.
        Args:
            item_level (WebElement): Элемент, из которого нужно извлечь элементы.
            item_level_number (int): Номер уровня, элементы которого нужно извлечь.
        Returns:
            list: Список найденных элементов.
        """
    items = item_level.find_elements(By.CLASS_NAME, 'item-level-{}'.format(item_level_number))
    return items


def parse_items(items, item_level_number):
    """
    Обрабатывает список элементов, извлекая информацию о департаментах и их вложенных элементах.
    Args:
        items (list): Список элементов для обработки.
        item_level_number (int): Номер уровня текущих элементов.
    Returns:
        dict: Словарь, содержащий информацию о департаментах и их вложенных элементах.
    """
    d = {}
    for item_level in items:
        department, number = None, None
        retries = 10
        while retries > 0:
            department, number = get_department_number(item_level)
            if department is None:
                time.sleep(1)
            else:
                break
            retries -= 1
        if department is not None:
            d[department] = {'number': number}
        else:
            pass
        arrow = get_arrow(item_level)
        if arrow is not None:
            arrow.click()
        nested_items = get_items(item_level, item_level_number + 1)
        if len(nested_items) != 0:
            nested_d = parse_items(nested_items, item_level_number + 1)
            d[department]['items'] = nested_d
    return d


def parse_data(year, driver, search_parameter):
    """
        Основная функция, которая извлекает данные о публикациях за указанный год с сайта.
        Args:
            year (int): Год, для которого нужно получить данные.
            driver (webdriver.Chrome): Экземпляр веб-драйвера для взаимодействия с веб-страницей.
            search_parameter (str): Параметр для запроса данных на сайте.
        Returns:
            dict: Словарь с данными о публикациях за указанный год, или пустой словарь в случае ошибки.
        """
    url = 'https://science.nsu.ru/publication-analytics?action={}&years={}%2C{}'.format(search_parameter, year, year)
    try:
        driver.get(url)
    except Exception as e:
        print('Failed to open page: {}'.format(e))
        return {}

    d = {year: {}}
    xpath_tree_items = '//*[@id="tree"]' #!!!!!!!
    try:
        tree_items = WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.XPATH, xpath_tree_items)))
    except Exception as e:
        print('Failed to load: {}'.format(e))
        return {}

    items = get_items(tree_items, 1)
    d[year] = parse_items(items, 1)

    return d
