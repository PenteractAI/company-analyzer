from datetime import datetime
from ollama import chat, ChatResponse
from prompt_loader import load_prompt
import json

MODEL_NAME = "qwen3.5:cloud"

def get_current_date():
    return datetime.now().strftime("%A, %B %d, %Y")

def generate_json_response(prompt: str) -> dict | None:
    response: ChatResponse = chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": prompt["system"]},
            {"role": "user", "content": prompt["user"]},
        ],
    )

    try:
        parse_json = json.loads(response.message.content)
        return parse_json
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def get_summary(website_content: str) -> dict | None:

    prompt = load_prompt("summary", website_content=website_content, current_date=get_current_date())

    json_response = generate_json_response(prompt)
    return json_response


def get_resume_matching_score(company_summary: str, user_resume: str) -> dict | None:

    prompt = load_prompt("matching_score", company_summary=company_summary, user_resume=user_resume, current_date=get_current_date())

    json_response = generate_json_response(prompt)
    return json_response
