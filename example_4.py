"""
Применение aiohttp совместно с asyncio.as_completed()
"""
import asyncio
import aiohttp
from time import perf_counter

async def get_hystori(num_page: int):
    async with aiohttp.ClientSession() as session:
        # async with session.get(f'https://eku.ru/category/story/?page={str(num_page)}', raise_for_status=True) as rec:
        try:
            async with session.get(f'https://fortuna-dom.ru/{num_page}', raise_for_status=True) as rec:
                # response = await rec.read()
                dc_res = {'num_page': num_page, 'status_code': rec.status}
        except:
            dc_res = {'num_page': num_page, 'status_code': 'Error'}
        finally:
            return dc_res


async def main():
    ls_cur = [get_hystori(i) for i in range(1, 500)]
    for cur in asyncio.as_completed(ls_cur):
        result = await cur
        print(result)


if __name__ == '__main__':
    t_1 = perf_counter()
    asyncio.run(main())
    print(perf_counter() - t_1)
    # 11.2, 10.6, 10.34, 10.2, 13.14 = 10.71