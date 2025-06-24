def suggest_times() -> str:
    prompt = """
Schlage zwei konkrete Zeitfenster für ein 30-minütiges Telefongespräch in den nächsten Tagen vor – möglichst Mittwoch oder Donnerstag vormittags.

Format:
- Mittwoch, 10:00 Uhr
- Donnerstag, 09:30 Uhr
"""
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content.strip()


