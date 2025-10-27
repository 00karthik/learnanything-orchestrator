from crewai import Task


def get_create_assessments_and_exercises_task() -> Task:
    """Task for creating comprehensive assessments and exercises."""
    return Task(
        description="""Design comprehensive assessment components for {topic} including:

**1. MODULE-SPECIFIC QUIZZES**
- 5-10 questions per module with multiple choice, true/false, and short answer formats
- Complete answer keys with detailed explanations
- Difficulty progression from basic recall to advanced application
- Clear scoring rubrics and mastery thresholds

**2. PRACTICE EXERCISES**
- Hands-on activities with step-by-step solutions
- Real-world application scenarios
- Varying difficulty levels for different learning stages
- Self-check mechanisms and progress indicators

**3. CHECKPOINT ASSESSMENTS**
- Module completion checkpoints with immediate feedback
- Knowledge gap identification tools
- Remediation recommendations for struggling areas
- Progress tracking and milestone celebrations

**4. COMPREHENSIVE EVALUATION**
- Capstone projects aligned with {assessment_goal}
- Final assessment covering all modules
- Mastery criteria and certification requirements
- Performance analytics and improvement suggestions

Create assessments that truly measure understanding and provide actionable feedback to learners.""",
        expected_output="""Complete assessment framework including: detailed module quizzes 
    with questions, answers, and explanations; practice exercises with solutions; 
    checkpoint assessments with feedback mechanisms; and comprehensive evaluation 
    tools. All assessments must include clear rubrics, mastery thresholds, and detailed 
    answer keys.""",
        agent=None,
        async_execution=True,
        context=[],
    )