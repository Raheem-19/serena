# Installation Guide

## Prerequisites

- Python 3.11 (required)
- Git
- Node.js (for some language servers)

## Quick Installation

### Using pip

```bash
pip install serena-agent
```

### From Source

```bash
git clone https://github.com/Raheem-19/serena.git
cd serena
pip install -e .
```

## Windows Installation

For Windows users, we provide batch scripts for easy installation:

```batch
# Install Python 3.11 and Serena
install_python_and_serena.bat

# Or if you already have Python 3.11
install_serena.bat
```

## Verification

After installation, verify that Serena is working:

```bash
serena --version
serena-mcp --help
```

## Configuration

1. Create a project configuration:
```bash
serena init
```

2. Configure your MCP client (Claude Desktop, etc.) to use Serena:
```json
{
  "mcpServers": {
    "serena": {
      "command": "serena-mcp",
      "args": ["--project", "/path/to/your/project"]
    }
  }
}
```

## Troubleshooting

If you encounter issues:

1. Ensure Python 3.11 is installed and in your PATH
2. Check that all dependencies are installed
3. Verify your project configuration
4. Check the logs for error messages

For more help, see our [documentation](docs/) or open an issue on GitHub.