import time
import pandas as pd
from utils import browser
from actions import access_page, add_user, copy_access, search_user, copy_company, copy_schedule, paste_access, paste_company, paste_schedule, paste_sectors

def execute(inputs, logger=None):

    tempo = time.time()
    filepath = inputs.get('Arquivo CSV')
    
    if filepath:
        raw_data = pd.read_csv(filepath)

    else:

        dados = {'Nome': [inputs['Nome Completo']],
                'Email': [inputs['Email']],}

        if inputs['Cadastra CPF']:
            dados['CPF'] = [inputs['CPF']]

        raw_data = pd.DataFrame(dados)

    driver = browser.get_driver(inputs['Base SOC'])
    access_page.execute(driver, "189")

    if not search_user.execute(driver, inputs['Usuario Espelho']):
        logger('Usuário Espelho não encontrado na base')
    else:

        copies = {'access': [True, copy_access.execute, '', paste_access.execute]
                  ,'company': [True, copy_company.execute, {}, paste_company.execute]
                  ,'schedule': [inputs['Espelhar Agenda'], copy_schedule.execute, {}, paste_schedule.execute]}

        for i in copies:
            
            if copies[i][0]:

                status = copies[i][1](driver)

                if not status[0]:
                    logger(status[1])
                    tempo = round(time.time() - tempo, 2)
                    logger("Tarefa Finalizada --- %s seconds" % (tempo))
                    return(False)

                copies[i][2] = status[1]

        users_data = pd.DataFrame(columns=['nome', 'usuario', 'senha', 'id'])
        for _, row in raw_data.iterrows():

            data = row.to_dict()

            user_data = add_user.execute(inputs, data, driver, logger)

            users_data.loc[len(users_data)] = user_data
            print(users_data)

            for i in copies:

                if copies[i][0]:

                    status = copies[i][3](driver, copies[i][2])
            
            if 'Unidades' in data.keys() and data['Unidades'] != 'Todas':
                paste_sectors.execute(driver, data)
        
        users_data.to_excel('data/usuarios_criados.xlsx', index=False)

    tempo = round(time.time() - tempo, 2)
    logger("Tarefa Finalizada --- %s seconds" % (tempo))