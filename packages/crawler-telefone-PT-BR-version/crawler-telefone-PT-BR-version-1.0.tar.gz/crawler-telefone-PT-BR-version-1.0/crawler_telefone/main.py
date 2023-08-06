import re
import threading
import requests
from bs4 import BeautifulSoup


DOMINIO = 'https://dominio.com'
URL_AUTOMOVEIS = 'https://dominio.com/pagina-para-encontrar-telefones/'

LINKS = []
TELEFONES = []

def requisicao(url):
    try:
        resposta = requests.get(url)
        if resposta.status_code == 200:
            return resposta.text
        else:
            print('Erro ao fazer requisição.')
    except Exception as error:
        print('Erro ao fazer requisição.')
        print(error)


def parsing(resposta_html):
    try:
        soup = BeautifulSoup(resposta_html, 'html.parser')
        return soup
    except:
        print('Erro ao fazer o parsing HTML.')


def encontrar_links(soup):
    try:
        cards_primarios = soup.find('div', class_='ui three doubling link cards') 
        cards= cards_primarios.find_all('a') 
    except:
        print('Erro ao encontrar links')
        return None
    
    links = []
    
    for card in cards:
        try:
            link = card['href']
            links.append(link)
        except:
            pass
    return links


def encontrar_telefone(soup): 
    try:
        descricao = soup.find_all('div', class_='sixteen wide column')[2].p.get_text().strip()
    except:
        print('Erro ao encontrar descrição.')
        return None

    regex = re.findall(r"\(?0?([1-9]{2})[ \-\.\)]{0,2}(9[ \-\.]?\d{4})[ \-\.]?(\d{4})", descricao) # RAW
    
    if regex:
        return regex


def descobrir_telefones():
    while True:
        try:
            link_anuncio = LINKS.pop(0) # type: ignore
        except:
            return None

        resposta_anuncio = requisicao(DOMINIO + link_anuncio)
        if resposta_anuncio:
            soup_anuncio = parsing(resposta_anuncio)
            if soup_anuncio:
                telefones = encontrar_telefone(soup_anuncio)
                if telefones:
                    for telefone in telefones:
                        print(f'Telefone encontrado: {telefone}')
                        # TELEFONES.append(telefone)
                        salvar_telefones(telefone) 


def salvar_telefones(telefone):
    str_telefone = f'{telefone[0]}{telefone[1]}{telefone[2]}\n'
    try:
        with open('telefones.csv', 'a') as arquivo:
            arquivo.write(str_telefone)
    except:
        print('Erro ao salvar arquivo.')


if __name__ == '__main__':
    resposta_busca = requisicao(URL_AUTOMOVEIS)
    if resposta_busca:
        soup_busca = parsing(resposta_busca)
        if soup_busca:
            LINKS = encontrar_links(soup_busca)

            THREADS = []
            
            for i in range(5):
                t = threading.Thread(target=descobrir_telefones)
                THREADS.append(t)

            for t in THREADS:
                t.start()
            
            for t in THREADS:
                t.join()

            print(TELEFONES)

