"""

Выдаёт ошибку
"""
import asyncio
import aiosonic

async def get_hystori():
    async with aiosonic.HTTPClient(verify_ssl=False) as client:

        ls_cur = [client.get(f'https://eku.ru/category/story/?page={str(i)}') for i in range(1, 10)]
        for cur in asyncio.as_completed(ls_cur):
            result = await cur
            print(result.status_code)
        # await cur.connection.release()
        # await client.connection.release()


if __name__ == '__main__':
    asyncio.run(get_hystori())