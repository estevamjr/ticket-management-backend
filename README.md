# 🎫 Ticket Management API - Backend MVP

## 🚀 Visão Geral

Este projeto é a implementação do Backend de um **Sistema de Gestão de Tickets** (MVP - Mínimo Produto Viável), desenvolvido em **Python** e **Flask**. A API é totalmente **RESTful** e **Stateless**, utilizando JSON Web Tokens (JWT) para autenticação e segurança.

O projeto foi estruturado para demonstrar a aplicação dos princípios de *key constraints* e boas práticas de engenharia de software (arquitetura em camadas).

## ⚙️ Arquitetura e Tecnologia

| Componente | Tecnologia | Destaque Técnico |
| :--- | :--- | :--- |
| **Framework** | Flask (Python) | Leveza e flexibilidade. |
| **Banco de Dados** | SQLite + SQLAlchemy (ORM) | Cumpre o requisito de BD local e utiliza Mapeamento Objeto-Relacional para abstração de dados. |
| **Segurança** | Flask-JWT-Extended | Implementa a arquitetura **Stateless** (Ausência de Estados). |
| **Serialização** | Marshmallow | Usado para validação e serialização de objetos para JSON. |
| **Documentação** | Flasgger (Swagger/OpenAPI) | Documentação gerada automaticamente a partir dos Schemas Marshmallow. |

### 🧭 Organização em Camadas (Princípios SOLID)

A aplicação segue uma arquitetura em camadas para garantir a **Responsabilidade Única** (SRP) e a manutenibilidade:

* **controllers/**: Define os endpoints da API e orquestra a requisição.
* **services/**: Contém a lógica de negócio pura.
* **models/**: Define os modelos de dados e as relações (SQLAlchemy).
* **utils/**: Utilitários para funções genéricas, como tratamento de respostas HTTP.

## 💻 Instalação e Execução

Para configurar e rodar o Backend em seu ambiente local:

1.  **Clonar e Navegar:**
    ```bash
    git clone [https://github.com/estevamjr/ticket-management-backend.git](https://github.com/estevamjr/ticket-management-backend.git)
    cd ticket-management-backend
    ```

2.  **Criar e Ativar o Ambiente Virtual:**
    (Exemplo para Windows/PowerShell)
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Instalar Dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Executar o Servidor Flask:**
    A primeira execução do app.py criará o banco de dados e as tabelas.
    ```bash
    python app.py
    ```

### Endereços Importantes

* **API Principal:** http://127.0.0.1:5000
* **Documentação Swagger:** http://127.0.0.1:5000/apidocs