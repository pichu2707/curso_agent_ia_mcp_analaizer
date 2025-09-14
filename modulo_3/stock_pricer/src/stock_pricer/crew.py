from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool # Hace búsquedas en Google
from pydantic import BaseModel, Field
from typing import List

from .tools.push_tool import PushNotificationTool

class TrendingCompany(BaseModel):
    """
    Modelo que representa una empresa en tendencia.

    Args:
        BaseModel (_type_): _description_
    """
    name: str = Field(description="Nombre de la empresa")
    ticker: str = Field(description="Ticker de la empresa")
    reason: str = Field(description="Razón por la que esta empresa está en tendencia")

class TrendingCompanyList(BaseModel):
    """
    Modelo que representa una lista de empresas en tendencia.

    Args:
        BaseModel (_type_): _description_
    """
    companies: List[TrendingCompany] = Field(description="Lista de empresas en tendencia")

class TrendingCompanyReserach(BaseModel):
    """
    Modelo que representa la investigación de una empresa en tendencia.

    Args:
        BaseModel (_type_): _description_
    """
    name: str = Field(..., description="Nombre de la empresa")
    market_position: str = Field(description="Posición en el mercado de la empresa")
    future_outlook: str = Field(description="Perspectiva de futuro y perspectiva de crecimiento de la empresa")
    investment_potentiial: str = Field(description="Potencial de inversión de la empresa")

@CrewBase
class StockPicker():
    """
    Clase para seleccionar acciones en función de la investigación de empresas en tendencia.
    """

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    @agent
    def trending_company_finder(self) -> Agent:
        """
        Agente que encuentra empresas en tendencia.

        Returns:
            Agent: Agente que encuentra empresas en tendencia.
        """
        return Agent(config=self.agents_config['trending_company_finder'], 
                    tools=[SerperDevTool()]
                    )
    
    @agent
    def financial_researcher(self) -> Agent:
        """
        Agente que realiza la investigación financiera de una empresa en tendencia.

        Returns:
            Agent: Agente que realiza la investigación financiera de una empresa en tendencia.
        """
        return Agent(config=self.agents_config['financial_researcher'], 
                    tools=[SerperDevTool()]
                    )
    
    @agent
    def stock_picker(self) -> Agent:
        """
        Agente que selecciona acciones en función de la investigación de empresas en tendencia.

        Returns:
            Agent: Agente que selecciona acciones en función de la investigación de empresas en tendencia.
        """
        return Agent(config=self.agents_config['stock_picker'],
                    tools=[PushNotificationTool()]
                    )
    
    @task
    def find_trending_companies(self) -> Task:
        """
        Tarea que encuentra empresas en tendencia.

        Returns:
            Task: Tarea que encuentra empresas en tendencia.
        """
        return Task(config=self.tasks_config['find_trending_companies'], 
                    output_pydantic=TrendingCompanyList,
                    )
    
    @task
    def research_trending_companies(self) -> Task:
        """
        Tarea que realiza la investigación financiera de una empresa en tendencia.

        Returns:
            Task: Tarea que realiza la investigación financiera de una empresa en tendencia.
        """
        return Task(config=self.tasks_config['research_trending_companies'], 
                    output_pydantic=TrendingCompanyReserach,
                    )
    
    @task
    def pick_best_company(self) -> Task:
        """_summary_

        Returns:
            Task: Seleccióna la mejor empresa en tendencia.
        """
        return Task(config=self.tasks_config['pick_best_company'])
    
    @crew
    def crew(self) -> Crew:
        """
        Crew que ejecuta el proceso de selección de acciones en función de la investigación de empresas en tendencia.

        Returns:
            Crew: Crew que ejecuta el proceso de selección de acciones en función de la investigación de empresas en tendencia.
        """
        manager = Agent(
            config=self.agents_config['manager'],
            allow_delegation=True,

        )

        return Crew(
            agents = self.agents,
            tasks = self.tasks,
            process=Process.hierarchical,
            verbose=True,
            manager_agent=manager
        )