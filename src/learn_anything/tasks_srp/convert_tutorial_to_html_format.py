from crewai import Task


def get_convert_tutorial_to_html_format_task() -> Task:
    """Task for converting the tutorial book to HTML-ready format."""
    return Task(
        description="""Convert the compiled tutorial book into a professionally structured HTML 
    document for {topic}. Transform the book content into a well-organized site-like output with:

1. **Page Structure**: Landing page, table of contents, chapter sections, appendices, and index
2. **Semantic HTML**: Proper headings, subheadings, ordered and unordered lists, callout blocks, and tables
3. **Navigation Aids**: Internal links, anchors, and consistent navigation to move across chapters
4. **Responsive Formatting**: Clean typography, spacing, and layout suitable for both desktop and mobile reading
5. **Asset Embedding Plan**: Guidance on placing media (images, code snippets, downloadable files) within HTML structure

Include all book components: introduction, chapters, resources, glossary, and assessments. 
Ensure the final HTML reads like a professional tutorial book with consistent styling hooks (classes, IDs) for later CSS theming.""",
        expected_output="""A professionally structured HTML tutorial book with semantic elements, 
    navigable sections, and styling hooks ready for theming. The output should clearly separate 
    chapters, reusable components, resources, and assessments in HTML format.""",
        agent=None,
    )
