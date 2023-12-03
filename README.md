# hyperhire-chat
A Simple Chat Room API using django, django-channels



## Getting Started

- clone the repo

    ```bash 
    git clone https://github.com/Iamdavidonuh/hyperhire-chat.git
    ```

### Installation

- Manual
    #### Install Redis
    - Checkout Redis Docs: 
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

- Load dummy users (Optional): 
    ```bash
    python manage.py loaddata test_users.json
    ```

### Visit API Swagger UI at:
- https://localhost:8000/swagger



### Authentication
- The api uses basic authentication for it's authentication.
Users can authenticate by sending a `base64 encoded` containing your `username` and `password` encoded the format `username:password`
    ```bash
    import base64
    base64.b64encode(b"username:password").decode("utf-8")

    ```
    Add `Authorization: Basic <ENCODED_STRING>` to request headers
#### A Note:

- `POST /chat-rooms/message` will be used to handle media files instead of sending it through the websocket
- You must be logged in to send messages


#### An Example chat frontend can be found at `/chat`
other webpages:
 - `/chat/<room_name>`
 - `/logout`
 - `/auth/login`
