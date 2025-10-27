from crewai import Task


def get_analyze_chapter_structure_task() -> Task:
    """Task for analyzing book chapter structure to determine optimal organization."""
    return Task(
        description="""Analyze {topic} to determine the optimal book chapter structure for 
    a comprehensive tutorial book. Based on the topic analysis and {cost_optimization} 
    settings, define:

1. **Chapter Count**: Determine optimal number of chapters 
   (typically 4-12 chapters based on topic complexity)
2. **Chapter Specifications**: For each chapter, define:
   - Chapter title and main focus area
   - Key concepts and learning objectives
   - Prerequisites and chapter dependencies  
   - Content depth and complexity level
   - Estimated content requirements

3. **Book Flow and Progression**: Create logical chapter sequence that builds knowledge progressively
4. **Parallel Content Creation Plan**: Assign chapters to available content creators 
   for efficient parallel processing
5. **Chapter Dependencies**: Identify which chapters must be sequential vs which can be created independently

Output a clear book structure plan with specific chapter assignments for each content creator 
agent.""",
        expected_output="""Detailed book chapter structure including: exact number of chapters 
    needed, specific chapter titles and objectives, content creator assignments for 
    parallel processing, and chapter dependency mapping. Format as structured book 
    outline with clear assignments.""",
        agent=None,
        context=[],
    )