import dotenv
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
from state import (initialize_state, sidebar_config_inputs)


def create_conversation_chain():
    history_string = '\n'.join(st.session_state.history)

    llm = ChatOpenAI(temperature=1, model='gpt-3.5-turbo-16k', openai_api_key=st.session_state.key)
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


def chat_section(container, conversation):
    for message in st.session_state.chat:
        if message.startswith('u:'):
            with container.chat_message(name=st.session_state.user, avatar='user'):
                st.write(message[3:])
        else:
            with container.chat_message(name=st.session_state.contact, avatar='ai'):
                st.write(message[3:])

    if user_prompt := st.chat_input(
            'Mande sua mensagem', disabled=not st.session_state.history):
        with container.chat_message(name=st.session_state.user, avatar='user'):
            st.write(user_prompt)
        st.session_state.chat.append('u: ' + user_prompt)
        with st.spinner('Esperando resposta...'):
            response = conversation({"question": user_prompt})
            st.session_state.chat.append('a: ' + response['text'])
            with container.chat_message(name=st.session_state.contact, avatar='ai'):
                st.write(response['text'])


dotenv.load_dotenv()

st.set_page_config(page_title="Chat.ai", page_icon="🤖",
                   initial_sidebar_state="expanded", )
st.title('Chat.ai')
st.caption('O chatbot que assume a identidade do seu contato.')

initialize_state()
sidebar_config_inputs()

chat_container = st.container()

if not st.session_state.key:
    with chat_container.chat_message(name='Chat.ai', avatar='ai'):
        st.warning(
            "⬅️ Você precisa preencher a sua API Key do OpenAI para começar")
    st.stop()

if not st.session_state.history:
    with chat_container.chat_message(name='Chat.ai', avatar='ai'):
        st.warning(
            "⬅️ Envie o seu arquivo de WhatsApp e preencha os campos ao lado")
    st.stop()

if not st.session_state.contact or not st.session_state.user:
    with chat_container.chat_message(name='Chat.ai', avatar='ai'):
        st.warning(
            "⬅️ Temos um histórico de conversa salvo, porém você ainda precisa preencher os campos de nome ao lado")
    st.stop()

if len(st.session_state.history) < 100:
    with chat_container.chat_message(name='Chat.ai', avatar='ai'):
        st.warning(
            ':warning: Essa conversa tem poucas mensagens e pode causar o modelo à ser impreciso')

conversation = create_conversation_chain()

chat_section(chat_container, conversation)
