from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from states.chat_states import ChatStates
from services.analytics import load_analytics, save_analytics
from services.detailed_analytics import update_user_activity
from config import logger
from services.openai_service import generate_image

router = Router()
analytics_data = load_analytics()

@router.message(F.text == '🖼 Image generation')
async def image_generation_prompt(message: Message, state: FSMContext):
    update_user_activity(message.from_user.id, message.from_user.full_name, feature='image_generation')
    await message.answer("Please describe the image you want to generate:")
    await state.set_state(ChatStates.generating_image)

def get_image_generation_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔄 Generate Image Again")],
            [KeyboardButton(text="🔙 Back")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

@router.message(F.text == "🔄 Generate Image Again")
async def re_generate_image(message: Message, state: FSMContext):
    await image_generation_prompt(message, state)

@router.message(ChatStates.generating_image)
async def do_generate_image(message: Message, state: FSMContext):
    update_user_activity(message.from_user.id, message.from_user.full_name)

    analytics_data['total_messages'] += 1
    save_analytics(analytics_data)

    prompt = message.text.strip()
    await message.answer("Generating image...")

    try:
        response = generate_image(prompt)
        image_url = response['data'][0]['url']
        await message.answer_photo(image_url)
    except Exception as e:
        await message.answer("An error occurred while generating the image.")
        logger.exception("An error occurred while generating the image.")
        return

    await state.clear()
    await message.answer(
        "What would you like to do next?",
        reply_markup=get_image_generation_keyboard()
    )
    await state.set_state(ChatStates.image_generation_options)
