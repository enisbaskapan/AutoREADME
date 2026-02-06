from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnableConfig
from graph.state import AgentState
from utils.prompt_loader import load_prompt
from agents.agent_handler import create_agent
from tools.github_tools import (
    explore_github_repo,
    get_github_repo_metadata,
    read_github_file,
)
from tools.local_file_tools import explore_directory, read_file, write_readme


def explorer_node(state: AgentState, config: RunnableConfig) -> AgentState:

    setup = config.get("configurable", {})
    provider = setup.get("provider", "groq")
    model = setup.get("model_name", "moonshotai/kimi-k2-instruct-0905")

    explorer_base = load_prompt("explorer", "base")

    if state.get("github_url"):
        tools = [explore_github_repo, get_github_repo_metadata]

        owner = state["github_repo"]["owner"]
        repo = state["github_repo"]["repo"]

        github_instructions = load_prompt("explorer", "github_instructions")
        additional_instructions = github_instructions.format(
            OWNER=owner, REPO=repo, GITHUB_URL=state["github_url"]
        )
    else:
        tools = [explore_directory]

        local_instructions = load_prompt("explorer", "local_instructions")
        additional_instructions = local_instructions.format(
            PROJECT_PATH=state["project_path"]
        )

    agent = create_agent(provider, model, tools)
    instructions = explorer_base.format(ADDITIONAL_INSTRUCTIONS=additional_instructions)
    system_msg = SystemMessage(content=instructions)

    response = agent.invoke([system_msg] + list(state["messages"]))
    return {"messages": [response], "current_agent": "explorer"}


def analyzer_node(state: AgentState, config: RunnableConfig) -> AgentState:

    setup = config.get("configurable", {})
    provider = setup.get("provider", "groq")
    model = setup.get("model_name", "moonshotai/kimi-k2-instruct-0905")

    analyzer_base = load_prompt("analyzer", "base")

    if state.get("github_url"):
        tools = [read_github_file]

        owner = state["github_repo"]["owner"]
        repo = state["github_repo"]["repo"]

        github_instructions = load_prompt("analyzer", "read_github")
        read_instructions = github_instructions.format(OWNER=owner, REPO=repo)
    else:
        tools = [read_file]
        read_instructions = load_prompt("analyzer", "read_local")

    agent = create_agent(provider, model, tools)
    instructions = analyzer_base.format(FILE_READ_INSTRUCTIONS=read_instructions)
    system_msg = SystemMessage(content=instructions)

    response = agent.invoke([system_msg] + list(state["messages"]))
    return {"messages": [response], "current_agent": "analyzer"}


def writer_node(state: AgentState, config: RunnableConfig) -> AgentState:

    setup = config.get("configurable", {})
    provider = setup.get("provider", "groq")
    model = setup.get("model_name", "moonshotai/kimi-k2-instruct-0905")

    writer_base = load_prompt("writer", "base")

    github_context = ""
    if state.get("github_url"):
        github_context = load_prompt("writer", "github_context")

    example_context = ""
    if state.get("example_readme"):
        example_context = load_prompt("writer", "example_readme")

    tools = [write_readme]
    agent = create_agent(provider, model, tools)
    instructions = writer_base.format(
        EXAMPLE_README=example_context,
        GITHUB_CONTEXT=github_context,
        OUTPUT_PATH=state["output_path"],
    )
    system_msg = SystemMessage(content=instructions)

    response = agent.invoke([system_msg] + list(state["messages"]))
    return {"messages": [response], "current_agent": "writer"}
