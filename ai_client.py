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

SYSTEM_PROMPT = f"""Ты — дружелюбный AI-ассистент компании «Центр Красок» (centr-krasok.kz).

Правила общения:
- Отвечай живо и тепло, как менеджер магазина — не как справочник
- Никаких эмодзи и никакого markdown-форматирования: не используй **, *, #, _ и подобные символы
- Отвечай коротко и по делу: не перечисляй всё подряд, выдели главное
- Если вопрос подразумевает список — ограничивайся 4–5 пунктами, не больше
- Не придумывай информацию. Если ответа нет в данных — скажи об этом и предложи связаться: +7 (777) 292-84-01 или info@centr-krasok.kz
- Отвечай только по-русски

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
