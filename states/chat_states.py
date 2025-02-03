from aiogram.fsm.state import State, StatesGroup

class ChatStates(StatesGroup):
    waiting_for_input = State()
    choosing_role = State()
    setting_custom_role = State()
    generating_image = State()
    waiting_for_voice = State()
    choosing_difficulty = State()
    choosing_topic = State()
    waiting_for_mode = State()
    conversation_mode = State()
    pronunciation_mode = State()
    waiting_for_reference_text = State()
    image_generation_options = State()
