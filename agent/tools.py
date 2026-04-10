
from config import get_llm

llm = get_llm()



def analyze_review(input_text: str):
    prompt = f"""
    Analyze the following input.

    Input:
    {input_text}

    Return ONLY JSON (no explanation):
    {{
      "business_type": "restaurant/clinic/salon/theatre/retail/other",
      "sentiment": "positive/negative/neutral",
      "intent": "complaint/praise/suggestion/other",
      "urgency": "low/medium/high",
      "emotion": "happy/angry/frustrated/neutral"
    }}
    """

    try:
        response = llm.invoke(prompt)
        return response.content
    except:
        return """{
          "business_type": "other",
          "sentiment": "neutral",
          "intent": "other",
          "urgency": "medium",
          "emotion": "neutral"
        }"""


# 🔹 2. Business Context (no hardcoding)
def get_business_context(input_text: str):
    prompt = f"""
    Extract business context.

    Input:
    {input_text}

    Return ONLY JSON:
    {{
        "business_type": "...",
        "tone": "...",
        "language": "...",
        "persona": "..."
    }}
    """

    try:
        response = llm.invoke(prompt)
        return response.content
    except:
        return """{
            "business_type": "other",
            "tone": "neutral",
            "language": "English",
            "persona": "simple and polite"
        }"""



def generate_response(input_text: str):
    prompt = f"""
    You are an AI replying to a customer review.

    Context:
    {input_text}

    Instructions:
    - Detect requested language from context (Language field if present)
    - Respond STRICTLY in that language
    - Use LOCAL, NATURAL tone (not textbook translation)
    - Adapt tone based on business context automatically
    - Keep response short (2–3 lines max)
    - Sound human, not robotic

    Language behavior:
    - English → conversational
    - Hinglish → casual mix (Hindi + English)
    - Telugu → natural spoken Telugu (not formal)
    - Hindi → friendly conversational Hindi

    Avoid:
    - "Dear valued customer"
    - overly formal phrases
    - long paragraphs

    Output ONLY the final response.
    """

    try:
        response = llm.invoke(prompt)
        return response.content
    except:
        return "Thanks for your feedback. We'll work on improving!"
