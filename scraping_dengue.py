import requests
import pandas as pd
from bs4 import BeautifulSoup
import os

def scraping_tabnet(dimensao, nome_arquivo):
    url = "http://tabnet.datasus.gov.br/cgi/tabcgi.exe?sinannet/cnv/denguebbr.def"

    # Cria a pasta 'dados' se não existir
    os.makedirs('dados', exist_ok=True)

    # Sessão para manter cookies e headers
    session = requests.Session()
    response = session.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    # Pega o formulário de ação
    form = soup.find('form')
    action_url = form['action']

    # Monta o payload com a dimensão específica
    payload = {
        'Linha': 'UF',  # Linha = UF
        'Coluna': dimensao,  # Coluna = parâmetro variável
        'Incremento': 'N',
        'Selec1': '1',
        'Selec2': '1',
        'Selec3': '1',
        'Selec4': '1',
        'Selec5': '1',
        'Selec6': '1',
        'Selec7': '1',
        'Selec8': '1',
        'Selec9': '1',
        'Selec10': '1',
        'formato': 'table',
    }

    # Faz a requisição POST para gerar a tabela
    result = session.post(f"http://tabnet.datasus.gov.br{action_url}", data=payload)

    # Usa o pandas para ler as tabelas do HTML
    tables = pd.read_html(result.text)

    if not tables:
        print(f"Nenhuma tabela foi encontrada para {nome_arquivo}.")
        return

    df = tables[0]

    # Limpeza básica de dados
    df.columns = [col.replace(' ', '_').lower() for col in df.columns]

    # Salva o CSV na pasta 'dados'
    output_path = os.path.join('dados', nome_arquivo)
    df.to_csv(output_path, index=False, encoding='utf-8-sig')

    print(f"Arquivo salvo com sucesso em: {output_path}")

if __name__ == "__main__":
    # Parâmetros: dimensão da coluna no TabNet e nome do arquivo
    scraping_tabnet('Escolaridade', 'educacao.csv')
    scraping_tabnet('Faixa_Etária', 'faixa-etaria.csv')
    scraping_tabnet('Sexo', 'genero.csv')
