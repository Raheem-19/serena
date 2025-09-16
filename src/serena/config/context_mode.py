#!/usr/bin/env python3
"""
Serena Context and Mode Configuration
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field

from sensai.util import logging

log = logging.getLogger(__name__)


@dataclass
class SerenaAgentContext:
    """Agent context configuration."""
    name: str
    description: str = ""
    settings: Dict[str, Any] = field(default_factory=dict)
    tools: List[str] = field(default_factory=list)
    memory_settings: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def load(cls, context: Union[str, 'SerenaAgentContext']) -> 'SerenaAgentContext':
        """
        Load context from string name or return existing context.
        
        :param context: Context name or existing context
        :return: Context instance
        """
        if isinstance(context, cls):
            return context
        
        # Try to load from built-in contexts
        builtin_contexts = {
            "default": cls(
                name="default",
                description="Default context with standard tools",
                tools=["find_symbol", "get_symbols_overview", "search_for_pattern"],
                settings={"max_results": 100, "timeout": 30}
            ),
            "minimal": cls(
                name="minimal",
                description="Minimal context with basic tools only",
                tools=["find_symbol", "search_for_pattern"],
                settings={"max_results": 50, "timeout": 15}
            ),
            "full": cls(
                name="full",
                description="Full context with all available tools",
                tools=[],  # Empty means all tools
                settings={"max_results": 500, "timeout": 60}
            )
        }
        
        if context in builtin_contexts:
            return builtin_contexts[context]
        
        # Try to load from file
        context_file = Path(context)
        if context_file.exists() and context_file.suffix == '.json':
            try:
                with open(context_file, 'r') as f:
                    data = json.load(f)
                return cls(**data)
            except Exception as e:
                log.warning(f"Failed to load context from {context_file}: {e}")
        
        # Default fallback
        log.warning(f"Context '{context}' not found, using default")
        return builtin_contexts["default"]


@dataclass
class SerenaAgentMode:
    """Agent mode configuration."""
    name: str
    description: str = ""
    enabled_tools: List[str] = field(default_factory=list)
    disabled_tools: List[str] = field(default_factory=list)
    settings: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def load(cls, mode: Union[str, 'SerenaAgentMode']) -> 'SerenaAgentMode':
        """
        Load mode from string name or return existing mode.
        
        :param mode: Mode name or existing mode
        :return: Mode instance
        """
        if isinstance(mode, cls):
            return mode
        
        # Try to load from built-in modes
        builtin_modes = {
            "interactive": cls(
                name="interactive",
                description="Interactive mode for user communication",
                enabled_tools=["ask_user", "show_message"],
                settings={"interactive": True, "auto_confirm": False}
            ),
            "editing": cls(
                name="editing",
                description="Editing mode for code modifications",
                enabled_tools=["edit_symbol", "create_file", "delete_file"],
                settings={"backup_files": True, "validate_syntax": True}
            ),
            "analysis": cls(
                name="analysis",
                description="Analysis mode for code inspection",
                enabled_tools=["analyze_code", "generate_report"],
                disabled_tools=["edit_symbol", "create_file", "delete_file"],
                settings={"deep_analysis": True, "generate_metrics": True}
            ),
            "monitoring": cls(
                name="monitoring",
                description="Monitoring mode for watching changes",
                enabled_tools=["watch_files", "track_changes"],
                settings={"watch_interval": 1.0, "auto_refresh": True}
            )
        }
        
        if mode in builtin_modes:
            return builtin_modes[mode]
        
        # Try to load from file
        mode_file = Path(mode)
        if mode_file.exists() and mode_file.suffix == '.json':
            try:
                with open(mode_file, 'r') as f:
                    data = json.load(f)
                return cls(**data)
            except Exception as e:
                log.warning(f"Failed to load mode from {mode_file}: {e}")
        
        # Default fallback
        log.warning(f"Mode '{mode}' not found, using interactive")
        return builtin_modes["interactive"]
    
    def is_tool_enabled(self, tool_name: str) -> bool:
        """
        Check if a tool is enabled in this mode.
        
        :param tool_name: Tool name
        :return: True if enabled, False otherwise
        """
        if tool_name in self.disabled_tools:
            return False
        
        if self.enabled_tools and tool_name not in self.enabled_tools:
            return False
        
        return True
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """
        Get a mode setting.
        
        :param key: Setting key
        :param default: Default value if not found
        :return: Setting value
        """
        return self.settings.get(key, default)


def create_context_file(name: str, context: SerenaAgentContext, output_dir: str = ".") -> Path:
    """
    Create a context configuration file.
    
    :param name: Context name
    :param context: Context configuration
    :param output_dir: Output directory
    :return: Path to created file
    """
    output_path = Path(output_dir) / f"{name}_context.json"
    
    data = {
        "name": context.name,
        "description": context.description,
        "settings": context.settings,
        "tools": context.tools,
        "memory_settings": context.memory_settings
    }
    
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    log.info(f"Created context file: {output_path}")
    return output_path


def create_mode_file(name: str, mode: SerenaAgentMode, output_dir: str = ".") -> Path:
    """
    Create a mode configuration file.
    
    :param name: Mode name
    :param mode: Mode configuration
    :param output_dir: Output directory
    :return: Path to created file
    """
    output_path = Path(output_dir) / f"{name}_mode.json"
    
    data = {
        "name": mode.name,
        "description": mode.description,
        "enabled_tools": mode.enabled_tools,
        "disabled_tools": mode.disabled_tools,
        "settings": mode.settings
    }
    
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    log.info(f"Created mode file: {output_path}")
    return output_path