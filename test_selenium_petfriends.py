from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC

import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()

@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    """"НЕЯВНОЕ ОЖИДАНИЕ"""
    driver.implicitly_wait(10)
    driver.get('https://petfriends.skillfactory.ru/login')
    driver.maximize_window()
    yield driver
    driver.quit()

def test_show_all_my_pets_name_age(driver):

    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('sereja@yandex.ru')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('12345test')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    # Нажимаем на кнопку мои питомцы
    driver.find_element(By.XPATH, '//a[text()="Мои питомцы"]').click()
    #Проверяем что мы на странице Мои питомцы
    assert driver.find_element(By.TAG_NAME, 'h2').text == "test_name_OAP"

    images = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    names = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    descriptions = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i]
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0

def test_show_quantity_my_pets(driver):
    """Проверяем, что присутствуют все питомцы:
    -находим кол-во питомцев по статистике и провер что кол-во соотв числу в таблице"""
    """ЯВНЫЕ ОЖИДАНИЯ"""
    # Вводим email, заменить на свой email для того чтобы получить свой список питомцев
    WDW(driver, 10).until(EC.presence_of_element_located((By.ID, 'email'))).send_keys('sereja@yandex.ru')
    # Вводим пароль
    WDW(driver, 10).until(EC.presence_of_element_located((By.ID, 'pass'))).send_keys('12345test')
    # Нажимаем на кнопку входа в аккаунт
    WDW(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))).click()
    WDW(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'h1'))).text == "PetFriends"
    time.sleep(1)
    # Нажимаем на кнопку Мои питомцы
    WDW(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[text()="Мои питомцы"]'))).click()

    pets_number = WDW(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class=".col-sm-4 left"]'))).text.split('\n')[1].split(': ')[1]
    pets_count = WDW(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//table[@class="table table-hover"]/tbody/tr')))
    assert int(pets_number) == len(pets_count)












