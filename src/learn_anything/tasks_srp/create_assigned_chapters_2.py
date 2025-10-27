from crewai import Task


def get_create_assigned_chapters_2_task() -> Task:
    """Task for creating assigned book chapters by Content Creator 2."""
    return Task(
        description="""Generate comprehensive tutorial book content for chapters assigned 
    to Content Creator 2 based on the book structure analysis for {topic}. Create 
    complete book chapters including:

**Content Creation Based on {cost_optimization}:**
- **AGGRESSIVE**: Core concepts with concise explanations, essential examples
- **BALANCED**: Thorough explanations with comprehensive examples and moderate depth   
- **QUALITY**: Detailed comprehensive content with multiple examples, deep 
    explanations, and extensive coverage

**Book Chapter Components:**
1. **Chapter Introduction**: Overview of what will be covered and learning objectives
2. **Detailed Theoretical Explanations**: Complete concepts, principles, background knowledge, 
    and theory
3. **Step-by-Step Procedures**: Clear, actionable instructions and techniques with screenshots/diagrams where helpful
4. **Practical Examples and Case Studies**: Real-world applications, scenarios, and worked examples
5. **Hands-On Exercises**: Practice activities with detailed solutions and explanations
6. **Troubleshooting Guides**: Common problems, error messages, and solutions
7. **Best Practices and Expert Tips**: Professional insights, recommendations, and advanced techniques
8. **Chapter Summary**: Key takeaways and what was learned
9. **Chapter Quiz**: 5-10 questions with detailed answers and explanations

Research current information using available tools to ensure content accuracy and relevance. 
Work only on chapters specifically assigned to Creator 2 in the book structure plan.""",
        expected_output="""Complete comprehensive book chapters for specifically assigned 
    chapters with appropriate depth based on cost optimization. Include detailed theoretical 
    content, step-by-step procedures, practical examples, exercises with solutions, 
    troubleshooting guides, and chapter assessments needed for readers to master the 
    material.""",
        agent=None,
        context=[],
    )