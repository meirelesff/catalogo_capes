# Catalogo de Teses e Dissertações :books:

Este repositório contém código para extrair e limpar dados do catálogo de Teses e Dissertações de Pós-Graduação no Brasil defendidas de 1987 a 2023, disponíveis no [Portal de Dados Abertos da Capes](https://dadosabertos.capes.gov.br/).


## Rodando a coleta

Depois de clonar o repositório, da pasta do projeto instale dependências necessárias com:

```bash
pip install -r requirements.txt
```

Isto feito, basta rodar o script de coleta:

```bash
python3 _coleta.py
```

A coleta é feita ano a ano para não sobrecarregar o servidor da Capes (o que deve levar algumas horas). Dados parciais brutos são salvos em formato CSV na pasta `raw_data` e, a base final, em `data`.