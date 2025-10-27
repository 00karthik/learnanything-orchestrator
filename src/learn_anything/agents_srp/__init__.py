"""
Single-responsibility agent factories.

Each module defines one agent factory. This package re-exports them
for convenient imports while keeping agents split by responsibility.
"""

from .topic_analysis_specialist import get_topic_analysis_specialist
from .resource_curator import get_resource_curator
from .assessment_designer import get_assessment_designer
from .tutorial_compiler import get_tutorial_compiler
from .chapter_creator_1 import get_chapter_creator_1
from .chapter_creator_2 import get_chapter_creator_2
from .structure_analyzer import get_structure_analyzer
from .html_document_generator import get_html_document_generator

__all__ = [
    "get_topic_analysis_specialist",
    "get_resource_curator",
    "get_assessment_designer",
    "get_tutorial_compiler",
    "get_chapter_creator_1",
    "get_chapter_creator_2",
    "get_structure_analyzer",
    "get_html_document_generator",
]