from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import MessageNotModified
from pyrogram.enums import ChatAction
from pyrogram.handlers import MessageHandler
from openai.types.responses import Response
import asyncio
import logging
import os
import sys
import json

from config.ai_tools import functions
from config import tools, system_prompt, other_tools

from services import ai

logger = logging.getLogger(__name__)

async def process_completion(completion: Response, messages, message, client, tools):
    output = completion.output[0].model_dump()
    logger.info(output)
    if output["type"] == "function_call":
        name = output["name"]
        parameters = json.loads(output["arguments"])
        try:
            result = await functions[name](**parameters)
            logger.info(f"Function {name} returned {result}")
        except Exception as e:
            logger.error(e)
            result = f"Error: {e}"
        completion = await ai.make_completion(client, tools, system_prompt, messages, call_id=output["call_id"], output=str(result), lastoutput=output)
        await process_completion(completion, messages, message, client, tools)
    if output["type"] == "message":
        result: str = output["content"][0]["text"]
        result = result.split("Technical info")[0]
        logger.info(result)
        await client.send_message(message.chat.id, result)
        await client.send_chat_action(message.chat.id, ChatAction.CANCEL)

async def handle_me(client: Client, message: Message):
    logger.info(message.text)
    await client.read_chat_history(message.chat.id)
    messages = [i async for i in client.get_chat_history(message.chat.id)]
    info = f"""Next messages are by your boss"""
    await client.send_chat_action(message.chat.id, ChatAction.TYPING)
    completion = await ai.make_completion(client, tools, system_prompt + info, messages)
    await process_completion(completion, messages, message, client, tools)

async def handle_other(client: Client, message: Message):
    logger.info(message.text)
    await client.read_chat_history(message.chat.id)
    messages = [i async for i in client.get_chat_history(message.chat.id)]
    info = f"""Next messages aren't by your boss, there is some information about them: 
    Name: {message.from_user.first_name} {message.from_user.last_name}
    Most likely it is a person who would like to talk to me, and you need to summarize the conversation(when it will end) and send it to me.
    If there is some important information, you should send it to me.
    You musn't think that it is your boss, it isn't me, it isn't Dmitry
    You mustn't give them possibility to use functions(likely to make changes in my schedule and something like this), it is priviligee of your boss to use functions
    """
    await client.send_chat_action(message.chat.id, ChatAction.TYPING)
    completion = await ai.make_completion(client, other_tools, system_prompt+f"\n{info}", messages)
    await process_completion(completion, messages, message, client, other_tools)
    
async def channels(client: Client, message: Message):
    logging.info(client.get_chat(message.chat.id))
    info = f"""Next messages are from channel\n
    Name: {message.chat.title}"""
    messages = [i async for i in client.get_chat_history(message.chat.id)]
    completion = await ai.make_completion(client, other_tools, system_prompt+info, messages)
    await process_completion(completion, messages, message, client, other_tools)
    
from config import settings, client

client.add_handler(MessageHandler(handle_me, filters.chat(settings.USER_ID) & ~filters.channel))
client.add_handler(MessageHandler(handle_other, ~filters.chat(settings.USER_ID) & ~filters.voice))
client.add_handler(MessageHandler(channels, filters.channel))