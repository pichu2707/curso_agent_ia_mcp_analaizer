from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class EngineeringTeam():
    """
    Clase que representa el equipo de ingeniería.
    """

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    @agent
    def engineering_lead(self) -> Agent:
        """
        Agente que actúa como líder del equipo de ingeniería.

        Returns:
            Agent: Agente que actúa como líder del equipo de ingeniería.
        """
        return Agent(config=self.agents_config['engineering_lead'],
                    memory=True
                    )
    
    @agent
    def backend_engineer(self) -> Agent:
        """
        Agente que actúa como ingeniero de backend.

        Returns:
            Agent: Agente que actúa como ingeniero de backend.
        """
        return Agent(
            config=self.agents_config['backend_engineer'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode='safe', # 'safe' Usa Docker para ejecutar el código de forma segura
            max_execution_time=300,
            max_retry_limit=5
                    )
    @agent
    def frontend_engineer(self) -> Agent:
        """
        Agente que actúa como ingeniero de frontend.

        Returns:
            Agent: Agente que actúa como ingeniero de frontend.
        """
        return Agent(
            config=self.agents_config['frontend_engineer'],
            verbose=True
        )
    
    @agent
    def test_engineer(self) -> Agent:
        """
        Agente que actúa como ingeniero de pruebas.

        Returns:
            Agent: Agente que actúa como ingeniero de pruebas.
        """
        return Agent(
            config=self.agents_config['test_engineer'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode='safe', # 'safe' Usa Docker para ejecutar el código de forma segura
            max_execution_time=300,
            max_retry_limit=5
        )
    
    @task
    def design_task(self) -> Task:
        """
        Tarea de diseño.

        Returns:
            Task: Tarea de diseño.
        """
        return Task(config=self.tasks_config['design_task'])

    @task
    def code_task(self) -> Task:
        """
        Tarea de codificación.

        Returns:
            Task: Tarea de codificación.
        """
        return Task(config=self.tasks_config['code_task'])
    
    @task
    def frontend_task(self) -> Task:
        """
        Tarea de frontend.

        Returns:
            Task: Tarea de frontend.
        """
        return Task(config=self.tasks_config['frontend_task'])
    
    @task
    def test_task(self) -> Task:
        """
        Tarea de pruebas.

        Returns:
            Task: Tarea de pruebas.
        """
        return Task(config=self.tasks_config['test_task'])
    

    @crew
    def crew(self) -> Crew:
        """
        Crew que representa el equipo de ingeniería.

        Returns:
            Crew: Crew que representa el equipo de ingeniería.
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )