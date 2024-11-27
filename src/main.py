import random
from funcs_for_parse import *

print('Please enter the path to the chromedriver:')
path_to_driver = input()
driver = driver_setup(path_to_driver)

data_dicts = []
for year in range(2020, 2025):
    data_dicts.append(parse_data(year, driver))
    time.sleep(random.uniform(1, 3))
driver.quit()
data = merge_dicts(data_dicts)

print('Please enter the path to the directory where the resulting file will be saved:')
name_of_dir = input()
writing_answer(name_of_dir, data)
