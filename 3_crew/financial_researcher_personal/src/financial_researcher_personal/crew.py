from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
# from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool
# from typing import List
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class FinancialResearcherPersonal():
    """FinancialResearcherPersonal crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools

    @agent
    def researcher(self) -> Agent:
        import os
        config = self.agents_config['researcher'].copy()  # Use .copy() to avoid mutating the original dict
        # Patch the api_key directly from env
        config['api_key'] = os.getenv("GOOGLE_API_KEY")
        print("DEBUG: API KEY at instantiation:", config['api_key'])  # For debug
        return Agent(config=config, verbose=True, tools=[SerperDevTool()])
    
    @agent
    def analyst(self) -> Agent:
        return Agent(config=self.agents_config['analyst'], verbose=True)

    @task
    def research_task(self) -> Task:
        return Task(config=self.tasks_config['research_task'])
    
    @task
    def analysis_task(self) -> Task:
        return Task(config=self.tasks_config['analysis_task'])
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents= self.agents,
            tasks= self.tasks,
            process= Process.sequential,
            verbose=True
        )
    
    