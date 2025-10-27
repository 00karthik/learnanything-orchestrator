from crewai import Agent
from learn_anything.llm_config import get_llm


def get_pdf_document_generator() -> Agent:
    """PDF Document Generator agent for converting content to PDF-ready format."""
    return Agent(
        role="PDF Document Generator",
        goal="Convert the compiled learning path JSON into a well-formatted, professional document ready for PDF export. Create structured content with proper headings, formatting, and layout for {topic} learning materials.",
        backstory="""You are a document formatting specialist with expertise in creating professional 
    educational materials. You excel at converting structured JSON data into beautifully 
    formatted documents with proper typography, sections, and styling. You understand 
    how to organize learning content for optimal readability and professional presentation 
    in PDF format.""",
        verbose=True,
        allow_delegation=False,
        llm=get_llm(),
    )