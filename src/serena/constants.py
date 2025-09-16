#!/usr/bin/env python3
"""
Serena Constants - Global constants and configuration values
"""

# Version information
SERENA_VERSION = "0.1.4"
SERENA_NAME = "Serena"
SERENA_DESCRIPTION = "AI-powered coding agent toolkit with semantic code retrieval and editing tools"

# Logging configuration
SERENA_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
SERENA_LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Default configuration
DEFAULT_CONTEXT = "default"
DEFAULT_MODES = ["interactive", "editing"]

# File patterns
DEFAULT_IGNORE_PATTERNS = [
    "*.pyc",
    "__pycache__",
    ".git",
    ".svn",
    ".hg",
    "node_modules",
    ".venv",
    "venv",
    ".env",
    "*.log",
    "*.tmp",
    "*.temp",
    ".DS_Store",
    "Thumbs.db",
    "*.swp",
    "*.swo",
    "*~"
]

DEFAULT_INCLUDE_PATTERNS = [
    "*.py",
    "*.js",
    "*.ts",
    "*.jsx",
    "*.tsx",
    "*.java",
    "*.cpp",
    "*.c",
    "*.h",
    "*.hpp",
    "*.cs",
    "*.go",
    "*.rs",
    "*.php",
    "*.rb",
    "*.swift",
    "*.kt",
    "*.scala",
    "*.clj",
    "*.hs",
    "*.ml",
    "*.r",
    "*.m",
    "*.sh",
    "*.bash",
    "*.zsh",
    "*.fish",
    "*.ps1",
    "*.bat",
    "*.cmd",
    "*.html",
    "*.css",
    "*.scss",
    "*.sass",
    "*.less",
    "*.xml",
    "*.json",
    "*.yaml",
    "*.yml",
    "*.toml",
    "*.ini",
    "*.cfg",
    "*.conf",
    "*.md",
    "*.rst",
    "*.txt",
    "*.sql",
    "Dockerfile",
    "Makefile",
    "CMakeLists.txt",
    "*.cmake",
    "*.gradle",
    "*.maven",
    "*.sbt",
    "*.cabal",
    "*.nix"
]

# Language detection patterns
LANGUAGE_PATTERNS = {
    "python": ["*.py", "*.pyw", "*.pyi"],
    "javascript": ["*.js", "*.mjs", "*.cjs"],
    "typescript": ["*.ts", "*.tsx"],
    "java": ["*.java"],
    "cpp": ["*.cpp", "*.cxx", "*.cc", "*.c++"],
    "c": ["*.c"],
    "csharp": ["*.cs"],
    "go": ["*.go"],
    "rust": ["*.rs"],
    "php": ["*.php"],
    "ruby": ["*.rb"],
    "swift": ["*.swift"],
    "kotlin": ["*.kt", "*.kts"],
    "scala": ["*.scala", "*.sc"],
    "clojure": ["*.clj", "*.cljs", "*.cljc"],
    "haskell": ["*.hs", "*.lhs"],
    "ocaml": ["*.ml", "*.mli"],
    "r": ["*.r", "*.R"],
    "matlab": ["*.m"],
    "shell": ["*.sh", "*.bash", "*.zsh", "*.fish"],
    "powershell": ["*.ps1"],
    "batch": ["*.bat", "*.cmd"],
    "html": ["*.html", "*.htm"],
    "css": ["*.css", "*.scss", "*.sass", "*.less"],
    "xml": ["*.xml", "*.xsd", "*.xsl"],
    "json": ["*.json"],
    "yaml": ["*.yaml", "*.yml"],
    "toml": ["*.toml"],
    "ini": ["*.ini", "*.cfg", "*.conf"],
    "markdown": ["*.md", "*.markdown"],
    "restructuredtext": ["*.rst"],
    "sql": ["*.sql"],
    "dockerfile": ["Dockerfile", "*.dockerfile"],
    "makefile": ["Makefile", "*.mk"],
    "cmake": ["CMakeLists.txt", "*.cmake"],
    "gradle": ["*.gradle"],
    "maven": ["pom.xml"],
    "sbt": ["*.sbt"],
    "cabal": ["*.cabal"],
    "nix": ["*.nix"]
}

# Tool categories
TOOL_CATEGORIES = {
    "search": ["find_symbol", "search_for_pattern", "find_file"],
    "analysis": ["get_symbols_overview", "find_referencing_symbols", "analyze_code"],
    "editing": ["edit_symbol", "create_file", "delete_file"],
    "navigation": ["list_dir", "find_file"],
    "reporting": ["generate_report"],
    "interaction": ["ask_user", "show_message"],
    "monitoring": ["watch_files", "track_changes"]
}

# Memory and performance settings
DEFAULT_MEMORY_LIMIT = 512 * 1024 * 1024  # 512MB
DEFAULT_CACHE_SIZE = 100  # Number of cached items
DEFAULT_TIMEOUT = 30  # Seconds
DEFAULT_MAX_RESULTS = 100

# MCP server settings
MCP_SERVER_NAME = "serena"
MCP_SERVER_VERSION = SERENA_VERSION
MCP_SERVER_DESCRIPTION = SERENA_DESCRIPTION

# Dashboard settings
DASHBOARD_HOST = "0.0.0.0"
DASHBOARD_PORT = 24287
DASHBOARD_DEBUG = True

# API endpoints
API_ENDPOINTS = {
    "status": "/api/status",
    "agents": "/api/agents",
    "projects": "/api/projects",
    "logs": "/api/logs",
    "metrics": "/api/metrics"
}

# Error messages
ERROR_MESSAGES = {
    "tool_not_found": "Tool '{tool_name}' not found",
    "invalid_parameters": "Invalid parameters for tool '{tool_name}': {error}",
    "execution_failed": "Tool '{tool_name}' execution failed: {error}",
    "project_not_found": "Project '{project_name}' not found",
    "context_not_found": "Context '{context_name}' not found",
    "mode_not_found": "Mode '{mode_name}' not found",
    "file_not_found": "File '{file_path}' not found",
    "permission_denied": "Permission denied: {operation}",
    "timeout_error": "Operation timed out after {timeout} seconds",
    "memory_error": "Out of memory: {operation}"
}