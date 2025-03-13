import sqlite3
from sqlite3 import Error
from models.test_case import TestCase
from utils.logger import logger

class DatabaseClient:
    def __init__(self, db_file="test_cases.db"):
        self.db_file = db_file
        self.conn = None

    def connect(self):
        """
        Подключается к базе данных и создаёт таблицу, если её нет.
        """
        try:
            self.conn = sqlite3.connect(self.db_file)
            logger.info(f"✅ Успешное подключение к базе данных: {self.db_file}")
            self._create_table()
        except Error as e:
            logger.error(f"❌ Ошибка подключения к базе данных: {e}")

    def _create_table(self):
        """
        Создаёт таблицу test_cases, если она не существует.
        """
        query = """
        CREATE TABLE IF NOT EXISTS test_cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            preconditions TEXT NOT NULL,
            steps TEXT NOT NULL,
            expected_result TEXT NOT NULL,
            priority TEXT NOT NULL
        );
        """
        try:
            self.conn.execute(query)
            self.conn.commit()
            logger.info("✅ Таблица 'test_cases' создана или уже существует.")
        except Error as e:
            logger.error(f"❌ Ошибка при создании таблицы: {e}")

    def save_test_case(self, test_case: TestCase) -> int:
        """
        Сохраняет тест-кейс в базу данных.

        :param test_case: Объект TestCase для сохранения.
        :return: ID сохранённого тест-кейса.
        """
        query = """
        INSERT INTO test_cases 
        (title, preconditions, steps, expected_result, priority)
        VALUES (?, ?, ?, ?, ?)
        """
        try:
            cur = self.conn.cursor()
            cur.execute(query, (
                test_case.title,
                test_case.preconditions,
                test_case.steps,
                test_case.expected_result,
                test_case.priority
            ))
            self.conn.commit()
            logger.info(f"✅ Тест-кейс сохранён: {test_case.title}")
            return cur.lastrowid
        except Error as e:
            logger.error(f"❌ Ошибка при сохранении тест-кейса: {e}")
            return None

    def close(self):
        """
        Закрывает соединение с базой данных.
        """
        if self.conn:
            self.conn.close()
            logger.info("✅ Соединение с базой данных закрыто.")