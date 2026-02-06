import os
import argparse
from dotenv import load_dotenv
from graph.workflow import app
from langchain_core.messages import HumanMessage
from utils.github_repo import parse_github_url


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="AI Repo Explorer")

    parser.add_argument("--repo", required=True, help="GitHub URL or local path")

    parser.add_argument(
        "--provider",
        default=os.getenv("LLM_PROVIDER", "groq"),
        choices=["openai", "groq"],
        help="LLM provider (overrides LLM_PROVIDER env var)",
    )

    parser.add_argument(
        "--model",
        default=os.getenv("LLM_MODEL", "moonshotai/kimi-k2-instruct-0905"),
        help="Specific model name (overrides LLM_MODEL env var)",
    )
    parser.add_argument("--example", help="Path to an example README for style")
    parser.add_argument("--output", default=".", help="Output directory")
    parser.add_argument(
        "--recursion-limit",
        type=int,
        default=30,
        help="Maximum recursion depth for agent interactions",
    )

    args = parser.parse_args()

    is_github = "github.com" in args.repo
    github_url = args.repo if is_github else None
    project_path = args.repo if not is_github else None

    if not project_path and not github_url:
        raise ValueError("Must provide either local project path or valid github url")

    github_repo = None
    if github_url:
        try:
            owner, repo = parse_github_url(github_url)
            github_repo = {"owner": owner, "repo": repo}
            print(f"📦 GitHub Repository: {owner}/{repo}")
        except ValueError as e:
            raise ValueError(f"Invalid GitHub URL: {e}")

    example_readme = ""
    if args.example:
        try:
            with open(args.example, "r", encoding="utf-8") as f:
                example_readme = f.read()
        except Exception as e:
            print(f"⚠️ Could not load example: {e}")

    source_desc = github_url if github_url else project_path
    initial_state = {
        "messages": [
            HumanMessage(content=f"Generate a comprehensive README for: {source_desc}")
        ],
        "project_path": project_path,
        "github_url": github_url,
        "github_repo": github_repo,
        "output_path": args.output,
        "directory_structure": {},
        "key_files": {},
        "tech_stack": [],
        "dependencies": {},
        "project_purpose": "",
        "entry_points": [],
        "repo_metadata": {},
        "example_readme": example_readme,
        "user_preferences": {},
        "readme_sections": {},
        "final_readme": "",
        "current_agent": "explorer",
        "next_agent": "explorer",
        "analysis_complete": False,
        "generation_complete": False,
    }

    config = {
        "configurable": {
            "provider": args.provider,
            "model_name": args.model
            or ("llama-3.3-70b-versatile" if args.provider == "groq" else "gpt-4o"),
        },
        "recursion_limit": args.recursion_limit,
    }

    print(f"\n> Starting README Generation using {args.provider.upper()}...")
    print(f"{'='*70}")

    current_agent = None
    for event in app.stream(initial_state, config=config, stream_mode="updates"):
        for node_name, node_output in event.items():
            if (
                node_name in ["explorer", "analyzer", "writer"]
                and node_name != current_agent
            ):
                current_agent = node_name
                print(f"\n# {node_name.upper()} AGENT ACTIVATED")
                print(f"{'='*70}")

            if "messages" in node_output:
                last_msg = node_output["messages"][-1]

                if hasattr(last_msg, "content") and last_msg.content:
                    if node_name == "writer":
                        content = last_msg.content
                        if len(content) > 200:
                            first_line = (
                                content.split("\n")[0]
                                if "\n" in content
                                else content[:100]
                            )
                            print(f" First Line: {first_line}")
                            print(
                                f"   Generated {len(content)} character README with {content.count('##')} sections"
                            )
                        else:
                            print(f"{content}")
                    else:
                        preview = last_msg.content[:150].replace("\n", " ")
                        print(f"{preview}...")

                if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
                    for tc in last_msg.tool_calls:
                        print(f"   Tool: {tc['name']}")

                        if tc["name"] == "write_readme" and "content" in tc.get(
                            "args", {}
                        ):
                            readme = tc["args"]["content"]
                            title = (
                                readme.split("\n")[0] if "\n" in readme else "README"
                            )
                            print(f"      Title: {title}")
                            print(
                                f"      Stats: {len(readme)} chars, {len(readme.split(chr(10)))} lines"
                            )

    print(f"\n{'='*70}\n✨ README Generation Complete!")


if __name__ == "__main__":
    main()
