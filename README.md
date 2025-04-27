# Tkinter MVC App

Este projeto é uma aplicação gráfica em Python utilizando **Tkinter** estruturada no padrão **MVC** (Model-View-Controller), com **separação entre backend e frontend**.

O desenvolvimento é orientado por **TDD (Test-Driven Development)**, visando garantir qualidade de código e facilidade de manutenção.

---

## Estrutura do projeto

app/ ├── backend/ │ ├── controller/ │ └── model/ ├── frontend/ └── main.py

tests/ ├── backend/ │ ├── controller/ │ └── model/ └── frontend/

venv/ (ambiente virtual)

yaml
Copiar
Editar

---

## Como rodar o projeto

1. Clone o repositório:
    ```bash
    git clone https://github.com/seu-usuario/tkinter-mvc-app.git
    cd tkinter-mvc-app
    ```

2. Crie e ative o ambiente virtual:
    ```bash
    python -m venv venv
    # Ativar no Windows
    venv\Scripts\activate
    # Ativar no Linux/Mac
    source venv/bin/activate
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4. Execute o app:
    ```bash
    python app/main.py
    ```

---

## Testes

O projeto usa **pytest** para rodar os testes unitários.

Para executar os testes:

```bash
pytest tests/
