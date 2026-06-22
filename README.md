# Test ERP K2

Small ERP service to manage clients, products, and orders.

## Features
- Create and manage clients, products, and orders.
- Orders amount is automatically calculated based on product prices and quantities.
- View all orders for a specific client.
- Simple HTMX frontend interface for interactions.

## Tech Stack
- **Backend:** FastAPI, Python 3.12+, SQLAlchemy (async), Asyncpg, Alembic.
- **Dependency Injection:** Dishka
- **Dependency Management:** Poetry
- **Database:** PostgreSQL
- **Frontend:** HTMX + HTML + CSS + Jinja2 Templates
- **Infrastructure:** Docker, Docker Compose
- **Linting & Formatting:** Ruff, Pre-commit

## Project Structure
We follow a modular architecture inspired by Django apps:
- `src/apps/`: Contains modules (`clients`, `products`, `orders`, `frontend`). Each domain module includes:
  - `routers.py`: FastAPI route definitions.
  - `services.py`: Core business logic.
  - `repositories.py`: Database access layer using SQLAlchemy.
  - `schemas.py`: Pydantic models for validation.
  - `provider.py`: Dishka dependency injection providers.
- `src/core/`: Contains base models, custom exceptions, application config, and logging.
- `src/infrastructure/`: Contains database connection setup and session management.
- `src/setup/`: Contains application initialization and DI container configuration.

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
3. Install frontend dependencies and build TypeScript:
   ```bash
   npm install
   npm run build:ts
   ```
4. Run migrations:
   ```bash
   poetry run alembic upgrade head
   ```
5. Start the application:
   ```bash
   poetry run python -m src.main
   ```

## Development and Linting
We use `pre-commit` and `ruff` to ensure code quality and formatting.

To run linters across the entire project:
```bash
poetry run pre-commit run --all-files
```

## Tests
To run tests locally:
```bash
poetry run pytest
```
