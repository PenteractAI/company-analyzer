import requests
import streamlit as st
from bs4 import BeautifulSoup
from ollama import chat, ChatResponse

st.title("Startup Analyzer")
st.caption("Mettez le lien du site web de la startup et appuyez sur 'Envoyer' !")

with st.form("website_analyzer"):
    website_url = st.text_input("Website URL")
    submit = st.form_submit_button("Envoyer")

if submit:
    response = requests.get(website_url)

    # Web scraping
    if response.status_code != 200:
        print(f"Erreur lors de la requête : {response.status_code}")
        quit()
        
        
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Gives instructions to the LLM to extract company's offer, target users, and potential tech stack
    chat_response: ChatResponse = chat(
        model='qwen3.5:cloud',
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

    # Display the answer as markdown
    st.markdown(chat_response.message.content)