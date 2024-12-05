import random
from funcs_for_parse import *

#print('Please enter the path to the chromedriver:')
#path_to_driver = input()
path_to_driver = 'C:/chromedriver/chromedriver.exe'
driver = driver_setup(path_to_driver)

search_parameters = ['contracts', 'mass-media', 'scopus', 'citations', 'web-of-science', 'authors', 'patents', 'number-of-protection', 'staff', 'applications', 'projects']
print(
    '0 - contracts' + '\n' +
    '1 - mass-media' + '\n' +
    '2 - scopus' + '\n' +
    '3 - citations' + '\n' +
    '4 - web-of-science' + '\n' +
    '5 - authors' + '\n' +
    '6 - patents' + '\n' +
    '7 - number-of-protection' + '\n' +
    '8 - staff' + '\n' +
    '9 - applications' + '\n' +
    '10 - projects'
)
print('Please enter the number of search parameter for parse:')
search_parameter_number = int(input())
search_parameter = search_parameters[search_parameter_number]

data_dicts = []
for year in range(2020, 2025):
    data_dicts.append(parse_data(year, driver, search_parameter))
    print(str(year) + ' year parsed.')
    time.sleep(random.uniform(1, 3))
driver.quit()
data = merge_dicts(data_dicts, search_parameter)

#print('Please enter the path to the directory where the resulting file will be saved:')
#name_of_dir = input()
name_of_dir = 'C:/Users/marin/OneDrive/Рабочий стол/Result'
writing_answer(name_of_dir, search_parameter, data)
