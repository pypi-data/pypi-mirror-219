from email.message import EmailMessage
from smtplib import SMTP
from typing import Final
import sys
from .env_pomes import APP_PREFIX, env_get_str, env_get_int

EMAIL_ACCOUNT: Final[str] = env_get_str(f"{APP_PREFIX}_EMAIL_ACCOUNT")
EMAIL_PWD: Final[str] = env_get_str(f"{APP_PREFIX}_EMAIL_PWD")
EMAIL_PORT: Final[int] = env_get_int(f"{APP_PREFIX}_EMAIL_PORT")
EMAIL_SERVER: Final[str] = env_get_str(f"{APP_PREFIX}_EMAIL_SERVER")


def email_send(errors: list[str], user_email: str, subject: str, content: str):

    # import needed function
    from .exception_pomes import exc_format

    # connstrói o email
    email_msg = EmailMessage()
    email_msg.set_content(content)
    email_msg["Subject"] = subject
    email_msg["From"] = EMAIL_ACCOUNT
    email_msg["To"] = user_email

    # instancia o email server
    server = SMTP(host=EMAIL_SERVER, port=EMAIL_PORT)
    server.starttls()
    server.login(user=EMAIL_ACCOUNT, password=EMAIL_PWD)

    # envia a mensagem
    try:
        server.send_message(email_msg)
        server.quit()
    except Exception as e:
        # a operação resultou em exceção
        errors.append(f"Erro no envio de email: {exc_format(e, sys.exc_info())}")
