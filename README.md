# Catalogo de Teses e Dissertações

Este repositório contém código para extrair e limpar dados do catálogo de Teses e Dissertações de Pós-Graduação no Brasil defendidas de 1987 a 2023, disponíveis no [Portal de Dados Abertos da Capes](https://dadosabertos.capes.gov.br/).


## Rodando a coleta

Depois de clonar o repositório, da pasta do projeto instale dependências necessárias com:

```bash
pip install -r requirements.txt
```

Isto feito, basta rodar o script de coleta:

```bash
python collect.py
```

Os dados coletados serão salvos em `data/teses.csv` e `data/dissertacoes.csv`.