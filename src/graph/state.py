import operator

from typing import TypedDict, Annotated, Sequence, Optional
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    """Shared state across all specialized agents"""

    messages: Annotated[Sequence[BaseMessage], operator.add]

    # Source information
    project_path: Optional[str]  # For local projects
    github_url: Optional[str]  # For GitHub projects
    github_repo: Optional[dict]  # GitHubRepo helper instance data
    output_path: str  # Where to save README

    # Analysis phase outputs
    directory_structure: dict
    key_files: dict
    tech_stack: list
    dependencies: dict
    project_purpose: str
    entry_points: list
    repo_metadata: dict  # GitHub stars, description, etc.

    # User customization
    example_readme: str
    user_preferences: dict

    # Generation phase
    readme_sections: dict
    final_readme: str

    # Control flow
    current_agent: str
    next_agent: str
    analysis_complete: bool
    generation_complete: bool
