import streamlit as st

st.set_page_config(
    page_title="Chat.ai - Como funciona?",
    page_icon="🤖",
)

st.write("#  🤖 Bem vindo ao Chat.ai 🤖")

st.markdown(
    """
    :robot: Chat.ai é um chatbot que utiliza inteligência artificial para assumir a
    identidade de uma pessoa. Para isso, basta que você envie um arquivo de
    texto exportado do WhatsApp e nos contar qual o nome do seu contato e o
    seu nome. 
    
    O Chat.ai irá analisar o seu arquivo e adaptar o seu chatbot para
    ser o seu contato, ele deve assumir os maneirismos, girias e a
    personalidade do seu contato.


    ## Como funciona?

    O Chat.ai utiliza a API do [OpenAI](https://openai.com/) para gerar
    respostas para as suas mensagens. Nós extraímos as mensagens do seu
    arquivo e enviamos uma **prompt** preparada para a API, instruindo
    o modelo a assumir a identidade do seu contato.

    ## Como usar?

    1. Exporte a conversa do WhatsApp em um arquivo de texto, siga as instruções
    [aqui](https://faq.whatsapp.com/android/chats/how-to-save-your-chat-history/?lang=pt_br).
    2. Nos informe o nome do seu contato :warning: **O nome deve ser exatamente igual ao que
    está salvo no seu celular**.
    3. Nos informe o seu nome, esse serve apenas para como o chatbot irá se referir a você.
    4. Envie o arquivo de texto exportado do WhatsApp.

    E pronto! O Chat.ai irá analisar o seu arquivo e gerar um chatbot que irá
    assumir a identidade do seu contato. Agora é só enviar mensagens e conversar como
    se fosse ele.
    

"""
)
