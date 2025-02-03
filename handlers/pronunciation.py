from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder

import random
from config import logger
from states.chat_states import ChatStates
from services.detailed_analytics import update_user_activity
from services.analytics import load_analytics, save_analytics
from services.openai_service import generate_practice_sentences, difficulty_levels


router = Router()
analytics_data = load_analytics()

topics = ["Job Interview", "Travel", "About Myself", "Weather"]

@router.message(F.text == '🎙 Pronunciation Check')
async def pronunciation_menu(message: Message, state: FSMContext):
    update_user_activity(message.from_user.id, message.from_user.full_name, feature='pronunciation_check')

    kb_builder = ReplyKeyboardBuilder()
    for level in difficulty_levels:
        kb_builder.button(text=level)
    kb_builder.button(text='🔙 Back')
    kb_builder.adjust(2)

    await message.answer("Choose your difficulty level:", reply_markup=kb_builder.as_markup())
    await state.set_state(ChatStates.choosing_difficulty)

@router.message(ChatStates.choosing_difficulty, F.text.in_(difficulty_levels.keys()))
async def choose_difficulty(message: Message, state: FSMContext):
    update_user_activity(message.from_user.id, message.from_user.full_name)
    level = message.text
    await state.update_data(level=level)

    kb_builder = ReplyKeyboardBuilder()
    for topic in topics:
        kb_builder.button(text=topic)
    kb_builder.button(text='🔙 Back')
    kb_builder.adjust(2)

    await message.answer("Choose a topic for practice:", reply_markup=kb_builder.as_markup())
    await state.set_state(ChatStates.choosing_topic)


@router.message(ChatStates.choosing_topic, F.text.in_(topics))
async def generate_practice_sentence(message: Message, state: FSMContext):
    user_data = await state.get_data()
    level = user_data.get("level", "A1")
    topic = message.text
    previous_sentences = user_data.get("previous_sentences", [])

    await message.answer(f"Generating a practice sentence for level {level} and topic '{topic}'...")

    try:
        response = generate_practice_sentences(topic, level, previous_sentences)
        sentences = response['choices'][0]['message']['content'].strip().split('\n')
        sentences = [s.strip().lstrip('12345. ') for s in sentences if s.strip()]

        practice_sentence = random.choice(sentences)
        previous_sentences.append(practice_sentence)
        await state.update_data(previous_sentences=previous_sentences)
        await state.update_data(reference_text=practice_sentence)

        await message.answer(
            f"Here is your practice sentence:\n\n'{practice_sentence}'\n\n"
            "Please send a voice message reading this sentence."
        )
        await state.set_state(ChatStates.waiting_for_voice)
    except Exception as e:
        logger.error(f"Error generating practice sentence: {e}")
        await message.answer("An error occurred. Please try again.")


def generate_retry_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔄 Try Again")],
            [KeyboardButton(text="🆕 New Sentence")],
            [KeyboardButton(text="Back")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard

@router.message(F.text == "🔄 Try Again")
async def try_again(message: Message, state: FSMContext):
    user_data = await state.get_data()
    reference_text = user_data.get("reference_text", "No sentence found.")
    await message.answer(f"Please repeat the sentence:\n'{reference_text}'")

@router.message(F.text == "🆕 New Sentence")
async def new_sentence(message: Message, state: FSMContext):
    await pronunciation_menu(message, state)

@router.message(F.text == "Back")
async def back_to_main_menu(message: Message, state: FSMContext):
    from handlers.start import cmd_start
    await cmd_start(message, state)
