from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class Coder():
    """
    Crew Progamador
    """
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def coder(self) -> Agent:
        """
        Agente programador

        Returns:
            Agent: Agente programador
        """
        return Agent(
                    config=self.agents_config['coder'],
                    verbose=True,
                    allow_code_execution=True, # Permite la ejecución de código
                    code_execution_mode='safe', # Usa Docker para ejecutar el código de forma segura
                    max_execution_time=300,  # Tiempo máximo de ejecución en segundos
                    max_retry_limit=5
                    )

    @task
    def generate_code(self) -> Task:
        """
        Tarea que genera código a partir de una descripción en lenguaje natural.

        Returns:
            Task: Tarea que genera código a partir de una descripción en lenguaje natural.
        """
        return Task(
                    config=self.tasks_config['coding_task'],
                    )
    
    @crew
    def crew(self) -> Crew:
        """
        Crew que ejecuta el proceso de generación de código a partir de una descripción en lenguaje natural.

        Returns:
            Crew: Crew que ejecuta el proceso de generación de código a partir de una descripción en lenguaje natural.
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )