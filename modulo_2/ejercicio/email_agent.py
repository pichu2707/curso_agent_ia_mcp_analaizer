import os
from typing import Dict

import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from agents import Agent, function_tool

@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    """
    Envia un correo electrónico utilizando SendGrid.
    
    Args:
        subject (str): Asunto del correo.
        html_body (str): Cuerpo del correo en formato HTML.
    
    Returns:
        Dict[str, str]: Resultado de la operación de envío.
    """
    sg = sendgrid.SendGridAPIClient(api_key=os.getenv("SENDGRID_API_KEY"))
    from_email = Email("pichu_2707@hotmail.com")
    to_email = To("pichu2707@gmail.com")
    content = Content("text/html", html_body)
    mail = Mail(from_email, to_email, subject, content).get()
    response = sg.client.mail.send.post(request_body=mail)
    print("Respuesta de correo electrónico:", response.status_code)
    return {"status": "success", "message": "Correo enviado correctamente."}

INSTRUCTIONS = """Eres un agente encargado de preparar y enviar correos electrónicos formateados profesionalmente. Recibirás como entrada un informe detallado en formato Markdown generado por otro agente.

Tu tarea consiste en:

Convertir el informe en HTML limpio y bien estructurado, optimizado para ser visualizado correctamente en clientes de correo electrónico. El diseño debe ser claro, legible y profesional.

Generar una línea de asunto adecuada y relevante para el contenido del informe, breve pero informativa.

Preparar el cuerpo del correo en HTML incluyendo encabezados, párrafos, listas y cualquier sección relevante del informe. Si el informe contiene gráficos o visualizaciones, incorpora los enlaces o indicaciones para visualizarlos correctamente (por ejemplo, como imagen embebida o enlace externo si fuera necesario).

La salida debe incluir únicamente:

El asunto del email

El cuerpo en HTML del mensaje

No añadas comentarios adicionales ni instrucciones fuera del contenido del correo."""

email_agent = Agent(
    name="Agente de correo electrónico",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    tools=[send_email],
)