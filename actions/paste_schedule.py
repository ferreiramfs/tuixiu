from utils import general
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

def execute(driver, schedule_access):
    
    if schedule_access['acessa_agenda']:

        general.codigo_js(driver, 'acessoAgenda')
        general.codigo_js(driver, 'alt')

        select_show = Select(driver.find_element(By.NAME, 'entrarAgendaComo'))
        if schedule_access['entrarAgendaComo'] != '':
            select_show.select_by_value(schedule_access['entrarAgendaComo'])

        checks = ['permiteImprimirPedidoExame', 'exibeAlertaFuncionaCompromissoDuplicado', 'enviarExamesNoEmail', 'visualizaProfissionalDaAgenda'
                  , 'preencherEmBrancoGradeDisponivel', 'permiteDuplicarCompromissoMesmoHorario', 'bloquearcadastromanualhorainiciofimcompromisso'
                  , 'utilizaHoraFimCompromisso', 'exibeResponderEmailAgenda', 'bloqueiaInclusaoCompromissoSemGradeHorario'
                  
                  , 'usuarioExternoAgenda'

                  , 'participaAgenda', 'utilizaMapaIndividual']
        
        for i in checks:
            status = driver.find_element(By.NAME, i).is_selected()
            if (schedule_access[i] and not status) or (not schedule_access[i] and status):
                driver.find_element(By.NAME, i).click()

        types = ['numeroDiasConsiderarCompromissoDuplicado', 'tempoConsulta', 'tempoConsultaTarde', 'quantidadePeriodoGrade', 'valorInicioHora'
                 , 'valorFimHora', 'quantidadeAtendimentoSimultaneo', 'quantidadeLimiteDeCompromissosDiaAgenda', 'assuntoEmail', 'textoEmail', 'textoAvisoAgenda',]

        for i in types:
            campo = driver.find_element(By.NAME, i)
            campo.clear()
            campo.send_keys(schedule_access[i])
        
        out_type = ['quantidadeDiasAdiante', 'quantidadeCompromissosDia', 'limiteComproExterno']
        out_check = ['enviaEmailPorCompromissoCadastrado', 'permiteReservaSemFuncionario', 'permiteExcluirCompromisso', 'agendaExternaRecebeEmailPorCompromissoCadastrado']

        if schedule_access['usuarioExternoAgenda']:
            for i in out_type:
                campo = driver.find_element(By.ID, i)
                campo.clear()
                campo.send_keys(schedule_access[i])
            
            select_show = Select(driver.find_element(By.NAME, 'codigoTipoExibicaoDadosEmpresa'))
            select_show.select_by_value(schedule_access['codigoTipoExibicaoDadosEmpresa'])

            for j in out_check:
                box = driver.find_element(By.NAME, j)
                status = box.is_selected()
                if (schedule_access[j] and not status) or (not schedule_access[j] and status):
                    box.click()
            
            if schedule_access['enviaEmailPorCompromissoCadastrado']:
                email = driver.find_element(By.NAME, 'emailPorCompromissoCadastrado')
                email.clear()
                email.send_keys(schedule_access['emailPorCompromissoCadastrado'])
            
        select_show = Select(driver.find_element(By.NAME, 'mapa'))
        if schedule_access['mapa'] != '0':
            select_show.select_by_value(schedule_access['mapa'])

        #Writing schedules and read-only schedules
        schedules = {'edit_schedules': ["usuarioAgendaListSel", "javascript:fdesassociarAgenda('acessoTotal');", "usuarioAgendaList", "javascript:fassociarAgenda('acessoTotal');"]
                     , 'consult_schedules': ["usuarioConsultaListSel", "javascript:fdesassociarAgenda('acessoConsulta');", "usuarioConsultaList", "javascript:fassociarAgenda('acessoConsulta');"]}

        for i in schedules:
            select_rem = Select(driver.find_element(By.ID, schedules[i][0]))
            list_rem = [opt.get_attribute("value") for opt in select_rem.options]

            for elem in list_rem:
                select_rem.select_by_value(elem)

            driver.execute_script(schedules[i][1])
            
            #Selecting companies
            select_schedules = Select(driver.find_element(By.ID, schedules[i][2]))

            for elem in schedule_access[schedules[i][0]]:
                select_schedules.select_by_value(elem)            
            driver.execute_script(schedules[i][3])
        
        driver.find_element(By.ID, 'limparSelecaoAgendaSocnet').click()
        driver.find_element(By.ID, 'pesquisarAgendaSocnet').click()

        general = driver.find_element(By.ID, 'lista-agendas')
        schedules_list = general.find_elements(By.TAG_NAME, 'li')
        
        #Finding and selecting SOCNET schedules
        for schedule in schedules_list:
            schedule_cod = schedule.get_attribute('data-codigo-agenda')
            if schedule_cod in schedule_access['agendasSocnetSelecionadas']:
                schedule_button = schedule.find_element(By.TAG_NAME, 'input')
                driver.execute_script("arguments[0].click();", schedule_button)
        
        driver.execute_script('javascript:selecionaAgendasSocnet();')

        general.codigo_js(driver, 'save')

        general.codigo_js(driver, 'volta')

        return(True)
    
    else:
        return(True)