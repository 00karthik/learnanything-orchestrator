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
For each chapter/section (excluding the final summary chapter):
- **Detailed Theoretical Explanations** - Complete concepts, principles, and background knowledge
- **Step-by-Step Procedures** - Clear, actionable instructions and techniques
- **Practical Examples and Case Studies** - Real-world applications and scenarios
- **Hands-On Exercises** - Practice activities with detailed solutions
- **Troubleshooting Guides** - Common problems and solutions
- **Best Practices and Expert Tips** - Professional insights and recommendations
- **Gamified Assessment & Practice** - Immediately following the core content, add a game-inspired assessment zone featuring a chapter quiz (5+ varied question types), interactive challenges or mini-games, progress trackers/XP badges, and reflective prompts. Design it so learners can instantly gauge mastery before moving on.

**3. SUPPLEMENTARY RESOURCES**
- **Recommended Tools and Materials** - What readers need to practice
- **External Resources** - Books, websites, and additional learning materials
- **Glossary** - Key terms and definitions
- **References** - Sources and further reading

**4. ASSESSMENT AND PRACTICE**
- **Cumulative Gameboard** - Summaries of chapter gamified results, leaderboard style progress, and achievement badges unlocked across the book
- **Practice Projects** - Comprehensive exercises to apply knowledge
- **Self-Assessment Tools** - Progress tracking and skill evaluation
- **Final Mastery Test** - Comprehensive assessment with rubrics

**5. SUMMARY & NEXT STEPS (FINAL CHAPTER)**
- Recap key insights from every chapter
- Highlight earned achievements and meta-skills
- Provide next-step challenges, further learning quests, and encouragement for continued growth
- Include a reflection checklist and optional journaling prompts

Format as a complete tutorial book that readers can use independently to master {topic}.""",
        expected_output="""A comprehensive tutorial book with complete chapters covering 
    all aspects of {topic}. Include: (1) Book introduction and usage guide, (2) Detailed 
    tutorial content with explanations, procedures, examples, and exercises, (3) Supplementary 
    resources and references, (4) Assessment materials that extend the per-chapter gamified 
    experiences into cumulative challenges, and (5) A closing summary chapter with next-step 
    guidance. The content should be self-contained, gamefully engaging, and book-like in structure.""",
        agent=None,
    )