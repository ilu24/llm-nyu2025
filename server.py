import streamlit as st
from openai import OpenAI
import base64
import io
import asyncio
from websockets.asyncio.server import serve
from websockets import connect
from langchain_openai import ChatOpenAI


async def echo(websocket):
    async for base64_string in websocket:
        binary_data = base64.b64decode(base64_string)

        await websocket.send("received")


async def main():
    async with serve(echo, "ws://localhost:8765") as server:
        await server.serve_forever()
