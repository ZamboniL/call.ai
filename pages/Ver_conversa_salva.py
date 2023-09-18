import streamlit as st
from state import (initialize_state, sidebar_config_inputs)

st.set_page_config(
    page_title="Chat.ai - Conversa salva",
    page_icon="🤖",
    initial_sidebar_state="expanded",
)

initialize_state()
sidebar_config_inputs()

st.write("# Conversa salva")

try:
    st.info("Nós salvamos apenas as mensagens do seu contato, as suas mensagens não são salvas.")

    container = st.container()

    for message in st.session_state.history:
        with container.chat_message(name='Você', avatar='user'):
            st.write(message)
except Exception:
    st.warning('Você ainda não submeteu uma conversa.')
