# API de MongoDB em Flask

Esta é uma API RESTful para gerenciar usuários utilizando Flask e MongoDB. A API permite criar, ler e atualizar usuários.

## Tecnologias Utilizadas

- Python
- Flask
- MongoDB
- PyMongo

## Endpoints

### 1. Criar um Novo Usuário

- **Método:** `POST`
- **Endpoint:** `/users`
- **Corpo da Requisição:** Documento JSON
- **Resposta:**
  - **Código 201:** Usuário criado com sucesso.
  ```json
  {
      "_id": "id_do_usuario"
  }
  ```
  - **Código 500:** Erro ao criar usuário.

### 2. Obter Usuários

- **Método:** `GET`
- **Endpoint:** `/users`
- **Parâmetros Opcionais:**
  - `query`: Filtros para a busca (JSON) (ex: `{"age":{"$gt":12}}`).
  - `fields`: Campos a serem incluídos ou excluídos na resposta (ex: `name,age,-name`).
- **Resposta:**
  - **Código 200:** Lista de usuários.
  ```json
  [
      {
          "_id": "id_do_usuario",
          "name": "Nome do Usuário",
          "age": <idade>
      }
  ]
  ```
  - **Código 500:** Erro ao obter usuários.

### 3. Obter um Usuário Específico

- **Método:** `GET`
- **Endpoint:** `/users/<user_id>`
- **Resposta:**
  - **Código 200:** Usuário encontrado.
  ```json
  {
        "_id": "id_do_usuario",
        "name": "Nome do Usuário",
        "age": <idade>
  }
  ```
  - **Código 404:** Usuário não encontrado.
  - **Código 400:** ID inválido.

### 4. Atualizar um Usuário

- **Método:** `PUT`
- **Endpoint:** `/users/<user_id>`
- **Corpo da Requisição:**
  ```json
  {
      "name": "Novo Nome",
      "age": <nova_idade>
  }
  ```
- **Resposta:**
  - **Código 204:** Usuário atualizado com sucesso.
  - **Código 404:** Usuário não encontrado.
  - **Código 400:** ID inválido.

## Execução

Apenas execute o arquivo `main.py` para executar a API. Certifique-se de ter instalado as dependências antes de executar o código e der uma instância do MongoDB na porta padrão `27017`.


A API estará disponível em `http://localhost:8080`.
