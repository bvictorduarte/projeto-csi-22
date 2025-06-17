import streamlit as st
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

st.title("Assistente de POO 🎓")

# Inicializa o histórico de mensagens se não existir
if "messages" not in st.session_state:
    st.session_state.messages = []

# Interface de chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input do usuário
if prompt := st.chat_input("Digite sua mensagem..."):
    # Adiciona mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Resposta temporária para teste
    with st.chat_message("assistant"):
        response = "Olá! Estou aqui para ajudar com POO. (Resposta de teste)"
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response}) 