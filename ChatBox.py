
import streamlit as st
import openai
from openai import OpenAI
import os
from dotenv import load_dotenv
import time


# 设置 OpenAI API 密钥
load_dotenv('.env')
openai.api_type = "azure"
openai.api_base = "https://xxx.openai.azure.com/"
openai.api_version = "2023-07-01-preview"
openai.api_key = os.getenv("OPENAI_API_KEY")



st.title("ChatGPT")

#client = OpenAI(api_key=openai.api_key)

client = openai.AzureOpenAI(
        azure_endpoint=openai.api_base,
        api_key=openai.api_key,
        api_version="2023-12-01-preview"
    )

#if "openai_model" not in st.session_state:
#    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        start_time = time.time()
        for response in client.chat.completions.create(
            model="xxx",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            print(response)
            if len(response.choices)>0 and response.choices[0].delta.content is not None:
                full_response += str(response.choices[0].delta.content)
            
            message_placeholder.markdown(full_response + "▌")
            end_time = time.time()

       
        #message_placeholder.markdown(full_response)
        message_placeholder.markdown(full_response+f"\n        Time taken: {end_time - start_time:.2f}s")
       
    st.session_state.messages.append({"role": "assistant", "content": full_response})