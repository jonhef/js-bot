import asyncio
from pyrogram import filters
from pyrogram.handlers import MessageHandler
import logging

from .config import client, settings
from .handlers.telegram import handle_me, handle_other

logger = logging.getLogger(__name__)

async def main():
    try:
        await client.start()
        logger.warning("Secretary successfully started")
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info("Secretary stopped")
        exit(0)
        

        
if __name__ == "__main__":
    try:
        client.run(main())
    except KeyboardInterrupt:
        logger.warning("Secretary stopped")
        exit(0)