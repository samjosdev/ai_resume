from agents import Agent, WebSearchTool, ModelSettings, Runner, trace
import asyncio

INSTRUCTIONS = '''Given a search term, return ONLY 2 clarifying followup questions, one per line,
    to help refine the search. Do NOT include any introduction, explanation, or preamble.
    Only output the questions.'''

followup_questions_agent = Agent(
    name="followup questions Agent",
    instructions=INSTRUCTIONS,
    model = 'gpt-4o-mini',
)

# async def main():
#     # test the agent
#     message = "Why do Christians believe Jesus is God?"

#     with trace("test followup questions"):
#         result = await Runner.run(search_agent, message)
#         print(result.final_output)

# if __name__ == "__main__":
#     asyncio.run(main())
