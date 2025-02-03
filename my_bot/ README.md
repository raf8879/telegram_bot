Telegram English Tutor Bot
A Telegram bot designed to help users practice English speaking, pronunciation, and conversation skills. The bot utilizes cutting-edge AI technologies from OpenAI (ChatGPT and DALL·E) and Whisper for speech recognition. Key features include:

Text-based chat with multiple “role” options (ESL Tutor, Math Teacher, Psychologist, etc.)
Voice-based Conversation Mode (with voice replies generated via gTTS)
Pronunciation Check (using Whisper and real-time feedback)
Image Generation (using DALL·E)
Detailed analytics and usage statistics for the bot owner
Table of Contents
Project Status
Key Features
Tech Stack
Installation
Usage
File and Folder Structure
Environment Variables
Analytics
Planned Improvements
License
Author
Project Status
This project is currently under active development (MVP stage). Features may change, and bugs may exist.

Key Features
Text Chat

Users can select different “roles” (ESL tutor, Psychologist, etc.) to interact with the bot in various contexts.
The bot stores recent conversation history to maintain context with the user.
Voice Conversation Mode

Supports voice messages from the user, recognized via Whisper.
The bot responds in voice form (via gTTS), emulating a real conversation partner.
Pronunciation Check

Provides practice sentences at different difficulty levels (A1–C2).
After the user sends a voice note, the bot compares the recognized text with the target sentence and offers feedback or corrections.
Image Generation

Uses OpenAI’s DALL·E to generate custom images from text prompts.
Analytics

Tracks the total number of users and messages.
Offers basic (/analytics_1) and detailed (/analytics_2) analytics for the bot owner (specified via OWNER_ID).
Session/Context Clearing

The /clear command erases conversation history for a fresh start.
An inactivity timeout automatically clears user context after 15 minutes.
Tech Stack
Python 3.9+
aiogram for Telegram Bot API
OpenAI API (ChatGPT for text, DALL·E for image generation)
Whisper for speech-to-text
gTTS for text-to-speech
pydub for audio conversions
dotenv for environment variable management


Installation
1. Clone the repository:
git clone https://github.com/raf8879/telegram_bot.git

2. python -m venv venv
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate


3. Install dependencies:
pip install -r requirements.txt

4. Configure environment variables:
Copy the .env.example file to .env:
cp .env.example .env
Fill in the required tokens/keys (e.g., TELEGRAM_BOT_TOKEN, OPENAI_API_KEY, OWNER_ID).


5. Run the bot:
python main.py

Once the bot starts, you can interact with it via Telegram using the bot token you provided.



Usage
Start the bot: Send /start in Telegram to access the main menu.
Text Chat: Choose “📝 Text chat,” select a role, and chat with the AI assistant.
Conversation Mode: Choose “🗣 Conversation Mode,” send voice messages to the bot, and listen to its voice replies.
Pronunciation Check: Choose “🎙 Pronunciation Check,” pick a difficulty and topic, then read the provided sentence in a voice message. The bot provides feedback on your pronunciation.
Image Generation: Choose “🖼 Image generation,” describe the image you want, and the bot will generate a DALL·E image link for you.
Analytics (admin-only):
/analytics_1 – basic analytics (total users, message count)
/analytics_2 – detailed analytics (e.g., usage per day, top features)



Analytics
analytics.json: Tracks base stats (total users, total messages).
detailed_analytics.json: Stores more granular data: daily user counts, feature usage, timestamps, etc.
Use /analytics_1 and /analytics_2 (owner-only commands) to view summaries in Telegram.

Planned Improvements
Additional advanced roles for text chat (e.g., “Professional Resume Reviewer,” “Career Counselor”).
Enhanced error handling, especially around network timeouts or OpenAI errors.
Real-time user prompts for advanced pronunciation corrections (phonetic details, etc.).
Webhook integration (replacing polling).
Dockerization for easier deployment.


License
This project is licensed under the MIT License. You are free to use, modify, and distribute this software in compliance with the license terms.

Author:
Rafael Dzhabrailov
Contact: 📩 Email: rafaelrafael8879@gmail.com 🔗 LinkedIn: www.linkedin.com/in/rafael-dzhabrailov-756716330
GitHub: https://github.com/raf8879
Feel free to reach out with questions, suggestions, or feedback!
