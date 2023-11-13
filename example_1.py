"""
Пример использования библиотеки aiosonic для выполнения GET-запроса к серверу Google
"""
import asyncio
import aiosonic

async def main():
    async with aiosonic.HTTPClient() as client:
        # Выполнение GET-запроса к серверу Google
        response = await client.get('https://www.google.com/')
        # проверяет, что статус ответа равен 200
        assert response.status_code == 200
        # проверяет, что текст ответа содержит слово "Google"
        # Если условие не выполняется, то assert вызывает исключение AssertionError.
        assert 'Google' in (await response.text())
        print(response.status_code)



if __name__ == '__main__':
    asyncio.run(main())
