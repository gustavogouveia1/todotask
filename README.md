# To-Do Task List

Uma aplicação web simples para gerenciamento de tarefas, construída com Flask para o backend e HTML/CSS/JavaScript para o frontend. Esta aplicação permite criar, visualizar, editar, atualizar o status e excluir tarefas, com persistência dos dados em um banco de dados MySQL.

## Funcionalidades

- Adicionar tarefas
- Visualizar lista de tarefas
- Editar título de tarefas
- Atualizar status de tarefas (Pendente, Em Andamento, Completa)
- Deletar tarefas

## Estrutura de Diretórios

todo/
│
├── .venv/
│
├── app/
│   ├── __init__.py
│   ├── db.py
│   └── routes.py
│
├── front-end/
│   ├── static/
│   │   ├── script.js
│   │   └── style.css
│   └── templates/
│       └── index.html
│
└── run.py

## Tecnologias Utilizadas

- **Backend**: Python com Flask
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Banco de Dados**: MySQL
- **Autenticação CORS**: Flask-CORS

## Configuração do Ambiente de Desenvolvimento

### Pré-requisitos

- Python 3.8+
- MySQL
- Git

### Passos para Instalação

1. **Clone o repositório**:

    ```bash
    git clone https://github.com/seu-usuario/seu-repositorio.git
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
        'user': 'seu_usuario',
        'password': 'sua_senha',
        'host': 'localhost',
        'database': 'nome_do_banco_de_dados'
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

## Frontend

A interface do usuário permite:
- Adicionar tarefas através de um formulário
- Visualizar a lista de tarefas com status
- Editar títulos de tarefas
- Atualizar o status das tarefas diretamente na lista
- Deletar tarefas

## Contribuição

Se você quiser contribuir para este projeto, siga os passos abaixo:

1. Faça um fork do projeto.
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`).
3. Faça commit das suas alterações (`git commit -am 'Adiciona nova feature'`).
4. Envie para a branch principal (`git push origin feature/nova-feature`).
5. Abra um Pull Request.

