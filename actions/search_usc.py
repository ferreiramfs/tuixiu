from selenium.webdriver.common.by import By
from utils import general

def execute(driver, search_key, usc_type, logger=None, type='code'):

        search_type = {'code': ['1'],
                        'name': ['2']}
        
        usc_types = {
             'Unidade': ['//form[@id="cad005"]/table/tbody/tr[2]/td/table//tbody/tr', './td[1]/a', 'inativo'],
             'Setor': ['//form[@id="cad006"]/table//tbody/tr', './td[1]/a', 'inativo'],
             'Cargo': ['//form[@id="cad004"]/table//tbody/tr', './td[1]', 'pesquisaInativo']
        }

        driver.find_element(By.NAME, "nomeSeach").send_keys(search_key)
        driver.find_element(By.ID, usc_types[usc_type][2]).click()


        general.codigo_js(driver, 'browse')
        general.waiter(driver)

        rows = driver.find_elements(By.XPATH, usc_types[usc_type][0])

        for row in rows:

            tds = row.find_elements(By.TAG_NAME, "td")

            if len(tds) >= 2:
                current_key = row.find_element(By.XPATH, './td[' + search_type[type][0] + ']').text

                if search_key.strip().lower() == current_key.strip().lower():
                    
                    row.find_element(By.XPATH, usc_types[usc_type][1]).click()

                    general.waiter(driver)
                    
                    return(True)

        return(False)