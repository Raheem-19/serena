<p align="center" style="text-align:center">
  <img src="resources/serena-logo.svg#gh-light-mode-only" style="width:500px">
  <img src="resources/serena-logo-dark-mode.svg#gh-dark-mode-only" style="width:500px">
</p>

* :rocket: Serena is a powerful **coding agent toolkit** capable of turning an LLM into a fully-featured agent that works **directly on your codebase**.
  Unlike most other tools, it is not tied to an LLM, framework or an interface, making it easy to use it in a variety of ways.
* :wrench: Serena provides essential **semantic code retrieval and editing tools** that are akin to an IDE's capabilities, extracting code entities at the symbol level and exploiting relational structure. When combined with an existing coding agent, these tools greatly enhance (token) efficiency.
* :free: Serena is **free & open-source**, enhancing the capabilities of LLMs you already have access to free of charge.

You can think of Serena as providing IDE-like tools to your LLM/coding agent. With it, the agent no longer needs to read entire
files, perform grep-like searches or string replacements to find and edit the right code. Instead, it can use code centered tools like `find_symbol`, `find_referencing_symbols` and `insert_after_symbol`.

<p align="center">
  <em>Serena is under active development! See the latest updates, upcoming features, and lessons learned to stay up to date.</em>
</p>

<p align="center">
  <a href="CHANGELOG.md">
    <img src="https://img.shields.io/badge/Updates-1e293b?style=flat&logo=rss&logoColor=white&labelColor=1e293b" alt="Changelog" />
  </a>
  <a href="roadmap.md">
    <img src="https://img.shields.io/badge/Roadmap-14532d?style=flat&logo=target&logoColor=white&labelColor=14532d" alt="Roadmap" />
  </a>
  <a href="lessons_learned.md">
    <img src="https://img.shields.io/badge/Lessons-Learned-7c4700?style=flat&logo=readthedocs&logoColor=white&labelColor=7c4700" alt="Lessons Learned" />
  </a>
</p>

### LLM Integration

Serena provides the necessary [tools](#list-of-tools) for coding workflows, but an LLM is required to do the actual work,
orchestrating tool use.

For example, **supercharge the performance of Claude Code** with a [one-line shell command](#claude-code).

In general, Serena can be integrated with an LLM in several ways:

* by using the **model context protocol (MCP)**.
  Serena provides an MCP server which integrates with
    * Claude Code and Claude Desktop,
    * Terminal-based clients like Codex, Gemini-CLI, Qwen3-Coder, rovodev, OpenHands CLI and others,
    * IDEs like VSCode, Cursor or IntelliJ,
    * Extensions like Cline or Roo Code
    * Local clients like [OpenWebUI](https://docs.openwebui.com/openapi-servers/mcp), [Jan](https://jan.ai/docs/mcp-examples/browser/browserbase#enable-mcp), [Agno](https://docs.agno.com/introduction/playground) and others
* by using [mcpo to connect it to ChatGPT](docs/serena_on_chatgpt.md) or other clients that don't support MCP but do support tool calling via OpenAPI.
* by incorporating Serena's tools into an agent framework of your choice, as illustrated [here](docs/custom_agent.md).
  Serena's tool implementation is decoupled from the framework-specific code and can thus easily be adapted to any agent framework.

## Installation

Serena can be installed and used in multiple ways depending on your needs and preferences.

### Quick Start

```bash
pip install serena-ai
```

### Development Installation

```bash
git clone https://github.com/Raheem-19/serena.git
cd serena
pip install -e .
```

## Features

- **Semantic Code Analysis**: Advanced code understanding using Language Server Protocol (LSP)
- **Multi-Language Support**: Python, TypeScript, JavaScript, Go, Rust, C/C++, Java, and more
- **MCP Integration**: Model Context Protocol server for seamless LLM integration
- **Dashboard Interface**: Web-based dashboard for monitoring and management
- **Enterprise Features**: Advanced scaling, security, and observability capabilities
- **Extensible Architecture**: Plugin system for custom tools and integrations

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## Support

For support, please check our [documentation](docs/) or open an issue on GitHub.