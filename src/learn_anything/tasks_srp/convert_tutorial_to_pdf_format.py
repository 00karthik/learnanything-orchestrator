from crewai import Task


def get_convert_tutorial_to_pdf_format_task() -> Task:
    """Task for converting the tutorial book to PDF-ready format."""
    return Task(
        description="""Convert the compiled tutorial book into a professionally formatted 
    document ready for PDF export for {topic}. Transform the book content into a well-structured 
    document with:

1. **Book Structure**: Title page, table of contents, chapter 
   sections, appendices, and index
2. **Chapter Formatting**: Proper headings, subheadings, 
   numbered sections, bullet points, and consistent typography  
3. **Content Organization**: Clear chapter progression, step-by-step procedures, examples, and exercises
4. **Professional Design**: Consistent styling, appropriate spacing, readable fonts, 
   and book-like layout
5. **PDF-Ready Format**: Structured content optimized for 
   both digital reading and printing

Include all book components: introduction, chapters, resources, glossary, and assessments. 
Ensure the final document reads like a professional tutorial book.""",
        expected_output="""A professionally formatted tutorial book document with proper book 
    structure, chapter organization, and layout ready for PDF conversion. The output 
    should be well-organized with clear chapters, consistent formatting, and include 
    all tutorial book components in a readable, book-like format.""",
        agent=None,
        context=[],
    )