import logging
import os
from datetime import datetime

# Создаем папку для логов, если её нет
if not os.path.exists("logs"):
    os.makedirs("logs")

# Настройка формата логов
log_format = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    handlers=[
        logging.FileHandler(f"logs/bot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),  # Логи в файл
        logging.StreamHandler()  # Логи в консоль
    ]
)

logger = logging.getLogger(__name__)