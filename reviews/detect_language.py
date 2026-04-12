from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def detect_language_style(review_text):
    prompt = f"""
    Detect the language style of this customer review.

    Possible outputs only:
    - english
    - hinglish
    - telugu_english
    - hindi_english
    - mixed

    Review:
    "{review_text}"

    Return only one label.
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt}
        ],
        model="llama-3.1-8b-instant"
    )

    return chat_completion.choices[0].message.content.strip().lower()