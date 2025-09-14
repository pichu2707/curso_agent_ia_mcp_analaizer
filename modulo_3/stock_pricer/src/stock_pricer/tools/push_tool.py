from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
import requests

class PushNotification(BaseModel):
    """
    Modelo para la notificación push.

    Args:
        BaseModel (_type_): _description_
    """
    title: str = Field(description="Título de la notificación")
    message: str = Field(description="Mensaje de la notificación")

class PushNotificationTool(BaseTool):
    """
    Herramienta para enviar notificaciones push utilizando Pushbullet.

    Args:
        BaseTool (_type_): _description_
    """
    name: str = "PushNotificationTool"
    description: str = "Envía una notificación push al usuario con un título y un mensaje."

    args_schemas: Type[BaseModel] = PushNotification

    def _run(self, title: str, message: str) -> str:
        """
        Envía una notificación push al usuario.

        Args:
            title (str): Título de la notificación.
            message (str): Mensaje de la notificación.

        Returns:
            str: Respuesta del servidor Pushbullet.
        """
        pushover_user = os.getenv("PUSHOVER_USER")
        pushover_token = os.getenv("PUSHOVER_TOKEN")
        pushover_url = "https://api.pushover.net/1/messages.json"

        print(f"Push: - {title} - \n{message}")
        payload = {"user": pushover_user, "token": pushover_token, "title": title, "message": message}
        requests.post(pushover_url, data=payload)
        return '{"notification": "sent"}'