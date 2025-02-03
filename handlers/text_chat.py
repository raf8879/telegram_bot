from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from states.chat_states import ChatStates
from services.analytics import load_analytics, save_analytics
from services.detailed_analytics import update_user_activity
from services.openai_service import chat_completion
from config import logger

router = Router()
analytics_data = load_analytics()

predefined_roles = {
    "ESL Tutor": "You are an ESL tutor helping students learn English.",
    "Math Teacher": "You are a math teacher assisting with math problems.",
    "Psychologist": "You are a psychologist providing support and guidance on anxiety.",
}

@router.message(F.text == '📝 Text chat')
async def test_chat_menu(message: Message, state: FSMContext):
    update_user_activity(message.from_user.id, message.from_user.full_name, feature='text_chat')
    kb = [
        ["ESL Tutor", "Math Teacher"],
        ["Psychologist", "🆕 Own role"],
        ["🔙 Back"]
    ]

    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=btn) for btn in row] for row in kb],
        resize_keyboard=True,
    )
    await message.answer("Choose a role or set your own:", reply_markup=keyboard)
    await state.set_state(ChatStates.choosing_role)

@router.message(ChatStates.choosing_role, F.text.in_(list(predefined_roles.keys())))
async def set_role(message: Message, state: FSMContext):
    update_user_activity(message.from_user.id, message.from_user.full_name)
    role_text = predefined_roles[message.text]
    await state.update_data(role=role_text, messages=[])
    await message.answer(f"Role set: '{message.text}'. You can start communicating.")
    await state.set_state(ChatStates.waiting_for_input)

@router.message(ChatStates.choosing_role, F.text == '🆕 Own role')
async def custom_role_prompt(message: Message, state: FSMContext):
    update_user_activity(message.from_user.id, message.from_user.full_name)
    await message.answer("Please describe the role that ChatGPT should take on:")
    await state.set_state(ChatStates.setting_custom_role)

@router.message(ChatStates.setting_custom_role)
async def set_custom_role(message: Message, state: FSMContext):
    update_user_activity(message.from_user.id, message.from_user.full_name)
    role = message.text.strip()
    await state.update_data(role=role, messages=[])
    await message.answer("Custom role set. You can start communicating.")
    await state.set_state(ChatStates.waiting_for_input)

@router.message(F.text == '🔙 Back')
async def back_to_main_menu(message: Message, state: FSMContext):
    from handlers.start import cmd_start
    await cmd_start(message, state)

@router.message(Command('clear'))
async def clear_context(message: Message, state: FSMContext):
    update_user_activity(message.from_user.id, message.from_user.full_name)
    await state.update_data(messages=[])
    await message.answer("The context has been cleared.")

@router.message(ChatStates.waiting_for_input)
async def chat_with_gpt(message: Message, state: FSMContext):
    update_user_activity(message.from_user.id, message.from_user.full_name)

    analytics_data['total_messages'] += 1
    save_analytics(analytics_data)

    user_data = await state.get_data()
    role = user_data.get('role', 'You are a helpful assistant.')
    messages = user_data.get('messages', [])

    if message.text and message.text.strip():
        messages.append({"role": "user", "content": message.text.strip()})
    messages = [m for m in messages if m.get("content")]

    if len(messages) > 20:
        messages = messages[-20:]

    try:
        response = chat_completion(role, messages, max_tokens=150, temperature=0.7)
        reply = response['choices'][0]['message']['content'].strip()
        messages.append({"role": "assistant", "content": reply})
        await state.update_data(messages=messages)

        await message.answer(reply)
    except Exception as e:
        await message.answer("An error occurred when accessing the AI.")
        logger.exception("Error when accessing the API")
