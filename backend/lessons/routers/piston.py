import httpx
from fastapi import APIRouter

from backend.settings import settings

router = APIRouter(tags=["Piston API"])
piston_api_uri=settings.PISTON_API_URI


@router.post("/piston/code/execute")
async def execute(request: dict):
    """Отправка кода на выполнение в контейнер Piston

    :param request: словарь вида:
        {
          "language": "python",
          "code": "# This is a comment\na=12\nb=13\nprint(f'{a}+{b}={a+b}')\nprint('Hello, world!')\n",
          "stdin": ""
        }
    :return: ответ-словарь вида:
        {
            "run": {
                "signal": null,
                "stdout": "12+13=25\nHello, world!\n",
                "stderr": "",
                "code": 0,
                "output": "12+13=25\nHello, world!\n",
                "memory": 9776000,
                "message": null,
                "status": null,
                "cpu_time": 29,
                "wall_time": 139
            },
            "language": "python",
            "version": "3.12.0"
        }
    """

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{piston_api_uri}/execute", json={
                "language": request["language"],
                "version": "*",
                "files": [
                    {
                        "content": request["code"]
                    }
                ],
                "stdin": request["stdin"],
                "compile_timeout": 0,
                "run_timeout": 0
            }
        )

    result = response.json()["run"]
    print(result)

    return {
        "stdout": result["stdout"],
        "stderr": result["stderr"],
        "output": result["output"],
        "cpu_time": result["cpu_time"],
        "memory": result["memory"],
        "message": result["message"],
        "status": result["status"]
    }


@router.get("/piston/installed_languages")
async def get_installed_languages():
    """Получение списка установленных языковых пакетов для Piston API

    :return: список словарей вида:
        [
            {
                "language": "python",
                "language_version": "3.12.0",
                "installed": true
            },
        ]
    """

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{piston_api_uri}/packages"
        )

    installed_languages = [item for item in response.json() if item.get("installed") is True]

    return installed_languages


@router.post("/piston/language/install")
async def install_language(request: dict):
    """Установка языка для Piston API

    :param request: словарь вида:
        {
            "language": "python",
            "version": "*"
        }
    :return: словарь
    """

    async with httpx.AsyncClient(timeout=600.0) as client:
        response = await client.post(
            f"{piston_api_uri}/packages", json=request
        )

    return response.json()


@router.delete("/piston/language/uninstall")
async def uninstall_language(request: dict):
    """Удаление языка из Piston API

    :param request: словарь вида:
        {
            "language": "python",
            "version": "*"
        }
    :return: словарь
    """

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.request(
            method="DELETE",
            url=f"{piston_api_uri}/packages",
            json=request
        )

    return response.json()
