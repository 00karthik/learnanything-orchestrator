# ComprehensiveTutorialBookGenerator Crew

Generate a comprehensive tutorial book from a topic using a multi-agent crew. The project uses crewAI with a single-responsibility architecture for agents and tasks, and a Python CLI for running and saving outputs.

## Features

- Multi-agent workflow to analyze topics, design structure, curate resources, and compile chapters.
- Centralized LLM configuration via `src/comprehensive_tutorial_generator/llm_config.py`.
- JSON-only output saving with timestamped filenames in `./outputs`.
- Interactive mode to fill missing inputs, or pass flags for non-interactive runs.

## Installation

Ensure you have Python >=3.10 and <3.14.

```bash
pip install -e .
```

## Configuration

Create a `.env` file at the project root to configure API keys and model:

```env
# API key (either works; GOOGLE_API_KEY is bridged to GEMINI_API_KEY)
GEMINI_API_KEY=your_api_key
GOOGLE_API_KEY=your_api_key

# Default model and temperature (optional)
GEMINI_MODEL=gemini/gemini-2.0-flash
LLM_TEMPERATURE=0.2
```

Notes:
- If `GEMINI_API_KEY` is not set, the code will use `GOOGLE_API_KEY` automatically.
- Agents read the LLM config from `llm_config.py`, so changes in `.env` apply across all agents.

## Running

Run the crew from the project root:

```bash
python -m comprehensive_tutorial_generator.main run --interactive
```

Provide inputs non-interactively with flags:

```bash
python -m comprehensive_tutorial_generator.main run \
  --topic "Kubernetes" \
  --skill-level "intermediate" \
  --assessment-goal "hands-on project" \
  --cost-optimization "low" \
  --time-commitment "6 weeks" \
  --learning-pace "steady" \
  --learning-style "visual" \
  --goal "prepare for certification" \
  --constraints-preferences "focus on CNFs" \
  --output-dir ./outputs \
  --output-basename kube_tutorial
```

Output saving:
- The final crew output is saved as a single JSON file under `./outputs`.
- Filenames include a timestamp: e.g., `kube_tutorial-YYYYMMDD-HHMMSS.json`.
- Non-JSON formats (PDF/Markdown/TXT) have been removed.

CLI help:

```bash
python -m comprehensive_tutorial_generator.main run --help
```

## Project Structure

```
src/comprehensive_tutorial_generator/
├── agents.py                  # Compatibility wrapper
├── agents_srp/                # Single-responsibility agents
├── crew.py                    # Crew assembly
├── llm_config.py              # Shared LLM configuration
├── main.py                    # CLI entrypoint
├── tasks.py                   # Compatibility wrapper
├── tasks_srp/                 # Single-responsibility tasks
└── tools/                     # Optional tools
```

## Development Notes

- To adjust agent models or temperature globally, edit `.env` or `llm_config.py`.
- To add new behaviors, create agents in `agents_srp/` and tasks in `tasks_srp/`, then wire them in `crew.py`.

## Support

- crewAI docs: https://docs.crewai.com
- crewAI GitHub: https://github.com/joaomdmoura/crewai

This project embraces SRP and a minimal CLI for predictable runs and outputs.
