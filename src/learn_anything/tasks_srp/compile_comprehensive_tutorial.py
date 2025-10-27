from crewai import Task


def get_compile_comprehensive_tutorial_task() -> Task:
    """Task for compiling all components into a comprehensive tutorial book."""
    return Task(
        description="""Compile all components into a comprehensive tutorial book for {topic} with these main sections:

**1. BOOK INTRODUCTION**
- Topic overview and what readers will learn
- Who this book is for (target audience)
- How to use this book effectively
- Prerequisites and required knowledge

**2. COMPREHENSIVE TUTORIAL CONTENT**
For each chapter/section:
- **Detailed Theoretical Explanations** - Complete concepts, principles, and background knowledge
- **Step-by-Step Procedures** - Clear, actionable instructions and techniques
- **Practical Examples and Case Studies** - Real-world applications and scenarios
- **Hands-On Exercises** - Practice activities with detailed solutions
- **Troubleshooting Guides** - Common problems and solutions
- **Best Practices and Expert Tips** - Professional insights and recommendations

**3. SUPPLEMENTARY RESOURCES**
- **Recommended Tools and Materials** - What readers need to practice
- **External Resources** - Books, websites, and additional learning materials
- **Glossary** - Key terms and definitions
- **References** - Sources and further reading

**4. ASSESSMENT AND PRACTICE**
- **Chapter Quizzes** - Questions with detailed answers and explanations
- **Practice Projects** - Comprehensive exercises to apply knowledge
- **Self-Assessment Tools** - Progress tracking and skill evaluation
- **Final Mastery Test** - Comprehensive assessment with rubrics

Format as a complete tutorial book that readers can use independently to master {topic}.""",
        expected_output="""A comprehensive tutorial book with complete chapters covering 
    all aspects of {topic}. Include: (1) Book introduction and usage guide, (2) Detailed 
    tutorial content with explanations, procedures, examples, and exercises, (3) Supplementary 
    resources and references, and (4) Assessment materials with quizzes and projects. 
    The content should be self-contained and book-like in structure.""",
        agent=None,
        context=[],
    )