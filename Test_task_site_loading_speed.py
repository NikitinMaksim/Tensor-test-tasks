from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

options = Options()
options.add_argument("--headless")

prefs = {
    "download_restrictions": 3,
}

options.add_experimental_option(
    "prefs", prefs
)

driver = webdriver.Chrome(options=options)

start_url = input("Введите стартовый url: ")

pages = dict()

def visit_url(url):
    if url in pages:
        return
    try:
        driver.get(url)
        
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.TAG_NAME,"body")))

        timing_data = driver.execute_script("return window.performance.timing;")

        navigation_start = timing_data['navigationStart']
        load_event_end = timing_data['loadEventEnd']
        page_load_time = load_event_end - navigation_start

        pages[url] = page_load_time

        print(f'Visiting: {url}, load time: {page_load_time}')

        links = driver.find_elements(By.TAG_NAME,'a')
        hrefs = set()
        for link in links:
            hrefs.add(link.get_attribute('href'))

        for href in hrefs:
            if href and href.startswith(start_url) and not '#' in href and not href in pages:
                visit_url(href)

    except Exception as e:
        print(F"Error visiting {url} : {e}")

visit_url(start_url)

print("__________________Finished testing__________________")

for line in sorted(pages, key=pages.get, reverse=True):
    print(f'{pages[line]}ms - {line}')

driver.quit()