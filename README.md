# Side-by-side Learn Web-App
___
## Установка зависимостей (backend)
### Prod/dev
`pip install -r backend/config/requirements.txt`
### Linting
`pip install -r backend/config/requirements_linting.txt`

## Установка зависимостей (frontend)
### Prod/dev
`npm install --prefix ./frontend`
___
## Запуск
`uvicorn main:app --reload` - backend

`cd ./frontend && npm run dev` - frontend
___
## Миграции
`alembic revision --autogenerate` - новая версия

`alembic upgrade head` - обновление БД до последней версии

`alembic downgrade -1` - Понижение версии БД на 1
