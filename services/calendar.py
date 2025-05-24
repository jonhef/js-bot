import datetime
import os.path
import asyncio

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from concurrent.futures import ThreadPoolExecutor

import logging

logger = logging.getLogger(__name__)

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

creds = None

if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

service = build("calendar", "v3", credentials=creds)

async def delete_event(event_id: str):
    loop = asyncio.get_event_loop()
    
    try:
        with ThreadPoolExecutor() as executor:
            logger.info("Try to delete an event")
            event = await loop.run_in_executor(
                executor,
                lambda: service.events().delete(
                    calendarId="primary",
                    eventId=event_id
                ).execute()
            )
            return event
    except Exception as e:
        logger.error(f"Ошибка при удалении события: {e}")
        raise

async def add_event(**kwargs):
    """Добавляет событие в календарь"""
    loop = asyncio.get_event_loop()
    
    try:
        with ThreadPoolExecutor() as executor:
            logger.info("Try to add an event")
            logger.info(kwargs)
            event = await loop.run_in_executor(
                executor,
                lambda: service.events().insert(
                    calendarId="primary",
                    body=kwargs
                ).execute()
            )
            return event
    except Exception as e:
        logger.error(f"Ошибка при добавлении события: {e}")
        raise


async def get_events(max_results: int = 1):
    now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
    loop = asyncio.get_event_loop()
    
    logger.info("Try to get events")
    
    with ThreadPoolExecutor() as executor:
        events_result = await loop.run_in_executor(
            executor,
            lambda: service.events().list(
                calendarId="primary",
                timeMin=now,
                maxResults=max_results,
                singleEvents=True,
                orderBy="startTime",
            ).execute()
        )
    
    return events_result.get("items", [])

if __name__ == "__main__":
    pass