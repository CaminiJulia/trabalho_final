### Autoria

- **Nome:** Julia Camini Veiga
- **Matrícula:** 202606

# Projeto: Gerenciador de Produtos com Testes

Este projeto é uma aplicação web CRUD (Create, Read, Update, Delete) desenvolvida em Flask, com uma suíte de testes completa cobrindo os três níveis da pirâmide de testes.

## Funcionalidades

* Adicionar, visualizar, editar e deletar produtos através de uma interface web.
* API REST para manipulação dos dados de produtos.

## Tecnologias Utilizadas

* **Backend:** Python, Flask, Flask-SQLAlchemy
* **Frontend:** HTML, CSS (embutido)
* **Banco de Dados:** SQLite
* **Testes:** Pytest, Selenium

## Como Executar o Projeto

1.  **Clone o repositório:**
    ```
    git clone https://github.com/CaminiJulia/trabalho_final.git
    ```

2.  **Crie e ative o ambiente virtual:**
    ```
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    ```

3.  **Instale as dependências:**
    ```
    pip install -r requirements.txt
    ```
    

4.  **Execute a aplicação:**
    ```
    python run.py
    ```
    Acesse `http://127.0.0.1:5000` no seu navegador.

## Como Executar os Testes

```
# Executar todos os testes
pytest

# Executar por nível
pytest tests/unit/
pytest tests/integration/
pytest tests/system/

