from openai.types.responses import Response
from base64 import b64encode
from pyrogram.types import Message
from pyrogram.enums import MessageMediaType
import logging

from config import openai

logger = logging.getLogger(__name__)

async def process_history(client, messages: list[Message]):
    result = []
    me = await client.get_me()
    for message in messages:
        if message.media is not None and type(message.media) == MessageMediaType.PHOTO:
            media = await client.download_media(message, file_name="media.jpg", in_memory=True)
            result.append({
                "role": "user",
                "content": [{
                    "type": "input_image",
                    "image_url": f"data:image/jpeg;base64,{b64encode(media).decode('utf-8')}"
                },
                {
                    "type": "input_text",
                    "text": message.text
                }]
            })
        else:
            result.append({
                "role": ("user" if message.from_user.id != me.id else "assistant"),
                "content": [{
                    "type": ("input_text" if message.from_user.id != me.id else "output_text"),
                    "text": message.text if message.text is not None else ""
                }]
            })
    
    result.reverse()
    logger.debug(result)
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
    logger.info(messages)
    return await openai.responses.create(
        model="gpt-4.1-nano-2025-04-14",
        input=messages,
        tools=tools
    )