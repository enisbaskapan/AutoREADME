import json
import os
from langchain_core.tools import tool
from utils.github_repo import GitHubRepo


@tool
def explore_github_repo(owner: str, repo: str) -> str:
    """
    Explore a GitHub repository structure using GitHub API.
    Returns a SUMMARY of structure with important files (not full tree).

    Args:
        owner: GitHub username or organization
        repo: Repository name

    Returns:
        JSON string with structure summary and key files
    """
    try:
        github_token = os.getenv("GITHUB_TOKEN")
        gh_repo = GitHubRepo(owner, repo, github_token)

        tree_data = gh_repo.get_tree(recursive=True)

        if "error" in tree_data:
            return json.dumps({"error": tree_data["error"]})

        IGNORE_PATTERNS = {
            "node_modules",
            ".git",
            "__pycache__",
            "dist",
            "build",
            ".next",
            ".cache",
            "coverage",
            "vendor",
            "target",
            "test",
            "tests",
            "__tests__",
            ".github",
            "docs",
            "examples",
        }

        CONFIG_FILES = {
            "package.json",
            "requirements.txt",
            "pyproject.toml",
            "setup.py",
            "Cargo.toml",
            "go.mod",
            "composer.json",
            "build.gradle",
            "pom.xml",
            "Makefile",
            "Dockerfile",
            "docker-compose.yml",
            "README.md",
            "LICENSE",
            ".env.example",
            "tsconfig.json",
            "setup.cfg",
            "poetry.lock",
            "yarn.lock",
            "package-lock.json",
        }

        SOURCE_EXTENSIONS = {
            ".py",
            ".js",
            ".jsx",
            ".ts",
            ".tsx",
            ".go",
            ".rs",
            ".java",
            ".cpp",
            ".c",
            ".h",
            ".rb",
            ".php",
            ".swift",
            ".kt",
        }

        summary = {
            "total_files": 0,
            "total_dirs": 0,
            "config_files": [],
            "source_files": [],
            "main_directories": {},
            "file_extensions": {},
            "readme_path": None,
            "license_path": None,
        }

        for item in tree_data.get("tree", []):
            path = item["path"]
            path_parts = path.split("/")

            if any(ignored in path_parts for ignored in IGNORE_PATTERNS):
                continue

            if item["type"] == "blob":
                summary["total_files"] += 1
                filename = path_parts[-1]
                file_ext = f".{filename.split('.')[-1]}" if "." in filename else ""

                if filename.lower() in [
                    "readme.md",
                    "readme.rst",
                    "readme.txt",
                    "readme",
                ]:
                    summary["readme_path"] = path

                if filename.lower() in ["license", "license.md", "license.txt"]:
                    summary["license_path"] = path

                if filename in CONFIG_FILES:
                    summary["config_files"].append(path)

                if file_ext in SOURCE_EXTENSIONS:
                    depth = len(path_parts)
                    if depth <= 4:
                        summary["source_files"].append(
                            {
                                "path": path,
                                "depth": depth,
                                "size": item.get("size", 0),
                                "filename": filename,
                            }
                        )

                if "." in filename:
                    ext = filename.split(".")[-1]
                    summary["file_extensions"][ext] = (
                        summary["file_extensions"].get(ext, 0) + 1
                    )

                if len(path_parts) > 1:
                    top_dir = path_parts[0]
                    summary["main_directories"][top_dir] = (
                        summary["main_directories"].get(top_dir, 0) + 1
                    )

            elif item["type"] == "tree":
                summary["total_dirs"] += 1

        summary["source_files"].sort(key=lambda x: (x["depth"], -x["size"]))

        summary["source_files"] = [f["path"] for f in summary["source_files"][:20]]

        top_extensions = sorted(
            summary["file_extensions"].items(), key=lambda x: x[1], reverse=True
        )[:15]
        summary["file_extensions"] = dict(top_extensions)

        top_dirs = sorted(
            summary["main_directories"].items(), key=lambda x: x[1], reverse=True
        )[:10]
        summary["main_directories"] = dict(top_dirs)

        return json.dumps(summary, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})


@tool
def read_github_file(owner: str, repo: str, filepath: str) -> str:
    """
    Read a file from a GitHub repository.

    Args:
        owner: GitHub username or organization
        repo: Repository name
        filepath: Path to file in repository

    Returns:
        File contents as string
    """
    try:
        github_token = os.getenv("GITHUB_TOKEN")
        gh_repo = GitHubRepo(owner, repo, github_token)
        content = gh_repo.get_file_content(filepath)

        if isinstance(content, list):
            file_names = [item.get("name", "unknown") for item in content]
            return (
                f"Error: '{filepath}' is a directory. "
                f"Contents: {', '.join(file_names)}. "
                "Please call read_github_file again with a specific file path."
            )

        if not isinstance(content, (str, bytes)):
            return f"Error: Unexpected data type received: {type(content).__name__}"

        max_chars = 50000
        if len(content) > max_chars:
            content = content[:max_chars] + "\n\n... (truncated)"

        return content

    except Exception as e:
        return f"Error reading file: {str(e)}"


@tool
def get_github_repo_metadata(owner: str, repo: str) -> str:
    """
    Get GitHub repository metadata (stars, description, topics, etc.)

    Args:
        owner: GitHub username or organization
        repo: Repository name

    Returns:
        JSON string of repository metadata
    """
    try:
        github_token = os.getenv("GITHUB_TOKEN")
        gh_repo = GitHubRepo(owner, repo, github_token)
        info = gh_repo.get_repo_info()

        if "error" in info:
            return json.dumps({"error": info["error"]})

        license_info = info.get("license")
        license_name = license_info.get("name") if license_info else "No License"

        # Extract useful metadata
        metadata = {
            "name": info.get("name"),
            "description": info.get("description"),
            "stars": info.get("stargazers_count"),
            "forks": info.get("forks_count"),
            "language": info.get("language"),
            "topics": info.get("topics", []),
            "license": license_name,
            "homepage": info.get("homepage"),
            "created_at": info.get("created_at"),
            "updated_at": info.get("updated_at"),
        }

        return json.dumps(metadata, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})
