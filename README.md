# Learn Anything - AI Tutorial Generator

Generate comprehensive tutorial books and interactive learning materials from any topic using a multi-agent crew system. The project uses crewAI with a single-responsibility architecture for agents and tasks, featuring both JSON output and HTML generation capabilities.

## Features

- **Multi-agent workflow** to analyze topics, design structure, curate resources, and compile chapters
- **Centralized LLM configuration** via `src/learn_anything/llm_config.py`
- **Multiple output formats**: JSON data and interactive HTML tutorials
- **Interactive CLI** with optional non-interactive mode for automation
- **Timestamped outputs** saved in `./outputs` directory
- **Modular agent architecture** with single-responsibility principle

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

# Optional: Custom environment path
LEARN_ANYTHING_ENV_PATH=/path/to/custom/.env
```

**Notes:**
- If `GEMINI_API_KEY` is not set, the code will use `GOOGLE_API_KEY` automatically
- Agents read the LLM config from `llm_config.py`, so changes in `.env` apply across all agents
- You can specify a custom environment file path using `LEARN_ANYTHING_ENV_PATH`

## Usage

### Interactive Mode

Run the crew interactively from the project root:

```bash
python -m learn_anything.main run --interactive
```

### Non-Interactive Mode

Provide inputs directly with flags:

```bash
python -m learn_anything.main run \
  --topic "Kubernetes" \
  --skill-level "intermediate" \
  --time-commitment "6 weeks"
```

### Available Input Parameters

- `--topic`: The subject you want to learn (required)
- `--skill-level`: Your current skill level (beginner, intermediate, advanced)
- `--time-commitment`: How much time you can dedicate (e.g., "2 weeks", "1 month")

### Output Formats

The system generates two types of outputs:

1. **JSON Data**: Complete structured tutorial data saved as `tutorial_book-YYYYMMDD-HHMMSS.json`
2. **HTML Tutorial**: Interactive web-based tutorial saved as `[topic]_tutorial.html`

All outputs are saved in the `./outputs` directory with automatic timestamping.

### CLI Help

```bash
python -m learn_anything.main run --help
```

## Project Structure

```
src/learn_anything/
├── agents.py                  # Agent factory functions
├── agents_srp/                # Single-responsibility agents
│   ├── assessment_designer.py
│   ├── chapter_creator_1.py
│   ├── chapter_creator_2.py
│   ├── html_document_generator.py
│   ├── resource_curator.py
│   ├── structure_analyzer.py
│   ├── topic_analysis_specialist.py
│   └── tutorial_compiler.py
├── book_schema.py             # Tutorial book data structures
├── config/                    # Configuration files
│   ├── agents.yaml
│   ├── tasks.yaml
│   └── topic_analysis_specialist.json
├── crew.py                    # Crew assembly and orchestration
├── html_builder.py            # HTML generation utilities
├── llm_config.py              # Shared LLM configuration
├── main.py                    # CLI entrypoint
├── tasks.py                   # Task factory functions
├── tasks_srp/                 # Single-responsibility tasks
│   ├── analyze_chapter_structure.py
│   ├── analyze_topic_and_requirements.py
│   ├── compile_comprehensive_tutorial.py
│   ├── convert_tutorial_to_html_format.py
│   ├── create_assessments_and_exercises.py
│   ├── create_assigned_chapters_1.py
│   ├── create_assigned_chapters_2.py
│   └── curate_and_verify_resources.py
└── tools/                     # Utility tools
    └── html_builder.py
```

## How It Works

The system uses a multi-agent workflow where each agent has a specific responsibility:

1. **Topic Analysis Specialist**: Analyzes the input topic and learning requirements
2. **Structure Analyzer**: Designs the overall tutorial structure and chapter breakdown
3. **Chapter Creators**: Generate detailed content for assigned chapters
4. **Resource Curator**: Finds and verifies relevant learning resources
5. **Assessment Designer**: Creates exercises and assessments
6. **Tutorial Compiler**: Assembles all components into a cohesive tutorial
7. **HTML Document Generator**: Converts the tutorial into an interactive HTML format

## Development Notes

- **LLM Configuration**: To adjust agent models or temperature globally, edit `.env` or `llm_config.py`
- **Adding New Agents**: Create new agents in `agents_srp/` and corresponding tasks in `tasks_srp/`, then wire them in `crew.py`
- **Custom HTML Styling**: Modify `tools/html_builder.py` to customize the HTML output format
- **Environment Variables**: The system supports custom environment file paths via `LEARN_ANYTHING_ENV_PATH`

## Example Outputs

Recent example tutorials generated:
- `kubernetes_tutorial.html` - Interactive Kubernetes learning tutorial
- `tutorial_book-20251027-024212.json` - Structured tutorial data

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure you've installed the package with `pip install -e .`
2. **API Key Issues**: Check that your `.env` file is in the project root and contains valid API keys
3. **Missing Dependencies**: Run `pip install -r requirements.txt` if some dependencies are missing

### Environment Setup

If you encounter issues with the environment configuration:

```bash
# Check current environment
python -c "import learn_anything.llm_config; print(learn_anything.llm_config.get_llm())"

# Verify package installation
python -c "import learn_anything; print(learn_anything.__file__)"
```

## Support and Resources

- **crewAI Documentation**: https://docs.crewai.com
- **crewAI GitHub**: https://github.com/joaomdmoura/crewai
- **LiteLLM Documentation**: https://docs.litellm.ai/ (for LLM configuration)

This project embraces the Single Responsibility Principle (SRP) and provides a minimal CLI for predictable, automated tutorial generation.
