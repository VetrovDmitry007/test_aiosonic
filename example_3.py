import asyncio
import aiosonic

async def get_hystori(num_page: int):
    async with aiosonic.HTTPClient(verify_ssl=False) as client:
        response = await client.get(f'https://www.google.com/')
        dc_res = {'num_page': num_page, 'status_code': response}
        return dc_res

async def main():
    ls_cur = [get_hystori(i) for i in range(1, 3)]
    for cur in asyncio.as_completed(ls_cur):
        result = await cur
        print(result)
    # ls_history = await asyncio.gather(*ls_task)
    # print(ls_history)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()