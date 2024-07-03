import os
from dotenv import load_dotenv
from langchain.agents import Tool, load_tools
from crewai import Agent, Task, Process, Crew
from crewai_tools import WebsiteSearchTool, SerperDevTool
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_google_genai import ChatGoogleGenerativeAI

class WebpageSummarizerAI:
    def __init__(self, web_site: str = None):
        self.setup_environment()
        self.setup_tools(web_site)
        self.setup_agents()
        self.setup_tasks()
        self.setup_crew()

    def setup_environment(self):
        load_dotenv()
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            verbose=False, 
            temperature=0.5,
            google_api_key=os.getenv("GEMINI_API_KEY")
        )
        self.serper_api_key = os.getenv("SERPER_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

    def setup_tools(self, web_site: str):
        self.web_extractor = WebsiteSearchTool(website=web_site)
        self.serper_tool = SerperDevTool()

    def setup_agents(self):
        self.extractor = Agent(
            role="Content Extractor",
            goal="Extract and summarize the most useful information from a given webpage URL",
            backstory="""You are an expert at analyzing and extracting key information from any webpage. You know how to identify and summarize the most 
            relevant and useful content, ensuring that the summary is comprehensive and accurate.""",
            verbose=False,
            llm=self.llm,
            allow_delegation=False,
            tools=[self.web_extractor],
        )

        self.summarizer = Agent(
            role="Content Summarizer",
            goal="Provide a concise and useful summary of the extracted content from the webpage",
            backstory="""You are skilled at summarizing large amounts of information into concise, clear, and useful content. You know how to highlight 
            the most important points and present them in a way that is easy to understand for the user.""",
            verbose=False,
            llm=self.llm,
            allow_delegation=True,
        )

    def setup_tasks(self):
        self.task_extract = Task(
            description="""Extract content from the provided webpage URL and summarize the key points. The summary should be comprehensive and cover the main 
            topics and useful information presented on the page. Your final output should be a text summary that captures the essence of the webpage content.""",
            agent=self.extractor,
            expected_output="""A comprehensive summary covering the main topics and useful information from the webpage. The summary should be text-only and well-structured."""
        )

        self.task_summarize = Task(
            description="""Provide a detailed and concise summary of the extracted webpage content. Ensure that the summary is easy to understand and includes 
            the most important and useful information. The summary should be well-organized and present the key points clearly.""",
            agent=self.summarizer,
            expected_output="""A concise and well-organized summary that highlights the most important and useful information from the extracted content. The summary should be clear and easy to understand.""",
            output_file="summary.txt"
        )

    def setup_crew(self):
        self.crew = Crew(
            agents=[self.extractor, self.summarizer],
            tasks=[self.task_extract, self.task_summarize],
            verbose=0,
            process=Process.sequential,
        )

    def run(self, url):
        result = self.crew.kickoff()
        print("######################")
        print(result)

if __name__ == "__main__":
    url = input("Enter the webpage URL: ")
    webpage_summarizer_ai = WebpageSummarizerAI(url)
    webpage_summarizer_ai.run(url)
