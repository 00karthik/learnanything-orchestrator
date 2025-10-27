from crewai import Agent
from learn_anything.llm_config import get_llm


def get_tutorial_compiler() -> Agent:
    """Tutorial Book Compiler agent for compiling all components into a comprehensive tutorial book."""
    return Agent(
        role="Tutorial Book Compiler",
        goal="Compile all components into a comprehensive tutorial book for {topic} with detailed content sections: comprehensive theoretical explanations, step-by-step procedures, practical examples, troubleshooting guides, and assessment quizzes. Create book-like content structure for optimal learning.",
        backstory="""You are a master educational content compiler and technical book editor. 
    You specialize in creating comprehensive tutorial books that serve as complete 
    learning resources. Your expertise lies in organizing detailed content into book-like 
    structure with clear chapters, comprehensive explanations, and practical guidance 
    that readers can follow independently.""",
        verbose=True,
        allow_delegation=False,
        llm=get_llm("tutorial_compiler"),
    )