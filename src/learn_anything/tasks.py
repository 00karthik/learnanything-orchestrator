"""
Task factories wrapper.

This module preserves the original import path while delegating to the
single-responsibility task modules in `tasks_srp/`.
"""

from .tasks_srp import (
    get_analyze_topic_and_requirements_task,
    get_analyze_chapter_structure_task,
    get_create_assigned_chapters_1_task,
    get_create_assigned_chapters_2_task,
    get_curate_and_verify_resources_task,
    get_create_assessments_and_exercises_task,
    get_compile_comprehensive_tutorial_task,
    get_convert_tutorial_to_pdf_format_task,
)

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