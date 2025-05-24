import smtplib, ssl
from config import settings
from concurrent.futures import ThreadPoolExecutor
import asyncio
import logging

logger = logging.getLogger(__name__)

port = 465  # For SSL

# Create a secure SSL context
context = ssl.create_default_context()

async def send_email(to, subject, text):
    password = settings.PASSWORD
    mail = settings.EMAIL
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        logger.info("Try to send email")
        with smtplib.SMTP_SSL("smtp.mail.ru", port, context=context) as server:
            server.login(mail, password)
            logger.info("Sending email")
            await loop.run_in_executor(executor, lambda: server.sendmail(mail, to, f"Subject: {subject}\n\n{text}"))
            logger.info("Email sent")
    