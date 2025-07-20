import json
import os
import requests
from dotenv import load_dotenv
from datetime import datetime, date

from openai import OpenAI

from pypdf import PdfReader
import gradio as gr

load_dotenv()

def push(text):
    """Envia un mensaje a través de Pushover."""
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "user": os.getenv("PUSHOVER_USER"),
            "token": os.getenv("PUSHOVER_TOKEN"),
            "message": text
        }
    )

def record_user_details(email, name="Nombre no indicado", notes="No proporcionadas"):
    """Registra los detalles del usuario."""
    push(f"Registarando {name} con el email {email} y notas: {notes}")
    return {"recorded": "ok"}

def record_unknown_question(question):
    """Registra una pregunta desconocida."""
    push(f"Pregunta desconocida: {question}")
    return {"recorded": "ok"}
    
record_user_details_json = {
    "name": "record_user_details",
    "description": "Registra los detalles del usuario, incluyendo su email, nombre y notas.",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "El email del usuario."
            },
            "name": {
                "type": "string",
                "description": "El nombre del usuario."
            },
            "notes": {
                "type": "string",
                "description": "Notas adicionales sobre el usuario."
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Registra una pregunta desconocida.",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "La pregunta que no se pudo responder."
            }
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

tools = [
    {
        "type": "function",
        "function": record_user_details_json
    },
    {
        "type": "function",
        "function": record_unknown_question_json
    }
]

class Me:

    def __init__(self):
        """Inicializa la clase Me con los detalles del usuario."""
        self.openai = OpenAI()
        self.name = "Javi Lazaro"
        reader = PdfReader("./perfil/Profile.pdf")
        self.linkedin = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.linkedin += text
        
        with open("./perfil/yoMismo.txt", "r", encoding='utf-8') as f:
            self.yomismo = f.read()

    def handle_tool_call(self, tool_calls):
        """Maneja las llamadas a herramientas."""
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"Herramienta llamada: {tool_name}", flush=True)
            tool = globals().get(tool_name)
            result = tool(**arguments) if tool else {}
            results.append({"role": "tool", "content": json.dumps(result), "tool_call_id": tool_call.id})
        return results
    
    def system_prompt(self):
        """Genera el prompt del sistema."""
        today = date.today()
        system_prompt =  f"""Actúas como {self.name}. Respondes preguntas en el sitio web de {self.name}, en particular preguntas relacionadas con la trayectoria profesional, los antecedentes, las habilidades y la experiencia de {self.name}.
            Tu responsabilidad es representar a {self.name} en las interacciones del sitio web con la mayor fidelidad posible.
            Se te proporciona un resumen de la trayectoria profesional y el perfil de LinkedIn de {self.name} que puedes usar para responder preguntas.
            Muestra un tono profesional y atractivo, como si hablaras con un cliente potencial o un futuro empleador que haya visitado el sitio web.
            Si no sabes la respuesta a alguna pregunta, usa la herramienta 'record_unknown_question' para registrar la pregunta que no pudiste responder, incluso si se trata de algo trivial o no relacionado con tu trayectoria profesional.
            Si el usuario participa en una conversación, intenta que se ponga en contacto por correo electrónico; pídele su correo electrónico y regístralo con la herramienta 'record_user_details'.
            Tienes que intetanr que a partir de la tercera pregunta, el usuario te proporcione su correo electrónico, y si no lo hace, debes recordárselo.
            La fecha actual es {today.strftime('%d/%m/%Y')}, algo que debes de tener en cuenta al responder preguntas relacionadas con fechas o eventos recientes.
            Si el usuario te pregunta por tu nombre, debes decir que te llamas {self.name} y que eres un profesional con experiencia en desarrollo de software, CRO, Analítica, SEO, programación, analítica y gestión de proyectos."""
        
        system_prompt += f"\n\n## Resumen:\n{self.yomismo}\n\n## Perfil de LinkedIn:\n{self.linkedin}\n\n"
        system_prompt += f"En este contexto, por favor chatea con el usuario, manteniéndote siempre en el personaje de {self.name}."
        return system_prompt
    
    def chat(self, message, history):
        messages = [
            {
                "role": "system",
                "content": self.system_prompt()
            }
        ] + history + [
            {
                "role": "user",
                "content": message
            }
        ]
        done = False
        while not done:
            response = self.openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=tools,
            )
            if response.choices[0].finish_reason == "tool_calls":
                message = response.choices[0].message
                tool_calls = message.tool_calls
                results = self.handle_tool_call(tool_calls)
                messages.append(message)
                messages.extend(results)
            else:
                done = True

        return response.choices[0].message.content
if __name__ == "__main__":
    me = Me()
    gr.ChatInterface(
        me.chat,
        type="messages"
    ).launch()
