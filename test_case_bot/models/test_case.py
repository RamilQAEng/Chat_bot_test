from pydantic import BaseModel

class TestCase(BaseModel):
    title: str  # Название тест-кейса
    preconditions: str  # Предварительные условия
    steps: str  # Шаги выполнения
    expected_result: str  # Ожидаемый результат
    priority: str  # Приоритет