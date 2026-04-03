from datetime import datetime

from ollama import chat, ChatResponse
import json

MODEL_NAME = "qwen3.5:cloud"
SYSTEM_INSTRUCTIONS = "You are a helpful assistant designed to extract information into JSON to help the user with its job seeking. You will answer in French."


def generate_json_response(text_content: str) -> dict | None:
    response: ChatResponse = chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_INSTRUCTIONS},
            {"role": "user", "content": text_content},
        ],
    )

    try:
        parse_json = json.loads(response.message.content)
        return parse_json
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def get_summary(website_text: str) -> dict | None:

    text_content = f"""
        Extrait ces 3 informations de manière claire et concise : l'offre concrète de l'entreprise, les utilisateurs cibles, et la stack technique probable de leur offre.
        Texte : "{website_text}"
        Format JSON attendu : 
        {{
            "offer": "string",
            "target_users": "string",
            "tech_stack": "string"
        }}
    """

    json_response = generate_json_response(text_content)
    return json_response


def get_resume_matching_score(website_summary: str, resume_text: str) -> dict | None:

    now = datetime.now()

    formatted_date = now.strftime("%A, %B %d, %Y")

    text_content = f"""
        L'utilisateur va te donner le résumé de l'offre d'une startup, et tu vas devoir calculer l'alignement de cette startup avec mon CV. 
        Le résultat sera un nombre entre 0 et 1.
        Date du jour: {formatted_date}. 
        Résumé de l'entreprise : "{website_summary}"
        CV : "{resume_text}"
        Format JSON attendu :
        {{
            "score": "float between 0 and 1",
            "justification": "string"
        }}
    """

    json_response = generate_json_response(text_content)
    return json_response
