from django.conf import settings
from dotenv import load_dotenv
from google import genai

from .models import PromptTemplate
from core.ai_instr import AI_PROMPT

load_dotenv()

client = genai.Client(api_key=settings.GOOGLE_API_KEY)


def get_embedding(text: str) -> list[float] | None:
    response = client.models.embed_content(
        model='gemini-embedding-001',
        contents=text
    )

    embedding_obj = response.embeddings[0]  # type: ignore
    return embedding_obj.values


def generate_answer(
    context: str = '', prompt: str = ''
) -> str:

    system_prompt = prompt or AI_PROMPT

    full_prompt = (
        'Отвечай строго по заданной теме\n'
        'Отвечай на том языке, на котором задан вопрос\n'
        f'{system_prompt}\n'
        f'{context}\n'
    )

    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=full_prompt
    )
    return response.text.strip()  # type: ignore


def get_current_prompt() -> str:
    obj = PromptTemplate.objects.filter(valid=True).first()
    return obj.prompt if obj and obj.prompt else AI_PROMPT
