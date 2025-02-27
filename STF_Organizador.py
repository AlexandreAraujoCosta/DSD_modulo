import dsd, os

path = 'ADItotal\\'
lista = os.listdir(path)

dsd.limpar_arquivo('ADItotal(sem_andamentos).txt')
dsd.limpar_arquivo('ADItotal(andamentos).txt')
dsd.limpar_arquivo('excluidos.txt')


partes_total = []
dados_csv = []
andamentos_csv = []
lista_excluidos = []
dsd.limpar_arquivo('ADItotalpartes.txt')
dsd.write_csv_header('ADItotalpartes.txt', 'nome, tipo, processo')
contador=0
excluidos = 0



for item in lista[0:]:
    gravar_processo = True
    contador = contador +1
    nome_arquivo = path+item
    processo = item.replace('.txt','')
         
    # carrega dados do arquivo
    html = 'NA'
    html = dsd.carregar_arquivo(nome_arquivo)
    

    
    html = html.replace(',',';')
    html = html.replace('\n','')
    html = html.replace('  ',' ')
    
    # extrai as partes
    partes_string = dsd.extrair(html,'partes>>>>', '<div id="partes-resumidas">')
    partes = dsd.extrair_partes(partes_string)
        
    lista_das_partes = []
    lista_das_partes = dsd.listar_partes(partes_string, item.replace('.txt',''))
    
    for y in lista_das_partes:
        dsd.write_csv_line('ADItotalpartes.txt', y)
    
    # extrai os andamentos
    andamentos = dsd.extrair(html,'andamentos>>>>', 'pauta>>>>')
    andamentos = dsd.extrair_andamentos(andamentos)
    
    
    #extrai os elementos do código fonte
    codigofonte =dsd.extrair(html,'fonte>>>>', 'partes>>>>')
    
    eletronico_fisico =dsd.extrair(codigofonte,'bg-primary">','</span>')
    
    sigilo =dsd.extrair(codigofonte,'bg-success">','</span>')
    
    nome_processo =dsd.extrair(codigofonte,'-processo" value="','">')
    
    numerounico  = dsd.extrair(codigofonte,'-rotulo">','</div>')
    numerounico = dsd.extrair(numerounico,': ', '')
    
    relator = dsd.extrair(codigofonte,'Relator:','</div>')
    relator = relator.strip(' ')
    relator = relator.replace('MIN. ','')
    relator = dsd.remover_acentos(relator)
    
    redator_acordao = dsd.extrair(codigofonte,'>Redator do acórdão:','</div>')
    redator_acordao = dsd.remover_acentos(redator_acordao)
    redator_acordao = redator_acordao.replace('MIN. ','')
    redator_acordao = redator_acordao.strip(' ')
    redator_acordao = redator_acordao.replace ('MINISTRO ','')

    
    relator_ultimo_incidente = dsd.extrair(codigofonte,
                                      'Relator do último incidente:'
                                      ,'</div>')
    relator_ultimo_incidente = relator_ultimo_incidente.replace ('MIN. ','')
    relator_ultimo_incidente = relator_ultimo_incidente.replace ('MINISTRO ','')
    relator_ultimo_incidente = relator_ultimo_incidente.strip(' ')
    relator_ultimo_incidente = dsd.remover_acentos(relator_ultimo_incidente)
    ultimoincidente = dsd.extrair(relator_ultimo_incidente,"(",'')
    relator_ultimo_incidente = dsd.extrair(relator_ultimo_incidente,'','(')
    ultimoincidente = ultimoincidente.replace(')','')
    ultimoincidente = ultimoincidente.strip(' ')
    
    #extrai os elementos da aba informações
    informacoes = dsd.extrair(html,'informacoes>>>>', '>>>>')
    
    assuntos = dsd.extrair(informacoes, '<ul style="list-style:none;">', '</ul>')
    assuntos = dsd.limpar(assuntos)
    assuntos = dsd.extrair(assuntos,'<li>','')
    assuntos = assuntos.replace('</li>','')
    assuntos = dsd.limpar(assuntos)
    
 
    protocolo_data = dsd.extrair(informacoes, '<div class="col-md-5 processo-detalhes-bold m-l-0">', '</div>')
    protocolo_data = protocolo_data.strip(' ')
        
    orgaodeorigem = dsd.extrair(informacoes, '''Órgão de Origem:
                </div>
                <div class="col-md-5 processo-detalhes">''', '</div>')
    
    numerodeorigem = dsd.extrair(informacoes, '''Número de Origem:
                </div>
                <div class="col-md-5 processo-detalhes">''', '</div>')
    
    origem  = dsd.extrair(informacoes, '''Origem:
                </div>
                <div class="col-md-5 processo-detalhes">''', '</div>')
                
    procedencia = dsd.extrair(informacoes, '''<span id="descricao-procedencia">''', '</span>')
    procedencia = procedencia.replace('  ','')
    procedencia = dsd.extrair(procedencia, '', ' -')
    
    cc = 'NA'
    # extrai campos CC
    if 'ADI' in nome_processo or 'ADPF' in nome_processo or 'ADC' in nome_processo or 'ADO' in nome_processo:
        
        cc = dsd.extrair(html, 'cc>>>','')
    
            # extrai campo incidente
        incidentecc = dsd.extrair (cc, 
                                 'verProcessoAndamento.asp?incidente=',
                                 '">')   
        
        # extrai campos classe + liminar + numero
        cln = 'NA'
        cln = dsd.extrair(cc, 
                          '<div><h3><strong>', 
                          '</strong>')
        dsd.limpar_cln(cln)
        cln = cln.upper()
        
        # extrai numero
        numerocc = 'NA'
        numerocc = dsd.extrair (cln, ' - ', '')
        numerocc = dsd.limpar_numero(numerocc)
        
        # extrai liminar e classe    
        if 'LIMINAR' in cln:
            liminarcc = 'sim'
            classecc = dsd.extrair(cln, '', ' (MED') 
        else:
            liminarcc = 'não'
            classecc = dsd.extrair(cln, '', ' - ') 
        
        dsd.limpar_classe(classecc)
        classecc.upper()
        classecc = classecc.replace('ACAO DIRETA DE INCONSTITUCIONALIDADE','ADI')
        classecc = classecc.replace('AÇÃO DIRETA DE INCONSTITUCIONALIDADE','ADI')
        classecc = classecc.replace('ARGUIÇÃO DE DESCUMPRIMENTO DE PRECEITO FUNDAMENTAL','ADPF')
        
        
        # definição de campo: origem  
        origemcc = 'NA'
        origemcc = dsd.extrair(cc,'Origem:</td><td><strong>','</strong>')
        procedencia = procedencia.replace('***', dsd.limpa_estado(origemcc).replace('/', ''))
        
               
        ## definição de campo: entrada
        entradacc = dsd.extrair(cc,'Entrada no STF:</td><td><strong>','</strong>')
        entradacc = dsd.substituir_data(entradacc)
        
        ## definição de campo: relator
        relatorcc = dsd.extrair(cc,'Relator:</td><td><strong>','</strong>')
        relatorcc = relatorcc.replace('MINISTRO ','')
        relatorcc = relatorcc.replace('MINISTRA ','')
        relatorcc = dsd.remover_acentos(relatorcc)
        
        
        ## definição de campo: distribuição
        distribuicaocc = dsd.extrair(cc,'Distribuído:</td><td><strong>','</strong>')
        distribuicaocc = dsd.substituir_data(distribuicaocc)
        distribuicaocc = distribuicaocc.replace('-','/')
        
        
        ## definição de campo: requerente
        requerentecc = dsd.extrair(cc,'Requerente: <strong>','</strong>')
        requerentecc = requerentecc.replace('  ',' ')
        requerentecc = requerentecc.replace(' ;',';')
        requerentecc = requerentecc.replace('; ',';')

        requerentecc = requerentecc.replace('( CF','(CF')
        if '(CF' in requerentecc:
            requerentesplit = requerentecc.split('(CF')
            requerentecc = requerentesplit[0]
            requerentecc = requerentecc.strip()
            requerentetipo = requerentesplit[1]
            requerentetipo = dsd.extrair(requerentetipo, ';','')
            requerentetipo = requerentetipo.replace(')','')
            requerentetipocc = requerentetipo.replace('0','')
            requerentetipocc = requerentetipocc.replace(' 2','')

        else:
            requerentesplit = 'NA'
            requerentetipocc = 'NA'
        
        ## definição de campo: requerido
        requeridocc = dsd.extrair(cc,
                            'Requerido :<strong>',
                            '</strong>')
        
        ## definição de campo: dispositivo questionado
        dispositivoquestionadocc = dsd.extrair(cc,
                                         'Dispositivo Legal Questionado</b></strong><br /><pre>',
                                         '</pre>')
        dispositivoquestionadocc = dsd.limpar(dispositivoquestionadocc)
        
        ## definição de campo: resultado da liminar
        resultadoliminarcc = dsd.extrair(cc,
                                       'Resultado da Liminar</b></strong><br /><br />',
                                       '<br />')
        ### filtro resultado liminar
        # filtros
        resultadoliminarcc = resultadoliminarcc.replace('Aguardadno','Aguardadno')
        resultadoliminarcc = resultadoliminarcc.replace('Decisão Monocrática - "Ad referendum"','Deferida')
        resultadoliminarcc = resultadoliminarcc.replace('Monicrática','Monocrática')
        resultadoliminarcc = resultadoliminarcc.replace('Monoacrática','Monocrática')
        resultadoliminarcc = resultadoliminarcc.replace('Monocrático','Monocrática')
        resultadoliminarcc = resultadoliminarcc.replace('Decisão Monocrática Deferida -','Deferida')
        resultadoliminarcc = resultadoliminarcc.replace('"','')
        
        resultadoliminarcc = resultadoliminarcc.replace('Decisão Monocrática - ','')
        resultadoliminarcc = resultadoliminarcc.replace('liminar deferida','Deferida')
        
        resultadoliminarcc = resultadoliminarcc.upper()
        resultadoliminarcc = resultadoliminarcc.replace('PREJUDICADO','PREJUDICADA')
        resultadoliminarcc = resultadoliminarcc.replace('PROCEDENTE','DEFERIDA')
        resultadoliminarcc = resultadoliminarcc.replace('AD REFERENDUM','')
        resultadoliminarcc = resultadoliminarcc.replace('PROCEDENTE','DEFERIDA')
        
        ## definição de campo: resultado final
        resultadofinalcc = dsd.extrair(cc,
                                     'Resultado Final</b></strong><br /><br />',
                                     '<br />')
        
        ## definição de campo: decisão monocrática final
        if 'Decisão Monocrática Final</b></strong><br /><pre>' in cc:
            decisaomonofinal = dsd.extrair(cc,
                                           'Decisão Monocrática Final</b></strong><br /><pre>',
                                           '</pre>')
            decisaomonofinalcc = dsd.limpar(decisaomonofinal)
        else: 
            decisaomonofinalcc = 'NA'
            

        
             
        ## definição de campo: fundamento    
        if 'Fundamentação Constitucional</b></strong><br /><pre>' in cc:
            fundamentocc = dsd.extrair(cc,
                                 'Fundamentação Constitucional</b></strong><br /><pre>',
                                 '</pre>')
            fundamentocc = dsd.limpar(fundamentocc)
        else:
            fundamentocc = 'NA'
        
        ## definição de campo: indexação
        if 'Indexação</b></strong><br /><pre>' in cc:
            indexacaocc = dsd.extrair(cc,
                                'Indexação</b></strong><br /><pre>',
                                '</pre>')
            indexacaocc = dsd.limpar(indexacaocc)        
        else:
            indexacaocc = 'NA'
    
    else:
        gravar_processo = False
 
        
        
    # criação da variável dados extraídos, com uma lista de dados
    dados = [processo, incidentecc, requerentecc, 
             requerentetipocc, requeridocc, len(lista_das_partes), lista_das_partes ,len(andamentos),
             andamentos[:9], eletronico_fisico, sigilo, 
             numerounico, relatorcc, relator, redator_acordao, ultimoincidente,
             relator_ultimo_incidente, assuntos, procedencia, protocolo_data, 
             distribuicaocc, orgaodeorigem, 
             numerodeorigem, origem,    
             liminarcc, dispositivoquestionadocc, resultadoliminarcc, resultadofinalcc, 
             decisaomonofinalcc, fundamentocc, indexacaocc]
    #inserir aqui o conteúdo da lista acima, trocando [] por ''
    campos = '''processo, incidentecc, requerentecc, 
             requerentetipocc, requeridocc, len(partes),partes,len(andamentos),
             andamentos[:9], eletronico_fisico, sigilo, 
             numerounico, relatorcc, relator, redator_acordao, ultimoincidente,
             relator_ultimo_incidente, assuntos, procedencia, protocolo_data, 
             distribuicaocc, orgaodeorigem, 
             numerodeorigem, origem,  
             liminarcc, dispositivoquestionadocc, resultadoliminarcc, resultadofinalcc, 
             decisaomonofinalcc, fundamentocc, indexacaocc'''
    campos = campos.replace('\n','')
    campos = campos.replace('             ','')
    
    dados2 = [processo, len(andamentos), len(str(andamentos)), andamentos]
    campos2 = 'processo, len(andamentos), len(str(andamentos)), andamentos'
    
        
    dsd.write_csv_header('ADItotal(sem_andamentos).txt',campos)
    dsd.write_csv_header('excluidos.txt','processos excluídos')
    dsd.write_csv_header('ADItotal(andamentos).txt',campos2)
    
    # grava de 500 em 500
    if andamentos == []:
        andamentos = ['SEM ANDAMENTOS CADASTRADOS']
        
    if  (gravar_processo == False or 
         nome_processo == 'NA' or 
          len(lista_das_partes) == 0 or
          'IMPOSSIBILIDADE DE PROCESSAMENTO' in andamentos[0] or
          'REAUTUADO' in andamentos[0] or
         'CANCELAMENTO DE AUTUACAO' in andamentos[0]):
        lista_excluidos.append(processo)
        excluidos = excluidos + 1

    else:

        dados_csv.append(dados)
        andamentos_csv.append(dados2)
    

    print(nome_processo)
    

    
dsd.write_csv_lines('ADItotal(sem_andamentos).txt',dados_csv)
dsd.write_csv_lines('ADItotal(andamentos).txt',andamentos_csv)
dsd.write_csv_lines('excluidos.txt',lista_excluidos)
    
print ('Gravados arquivos ADItotal(sem_andamentos).txt e ADItotal(andamentos).txt')
print (f'Excluídos {excluidos} processos')
