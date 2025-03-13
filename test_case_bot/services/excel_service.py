import pandas as pd
from io import BytesIO
from datetime import datetime

def create_excel_from_test_cases(test_cases_text: str) -> str:
    lines = [line.split("|") for line in test_cases_text.strip().split("\n") if line]
    
    df = pd.DataFrame(
        lines,
        columns=["Название", "Предусловия", "Шаги", "Ожидаемый результат", "Приоритет"]
    )
    
    file_name = f"test_cases_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    df.to_excel(file_name, index=False)
    
    return file_name