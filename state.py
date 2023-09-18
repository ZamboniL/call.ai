import streamlit as st
import re


def initialize_state():
    if 'history' not in st.session_state:
        st.session_state.history = []

    if 'chat' not in st.session_state:
        st.session_state.chat = []

    if 'key' not in st.session_state:
        st.session_state.key = ''

    if 'contact' not in st.session_state:
        st.session_state.contact = ''

    if 'user' not in st.session_state:
        st.session_state.user = ''


def _format_history(upload):
    other_person = False
    for line in upload:
        line = line.decode("utf-8").replace('\u200e', '')

        # Skip messages that are not from the target contact
        if st.session_state.contact not in line and re.search(r'\d{2}/\d{2}/\d{4}', line):
            other_person = True
            continue

        # Skip multiline messages that are not from the target contact or are media files
        if other_person and st.session_state.contact not in line or '<Arquivo de mídia oculto>' in line:
            continue

        other_person = False

        if re.search(r'\d{2}/\d{2}/\d{4}', line):
            index = line.find(st.session_state.contact)
            line = line[index:]

        st.session_state.history.append(line)


def sidebar_config_inputs():
    with st.sidebar:
        st.title('Configurações')

        if key_input := st.text_input("OpenAI API Key", st.session_state.key, type='password', autocomplete='off'):
            st.session_state.key = key_input

        if contact_input := st.text_input("Qual o nome do seu contato?", st.session_state.contact):
            st.session_state.contact = contact_input

        if user_input := st.text_input("Qual o seu nome?", st.session_state.user):
            st.session_state.user = user_input

        if upload_input := st.file_uploader("Envie o seu arquivo de chat do WhatsApp", type=['txt']):
            _format_history(upload_input)
