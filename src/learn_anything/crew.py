import os
import json
from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
# Removed SerperDevTool integration per request



from pydantic import BaseModel
from jambo import SchemaConverter

# Use Python agent & task factories instead of YAML configs
from .agents import (
    get_topic_analysis_specialist,
    get_resource_curator,
    get_assessment_designer,
    get_tutorial_compiler,
    get_chapter_creator_1,
    get_chapter_creator_2,
    get_structure_analyzer,
    get_html_document_generator,
)
from .tasks import (
    get_analyze_topic_and_requirements_task,
    get_analyze_chapter_structure_task,
    get_create_assigned_chapters_1_task,
    get_create_assigned_chapters_2_task,
    get_curate_and_verify_resources_task,
    get_create_assessments_and_exercises_task,
    get_compile_comprehensive_tutorial_task,
    get_convert_tutorial_to_html_format_task,
)

# Bridge GOOGLE_API_KEY -> GEMINI_API_KEY for LiteLLM/Gemini
if "GOOGLE_API_KEY" in os.environ and not os.environ.get("GEMINI_API_KEY"):
    os.environ["GEMINI_API_KEY"] = os.environ["GOOGLE_API_KEY"]

@CrewBase
class ComprehensiveTutorialGeneratorCrew:
    """ComprehensiveTutorialGenerator crew"""

    
    @agent
    def topic_analysis_specialist(self) -> Agent:
        agent = get_topic_analysis_specialist()
        return agent
    
    @agent
    def resource_curator(self) -> Agent:
        return get_resource_curator()
    
    @agent
    def assessment_designer(self) -> Agent:
        return get_assessment_designer()
    
    @agent
    def tutorial_compiler(self) -> Agent:
        return get_tutorial_compiler()
    
    @agent
    def chapter_creator_1(self) -> Agent:
        return get_chapter_creator_1()
    
    @agent
    def chapter_creator_2(self) -> Agent:
        return get_chapter_creator_2()
    
    @agent
    def structure_analyzer(self) -> Agent:
        agent = get_structure_analyzer()
        return agent
    
    @agent
    def html_document_generator(self) -> Agent:
        return get_html_document_generator()
    

    
    @task
    def analyze_topic_and_requirements(self) -> Task:
        task = get_analyze_topic_and_requirements_task()
        task.agent = self.topic_analysis_specialist()
        task.markdown = False
        return task
    
    @task
    def analyze_chapter_structure(self) -> Task:
        task = get_analyze_chapter_structure_task()
        task.agent = self.structure_analyzer()
        task.markdown = False
        return task
    
    @task
    def create_assigned_chapters_1(self) -> Task:
        task = get_create_assigned_chapters_1_task()
        task.agent = self.chapter_creator_1()
        task.markdown = False
        return task
    
    @task
    def create_assigned_chapters_2(self) -> Task:
        task = get_create_assigned_chapters_2_task()
        task.agent = self.chapter_creator_2()
        task.markdown = False
        return task
    
    @task
    def curate_and_verify_resources(self) -> Task:
        task = get_curate_and_verify_resources_task()
        task.agent = self.resource_curator()
        task.markdown = False
        return task
    
    @task
    def create_assessments_and_exercises(self) -> Task:
        task = get_create_assessments_and_exercises_task()
        task.agent = self.assessment_designer()
        task.markdown = False
        return task
    
    @task
    def compile_comprehensive_tutorial_book(self) -> Task:
        task = get_compile_comprehensive_tutorial_task()
        task.agent = self.tutorial_compiler()
        task.markdown = False
        return task
    
    @task
    def convert_tutorial_to_html_format(self) -> Task:
        task = get_convert_tutorial_to_html_format_task()
        task.agent = self.html_document_generator()
        task.markdown = False
        return task
    

    @crew
    def crew(self) -> Crew:
        """Creates the ComprehensiveTutorialBookGenerator crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )

    def _load_response_format(self, name):
        with open(os.path.join(self.base_directory, "config", f"{name}.json")) as f:
            json_schema = json.loads(f.read())

        return SchemaConverter.build(json_schema)
