# Mocked API

A modular REST API built with **FastAPI**, **SQLAlchemy**, and **MySQL**, supporting multi-user roles, JWT authentication (with PyJWT), and API key management. This API provides endpoints for users, products, authentication, and API key CRUD operations, with auto-generated mock data using **Faker**.

- API: [https://mock-api.barcelos.dev](https://mock-api.barcelos.dev)

- SWAGGER: [https://mock-api.barcelos.dev/docs](https://mock-api.barcelos.dev/docs)

## Table of Contents

* [Features](#features)
* [Technologies](#technologies)
* [Project Structure](#project-structure)
* [Installation](#installation)
* [Configuration](#configuration)
* [Running the API](#running-the-api)
* [API Documentation](#api-documentation)

  * [Authentication](#authentication)
  * [API Key](#api-key)
  * [Users](#users)
  * [Products](#products)
* [Schemas](#schemas)
* [Security](#security)
* [License](#license)

---

## Features

* JWT-based authentication (`login` / `register`) using **PyJWT**
* API key management (create/delete API keys)
* Role-based access control (`admin`, `manager`, `vendor`, `customer`)
* CRUD operations for users and products
* Pagination support
* Auto-generation of mock data using **Faker**
* Password hashing with **bcrypt**

---

## Technologies

* **FastAPI** – API framework
* **SQLAlchemy** – ORM
* **MySQL** – Database
* **PyJWT** – JWT token handling
* **bcrypt** – Password hashing
* **Faker** – Mock data generation
* **Uvicorn** – ASGI server

---

## Project Structure

```
pythonanywhere/
│── main.py                 # Entry point
│── database.py             # Database connection and session
│── dependencies.py         # FastAPI dependencies
│── models/                 # SQLAlchemy models
│   ├── __init__.py
│   ├── user.py
│   ├── product.py
│   └── api_key.py
│── routers/                # API routes
│   ├── __init__.py
│   ├── auth.py
│   ├── users.py
│   ├── products.py
│   └── api_key.py
│── schemas/                # Pydantic schemas
│   ├── __init__.py
│   ├── user.py
│   ├── product.py
│   └── auth.py
│── utils/                  # Utility functions
│   ├── __init__.py
│   ├── security.py         # Password hashing/verification
│   └── auth.py             # JWT token creation/validation with PyJWT
│── requirements.txt        # Python dependencies
```

---

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd mock-api
```

2. Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install fastapi uvicorn sqlalchemy "pydantic[email]" pyjwt bcrypt faker mysql-connector-python
```

---

## Configuration

1. Update `DATABASE_URL` in `database.py`:

```python
DATABASE_URL = "mysql+mysqlconnector://<DB_USER>:<DB_PASSWORD>@<DB_HOST>/<DB_NAME>"
```

2. Set JWT configuration in `utils/auth.py`:

```python
SECRET_KEY = "your-super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
```

---

## Running the API

Start the development server:

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

FastAPI automatically provides **Swagger UI** at:

```
http://127.0.0.1:8000/docs
```

---

## API Documentation

### Authentication

| Endpoint         | Method | Description                            |
| ---------------- | ------ | -------------------------------------- |
| `/auth/register` | POST   | Register a new customer                |
| `/auth/login`    | POST   | Login with email/password, returns JWT |

**Example `register` request body:**

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "address": "123 Main St",
  "password": "password123"
}
```

**Example `login` request body:**

```json
{
  "email": "john@example.com",
  "password": "password123"
}
```

---

### API Key

| Endpoint | Method | Description                               |
| -------- | ------ | ----------------------------------------- |
| `/api`   | GET    | Create a new API key (returns admin user) |
| `/api`   | DELETE | Delete an existing API key                |

**Headers:** `API-Key: <your_api_key>`

---

### Users

| Endpoint      | Method | Description            |
| ------------- | ------ | ---------------------- |
| `/users`      | GET    | List users (paginated) |
| `/users`      | POST   | Create a new user      |
| `/users/{id}` | PUT    | Update user info       |
| `/users/{id}` | DELETE | Delete user            |

**Permissions:**

* Only `admin` can create/delete other users.
* Users can update their own profile.

---

### Products

| Endpoint         | Method | Description                      |
| ---------------- | ------ | -------------------------------- |
| `/products`      | GET    | List products (paginated)        |
| `/products`      | POST   | Create a product (admin only)    |
| `/products/{id}` | PUT    | Update a product (admin/manager) |
| `/products/{id}` | DELETE | Delete a product (admin only)    |

**Headers:** `API-Key: <your_api_key>`
**Permissions:** Role-based access control.

---

## Schemas

* `UserCreate` – input for creating users
* `UserResponse` – output for user info
* `ProductCreate` – input for creating products
* `ProductResponse` – output for product info
* `AuthLogin` – input for login
* `AuthResponse` – output for login JWT

---

## Security

* **Passwords** are hashed using **bcrypt**.
* **JWT tokens** are created/verified with **PyJWT**.
* **API keys** are required for all requests, even for authentication.
* Role-based permissions are enforced for sensitive actions.

---

## Notes

* The API automatically generates mock data for products and users if the database is empty, using **Faker**.
* Pagination defaults:

  * Users: 10 per page
  * Products: 20 per page

---

## License

MIT License – free to use and modify.
