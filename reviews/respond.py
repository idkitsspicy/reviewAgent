import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_response(review_text, tone, intent,language_style,memory):
    
    strategy = {
        "complaint": "Apologize and offer resolution",
        "praise": "Thank warmly and invite again",
        "neutral": "Acknowledge politely"
    }

    prompt = f"""
    You are a local business owner replying to customer reviews in a warm, natural, human-like tone.

Customer Review:
{review_text}

Review Intent:
{intent}

Desired Tone:
{tone}

Response Strategy:
{strategy[intent]}

Detected Language Style:
{language_style}
Owner Memory Preferences:
- Preferred Tone: {memory['preferred_tone']}
- Emoji Usage: {memory['emoji_usage']}
- Reply Length: {memory['reply_length']}
- Preferred Language Style: {memory['language_preference']}

Instructions:
- Generate one concise reply under 25 words.
- Match the customer's language style naturally.
If Telugu words are written in English script like:
  andi, chala, bagundi, mee, malli
  classify as telugu_english.
- If Hindi words dominate:
  classify as hinglish or hindi_english.
- Be culturally accurate.
- If review contains native Unicode language text, reply in same native script.
- Sound authentic, conversational, and friendly.
- Avoid robotic or overly formal wording.
- Do not repeat the review text.
- Output only the reply message.
"""

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt}
        ],
        model="llama-3.1-8b-instant"
    )

    return chat_completion.choices[0].message.content