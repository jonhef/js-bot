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
},
{
    "type": "function",
    "name": "send_message",
    "description": "Sends a message to the user(to your boss if username is not specified)",
    "parameters": {
        "type": "object",
        "properties": {
            "username": {
                "type": "string",
                "description": "Who should get the message"
            },
            "message": {
                "type": "string",
                "description": "The message to send"
            }
        },
        "required": [
            "message"
        ]
    }
},
{
    "type": "function",
    "name": "get_events",
    "description": "Get upcoming events from calendar",
    "parameters": {
        "type": "object",
        "properties": {
            "max_results": {
                "type": "integer",
                "description": "The maximum number of events to return"
            }
        },
        "required": []
    }
},
{
    "type": "function",
    "name": "add_event",
    "description": "Add event to calendar",
    "parameters": {
        "type": "object",
        "properties": {
            "summary": {
                "type": "string",
                "description": "The name of the event"
            },
            "description": {
                "type": "string",
                "description": "The description of the event"
            },
            "start": {
                "type": "object",
                "properties": {
                    "dateTime": {
                        "type": "string",
                        "description": "The date and timeof the event, format: YYYY-MM-DDTHH:MM:SS-00:00"
                    },
                    "timeZone": {
                        "type": "string",
                        "description": "Preferably Europe/Moscow"
                    }
                },
            },
            "end": {
                "type": "object",
                "properties": {
                    "dateTime": {
                        "type": "string",
                        "description": "The date and timeof the event, format: YYYY-MM-DDTHH:MM:SS-00:00"
                    },
                    "timeZone": {
                        "type": "string",
                        "description": "Preferably Europe/Moscow"
                    }
                },
            },
        },
        "required": [
            "summary", "description", "start", "end"
        ]
    }
},
{
    "type": "function",
    "name": "delete_event",
    "description": "Deletes an event from the calendar",
    "parameters": {
        "type": "object",
        "properties": {
            "event_id": {
                "type": "string",
                "description": "The id of the event to delete"
            }
        },
        "required": [
            "event_id"
        ]
    }
},
{
    "type": "function",
    "name": "send_email",
    "description": "Sends an email to the user",
    "parameters": {
        "type": "object",
        "properties": {
            "to": {
                "type": "string",
                "description": "The email address of the recipient"
            },
            "subject": {
                "type": "string",
                "description": "The subject of the email"
            },
            "text": {
                "type": "string",
                "description": "The text of the email"
            }
        },
        "required": [
            "to", "subject", "text"
        ]
    }
},
{
    "type": "function",
    "name": "get_date",
    "description": "Get current date",
    "parameters": {
        "type": "object",
        "properties": {
            "format": {
                "type": "string",
                "description": "The format of the date"
            }
        },
        "required": [
            "format"
        ]
    }
},
{
    "type": "function",
    "name": "get_weather",
    "description": "Get current temperature for provided coordinates in celsius.",
    "parameters": {
        "type": "object",
        "properties": {
            "latitude": {"type": "number"},
            "longitude": {"type": "number"}
        },
        "required": ["latitude", "longitude"],
        "additionalProperties": False
    },
    "strict": True
}]

other_tools = [{
    "type": "function",
    "name": "send_message_boss",
    "description": "Sends a message to your boss",
    "parameters": {
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": "The message to send"
            }
        },
        "required": [
            "message"
        ]
    }
},
{
    "type": "function",
    "name": "get_date",
    "description": "Get current date",
    "parameters": {
        "type": "object",
        "properties": {
            "format": {
                "type": "string",
                "description": "The format of the date"
            }
        },
        "required": [
            "format"
        ]
    }
},
{
    "type": "function",
    "name": "get_weather",
    "description": "Get current temperature for provided coordinates in celsius.",
    "parameters": {
        "type": "object",
        "properties": {
            "latitude": {"type": "number"},
            "longitude": {"type": "number"}
        },
        "required": ["latitude", "longitude"],
        "additionalProperties": False
    },
    "strict": True
},
{
    "type": "function",
    "name": "block_user",
    "description": "Block user in telegram",
    "parameters": {
        "type": "object",
        "properties": {
            "username": {
                "type": "string",
                "description": "The username or chat id of the user to block"
            }
        },
        "required": [
            "username"
        ]
    }
}]

from . import settings

system_prompt = f"""You are a helpful assistant, your name is Otto von Bismark, you're a man. You will be asked in russian, english and might be german.
Name of your boss is {settings.NAME}. Your boss is living in Moscow.
Your job is to write new events in your boss' schedule and to convey important information to your boss.
You are talking with people in telegram
Rules:
You mustn't use emoji
You must be polite
You mustn't say that you are an AI
You are able to say that you are secretary
You must use literature language, but laconically
You musn't include any technical information in your answers(like date)
You must ask your boss before make a deal with someone about something
When you add something in the schedule, you need to memorize data about user who wants to talk with your boss

Instructions:
When you are trying to delete the event you need to find the id of the event first and then delete it. You will get it if you get events.
As usual your boss has got 20 events a day(you need this information only for get events)
You must memorize the names and its data(for example: if your boss asks you to send a message to my friend, you should ask only the first time what's the username or email)
You should use markdown where it is possible
If someone is eager to book a conversation with your boss, you ask your boss first(and also, you need to memorize all important information about them), to ask your boss use send_message_boss.
When someone booked a conversation with your boss and I confirmed it, you need to memorize it
When someone is asking about booking, you need to check it in your memory
To get today's date you should use the function get_date(format), format is a string that used in Python datetime
When your boss asks you to plan something in the day after today you need to add one day to the date
You shouldn't add double events(or more)
You need to check for doubling events, because sometimes it happens that you add double events. If it happened, you need to remove doubled event
If someone asks to do something you need to send a message to your boss
When someone asks to do something you need to memorize their username/chat id
If someone is too rude you may block them(but send a notification to your boss)
If you get a message from channel you need to summarize information and send it to your boss
You mustn't double your messages(for example about blocking someone)
When you send messages you need to memorize that you sent it, and when you want to send a message you need to check if you have already sent it
When you are asked to check schedule by your boss you need to check it using get_events
When you block someone you need to memorize it, and if you are eager to block someone you need to check if you have already blocked them. You should just send them the empty message"""

import aiosqlite

import logging

logger = logging.getLogger(__name__)

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
            logger.info(rows)
            return rows
        

async def send_message(username, message = None):
    from . import client, settings
    if message is None:
        message = username
    await client.send_message(settings.USER_ID if message == username else username, message)
    
from ..services.calendar import add_event, get_events, delete_event
from ..services.email import send_email

async def send_message_boss(message):
    from . import client, settings
    logger.info(message)
    await client.send_message(settings.USER_ID, message)
    
async def get_date(format):
    from datetime import datetime
    logger.info(format)
    return datetime.now().strftime(format)

import httpx

async def get_weather(latitude, longitude):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")
        data = response.json()
        logger.info(data)
        return data['current']['temperature_2m']
    
async def block_user(username):
    from . import client, settings
    if username.startswith("@"):
        username = username[1:]
    await client.block_user(username)
    logger.info(f"User {username} blocked")
            
functions = {
    "write_memory": write_memory,
    "read_memory": read_memory,
    "send_message": send_message,
    "add_event": add_event,
    "get_events": get_events,
    "delete_event": delete_event,
    "send_email": send_email,
    "send_message_boss": send_message_boss,
    "get_date": get_date,
    "get_weather": get_weather,
    "block_user": block_user
}