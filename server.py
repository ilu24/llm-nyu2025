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
        try:
            # Decode the base64-encoded string
            binary_data = base64.b64decode(base64_string)
            print("Received binary data")

            # Send back a simple response
            await websocket.send("received")
        except Exception as e:
            await websocket.send(f"Error: {str(e)}")

async def main():
    async with serve(echo, "localhost", 8765):
        await asyncio.Future() 

# Run the WebSocket server
asyncio.run(main())