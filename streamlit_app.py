import streamlit as st
from openai import OpenAI
import base64
from pydub import AudioSegment
import io
import asyncio
from websockets.asyncio.server import serve, connect
from langchain_openai import ChatOpenAI


async def send_audio(audiofile, web_url):
    with open(audiofile, "rb") as f:
        audio_file = f.read()

    audio_b64 = base64.b64encode(audio_file).decode()
  
    async with connect(web_url) as websocket:
        # sends in b64
        await websocket.send(audio_b64)
        print("File sent to server")

        response = await websocket.recv()
    
    return response

st.title("📄 Document question answering")
st.write(
    "Upload a document below and ask a question about it – GPT will answer! "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
)

# Ask user for their OpenAI API key via `st.text_input`.

openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Let the user record audio.

    uploaded_audio = st.audio_input("Record message:")

    text = send_audio(uploaded_audio)
    st.write_stream(text)