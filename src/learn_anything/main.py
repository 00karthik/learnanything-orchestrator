#!/usr/bin/env python
import argparse
import sys
import os
import json
from datetime import datetime
from learn_anything.crew import ComprehensiveTutorialGeneratorCrew

# Input fields expected by tasks/agents
INPUT_FIELDS = [
    "topic",
    "skill_level",
    "time_commitment",
]


def _prompt_for_inputs(defaults=None):
    """Prompt for all inputs via CLI (interactive)."""
    defaults = defaults or {k: "sample_value" for k in INPUT_FIELDS}
    values = {}
    print("Please provide the following inputs (press Enter to accept defaults):")
    for key in INPUT_FIELDS:
        default = defaults.get(key, "")
        prompt = f"{key.replace('_', ' ').title()} [{default}]: "
        try:
            val = input(prompt).strip()
        except EOFError:
            # Non-interactive environments fall back to defaults
            val = ""
        values[key] = val or default
    return values


def _build_inputs_from_args(args, interactive=False):
    """Build the inputs dict from argparse Namespace, optionally prompting for missing values."""
    inputs = {}
    for field in INPUT_FIELDS:
        inputs[field] = getattr(args, field, None)
    if interactive or any(v in (None, "") for v in inputs.values()):
        # Prompt for any missing/empty values
        defaults = {k: (inputs[k] or "sample_value") for k in INPUT_FIELDS}
        prompted = _prompt_for_inputs(defaults)
        inputs.update(prompted)
    return inputs


def run():
    """Run the crew, prompting for inputs interactively when invoked via console script."""
    inputs = _prompt_for_inputs()
    ComprehensiveTutorialGeneratorCrew().crew().kickoff(inputs=inputs)


def cmd_run(args):
    inputs = _build_inputs_from_args(args, interactive=args.interactive)
    result = ComprehensiveTutorialGeneratorCrew().crew().kickoff(inputs=inputs)
    try:
        _save_outputs_after_run(result, args)
    except Exception as e:
        print(f"Warning: could not save outputs: {e}")


def train():
    """Train via console script with interactive inputs and defaults (iterations=1, filename='train.json')."""
    inputs = _prompt_for_inputs()
    ComprehensiveTutorialGeneratorCrew().crew().train(n_iterations=1, filename="train.json", inputs=inputs)


def cmd_train(args):
    inputs = _build_inputs_from_args(args, interactive=args.interactive)
    try:
        ComprehensiveTutorialGeneratorCrew().crew().train(
            n_iterations=args.iterations,
            filename=args.filename,
            inputs=inputs,
        )
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """Replay via console script is not interactive; provide task_id='1'."""
    ComprehensiveTutorialGeneratorCrew().crew().replay(task_id="1")


def cmd_replay(args):
    try:
        ComprehensiveTutorialGeneratorCrew().crew().replay(task_id=args.task_id)
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """Test via console script with interactive inputs and defaults (iterations=1, model='gpt-4o-mini')."""
    inputs = _prompt_for_inputs()
    ComprehensiveTutorialGeneratorCrew().crew().test(n_iterations=1, openai_model_name="gpt-4o-mini", inputs=inputs)


def cmd_test(args):
    inputs = _build_inputs_from_args(args, interactive=args.interactive)
    try:
        ComprehensiveTutorialGeneratorCrew().crew().test(
            n_iterations=args.iterations,
            openai_model_name=args.model,
            inputs=inputs,
        )
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


def _extract_text_result(result):
    """Best-effort extraction of final textual result from kickoff output.

    Tries common shapes: str, dict-like (final_output/output), list of strings,
    objects with to_json()/model_dump() or attributes.
    """
    if result is None:
        return ""
    # Direct string
    if isinstance(result, str):
        return result
    # Dict-like
    try:
        if isinstance(result, dict):
            for k in ("final_output", "output", "result", "text"):
                if k in result and isinstance(result[k], (str, list, dict)):
                    v = result[k]
                    if isinstance(v, str):
                        return v
                    if isinstance(v, list):
                        return "\n\n".join(map(str, v))
                    return json.dumps(v, indent=2)
    except Exception:
        pass
    # List-like
    try:
        if isinstance(result, list):
            return "\n\n".join(map(str, result))
    except Exception:
        pass
    # Pydantic-like / dataclass-like
    for attr in ("final_output", "output", "result", "text", "content"):
        try:
            v = getattr(result, attr, None)
            if isinstance(v, str):
                return v
        except Exception:
            pass
    # to_json / model_dump
    for meth in ("to_json", "model_dump", "dict"):
        try:
            f = getattr(result, meth, None)
            if callable(f):
                data = f()
                if isinstance(data, str):
                    return data
                return json.dumps(data, indent=2)
        except Exception:
            pass
    # Fallback to repr
    try:
        return repr(result)
    except Exception:
        return ""


def _safe_filename(basename):
    base = basename or "tutorial_book"
    base = base.strip().replace(" ", "_")
    # remove unsafe chars
    return "".join(c for c in base if c.isalnum() or c in ("_", "-")) or "tutorial_book"


def _ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def _save_outputs_after_run(result, args):
    """Save final outputs to JSON for testing purposes."""
    output_dir = getattr(args, "output_dir", None) or os.path.join(os.getcwd(), "outputs")
    topic = getattr(args, "topic", "") or ""
    basename = getattr(args, "output_basename", None) or (topic.strip() or "tutorial_book")
    basename = _safe_filename(basename)

    _ensure_dir(output_dir)

    text = _extract_text_result(result)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    # Always save JSON (only output format supported)
    json_path = os.path.join(output_dir, f"{basename}-{timestamp}.json")
    # If text looks like JSON, try to parse; else wrap in object
    try:
        data = json.loads(text)
    except Exception:
        data = {"content": text}
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Saved JSON to: {json_path}")


def _build_parser():
    parser = argparse.ArgumentParser(description="ComprehensiveTutorialBookGenerator CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Common input args
    def add_common_inputs(sp):
        sp.add_argument("--interactive", action="store_true", help="Prompt for any missing inputs interactively")
        sp.add_argument("--topic")
        sp.add_argument("--skill-level")
        sp.add_argument("--time-commitment")
        # output control
        sp.add_argument("--output-dir", help="Directory to save outputs (default: ./outputs)")
        sp.add_argument("--output-basename", help="Base filename for outputs (default: topic)")

    # run
    sp_run = subparsers.add_parser("run", help="Kick off the crew with provided inputs")
    add_common_inputs(sp_run)

    # train
    sp_train = subparsers.add_parser("train", help="Train the crew")
    sp_train.add_argument("--iterations", type=int, default=1)
    sp_train.add_argument("--filename", type=str, default="train.json")
    add_common_inputs(sp_train)

    # replay
    sp_replay = subparsers.add_parser("replay", help="Replay the crew from a task id")
    sp_replay.add_argument("--task-id", required=True)

    # test
    sp_test = subparsers.add_parser("test", help="Test the crew")
    sp_test.add_argument("--iterations", type=int, default=1)
    sp_test.add_argument("--model", type=str, default="gpt-4o-mini")
    add_common_inputs(sp_test)

    return parser


if __name__ == "__main__":
    parser = _build_parser()
    args = parser.parse_args()

    # Normalize hyphenated args to underscore for inputs mapping
    for k in INPUT_FIELDS:
        v = getattr(args, k.replace("_", "-"), None)
        if v is not None:
            setattr(args, k, v)

    if args.command == "run":
        cmd_run(args)
    elif args.command == "train":
        cmd_train(args)
    elif args.command == "replay":
        cmd_replay(args)
    elif args.command == "test":
        cmd_test(args)
    else:
        print(f"Unknown command: {args.command}")
        sys.exit(1)
