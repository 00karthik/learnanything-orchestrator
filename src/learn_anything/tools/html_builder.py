import re
from dataclasses import dataclass
from typing import Dict, List, Optional

try:
    from markdown import Markdown  # type: ignore
except ImportError:  # pragma: no cover - fallback when markdown isn't installed yet
    Markdown = None  # type: ignore


@dataclass
class Chapter:
    """Simple data container for chapter level content."""

    index: int
    title: str
    anchor: str
    html: str


def _strip_code_fences(text: Optional[str]) -> str:
    if not text:
        return ""
    cleaned = text.strip()
    if cleaned.startswith("```") and cleaned.endswith("```"):
        cleaned = cleaned.split("\n", 1)[1]
        cleaned = cleaned.rsplit("\n", 1)[0]
    return cleaned.strip()


def _markdown_to_html(text: str) -> str:
    if not text:
        return ""
    if Markdown is None:
        # Minimal fallback: wrap paragraphs and preserve code blocks verbatim.
        escaped = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        paragraphs = [p.strip() for p in escaped.split("\n\n") if p.strip()]
        formatted = (para.replace("\n", "<br>") for para in paragraphs)
        return "".join(f"<p>{chunk}</p>" for chunk in formatted)
    md = Markdown(extensions=["fenced_code", "tables", "sane_lists"])
    return md.convert(text)


def _safe_anchor(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "section"


def _split_sections(content: str, level: str) -> Dict[str, str]:
    pattern = re.compile(rf"^{re.escape(level)}\s+(.+)$", re.MULTILINE)
    sections: Dict[str, str] = {}
    matches = list(pattern.finditer(content))
    for idx, match in enumerate(matches):
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(content)
        key = match.group(1).strip()
        sections[key] = content[start:end].strip()
    return sections


def _extract_chapters(content: str) -> List[Chapter]:
    chapters_raw = _split_sections(content, "###")
    chapters: List[Chapter] = []
    for idx, (title, body) in enumerate(chapters_raw.items(), start=1):
        anchor = _safe_anchor(f"chapter-{idx}-{title}")
        chapters.append(Chapter(index=idx, title=title, anchor=anchor, html=_markdown_to_html(body)))
    return chapters


def build_html_document(
    topic: str,
    compiled_book_text: str,
    curated_resources_text: str,
    assessments_text: str,
) -> str:
    """Render a complete HTML document from the generated markdown artefacts."""

    compiled_book_text = _strip_code_fences(compiled_book_text)
    curated_resources_text = _strip_code_fences(curated_resources_text)
    assessments_text = _strip_code_fences(assessments_text)

    title_match = re.search(r"^#\s+(.+)$", compiled_book_text, flags=re.MULTILINE)
    book_title = title_match.group(1).strip() if title_match else topic.title()

    body_after_title = compiled_book_text
    if title_match:
        title_line_end = title_match.end()
        body_after_title = compiled_book_text[title_line_end:].strip()

    top_sections = _split_sections(body_after_title, "##")

    introduction_md = top_sections.get("1. BOOK INTRODUCTION", "")
    tutorial_content_md = top_sections.get("2. COMPREHENSIVE TUTORIAL CONTENT", "")
    supplementary_md = top_sections.get("3. SUPPLEMENTARY RESOURCES", "")
    assessments_md = top_sections.get("4. ASSESSMENT AND PRACTICE", "")

    introduction_html = _markdown_to_html(introduction_md)

    chapters = _extract_chapters(tutorial_content_md)

    supplementary_sections = _split_sections(supplementary_md, "###")
    resources_tools_html = _markdown_to_html(supplementary_sections.get("3.1. Recommended Tools and Materials", ""))
    external_resources_html = _markdown_to_html(supplementary_sections.get("3.2. External Resources", ""))
    glossary_html = _markdown_to_html(supplementary_sections.get("3.3. Glossary", ""))
    references_html = _markdown_to_html(supplementary_sections.get("3.4. References", ""))

    curated_resources_html = _markdown_to_html(curated_resources_text)

    toc_entries = [("introduction", "Introduction")]
    for chapter in chapters:
        toc_entries.append((chapter.anchor, chapter.title))
    toc_entries.append(("resources", "Resources"))
    toc_entries.append(("glossary", "Glossary"))

    chapter_articles = []
    for chapter in chapters:
        quiz_html = _render_default_quiz(chapter)
        chapter_html = f"""
        <article id="{chapter.anchor}">
            <h3>{chapter.title}</h3>
            {chapter.html}
            {quiz_html}
            <a href="#" class="back-to-top">Back to Top</a>
        </article>
        """
        chapter_articles.append(chapter_html)

    toc_list = "\n".join(
        f'<li><a href="#{anchor}">{label}</a></li>' for anchor, label in toc_entries
    )

    html = f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>{book_title}</title>
    <style>
        *, *::before, *::after {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        :root {{
            --color-bg: #f9f9f9;
            --color-text: #333;
            --color-primary: #007bff;
            --color-secondary: #6c757d;
            --color-accent: #28a745;
            --color-warning: #ffc107;
            --color-error: #dc3545;
            --color-info: #17a2b8;
            --color-light: #f8f9fa;
            --color-dark: #343a40;
            --color-border: #dee2e6;
            --font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            --font-size-base: 1rem;
            --line-height-base: 1.5;
            --border-radius: 0.25rem;
            --box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
            --spacing-xs: 0.25rem;
            --spacing-sm: 0.5rem;
            --spacing-md: 1rem;
            --spacing-lg: 1.5rem;
            --spacing-xl: 3rem;
            --transition-duration: 0.2s;
        }}

        @media (prefers-color-scheme: dark) {{
            :root {{
                --color-bg: #121212;
                --color-text: #eee;
                --color-border: #444;
                --color-light: #1e1e1e;
            }}
        }}

        body {{
            font-family: var(--font-family);
            font-size: var(--font-size-base);
            line-height: var(--line-height-base);
            color: var(--color-text);
            background-color: var(--color-bg);
            margin: 0;
            transition: background-color var(--transition-duration), color var(--transition-duration);
        }}

        .skip-link {{
            position: absolute;
            top: -40px;
            left: 0;
            background: var(--color-dark);
            color: var(--color-light);
            padding: var(--spacing-sm);
            z-index: 1000;
        }}

        .skip-link:focus {{
            top: 0;
        }}

        nav {{
            background-color: var(--color-dark);
            color: var(--color-light);
            padding: var(--spacing-sm) 0;
            position: sticky;
            top: 0;
            z-index: 100;
        }}

        nav .container {{
            width: 90%;
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        nav ul {{
            list-style: none;
            display: flex;
            gap: var(--spacing-sm);
        }}

        nav a {{
            color: var(--color-light);
            text-decoration: none;
            padding: var(--spacing-sm) var(--spacing-md);
            border-radius: var(--border-radius);
            display: inline-block;
        }}

        nav a:hover,
        nav a:focus {{
            background-color: rgba(255, 255, 255, 0.1);
        }}

        header.landing {{
            text-align: center;
            padding: var(--spacing-xl) 0;
            background: linear-gradient(135deg, var(--color-primary), var(--color-info));
            color: var(--color-light);
        }}

        header.landing h1 {{
            font-size: clamp(2.2rem, 4vw, 3rem);
            margin-bottom: var(--spacing-md);
        }}

        header.landing p {{
            font-size: 1.2rem;
        }}

        .container {{
            width: 90%;
            max-width: 1100px;
            margin: 0 auto;
            padding: var(--spacing-lg) 0;
        }}

        section {{
            margin-bottom: var(--spacing-xl);
        }}

        section h2 {{
            margin-bottom: var(--spacing-md);
            border-bottom: 2px solid var(--color-primary);
            padding-bottom: var(--spacing-sm);
        }}

        h3 {{
            margin-bottom: var(--spacing-sm);
            color: var(--color-dark);
        }}

        p {{
            margin-bottom: var(--spacing-md);
        }}

        ul, ol {{
            margin-bottom: var(--spacing-md);
            padding-left: 1.25rem;
        }}

        li {{
            margin-bottom: var(--spacing-xs);
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: var(--spacing-lg);
        }}

        th, td {{
            border: 1px solid var(--color-border);
            padding: var(--spacing-sm);
            text-align: left;
        }}

        th {{
            background-color: var(--color-light);
        }}

        pre {{
            background: #1e1e1e;
            color: #f5f5f5;
            padding: var(--spacing-md);
            border-radius: var(--border-radius);
            overflow-x: auto;
            margin-bottom: var(--spacing-md);
        }}

        code {{
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
            font-size: 0.9rem;
        }}

        .toc ul {{
            list-style: none;
            padding-left: 0;
        }}

        .toc li {{
            margin-bottom: var(--spacing-sm);
        }}

        .toc a {{
            color: var(--color-primary);
            text-decoration: none;
        }}

        .toc a:hover {{
            text-decoration: underline;
        }}

        .callout-info,
        .callout-warning,
        .callout-error,
        .callout-success {{
            padding: var(--spacing-md);
            border-left: 4px solid;
            border-radius: var(--border-radius);
            margin-bottom: var(--spacing-md);
        }}

        .callout-info {{
            border-color: var(--color-info);
            background-color: rgba(23, 162, 184, 0.1);
        }}

        .callout-warning {{
            border-color: var(--color-warning);
            background-color: rgba(255, 193, 7, 0.1);
        }}

        .callout-error {{
            border-color: var(--color-error);
            background-color: rgba(220, 53, 69, 0.1);
        }}

        .callout-success {{
            border-color: var(--color-accent);
            background-color: rgba(40, 167, 69, 0.1);
        }}

        .learning-objective {{
            padding: var(--spacing-md);
            background-color: var(--color-light);
            border-left: 5px solid var(--color-accent);
            margin-bottom: var(--spacing-md);
        }}

        .checklist {{
            list-style: none;
            padding-left: 0;
        }}

        .checklist li::before {{
            content: "\2713";
            color: var(--color-accent);
            margin-right: var(--spacing-sm);
        }}

        .assessment-card {{
            border: 1px solid var(--color-border);
            border-radius: var(--border-radius);
            padding: var(--spacing-md);
            margin-bottom: var(--spacing-md);
            box-shadow: var(--box-shadow);
        }}

        .chapter-quiz {{
            border: 1px solid var(--color-border);
            border-radius: var(--border-radius);
            padding: var(--spacing-md);
            margin: var(--spacing-lg) 0;
            background-color: var(--color-light);
        }}

        .chapter-quiz h4 {{
            margin-bottom: var(--spacing-md);
        }}

        fieldset {{
            border: none;
            margin-bottom: var(--spacing-md);
        }}

        legend {{
            font-weight: 600;
            margin-bottom: var(--spacing-sm);
        }}

        label {{
            display: block;
            margin-bottom: var(--spacing-xs);
        }}

        textarea {{
            width: 100%;
            padding: var(--spacing-sm);
            border-radius: var(--border-radius);
            border: 1px solid var(--color-border);
            min-height: 5rem;
            resize: vertical;
        }}

        details {{
            margin-top: var(--spacing-md);
            padding: var(--spacing-sm) var(--spacing-md);
            border: 1px solid var(--color-border);
            border-radius: var(--border-radius);
            background-color: white;
        }}

        summary {{
            font-weight: 600;
            cursor: pointer;
        }}

        .resource-appendix {{
            margin-top: var(--spacing-lg);
            border-top: 1px solid var(--color-border);
            padding-top: var(--spacing-lg);
        }}

        .media-frame {{
            position: relative;
            padding-bottom: 56.25%;
            height: 0;
            overflow: hidden;
            border-radius: var(--border-radius);
            margin-bottom: var(--spacing-md);
        }}

        .media-frame iframe,
        .media-frame img {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: 0;
        }}

        .back-to-top {{
            display: inline-block;
            margin-top: var(--spacing-md);
            padding: var(--spacing-sm) var(--spacing-md);
            background-color: var(--color-primary);
            color: var(--color-light);
            border-radius: var(--border-radius);
            text-decoration: none;
        }}

        footer {{
            background-color: var(--color-dark);
            color: var(--color-light);
            text-align: center;
            padding: var(--spacing-lg) 0;
            font-size: 0.875rem;
        }}

        @media (max-width: 768px) {{
            nav .container {{
                flex-direction: column;
                gap: var(--spacing-sm);
            }}

            nav ul {{
                flex-wrap: wrap;
                justify-content: center;
            }}

            .container {{
                width: 95%;
            }}
        }}
    </style>
</head>
<body>
    <a class=\"skip-link\" href=\"#main\">Skip to main content</a>
    <nav>
        <div class=\"container\">
            <a href=\"#\">{book_title}</a>
            <ul>
                <li><a href=\"#introduction\">Introduction</a></li>
                <li><a href=\"#chapters\">Chapters</a></li>
                <li><a href=\"#resources\">Resources</a></li>
                <li><a href=\"#glossary\">Glossary</a></li>
            </ul>
        </div>
    </nav>

    <header class=\"landing\">
        <div class=\"container\">
            <h1>{book_title}</h1>
            <p>Learn {topic.title()} from foundational concepts to confident application.</p>
        </div>
    </header>

    <main id=\"main\">
        <section class=\"container toc\">
            <h2>Table of Contents</h2>
            <ul>
                {toc_list}
            </ul>
        </section>

        <section id=\"introduction\" class=\"container\">
            <h2>Introduction</h2>
            <article>
                {introduction_html}
            </article>
            <a href=\"#\" class=\"back-to-top\">Back to Top</a>
        </section>

        <section id=\"chapters\" class=\"container\">
            <h2>Chapters</h2>
            {''.join(chapter_articles)}
        </section>

        <section id=\"resources\" class=\"container\">
            <h2>Resources</h2>
            <article>
                <h3>Recommended Tools and Materials</h3>
                {resources_tools_html}
            </article>
            <article>
                <h3>External Resources</h3>
                {external_resources_html}
            </article>
            <article class=\"resource-appendix\">
                <h3>Curated Resource Guide</h3>
                {curated_resources_html}
            </article>
            <a href=\"#\" class=\"back-to-top\">Back to Top</a>
        </section>

        <section id=\"glossary\" class=\"container\">
            <h2>Glossary &amp; References</h2>
            <article>
                <h3>Glossary</h3>
                {glossary_html}
            </article>
            <article>
                <h3>References</h3>
                {references_html}
            </article>
            <a href=\"#\" class=\"back-to-top\">Back to Top</a>
        </section>
    </main>

    <footer>
        <p>&copy; {book_title}. Crafted with the Comprehensive Tutorial Generator.</p>
    </footer>
</body>
</html>"""

    return html


def _render_default_quiz(chapter: Chapter) -> str:
    """Generate a lightweight formative quiz for each chapter."""

    base_id = chapter.anchor
    mc_question_id = f"{base_id}-mc"
    tf_question_id = f"{base_id}-tf"
    mc_two_question_id = f"{base_id}-mc2"

    multiple_choice_options = """
                <label><input type=\"radio\" name=\"{mc_question_id}\" value=\"option1\"> Reinforcing the key ideas from {chapter_title}</label>
                <label><input type=\"radio\" name=\"{mc_question_id}\" value=\"option2\"> Exploring unrelated infrastructure topics</label>
                <label><input type=\"radio\" name=\"{mc_question_id}\" value=\"option3\"> Reviewing project management methodologies</label>
                <label><input type=\"radio\" name=\"{mc_question_id}\" value=\"option4\"> Designing user interface mockups</label>
    """.format(mc_question_id=mc_question_id, chapter_title=chapter.title)

    second_mc_options = """
                <label><input type=\"radio\" name=\"{mc_two_question_id}\" value=\"option1\"> Repeat the hands-on exercise described in the chapter</label>
                <label><input type=\"radio\" name=\"{mc_two_question_id}\" value=\"option2\"> Memorise definitions without practice</label>
                <label><input type=\"radio\" name=\"{mc_two_question_id}\" value=\"option3\"> Skip directly to advanced certification topics</label>
                <label><input type=\"radio\" name=\"{mc_two_question_id}\" value=\"option4\"> Focus solely on command syntax flashcards</label>
    """.format(mc_two_question_id=mc_two_question_id)

    quiz_html = f"""
        <section class=\"chapter-quiz\">
            <h4>Chapter {chapter.index} Quiz</h4>
            <form>
                <fieldset>
                    <legend>1. Multiple Choice: What is the primary focus of {chapter.title}?</legend>
                    {multiple_choice_options}
                </fieldset>
                <fieldset>
                    <legend>2. True or False: Mastery of this chapter prepares you for the next module.</legend>
                    <label><input type=\"radio\" name=\"{tf_question_id}\" value=\"true\"> True</label>
                    <label><input type=\"radio\" name=\"{tf_question_id}\" value=\"false\"> False</label>
                </fieldset>
                <fieldset>
                    <legend>3. Short Answer: Identify one critical term or command from this chapter.</legend>
                    <textarea name=\"{base_id}-sa-1\" aria-label=\"List a key concept\"></textarea>
                </fieldset>
                <fieldset>
                    <legend>4. Multiple Choice: Which activity best reinforces the learning objectives?</legend>
                    {second_mc_options}
                </fieldset>
                <fieldset>
                    <legend>5. Short Answer: Describe how you would apply lessons from this chapter in a real scenario.</legend>
                    <textarea name=\"{base_id}-sa-2\" aria-label=\"Describe application\"></textarea>
                </fieldset>
            </form>
            <details>
                <summary>Answer Key &amp; Mastery Guidance</summary>
                <ul>
                    <li><strong>Q1:</strong> Reinforcing the key ideas from {chapter.title}. Focus on the essential concepts and workflows presented.</li>
                    <li><strong>Q2:</strong> True. Each chapter builds toward the comprehensive mastery goals.</li>
                    <li><strong>Q3:</strong> Accept any term highlighted in the chapter narrative or exercises.</li>
                    <li><strong>Q4:</strong> Repeat the hands-on exercise described in the chapter to consolidate knowledge.</li>
                    <li><strong>Q5:</strong> Learner articulates a scenario demonstrating practical transfer of the chapter's skills.</li>
                </ul>
                <p><strong>Scoring rubric:</strong> Award 1 point per multiple-choice or true/false question, and 0-2 points for each short answer. Aim for 80%+ to progress confidently.</p>
            </details>
        </section>
    """
    return quiz_html


__all__ = ["build_html_document"]
