import gradio as gr
from dotenv import load_dotenv
from research_manager import ResearchManager

load_dotenv(override=True)

async def run(query: str):
    """Ejecuta el proceso de investigación y devuelve el informe final."""
    async for chunk in ResearchManager().run(query):
        yield chunk

with gr.Blocks(theme=gr.themes.Citrus(primary_hue="blue")) as ui:
    gr.Markdown("# Agente de Investigación Profunda")
    gr.Markdown("Este agente realiza una investigación profunda sobre un tema, generando un informe detallado y enviándolo por correo electrónico.")
    query_input = gr.Textbox(label="Consulta de Investigación", placeholder="Escribe aquí tu consulta...")
    run_button = gr.Button("Iniciar Investigación")
    report = gr.Markdown(label="Informe Final")
    
    
    run_button.click(run, inputs=query_input, outputs=report)
    query_input.submit(fn=run, inputs=query_input, outputs=report)

ui.launch(inbrowser=True)