# 🤖 AutoREADME

An intelligent multi-agent system that automatically generates comprehensive, professional README files for GitHub repositories and local projects. Powered by advanced AI models and a sophisticated workflow pipeline.

## 🌟 Overview

AutoREADME revolutionizes documentation generation by employing three specialized AI agents that work in concert to analyze your codebase and create detailed README files. Whether you're working with remote GitHub repositories or local projects, this tool automatically detects your tech stack, analyzes dependencies, and generates engaging documentation that truly represents your project.

The system intelligently explores project structures, reads configuration files, analyzes source code, and produces professional README files with installation instructions, usage examples, and comprehensive project documentation - all without manual intervention.

## ✨ Key Features

- **Multi-Agent Intelligence**: Three specialized agents (Explorer, Analyzer, Writer) collaborate for comprehensive analysis
- **GitHub Integration**: Seamlessly analyze remote repositories via GitHub API
- **Local Project Support**: Full support for local project directories
- **Multi-Provider LLM Support**: Compatible with OpenAI and Groq models
- **Smart File Filtering**: Automatically ignores irrelevant files (node_modules, __pycache__, etc.)
- **Tech Stack Detection**: Automatically identifies programming languages and frameworks
- **Dependency Analysis**: Analyzes package.json, requirements.txt, and other config files
- **Customizable Output**: Specify output directory and use example READMEs for styling
- **Professional Formatting**: Generates engaging, well-structured documentation

## 🛠️ Tech Stack

- **Language**: Python 3.8+
- **AI Framework**: LangChain & LangGraph
- **LLM Providers**: OpenAI, Groq
- **GitHub Integration**: PyGithub
- **Configuration**: python-dotenv
- **Workflow**: State-based agent coordination

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/enisbaskapan/AutoREADME.git
cd AutoREADME
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# For OpenAI
export OPENAI_API_KEY="your-openai-api-key"

# For Groq
export GROQ_API_KEY="your-groq-api-key"

# For GitHub access (optional, for private repos)
export GITHUB_TOKEN="your-github-token"
```

## 🚀 Usage

### Basic Usage

Generate a README for a GitHub repository:
```bash
python src/main.py --repo https://github.com/owner/repo-name
```

Generate a README for a local project:
```bash
python src/main.py --repo /path/to/your/project
```

### Advanced Options

```bash
# Use a specific LLM provider and model
python src/main.py --repo https://github.com/owner/repo-name --provider openai --model gpt-4o

# Specify custom output directory
python src/main.py --repo https://github.com/owner/repo-name --output ./docs

# Use an example README for styling
python src/main.py --repo https://github.com/owner/repo-name --example ./example-readme.md

# Adjust recursion limit for complex projects
python src/main.py --repo https://github.com/owner/repo-name --recursion-limit 50
```

### Command Line Arguments

- `--repo`: GitHub URL or local path (required)
- `--provider`: LLM provider (`openai` or `groq`, default: `groq`)
- `--model`: Specific model name
- `--example`: Path to example README for styling
- `--output`: Output directory (default: current directory)
- `--recursion-limit`: Maximum recursion depth (default: 30)

## 📁 Project Structure

```
AutoREADME/
├── src/                          # Source code
│   ├── agents/                  # Agent definitions
│   │   ├── agent_handler.py     # Agent creation utilities
│   │   └── __init__.py
│   ├── graph/                   # LangGraph workflow
│   │   ├── nodes.py             # Agent node definitions
│   │   ├── state.py             # State management
│   │   └── workflow.py            # Workflow orchestration
│   ├── llm/                     # LLM configurations
│   │   └── model.py              # Model provider setup
│   ├── tools/                   # Tool definitions
│   │   ├── github_tools.py      # GitHub API tools
│   │   ├── local_file_tools.py  # Local file system tools
│   │   └── __init__.py
│   ├── utils/                   # Utility functions
│   │   ├── github_repo.py       # GitHub repository wrapper
│   │   ├── prompt_loader.py     # Prompt management
│   │   └── __init__.py
│   └── main.py                  # Entry point
├── data/prompts/                # Agent prompts
│   ├── explorer/                # Explorer agent prompts
│   ├── analyzer/                # Analyzer agent prompts
│   └── writer/                  # Writer agent prompts
└── LICENSE
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file or set these environment variables:

```bash
# LLM Provider (default: groq)
LLM_PROVIDER=groq

# Default model (default: moonshotai/kimi-k2-instruct-0905)
LLM_MODEL=moonshotai/kimi-k2-instruct-0905

# API Keys
OPENAI_API_KEY=your-openai-key
GROQ_API_KEY=your-groq-key

# GitHub token for private repositories
GITHUB_TOKEN=your-github-token
```

### Supported Models

- **OpenAI**: GPT-4, GPT-3.5, and compatible models
- **Groq**: Llama models, Gemma, and other supported models

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- LangChain and LangGraph for the AI framework
- Groq for providing fast LLM inference
- GitHub for the excellent API
- The open-source community for inspiration

## 🔗 Links

- [GitHub Repository](https://github.com/your-username/ai-repo-explorer)
- [Issues](https://github.com/your-username/ai-repo-explorer/issues)
- [Contributors](https://github.com/your-username/ai-repo-explorer/contributors)

---

**Made with ❤️ by the AutoREADME team**