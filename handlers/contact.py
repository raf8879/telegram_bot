from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("contact"))
async def send_contact(message: Message):
    await message.answer(
        "Связаться со мной можно, перейдя по ссылке: [Нажмите здесь](https://t.me/raf8879)",
        parse_mode="Markdown"
    )
