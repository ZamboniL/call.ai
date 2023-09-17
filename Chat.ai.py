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

dotenv.load_dotenv()
file_path = 'chat.txt'

if 'history' not in st.session_state:
    try:
        st.session_state.history = open(file_path, 'r').readlines()
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

st.title('Chat.ai')
st.caption('O chatbot que assume a identidade do seu contato.')
st.sidebar.title('Configurações')


contact_input = st.sidebar.text_input(
    "Qual o nome do seu contato?", st.session_state.contact)
user_input = st.sidebar.text_input("Qual o seu nome?", st.session_state.user)
upload_input = st.sidebar.file_uploader(
    "Envie o seu arquivo de chat do WhatsApp", type=['txt'])


if contact_input:
    st.session_state.contact = contact_input
    # store the contact name in a file
    with open('.contact', 'w') as f:
        f.write(contact_input)

if user_input:
    st.session_state.user = user_input
    # store the user name in a file
    with open('.user', 'w') as f:
        f.write(user_input)

# process the file line by line and save to chat.txt
if upload_input:
    with open(file_path, "w") as f:
        owner_message = False
        for line in upload_input:
            line = line.decode("utf-8").replace('\u200e', '')
            if st.session_state.contact not in line and re.search(r'\d{2}/\d{2}/\d{4}', line):
                owner_message = True
                continue

            if owner_message and st.session_state.contact not in line or '<Arquivo de mídia oculto>' in line:
                continue

            owner_message = False

            if re.search(r'\d{2}/\d{2}/\d{4}', line):
                index = line.find(st.session_state.contact)
                line = line[index:]

            f.write(line)
    st.session_state.history = open(file_path, 'r').readlines()


messages_string = '\n'.join(st.session_state.history)


user_prompt = st.chat_input(
    'Mande sua mensagem', disabled=not st.session_state.history)


container = st.container()

# if upload not done, stop the program

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


llm = ChatOpenAI(temperature=0.5, model='gpt-3.5-turbo-16k')
prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(
            f"""
            Você se chama {st.session_state.contact} e está conversando com o {st.session_state.user},
            essa conversa esta acontecendo pelo whatsapp.
            Em abaixo constam alguns exemplos de mensagens suas, copie os
            maneirismos, as girias e personalidades dessas mensagens:
            {messages_string}
            
"""),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{question}"),
    ]
)
memory = ConversationBufferMemory(
    llm=llm, memory_key='chat_history', return_messages=True)
conversation = LLMChain(memory=memory, llm=llm, verbose=True, prompt=prompt)

if user_prompt:
    st.session_state.chat.append('u: ' + user_prompt)
    response = conversation({"question": user_prompt})
    st.session_state.chat.append('a: ' + response['text'])

for message in st.session_state.chat:
    if message.startswith('u:'):
        with container.chat_message(name=st.session_state.user, avatar='user'):
            st.write(message[3:])
    else:
        with container.chat_message(name=st.session_state.contact, avatar='ai'):
            st.write(message[3:])
