# dsf-interlup-api

Bem-vindo ao repositório dsf-interlup-api! Este repositório contém o código-fonte para o projeto DSF Interlup API.

## Descrição

DSF Interlup API é uma API RESTful construída usando Flask, projetada para fornecer funcionalidades de backend para o gerenciamento de tarefas e categorias de tarefas. Inclui recursos para autenticação de usuários, criação, atualização, exclusão de tarefas e muito mais.

## Instalação Local

Para executar este projeto localmente, siga estas etapas:

1. Clone o repositório para sua máquina local:

   ```bash
   git clone https://github.com/danielxavierjob/dsf-interlup-api.git
   ```

2. Instale as dependências do projeto:

   ```bash
   cd dsf-interlup-api
   pip install -r requirements.txt
   ```

3. Configure o ambiente:

   - Crie um arquivo `.env` no diretório raiz.
   - Defina as variáveis de ambiente necessárias no arquivo `.env`. Exemplo:
     ```
     SECRET_KEY=sua_chave_secreta
     DATABASE_URL=sqlite:///db.db
     DEBUG=True
     ```

4. Inicialize o banco de dados:

   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

5. Execute a aplicação Flask:

   ```bash
   flask run
   ```

6. Acesse os endpoints da API em `http://localhost:5000`.

## Instalação Docker

Para executar este projeto no Docker, siga estas etapas:

1. Clone o repositório para sua máquina local:

   ```bash
   git clone https://github.com/danielxavierjob/dsf-interlup-api.git
   ```

2. Entre na pasta do projeto:

   ```bash
   cd dsf-interlup-api
   ```

3. Configure o ambiente:

   - Crie um arquivo `.env` no diretório raiz.
   - Defina as variáveis de ambiente necessárias no arquivo `.env`. Exemplo:
     ```
     SECRET_KEY=sua_chave_secreta
     DATABASE_URL=postgresql://postgres:1234@your_ip:5432/postgres
     DEBUG=True
     ```

5. Execute a aplicação no Docker:

   ```bash
   docker compose build
   docker compose up
   ```

6. Acesse os endpoints da API em `http://localhost:5000`.


## Uso

Depois que a aplicação estiver em execução, você pode interagir com a API usando ferramentas como `curl`, Postman ou qualquer biblioteca de cliente HTTP. Aqui estão alguns exemplos de endpoints da API:

- `GET /tasks`: Recupere todas as tarefas.
- `POST /tasks`: Crie uma nova tarefa.
- `PUT /tasks/<task_id>`: Atualize uma tarefa existente.
- `DELETE /tasks/<task_id>`: Exclua uma tarefa.

Para documentação detalhada da API e exemplos de uso, consulte as docstrings e comentários no código-fonte, ou acesse a documentação no Swagger na rota / da api

## Contribuição

Contribuições são bem-vindas! Se você tiver ideias para melhorias, correções de bugs ou novos recursos, sinta-se à vontade para abrir uma issue ou enviar um pull request.

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).
