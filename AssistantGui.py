import streamlit as st
import openai
import requests
import os
from dotenv import load_dotenv

# Set up OpenAI API credentials
#openai.api_key = "YOUR_API_KEY"
load_dotenv('.env')
openai.api_type = "azure"
openai.api_base = "https://smartopaifranc.openai.azure.com/"
openai.api_version = "2023-07-01-preview"
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("AI Code Assistant")
option = st.selectbox(
     'What do you want to do?',
     ('Code Review', 'UT Generation', 'Test Case Generation'))

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# Allow user to upload a Java file
uploaded_file = st.file_uploader("Choose a Java file", type="java")

#'''You are an code reviewer that help developer find program languange potential issue, such as memory leak, empty pointer,unclosed resources, infinite loop etc.
##Unclosed resources: When working with input/output streams, it's important to ensure that any resources that are opened (such as InputStream or OutputStream objects) are closed when they are no longer needed. Failure to close these resources can lead to resource leaks and other issues. 
#Reading large input streams: When reading from input streams, it's important to be aware of the size of the stream. If the stream is very large, it may not be possible to read the entire stream into memory at once without causing an OutOfMemoryError. In these cases, it's best to read the stream in smaller chunks using a buffer. 
#Provide output for the issue only related current input.
#Expected output:
#Provide explanation about the issue.
#Provide solution for the issue.
#Provide the modified code that fix the issue.'''

system_prompt=""

review_prompt = "system: \nYou are an code reviewer that help developer find program languange potential issue, such as memory leak, empty pointer,unclosed resources, infinite loop etc.\n Unclosed resources: When working with input/output streams, it's important to ensure that any resources that are opened (such as InputStream or OutputStream objects) are closed when they are no longer needed. Failure to close these resources can lead to resource leaks and other issues. \n Reading larg input streams: When reading from input streams, it's important to be aware of the size of the stream. If the stream is very large, it may not be possible to read the entire stream into memory at once without causing an OutOfMemoryError. In these cases, it's best to read the stream in smaller chunks using a buffer. Provide output for the issue only related current input using chinese. Expected output:Provide explanation about the issue. Provide solution for the issue. Provide the modified code that fix the issue. for example: 问题：xxx  解决方案：xxxx 修改后的代码：xxxx"

ut_prompt="You are a developer that want to generate unit test for your code.\nProvide the code that you want to generate unit test.\nExpected output:\nProvide the unit test for the code."

tc_prompt="You are a QA that want to generate test case for code to make sure there is no issue .\nAnalysis the source code semantic and provide use cases that you want to test.\nExpected output:\nProvide formatted test suit and test case for the code."


match  option:
    case 'Code Review':
        system_prompt=review_prompt
        message = "user:\n OpenAI found the following issues with below code:"
    case 'UT Generation':
        system_prompt=ut_prompt
        message = "OpenAI generated the following unit test for your code:"
    case 'Test Case Generation':
        system_prompt=tc_prompt
        message = "OpenAI generated the following test case for your code:"


# If user has uploaded a file
if uploaded_file is not None:
    # Read the file contents
    file_contents = uploaded_file.read()

    # Call OpenAI API to review the code
    #'''response = openai.Completion.create(
    #    engine="fracengpt4",
    #    prompt=f"{system_prompt}:\n{file_contents.decode()}",
    #    max_tokens=1024,
    #    n=1,
    #    stop=None,
    #    temperature=0,
    #) '''

    conversation  = [{"role":"system","content":f"{system_prompt}"}]

    conversation.append({"role":"user","content":f"{message}:\n"+file_contents.decode()})

    response = openai.ChatCompletion.create(
        engine="gpt4turbo",
        messages = conversation,
        temperature=0,
        max_tokens=4096,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
        )

    print(response)
  

    color = "#0000ff"  # red
    st.write(f'<span style="color:{color}">{message}</span>', unsafe_allow_html=True)
    #st.write(message,color)

    content = response['choices'][0]['message']['content']
    st.write(content)
    print(content)
    # If OpenAI found issues with the code

    
        