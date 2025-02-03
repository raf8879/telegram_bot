import os
import tempfile
import whisper
from pydub import AudioSegment


model = whisper.load_model("base", device="cpu", download_root="./models")

async def transcribe_ogg_file(bot, file_id, file_path):

    with tempfile.TemporaryDirectory() as tmpdir:
        ogg_path = os.path.join(tmpdir, f"{file_id}.ogg")
        wav_path = os.path.join(tmpdir, f"{file_id}.wav")


        await bot.download_file(file_path, destination=ogg_path)


        audio = AudioSegment.from_file(ogg_path)
        audio.export(wav_path, format="wav")


        transcription = model.transcribe(wav_path, language="en")
        user_text = transcription["text"].strip()
        return user_text
