from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common import action_chains
from selenium.webdriver.chrome.options import Options
from pathlib import Path
import re
import time
import os

class PageObject:

    def __init__(self,driver,url):
        self.driver = driver
        self.url = url
    
    def go_to_site(self):
        self.driver.get(self.url)
        self.driver.implicitly_wait(1)
    
    def close(self):
        if self.driver != None:
            self.driver.quit()

    def find_first_by_XPATH(self, xpath):
        assert self.driver.find_element(By.XPATH, xpath), 'Не найден элемент '+str(xpath)
        return self.driver.find_element(By.XPATH, xpath)

    def find_list_by_XPATH(self, xpath):
        assert self.driver.find_elements(By.XPATH, xpath), 'Не найдены элементы '+str(xpath)
        return self.driver.find_elements(By.XPATH, xpath)

    def click_on_element(self, element):
        element.click()

    def change_tab(self, tab_number):
        self.driver.switch_to.window(self.driver.window_handles[tab_number])

    def get_current_url(self):
        return self.driver.current_url
    
    def get_title(self):
        return self.driver.title

    def scroll_to_element(self, element):
        action_chains.ActionChains(self.driver).scroll_to_element(element).perform()

def test_scenario_1():
    main_page = PageObject(webdriver.Chrome(),"https://saby.ru/")
    main_page.go_to_site()
    button = main_page.find_first_by_XPATH("//div[@class = 'sbisru-Header-ContactsMenu js-ContactsMenu']/div[1]")
    main_page.click_on_element(button)
    button = main_page.find_first_by_XPATH("//a[@href = '/contacts']")
    main_page.click_on_element(button)
    button = main_page.find_first_by_XPATH("//a[@href = 'https://tensor.ru/']")
    main_page.click_on_element(button)
    main_page.change_tab(1)
    main_page.find_first_by_XPATH("//p[text()='Сила в людях']")
    button = main_page.find_first_by_XPATH("//a[@href = '/about']")
    main_page.click_on_element(button)
    assert main_page.get_current_url()=="https://tensor.ru/about", "Не выполнился переход по ссылке"
    block_working = main_page.find_first_by_XPATH("//div[@class = 'tensor_ru-container tensor_ru-section tensor_ru-About__block3']")
    main_page.scroll_to_element(block_working)
    photos = main_page.find_list_by_XPATH("//img[@class='tensor_ru-About__block3-image new_lazy loaded']")
    width = photos[0].get_attribute("width")
    height = photos[0].get_attribute("height")
    for photo in photos:
        assert width == photo.get_attribute("width"), "Не соответствует ширина"
        assert height == photo.get_attribute("height"), "Не соответствует высота"
    main_page.close()

def test_scenario_2():
    main_page = PageObject(webdriver.Chrome(),"https://saby.ru/")
    main_page.go_to_site()
    button = main_page.find_first_by_XPATH("//div[@class = 'sbisru-Header-ContactsMenu js-ContactsMenu']/div[1]")
    main_page.click_on_element(button)
    button = main_page.find_first_by_XPATH("//a[@href = '/contacts']")
    main_page.click_on_element(button)
    region_text = main_page.find_first_by_XPATH("//span[@class='sbis_ru-Region-Chooser__text sbis_ru-link']")
    assert region_text.text == "Тюменская обл.", "Неправильно определён регион"
    partners_list = main_page.find_list_by_XPATH("//div[@class='controls-ListView__itemV-relative controls-ListView__itemV controls-ListView__item_default controls-ListView__item_contentWrapper js-controls-ListView__editingTarget  controls-ListView__itemV_cursor-pointer  controls-ListView__item_showActions js-controls-ListView__measurableContainer controls-ListView__item__unmarked_default controls-ListView__item_highlightOnHover controls-hover-background-default controls-Tree__item']")
    assert len(partners_list)>0, "Нет списка партнёров"
    main_page.click_on_element(region_text)
    time.sleep(0.5)
    button = main_page.find_first_by_XPATH("//span[@title='Камчатский край']")
    main_page.click_on_element(button)
    time.sleep(2)
    region_text = main_page.find_first_by_XPATH("//span[@class='sbis_ru-Region-Chooser__text sbis_ru-link']")
    assert region_text.text == "Камчатский край", "Неправильно выбран регион"
    assert partners_list != main_page.find_list_by_XPATH("//div[@class='controls-ListView__itemV-relative controls-ListView__itemV controls-ListView__item_default controls-ListView__item_contentWrapper js-controls-ListView__editingTarget  controls-ListView__itemV_cursor-pointer  controls-ListView__item_showActions js-controls-ListView__measurableContainer controls-ListView__item__unmarked_default controls-ListView__item_highlightOnHover controls-hover-background-default controls-Tree__item']"), "Не изменился список партнёров"
    assert "41-kamchatskij-kraj" in str(main_page.get_current_url()), "Неправильный URL"
    assert "Камчатский край" in str(main_page.get_title()), "Неправильный тайтл сайта"
    main_page.close()

def test_scenario_3():
    chrome_options = Options()
    chrome_options.add_argument("--allow-running-insecure-content")  
    chrome_options.add_argument("--unsafely-treat-insecure-origin-as-secure=https://saby.ru/")  
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": os.path.abspath("files"),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    main_page = PageObject(webdriver.Chrome(options=chrome_options),"https://saby.ru/")
    main_page.go_to_site()
    button = main_page.find_first_by_XPATH("//a[@href='/download']")
    main_page.click_on_element(button)
    button = main_page.find_first_by_XPATH("//a[@href='https://update.saby.ru/Sbis3Plugin/master/win32/sbisplugin-setup-web.exe']")
    main_page.click_on_element(button)
    time.sleep(5)
    file_path = Path("files/sbisplugin-setup-web.exe")
    assert file_path.is_file()
    size_on_site = float(re.search(r'\d{2,3}.\d{2,3}',"Скачать (Exe 10.43 МБ)").group(0))
    size_on_disk = round(Path("files/sbisplugin-setup-web.exe").stat().st_size / 1024 / 1024,2)
    assert size_on_disk == size_on_site
    Path.unlink(file_path,missing_ok=True)
