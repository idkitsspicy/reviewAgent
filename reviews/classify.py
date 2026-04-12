import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def classify_review(review_text):
    prompt = f"""
Classify this customer review sentiment.

Possible outputs only:
- POSITIVE
- NEGATIVE

Review:
"{review_text}"

Return only one label.
"""

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt}
        ],
        model="llama3-8b-8192",
        temperature=0
    )

    return chat_completion.choices[0].message.content.strip()
