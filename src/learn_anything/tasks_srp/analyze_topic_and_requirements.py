from crewai import Task


def get_analyze_topic_and_requirements_task() -> Task:
    """Task for analyzing topic and requirements to create a validated foundation for curriculum design."""
    return Task(
        description="""You are analyzing the topic **{topic}** to create a validated foundation for curriculum design.

LEARNER CONTEXT:
- Topic: {topic}
- Skill Level: {skill_level}
- Available Study Time: {time_commitment}

═══════════════════════════════════════════════════════════════
YOUR ANALYSIS MUST COVER 5 KEY AREAS:
═══════════════════════════════════════════════════════════════

1. COMPETENCY MODEL (Skill Hierarchy)
───────────────────────────────────────────────────────────────
Map the topic into a hierarchical competency model using Bloom's Taxonomy levels:

**Level 1: AWARENESS / REMEMBERING**
- What learners should recognize and recall
- Fundamental concepts and terminology
- Basic definitions and context

**Level 2: COMPREHENSION / UNDERSTANDING**
- What learners should understand and explain
- Relationships between concepts
- How things work and why they matter

**Level 3: APPLICATION / APPLYING**
- What learners should be able to do
- Practical skills and hands-on tasks
- Using concepts in new situations

**Level 4: ANALYSIS (if time permits)**
- What learners should be able to evaluate and compare
- Troubleshooting and debugging
- Decision-making between alternatives

**Level 5+: SYNTHESIS/EVALUATION (only include if skill_level is advanced and the time commitment allows)

For each level, list 4-6 specific skills using action verbs and connect them back to the expected learner outcome.

2. PREREQUISITE ANALYSIS
───────────────────────────────────────────────────────────────
Identify what learners need to know BEFORE starting:

**CRITICAL PREREQUISITES (Must Have):**
For each prerequisite:
- Skill name (e.g., "Basic command line usage")
- Why it's required
- How to validate readiness quickly
- Risk if missing

**HELPFUL PREREQUISITES (Nice to Have):**
For each:
- Skill name
- Why it helps (makes learning easier/faster)
- Workaround if missing (can be learned just-in-time)

**KNOWLEDGE GAP IDENTIFICATION:**
- Common gaps in prerequisite knowledge for {skill_level} learners
- Which prerequisites can be taught in a "Module 0" or prework segment
- Estimated time to cover each gap inside the available {time_commitment}

3. COMMON MISCONCEPTIONS
───────────────────────────────────────────────────────────────
Research and list common misunderstandings about {topic} for {skill_level} learners. For each misconception:
- **What learners often think**: The incorrect belief
- **Why it's wrong**: The reality
- **How to address**: Teaching strategy to correct it
- **When to address**: Which module/lesson should tackle it

Identify 5-8 misconceptions specific to {topic}.

4. MEASURABLE LEARNING OBJECTIVES
───────────────────────────────────────────────────────────────
Define 5-8 top-level learning outcomes for the entire curriculum.

**Requirements:**
- Use Bloom's Taxonomy action verbs (avoid "understand", "learn", "know")
- Be specific and measurable
- Align with the {skill_level} learner profile
- Be achievable within {time_commitment}
- Progress from lower to higher cognitive levels

5. SCOPE VALIDATION
───────────────────────────────────────────────────────────────
Validate what's realistically achievable given the time limit:

**Time Analysis:**
- Total available time: {time_commitment}
- Provide an explicit breakdown (minutes per session, sessions per week, total weeks) using reasonable assumptions
- Recommend time allocation: ~70% core content, ~20% practice, ~10% review

**Realistic Scope Statement:**
Given {time_commitment} for {skill_level} learners, clarify:
- Cover: [What CAN be covered comprehensively]
- Touch on: [What can be introduced but not mastered]
- Exclude: [What should be left for future learning]

**Assumptions & Constraints:**
- Note any assumptions you made about learner pace or access to resources
- Flag potential risks (e.g., topic complexity vs available time) and mitigation ideas

═══════════════════════════════════════════════════════════════
INDUSTRY STANDARDS RESEARCH
═══════════════════════════════════════════════════════════════

Research current standards for {topic}:
- Skills commonly required by job postings or certifications
- Focus areas in reputable courses or bootcamps
- Recent changes or trends learners should know

Use this to recommend which skills and terminology to prioritise during curriculum design.""",
        expected_output="""Return your analysis in this structure:
TOPIC ANALYSIS: {topic}
═══════════════════════════════════════════════════════════════

COMPETENCY MODEL
───────────────────────────────────────────────────────────────
Level 1 - AWARENESS:


[Skill 1]
[Skill 2]
...

Level 2 - COMPREHENSION:

[Skill 1]
...

Level 3 - APPLICATION:

[Skill 1]
...


PREREQUISITE ANALYSIS
───────────────────────────────────────────────────────────────
CRITICAL PREREQUISITES:


[Prerequisite 1]

Why: [Explanation]
Validation: [How to check]
Risk if missing: [Impact]



HELPFUL PREREQUISITES:

[Prerequisite 1]

Why: [Benefit]
Workaround: [Alternative]



KNOWLEDGE GAPS TO ADDRESS:

[Gap 1]
Why it matters: [Reason]
Time to cover: [Estimate]


COMMON MISCONCEPTIONS
───────────────────────────────────────────────────────────────
[Misconception]
Reality: [Correction]
Fix: [Strategy]
When to address: [Module/lesson]


MEASURABLE LEARNING OBJECTIVES
───────────────────────────────────────────────────────────────
1. [Objective]
...


SCOPE VALIDATION
───────────────────────────────────────────────────────────────
Time breakdown: [Minutes/session * sessions/week * weeks]
Coverage plan:
- Cover: [...]
- Touch on: [...]
- Exclude: [...]
Risks & assumptions: [...]


INDUSTRY INSIGHTS
───────────────────────────────────────────────────────────────
- [Insight 1]
- [Insight 2]

""",
                agent=None,
                context=[],
        )