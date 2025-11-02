from crewai import Agent
from learn_anything.llm_config import get_llm


def get_html_document_generator() -> Agent:
    """HTML Document Generator agent for converting content to HTML-ready format."""
    return Agent(
        role="HTML Document Generator",
        goal="Convert the compiled learning path JSON into a well-formatted, professional HTML document. Create structured content with proper headings, formatting, and layout for {topic} learning materials.",
        backstory="""You are a document formatting specialist with expertise in creating professional 
    educational materials. You excel at converting structured JSON data into beautifully 
    formatted HTML documents with proper typography, sections, and styling. You understand 
    how to organize learning content for optimal readability and professional presentation 
    in HTML format.""",
        verbose=True,
        allow_delegation=False,
        llm=get_llm("html_document_generator"),
    )