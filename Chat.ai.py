import dotenv
import re
import streamlit as st
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


FILE_PATH = 'chat.txt'


def _initialize_state():
    if 'history' not in st.session_state:
        try:
            st.session_state.history = open(FILE_PATH, 'r').readlines()
        except:
            st.session_state.history = []
    if 'chat' not in st.session_state:
        st.session_state.chat = []

    if 'contact' not in st.session_state:
        try:
            st.session_state.contact = open('.contact', 'r').read()
        except:
            st.session_state.contact = 'Ex: João'

    if 'user' not in st.session_state:
        try:
            st.session_state.user = open('.user', 'r').read()
        except:
            st.session_state.user = 'Ex: Maria'


def _format_history(upload):
    with open(FILE_PATH, "w") as f:
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

            f.write(line)
    st.session_state.history = open(FILE_PATH, 'r').readlines()


def _format_user_name(user):
    st.session_state.user = user
    with open('.user', 'w') as f:
        f.write(user)


def _format_contact_name(contact):
    st.session_state.contact = contact
    with open('.contact', 'w') as f:
        f.write(contact)


def _user_configuration_section():
    st.sidebar.title('Configurações')

    contact_input = st.sidebar.text_input(
        "Qual o nome do seu contato?", st.session_state.contact)
    user_input = st.sidebar.text_input(
        "Qual o seu nome?", st.session_state.user)
    upload_input = st.sidebar.file_uploader(
        "Envie o seu arquivo de chat do WhatsApp", type=['txt'])

    if upload_input:
        _format_history(upload_input)

    if contact_input:
        _format_contact_name(contact_input)

    if user_input:
        _format_user_name(user_input)


def _check_if_user_configuration_is_done(container):
    if not st.session_state.history:
        with container.chat_message(name='Chat.ai', avatar='ai'):
            st.warning(
                "⬅️ Envie o seu arquivo de WhatsApp e preencha os campos ao lado para começar")
        st.stop()

    if st.session_state.contact.find('Ex:') != -1 or st.session_state.user.find('Ex:') != -1:
        with container.chat_message(name='Chat.ai', avatar='ai'):
            st.warning(
                "⬅️ Temos um histórico de conversa salvo, porém você ainda precisa preencher os campos de nome ao lado para começar")
        st.stop()

    if len(st.session_state.history) < 100:
        with container.chat_message(name='Chat.ai', avatar='ai'):
            st.warning(
                ':warning: Essa conversa tem poucas mensagens e pode causar o modelo à ser impreciso')


def _create_conversation_chain():
    history_string = '\n'.join(st.session_state.history)

    llm = ChatOpenAI(temperature=1, model='gpt-3.5-turbo-16k')
    prompt = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(
                f"""
                Você deve assumir a personalidade de {st.session_state.contact} com base em suas conversas de WhatsApp. Use as mensagens a seguir como dados de treinamento para adaptar sua IA e responder como {st.session_state.contact}:
                {history_string}
                O objetivo é você interagir em conversas semelhantes às de {st.session_state.contact}, incorporando seu estilo de comunicação e personalidade.
            """),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{question}"),
        ]
    )
    memory = ConversationBufferMemory(
        llm=llm, memory_key='chat_history', return_messages=True)
    conversation = LLMChain(memory=memory, llm=llm,
                            verbose=True, prompt=prompt)
    return conversation


def _chat_section(container, conversation):
    user_prompt = st.chat_input(
        'Mande sua mensagem', disabled=not st.session_state.history)

    for message in st.session_state.chat:
        if message.startswith('u:'):
            with container.chat_message(name=st.session_state.user, avatar='user'):
                st.write(message[3:])
        else:
            with container.chat_message(name=st.session_state.contact, avatar='ai'):
                st.write(message[3:])

    if user_prompt:
        st.session_state.chat.append('u: ' + user_prompt)
        with container.chat_message(name=st.session_state.user, avatar='user'):
            st.write(user_prompt)

        with st.spinner('Esperando resposta...'):
            response = conversation({"question": user_prompt})
            st.session_state.chat.append('a: ' + response['text'])
            with container.chat_message(name=st.session_state.contact, avatar='ai'):
                st.write(response['text'])


def main():
    _initialize_state()

    st.title('Chat.ai')
    st.caption('O chatbot que assume a identidade do seu contato.')
    container = st.container()

    _user_configuration_section()
    _check_if_user_configuration_is_done(container)
    conversation = _create_conversation_chain()

    _chat_section(container, conversation)


if __name__ == "__main__":
    st.set_page_config(page_title="Chat.ai", page_icon="🤖",
                       initial_sidebar_state="expanded",)
    dotenv.load_dotenv()

    main()
