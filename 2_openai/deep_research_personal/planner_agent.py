from pydantic import BaseModel, Field
from agents import Agent
from typing import List

HOW_MANY_SEARCHES = 1

INSTRUCTIONS = f"You are a helpful research assistant. Given a query, come up with a set of web searches \
to perform to best answer the query. Only Output {HOW_MANY_SEARCHES} terms to query for."

class WebSearchItem(BaseModel):
    reason: str = Field(description="The reasoning for why this search is important to the query")

    query: str = Field(description="The search query to perform")

class WebSearchList(BaseModel):
    searches: List[WebSearchItem] = Field(description="A list of web searches to perform")


planner_agent = Agent(
    name="Web Search Planner",
    instructions=INSTRUCTIONS,
    model = 'gpt-4o-mini',
    output_type=WebSearchList
)