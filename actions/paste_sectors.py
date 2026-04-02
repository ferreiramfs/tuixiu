from utils import general
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

def execute(driver, data):
    
    general.codigo_js(driver, 'empresasUsu')

    driver.execute_script("javascript:selecionaEmpUsu('" + str(data['Codigo Empresa']) + "','" + data['Empresa'] +"');")

    general.codigo_js(driver, 'alt')

    #Selection the sectors
    select = Select(driver.find_element(By.ID, 'grupoSel'))

    unidades = data['Unidades'].split(',')

    for elem in unidades:
        select.select_by_value(elem)            
        driver.execute_script('javascript:fassociar();')
        select.deselect_by_value(elem)

    general.codigo_js(driver, 'save')

    general.codigo_js(driver, 'volta')
    general.codigo_js(driver, 'volta')
    return(True)