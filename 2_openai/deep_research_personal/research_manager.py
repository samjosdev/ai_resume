
from agents import trace, Runner
from planner_agent import planner_agent, WebSearchList, WebSearchItem
from search_agent import search_agent
from writer_agent import writer_agent, ReportData
from email_agent import email_agent
from followup_questions import followup_questions_agent
from agents import gen_trace_id
import asyncio
from typing import List


class ResearchManager:
    # ---------- ASK THE LLM FOR CLARIFYING QUESTIONS -----------------

    async def generate_followup_questions(self, query: str) -> List[str]:
        '''Returns a list of strings (1 line per question)'''
        result = await Runner.run(followup_questions_agent, f'Query: {query}')
        text = getattr(result, "final_output", result)

        if isinstance(text, list):
            return text
        return [q.strip(" -*•") for q in str(text).splitlines() if q.strip()]        


    # ---------- WRAPPER THAT APPENDS USER ANSWERS --------------------
    async def run_with_clarifications(self, query:str, answers:[list[str]]):
        '''Concatenate the clarifications and call the normal .run().'''
        clarified = (
            query+ "\n\n" +"CLARIFICATIONS: \n" + "\n".join(f"- {a}" for a in answers))
        async for chunk in self.run(clarified):
            yield chunk

    # ---------- THE MAIN RUN METHOD -------------------------------
    async def run(self, query: str):
        ''' Run the deep research process, yielding the status updates and final report'''
        trace_id = gen_trace_id()
        with trace("Research Pipeline", trace_id = trace_id):
            print (f'View trace at https://platform.openai.com/traces/trace?trace_id={trace_id}')
            yield f'View trace at https://platform.openai.com/traces/trace?trace_id={trace_id}'
            print ("Generating Followup Questions")
            followup_questions = await self.generate_followup_questions(query)
            print ("Followup Questions Generated")
            yield "Followup Questions Generated"
            
            print ("Starting Research Pipeline")
            yield "Starting Research Pipeline"
            search_plan = await self.plan_searches(query)
            yield "Search Plan Generated"
            search_results = await self.perform_search(search_plan)
            yield "Search Results Generated"
            report = await self.write_report(query, search_results)
            yield "Report Generated"
            yield "Research complete"
            # Store the report object for later use
            self.last_report = report
            # Yield the actual markdown content
            yield f"REPORT_CONTENT:{report.markdown_report}"
            # print ("Research Pipeline Complete")

        
    async def plan_searches(self, query: str) -> WebSearchList:
        '''User planner agent to Plan which searches to run for the query'''
        print ("Planning searches...")
        result = await Runner.run(planner_agent, f'Query: {query}')
        print (f"Will perform {len(result.final_output.searches)} searches")
        return result.final_output_as(WebSearchList)

    async def perform_search(self, search_plan: WebSearchList) -> List[str]:
        '''Use the search agent to run a websearch for each item in the search plan'''
        print ("searching...")
        num_completed = 0
        tasks = [asyncio.create_task(self.search(item)) for item in search_plan.searches]
        results = []
        for task in asyncio.as_completed(tasks):
            result = await task
            if result is not None:
                results.append(result)
            num_completed += 1
            print (f"Completed {num_completed} of {len(tasks)} searches")
        print ("Finished Searching")
        return results

    async def search(self, item: WebSearchItem)-> str | None:
        '''Use the search agent to run a websearch for each item in the search plan'''
        print (f"Searching for {item.query}")
        input = f'Search term: {item.query} \n Reason for the search: {item.reason}'
        try:
            result = await Runner.run(search_agent, input)
            return result.final_output
        except Exception:
            return None




    
    async def write_report(self, query: str, search_results: List[str]) -> ReportData:
        '''Use the writer agent to write a report based on the search results'''
        print ("Thinking about the report...")
        input = f'Original Query: {query} \n Summarized Search Results: {search_results}'
        result = await Runner.run(writer_agent, input)
        print ("Finished Writing Report")
        return result.final_output_as(ReportData)
    

    async def send_report_with_email(self, report: ReportData, email: str) -> None:
        '''Use the email agent to send the report to the specified email address'''
        print (f"Writing Email to {email}...")
        message = f'Please send this report to {email}: \n\n {report.markdown_report}'
        result = await Runner.run(email_agent, message)
        print ("Email Sent")
        return report