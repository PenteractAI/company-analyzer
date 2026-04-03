import requests
import prompts
import streamlit as st
import json

from bs4 import BeautifulSoup


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
        st.stop()

    soup = BeautifulSoup(response.text, "html.parser")
    website_text = soup.get_text()

    # Summarize the startup in 3 dimensions to enable CV matching later
    startup_summary_json = prompts.get_summary(website_text)

    if not startup_summary_json:
        st.error(f"Le résumé n'a pas pu être généré.")
        st.stop()

    startup_summary_md = f"""
        ## Offre
        {startup_summary_json['offer']} 
        
        ## Utilisateurs cibles 
        {startup_summary_json['target_users']}
        
        ## Stack technique
        {startup_summary_json['tech_stack']}
    """

    st.markdown(startup_summary_md)

    # Gives instructions to the LLM to compute the alignment between the user's resume and the startup
    matching_score = prompts.get_resume_matching_score(
        website_summary=json.dumps(startup_summary_json), resume_text=cv
    )

    if not matching_score:
        st.error(f"Le score d'alignement n'a pas pu être calculé.")
        st.stop()

    # Display the answer as markdown for debugging
    st.markdown(
        f"""
            # Alignement
            ## Score
            {matching_score['score']}

            ## Justification
            {matching_score['justification']}
        """
    )
