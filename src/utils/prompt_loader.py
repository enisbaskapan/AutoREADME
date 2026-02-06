import pathlib

BASE_DIR = pathlib.Path(__file__).parent.parent.parent
PROMPTS_DIR = BASE_DIR / "data" / "prompts"


def load_prompt(agent: str, prompt_type: str) -> str:
    prompt_path = PROMPTS_DIR / agent / f"{prompt_type}.md"

    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found at: {prompt_path.absolute()}")

    return prompt_path.read_text(encoding="utf-8")
