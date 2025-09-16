#!/usr/bin/env python3
"""
The Serena Model Context Protocol (MCP) Server
"""

import sys
from abc import abstractmethod
from collections.abc import AsyncIterator, Iterator, Sequence
from contextlib import asynccontextmanager
import functools
from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Literal, cast

import docstring_parser
from mcp.server.fastmcp import server
from mcp.server.fastmcp.server import FastMCP, Settings
from mcp.server.fastmcp.tools.base import Tool as MCPTool
from pydantic_settings import SettingsConfigDict
from sensai.util import logging

from serena.agent import (
    SerenaAgent,
    SerenaConfig,
)
from serena.config.context_mode import SerenaAgentContext, SerenaAgentMode
from serena.constants import DEFAULT_CONTEXT, DEFAULT_MODES, SERENA_LOG_FORMAT
from serena.tools import Tool
from serena.util.exception import show_fatal_exception_safe
from serena.util.logging import MemoryLogHandler

log = logging.getLogger(__name__)


def configure_logging(*args, **kwargs) -> None:  # type: ignore
    """Configure logging for the MCP server."""
    # We only do something here if logging has not yet been configured.
    # Normally, logging is configured in the MCP server startup script.
    if not logging.is_enabled():
        logging.basicConfig(level=logging.INFO, stream=sys.stderr, format=SERENA_LOG_FORMAT)


# patch the logging configuration function in fastmcp, because it's hard-coded and broken
server.configure_logging = configure_logging  # type: ignore


@dataclass
class SerenaMCPRequestContext:
    """Context for MCP requests."""
    agent: SerenaAgent


class SerenaMCPFactory:
    """Factory for creating Serena MCP servers."""
    
    def __init__(self, context: str = DEFAULT_CONTEXT, project: str | None = None):
        """
        Initialize the MCP factory.
        
        :param context: The context name or path to context file
        :param project: Either an absolute path to the project directory or a name of an already registered project.
            If the project passed here hasn't been registered yet, it will be registered automatically and can be activated by its name
            afterward.
        """
        self.context = SerenaAgentContext.load(context)
        self.project = project

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def _sanitize_for_openai_tools(schema_json: str) -> dict:
        """
        Make a Pydantic/JSON Schema object compatible with OpenAI tool schema.
        This method was written by GPT-5, I have not reviewed it in detail.
        Only called when `openai_tool_compatible` is True.
        
        - 'integer' -> 'number' (+ multipleOf: 1)
        - remove 'null' from union type arrays
        - coerce integer-only enums to number
        - best-effort simplify oneOf/anyOf when they only differ by integer/number
        """
        import json

        schema = json.loads(schema_json)
        s = deepcopy(schema)

        def walk(node):  # type: ignore
            if not isinstance(node, dict):
                # lists get handled by parent calls
                return node

            # ---- handle type ----
            t = node.get("type")
            if isinstance(t, str):
                if t == "integer":
                    node["type"] = "number"
                    # preserve existing multipleOf but ensure it's integer-like
                    if "multipleOf" not in node:
                        node["multipleOf"] = 1
            elif isinstance(t, list):
                # remove 'null' (OpenAI tools don't support nullables)
                t2 = [x if x != "integer" else "number" for x in t if x != "null"]
                if not t2:
                    # fall back to object if it somehow becomes empty
                    t2 = ["object"]
                node["type"] = t2[0] if len(t2) == 1 else t2
                if "integer" in t or "number" in t2:
                    # if integers were present, keep integer-like restriction
                    if "multipleOf" not in node:
                        node["multipleOf"] = 1

            # ---- handle enum ----
            enum_vals = node.get("enum")
            if enum_vals and isinstance(enum_vals, list):
                # if all enum values are integers, convert to numbers
                if all(isinstance(v, int) for v in enum_vals):
                    node["enum"] = [float(v) for v in enum_vals]
                    if node.get("type") == "integer":
                        node["type"] = "number"
                        if "multipleOf" not in node:
                            node["multipleOf"] = 1

            # ---- recursively handle nested structures ----
            for key, value in node.items():
                if key in ["properties", "additionalProperties", "items"]:
                    if isinstance(value, dict):
                        walk(value)
                    elif isinstance(value, list):
                        for item in value:
                            walk(item)
                elif key in ["oneOf", "anyOf", "allOf"]:
                    if isinstance(value, list):
                        for item in value:
                            walk(item)
                        # attempt to simplify oneOf/anyOf that only differ by integer/number
                        if key in ["oneOf", "anyOf"] and len(value) == 2:
                            types = [item.get("type") for item in value]
                            if set(types) == {"integer", "number"}:
                                # merge into a single number type
                                merged = deepcopy(value[0])
                                merged["type"] = "number"
                                if "multipleOf" not in merged:
                                    merged["multipleOf"] = 1
                                node.pop(key)
                                node.update(merged)

            return node

        walk(s)
        return s

    def create_mcp_server(
        self,
        name: str = "serena",
        version: str = "0.1.4",
        openai_tool_compatible: bool = False,
    ) -> FastMCP:
        """
        Create an MCP server instance.
        
        :param name: Server name
        :param version: Server version
        :param openai_tool_compatible: Whether to make tools compatible with OpenAI format
        :return: FastMCP server instance
        """
        # Create the agent configuration
        modes = [SerenaAgentMode.load(mode) for mode in DEFAULT_MODES]
        config = SerenaConfig(
            project_path=self.project,
            context=self.context,
            modes=modes
        )
        
        # Create the agent
        agent = SerenaAgent(config)
        
        # Create MCP server
        mcp = FastMCP(
            name=name,
            version=version,
        )
        
        # Register tools
        self._register_tools(mcp, agent, openai_tool_compatible)
        
        return mcp
    
    def _register_tools(self, mcp: FastMCP, agent: SerenaAgent, openai_tool_compatible: bool) -> None:
        """
        Register Serena tools with the MCP server.
        
        :param mcp: The MCP server instance
        :param agent: The Serena agent
        :param openai_tool_compatible: Whether to make tools OpenAI compatible
        """
        # Get all available tools from the agent
        tools = agent.get_available_tools()
        
        for tool in tools:
            # Create MCP tool wrapper
            mcp_tool = self._create_mcp_tool(tool, agent, openai_tool_compatible)
            mcp.register_tool(mcp_tool)
    
    def _create_mcp_tool(self, tool: Tool, agent: SerenaAgent, openai_tool_compatible: bool) -> MCPTool:
        """
        Create an MCP tool wrapper for a Serena tool.
        
        :param tool: The Serena tool
        :param agent: The Serena agent
        :param openai_tool_compatible: Whether to make the tool OpenAI compatible
        :return: MCP tool wrapper
        """
        # Get tool schema
        schema = tool.get_schema()
        
        if openai_tool_compatible:
            schema = self._sanitize_for_openai_tools(schema)
        
        # Create the MCP tool
        @mcp.tool(name=tool.name, description=tool.description)
        async def mcp_tool_wrapper(**kwargs) -> str:
            """MCP tool wrapper."""
            try:
                # Create request context
                context = SerenaMCPRequestContext(agent=agent)
                
                # Execute the tool
                result = await tool.execute(context, **kwargs)
                
                # Return result as string
                if isinstance(result, str):
                    return result
                else:
                    return str(result)
                    
            except Exception as e:
                log.error(f"Error executing tool {tool.name}: {e}")
                return f"Error: {str(e)}"
        
        return mcp_tool_wrapper


def create_mcp_server(
    context: str = DEFAULT_CONTEXT,
    project: str | None = None,
    name: str = "serena",
    version: str = "0.1.4",
    openai_tool_compatible: bool = False,
) -> FastMCP:
    """
    Create a Serena MCP server.
    
    :param context: The context name or path to context file
    :param project: Project directory or name
    :param name: Server name
    :param version: Server version
    :param openai_tool_compatible: Whether to make tools compatible with OpenAI format
    :return: FastMCP server instance
    """
    factory = SerenaMCPFactory(context=context, project=project)
    return factory.create_mcp_server(
        name=name,
        version=version,
        openai_tool_compatible=openai_tool_compatible
    )


if __name__ == "__main__":
    import asyncio
    import argparse
    
    parser = argparse.ArgumentParser(description="Serena MCP Server")
    parser.add_argument("--project", "-p", help="Project directory or name")
    parser.add_argument("--context", "-c", default=DEFAULT_CONTEXT, help="Context configuration")
    parser.add_argument("--name", default="serena", help="Server name")
    parser.add_argument("--version", default="0.1.4", help="Server version")
    parser.add_argument("--openai-compatible", action="store_true", help="Make tools OpenAI compatible")
    
    args = parser.parse_args()
    
    try:
        # Configure logging
        configure_logging()
        
        # Create and run the server
        server = create_mcp_server(
            context=args.context,
            project=args.project,
            name=args.name,
            version=args.version,
            openai_tool_compatible=args.openai_compatible
        )
        
        # Run the server
        asyncio.run(server.run())
        
    except Exception as e:
        show_fatal_exception_safe(e)
        sys.exit(1)