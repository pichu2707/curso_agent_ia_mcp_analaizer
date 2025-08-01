import asyncio

from writer_agent import writer_agent, ReportData
from email_agent import email_agent
from planner_agent import planner_agent, WebSearchItem, webSearchPlan

from agents import Runner, trace, gen_trace_id
from search_agent import search_agent

class ResearchManager:

    async def run(self, query: str):
        """Ejecuta el proceso de investigación profunda, generando las actualizaciones necesarias y enviando el informe final por correo electrónico."""
        trace_id = gen_trace_id()
        with trace("Investigacion", trace_id=trace_id):
            print(f"Ver traza: https://trace.agentic.ai/trace/{trace_id}")
            yield f"Ver traza: https://trace.agentic.ai/trace/{trace_id}"
            print("Iniciando el proceso de investigación...")
            yield "Iniciando el proceso de investigación..."
            # Paso 1: Planificación de la investigación
            print("Paso 1: Planificación de la investigación")
            yield "Paso 1: Planificación de la investigación"
            search_plan = await self.plan_searches(query)
            yield "Búsquedas completas, escibiendo el informe..."
            report = await self.write_report(query, search_plan)
            yield "Informe escrito, enviando por correo electrónico..."
            await self.send_email(report)
            yield "Correo electrónico enviado."
            yield report.markdown_content

    async def plan_searches(self, query: str) -> webSearchPlan:
        """Genera un plan de búsqueda basado en la consulta inicial."""
        print("planificando búsquedas...")
        result = await Runner.run(
            planner_agent,
            f"Consulta: {query}",
        )

        print(f"Se realizarán {len(result.final_output.searches)} búsquedas.")
        return result.final_output_as(webSearchPlan)
    
    async def perform_searches(self, search_plan: webSearchPlan) -> list[str]:
        """Realiza las búsquedas web según el plan generado."""
        print("Realizando búsquedas...")
        num_completed = 0
        tasks = [asyncio.create_task(self.search(item)) for item in search_plan.searches]
        results = []
        for task in asyncio.as_completed(tasks):
            result = await task
            if result is not None:
                results.append(result)
            num_completed += 1
            print(f"Búsquedas completadas: {num_completed}/{len(tasks)} completadas.")
        print("Todas las búsquedas completadas.")
        return results
        
    async def search(self, item: WebSearchItem) -> str | None:
        """Realiza una búsqueda para la consulta

        Args:
            item (WebSearchItem): Será el elemento de búsqueda que contiene la razón y la consulta.

        Returns:
            str | None: Nos devuelve una cadena con el resultado de la búsqueda o None si no se encontró información.
        """
        input = f"Término de búsqueda: {item.query}\nRazón: {item.reason}"
        try:
            result = await Runner.run(
                search_agent,
                input,
            )
            return str(result.final_output)
        except Exception:
            return None
        
    async def write_report(self, query: str, search_results: list[str]) -> ReportData:
        """Redacta un informe detallado basado en la consulta y los resultados de las búsquedas."""
        print("Escribiendo el informe...")
        input = f"Consulta: {query}\nBúsquedas realizadas:\n{search_results}"
        result = await Runner.run(
            writer_agent,
            input,
        )
        print("Informe redactado.")
        return result.final_output_as(ReportData)
    
    async def send_email(self, report: ReportData) -> None:
        """Envía el informe redactado por correo electrónico."""
        print("Enviando el correo electrónico...")
        result = await Runner.run(
            email_agent,
            report.markdown_content,
        )
        print("Correo electrónico enviado.")
        return report