# To-Do Task List

Uma aplicação web simples para gerenciamento de tarefas, construída com Flask para o backend, HTML, CSS e JavaScript para o frontend, com persistência dos dados em um banco de dados MySQL. A aplicação permite criar, visualizar, editar, atualizar o status e excluir tarefas, além de incluir um sistema de autenticação com JWT para controle de usuários.

## Funcionalidades

- Autenticação de usuário
- Adicionar tarefas
- Visualizar lista de tarefas
- Editar título de tarefas
- Atualizar status de tarefas (Pendente, Em Andamento, Completa)
- Deletar tarefas

## Estrutura de Diretórios

- todo/
- │
- ├── .venv/                   # Ambiente virtual
- │
- ├── app/                      # Lógica do backend
- │   ├── __init__.py           # Inicialização do Flask
- │   ├── db.py                 # Configurações do banco de dados
- │   ├── routes.py             # Rotas do Flask (API e autenticação)
- │   └── auth/                 # Blueprint de autenticação
- │       ├── __init__.py
- │       ├── routes.py
- │       └── models.py
- │
- ├── front-end/                # Arquivos do frontend
- │   ├── static/               # Arquivos estáticos (CSS, JS)
- │   │   ├── script.js         # Lógica JavaScript para interação
- │   │   └── style.css         # Estilos CSS
- │   └── templates/            # Templates HTML
- │       ├── index.html        # Página principal (Lista de tarefas)
- │       ├── login.html        # Página de login
- │       └── register.html     # Página de registro de usuário
- │
- ├── run.py                    # Arquivo para rodar a aplicação
- └── requirements.txt          # Dependências do projeto


## Tecnologias Utilizadas

- **Backend**: Python com Flask
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Banco de Dados**: MySQL
- **Autenticação**: JWT (JSON Web Tokens)
- **Autenticação CORS**: Flask-CORS

## Configuração do Ambiente de Desenvolvimento

### Pré-requisitos

- Python 3.8+
- MySQL
- Git

### Passos para Instalação

1. **Clone o repositório**:

    ```bash
    git clone https://github.com/gustavogouveia1/todotask
    cd todo
    ```

2. **Crie um ambiente virtual**:

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # No Windows: .venv\Scripts\activate
    ```

3. **Instale as dependências**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Configurar o banco de dados**:

    No arquivo `db.py`, altere as credenciais de conexão para o MySQL de acordo com suas configurações locais:

    ```python
    db_config = {
        'user': os.getenv('DB_USER', 'seu_usuario'),
        'password': os.getenv('DB_PASSWORD', 'sua_senha'),
        'host': os.getenv('DB_HOST', 'localhost'),
        'database': os.getenv('DB_NAME', 'nome_do_banco_de_dados')
    }
    ```

5. **Iniciar o servidor de desenvolvimento**:

    No diretório raiz, execute:

    ```bash
    python run.py
    ```

    A aplicação estará disponível em `http://127.0.0.1:5000/`.

## Rotas da API

A aplicação possui as seguintes rotas para interagir com as tarefas:

- `GET /tasks`: Retorna todas as tarefas
- `POST /tasks/add`: Adiciona uma nova tarefa
- `POST /tasks/edit/<int:task_id>`: Edita o título de uma tarefa
- `POST /tasks/update_status/<int:task_id>`: Atualiza o status de uma tarefa
- `DELETE /tasks/delete/<int:task_id>`: Deleta uma tarefa

## Autenticação

- `POST /auth/login`: Realiza o login do usuário
- `POST /auth/register`: Registra um novo usuário
- `POST /auth/logout`: Realiza o logout do usuário
- `GET /auth/me`: Retorna informações do usuário autenticado

## Frontend

A interface do usuário permite:
- Página de login: Formulário para login de usuários.
- Página de registro: Formulário para registrar novos usuários.
- Página principal: Exibição da lista de tarefas com opções para adicionar, editar, atualizar status e deletar.

## Contribuição

Se você quiser contribuir para este projeto, siga os passos abaixo:

1. Faça um fork do projeto.
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`).
3. Faça commit das suas alterações (`git commit -am 'Adiciona nova feature'`).
4. Envie para a branch principal (`git push origin feature/nova-feature`).
5. Abra um Pull Request.

