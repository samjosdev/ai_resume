from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from pydantic import BaseModel, Field
from crewai_tools import SerperDevTool
from .tools.push_tool import PushNotificationTool
from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory
from crewai.memory.storage.rag_storage import RAGStorage
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage


class TrendingCompany(BaseModel):
    ''' A Company that is in the news and attracting attention'''
    name: str = Field(description="Company name")
    ticker: str = Field(description="Stock ticker symbol")
    reason: str = Field(description="Reason for the company being trending in the news")

class TrendingCompanyList(BaseModel):
    ''' A list of multiple trending companies that are in the news'''
    companies: List[TrendingCompany] = Field(description="List of companies trending in the news")

class TrendingCompaniesResearch(BaseModel):
    ''' Detailed research of each company'''
    name: str = Field(description="Company Name")
    market_position: str = Field(description="Market position and competitive analysis of the company")
    future_outlook: str = Field(description="Future Outlook and growth prospects")
    investement_potential: str = Field(description="Investement potential and sustainability for investment")

class TrendingCompaniesResearchList(BaseModel):
    ''' A list of detailed research for each company'''
    research_list: List[TrendingCompaniesResearch] = Field(description="Comphrensive research for all trending company")

@CrewBase
class StockPickerPersonal():
    """StockPickerPersonal crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def trending_company_finder(self) -> Agent:
        return Agent(config=self.agents_config['trending_company_finder'], tools=[SerperDevTool()], memory=True)

    @agent
    def financial_researcher(self) -> Agent:
        return Agent(config=self.agents_config['financial_researcher'], tools=[SerperDevTool()])
    
    @agent
    def stock_picker(self) -> Agent:
        return Agent(config=self.agents_config['stock_picker'], tools=[PushNotificationTool()], memory=True)
    
    @task
    def find_trending_companies(self) -> Task:
        return Task(
            config=self.tasks_config['find_trending_companies'], 
            output_pydantic=TrendingCompanyList)
    
    @task
    def research_trending_companies(self) -> Task:
        return Task(config=self.tasks_config['research_trending_companies'], 
                    output_pydantic=TrendingCompaniesResearchList)
    
    @task
    def pick_best_company(self) -> Task:
        return Task(
            config=self.tasks_config['pick_best_company'], 
        )
    @crew
    def crew(self) -> Crew:
        '''Create the StockPicker crew'''
        
        manager = Agent(
            config=self.agents_config['manager'],
            allow_delegation=True
        )
        
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            verbose=True,
            manager_agent=manager,
            memory=True,
            # Initialize memory
            short_term_memory = ShortTermMemory(
                    storage=RAGStorage(
                        embedder_config={
                            "provider": "openai",
                            "config": {"model": "text-embedding-3-small"}
                        },
                        type="short_term",
                        path="./memory/"
                    )
                ),
            long_term_memory = LongTermMemory(
                storage=LTMSQLiteStorage(db_path='./memory/long_term_memory.db')
            ),
            entity_memory = EntityMemory(
                storage = RAGStorage(
                    embedder_config={
                        "provider": "openai",
                        "config": {"model": "text-embedding-3-small"}
                    },
                    type="entity",
                    path="./memory/"
                )
            )
        )
        
        
