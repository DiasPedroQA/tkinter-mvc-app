# Tkinter MVC App - Aplicação gráfica em Python utilizando o padrão MVC

Esse projeto é uma aplicação gráfica em Python utilizando **Tkinter**, estruturada no padrão **MVC** (Model-View-Controller). A aplicação permite a interação com o usuário para análise e conversão de arquivos, com a separação clara entre o **backend** (lógica de negócio) e o **frontend** (interface gráfica), garantindo fácil manutenção e escalabilidade.

---

## 🛠 Estrutura do Projeto

A estrutura do projeto está organizada da seguinte forma:

```bash
tkinter-mvc-app/
├── .github/                 # Configurações de integração contínua (CI)
├── .logs_makefile           # Logs gerados pelo Makefile
├── .venv/                   # Ambiente virtual (não versionado)
├── .vscode/                 # Configurações do VSCode
├── app/                     # Código principal da aplicação
│   ├── backend/             # Lógica de backend (controller, model, tools, logs)
│   │   └── __init__.py      # Inicialização do módulo backend
│   ├── frontend/            # Interface gráfica (views)
│   │   └── __init__.py      # Inicialização do módulo frontend
│   ├── __init__.py          # Inicialização do módulo principal
├── tests/                   # Testes unitários
│   ├── backend/             # Testes para o backend
│   ├── frontend/            # Testes para a interface gráfica
│   └── __init__.py          # Inicialização dos testes
├── .coverage                # Relatório de cobertura de testes
├── .editorconfig            # Configuração para o estilo de código entre editores
├── .env                     # Arquivo de variáveis de ambiente (não versionado)
├── .gitignore               # Arquivo que define o que o Git deve ignorar
├── .pylintrc                # Configuração do Pylint para verificar o estilo do código
├── LICENSE                  # Licença do projeto
├── Makefile                 # Facilita execução de comandos
├── pyproject.toml           # Configuração de ferramentas como Black
├── README.md                # Documento de explicação do projeto
└── requirements-dev.txt     # Dependências para desenvolvimento
````

### Descrição dos Arquivos e Diretórios

* **`.github/`**: Contém as configurações de integração contínua (CI), incluindo workflows do GitHub Actions, que automatizam os testes e outras tarefas.

* **`.logs_makefile`**: Armazena logs gerados pelos comandos do `Makefile`.

* **`.venv/`**: Ambiente virtual, onde todas as dependências do projeto são instaladas. Esse diretório não é versionado no Git.

* **`.vscode/`**: Configurações específicas do VSCode, como preferências de formatação, depuração, etc.

* **`app/`**: Contém a lógica principal da aplicação:

  * **`backend/`**: Lógica do backend, como controllers, models e ferramentas de manipulação.
  * **`frontend/`**: Código da interface gráfica, incluindo as views que interagem com o usuário.
  * **`__init__.py`**: Arquivos de inicialização que configuram os pacotes do Python.

* **`tests/`**: Diretório onde estão os testes do projeto:

  * **`backend/`**: Testes para o backend.
  * **`frontend/`**: Testes para a interface gráfica.

* **`.coverage`**: Relatório de cobertura de testes gerado pelo pytest.

* **`.editorconfig`**: Arquivo que define a formatação e estilo de código a ser seguido, garantindo consistência no código entre diferentes editores de texto.

* **`.env`**: Contém variáveis de ambiente específicas, como chaves de API e configurações sensíveis. Este arquivo não deve ser versionado.

* **`.gitignore`**: Define arquivos e diretórios que não devem ser rastreados pelo Git, como o ambiente virtual `.venv/` e outros arquivos temporários.

* **`.pylintrc`**: Arquivo de configuração para o Pylint, que é utilizado para garantir a qualidade do código, verificando padrões e erros comuns.

* **`LICENSE`**: Arquivo que contém a licença sob a qual o projeto está disponibilizado.

* **`Makefile`**: Facilita a execução de tarefas comuns no projeto, como instalação de dependências, execução de testes e execução da aplicação.

* **`pyproject.toml`**: Arquivo de configuração para ferramentas de formatação e análise de código, como o Black, Flake8 e outros.

* **`requirements-dev.txt`**: Contém as dependências necessárias para o desenvolvimento do projeto, como bibliotecas de teste, ferramentas de linting e formatação de código.

---

## 🚀 Como rodar o projeto

1. **Clone o repositório**

   ```bash
   git clone https://github.com/seu-usuario/tkinter-mvc-app.git
   cd tkinter-mvc-app
   ```

2. **Crie e ative o ambiente virtual**

   É recomendado criar um ambiente virtual para o projeto para manter as dependências isoladas:

   ```bash
   python -m venv venv
   ```

   * No Windows, ative o ambiente:

   ```bash
   venv\Scripts\activate
   ```

   * No Linux/Mac, ative o ambiente:

   ```bash
   source venv/bin/activate
   ```

3. **Instale as dependências**

   Para instalar as dependências, você pode usar o `Makefile` ou instalar diretamente com o `pip`:

   Usando o `Makefile`:

   ```bash
   make install
   ```

   Ou manualmente com o `pip`:

   ```bash
   pip install -r requirements-dev.txt
   ```

4. **Execute o aplicativo**

   Para rodar o aplicativo, use o comando:

   ```bash
   make run
   ```

   Ou execute diretamente o script Python:

   ```bash
   python app/meu_app.py
   ```

5. **Verifique se está funcionando**

   Após rodar o aplicativo, você verá a interface gráfica sendo carregada. Se tiver problemas, verifique o log de erros no diretório `app/logs/`.

---

## 🧪 Rodando os Testes

Os testes são essenciais para garantir que o código esteja funcionando corretamente. Eles foram escritos utilizando o **pytest**.

Para rodar todos os testes, use o seguinte comando:

```bash
make test
```

Ou execute diretamente com o **pytest** para gerar um relatório de cobertura de código:

```bash
pytest --cov=app tests/ --cov-report=html
```

Os testes estão organizados em pastas correspondentes às camadas do aplicativo (backend e frontend).

---

## 🔄 Integração Contínua (CI)

A integração contínua está configurada para rodar automaticamente sempre que houver um `push` ou `pull request` para o branch `main`. Ela executa os testes usando o **pytest** para garantir que tudo esteja funcionando.

O arquivo de workflow do CI pode ser encontrado em: `.github/workflows/python-app.yml`.

---

## 🧹 Qualidade de Código

Garantimos a qualidade do código com ferramentas de formatação e verificação de estilo:

* **EditorConfig**: O arquivo `.editorconfig` ajuda a garantir que todos os desenvolvedores sigam o mesmo padrão de formatação de código.
* **Pre-commit hooks**: Usamos o `pre-commit` para rodar automaticamente o `black` (formatador de código) e o `flake8` (verificador de estilo), garantindo que o código esteja sempre limpo e sem erros.

### Como configurar o pre-commit

1. Instale o pre-commit:

   ```bash
   pip install pre-commit
   ```

2. Instale os hooks configurados:

   ```bash
   pre-commit install
   ```

Agora, sempre que você fizer um commit, o código será automaticamente formatado e verificado.

---

## 📜 Licença

Este projeto está sob a licença **MIT**. Para mais detalhes, consulte o arquivo `LICENSE`.

---

## 📄 Explicação dos Arquivos de Configuração

### 1. **`.gitignore`**

Esse arquivo define quais arquivos e pastas não devem ser versionados no Git. Ele ignora o diretório do ambiente virtual `venv/`, arquivos temporários e outras pastas que não fazem sentido estarem no repositório.

### 2. **`requirements-dev.txt`**

Contém todas as dependências do projeto necessárias para o desenvolvimento, como `pytest` para testes, ferramentas de linting e formatação de código.

### 3. **`.editorconfig`**

Esse arquivo ajuda a padronizar a formatação do código entre diferentes editores de texto. Ele define coisas como o tipo de indentação, tamanho da tabulação, e outros detalhes para garantir que o código esteja sempre bem formatado.

### 4. **`pyproject.toml`**

Este arquivo é utilizado para configurar o **Black**, o formatador de código. Com ele, a formatação é feita automaticamente sempre que você rodar o `black` no código.

### 5. **`Makefile`**

O `Makefile` facilita a execução de comandos repetitivos, como instalação de dependências (`make install`), rodar o app (`make run`) e rodar os testes (`make test`). Isso ajuda a evitar que você precise lembrar de todos os comandos e torna o fluxo de trabalho mais rápido e eficiente.

### 6. **`.github/workflows/python-app.yml`**

Este arquivo configura o **GitHub Actions**, que é usado para a integração contínua (CI). Sempre que houver um `push` ou `pull request` no branch `main`, ele executa os testes com o `pytest` para garantir que tudo esteja funcionando.

---
