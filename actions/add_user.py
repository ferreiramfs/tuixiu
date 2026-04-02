import time
from utils import general
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from datetime import date, datetime

def execute(inputs, data, driver, logger=None):

    nome_completo = data['Nome']

    general.codigo_js(driver, 'inc')

    if inputs['Empresa'] in ['3778', 'imtep']:
        user = nome_completo.split()[0] + '.' + nome_completo.split()[1] + inputs['Base SOC']
        driver.find_element(By.ID, "nome").send_keys(nome_completo)
    else:
        nomes = nome_completo.strip().split()
        user = inputs['Empresa'].replace(' ', '') + '.' + nomes[0] + ''.join(s[0] for s in nomes[1:])
        driver.find_element(By.ID, "nome").send_keys('Cliente - ' + inputs['Empresa'] + ' - ' + nome_completo)
    
    driver.find_element(By.ID, "email").send_keys(data['Email'])
    
    if inputs['Cadastra CPF']:
        cpf = str(data['CPF']).strip('-').strip('.')
        cpf = (11 - len(cpf)) * '0' + cpf
        driver.find_element(By.ID, "cpf").send_keys(cpf)

    general.codigo_js(driver, 'save')
    general.codigo_js(driver, 'usuario')
    driver.switch_to.alert.accept()
    time.sleep(0.25)

    user_type = Select(driver.find_element(By.ID, "tipoUsuario"))
    user_type.select_by_visible_text("Administrativo")

    driver.find_element(By.ID, "apelido").send_keys(user)

    pswrd = 'mudar123'
    driver.find_element(By.ID, "senha").send_keys(pswrd)
    driver.find_element(By.ID, "senhaRedigitada").send_keys(pswrd)
    
    general.codigo_js(driver, 'save')

    usuario_resetado = driver.find_element(By.XPATH, '//*[@id="conteudosTable"]').text
    logger(usuario_resetado)

    general.codigo_js(driver, 'alt')
    
    data = driver.find_element(By.XPATH, '//*[@name="dataLimiteAcesso"]')
    hoje = datetime.strptime(str(date.today()), '%Y-%m-%d')
    mes = hoje.month if hoje.month > 9 else '0' + str(hoje.month)
    nova_data = '01' + str(mes) + str(hoje.year+1)
    data.clear()
    data.send_keys(nova_data)

    general.codigo_js(driver, 'save')
    
    general.codigo_js(driver, 'volta')

    out_data = {'nome': nome_completo
                , 'usuario': user.lower()
                , 'senha': pswrd
                , 'id': '3134'}

    return(out_data) 