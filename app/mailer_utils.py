from re import TEMPLATE
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.email_utils import DefaultChecker
from app.schemas import EmailStr
from pathlib import Path
from .config import settings
from fastapi_mail.errors import ConnectionErrors

config = ConnectionConfig(
MAIL_USERNAME = settings.mail_user_name,
MAIL_PASSWORD = settings.mail_password,
MAIL_FROM= settings.mail_from,
MAIL_PORT = int(settings.mail_port),
MAIL_SERVER= settings.mail_server,
MAIL_STARTTLS=True,
MAIL_SSL_TLS=False,
TEMPLATE_FOLDER= Path(__file__).parent.parent/'templates/'
)

async def send_email_async(subject:str, email_to:EmailStr, body:dict, template:str):
    
    message = MessageSchema(
        subject=subject,
        recipients= [email_to,],
        template_body=body,
        subtype=MessageType.html
        )
    
    fm = FastMail(config)
    
    try:
        await fm.send_message(message, template_name=template)
        return True
    except ConnectionErrors as e:
        print(e)
    return False