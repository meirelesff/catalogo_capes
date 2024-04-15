from bs4 import BeautifulSoup
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
        
        # Importa dados
        print(f'Planilha atual: {link}')
        df = pd.read_csv(link, sep=';', encoding='latin1', error_bad_lines=False)
        ano_base = df['AnoBase'][0]
        df.to_csv(f"raw_data/{ano_base}.csv", index=False)
        
        # Seleciona apenas algumas colunas
        colunas = ['AnoBase', 'CodigoPrograma', 'Regiao', 'Uf', 'SiglaIes', 'NomeIes',
                   'NomePrograma', 'GrandeAreaDescricao', 'AreaConhecimento',
                   'AreaAvaliacao', 'Autor', 'TituloTese', 'Nivel', 'DataDefesa',
                   'PalavrasChave', 'NumeroPaginas', 'ResumoTese']
        
        df = df[colunas]
        return df
    
    
    # Método para importar todos os dados
    def coleta(self):
        
        # Importa todos os dados
        print('Extraindo dados da Capes...')
        links = self.extrai_todos_links()
        dados = [self.importa_dados(link) for link in links]
        
        # Concatena os DataFrames
        dados = pd.concat(dados)
              
        # Exporta os dados para CSV na pasta data (separado por Nivel, 'Mestrado' e 'Doutorado')
        dados[dados['Nivel'] == 'Mestrado'].to_csv('data/mestrado.csv', index=False)
        dados[dados['Nivel'] == 'Doutorado'].to_csv('data/doutorado.csv', index=False)
        print('Extração concluída!')
        
        return dados
    
    
    
# Coleta os dados
if __name__ == '__main__':
    capes = Coleta()
    capes.coleta()
    