#!/usr/bin/env python3
"""
Serena Agent - Core agent implementation
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field

from sensai.util import logging

from serena.config.context_mode import SerenaAgentContext, SerenaAgentMode
from serena.tools import Tool, ToolRegistry
from serena.util.exception import SerenaException

log = logging.getLogger(__name__)


@dataclass
class SerenaConfig:
    """Configuration for Serena agent."""
    project_path: Optional[str] = None
    context: Optional[SerenaAgentContext] = None
    modes: List[SerenaAgentMode] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)
    settings: Dict[str, Any] = field(default_factory=dict)


class SerenaAgent:
    """Main Serena agent class."""
    
    def __init__(self, config: SerenaConfig):
        """
        Initialize the Serena agent.
        
        :param config: Agent configuration
        """
        self.config = config
        self.project_path = self._resolve_project_path(config.project_path)
        self.context = config.context
        self.modes = config.modes
        self.tool_registry = ToolRegistry()
        
        # Initialize the agent
        self._initialize()
    
    def _resolve_project_path(self, project_path: Optional[str]) -> Optional[Path]:
        """
        Resolve the project path.
        
        :param project_path: Project path string
        :return: Resolved Path object or None
        """
        if not project_path:
            return None
        
        path = Path(project_path)
        if not path.is_absolute():
            path = Path.cwd() / path
        
        return path.resolve()
    
    def _initialize(self) -> None:
        """
        Initialize the agent with tools and configuration.
        """
        log.info(f"Initializing Serena agent for project: {self.project_path}")
        
        # Load tools based on modes
        self._load_tools()
        
        # Apply configuration
        self._apply_configuration()
        
        log.info(f"Agent initialized with {len(self.tool_registry.tools)} tools")
    
    def _load_tools(self) -> None:
        """
        Load tools based on the configured modes.
        """
        # Load default tools
        self._load_default_tools()
        
        # Load mode-specific tools
        for mode in self.modes:
            self._load_mode_tools(mode)
        
        # Load explicitly configured tools
        for tool_name in self.config.tools:
            self._load_tool(tool_name)
    
    def _load_default_tools(self) -> None:
        """
        Load default tools that are always available.
        """
        default_tools = [
            "find_symbol",
            "get_symbols_overview",
            "find_referencing_symbols",
            "search_for_pattern",
            "list_dir",
            "find_file"
        ]
        
        for tool_name in default_tools:
            try:
                self._load_tool(tool_name)
            except Exception as e:
                log.warning(f"Failed to load default tool {tool_name}: {e}")
    
    def _load_mode_tools(self, mode: SerenaAgentMode) -> None:
        """
        Load tools specific to a mode.
        
        :param mode: The mode to load tools for
        """
        mode_tools = {
            "interactive": ["ask_user", "show_message"],
            "editing": ["edit_symbol", "create_file", "delete_file"],
            "analysis": ["analyze_code", "generate_report"],
            "monitoring": ["watch_files", "track_changes"]
        }
        
        tools = mode_tools.get(mode.name, [])
        for tool_name in tools:
            try:
                self._load_tool(tool_name)
            except Exception as e:
                log.warning(f"Failed to load mode tool {tool_name} for mode {mode.name}: {e}")
    
    def _load_tool(self, tool_name: str) -> None:
        """
        Load a specific tool.
        
        :param tool_name: Name of the tool to load
        """
        try:
            tool = self.tool_registry.get_tool(tool_name)
            if tool:
                log.debug(f"Loaded tool: {tool_name}")
            else:
                log.warning(f"Tool not found: {tool_name}")
        except Exception as e:
            log.error(f"Failed to load tool {tool_name}: {e}")
            raise SerenaException(f"Failed to load tool {tool_name}: {e}")
    
    def _apply_configuration(self) -> None:
        """
        Apply agent configuration settings.
        """
        # Apply context settings
        if self.context:
            log.debug(f"Applying context: {self.context.name}")
        
        # Apply mode settings
        for mode in self.modes:
            log.debug(f"Applying mode: {mode.name}")
        
        # Apply custom settings
        for key, value in self.config.settings.items():
            log.debug(f"Applying setting: {key} = {value}")
    
    def get_available_tools(self) -> List[Tool]:
        """
        Get list of available tools.
        
        :return: List of available tools
        """
        return list(self.tool_registry.tools.values())
    
    def execute_tool(self, tool_name: str, **kwargs) -> Any:
        """
        Execute a tool with the given parameters.
        
        :param tool_name: Name of the tool to execute
        :param kwargs: Tool parameters
        :return: Tool execution result
        """
        tool = self.tool_registry.get_tool(tool_name)
        if not tool:
            raise SerenaException(f"Tool not found: {tool_name}")
        
        try:
            log.debug(f"Executing tool: {tool_name} with args: {kwargs}")
            result = tool.execute(self, **kwargs)
            log.debug(f"Tool {tool_name} completed successfully")
            return result
        except Exception as e:
            log.error(f"Tool {tool_name} failed: {e}")
            raise SerenaException(f"Tool {tool_name} failed: {e}")
    
    def get_project_info(self) -> Dict[str, Any]:
        """
        Get information about the current project.
        
        :return: Project information dictionary
        """
        if not self.project_path:
            return {"project_path": None, "exists": False}
        
        return {
            "project_path": str(self.project_path),
            "exists": self.project_path.exists(),
            "is_directory": self.project_path.is_dir(),
            "name": self.project_path.name,
            "parent": str(self.project_path.parent)
        }
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get agent status information.
        
        :return: Status information dictionary
        """
        return {
            "project": self.get_project_info(),
            "context": self.context.name if self.context else None,
            "modes": [mode.name for mode in self.modes],
            "tools_count": len(self.tool_registry.tools),
            "available_tools": [tool.name for tool in self.get_available_tools()]
        }
    
    def shutdown(self) -> None:
        """
        Shutdown the agent and clean up resources.
        """
        log.info("Shutting down Serena agent")
        
        # Clean up tools
        for tool in self.get_available_tools():
            try:
                if hasattr(tool, 'cleanup'):
                    tool.cleanup()
            except Exception as e:
                log.warning(f"Error cleaning up tool {tool.name}: {e}")
        
        log.info("Agent shutdown complete")