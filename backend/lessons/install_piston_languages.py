import asyncio
import httpx

LANGUAGES = [
    {
        "language": "python",
        "version": "*"
    },
    {
        "language": "javascript",
        "version": "*"
    },
    {
        "language": "c++",
        "version": "*"
    }
]


async def install_language(client, lang):
    try:
        r = await client.post(
            "http://piston:2000/api/v2/packages",
            json=lang
        )
        print(r.json())
    except Exception as e:
        print(f"skip {lang['language']}: {e}")


async def main():
    async with httpx.AsyncClient() as client:
        for language in LANGUAGES:
            await install_language(client, language)


if __name__ == "__main__":
    asyncio.run(main())