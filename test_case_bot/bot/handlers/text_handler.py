import json
from aiogram import types
from aiogram.fsm.context import FSMContext
from pydantic import ValidationError
from services.gigachat_service import GigaChatService
from services.excel_service import create_excel_from_test_cases
from database.db_client import DatabaseClient
from models.test_case import TestCase
from utils.logger import logger
from bot.keyboard.inline_keyboards import get_main_keyboard

gigachat = GigaChatService()

def parse_json_response(response: str):
    """
    Парсит JSON-ответ от GigaChat.
    """
    try:
        # Удаляем Markdown-код (```json и ```)
        if response.startswith("```json") and response.endswith("```"):
            response = response[7:-3].strip()  # Удаляем первые 7 и последние 3 символа
        return json.loads(response)
    except json.JSONDecodeError as e:
        logger.error(f"❌ Ошибка парсинга JSON: {e}")
        return None

async def process_text_tz(message: types.Message, state: FSMContext):
    logger.info("Обработка текстового ТЗ")
    await message.answer("⏳ Обрабатываю текст...")
    
    try:
        # Генерация тест-кейсов
        response = await gigachat.generate_test_cases(message.text)
        
        # Логирование ответа от GigaChat
        logger.info(f"Ответ от GigaChat: {response}")
        
        if not response:
            logger.error("❌ Ответ от GigaChat пустой.")
            return await message.answer("❌ Ошибка: сервис GigaChat не вернул данные.")
        
        # Парсинг JSON
        test_cases = parse_json_response(response)
        if not test_cases:
            return await message.answer("❌ Не удалось распарсить тест-кейсы.")
        
        # Логирование для отладки
        logger.info(f"Полученные тест-кейсы: {test_cases}")
        
        # === Сохранение в базу данных ===
        db = DatabaseClient()
        db.connect()
        
        for test_case_data in test_cases:
            try:
                # Преобразуем данные, если они приходят с русскоязычными ключами
                transformed_data = {
                    "title": test_case_data.get("Название", test_case_data.get("title", "")),
                    "preconditions": test_case_data.get("Предусловия", test_case_data.get("preconditions", "")),
                    "steps": test_case_data.get("Шаги", test_case_data.get("steps", "")),
                    "expected_result": test_case_data.get("Ожидаемый результат", test_case_data.get("expected_result", "")),
                    "priority": test_case_data.get("Приоритет", test_case_data.get("priority", ""))
                }
                
                # Заменяем None на пустую строку
                for key, value in transformed_data.items():
                    if value is None:
                        transformed_data[key] = ""
                
                # Создаём объект TestCase
                test_case = TestCase(**transformed_data)
                
                # Сохраняем в базу данных
                db.save_test_case(test_case)
                logger.info(f"✅ Тест-кейс сохранён: {test_case.title}")
            except ValidationError as e:
                logger.error(f"❌ Ошибка валидации тест-кейса: {e}")
                continue
            except Exception as e:
                logger.error(f"❌ Ошибка при сохранении тест-кейса: {e}")
                continue
        
        db.close()
        # === Конец сохранения в базу данных ===
        
        # Создание Excel-файла
        excel_file = create_excel_from_test_cases(test_cases)
        await message.answer_document(types.FSInputFile(excel_file), caption="✅ Готово! Вот тест-кейсы.")
        
        # Сбрасываем состояние
        await state.clear()
        
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await message.answer("⚠️ Произошла ошибка при обработке ТЗ.")
        await state.clear()

async def handle_button_press(message: types.Message, state: FSMContext):
    """Обработчик нажатий на кнопки клавиатуры"""
    if message.text == "📝 Отправить ТЗ":
        await message.answer("Пожалуйста, отправьте текст ТЗ.")
    elif message.text == "🆕 Новая сессия":
        await state.clear()
        await message.answer("🆕 Новая сессия начата. Отправьте мне ТЗ.", reply_markup=get_main_keyboard())
    elif message.text == "ℹ️ Помощь":
        await state.clear()
        await message.answer(
            "📚 Как использовать бота:\n"
            "1. Отправьте ТЗ в виде текста или файла.\n"
            "2. Дождитесь обработки.\n"
            "3. Получите Excel-файл с тест-кейсами.\n\n"
            "Доступные кнопки:\n"
            "📝 Отправить ТЗ - Отправить новое ТЗ\n"
            "🆕 Новая сессия - Начать новую сессию\n"
            "ℹ️ Помощь - Показать эту справку",
            reply_markup=get_main_keyboard()
        )
    else:
        return False
    return True

def register_handlers(dp):
    # Регистрируем обработчик кнопок
    dp.message.register(handle_button_press, lambda msg: msg.text in ["📝 Отправить ТЗ", "🆕 Новая сессия", "ℹ️ Помощь"])
    # Регистрируем обработчик текстовых сообщений
    dp.message.register(process_text_tz, lambda msg: msg.text and not msg.text.startswith('/') and msg.text not in ["📝 Отправить ТЗ", "🆕 Новая сессия", "ℹ️ Помощь"])