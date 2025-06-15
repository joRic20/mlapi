# Iris Species Prediction API

**A secure, containerized FastAPI microservice for predicting the species of an Iris flower using a pre-trained machine learning model.**

---

## Table of Contents

1. [Features](#features)
2. [Architecture](#architecture)
3. [Prerequisites](#prerequisites)
4. [Getting Started](#getting-started)
5. [API Reference](#api-reference)

   * [Authentication](#authentication)
   * [`POST /predict`](#post-predict)
   * [`POST /hello`](#post-hello)
6. [Testing](#testing)
7. [Docker & Development](#docker--development)
8. [Deployment (CapRover)](#deployment-caprover)
9. [Contributing](#contributing)
10. [License](#license)

---

## Features

* **ML-driven predictions**: Random Forest model trained on the Iris dataset.
* **Input validation**: Strict schema enforcement with Pydantic.
* **Token-based authentication**: Secure endpoint access via `X-API-Token`.
* **Containerization**: Dockerfile and `docker-compose.yml` for consistent environments.
* **Effortless deployment**: One-command deploy to CapRover with CI/CD support.

---

## Architecture

1. **FastAPI** handles HTTP requests and automatically generates OpenAPI docs.
2. **Pydantic** validates incoming JSON payloads.
3. **Joblib** loads the pre-trained scikit-learn Random Forest model.
4. **Docker** ensures parity between development, testing, and production.
5. **CapRover** orchestrates CI/CD and environment configuration.

---

## Prerequisites

* Python 3.10+
* Docker & Docker Compose or Docker Desktop
* CapRover CLI (for production deploy)
* A CapRover server with DNS configured for `iris.yourdomain.com`

---

## Getting Started

1. **Clone the repo**

   ```bash
   git clone https://github.com/<your-username>/mlapi.git
   cd mlapi
   ```
2. **Environment variables**

   * Copy `.env.example` to `.env` and set your token:

     ```dotenv
     API_TOKEN=YOUR_SECRET_TOKEN
     ```
3. **Install dependencies**

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install --no-cache-dir -r app/requirements.txt
   ```
4. **Run locally**

   ```bash
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```
5. **Open the docs**

   * [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## API Reference

### Authentication

All protected endpoints require the `X-API-Token` header:

```
X-API-Token: YOUR_SECRET_TOKEN
```

### `POST /predict`

Predict the Iris species.

* **URL**: `/predict`
* **Method**: `POST`
* **Headers**:

  * `Content-Type: application/json`
  * `X-API-Token: YOUR_SECRET_TOKEN`
* **Body**:

  ```json
  {
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
  }
  ```
* **Success Response**:

  * **Code**: `200 OK`
  * **Content**:

    ```json
    { "species": "Iris-setosa" }
    ```
* **Error Responses**:

  * `401 Unauthorized` – invalid or missing token
  * `422 Unprocessable Entity` – validation error

### `POST /hello`

Lightweight health-check/greeting endpoint.

* **URL**: `/hello`
* **Method**: `POST`
* **Body**:

  ```json
  { "name": "Alice" }
  ```
* **Response**:

  ```json
  { "message": "Hello Alice" }
  ```

---

## Testing

Automated tests with **pytest** and FastAPI’s **TestClient**:

```bash
pytest
```

Tests cover:

* Valid prediction scenarios
* Authentication failures
* Input validation
* Health-check endpoint

---

## Docker & Development

1. **Build & run** locally with Docker Compose:

   ```bash
   ```

docker compose up --build

````
2. **Access**:
- API = http://127.0.0.1/predict
- Docs = http://127.0.0.1/docs
3. **Override code** live via volume mount (`./app:/app`).

---

## Deployment (CapRover)

1. **Login & Create App** `iris` on your CapRover server.
2. **Define** `captain-definition` at project root:
```json
{
  "schemaVersion": 2,
  "dockerfilePath": "./Dockerfile"
}
````

3. **Deploy** via CLI:

   ```bash
   caprover login
   caprover deploy
   ```
4. **Configure Env Var** in CapRover Web GUI:

   * Key: `API_TOKEN`
   * Value: your secret token
5. **Test** on production domain:

   * Predict: `https://iris.yourdomain.com/predict`
   * Docs:    `https://iris.yourdomain.com/docs`

---

## Contributing

Contributions are welcome! Please open an issue or a pull request with your suggestions.

---

## License

This project is licensed under the [MIT License](LICENSE).
