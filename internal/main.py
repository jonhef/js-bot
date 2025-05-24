import asyncio
from pyrogram import filters
from pyrogram.handlers import MessageHandler
import logging

from .config import client, settings
from .handlers.telegram import handle_me, handle_other

logger = logging.getLogger(__name__)

async def main():
    await client.start()
    logger.info("Secretary successfully started")
    while True:
        await asyncio.sleep(1)   
        

        
if __name__ == "__main__":
    client.run(main())