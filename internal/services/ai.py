from openai.types.responses import Response
from base64 import b64encode
from pyrogram.types import Message
from pyrogram import Client
from pyrogram.enums import MessageMediaType
import logging

from ..config import openai

logger = logging.getLogger(__name__)

cached_history = {}

async def process_history(client: Client, messages: list[Message]):
    result = []
    me = await client.get_me()
    for message in messages:
        if message.photo is not None:
            logger.info(message.photo.thumbs)
            thumbnail = message.photo.thumbs
            try:
                thumbnail = thumbnail[0]
            except Exception as e:
                logger.error(e)
            
            if thumbnail is not None:
                media = await client.download_media(thumbnail.file_id, file_name="thumbnail.jpg", in_memory=True)
            else:
                media = await client.download_media(message.photo.file_id, file_name="media.jpg", in_memory=True)
            
            logger.info(f"Media downloaded: {media}")
            url = f"data:image/jpeg;base64,{b64encode(bytes(media.getbuffer())).decode('utf-8')}"
            result.append({
                "role": "user",
                "content": [{
                    "type": "input_image",
                    "image_url": url
                },
                {
                    "type": "input_text",
                    "text": f"{message.text}\nTechnical info:\n\tDate:{message.date}\n\tFrom:{message.from_user.first_name} {message.from_user.last_name}\n\tChat/username: {message.chat.id}" if message.text is not None else "Technical info:\n\tDate:{message.date}\n\tFrom:{message.from_user.first_name} {message.from_user.last_name}\n\tChat/username: {message.chat.id}"
                }]
            })
        else:
            result.append({
                "role": ("user" if message.from_user.id != me.id else "assistant"),
                "content": [{
                    "type": ("input_text" if message.from_user.id != me.id else "output_text"),
                    "text": f"{message.text}\nTechnical info:\n\tDate:{message.date}\n\tFrom:{message.from_user.first_name} {message.from_user.last_name}\n\tChat/username: {message.chat.id}" if message.text is not None else "Technical info:\n\tDate:{message.date}\n\tFrom:{message.from_user.first_name} {message.from_user.last_name}\n\tChat/username: {message.chat.id}"
                }]
            })
    
    result.reverse()
    logger.debug(result)
    logger.info("History processed")
    return result

async def make_completion(client, tools: list, system_prompt: str, history: list[Message], call_id: str = None, output: str = None, lastoutput = None):
    messages = [{
        "role": "developer",
        "content": system_prompt
    }]
    messages.extend(await process_history(client, history))
    if call_id is not None and output is not None and lastoutput is not None:
        messages.append(lastoutput)
        messages.append({
            "type": "function_call_output",
            "call_id": call_id,
            "output": output
        })
    logger.info("Completion created")
    return await openai.responses.create(
        model="gpt-4.1-mini-2025-04-14",
        input=messages,
        tools=tools
    )