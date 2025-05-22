import asyncio
from pyrogram import filters
from pyrogram.handlers import MessageHandler
import logging

from config import client, settings
from handlers.telegram import handle_me, handle_other

logger = logging.getLogger(__name__)

async def main():
    await client.start()
    logger.info("Sekretarin successfully started")
    while True:
        await asyncio.sleep(1)   
        
client.add_handler(MessageHandler(handle_me, filters.chat(settings.USER_ID)))
client.add_handler(MessageHandler(handle_other, ~filters.chat(settings.USER_ID)))
        
if __name__ == "__main__":
    client.run(main())