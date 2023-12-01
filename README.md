# hyperhire-chat
A Simple Whatsapp API Clone 



## Getting Started

- clone the repo

    ```bash 
    git clone https://github.com/Iamdavidonuh/hyperhire-chat.git
    ```

### Installation

- Manual
    #### Creating a virutal environment

    - Setup Poetry

    - Install requirements

        ``` poetry install ```

    #### Run migrations before starting the server

    ```bash
    python manage.py migrate && python manage.py runserver
    ```
- Docker

    ```bash
    docker-compose up
    ```

### Visit API Swagger UI at:
- https://localhost:8000/swagger
