tools = [{
    "type": "function",
    "name": "write_memory",
    "description": "Writes a memory to the database",
    "parameters": {
        "type": "object",
        "properties": {
            "memory": {
                "type": "string",
                "description": "The memory to write to the database"
            },
            "date": {
                "type": "string",
                "description": "The date of the memory"
            }
        },
        "required": [
            "memory", "date"
        ]
    }
},
{
    "type": "function",
    "name": "read_memory",
    "description": "Reads a memory from the database",
    "parameters": {
        "type": "object",
        "properties": {
            "date": {
                "type": "string",
                "description": "The date of the memory"
            }
        }
    },
    "required": []
}]




system_prompt = """You are a helpful assistant, your name is Sekretärin. You will be asked in russian, english and might be german.
My name is Dmitry, I am your boss.
Your job is to write new events in my schedule and to convey important information to me. 
Rules:
You mustn't use emoji
You must be polite
You mustn't say that you are an AI
You are able to say that you are my secretary"""

import aiosqlite

async def write_memory(memory, date):
    async with aiosqlite.connect("memory.db") as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("INSERT INTO memory (memory, date) VALUES (?, ?)", (memory, date))
            await conn.commit()
            
async def read_memory(date = None):
    async with aiosqlite.connect("memory.db") as conn:
        async with conn.cursor() as cursor:
            if date is None:
                await cursor.execute("SELECT * FROM memory")
            else:
                await cursor.execute("SELECT * FROM memory WHERE date = ?", (date,))
            rows = await cursor.fetchall()
            return rows
            
functions = {
    "write_memory": write_memory,
    "read_memory": read_memory
}