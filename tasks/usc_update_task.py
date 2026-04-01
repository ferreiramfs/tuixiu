import time
from utils import browser
from actions import access_company, access_page, search_usc, update_usc, get_usc
import pandas as pd


def execute(inputs, logger=None):

    tempo = time.time()

    tipo_update = inputs['USC']

    filepath = inputs.get('Arquivo CSV')
    usc_param = {
        'Unidade': ['231'],
        'Setor': ['220'],
        'Cargo': ['225']
    }

    if filepath:
        raw_data = pd.read_csv(filepath)
        
        usc_names = raw_data['nome']
        usc_codes = raw_data['codigo']
        usc_empresas = raw_data['empresa']

        empresas_unicas = list(set(usc_empresas))

        data = pd.DataFrame({
            'empresa': usc_empresas,
            'nome': usc_names,
            'codigo': usc_codes,
            'status': 'Pendente'
        })

        if inputs['Validação'] == 'Sim':
            processed_data = get_usc.execute(empresas_unicas, data, tipo_update, logger=logger)
        else:
            processed_data = data

    else:
        
        usc_names = [inputs['Nome USC']]
        usc_codes = [inputs['Codigo RH']]
        usc_empresas = [inputs['Empresa']]
        
        if usc_names == '' or usc_codes == '' or usc_empresas == '':
            logger('Os campos Nome USC, Codigo RH e Empresa são obrigatórios')
            return(False)
        
        processed_data = pd.DataFrame({
            'empresa': usc_empresas,
            'nome': usc_names,
            'codigo': usc_codes,
            'status': 'Pendente'
        })

    driver = browser.get_driver(inputs['Base SOC'])

    previous_emp = ''
    reload_page = True

    mask = processed_data['status'] == 'Pendente'
    for index in processed_data[mask].index:
        row = data.loc[index]

        try:
            if row['empresa'] != previous_emp:
                
                driver.switch_to.default_content()
                driver.execute_script("javascript:Empresas(); hideall();hidemenus('');menu_close();avisoLogin();")
                access_company.execute(driver, str(row['empresa']))
                previous_emp = row['empresa']

            if reload_page:
                access_page.execute(driver, usc_param[tipo_update][0])

            status = search_usc.execute(driver, row['nome'], tipo_update , logger, type='name')

            if status:
                status_update = update_usc.execute(driver, tipo_update, row['codigo'], inputs['Tipo'])
                reload_page = True

                if status_update[0]:
                    logger(f"{tipo_update}: {row['nome']} atualizado com sucesso")
                    data.at[index, 'status'] = 'OK'
                    
                else:
                    logger(f"{tipo_update}: {row['nome']} {status_update[1]}")
                    data.at[index, 'status'] = status_update[1]

            else:
                logger(f"{tipo_update}: {row['nome']} não encontrada")
                reload_page = False
                data.at[index, 'status'] = 'Não encontrado'
    
        except:
            
            logger(f"{tipo_update}: {row['nome']} erro")
            data.at[index, 'status'] = 'Erro'

            driver = browser.get_driver(inputs['Base SOC'])
            previous_emp = ''
            reload_page = True
            
    data.to_excel('data/USC_alterados.xlsx', index=False)

    tempo = round(time.time() - tempo, 2)
    logger("Tarefa Finalizada --- %s seconds" % (tempo))