import requests
import streamlit as st
from bs4 import BeautifulSoup
from ollama import chat, ChatResponse
from datetime import datetime

MODEL_NAME = "qwen3.5:cloud"

with open("data/cv.txt") as f:
    cv = f.read()

st.title("Startup Analyzer")
st.caption("Mettez le lien du site web de la startup et appuyez sur 'Envoyer' !")

with st.form("website_analyzer"):
    website_url = st.text_input("Website URL")
    submit = st.form_submit_button("Envoyer")

if submit:
    response = requests.get(website_url)

    # Web scraping
    if response.status_code != 200:
        st.error(f"Erreur lors de la requête : {response.status_code}")
    else:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Summarize the startup in 3 dimensions to enable CV matching later
        chat_response: ChatResponse = chat(
            model=MODEL_NAME,
            messages=[
                {
                    'role': 'system',
                    'content': "Tu es un assistant pour la recherche d'emploi de l'utilisateur. L'utilisateur va te donner le contenu de la page web d'une entreprise, et tu vas devoir extraires ces 3 informations de manière claire et concise : l'offre concrète de l'entreprise, les utilisateurs cibles, et la stack technique probable de leur offre."
                },
                {
                    'role': 'user',
                    'content': soup.get_text()
                }
            ]
        )

        startup_summary = chat_response.message.content
        st.markdown(startup_summary)

        alignment_request = (
            f"# STARTUP OFFER:\n{startup_summary}\n"
            f"# USER'S RESUME:\n{cv}"
        )

        # Gives instructions to the LLM to compute the alignment between the user's resume and the startup
        now = datetime.now()
        formatted_date = now.strftime("%A, %B %d, %Y")
        chat_response: ChatResponse = chat(
            model=MODEL_NAME,
            messages=[
                {
                    'role': 'system',
                    'content': f"Date du jour: {formatted_date}. Tu es un assistant pour la recherche d'emploi de l'utilisateur. L'utilisateur va te donner le résumé de l'offre d'une startup, et tu vas devoir calculer l'alignement de cette startup avec mon CV. Le résultat sera un nombre entre 0 et 1."
                },
                {
                    'role': 'user',
                    'content': alignment_request
                }
            ]
        )

        # Display the answer as markdown for debugging
        st.markdown("# Alignement")

        alignment_score = chat_response.message.content
        st.markdown(alignment_score)