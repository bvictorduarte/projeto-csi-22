import streamlit as st
import os
import asyncio
from dotenv import load_dotenv
from src.controllers.chat_controller import ChatController

# Carrega variáveis de ambiente
load_dotenv()

# Configuração do controller
controller = ChatController()

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
    
    # Processa a mensagem
    with st.chat_message("assistant"):
        try:
            response = asyncio.run(controller.process_message(
                [msg["content"] for msg in st.session_state.messages]
            ))
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            error_msg = "Desculpe, ocorreu um erro ao processar sua mensagem. Por favor, tente novamente."
            st.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg}) 