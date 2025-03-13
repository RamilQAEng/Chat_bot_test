import aiohttp
import logging
import time
import ssl
from config import TOKEN_URL, API_URL, AUTHORIZATION_KEY, SCOPE

class GigaChatService:
    def __init__(self):
        self.token = None
        self.token_expiry = 0  # Время истечения токена
        self.ssl_context = ssl.create_default_context()  # Контекст SSL

    async def _get_access_token(self):
        """
        Получает новый токен доступа от GigaChat API.
        """
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "RqUID": "6f0b129d-c7f3-4c16-a5f4-1234567890ab",  # Уникальный идентификатор запроса
            "Authorization": f"Basic {AUTHORIZATION_KEY}"  # Авторизация через Basic Auth
        }
        data = {"scope": SCOPE}  # Область действия токена
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    TOKEN_URL,
                    headers=headers,
                    data=data,
                    ssl=self.ssl_context  # Используем SSL-контекст
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        self.token = data.get("access_token")
                        self.token_expiry = time.time() + data.get("expires_in", 3600)  # Время жизни токена
                        logging.info("✅ Успешно получен новый Access Token")
                        return self.token
                    else:
                        error = await resp.text()
                        logging.error(f"❌ Ошибка получения Access Token: {resp.status}, {error}")
                        return None
        except Exception as e:
            logging.error(f"❌ Ошибка подключения к GigaChat API: {e}")
            return None

    async def get_valid_token(self):
        """
        Возвращает актуальный токен. Если токен истёк, запрашивает новый.
        """
        if not self.token or time.time() >= self.token_expiry:
            return await self._get_access_token()
        return self.token

    async def generate_test_cases(self, text: str):
        """
        Генерирует тест-кейсы на основе текста ТЗ.
        """
        token = await self.get_valid_token()
        if not token:
            logging.error("❌ Невозможно выполнить запрос: отсутствует Access Token")
            return None
        
        url = f"{API_URL}/chat/completions"  # URL для запроса к GigaChat API
        headers = {
            "Authorization": f"Bearer {token}",  # Используем Bearer Token для авторизации
            "Content-Type": "application/json"
        }
        payload = {
            "model": "GigaChat",  # Модель GigaChat
            "messages": [
                {
                    "role": "system",
                    "content": "Ты опытный QA-инженер. Создай тест-кейсы в формате: Название|Предусловия|Шаги|Ожидаемый результат|Приоритет"
                },
                {
                    "role": "user",
                    "content": text  # Текст ТЗ от пользователя
                }
            ],
            "temperature": 0.1  # Параметр температуры для генерации
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    json=payload,
                    headers=headers,
                    ssl=self.ssl_context  # Используем SSL-контекст
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data['choices'][0]['message']['content']  # Возвращаем сгенерированный текст
                    else:
                        error = await resp.text()
                        logging.error(f"❌ Ошибка GigaChat API: {resp.status}, {error}")
                        return None
        except Exception as e:
            logging.error(f"❌ Ошибка подключения к GigaChat API: {e}")
            return None