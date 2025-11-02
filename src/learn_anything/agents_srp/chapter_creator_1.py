from crewai import Agent
from learn_anything.llm_config import get_llm


def get_chapter_creator_1() -> Agent:
    """Book Chapter Creator 1 agent for generating comprehensive tutorial book chapters."""
    return Agent(
        role="Book Chapter Creator 1",
    goal="Generate comprehensive tutorial book chapters for assigned sections of {topic}. Create detailed, self-contained book chapters including theoretical explanations, step-by-step procedures, practical examples, exercises, and assessments tailored to {skill_level} learners and the available study time of {time_commitment}.",
        backstory="""You are a specialized tutorial book author and educational content creator. 
    You excel at producing comprehensive book chapters that serve as complete guides 
    for learners. You understand how to create book content at different depth levels 
    based on optimization requirements, always ensuring readers have everything they 
    need to master their assigned chapters.""",
        verbose=True,
        allow_delegation=False,
        llm=get_llm("chapter_creator_1"),
    )