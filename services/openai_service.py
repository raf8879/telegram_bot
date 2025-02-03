import openai
import random
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY


difficulty_levels = {
    "A1": "simple and short sentences with basic vocabulary.",
    "A2": "slightly longer sentences with more varied vocabulary.",
    "B1": "complex sentences with intermediate vocabulary and grammar.",
    "B2": "long and detailed sentences with upper-intermediate vocabulary.",
    "C1": "advanced sentences with idioms and professional terms.",
    "C2": "highly advanced sentences with academic or professional phrasing.",
}

def generate_practice_sentences(topic: str, level: str, previous_sentences: list):
    """

    """
    adjectives = ["interesting", "engaging", "thought-provoking", "funny", "unusual"]
    chosen_adjective = random.choice(adjectives)
    previous_sentences_text = ' | '.join(previous_sentences) if previous_sentences else "None"

    prompt = (
        f"Generate 5 unique and {chosen_adjective} sentences about '{topic}' for English learners at level {level}. "
        f"Each sentence should be {difficulty_levels[level]} "
        f"and different from each other and from these sentences: {previous_sentences_text}. "
        f"Provide the sentences in a numbered list."
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant creating sentences for English practice."
            },
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
        temperature=0.9,
        presence_penalty=0.6,
        frequency_penalty=0.5,
    )
    return response

def chat_completion(role: str, messages: list, max_tokens=150, temperature=0.7):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": role}] + messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return response

def generate_image(prompt: str):
    response = openai.Image.create(
        prompt=prompt,
        model="dall-e-3",
        n=1,
        size="1024x1024",
        quality="standard",
    )
    return response
