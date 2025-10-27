from crewai import Task


def get_analyze_topic_and_requirements_task() -> Task:
    """Task for analyzing topic and requirements to create a validated foundation for curriculum design."""
    return Task(
        description="""You are analyzing the topic **{topic}** to create a validated foundation for curriculum design.

LEARNER CONTEXT:
- Topic: {topic}
- Skill Level: {skill_level}
- Time Commitment: {time_commitment}
- Learning Pace: {learning_pace}
- Learning Style: {learning_style}
- Goal: {goal}
- Constraints/Preferences: {constraints_preferences}

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
Example skills: "Define container", "Identify orchestration tools", "List Kubernetes components"

**Level 2: COMPREHENSION / UNDERSTANDING**
- What learners should understand and explain
- Relationships between concepts
- How things work and why they matter
Example skills: "Explain how containers differ from VMs", "Describe pod lifecycle", "Interpret kubectl output"

**Level 3: APPLICATION / APPLYING**
- What learners should be able to do
- Practical skills and hands-on tasks
- Using concepts in new situations
Example skills: "Deploy an application to Kubernetes", "Create a service manifest", "Scale a deployment"

**Level 4: ANALYSIS (if time permits)**
- What learners should be able to evaluate and compare
- Troubleshooting and debugging
- Decision-making between alternatives
Example skills: "Debug pod failures", "Choose between deployment strategies", "Analyze cluster performance"

**Level 5+: SYNTHESIS/EVALUATION (typically beyond beginner scope)**
- Advanced design, optimization, production patterns
- Only include if skill_level is advanced and time allows

For each level, list 5-8 specific skills using action verbs.

2. PREREQUISITE ANALYSIS
───────────────────────────────────────────────────────────────
Identify what learners need to know BEFORE starting:

**CRITICAL PREREQUISITES (Must Have):**
For each prerequisite:
- Skill name (e.g., "Basic command line usage")
- Why it's required (e.g., "Kubernetes is managed via CLI tools")
- How to validate (e.g., "Can navigate directories, run commands with flags")
- Risk if missing (e.g., "Learner will struggle with kubectl syntax")

**HELPFUL PREREQUISITES (Nice to Have):**
For each:
- Skill name
- Why it helps (makes learning easier/faster)
- Workaround if missing (can be learned just-in-time)

**KNOWLEDGE GAP IDENTIFICATION:**
- Common gaps in prerequisite knowledge for {skill_level} learners
- Which prerequisites can be taught in "Module 0" if needed
- Estimated time to cover gaps (if we need to include them)

Example format:

CRITICAL:

Command Line Basics
Why: Kubernetes uses kubectl CLI for all operations
Validation: Can cd, ls, run programs with flags
Risk: Won't be able to follow hands-on exercises

HELPFUL:

YAML Syntax
Why: Kubernetes configs are YAML
Workaround: Can teach YAML basics in 5-10 minutes within curriculum


3. COMMON MISCONCEPTIONS
───────────────────────────────────────────────────────────────
Research and list common misunderstandings about {topic}:

For each misconception:
- **What learners often think**: The incorrect belief
- **Why it's wrong**: The reality
- **How to address**: Teaching strategy to correct it
- **When to address**: Which module/lesson should tackle it

Example:

Misconception: "Kubernetes is just Docker for production"
Reality: Kubernetes is a container orchestration platform; Docker is a container runtime.
K8s can use Docker but also containerd, CRI-O, etc.
Address: Clarify in Module 1 with clear definitions and a comparison table
Timing: Lesson M1.L1 or M1.L2

Identify 5-10 misconceptions specific to {topic} at {skill_level}.

4. MEASURABLE LEARNING OBJECTIVES
───────────────────────────────────────────────────────────────
Define 5-8 top-level learning outcomes for the entire curriculum.

**Requirements:**
- Use Bloom's Taxonomy action verbs (avoid "understand", "learn", "know")
- Be specific and measurable
- Align with learner's goal: {goal}
- Be achievable within time constraint: {time_commitment}
- Progress from lower to higher cognitive levels

**Bloom's Action Verbs by Level:**
- Remember: Define, List, Identify, Label, Name, State
- Understand: Explain, Describe, Summarize, Classify, Compare, Interpret
- Apply: Execute, Implement, Use, Demonstrate, Solve, Apply
- Analyze: Differentiate, Distinguish, Examine, Compare, Debug
- Evaluate: Judge, Critique, Assess, Evaluate
- Create: Design, Construct, Develop, Formulate, Build

Example (BAD):
❌ "Understand Kubernetes concepts"

Example (GOOD):
✅ "Explain the role of pods, services, and deployments in a Kubernetes cluster"
✅ "Deploy a containerized application using kubectl and YAML manifests"
✅ "Differentiate between ClusterIP, NodePort, and LoadBalancer service types"

List 5-8 objectives that span multiple Bloom levels.

5. SCOPE VALIDATION
───────────────────────────────────────────────────────────────
Validate what's realistically achievable given constraints:

**Time Analysis:**
- Total available time: {time_commitment}
- Parse into: X minutes per day, Y days per week, Z weeks
- Calculate total minutes: (X * Y * Z)
- Time allocation recommendation:
  * 70% core content
  * 20% exercises/practice
  * 10% buffer/review

**Realistic Scope Statement:**
Given {time_commitment} for {skill_level} learners, this curriculum should:
- Cover: [What CAN be covered comprehensively]
- Touch on: [What can be introduced but not mastered]
- Exclude: [What should be left for future learning]

Example:
Time: 10 min/day, 5 days/week, 3 weeks = 150 minutes (2.5 hours)
Realistic Scope:

CAN cover: Core Kubernetes concepts (pods, deployments, services), basic kubectl commands,
architecture understanding, hands-on with playground
CAN touch on: ConfigMaps, namespaces, basic troubleshooting
MUST exclude: Advanced networking, Helm, operators, security policies, production best
practices, certification prep

Scope Statement: "This curriculum provides foundational Kubernetes knowledge suitable for
casual learning—understanding what Kubernetes is, why it's used, and core architectural
concepts. Learners will gain hands-on exposure via playgrounds but won't achieve
production-readiness or certification level."
**Constraint Analysis:**
Review {constraints_preferences} and identify:
- Technical constraints (no local setup, need free resources)
- Learning constraints (prefer videos, avoid math-heavy content)
- Accessibility needs (screen reader support, color blindness)
- How these affect curriculum design decisions

═══════════════════════════════════════════════════════════════
INDUSTRY STANDARDS RESEARCH
═══════════════════════════════════════════════════════════════

Research current standards for {topic}:
- What skills do job postings commonly require?
- What certifications exist (CKAD, CKA for Kubernetes)?
- What do popular bootcamps/courses cover?
- What do official docs emphasize?
- What changed recently in this field?

Use this to inform:
- Which skills are most valuable to prioritize
- Industry terminology to use consistently
- Common tools/platforms learners should know
- Skills that are outdated or less relevant now""",
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

""",
        agent=None,
    )