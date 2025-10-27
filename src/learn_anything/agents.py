"""
Agent factories wrapper.

This module preserves the original import path while delegating to the
single-responsibility agent modules in `agents_srp/`.
"""

from .agents_srp import (
    get_topic_analysis_specialist,
    get_resource_curator,
    get_assessment_designer,
    get_tutorial_compiler,
    get_chapter_creator_1,
    get_chapter_creator_2,
    get_structure_analyzer,
    get_html_document_generator,
)

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
