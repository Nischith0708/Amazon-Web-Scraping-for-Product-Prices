import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import datetime
import time
import re

today = datetime.date.today()

def create_list():
    file = open('Names.txt', 'r')
    list1 = []
    for line in file:
        # Remove unwanted characters using regex
        cleaned_line = re.sub(r'[.,\'()|]', '', line)
        list1.append(cleaned_line.strip())
    file.close()
    return list1

def preprocess_text(text):
    # Remove unwanted characters using regex
    cleaned_text = re.sub(r'[.,\'()|]', '', text)
    return cleaned_text

def price_value(product_name, l3, writer):
    driver_path = r'C:\Users\Engro\Downloads\chromedriver.exe'
    options = Options()
    # options.add_argument('--headless')

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    retry_count = 0
    max_retries = 3

    while retry_count < max_retries:
        try:
            driver.get('https://www.amazon.in/')
            time.sleep(5)
            search_box = driver.find_element(By.XPATH, '//*[@id="twotabsearchtextbox"]')
            keyword = product_name
            search_box.send_keys(keyword)
            search_button = driver.find_element(By.XPATH, '//*[@id="nav-search-submit-text"]')
            search_button.click()
            time.sleep(5)

            l6_list = []
            highest_percentage = 0

            for x in range(2, 5):
                css_selector = f'[data-cel-widget="search_result_{x}"]'
                element_with_data_cell_widget = driver.find_element('css selector', css_selector)
                l2 = preprocess_text(element_with_data_cell_widget.text).split()

                def convert_to_upper(item):
                    if isinstance(item, str):
                        return item.upper()
                    return item
                l5 = [convert_to_upper(item) for item in l2]

                # Calculate the percentage of elements in l3 that exist in l5
                common_elements = set(l3).intersection(l5)
                percentage_common = len(common_elements) / len(l3) * 100

                if percentage_common == 100:
                    for i in l2:
                        if '₹' in i and '/' not in i and '(' not in i:
                            l6_list.append(i.replace(',', ''))
                elif percentage_common > highest_percentage and percentage_common > 65:
                    # Update highest_percentage and l6_list for non-100 percent matches
                    highest_percentage = percentage_common
                    l6_list = []
                    for i in l2:
                        if '₹' in i and '/' not in i and '(' not in i:
                            l6_list.append(i.replace(',', ''))

            break

        except Exception as e:
            print(f"An error occurred for product '{product_name}': {e}")
            driver.quit()
            retry_count += 1
            if retry_count < max_retries:
                print(f"Retrying the search for product '{product_name}'...")
                time.sleep(5)
                continue
            else:
                print(f"Maximum retries reached for product '{product_name}'. Skipping...")
                return

    def extract_value(element):
        return int(element[1:])

    # Convert elements to integers and find the minimum value
    int_elements = list(map(extract_value, l6_list))
    if not int_elements:
        # If the list is empty, set lowest value to 0
        lowest_value = '₹0'
    else:
        min_value = min(int_elements)
        # Find the element with the lowest value
        lowest_value = l6_list[int_elements.index(min_value)]

    # Write data to CSV
    writer.writerow([today, product_name, lowest_value])

    driver.quit()

l1 = create_list()

# Create and open the CSV file in write mode
with open('output.csv', mode='w', encoding="utf-8", newline='') as file:
    writer = csv.writer(file)

    # Write the header row
    writer.writerow(['Date', 'Product Name', 'Lowest Value'])

    for j in l1:
        l = j.split()

        def convert_to_upper(item):
            if isinstance(item, str):
                return item.upper()
            return item

        l4 = [convert_to_upper(item) for item in l]
        
        # Pass the writer to the price_value function
        price_value(j, l4, writer)