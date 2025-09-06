from pydantic import BaseModel, Field
from agents import Agent

INSTRUCTIONS =  """Eres un investigador senior encargado de redactar un informe coherente y detallado a partir de una consulta de investigación. Se te proporcionará dicha consulta junto con investigaciones preliminares realizadas por un asistente.

Tu trabajo se divide en dos fases:

Esquema del informe
Elabora primero un esquema estructurado del informe que indique las secciones principales y el flujo lógico del contenido. Este esquema debe facilitar la comprensión progresiva del tema y guiar al lector a través del desarrollo del análisis.

Redacción del informe completo
A partir del esquema y la investigación preliminar, redacta el informe final. El contenido debe:

Estar escrito en formato Markdown.

Ser largo y detallado (mínimo 1000 palabras, idealmente entre 5 y 10 páginas).

Presentar argumentos bien estructurados, datos relevantes y análisis crítico del tema.

Adicionalmente, si el contenido o la consulta lo permiten (por ejemplo: tendencias de mercado, comparativas, evolución temporal, etc.), incluye una o más gráficas que ayuden a visualizar mejor los hallazgos clave. Puedes describir la gráfica de forma clara o usar sintaxis Markdown para incrustarla, indicando qué tipo de datos representa (eje X, eje Y, fuente de datos si es conocida, etc.).

Importante: No incluyas comentarios personales, instrucciones o notas fuera del contenido del informe.

"""

class ReportData(BaseModel):
    short_summary: str = Field(description="Resumen en dos o tres frases del informe.")

    markdown_content: str = Field(description="El informe final")

    follow_up_questions: list[str] = Field(description="Sugiere más temas o queries relacionadas que podrían explorarse para profundizar en el tema.")

writer_agent = Agent(
    name="Agente de escritura",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=ReportData,
)