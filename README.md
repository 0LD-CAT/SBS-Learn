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

## Инициализация docker контейнера piston api
docker run `
  --privileged `
  -v ${PWD}/piston_data:/piston `
  -dit `
  -p 2000:2000 `
  --name piston_api `
  ghcr.io/engineer-man/piston

___
## Запуск
`uvicorn main:app --reload` - backend

`cd ./frontend && npm run dev` - frontend

`docker start piston_api` - piston api

через endpoint `/piston/language/install` - установка языков для piston
___
## Миграции
`alembic revision --autogenerate` - новая версия

`alembic upgrade head` - обновление БД до последней версии

`alembic downgrade -1` - Понижение версии БД на 1

