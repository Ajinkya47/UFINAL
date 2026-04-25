# learning_engine/ai_assistant.py

from google import genai
from django.conf import settings


# Configure Gemini
client = genai.Client(api_key=settings.GOOGLE_API_KEY)


def generate_ai_response(question, topic, level, accuracy=None):
    """
    Core Learning Engine Logic
    """

    # Adaptive Level Based on Accuracy (Optional)
    if accuracy is not None:
        if accuracy < 50:
            level = "Beginner"
        elif accuracy < 80:
            level = "Intermediate"
        else:
            level = "Advanced"

    difficulty_instruction = {
        "Beginner": "Explain in very simple language using real-life analogy.",
        "Intermediate": "Explain clearly with one technical example.",
        "Advanced": "Explain deeply with edge cases and complexity."
    }

    prompt = f"""
    You are an adaptive AI tutor.

    Student Level: {level}
    Topic: {topic}

    {difficulty_instruction.get(level)}

    Question: {question}

    Only answer if the question is related to academic syllabus.
    Keep answer under 200 words.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"Gemini API failed: {e}. Trying Groq fallback.")
        
        # Fallback to Groq
        try:
            from groq import Groq
            groq_key = getattr(settings, 'GROQ_API_KEY', '')
            if groq_key:
                groq_client = Groq(api_key=groq_key)
                response = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=250,
                )
                return response.choices[0].message.content.strip()
        except Exception as e2:
            logger.warning(f"Groq API fallback failed: {e2}")
            pass
        
        # If both fail or Groq not configured, return a friendly message instead of raising
        return "The AI service is currently busy (Too Many Requests). Please try again in a few moments."