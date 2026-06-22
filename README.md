# Test ERP K2

Small ERP service to manage clients, products, and orders.

## Features
- Create clients, products, orders.
- Orders amount is automatically calculated.
- View all orders for a client.
- Simple HTMX frontend interface.

## Tech Stack
- **Backend:** FastAPI, Python 3.10+, SQLAlchemy (async), Asyncpg, Alembic.
- **Dependency Injection:** Dishka
- **Dependency Management:** Poetry
- **Database:** PostgreSQL
- **Frontend:** HTMX + HTML + CSS
- **Infrastructure:** Docker, Docker Compose

## Project Structure
We follow a modular architecture inspired by Django apps:
- `src/apps/`: Contains modules (`clients`, `products`, `orders`, `frontend`), each with their own `routers`, `services`, `repositories`, `schemas`.
- `src/core/`: Contains models and configuration.
- `src/infrastructure/`: Contains database setup.

## Running the Application

### Using Docker Compose
1. Make sure Docker is running.
2. Run the application:
   ```bash
   docker-compose up --build
   ```
3. Open the app in your browser: [http://localhost:8000](http://localhost:8000)
4. API docs (Swagger) available at: [http://localhost:8000/docs](http://localhost:8000/docs)

### Running locally without Docker
1. Make sure you have a running PostgreSQL instance and create a database named `test_erp`.
2. Install dependencies:
   ```bash
   poetry install
   ```
3. Run migrations:
   ```bash
   poetry run alembic upgrade head
   ```
4. Start the application:
   ```bash
   poetry run uvicorn src.main:app --reload
   ```

## Tests
To run tests locally:
```bash
poetry run pytest
```
