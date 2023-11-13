"""
Применение aiosonic совместно с asyncio.as_completed()

!!! Диспетчер HTTPClientконтекста зависает при выходе,
если содержимое ответа не читается или соединение ответа не освобождается вручную.

Ожидаемое поведение
Ответное соединение должно быть разорвано автоматически. --  await response.connection.release()
"""
import asyncio
import aiosonic

async def get_hystori(num_page: int):
    async with aiosonic.HTTPClient(verify_ssl=False) as client:
        response = await client.get(f'https://eku.ru/category/story/?page={str(num_page)}')
        dc_res = {'num_page': num_page, 'status_code': response.status_code}
        await response.connection.release()
        return dc_res

async def main():
    ls_cur = [get_hystori(i) for i in range(1, 10)]
    for cur in asyncio.as_completed(ls_cur):
        result = await cur
        print(result)


if __name__ == '__main__':
    asyncio.run(main())