from crewai import Task


def get_create_assigned_chapters_1_task() -> Task:
    """Task for creating assigned book chapters by Content Creator 1."""
    return Task(
        description="""Generate comprehensive tutorial book content for chapters assigned 
    to Content Creator 1 based on the book structure analysis for {topic}. Tailor the
    depth of coverage to suit {skill_level} learners who have {time_commitment} to invest.
    Create complete book chapters including:

**Book Chapter Components:**
1. **Chapter Introduction**: Overview of what will be covered and learning objectives
2. **Detailed Theoretical Explanations**: Complete concepts, principles, background knowledge, 
    and theory
3. **Step-by-Step Procedures**: Clear, actionable instructions and techniques with screenshots/diagrams where helpful
4. **Practical Examples and Case Studies**: Real-world applications, scenarios, and worked examples
5. **Hands-On Exercises**: Practice activities with detailed solutions and explanations
6. **Troubleshooting Guides**: Common problems, error messages, and solutions
7. **Best Practices and Expert Tips**: Professional insights, recommendations, and advanced techniques sized appropriately for the learner profile
8. **Chapter Summary**: Key takeaways and what was learned
9. **Chapter Quiz**: 5-10 questions with detailed answers and explanations

Research current information using available tools to ensure content accuracy and relevance. 
Work only on chapters specifically assigned to Creator 1 in the book structure plan.""",
        expected_output="""Complete comprehensive book chapters for specifically assigned 
    chapters with appropriate depth based on the learner skill level and available study time. Include detailed theoretical 
    content, step-by-step procedures, practical examples, exercises with solutions, 
    troubleshooting guides, and chapter assessments needed for readers to master the 
    material.""",
        agent=None,
    )