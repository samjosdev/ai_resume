from playwright.async_api import async_playwright
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
from dotenv import load_dotenv
import os
import requests
from langchain.agents import Tool
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_experimental.tools import PythonREPLTool
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper

import re


pushover_token = os.getenv("PUSHOVER_TOKEN")
pushover_user = os.getenv("PUSHOVER_USER")
pushover_url = f"https://api.pushover.net/1/messages.json"
serper  = GoogleSerperAPIWrapper()

#Sanitize tool name to avoid errors
def sanitize_tool_name(tool):
    tool.name = re.sub(r"[^a-zA-Z0-9_-]", "_", tool.name)
    return tool

#Push Tool function
def push(text:str):
    """Send a push notification to the user"""
    requests.post(pushover_url, data={"token": pushover_token, "user": pushover_user, "message": text})
    return "success"

#Playwright Tools for UI access
async def playwright_tools():
    async_play = await async_playwright().start()
    # sync_play = sync_playwright().start()
    async_browser = await async_play.chromium.launch(headless=False)
    # sync_browser = sync_play.chromium.launch(headless=False)
    # playwright = await async_playwright().start()
    # browser = await playwright.chromium.launch(headless=False)
    # toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=browser)
    toolkit = PlayWrightBrowserToolkit( async_browser=async_browser)
    # return toolkit.get_tools(), sync_browser, async_browser
    tools = toolkit.get_tools()
    return [sanitize_tool_name(t) for t in tools], async_browser, async_play


#File Management Tools
def get_file_tools():
    """Get file management tools"""
    toolkit = FileManagementToolkit(root_dir="sandbox")
    return toolkit.get_tools()

async def other_tools():
    push_tool = Tool(name="Push Notification", func=push, description="Send a push notification to the user")
    file_tools = get_file_tools()
    tool_search = Tool(name="search",
                       func=serper.run,
                       description="Search the web for information")
    wikipedia = WikipediaAPIWrapper()
    wiki_tool = WikipediaQueryRun(api_wrapper=wikipedia)
    python_repl = PythonREPLTool()
    all_tools = file_tools + [push_tool, tool_search, wiki_tool, python_repl]
    return [sanitize_tool_name(t) for t in all_tools]



