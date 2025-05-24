from .settings import Settings

config = Settings()

from .ai_tools import tools, system_prompt, other_tools

from pyrogram import Client

from openai import AsyncOpenAI

import httpx

openai = AsyncOpenAI(api_key=config.OPENAI_API_KEY, http_client=httpx.AsyncClient(mounts={
    "https://": httpx.HTTPTransport(proxy=config.PROXY), 
    "http://": httpx.HTTPTransport(proxy=config.PROXY)
}))

client = Client(config.TELEGRAM_API_ID, api_hash=config.TELEGRAM_API_HASH, phone_number=config.PHONE_NUMBER)

import logging

logging.basicConfig(level=logging.INFO, format="[%(levelname)s]:%(asctime)s:%(name)s - %(message)s")

import sqlite3

with sqlite3.connect("memory.db") as conn:
    conn.execute("CREATE TABLE IF NOT EXISTS memory (memory TEXT, date TEXT)")