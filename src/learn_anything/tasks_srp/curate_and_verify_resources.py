from crewai import Task


def get_curate_and_verify_resources_task() -> Task:
    """Task for curating and verifying external learning resources."""
    return Task(
        description="""Create a curated list of recommended external learning resources for 
    {topic} including:
1. **Resource Categories**: Books, websites, online courses, documentation, and tools
2. **Resource Descriptions**: Brief descriptions of what each resource offers
3. **Quality Assessment**: Authority, relevance, and skill level match  
4. **Alternative Sources**: Multiple options for each resource type
5. **Accessibility Notes**: Free vs paid resources, account requirements

Focus on providing resource recommendations and categories rather than extensive link 
validation. Provide search terms and resource types when specific URLs aren't 
available.""",
        expected_output="""A curated resource guide with recommended learning materials organized 
    by category, including resource descriptions, quality assessments, and alternative 
    options. Focus on resource recommendations rather than extensive link validation.""",
        agent=None,
        async_execution=True,
        context=[],
    )