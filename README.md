# Tkinter MVC App

Esse projeto é uma aplicação gráfica em Python utilizando **Tkinter**, estruturada no padrão **MVC** (Model-View-Controller). A ideia é manter uma separação clara entre o **backend** e o **frontend**, com foco na organização e fácil manutenção.

O desenvolvimento foi feito com **TDD (Test-Driven Development)**, usando `pytest` para garantir que o código esteja sempre funcionando como esperado.

---

## 🛠 Estrutura do Projeto

```bash
tkinter-mvc-app/
├── ├── .github/
│   │   └── workflows/
│   │       └── python-app.yml
│   ├── .venv/
│   ├── .vscode/
│   ├── app/
│   │   ├── backend/
│   │   │   ├── controller/
│   │   │   │   └── app_controller.py
│   │   │   ├── logs/
│   │   │   │   └── app_logs.py
│   │   │   ├── model/
│   │   │   │   └── app_model.py
│   │   │   └── tools/
│   │   │       └── app_tools.py
│   │   ├── frontend/
│   │   └── main.py
│   ├── htmlcov/
│   ├── tests/
│   │   ├── backend/
│   │   │   ├── controller/
│   │   │   ├── logs/
│   │   │   ├── model/
│   │   │   └── tools/
│   │   ├── frontend/
│   ├── .coverage
│   ├── .editorconfig
│   ├── .gitignore
│   ├── .pre-commit-config.yaml
│   ├── LICENSE
│   ├── Makefile
│   ├── pyproject.toml
│   ├── README.md
│   └── requirements.txt
```

---

## 🚀 Como rodar o projeto

1. **Clone o repositório**

    ```bash
    git clone https://github.com/seu-usuario/tkinter-mvc-app.git
    cd tkinter-mvc-app
    ```

2. **Crie e ative o ambiente virtual**

    ```bash
    python -m venv venv

    # Ativar no Windows
    venv\Scripts\activate

    # Ativar no Linux/Mac
    source venv/bin/activate
    ```

3. **Instale as dependências**

    Para instalar todas as dependências, use o `Makefile`:

    ```bash
    make install
    ```

    Ou, se preferir, instale manualmente:

    ```bash
    pip install -r requirements.txt
    ```

4. **Execute o aplicativo**

    Execute o projeto com:

    ```bash
    make run
    ```

---

## 🧪 Rodando os Testes

Para garantir que tudo esteja funcionando, os testes estão configurados com **pytest**.

Para rodar todos os testes, basta usar o comando:

```bash
make test
```

Ou então, execute diretamente com o pytest com coverage junto (cobertura de código):

```bash
pytest --cov=app tests/ --cov-report=html
```

---

## 🔄 Integração Contínua (CI)

A integração contínua está configurada para rodar automaticamente sempre que houver um `push` ou `pull request` para o branch `main`. Ela executa os testes com o `pytest` para garantir que não quebrem nada.

O arquivo de workflow está em: `.github/workflows/python-app.yml`.

---

## 🧹 Qualidade de Código

A qualidade do código é garantida com alguns recursos:

- **EditorConfig**: O arquivo `.editorconfig` ajuda a garantir que todos os desenvolvedores sigam o mesmo padrão de formatação de código.
- **Pre-commit hooks**: Utilizamos o `pre-commit` para rodar o `black` (formatador de código) e o `flake8` (verificador de estilo), garantindo que o código esteja sempre limpo e sem erros.

Para instalar os hooks, é só rodar:

```bash
pip install pre-commit
pre-commit install
```

---

## 📜 Licença

Este projeto está sob a licença **MIT**. Para mais detalhes, consulte o arquivo `LICENSE`.

---

## 📄 Explicação dos Arquivos de Configuração

Aqui está o propósito de cada um dos arquivos de configuração no projeto:

### 1. **`.gitignore`**

Esse arquivo define quais arquivos e pastas não devem ser versionados no Git. Ele ignora o diretório do ambiente virtual `venv/`, arquivos temporários e outras pastas que não fazem sentido estarem no repositório.

### 2. **`requirements.txt`**

Contém todas as dependências do projeto, como `pytest` para testes e outras bibliotecas necessárias. Isso facilita a instalação das dependências com um simples comando:

```bash
pip install -r requirements.txt
```

### 3. **`.editorconfig`**

Esse arquivo ajuda a padronizar a formatação do código entre diferentes editores de texto. Ele define coisas como o tipo de indentação, tamanho da tabulação, e outros detalhes para garantir que o código esteja sempre bem formatado.

### 4. **`pyproject.toml`**

Este arquivo é utilizado para configurar o **Black**, o formatador de código. Com ele, a formatação é feita automaticamente sempre que você rodar o `black` no código.

### 5. **`.pre-commit-config.yaml`**

Aqui estão configurados os **pre-commit hooks**. Ele garante que o código passe por uma formatação automática com `black` e que não haja problemas de estilo com `flake8` antes de qualquer commit ser feito.

### 6. **`Makefile`**

O `Makefile` facilita a execução de comandos repetitivos, como instalar dependências (`make install`), rodar o app (`make run`) e rodar os testes (`make test`). Isso ajuda a evitar que você precise lembrar de todos os comandos e torna o fluxo de trabalho mais rápido e eficiente.

### 7. **`.github/workflows/python-app.yml`**

Este arquivo configura o **GitHub Actions**, que é usado para a integração contínua (CI). Sempre que houver um `push` ou `pull request` no branch `main`, ele executa os testes com o `pytest` para garantir que tudo esteja funcionando.

---

## 📌 To Do

Aqui estão algumas coisas que ainda podem ser feitas para melhorar o projeto:

- **Criar a primeira tela em Tkinter**: Começar a implementar a interface gráfica usando Tkinter.
- **Conectar o backend com a view**: Criar a lógica no **controller** para conectar os dados do modelo à interface.
- **Adicionar mais testes**: Escrever testes para as interações da interface gráfica e validar o comportamento completo da aplicação.
- **Melhorar a interface**: Adicionar elementos gráficos para tornar a interface mais atraente.
- **Adicionar tratamento de erros**: Melhorar a forma como a aplicação lida com erros, mostrando mensagens amigáveis ao usuário.
- **Refinar o fluxo de dados**: Documentar e melhorar a forma como os dados são passados entre **model**, **view** e **controller**.
- **Configurar logs de execução**: Implementar logs para monitorar o funcionamento do app em produção.
- **Testar em outros sistemas operacionais**: Garantir que a aplicação funcione bem em diferentes plataformas (Windows, Linux, Mac).

---
