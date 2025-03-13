import json
import aiohttp
import logging
import time
import ssl
from config import TOKEN_URL, API_URL, AUTHORIZATION_KEY, SCOPE
from utils.logger import logger

class GigaChatService:
    def __init__(self):
        self.token = None
        self.token_expiry = 0  # Время истечения токена
        # Создаем SSL-контекст с пользовательским сертификатом
        self.ssl_context = ssl.create_default_context(cafile="/Users/ramilallahverdiev/Desktop/Chat_bot/venv/lib/python3.13/site-packages/certifi/cacert.pem")

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
                    ssl=self.ssl_context  # Используем SSL-контекст с сертификатом
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
    "model": "GigaChat",
    "messages": [
        {
            "role": "system",
            "content": "Ты QA-инженер. Создай тест-кейсы и верни их в формате JSON. Пример:\n"
                       "[\n"
                       "  {\n"
                       "    \"Название\": \"Тест-кейс 1\",\n"
                       "    \"Предусловия\": \"Предусловие 1\",\n"
                       "    \"Шаги\": \"Шаг 1\",\n"
                       "    \"Ожидаемый результат\": \"Ожидаемый результат 1\",\n"
                       "    \"Приоритет\": \"Высокий\"\n"
                       "  },\n"
                       "  {\n"
                       "    \"Название\": \"Тест-кейс 2\",\n"
                       "    \"Предусловия\": \"Предусловие 2\",\n"
                       "    \"Шаги\": \"Шаг 2\",\n"
                       "    \"Ожидаемый результат\": \"Ожидаемый результат 2\",\n"
                       "    \"Приоритет\": \"Средний\"\n"
                       "  }\n"
                       "]"
        },
        {
            "role": "user",
            "content": text
        }
    ],
    "temperature": 0.1
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
                        logger.info(f"Ответ от GigaChat API: {data}")  # Логируем полный ответ
                        
                        # Проверяем структуру ответа
                        if 'choices' not in data or not data['choices']:
                            logger.error("❌ Неправильная структура ответа: отсутствует 'choices'")
                            return None
                        
                        first_choice = data['choices'][0]
                        if 'message' not in first_choice or 'content' not in first_choice['message']:
                            logger.error("❌ Неправильная структура ответа: отсутствует 'message' или 'content'")
                            return None
                        
                        # Возвращаем содержимое ответа
                        return first_choice['message']['content']
                    else:
                        error = await resp.text()
                        logger.error(f"❌ Ошибка GigaChat API: {resp.status}, {error}")
                        return None
        except Exception as e:
            logger.error(f"❌ Ошибка подключения к GigaChat API: {e}")
            return None
        
    @staticmethod
    def parse_json_response(response: str) -> list:
        """
        Парсит JSON-ответ от GigaChat API в список тест-кейсов.
        
        :param response: JSON-строка с тест-кейсами.
        :return: Список тест-кейсов или пустой список в случае ошибки.
        """
        try:
            # Парсим JSON-строку
            test_cases = json.loads(response)
            
            # Проверяем, что это список
            if not isinstance(test_cases, list):
                logger.error("❌ Ответ от GigaChat не является списком.")
                return []
            
            return test_cases
        except json.JSONDecodeError as e:
            logger.error(f"❌ Ошибка парсинга JSON: {e}")
            return []
        except Exception as e:
            logger.error(f"❌ Ошибка при обработке JSON: {e}")
            return []