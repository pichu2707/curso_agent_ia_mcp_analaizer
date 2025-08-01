from pydantic import BaseModel, Field
from agents import Agent


HOW_MANY_SEARCHES = 5

INSTRUCTIONS = f"""Eres un agente de planificación de tareas de investigación. Dada una consulta o término inicial, genera un conjunto de frases o términos que puedan usarse como búsquedas web relevantes para recopilar la información necesaria y responder eficazmente a la consulta original. Asegúrate de cubrir distintos enfoques o subtemas útiles relacionados.

Devuelve exactamente {HOW_MANY_SEARCHES} consultas de búsqueda web."""

class WebSearchItem(BaseModel):
    reason: str = Field(description="Tu razonamiento de por qué esta b´suqeuda es importante ")
    query: str = Field(description="Consulta de búsqueda web generada por el agente de planificación.")

class webSearchPlan(BaseModel):
    searches: list[WebSearchItem] = Field(
        description="Lista de consultas de búsqueda web generadas por el agente de planificación."
    )

planner_agent = Agent(
    name="Agente de búsqueda",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=webSearchPlan,
)
