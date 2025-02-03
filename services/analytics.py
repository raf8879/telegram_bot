import os
import json
from datetime import datetime, timedelta
from aiogram.fsm.storage.memory import MemoryStorage
from config import ANALYTICS_FILE, logger


def load_analytics():
    if os.path.exists(ANALYTICS_FILE):
        with open(ANALYTICS_FILE, 'r') as f:
            analytics_data = json.load(f)
            # Преобразуем множество пользователей из списка
            analytics_data['total_users'] = set(analytics_data['total_users'])
    else:
        analytics_data = {
            'total_users': set(),
            'total_messages': 0,
        }
    return analytics_data



def save_analytics(analytics_data):
    # Преобразуем множество пользователей в список для сохранения в JSON
    analytics_data_copy = analytics_data.copy()
    analytics_data_copy['total_users'] = list(analytics_data['total_users'])
    with open(ANALYTICS_FILE, 'w') as f:
        json.dump(analytics_data_copy, f)

