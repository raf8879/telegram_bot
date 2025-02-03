import os
import logging
import warnings
from dotenv import load_dotenv

warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

load_dotenv()  # Загружаем переменные окружения

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка токенов из переменных окружения
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ID владельца бота (используется в analytics)
OWNER_ID = int(os.getenv("OWNER_ID", "YOUR_ID"))

# Файл для базовой аналитики
ANALYTICS_FILE = 'analytics.json'

# Файл для детализированной аналитики
DETAILED_ANALYTICS_FILE = 'detailed_analytics.json'
