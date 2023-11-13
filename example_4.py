"""
Применение aiohttp совместно с asyncio.as_completed()
"""
import asyncio
import aiohttp

async def get_hystori(num_page: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://eku.ru/category/story/?page={str(num_page)}', raise_for_status=True) as rec:
            # response = await rec.read()
            dc_res = {'num_page': num_page, 'status_code': rec.status}
            return dc_res

async def main():
    ls_cur = [get_hystori(i) for i in range(1, 200)]
    for cur in asyncio.as_completed(ls_cur):
        result = await cur
        print(result)


if __name__ == '__main__':
    asyncio.run(main())