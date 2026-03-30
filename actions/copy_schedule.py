from utils import general
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

def execute(driver):
    
    general.codigo_js(driver, 'acessoAgenda')
    general.codigo_js(driver, 'alt')

    schedule_access = {'acessa_agenda': True, 'entrarAgendaComo': None, 'permiteImprimirPedidoExame': None, 'exibeAlertaFuncionaCompromissoDuplicado': None, 
                       'numeroDiasConsiderarCompromissoDuplicado': None, 'tempoConsulta': None, 'tempoConsultaTarde': None, 'quantidadePeriodoGrade': None,
                       'valorInicioHora': None, 'valorFimHora': None, 'quantidadeAtendimentoSimultaneo': None, 'limiteComproNaoExterno': None, 'assuntoEmail': None,
                       'textoEmail': None, 'textoAvisoAgenda': None, 'enviarExamesNoEmail': None, 'visualizaProfissionalDaAgenda': None, 
                       'preencherEmBrancoGradeDisponivel': None, 'permiteDuplicarCompromissoMesmoHorario': None, 'bloquearcadastromanualhorainiciofimcompromisso': None,
                       'utilizaHoraFimCompromisso': None, 'exibeResponderEmailAgenda': None, 'bloqueiaInclusaoCompromissoSemGradeHorario': None, 
                       
                       'usuarioExternoAgenda': None, 'quantidadeDiasAdiante': None, 'quantidadeCompromissosDia': None, 'limiteComproExterno': None, 
                       'codigoTipoExibicaoDadosEmpresa': None, 'enviaEmailPorCompromissoCadastrado': None, 'emailPorCompromissoCadastrado': None, 
                       'permiteReservaSemFuncionario': None, 'permiteExcluirCompromisso': None, 'agendaExternaRecebeEmailPorCompromissoCadastrado': None,
                       
                       'participaAgenda': None, 'usuarioAgendaListSel': None, 'usuarioConsultaListSel': None, 'agendasSocnetSelecionadas': None,
                       
                       'mapa': None, 'utilizaMapaIndividual': None}
    
    schedule_access['entrarAgendaComo'] = Select(driver.find_element(By.NAME, "entrarAgendaComo")).first_selected_option.get_attribute("value")

    checks = ['permiteImprimirPedidoExame', 'exibeAlertaFuncionaCompromissoDuplicado', 'enviarExamesNoEmail', 'visualizaProfissionalDaAgenda'
                  , 'preencherEmBrancoGradeDisponivel', 'permiteDuplicarCompromissoMesmoHorario', 'bloquearcadastromanualhorainiciofimcompromisso'
                  , 'utilizaHoraFimCompromisso', 'exibeResponderEmailAgenda', 'bloqueiaInclusaoCompromissoSemGradeHorario'
                  
                  , 'usuarioExternoAgenda'

                  , 'participaAgenda', 'utilizaMapaIndividual']
        
    for i in checks:
        schedule_access[i] = driver.find_element(By.NAME, i).is_selected()

    types = ['numeroDiasConsiderarCompromissoDuplicado', 'tempoConsulta', 'tempoConsultaTarde', 'quantidadePeriodoGrade', 'valorInicioHora'
                , 'valorFimHora', 'quantidadeAtendimentoSimultaneo', 'quantidadeLimiteDeCompromissosDiaAgenda', 'assuntoEmail']

    for i in types:
        schedule_access[i] = driver.find_element(By.NAME, i).get_attribute("value")
    
    out_type = ['quantidadeDiasAdiante', 'quantidadeCompromissosDia', 'limiteComproExterno']
    out_check = ['enviaEmailPorCompromissoCadastrado', 'permiteReservaSemFuncionario', 'permiteExcluirCompromisso', 'agendaExternaRecebeEmailPorCompromissoCadastrado']

    schedule_access['textoEmail'] = driver.find_element(By.NAME, 'textoEmail').text
    schedule_access['textoAvisoAgenda'] = driver.find_element(By.NAME, 'textoAvisoAgenda').text

    if schedule_access['usuarioExternoAgenda']:
        for i in out_type:
            schedule_access[i] = driver.find_element(By.ID, i).get_attribute("value")

        schedule_access['codigoTipoExibicaoDadosEmpresa'] = Select(driver.find_element(By.NAME, "codigoTipoExibicaoDadosEmpresa")).first_selected_option.get_attribute("value")
        
        for j in out_check:
            schedule_access[j] = driver.find_element(By.NAME, j).is_selected()
        
        if schedule_access['enviaEmailPorCompromissoCadastrado']:
            schedule_access['emailPorCompromissoCadastrado'] = driver.find_element(By.NAME, 'emailPorCompromissoCadastrado').get_attribute("value")

    if schedule_access['participaAgenda']:
        schedules_list = Select(driver.find_element(By.ID, "usuarioAgendaListSel")).options
        schedule_access['usuarioAgendaListSel'] = [opt.get_attribute("value") for opt in schedules_list]
        schedules_read_only = Select(driver.find_element(By.ID, "usuarioConsultaListSel")).options
        schedule_access['usuarioConsultaListSel'] = [opt.get_attribute("value") for opt in schedules_read_only]

        schedules_socnet = Select(driver.find_element(By.ID, "agendasSocnetSelecionadas")).options
        schedule_access['agendasSocnetSelecionadas'] = [opt.get_attribute("value") for opt in schedules_socnet]

    schedule_access['mapa'] = Select(driver.find_element(By.NAME, "mapa")).first_selected_option.get_attribute("value")
    schedule_access['utilizaMapaIndividual'] = driver.find_element(By.ID, 'utilizaMapaIndividual').is_selected()

    general.codigo_js(driver, 'can')

    general.codigo_js(driver, 'volta')

    if schedule_access['usuarioAgendaListSel'] in [[], None] and schedule_access['usuarioConsultaListSel'] in [[], None] and schedule_access['agendasSocnetSelecionadas'] in [[], None]:
        schedule_access['acessa_agenda'] = False
        print('Origin user without schedules')

    return(True, schedule_access)