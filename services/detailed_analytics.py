import os
import json
from datetime import datetime, timedelta
from config import DETAILED_ANALYTICS_FILE, logger, OWNER_ID


def load_detailed_analytics():
    if os.path.exists(DETAILED_ANALYTICS_FILE):
        with open(DETAILED_ANALYTICS_FILE, 'r') as f:
            return json.load(f)
    else:
        return {
            'users': {},  # Структура: {user_id: {"name": str, "last_active": str}}
            'daily_stats': {},
            'feature_usage': {
                'text_chat': 0,
                'image_generation': 0,
                'pronunciation_check': 0,
                'conversation_mode': 0
            }
        }


def save_detailed_analytics(data):
    for date_key, stats in data['daily_stats'].items():
        if isinstance(stats['users'], set):
            stats['users'] = list(stats['users'])
    with open(DETAILED_ANALYTICS_FILE, 'w') as f:
        json.dump(data, f, indent=4)


def update_user_activity(user_id, user_name, detailed_analytics, feature=None):
    current_time = datetime.now()
    detailed_analytics['users'][user_id] = {
        "name": user_name,
        "last_active": current_time.isoformat()
    }


    date_key = current_time.strftime('%Y-%m-%d')
    if date_key not in detailed_analytics['daily_stats']:
        detailed_analytics['daily_stats'][date_key] = {'messages': 0, 'users': set()}
    detailed_analytics['daily_stats'][date_key]['messages'] += 1


    for d_key, stats in detailed_analytics['daily_stats'].items():
        if not isinstance(stats['users'], set):
            stats['users'] = set(stats['users'])
    detailed_analytics['daily_stats'][date_key]['users'].add(user_id)


    if feature:
        if feature not in detailed_analytics['feature_usage']:
            detailed_analytics['feature_usage'][feature] = 0
        detailed_analytics['feature_usage'][feature] += 1

    save_detailed_analytics(detailed_analytics)


def get_detailed_analytics(detailed_analytics):
    current_time = datetime.now()
    total_users = len(detailed_analytics['users'])
    user_names = list(set([details["name"] for details in detailed_analytics['users'].values()]))


    users_data = {str(uid): details for uid, details in detailed_analytics['users'].items()}


    last_hour_users = [
        user_id for user_id, details in users_data.items()
        if current_time - datetime.fromisoformat(details["last_active"]) <= timedelta(hours=1)
    ]


    date_key = current_time.strftime('%Y-%m-%d')
    today_stats = detailed_analytics['daily_stats'].get(date_key, {})
    today_users = len(today_stats.get('users', set()))
    today_messages = today_stats.get('messages', 0)


    week_users = {
        user_id for user_id, details in users_data.items()
        if current_time - datetime.fromisoformat(details["last_active"]) <= timedelta(weeks=1)
    }
    week_messages = 0
    for d_key, stats in detailed_analytics['daily_stats'].items():
        dt = datetime.strptime(d_key, '%Y-%m-%d')
        if current_time - dt <= timedelta(weeks=1):
            week_messages += stats.get('messages', 0)


    month_users = {
        user_id for user_id, details in users_data.items()
        if current_time - datetime.fromisoformat(details["last_active"]) <= timedelta(days=30)
    }
    month_messages = 0
    for d_key, stats in detailed_analytics['daily_stats'].items():
        dt = datetime.strptime(d_key, '%Y-%m-%d')
        if current_time - dt <= timedelta(days=30):
            month_messages += stats.get('messages', 0)


    avg_messages_per_user = today_messages / today_users if today_users > 0 else 0

    return {
        "total_users": total_users,
        "user_names": user_names,
        "last_hour_users": len(set(last_hour_users)),
        "today_users": today_users,
        "week_users": len(set(week_users)),
        "month_users": len(set(month_users)),
        "feature_usage": detailed_analytics.get('feature_usage', {})
    }
