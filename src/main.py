import uvicorn
from dishka.integrations.fastapi import setup_dishka

from src.setup.app import create_app
from src.setup.ioc import create_container

app = create_app()
container = create_container()
setup_dishka(container, app)

if __name__ == "__main__":
    # Запуск для локальної розробки (без Docker)
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)
