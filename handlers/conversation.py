from aiogram import Router, F
from aiogram.types import Message, FSInputFile, Voice
from aiogram.fsm.context import FSMContext
from states.chat_states import ChatStates
from services.detailed_analytics import update_user_activity
from config import logger
from gtts import gTTS
from datetime import datetime
import os
import tempfile

from services.whisper_service import model  # Или отдельную функцию если есть
import asyncio
import openai
from services.openai_service import chat_completion

router = Router()

@router.message(F.text == "🗣 Conversation Mode")
async def conversation_mode(message: Message, state: FSMContext):
    update_user_activity(message.from_user.id, message.from_user.full_name, feature='conversation_mode')
    await message.answer(
        "You have entered Conversation mode for practicing English.\n"
        "The bot will help you with grammar, pronunciation, vocabulary, and communication.\n"
        "If you want to clear the history, enter the /clear command.\n"
        "Start the dialogue!"
    )
    await state.update_data(role="You are a friendly conversational partner helping the user practice English.", messages=[])
    await state.set_state(ChatStates.conversation_mode)

@router.message(F.voice, ChatStates.conversation_mode)
async def handle_voice_message(message: Message, state: FSMContext):
    update_user_activity(message.from_user.id, message.from_user.full_name)

    try:
        voice_file = await message.bot.get_file(message.voice.file_id)
        file_path = voice_file.file_path

        with tempfile.TemporaryDirectory() as tmpdir:
            ogg_path = os.path.join(tmpdir, f"{message.voice.file_id}.ogg")
            wav_path = os.path.join(tmpdir, f"{message.voice.file_id}.wav")
            await message.bot.download_file(file_path, destination=ogg_path)

            # Whisper:
            from pydub import AudioSegment
            audio = AudioSegment.from_file(ogg_path)
            audio.export(wav_path, format="wav")

            transcription = model.transcribe(wav_path, language="en")
            user_text = transcription["text"].strip()
            logger.info(f"Recognized text: {user_text}")
            await message.answer(f"You said: {user_text}")

        user_data = await state.get_data()
        role = user_data.get('role',
                             "You are a friendly and knowledgeable English tutor. "
                             "Always be encouraging, etc...")
        messages = user_data.get('messages', [])
        messages.append({"role": "user", "content": user_text})

        if len(messages) > 20:
            messages = messages[-20:]


        try:
            response = chat_completion(role, messages, max_tokens=150, temperature=0.7)
            bot_reply = response['choices'][0]['message']['content']
        except Exception as e:
            logger.error(f"Error when accessing the API: {e}")
            await message.answer("An error occurred while processing the request. Please try again.")
            return

        messages.append({"role": "assistant", "content": bot_reply})
        await state.update_data(messages=messages)


        try:
            tts = gTTS(text=bot_reply, lang="en")
            response_voice_path = os.path.join(tmpdir,
                                               f"{message.from_user.id}_{datetime.now().timestamp()}_response.ogg")
            tts.save(response_voice_path)

            voice = FSInputFile(response_voice_path)
            await message.answer_voice(voice)
        except Exception as e:
            logger.error(f"Error generating voice response: {e}")
            await message.answer("An error occurred while generating the voice response. Please try again.")

    except Exception as e:
        logger.error(f"Error processing voice message: {e}")
        await message.answer("An error occurred while processing your voice message. Please try again.")
