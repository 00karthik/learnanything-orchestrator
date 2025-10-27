# Orchestrator Project Brief (for AI Agents)

## Mission Snapshot
- **Goal:** Generate a polished, self-contained tutorial "book" for a learner-specified topic, skill level, and time commitment.
- **Inputs:** `topic`, `skill_level`, `time_commitment` collected via CLI prompts or arguments.
- **Deliverables:**
  - Structured intermediate artefacts (analysis notes, chapter drafts, resource list, assessments).
  - Final HTML tutorial saved to `outputs/<topic>_tutorial.html` with quizzes, resources, glossary, and assessments.
  - JSON run log written to `outputs/<topic>-<timestamp>.json` for auditing/testing.

## System Architecture
1. **Entry Point:** `python -m learn_anything.main run`
   - Prompts for inputs when missing.
   - Instantiates `ComprehensiveTutorialGeneratorCrew` and kicks off sequential task pipeline.
   - After completion, rebuilds HTML locally via `build_html_document()` to ensure deterministic output.

2. **Crew Configuration (`src/learn_anything/crew.py`):**
   - Eight agents mapped to single-responsibility tasks (topic analysis, structure, two chapter creators, resources, assessments, compilation, HTML).
   - Sequential process ensures each task sees previous artefacts.
   - Per-agent LLM configuration handled via `llm_config.get_llm()` (supports environment-driven provider overrides and `LLM_MODE`).

3. **Tasks (`src/learn_anything/tasks_srp/`):**
   - Each factory returns a `Task` with detailed instructions focused on the simplified inputs.
   - Notable requirements:
     - Chapter creators generate different chapter subsets for parallel coverage.
     - Compilation task enforces gamified assessments plus summary chapter.
     - HTML task expects a full `<html>` document with styling, navigation, quizzes, and accessibility features.

4. **HTML Builder (`src/learn_anything/html_builder.py`):**
   - Parses compiled book markdown and related artefacts.
   - Generates deterministic HTML with sections:
     - Landing header, table of contents, introduction, per-chapter articles (each with embedded quiz), resources, assessments, glossary, footer.
   - Includes accessible styling, responsive layout, reusable components, and back-to-top navigation.
   - Uses Python-Markdown library when available; falls back to lightweight converter otherwise.

## Environment & Dependencies
- Python >= 3.10.
- Key packages: `crewai[tools]`, `jambo`, `markdown` (new dependency for HTML conversion).
- `.env` expected with LLM credentials and `LLM_MODE` to route to Gemini or Bedrock.
- CLI commands respect Fish shell quirks (no heredocs).

## Generated Outputs
- **HTML:** `outputs/<topic>_tutorial.html` (always rebuilt locally post-run to avoid truncation issues).
- **JSON log:** `outputs/<topic>-<timestamp>.json` containing structured summary of task outputs.
- **Historical artefacts:** Intermediate tutorial book markdown stored transiently in task results (also persisted in JSON log when saving).

## Known Considerations
- Chapter extraction currently parses markdown headings; migrating to structured JSON would increase reliability for large topics.
- Additional chapter agents can be added by extending crew configuration to handle larger curricula.
- Ensure `markdown` package installed to avoid fallback rendering when high-fidelity HTML is required.

## Suggested Next Steps
1. Define a JSON schema for chapter outputs to reduce parsing heuristics.
2. Add more chapter-creation agents for large or advanced topics.
3. Enhance error handling around LLM failures and partial outputs.
4. Expand unit/integration tests around HTML builder to guard against regressions.

This brief should give downstream AI agents enough context to operate on the project without re-deriving the architecture or historical decisions.