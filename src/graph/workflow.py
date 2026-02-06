from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from graph.state import AgentState
from graph.nodes import explorer_node, analyzer_node, writer_node
from tools.github_tools import (
    explore_github_repo,
    read_github_file,
    get_github_repo_metadata,
)
from tools.local_file_tools import explore_directory, read_file, write_readme


workflow = StateGraph(AgentState)

workflow.add_node("explorer", explorer_node)
workflow.add_node("analyzer", analyzer_node)
workflow.add_node("writer", writer_node)

workflow.add_node(
    "explorer_tools",
    ToolNode([explore_github_repo, get_github_repo_metadata, explore_directory]),
)
workflow.add_node("analyzer_tools", ToolNode([read_github_file, read_file]))
workflow.add_node("writer_tools", ToolNode([write_readme]))

workflow.set_entry_point("explorer")

# Explorer loop
workflow.add_conditional_edges(
    "explorer", tools_condition, {"tools": "explorer_tools", "__end__": "analyzer"}
)
workflow.add_edge("explorer_tools", "explorer")

# Analyzer loop
workflow.add_conditional_edges(
    "analyzer", tools_condition, {"tools": "analyzer_tools", "__end__": "writer"}
)
workflow.add_edge("analyzer_tools", "analyzer")

workflow.add_conditional_edges(
    "writer", tools_condition, {"tools": "writer_tools", "__end__": END}
)

app = workflow.compile()
