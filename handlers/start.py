from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.context import FSMContext

from states.chat_states import ChatStates
from services.analytics import load_analytics, save_analytics
from services.detailed_analytics import update_user_activity
from config import OWNER_ID, logger

router = Router()


analytics_data = load_analytics()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    global analytics_data
    user_id = message.from_user.id

    update_user_activity(user_id, message.from_user.full_name, feature=None)


    if user_id not in analytics_data['total_users']:
        analytics_data['total_users'].add(user_id)
        save_analytics(analytics_data)


    kb_builder = ReplyKeyboardBuilder()
    kb_builder.button(text='📝 Text chat')
    kb_builder.button(text='🖼 Image generation')
    kb_builder.button(text='🗣 Conversation Mode')
    kb_builder.button(text='🎙 Pronunciation Check')
    kb_builder.adjust(2, 2)

    await message.answer("Welcome! Select a mode of operation:", reply_markup=kb_builder.as_markup())
    await state.clear()
