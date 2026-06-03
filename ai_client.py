from openai import AsyncOpenAI
from config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, OPENROUTER_MODEL

client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL,
)


def load_company_info() -> str:
    try:
        with open("company_info.txt", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""


COMPANY_INFO = load_company_info()

SYSTEM_PROMPT = f"""Ты — AI-ассистент компании «Центр Красок» (centr-krasok.kz).
Отвечай только на основе информации о компании, приведённой ниже.
Если вопрос выходит за рамки информации о компании или ответа нет в данных — вежливо сообщи об этом и предложи обратиться напрямую: +7 (777) 292-84-01 или info@centr-krasok.kz.
Не придумывай информацию. Отвечай по-русски, кратко и по делу.

--- ИНФОРМАЦИЯ О КОМПАНИИ ---
{COMPANY_INFO}
--- КОНЕЦ ИНФОРМАЦИИ ---"""


async def get_ai_response(history: list[dict]) -> str:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history
    response = await client.chat.completions.create(
        model=OPENROUTER_MODEL,
        messages=messages,
        max_tokens=1024,
        temperature=0.3,
    )
    return response.choices[0].message.content
