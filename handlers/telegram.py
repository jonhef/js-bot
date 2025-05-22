from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import MessageNotModified
from pyrogram.handlers import MessageHandler
from openai.types.responses import Response
import asyncio
import logging
import os
import sys
import json

from config.ai_tools import functions
from config import tools, system_prompt

from services import ai

logger = logging.getLogger(__name__)

async def process_completion(completion: Response, messages, message, client):
    output = completion.output[0].model_dump()
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
        await process_completion(completion, messages, message, client)
    if output["type"] == "message":
        result = output["content"]
        logger.info(result)
        await client.send_message(message.chat.id, result[0]["text"])

async def handle_me(client: Client, message: Message):
    logger.info(message.text)
    messages = [i async for i in client.get_chat_history(message.chat.id)]
    completion = await ai.make_completion(client, tools, system_prompt, messages)
    await process_completion(completion, messages, message, client)

async def handle_other(client: Client, message: Message):
    logger.info(message.text)
    messages = [i async for i in client.get_chat_history(message.chat.id)]
    info = f"""It isn't me, there is some information about them: 
    Name: {message.from_user.first_name} {message.from_user.last_name}
    """
    completion = await ai.make_completion(client, tools, system_prompt+f"\n{info}", messages)
    await process_completion(completion, messages, message, client)