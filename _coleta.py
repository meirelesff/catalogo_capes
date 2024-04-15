from bs4 import BeautifulSoup
from io import StringIO
import pandas as pd
import requests
import os


# Define classe para coleta de dados
class Coleta:
    def __init__(self):
        
        # Cria diretorios
        if not os.path.exists('data'):
            os.makedirs('data')
            
        if not os.path.exists('raw_data'):
            os.makedirs('raw_data')
            
            
    # Método para extrair links de download de CSV
    def extrai_links(self, site_capes):
        self.site_capes = site_capes
        
        # Extrai links de download
        response = requests.get(site_capes)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.select('.btn-recursos+ .btn-recursos')
        links = [link.get('href') for link in links]
        
        # Seleciona apenas links de arquivos CSV
        links = [link for link in links if link.endswith('.csv')]
        return links
    
    
    # Método para extrair todos os links de download
    def extrai_todos_links(self):
        
        # Links de todas as paginas
        print('Extraindo links de todas as páginas...')
        paginas = ['https://dadosabertos.capes.gov.br/dataset/1987-a-2012-catalogo-de-teses-e-dissertacoes-brasil',
                   'https://dadosabertos.capes.gov.br/dataset/catalogo-de-teses-e-dissertacoes-de-2013-a-2016',
                   'https://dadosabertos.capes.gov.br/dataset/2017-2020-catalogo-de-teses-e-dissertacoes-da-capes',
                   'https://dadosabertos.capes.gov.br/dataset/2021-a-2024-catalogo-de-teses-e-dissertacoes-brasil']
        
        # Extrai todos os links
        links = []
        for pagina in paginas:
            links += self.extrai_links(pagina)
            
        return links


    # Método para importar dados como DataFrame
    def importa_dados(self, link):
        self.link = link
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        
        # Importa dados
        print(f'Planilha atual: {self.link}')
        response = requests.get(self.link, headers=headers)
        df = pd.read_csv(StringIO(response.text), sep=';', encoding='latin1', dtype=str)
             
        # Seleciona apenas algumas colunas
        if 'AnoBase' not in df.columns:
            colunas = ['AN_BASE', 'CD_PROGRAMA', 'SG_ENTIDADE_ENSINO', 'NM_ENTIDADE_ENSINO',
                       'NM_PROGRAMA', 'NM_GRANDE_AREA_CONHECIMENTO', 'NM_AREA_CONHECIMENTO',
                       'NM_AREA_AVALIACAO', 'NM_DISCENTE', 'NM_PRODUCAO', 'NM_GRAU_ACADEMICO', 'DT_TITULACAO',
                       'DS_PALAVRA_CHAVE', 'DS_RESUMO']
        else:
            colunas = ['AnoBase', 'CodigoPrograma',  'SiglaIes', 'NomeIes',
                   'NomePrograma', 'GrandeAreaDescricao', 'AreaConhecimento',
                   'AreaAvaliacao', 'Autor', 'TituloTese', 'Nivel', 'DataDefesa',
                   'PalavrasChave', 'ResumoTese']
        
        df = df[colunas]
        
        # Padroniza nome das colunas
        colunas = ['ano', 'codigo_programa', 'sigla_ies', 'nome_ies', 'nome_programa',
                   'grande_area', 'area_conhecimento', 'area_avaliacao', 'autor', 'titulo',
                   'nivel', 'data_defesa', 'palavras_chave', 'resumo']
        df.columns = colunas
        
        # Exporta uma versao raw
        nome_arq = self.link.split('/')[-1]
        df.to_csv(f"raw_data/{nome_arq}", index=False)

        return df
    
    
    # Método para importar todos os dados
    def coleta(self):
        
        # Extrai links
        print('Extraindo dados da Capes...')
        links = self.extrai_todos_links()
        
        # Checa na pasta data quais arqs já foram extraídos
        arquivos = os.listdir('raw_data')
        
        # Remove os links já extraídos
        links = [link for link in links if not any(ano in link for ano in arquivos)]
        
        # Importa dados
        dados = [self.importa_dados(link) for link in links]
        
        # Carrega os dados brutos
        dados_brutos = os.listdir('raw_data')
        dados_brutos = [pd.read_csv(f'raw_data/{arquivo}') for arquivo in dados_brutos]
        
        # Concatena os DataFrames
        df = pd.concat(dados_brutos)
              
        # Exporta os dados em CSV
        df[df['Nivel'] == 'Mestrado'].to_csv('data/mestrado.csv', index=False)
        df[df['Nivel'] == 'Doutorado'].to_csv('data/doutorado.csv', index=False)
        print('Extração concluída!')
        
        return dados
    
    
    
# Coleta os dados
if __name__ == '__main__':
    capes = Coleta()
    capes.coleta()