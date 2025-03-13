import pandas as pd
from datetime import datetime
from utils.logger import logger

def create_excel_from_test_cases(test_cases: list, filename: str = None) -> str:
    """
    Создаёт Excel-файл из списка тест-кейсов.

    :param test_cases: Список тест-кейсов (каждый тест-кейс — это словарь).
    :param filename: Имя файла (если не указано, генерируется автоматически).
    :return: Имя созданного файла.
    """
    try:
        # Если имя файла не указано, генерируем его
        if not filename:
            filename = f"test_cases_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        # Создаём DataFrame из списка тест-кейсов
        df = pd.DataFrame(test_cases)
        
        # Сохраняем DataFrame в Excel-файл
        df.to_excel(filename, index=False)
        
        logger.info(f"✅ Excel-файл успешно создан: {filename}")
        return filename
    except Exception as e:
        logger.error(f"❌ Ошибка при создании Excel-файла: {e}")
        return None