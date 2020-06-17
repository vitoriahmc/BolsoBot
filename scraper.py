from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
browser = webdriver.Chrome(executable_path='./chromedriver.exe')
pages = 35
for i in range(8, pages):
    page = i
    browser.get(f'https://www.camara.leg.br/internet/sitaqweb/resultadoPesquisaDiscursos.asp?CurrentPage={page}&txOrador=BOLSONARO&txPartido=&txUF=&dtInicio=&dtFim=&txTexto=&txSumario=&basePesq=plenario&CampoOrdenacao=dtSessao&PageSize=50&TipoOrdenacao=DESC&btnPesq=Pesquisar')
    # browser.get(f'https://www.camara.leg.br/internet/sitaqweb/resultadoPesquisaDiscursos.asp?CurrentPage={page}&BasePesq=plenario&txIndexacao=&txOrador=JAIR%20BOLSONARO&txPartido=&dtInicio=&dtFim=&txUF=&txSessao=&listaTipoSessao=&listaTipoInterv=&inFalaPres=&listaTipoFala=&listaFaseSessao=&txAparteante=&listaEtapa=&CampoOrdenacao=dtSessao&TipoOrdenacao=DESC&PageSize=50&txTexto=&txSumario=')
    tables = browser.find_elements_by_tag_name('table')
    try:
        table_content = tables[0].find_elements_by_tag_name('tbody')[0].find_elements_by_tag_name('tr')
        j = 0
        while j < len(table_content):
            tr = table_content[j]
            try:
                tr.find_elements_by_tag_name('td')[3].find_elements_by_tag_name('a')[0].click()
                myElem = WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.ID, 'content')))
                text = browser.find_elements_by_tag_name('font')
                # print(browser.find_elements_by_tag_name('font'))
                try:    
                    speech = browser.find_elements_by_tag_name('font')[1].text
                except IndexError:
                    speech = browser.find_elements_by_tag_name('font')[0].text
                with open(f'./camara-all/file{j}{i}.txt', 'w') as file:
                    file.write(speech)
                    file.close()
            except Exception as err:
                print(err)
                pass
            browser.get(f'https://www.camara.leg.br/internet/sitaqweb/resultadoPesquisaDiscursos.asp?CurrentPage={page}&txOrador=BOLSONARO&txPartido=&txUF=&dtInicio=&dtFim=&txTexto=&txSumario=&basePesq=plenario&CampoOrdenacao=dtSessao&PageSize=50&TipoOrdenacao=DESC&btnPesq=Pesquisar')
            tables = browser.find_elements_by_tag_name('table')
            table_content = tables[0].find_elements_by_tag_name('tbody')[0].find_elements_by_tag_name('tr')

            j += 2
    except Exception:
        continue
browser.close()
