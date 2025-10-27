from crewai import Agent
from learn_anything.llm_config import get_llm


def get_structure_analyzer() -> Agent:
    """Book Structure Analyzer agent for determining optimal book chapter structure."""
    return Agent(
        role="Book Structure Analyzer",
        goal="Analyze {topic} for {skill_level} learners to determine optimal book chapter structure. Define exactly how many chapters are needed, what each should cover, and optimal sequencing for a comprehensive tutorial book based on {cost_optimization} requirements.",
        backstory="""You are a book architecture specialist with expertise in technical and 
    educational book design. You excel at breaking down complex topics into logical 
    book chapters, determining the right depth and progression for different skill 
    levels, and creating efficient content distribution plans that maximize parallel 
    processing while maintaining clear book structure.""",
        verbose=True,
        allow_delegation=False,
        llm=get_llm(),
    )