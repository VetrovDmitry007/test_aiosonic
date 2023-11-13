"""
Пример использования библиотеки aiosonic для выполнения запроса с таймаутом.
Устанавливается таймаут для чтения и подключения, выполняем GET-запрос к серверу Google
с установленными таймаутами и проверяем, что статус ответа равен 200 и содержит слово "Google".
"""
import asyncio
import aiosonic
from aiosonic.timeout import Timeouts

async def run():
    async with aiosonic.HTTPClient() as client:
        # Установка таймаутов
        timeouts = Timeouts(sock_read=10, sock_connect=3)

        # Выполнение GET-запроса к серверу Google с таймаутом
        response = await client.get('https://www.google.com/', timeouts=timeouts)
        assert response.status_code == 200
        assert 'Google' in (await response.text())

# Запуск асинхронной функции
asyncio.run(run())