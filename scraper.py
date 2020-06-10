from selenium import webdriver
browser = webdriver.Chrome(executable_path='./chromedriver-1')
pages = 32
for i in range(10, pages):
    page = i
    browser.get(f'https://www.camara.leg.br/internet/sitaqweb/resultadoPesquisaDiscursos.asp?CurrentPage={page}&BasePesq=plenario&txIndexacao=&txOrador=JAIR%20BOLSONARO&txPartido=&dtInicio=&dtFim=&txUF=&txSessao=&listaTipoSessao=&listaTipoInterv=&inFalaPres=&listaTipoFala=&listaFaseSessao=&txAparteante=&listaEtapa=&CampoOrdenacao=dtSessao&TipoOrdenacao=DESC&PageSize=50&txTexto=&txSumario=')
    tables = browser.find_elements_by_tag_name('table')
    table_content = tables[0].find_elements_by_tag_name('tbody')[0].find_elements_by_tag_name('tr')
    j = 0
    while j < len(table_content):
        tr = table_content[j]
        try:
            tr.find_elements_by_tag_name('td')[3].find_elements_by_tag_name('a')[0].click()
            text = browser.find_elements_by_tag_name('font')
            try:    
                speech = browser.find_elements_by_tag_name('font')[1].text
            except IndexError:
                speech = browser.find_elements_by_tag_name('font')[0].text
            with open(f'./camara/file{j}{i}.txt', 'w') as file:
                file.write(speech)
                file.close()
        except Exception as err:
            print(err)
            pass
        browser.get(f'https://www.camara.leg.br/internet/sitaqweb/resultadoPesquisaDiscursos.asp?CurrentPage={page}&BasePesq=plenario&txIndexacao=&txOrador=JAIR%20BOLSONARO&txPartido=&dtInicio=&dtFim=&txUF=&txSessao=&listaTipoSessao=&listaTipoInterv=&inFalaPres=&listaTipoFala=&listaFaseSessao=&txAparteante=&listaEtapa=&CampoOrdenacao=dtSessao&TipoOrdenacao=DESC&PageSize=50&txTexto=&txSumario=')
        tables = browser.find_elements_by_tag_name('table')
        table_content = tables[0].find_elements_by_tag_name('tbody')[0].find_elements_by_tag_name('tr')

        j += 2
browser.close()
