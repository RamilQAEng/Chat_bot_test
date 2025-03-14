# Тестовый Бот для Генерации Тест-Кейсов

Этот проект представляет собой бота, который помогает генерировать тест-кейсы на основе текстовых заданий. Бот использует API GigaChat для обработки текстов и создания тест-кейсов в формате Excel.

## Структура проекта

```
test_case_bot/
│
├── bot/
│   ├── __init__.py
│   ├── bot.py
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── commands.py
│   │   ├── document_handler.py
│   │   ├── inline_handlers.py
│   │   ├── states.py
│   │   └── text_handler.py
│   └── keyboard/
│       ├── __init__.py
│       └── inline_keyboards.py
│
├── config.py
├── database/
│   ├── __init__.py
│   └── db_client.py
│
├── logs/
│   └── bot_YYYYMMDD_HHMMSS.log
│
├── models/
│   └── test_case.py
│
├── services/
│   ├── excel_service.py
│   └── gigachat_service.py
│
├── .env
├── .gitignore
└── requirements.txt
```

## Установка

1. **Клонируйте репозиторий:**

   ```bash
   git clone <URL_вашего_репозитория>
   cd <имя_папки_репозитория>
   ```

2. **Создайте виртуальное окружение:**

   ```bash
   python -m venv venv
   ```

3. **Активируйте виртуальное окружение:**

   - На Windows:
     ```bash
     venv\Scripts\activate
     ```
   - На macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Установите зависимости:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Настройте переменные окружения:**

   Создайте файл `.env` в корне проекта и добавьте следующие переменные:

   ```plaintext
   BOT_TOKEN="ваш_токен_бота"
   CLIENT_ID="ваш_client_id"
   AUTHORIZATION_KEY="ваш_authorization_key"
   SCOPE="GIGACHAT_API_PERS"
   TOKEN_URL="https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
   API_URL="https://gigachat.devices.sberbank.ru/api/v1"
   ```

## Запуск

Для запуска бота выполните следующую команду:

```bash
python -m bot.bot
```

## Использование

- После запуска бота, вы можете отправить команду `/start`, чтобы начать взаимодействие с ботом.
- Используйте команду `/help`, чтобы получить информацию о доступных командах.

## Логирование

Логи работы бота будут сохраняться в папке `logs/` с именем файла в формате `bot_YYYYMMDD_HHMMSS.log`.

## Вклад

Если вы хотите внести свой вклад в проект, пожалуйста, создайте форк репозитория и отправьте пулл-реквест с вашими изменениями.

## Лицензия

Этот проект лицензирован под MIT License. Пожалуйста, смотрите файл LICENSE для получения дополнительной информации.