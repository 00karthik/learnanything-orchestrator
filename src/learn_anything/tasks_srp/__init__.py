"""
Single-responsibility task factories.

Each module defines one task factory. This package re-exports them
for convenient imports while keeping tasks split by responsibility.
"""

from .analyze_topic_and_requirements import get_analyze_topic_and_requirements_task
from .analyze_chapter_structure import get_analyze_chapter_structure_task
from .create_assigned_chapters_1 import get_create_assigned_chapters_1_task
from .create_assigned_chapters_2 import get_create_assigned_chapters_2_task
from .curate_and_verify_resources import get_curate_and_verify_resources_task
from .create_assessments_and_exercises import get_create_assessments_and_exercises_task
from .compile_comprehensive_tutorial import get_compile_comprehensive_tutorial_task
from .convert_tutorial_to_pdf_format import get_convert_tutorial_to_pdf_format_task

__all__ = [
    "get_analyze_topic_and_requirements_task",
    "get_analyze_chapter_structure_task",
    "get_create_assigned_chapters_1_task",
    "get_create_assigned_chapters_2_task",
    "get_curate_and_verify_resources_task",
    "get_create_assessments_and_exercises_task",
    "get_compile_comprehensive_tutorial_task",
    "get_convert_tutorial_to_pdf_format_task",
]