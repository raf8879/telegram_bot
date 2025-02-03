from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from config import OWNER_ID
from services.analytics import load_analytics
from services.detailed_analytics import (load_detailed_analytics,
                                        get_detailed_analytics)

router = Router()
analytics_data = load_analytics()
detailed_analytics = load_detailed_analytics()

@router.message(Command('analytics_1'))
async def show_analytics(message: Message):
    if message.from_user.id != OWNER_ID:
        await message.answer("You do not have permission to execute this command.")
        return

    total_users = len(analytics_data['total_users'])
    total_messages = analytics_data.get('total_messages', 0)

    analytics_message = (
        f"📊 Bot usage statistics:\n"
        f"👥 Total number of users: {total_users}\n"
        f"💬 Total number of messages: {total_messages}"
    )

    await message.answer(analytics_message)

@router.message(Command('analytics_2'))
async def show_detailed(message: Message):
    if message.from_user.id != OWNER_ID:
        await message.answer("You do not have permission to execute this command.")
        return

    stats = get_detailed_analytics(detailed_analytics)

    analytics_message = (
        f"📊 **Bot Analytics:**\n"
        f"👥 Total Users: {stats['total_users']}\n"
        f"📋 Names of Users: {', '.join(stats['user_names'])}\n"
        f"🕒 Active Users (Last Hour): {stats['last_hour_users']}\n"
        f"📆 Active Users (Today): {stats['today_users']}\n"
        f"📅 Active Users (This Week): {stats['week_users']}\n"
        f"📈 Active Users (This Month): {stats['month_users']}\n\n"
        f"📌 **Feature Usage:**\n"
        f"📝 Text Chat: {stats['feature_usage'].get('text_chat', 0)}\n"
        f"🖼 Image Generation: {stats['feature_usage'].get('image_generation', 0)}\n"
        f"🎙 Pronunciation Check: {stats['feature_usage'].get('pronunciation_check', 0)}\n"
        f"🗣 Conversation Mode: {stats['feature_usage'].get('conversation_mode', 0)}\n"
    )
    await message.answer(analytics_message)
