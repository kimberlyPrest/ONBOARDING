import os

from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
	FileReadTool
)
from upsell_navigator___deploy_ready.tools.report_data_formatter import ReportDataFormatterTool





@CrewBase
class UpsellNavigatorDeployReadyCrew:
    """UpsellNavigatorDeployReady crew"""

    
    @agent
    def data_ingestion_and_normalization_specialist(self) -> Agent:

        
        return Agent(
            config=self.agents_config["data_ingestion_and_normalization_specialist"],
            
            
            tools=[
				FileReadTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gemini/gemini-2.5-pro",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def chat_engagement_and_sentiment_analyst(self) -> Agent:

        
        return Agent(
            config=self.agents_config["chat_engagement_and_sentiment_analyst"],
            
            
            tools=[
				FileReadTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gemini/gemini-2.5-pro",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def performance_analytics_and_report_generator(self) -> Agent:

        
        return Agent(
            config=self.agents_config["performance_analytics_and_report_generator"],
            
            
            tools=[
				FileReadTool(),
				ReportDataFormatterTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gemini/gemini-2.5-pro",
                temperature=0.7,
            ),
            
        )
    

    
    @task
    def data_ingestion_and_normalization(self) -> Task:
        return Task(
            config=self.tasks_config["data_ingestion_and_normalization"],
            markdown=False,
            
            
        )
    
    @task
    def chat_engagement_and_sentiment_analysis(self) -> Task:
        return Task(
            config=self.tasks_config["chat_engagement_and_sentiment_analysis"],
            markdown=False,
            
            
        )
    
    @task
    def performance_analysis_and_report_generation(self) -> Task:
        return Task(
            config=self.tasks_config["performance_analysis_and_report_generation"],
            markdown=False,
            
            
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the UpsellNavigatorDeployReady crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )

    def _load_response_format(self, name):
        with open(os.path.join(self.base_directory, "config", f"{name}.json")) as f:
            json_schema = json.loads(f.read())

        return SchemaConverter.build(json_schema)
