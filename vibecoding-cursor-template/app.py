## pip install streamlit google-genai
## pip install python-dotenv

import streamlit as st
from google import genai
from google.genai.errors import APIError
import os
from dotenv import load_dotenv

# Carrega as variáveis do ficheiro .env
load_dotenv()

# Configuração da Página Streamlit
st.set_page_config(
    page_title="Gerador de User Stories & Critérios de Aceite (Vibe Coding)",
    layout="centered"
)

st.title("✨ Gerador de User Stories & Critérios de Aceite")
st.markdown("Vibe: **Automação da Documentação e Foco na Qualidade da Feature**")

# Inicializar o cliente Gemini
# Tenta obter a chave da variável de ambiente GEMINI_API_KEY
api_key = os.getenv("GEMINI_API_KEY")
client = None

if api_key:
    try:
        # A API do Gemini usa a chave automaticamente se estiver no ambiente ou for passada
        client = genai.Client(api_key=api_key)
    except Exception as e:
        st.error(f"Erro ao inicializar o cliente Gemini: {e}")
        st.warning("Verifique se a chave na variável de ambiente GEMINI_API_KEY é válida.")
else:
    st.error("ERRO DE CONFIGURAÇÃO: A variável de ambiente 'GEMINI_API_KEY' não foi encontrada. Certifique-se de que o ficheiro `.env` existe na raiz e que a chave está lá definida.")


# --- Formulário de Input ---
with st.form("user_story_form"):
    st.header("1. Detalhes da User Story")
    
    # Textos de entrada para os 3 elementos da User Story
    user_role = st.text_input(
        "Tipo de Utilizador (Como...)",
        placeholder="Ex: PM, Cliente VIP, Utilizador Não Autenticado",
        key="role"
    )
    
    feature = st.text_input(
        "Funcionalidade (Quero poder...)",
        placeholder="Ex: Quero poder exportar relatórios",
        key="feature"
    )
    
    benefit = st.text_input(
        "Valor/Benefício (Para que...)",
        placeholder="Ex: Para poder partilhar os dados com a gestão",
        key="benefit"
    )
    
    generate_button = st.form_submit_button("Gerar User Story & Critérios de Aceite")

# --- Lógica de Geração ---

# Só processa se o botão foi clicado E o cliente Gemini foi inicializado com sucesso
if generate_button and client:
    if not all([user_role, feature, benefit]):
        st.error("Por favor, preencha todos os campos do formulário para gerar a User Story.")
    else:
        # 1. Gerar a User Story no formato padrão
        user_story = f"**Como {user_role}**, **quero {feature}**, **para que {benefit}**."
        
        # 2. Gerar o Prompt para a IA
        prompt_ia = f"""
        Gera 4 a 6 Critérios de Aceite (Acceptance Criteria, CAs) **claros e testáveis** para a seguinte User Story.
        
        Foca-te em cobrir diferentes aspetos da funcionalidade: regras de negócio, interface, e casos limite/sucesso.
        
        User Story: "{user_story.replace('**', '')}"
        
        Formato de Saída:
        Apenas uma lista numerada ou com marcadores (bullet points), sem introduções ou conclusões.
        """
        
        st.subheader("2. Resultado da Geração")
        st.success(user_story)
        
        st.subheader("3. Critérios de Aceite (Gerados pela IA)")
        
        # Usar o st.empty para manter o spinner visível
        ca_placeholder = st.empty()
        
        with st.spinner("A IA está a pensar nos critérios de qualidade..."):
            try:
                # Chamar a API do Gemini
                response = client.models.generate_content(
                    model="gemini-2.5-flash",  # Um modelo rápido e eficaz
                    contents=prompt_ia,
                    config=genai.types.GenerateContentConfig(
                        temperature=0.3
                    )
                )
                
                # Exibir os Critérios de Aceite (CAs) formatados
                ca_placeholder.markdown(response.text)

            except APIError as e:
                ca_placeholder.error(f"Ocorreu um erro na chamada à API do Gemini: {e}")
                ca_placeholder.warning("Verifique a sua chave API e os limites de utilização.")
            except Exception as e:
                ca_placeholder.error(f"Ocorreu um erro inesperado: {e}")

# Footer de Vibe Coding
st.markdown("---")
st.caption("Projeto Vibe Coding: Automação e Qualidade - Powered by Streamlit & Gemini")