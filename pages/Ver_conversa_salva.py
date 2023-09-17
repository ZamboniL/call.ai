import streamlit as st

st.set_page_config(
    page_title="Chat.ai - Conversa salva",
    page_icon="🤖",
    initial_sidebar_state="expanded",
)

st.write("# Conversa salva")

try:
    history = open('chat.txt', 'r').readlines()
    st.info("Nós salvamos apenas as mensagens do seu contato, as suas mensagens não são salvas.")

    container = st.container()

    for message in history:
        with container.chat_message(name='Você', avatar='user'):
            st.write(message)
except:
    st.warning('Ainda não temos nenhuma conversa salva.')
