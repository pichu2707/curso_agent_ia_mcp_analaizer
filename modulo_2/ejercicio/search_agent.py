from agents import Agent, WebSearchTool, ModelSettings

INSTRUCTIONS = """Eres un asistente de investigación. Dado un término de búsqueda, realiza una consulta web sobre ese término y produce un resumen conciso de los resultados encontrados. El resumen debe contener únicamente los puntos clave más relevantes, distribuidos en 2 a 3 párrafos, con un máximo de 300 palabras.

Escribe de forma directa y condensada, sin adornos, explicaciones innecesarias ni frases completas si no aportan claridad. No es necesario respetar la gramática o redacción formal: lo importante es capturar la esencia de la información de forma útil y rápida.

No incluyas ningún comentario adicional fuera del resumen."""

search_agent = Agent(
    name="Agente de búsqueda",
    instructions=INSTRUCTIONS,
    tools=[WebSearchTool(search_context_size="low")],
    model="gpt-4o-mini",
    model_settings=ModelSettings(tool_choice="required"), 
)