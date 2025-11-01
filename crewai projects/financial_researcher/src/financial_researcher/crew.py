# src/financial_researcher/crew.py
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool

@CrewBase
class SPXTradingCrew():
    """SPX Trading crew with tech news, SPX weekly data, and Fed policy analysis"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def news_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['news_researcher'],
            verbose=True,
            tools=[SerperDevTool()]
        )

    @agent
    def spx_data_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['spx_data_analyst'],
            verbose=True,
            tools=[SerperDevTool()]
        )

    @agent
    def fed_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['fed_analyst'],
            verbose=True,
            tools=[SerperDevTool()]
        )

    @agent
    def risk_management_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['risk_management_analyst'],
            verbose=True,
            tools=[SerperDevTool()]
        )

    @agent
    def aggressive_trader(self) -> Agent:
        return Agent(
            config=self.agents_config['aggressive_trader'],
            verbose=True
        )

    @agent
    def cautious_trader(self) -> Agent:
        return Agent(
            config=self.agents_config['cautious_trader'],
            verbose=True
        )

    @agent
    def spx_trader(self) -> Agent:
        return Agent(
            config=self.agents_config['spx_trader'],
            verbose=True
        )

    @task
    def news_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['news_research_task']
        )

    @task
    def spx_weekly_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['spx_weekly_analysis_task']
        )

    @task
    def fed_policy_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['fed_policy_analysis_task']
        )

    @task
    def risk_management_task(self) -> Task:
        return Task(
            config=self.tasks_config['risk_management_task']
        )

    @task
    def aggressive_trader_task(self) -> Task:
        return Task(
            config=self.tasks_config['aggressive_trader_task']
        )

    @task
    def cautious_trader_task(self) -> Task:
        return Task(
            config=self.tasks_config['cautious_trader_task']
        )

    @task
    def spx_trading_decision_task(self) -> Task:
        return Task(
            config=self.tasks_config['spx_trading_decision_task']
        )

    @crew
    def crew(self) -> Crew:
        """Creates the SPX trading crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
