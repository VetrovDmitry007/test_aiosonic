"""
Пример использования библиотеки aiosonic для выполнения GET-запроса к серверу Google
"""
import asyncio
import aiosonic

async def main():
    async with aiosonic.HTTPClient() as client:
        # Выполнение GET-запроса к серверу Google
        # response = await client.get('https://www.google.com/')
        response = await client.get('https://eku.ru/category/story/?page=1')
        # проверяет, что статус ответа равен 200
        assert response.status_code == 200
        # проверяет, что текст ответа содержит слово "Google"
        # Если условие не выполняется, то assert вызывает исключение AssertionError.
        # assert 'Google' in (await response.text())
        print(response.status_code)
        await response.connection.release()



if __name__ == '__main__':
    asyncio.run(main())
