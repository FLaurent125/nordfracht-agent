from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def classify_reply(email_text: str) -> str:
    prompt = f"""
Lies folgende E-Mail-Antwort und schätze das Potenzial für eine Zusammenarbeit mit Nordfracht ein.
Gib **nur** eine der folgenden Kategorien zurück:

• sehr wahrscheinlich
• wahrscheinlich
• neutral
• unwahrscheinlich
• sehr unwahrscheinlich

Antwort:
\"\"\"
{email_text}
\"\"\"
Antwort nur als Kategorie:"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip().lower()

