"""Dataclasses and helpers for structured tutorial book payloads."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def _strip_code_fence(text: str) -> str:
    text = text.strip()
    if text.startswith("```") and text.endswith("```"):
        # remove the first fence and the trailing fence line
        stripped = text.split("\n", 1)[1]
        stripped = stripped.rsplit("\n", 1)[0]
        return stripped.strip()
    return text


def _ensure_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


@dataclass
class SectionBlock:
    title: str = ""
    content: str = ""
    kind: str = "content"

    @classmethod
    def from_dict(cls, data: Any) -> "SectionBlock":
        if not isinstance(data, dict):
            return cls(content=str(data or ""))
        title = (data.get("title") or data.get("heading") or data.get("name") or "").strip()
        content = (data.get("content") or data.get("body") or data.get("text") or "").strip()
        kind = (data.get("kind") or data.get("type") or "content").strip()
        return cls(title=title, content=content, kind=kind)


@dataclass
class HandsOnExercise:
    title: str = ""
    objective: str = ""
    steps: List[str] = field(default_factory=list)
    solution: str = ""

    @classmethod
    def from_dict(cls, data: Any) -> "HandsOnExercise":
        if not isinstance(data, dict):
            return cls(title=str(data or ""))
        return cls(
            title=(data.get("title") or data.get("name") or "").strip(),
            objective=(data.get("objective") or data.get("goal") or "").strip(),
            steps=[str(item).strip() for item in _ensure_list(data.get("steps")) if str(item).strip()],
            solution=(data.get("solution") or data.get("answer") or "").strip(),
        )


@dataclass
class TroubleshootingItem:
    problem: str = ""
    solution: str = ""
    notes: str = ""

    @classmethod
    def from_dict(cls, data: Any) -> "TroubleshootingItem":
        if not isinstance(data, dict):
            return cls(problem=str(data or ""))
        return cls(
            problem=(data.get("problem") or data.get("issue") or data.get("symptom") or "").strip(),
            solution=(data.get("solution") or data.get("resolution") or "").strip(),
            notes=(data.get("notes") or data.get("tip") or "").strip(),
        )


@dataclass
class QuizQuestion:
    question: str = ""
    question_type: str = "short_answer"
    options: List[str] = field(default_factory=list)
    answer: str = ""
    explanation: str = ""

    @classmethod
    def from_dict(cls, data: Any) -> "QuizQuestion":
        if not isinstance(data, dict):
            return cls(question=str(data or ""))
        return cls(
            question=(data.get("question") or data.get("prompt") or "").strip(),
            question_type=(data.get("question_type") or data.get("type") or "short_answer").strip().lower(),
            options=[str(opt).strip() for opt in _ensure_list(data.get("options")) if str(opt).strip()],
            answer=(data.get("answer") or data.get("solution") or "").strip(),
            explanation=(data.get("explanation") or data.get("rationale") or "").strip(),
        )


@dataclass
class IntroductionPayload:
    topic_overview: str = ""
    what_you_will_learn: List[str] = field(default_factory=list)
    target_audience: List[str] = field(default_factory=list)
    how_to_use: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Any) -> "IntroductionPayload":
        if not isinstance(data, dict):
            return cls(topic_overview=str(data or ""))
        return cls(
            topic_overview=str(data.get("topic_overview") or data.get("overview") or "").strip(),
            what_you_will_learn=[str(item).strip() for item in _ensure_list(data.get("what_you_will_learn")) if str(item).strip()],
            target_audience=[str(item).strip() for item in _ensure_list(data.get("target_audience")) if str(item).strip()],
            how_to_use=[str(item).strip() for item in _ensure_list(data.get("how_to_use")) if str(item).strip()],
            prerequisites=[str(item).strip() for item in _ensure_list(data.get("prerequisites")) if str(item).strip()],
        )


@dataclass
class ResourceItem:
    name: str = ""
    description: str = ""
    url: str = ""
    access: str = ""

    @classmethod
    def from_dict(cls, data: Any) -> "ResourceItem":
        if not isinstance(data, dict):
            return cls(name=str(data or ""))
        return cls(
            name=(data.get("name") or data.get("title") or "").strip(),
            description=(data.get("description") or data.get("summary") or "").strip(),
            url=(data.get("url") or data.get("link") or "").strip(),
            access=(data.get("access") or data.get("notes") or "").strip(),
        )


@dataclass
class GlossaryEntry:
    term: str = ""
    definition: str = ""

    @classmethod
    def from_dict(cls, data: Any) -> "GlossaryEntry":
        if not isinstance(data, dict):
            return cls(term=str(data or ""))
        return cls(
            term=(data.get("term") or data.get("word") or "").strip(),
            definition=(data.get("definition") or data.get("meaning") or "").strip(),
        )


@dataclass
class SupplementaryResources:
    recommended_tools: List[ResourceItem] = field(default_factory=list)
    external_resources: List[ResourceItem] = field(default_factory=list)
    glossary: List[GlossaryEntry] = field(default_factory=list)
    references: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Any) -> "SupplementaryResources":
        if not isinstance(data, dict):
            return cls()
        return cls(
            recommended_tools=[ResourceItem.from_dict(item) for item in _ensure_list(data.get("recommended_tools"))],
            external_resources=[ResourceItem.from_dict(item) for item in _ensure_list(data.get("external_resources"))],
            glossary=[GlossaryEntry.from_dict(item) for item in _ensure_list(data.get("glossary"))],
            references=[str(item).strip() for item in _ensure_list(data.get("references")) if str(item).strip()],
        )


@dataclass
class ChapterPayload:
    chapter_number: int
    title: str
    estimated_time_minutes: Optional[int] = None
    learning_objectives: List[str] = field(default_factory=list)
    overview: str = ""
    theoretical_concepts: List[SectionBlock] = field(default_factory=list)
    procedures: List[SectionBlock] = field(default_factory=list)
    examples: List[SectionBlock] = field(default_factory=list)
    hands_on_exercises: List[HandsOnExercise] = field(default_factory=list)
    troubleshooting: List[TroubleshootingItem] = field(default_factory=list)
    best_practices: List[str] = field(default_factory=list)
    summary: str = ""
    quiz: List[QuizQuestion] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Any) -> "ChapterPayload":
        if not isinstance(data, dict):
            raise ValueError("Chapter payload must be a dictionary")
        chapter_number_raw = data.get("chapter_number") or data.get("number") or data.get("index") or 0
        try:
            chapter_number = int(chapter_number_raw)
        except (TypeError, ValueError):
            chapter_number = 0
        estimated_time = data.get("estimated_time_minutes") or data.get("estimated_minutes")
        try:
            estimated_time_minutes = int(estimated_time) if estimated_time is not None else None
        except (TypeError, ValueError):
            estimated_time_minutes = None

        return cls(
            chapter_number=chapter_number,
            title=(data.get("title") or data.get("name") or "").strip(),
            estimated_time_minutes=estimated_time_minutes,
            learning_objectives=[str(item).strip() for item in _ensure_list(data.get("learning_objectives")) if str(item).strip()],
            overview=(data.get("overview") or data.get("introduction") or "").strip(),
            theoretical_concepts=[SectionBlock.from_dict(item) for item in _ensure_list(data.get("theoretical_concepts"))],
            procedures=[SectionBlock.from_dict(item) for item in _ensure_list(data.get("procedures"))],
            examples=[SectionBlock.from_dict(item) for item in _ensure_list(data.get("examples"))],
            hands_on_exercises=[HandsOnExercise.from_dict(item) for item in _ensure_list(data.get("hands_on_exercises"))],
            troubleshooting=[TroubleshootingItem.from_dict(item) for item in _ensure_list(data.get("troubleshooting"))],
            best_practices=[str(item).strip() for item in _ensure_list(data.get("best_practices")) if str(item).strip()],
            summary=(data.get("summary") or data.get("recap") or "").strip(),
            quiz=[QuizQuestion.from_dict(item) for item in _ensure_list(data.get("quiz"))],
        )


@dataclass
class BookPayload:
    title: str
    introduction: IntroductionPayload
    chapters: List[ChapterPayload]
    supplementary: SupplementaryResources
    summary: str = ""

    @classmethod
    def from_dict(cls, data: Any) -> "BookPayload":
        if not isinstance(data, dict):
            raise ValueError("Book payload must be a dictionary")

        if "book" in data and isinstance(data["book"], dict):
            data = data["book"]

        title = (data.get("title") or data.get("book_title") or data.get("name") or "").strip()
        introduction = IntroductionPayload.from_dict(data.get("introduction") or {})
        chapters = [ChapterPayload.from_dict(item) for item in _ensure_list(data.get("chapters"))]
        supplementary = SupplementaryResources.from_dict(data.get("supplementary") or data.get("resources") or {})
        summary = (data.get("summary") or data.get("conclusion") or data.get("next_steps") or "").strip()

        if not chapters:
            raise ValueError("Book payload must contain at least one chapter")

        return cls(
            title=title,
            introduction=introduction,
            chapters=chapters,
            supplementary=supplementary,
            summary=summary,
        )


def parse_book_payload(raw_text: str) -> BookPayload:
    """Parse a raw string (possibly fenced) into a BookPayload."""

    cleaned = _strip_code_fence(raw_text)
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError("Provided text is not valid JSON") from exc
    return BookPayload.from_dict(data)


__all__ = [
    "BookPayload",
    "ChapterPayload",
    "SectionBlock",
    "HandsOnExercise",
    "TroubleshootingItem",
    "QuizQuestion",
    "SupplementaryResources",
    "parse_book_payload",
]
