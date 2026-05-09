# Side-by-side Learn Web-App
___
```
SBSLearn
├── backend/        # Сервер (backend) приложения
│   ├── auth/            # Блок, отвечающий за авторизацию и аутентификацию
│   ├── config/                # Библиотеки для работы backend (requirements.txt)
│   ├── lessons/        # Блок, отвечающий за уроки и практику
│   ├── migrations/        # Миграции (версии) для БД
│   ├── .env        # Переменные окружения
│   ├── .env.example        # Пример переменных окружения
│   ├── database.py        # Файл асинхронного подключения к БД
│   ├── Dockerfile        # Инструкции для создания образа контейнера в Docker
│   └── settings.py            # Файл конфигурации (работы с .env) и подключения к БД
├── frontend/        # клиент (frontend) приложения
│   ├── Dockerfile        # Инструкции для создания образа контейнера в Docker
│   ├── public/        # Иконки языков программирования
│   ├── src/        # Основная директория для frontend части (api, components, pages)
│   ├── Dockerfile        # Инструкции для создания образа контейнера в Docker
│   ├── package.json        # Библиотеки для работы frontendend
│   └── tailwind.config.js            # Файл конфигурации для TailwindCSS
├── alembic.ini                 # Файл конфигурации для alembic
├── docker-compose.yml          # Docker файл для запуска контейнеров (backend, frontend, piston_api)
├── main.py                      # Точка входа в приложение.
└── README.md                # Описание и команды для управления проектом
```
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
## Запуск (одной командой)
`docker compose up --build` - docker container (backend, frontend, piston)

## Запуск (по отдельности)
`uvicorn main:app --reload` - backend

`cd ./frontend && npm run dev` - frontend

`docker start piston_api` - piston api

___
## Инициализация docker контейнера piston api
```
docker run `
  --privileged `
  -v ${PWD}/piston_data:/piston `
  -dit `
  -p 2000:2000 `
  --name piston_api `
  ghcr.io/engineer-man/piston
```

через endpoint `/piston/language/install` - установка языков для piston
___
## Миграции
`alembic revision --autogenerate` - новая версия

`alembic upgrade head` - обновление БД до последней версии

`alembic downgrade -1` - Понижение версии БД на 1
___
## API endpoints
### user
1. Получить данные пользователя

GET `/protected/`

Headers:
```
Authorization: Bearer <access_token>
```

Response:
```
{
    "user": {
        "id": 8,
        "username": "test2",
        "email": "test2@mail.ru",
        "language_pair": {
            "id": 2,
            "slug": "python-vs-javascript",
            "lang1": {
                "id": 1,
                "name": "Python",
                "slug": "python",
                "icon_url": "/assets/python_icon.png"
            },
            "lang2": {
                "id": 3,
                "name": "JavaScript",
                "slug": "javascript",
                "icon_url": "/assets/js_icon.png"
            }
        }
    }
}
```

2. Выбрать языковую пару

POST `/select-languages-pair`

Request:
```
{
  "lang1_id": 1,
  "lang2_id": 2
}
```
Response:
```
{
  "msg": "Пара ЯП выбрана, прогресс инициализирован",
  "pair_slug": "python-vs-cpp"
}
```

3. Получение прогресса уроков для пользователя

GET `/lessons/user`

Headers:
```
Authorization: Bearer <access_token>
```

Response:
```
{
    "lessons": [
        {
            "id": 1,
            "title": "Введение в языки",
            "slug": "intro",
            "order_index": 1,
            "status": "available"
        },
        {
            "id": 2,
            "title": "Переменные и типы данных",
            "slug": "variables",
            "order_index": 2,
            "status": "locked"
        },
    ]
}
```
4. Завершить урок

POST `/lessons/{lesson_id}/complete`

Headers:
```
Authorization: Bearer <access_token>
```

Response:
```
{
  "result": True
}
```
5. Получить прогресс по языковым парам

GET `/lessons/progress`

Headers:
```
Authorization: Bearer <access_token>
```

Response:
```
{
    "user_id": 8,
    "progress": [
        {
            "language_pair_id": 1,
            "slug": "python-vs-cpp",
            "progress": 0
        },
        {
            "language_pair_id": 2,
            "slug": "python-vs-javascript",
            "progress": 0
        },
        {
            "language_pair_id": 3,
            "slug": "cpp-vs-javascript",
            "progress": 0
        }
    ]
}
```
___
### auth
1. Регистрация пользователя

POST `/auth/register`

Request:
```
{
  "login": "ivanov",
  "email": "ivanov@example.com",
  "password": "securepassword123"
}
```

Response:
```
{
  "User registered": True
}
```

2. Авторизация (вход) пользователя

POST `/auth/login`

Request:
```
{
  "login": "ivanov",
  "password": "securepassword123"
}
```
Response:
```
{
    "result": {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4IiwidXNlcm5hbWUiOiJ0ZXN0MiIsImVtYWlsIjoidGVzdDJAbWFpbC5ydSIsImlhdCI6MTc3ODMzMjA3MCwiZXhwIjoxNzc4MzM1NjcwfQ.MS17TkXwyXCbav7OH2F35EXODU2oCPDAQV3lRr8rWiQ",
        "token_type": "Bearer"
    }
}
```
3. Выход (завершение сессии)

POST `/auth/logout`

Headers:
```
Authorization: Bearer <access_token>
```
Response:
```
{
  "logout": True
}
```
___
### oauth
1. SSO авторизация пользователя через Google

GET `/google/login`

Redirect на `/google/callback`

2. Получение токена и данных об пользователе через Google

GET `/google/callback`

Redirect на frontend

3. SSO авторизация пользователя через Github

GET `/github/login`

Redirect на `/github/callback`

4. Получение токена и данных об пользователе через Github

GET `/github/callback`

Redirect на frontend
___
### languages
1. Получение списка всех языков программирования

GET `/languages`

Response:
```
{
    "languages": [
        {
            "slug": "python",
            "extension": "py",
            "icon_url": "/assets/python_icon.png",
            "name": "Python",
            "id": 1,
            "description": "Универсальный интерпретируемый язык программирования с простым синтаксисом. Отлично подходит для начинающих и широко используется в веб-разработке, анализе данных и автоматизации.",
            "demo_code": "#Test\r\nprint(\"Hello, Python!\")"
        },
    ]
}
```
___
### lessons
1. Получение тем уроков

GET `/lessons`

Response:
```
{
    "lessons": [
        {
            "order_index": 1,
            "title": "Введение в языки",
            "slug": "intro",
            "id": 1
        },
        {
            "order_index": 2,
            "title": "Переменные и типы данных",
            "slug": "variables",
            "id": 2
        },
    ]
}
```

2. Получение контента для темы урока

POST `/lessons/{lesson_id}/content?left_lang=cpp&right_lang=javascript`

Response:
```
{
    "title": "Условные операторы",
    "blocks": [
        {
            "type": "fact",
            "cpp": {
                "content": "В C++ условие в скобках должно быть выражением, которое преобразуется в `bool`. Ненулевые значения считаются `true`."
            },
            "javascript": {
                "content": "В JavaScript есть как строгое (`===`), так и нестрогое (`==`) сравнение. Нестрогое может приводить к неожиданным результатам (например, `0 == false` даёт `true`)."
            }
        },
        {
            "type": "side_by_side_code",
            "title": "Проверка числа на положительность, ноль или отрицательность",
            "snippets": {
                "cpp": {
                    "code": "#include <iostream>\nusing namespace std;\n\nint main() {\n    int x;\n    cout << \"Enter number: \";\n    cin >> x;\n    if (x > 0) {\n        cout << \"Positive\" << endl;\n    } else if (x == 0) {\n        cout << \"Zero\" << endl;\n    } else {\n        cout << \"Negative\" << endl;\n    }\n    return 0;\n}",
                    "label": "C++"
                },
                "javascript": {
                    "code": "let x = prompt(\"Enter number:\");\nx = Number(x);\nif (x > 0) {\n    console.log(\"Positive\");\n} else if (x === 0) {\n    console.log(\"Zero\");\n} else {\n    console.log(\"Negative\");\n}",
                    "label": "JavaScript"
                }
            },
            "description": "Пример if-elif-else (или else if) для трёх случаев."
        }
    ],
    "lessonSlug": "conditions",
    "description": "Как принимать решения в коде: if, else, switch и тернарный оператор."
}
```
___
### piston
1. Отправка кода на выполнение

POST `/piston/code/execute`

Request:
```
{
  "language": "python",
  "code": "# This is a comment\na=12\nb=13\nprint(f'{a}+{b}={a+b}')\nprint('Hello, world!')\n",
  "stdin": ""
}
```

Response:
```
{
  "stdout": "12+13=25\nHello, world!\n",
  "stderr": "",
  "output": "12+13=25\nHello, world!\n",
  "cpu_time": 29,
  "memory": 9776000,
  "message": null,
  "status": null
}
```

2. Получить список установленных языков

GET `/piston/installed_languages`

Response:
```
[
  {
    "language": "python",
    "language_version": "3.12.0",
    "installed": true
  },
  {
    "language": "javascript",
    "language_version": "20.15.0",
    "installed": true
  }
]
```
3. Установить языковой пакет

POST `/piston/language/install`

Request:
```
{
  "language": "python",
  "version": "*"
}
```

Response:
```
{
  "language": "python",
  "version": "3.12"
}
```
4. Удалить языковой пакет

DELETE `/piston/language/uninstall`

Request:
```
{
  "language": "python",
  "version": "*"
}
```

Response:
```
{
  "language": "python",
  "version": "3.12"
}
```
