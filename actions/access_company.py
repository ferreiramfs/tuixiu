from selenium.webdriver.common.by import By
from utils import general
import time

def execute(driver, company):
    driver.switch_to.default_content()
    time.sleep(0.5)
    
    driver.find_element(By.ID, 'div-campo-clicavel-busca').click()
    driver.find_element(By.ID, "ipt-txt-barra-busca-empresa").send_keys(company)
    driver.find_element(By.XPATH, '//*[@id="div-busca-empresa"]/div[2]/i').click()
    
    time.sleep(0.5)
    driver.find_element(By.XPATH, '//*[@id="lista-retorno-empresas-busca"]/li/span[1]/span[2]/h6').click()
    time.sleep(0.5)

    general.waiter(driver)