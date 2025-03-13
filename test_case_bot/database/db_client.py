import sqlite3
from sqlite3 import Error
from models.test_case import TestCase

class DatabaseClient:
    def __init__(self, db_file="test_cases.db"):
        self.db_file = db_file
        self.conn = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_file)
            self._create_table()
        except Error as e:
            print(f"Database error: {e}")

    def _create_table(self):
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
        self.conn.execute(query)
        self.conn.commit()

    def save_test_case(self, test_case: TestCase):
        query = """
        INSERT INTO test_cases 
        (title, preconditions, steps, expected_result, priority)
        VALUES (?, ?, ?, ?, ?)
        """
        cur = self.conn.cursor()
        cur.execute(query, (
            test_case.title,
            test_case.preconditions,
            test_case.steps,
            test_case.expected_result,
            test_case.priority
        ))
        self.conn.commit()
        return cur.lastrowid

    def close(self):
        if self.conn:
            self.conn.close()