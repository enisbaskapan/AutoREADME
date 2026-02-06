import json
from pathlib import Path
from langchain_core.tools import tool


@tool
def explore_directory(path: str, max_depth: int = 3) -> str:
    """Explore local directory structure (original tool)"""
    IGNORE_DIRS = {
        "node_modules",
        ".git",
        "__pycache__",
        ".venv",
        "venv",
        "dist",
        "build",
        ".next",
        ".cache",
        "coverage",
        ".pytest_cache",
    }

    def _explore(current_path: Path, current_depth: int = 0) -> dict:
        if current_depth > max_depth:
            return {}

        result = {"type": "directory", "children": {}}

        try:
            for item in sorted(current_path.iterdir()):
                if item.name.startswith(".") or item.name in IGNORE_DIRS:
                    continue

                if item.is_dir():
                    result["children"][item.name] = _explore(item, current_depth + 1)
                else:
                    result["children"][item.name] = {
                        "type": "file",
                        "size": item.stat().st_size,
                    }
        except PermissionError:
            result["error"] = "Permission denied"

        return result

    path_obj = Path(path).resolve()
    if not path_obj.exists():
        return json.dumps({"error": f"Path does not exist: {path}"})

    structure = _explore(path_obj)
    return json.dumps(structure, indent=2)


@tool
def read_file(filepath: str, max_lines: int = 500) -> str:
    """Read local file (original tool)"""
    try:
        path = Path(filepath).resolve()
        if not path.exists():
            return f"Error: File not found: {filepath}"

        if path.stat().st_size > 1_000_000:
            return f"Error: File too large (>1MB): {filepath}"

        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            lines = []
            for i, line in enumerate(f):
                if i >= max_lines:
                    lines.append(f"\n... (truncated after {max_lines} lines)")
                    break
                lines.append(line)
            return "".join(lines)

    except Exception as e:
        return f"Error reading file: {str(e)}"


@tool
def write_readme(content: str, output_path: str) -> str:
    """Write README to file"""
    try:
        dir_path = Path(output_path)
        if dir_path.is_file():
            dir_path = dir_path.parent

        readme_path = dir_path / "README.md"
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote README to {readme_path}"
    except Exception as e:
        return f"Error writing README: {str(e)}"
