from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class EnhancedEngineeringTeam():
    """EngineeringTeamPersonal crew"""

    agents_config: 'config/agents.yaml'
    tasks_config: 'config/tasks.yaml'

    @agent
    def business_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['business_analyst'], # type: ignore[index]
            verbose=True
        )
    
    @agent
    def engineering_lead(self) -> Agent:
        return Agent(
            config=self.agents_config['engineering_lead'], # type: ignore[index]
            verbose=True
        )


    @agent
    def database_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['database_engineer'], # type: ignore[index]
            allow_code_execution=True,
            code_execution_timeout=500,
            code_execution_mode='safe',
            max_retries=5,
            verbose=True
        )
    
    @agent
    def backend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['backend_engineer'], # type: ignore[index]
            verbose=True,
            allow_code_execution=True,
            code_execution_timeout=500,
            code_execution_mode='safe',
            max_retries=5
        )
    
    @agent
    def frontend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['frontend_engineer'], # type: ignore[index]
            verbose=True
        )
    
    @agent
    def test_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['test_engineer'], # type: ignore[index]
            verbose=True,
            allow_code_execution=True,
            code_execution_timeout=500,
            code_execution_mode='safe',
            max_retries=5
        )
    
    @agent
    def human_interface_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['human_interface_agent'], # type: ignore[index]
            verbose=True
        )

    @agent
    def demo_builder(self) -> Agent:
        return Agent(
            config=self.agents_config['demo_builder'], # type: ignore[index],
            allow_code_execution=True,
            code_execution_timeout=500,
            code_execution_mode='safe',
            max_retries=5,
            verbose=True
        )
    
    @agent
    def integration_coordinator(self) -> Agent:
        return Agent(
            config=self.agents_config['integration_coordinator'], # type: ignore[index]
            verbose=True
        )
    
    @agent
    def quality_gate_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['quality_gate_agent'], # type: ignore[index]
            verbose=True
        )


    @task
    def requirement_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['requirement_analysis_task'], # type: ignore[index]
        )
    
    @task
    def requirements_review_checkpoint(self) -> Task:
        return Task(
            config=self.tasks_config['requirements_review_checkpoint'],
        )
       
    @task
    def design_task(self) -> Task:
        return Task(
            config=self.tasks_config['design_task'], # type: ignore[index]
        )
    @task
    def design_review_checkpoint(self) -> Task:
        return Task(
            config=self.tasks_config['design_review_checkpoint'],
        )

  
    @task
    def database_design_task(self) -> Task:
        return Task(
            config=self.tasks_config['database_design_task'], # type: ignore[index]
        )

    @task
    def code_task(self) -> Task:
        return Task(
            config=self.tasks_config['code_task'], # type: ignore[index]
        )

    @task
    def frontend_task(self) -> Task:
        return Task(
            config=self.tasks_config['frontend_task'], # type: ignore[index]
        )
    
    @task
    def testing_task(self) -> Task:
        return Task(
            config=self.tasks_config['testing_task'], # type: ignore[index]
        )

    @task
    def human_review_preperation_task(self) -> Task:
        return Task(
            config=self.tasks_config['human_review_preperation_task'], # type: ignore[index]
        )

    @task
    def integration_demo_task(self) -> Task:
        return Task(
            config=self.tasks_config['integration_demo_task'], # type: ignore[index]
        )
    @task
    def feature_review_checkpoint(self) -> Task:
        return Task(
            config=self.tasks_config['feature_review_checkpoint'],
        ) 
        
    @task
    def integration_coordination_task(self) -> Task:
        return Task(
            config=self.tasks_config['integration_coordination_task'], # type: ignore[index]
        )
    
    @task
    def feedback_implementation_task(self) -> Task:
        return Task(
            config=self.tasks_config['feedback_implementation_task'], # type: ignore[index]
        )
    
    @task
    def quality_validation_task(self) -> Task:
        return Task(
            config=self.tasks_config['quality_validation_task'], # type: ignore[index]
        )
    



    @crew
    def crew(self) -> Crew:
        """Creates the EngineeringTeamPersonal crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
