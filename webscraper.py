from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import csv
import re

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
page = 1

with open('all_immobile.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file, delimiter=';')
    writer.writerow(['Título', 'Preço', 'Localização', 'Data'])
    while True:
        url = f'https://www.olx.com.br/imoveis/estado-sc?o={page}'
        driver.get(url=url)
        try:
            main_content = driver.find_element(By.ID, 'main-content')
            print(f'-- scraping page {page}')
            elements = main_content.find_elements(By.CLASS_NAME, 'renderIfVisible')
            for immobile in elements:
                driver.execute_script("arguments[0].scrollIntoView();", immobile)
                location = None
                title = immobile.find_element(By.CLASS_NAME, 'title').text
                date = immobile.find_element(By.CLASS_NAME, 'date').text
                price = 'Preço não disponível'
                for p_tag in immobile.find_elements(By.TAG_NAME, 'p'):
                    if re.compile(r'^sc-\w+\s\w+$').match(p_tag.get_attribute('class')):
                        location = p_tag.text
                try:
                    price = immobile.find_element(By.CLASS_NAME, 'price').text
                except NoSuchElementException as e:
                    print(f'{title}: preco nao disponivel')
                writer.writerow([title, price, location, date])
            page += 1
        except NoSuchElementException as e:
            print('Sem mais resultados')
            break
