from pydantic import BaseModel
from typing import Optional

class TestCase(BaseModel):
    id: Optional[int] = None
    title: str
    preconditions: str
    steps: str
    expected_result: str
    priority: str