from agent import myAgent
import chainlit as cl

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="Welcome to the Multi Agent System! How can I assist you today?").send()

@cl.on_message
async def on_message(message: cl.Message):
    response = await myAgent(message.content)
    await cl.Message(content=response).send()
