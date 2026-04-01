from selenium.webdriver.common.by import By
from utils import general

def execute(driver, usc, new_data, update_type = 'Codigo RH'):
        
        general.codigo_js(driver, 'alt')
        general.waiter(driver)

        usc_type = {
                'Unidade': ['selecaoUnidadeVo.codigoRH', 'selecaoUnidadeVo.nome', 'alertaHistoricoUnidade', 'javascript:ignoraHistoricoUnidade();'],
                'Setor': ['setorVo.codigoRH', 'setorVo.nome', 'alertaHistoricoSetor', 'javascript:ignoraHistoricoSetor();'],
                'Cargo': ['cargo.codigoRH', 'cargo.nome', 'alertaHistoricoCargo', 'javascript:ignoraHistoricoCargo();']
        }
        
        activated = False
        if update_type in ['Codigo RH', 'Ativar']:

                current_status = driver.find_element(By.ID, 'ativo')

                if not current_status.is_selected():
                        current_status.click()
                        activated = True

        elif update_type == 'Renomear':
                pass
        else:
                return(False, 'Tipo de atualização inválido')

        if update_type == 'Codigo RH' and str(current_codrh) != str(new_data):

                current_codrh = driver.find_element(By.NAME, usc_type[usc][0]).get_attribute("value")

                cod_rh = driver.find_element(By.NAME, usc_type[usc][0])

                cod_rh.clear()
                cod_rh.send_keys(new_data)

        
        elif update_type == 'Renomear':

                name_usc = driver.find_element(By.NAME, usc_type[usc][1])

                name_usc.send_keys('.')
        
        general.codigo_js(driver, 'save')
        general.waiter(driver)

        return_data = {
                'Codigo RH': 'código já cadastrado para outro USC',
                'Renomear': 'erro ao tentar renomear o USC',
                'Ativar': 'USC já estava ativo'
        }

        erro = driver.find_elements(By.ID, 'err')
        hist_alteracao = driver.find_elements(By.ID, usc_type[usc][2])

        if not activated and update_type == 'Ativar': 
                return(False, return_data[update_type])

        elif erro and erro[0].is_displayed():

                driver.execute_script("javascript:closeIcones();")
                if activated and update_type == 'Ativar':
                        current_status.click()
                return(False, return_data[update_type])
        
        elif hist_alteracao and hist_alteracao[0].is_displayed():
                driver.execute_script(usc_type[usc][3])
                return(True, 'OK')
        
        else:
                return(True, 'OK')
