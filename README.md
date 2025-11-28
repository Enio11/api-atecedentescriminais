# API Antecedentes Criminais

API para consulta de antecedentes criminais através do Portal da Transparência.

## Descrição

Este projeto fornece uma API REST para consultar informações de antecedentes criminais a partir de CPF usando web scraping do Portal da Transparência.

## Tecnologias

- Python 3.x
- FastAPI
- Selenium WebDriver
- SQLite

## Estrutura do Projeto

- `main.py` - Aplicação principal FastAPI
- `scraper.py` - Script de web scraping para coleta de dados
- `database.py` - Gerenciamento de banco de dados SQLite
- `test_api.py` - Testes da API
- `requirements.txt` - Dependências do projeto

## Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/api-atecedentescriminais.git
cd api-atecedentescriminais

# Instale as dependências
pip install -r requirements.txt
```

## Uso

```bash
# Execute a API
python main.py
```

A API estará disponível em `http://localhost:8000`

## Endpoints

- `GET /` - Health check
- `POST /consultar` - Consultar antecedentes por CPF
- `GET /historico` - Visualizar histórico de consultas

## Licença

Este projeto é de código aberto.
