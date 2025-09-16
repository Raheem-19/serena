#!/usr/bin/env python3
"""
Serena Tools - Tool registry and base classes
"""

import inspect
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type, Union
from dataclasses import dataclass

from sensai.util import logging

log = logging.getLogger(__name__)


@dataclass
class ToolParameter:
    """Tool parameter definition."""
    name: str
    type: Type
    description: str
    required: bool = True
    default: Any = None


class Tool(ABC):
    """Base class for all Serena tools."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self._parameters: List[ToolParameter] = []
    
    @abstractmethod
    async def execute(self, context: Any, **kwargs) -> Any:
        """
        Execute the tool with the given context and parameters.
        
        :param context: Execution context
        :param kwargs: Tool parameters
        :return: Tool execution result
        """
        pass
    
    def add_parameter(self, param: ToolParameter) -> None:
        """
        Add a parameter to the tool.
        
        :param param: Parameter to add
        """
        self._parameters.append(param)
    
    def get_parameters(self) -> List[ToolParameter]:
        """
        Get tool parameters.
        
        :return: List of tool parameters
        """
        return self._parameters.copy()
    
    def get_schema(self) -> str:
        """
        Get tool schema as JSON string.
        
        :return: JSON schema string
        """
        import json
        
        schema = {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
        
        for param in self._parameters:
            schema["parameters"]["properties"][param.name] = {
                "type": self._get_json_type(param.type),
                "description": param.description
            }
            
            if param.required:
                schema["parameters"]["required"].append(param.name)
        
        return json.dumps(schema)
    
    def _get_json_type(self, python_type: Type) -> str:
        """
        Convert Python type to JSON schema type.
        
        :param python_type: Python type
        :return: JSON schema type string
        """
        type_mapping = {
            str: "string",
            int: "integer",
            float: "number",
            bool: "boolean",
            list: "array",
            dict: "object"
        }
        
        return type_mapping.get(python_type, "string")
    
    def validate_parameters(self, **kwargs) -> Dict[str, Any]:
        """
        Validate and process tool parameters.
        
        :param kwargs: Input parameters
        :return: Validated parameters
        :raises ValueError: If validation fails
        """
        validated = {}
        
        for param in self._parameters:
            if param.name in kwargs:
                value = kwargs[param.name]
                # Basic type checking
                if not isinstance(value, param.type):
                    try:
                        value = param.type(value)
                    except (ValueError, TypeError):
                        raise ValueError(f"Parameter {param.name} must be of type {param.type.__name__}")
                validated[param.name] = value
            elif param.required:
                if param.default is not None:
                    validated[param.name] = param.default
                else:
                    raise ValueError(f"Required parameter {param.name} is missing")
            elif param.default is not None:
                validated[param.name] = param.default
        
        return validated


class ToolRegistry:
    """Registry for managing tools."""
    
    def __init__(self):
        self.tools: Dict[str, Tool] = {}
        self._load_builtin_tools()
    
    def _load_builtin_tools(self) -> None:
        """
        Load built-in tools.
        """
        # This would load actual tool implementations
        # For now, we'll create placeholder tools
        
        builtin_tools = [
            ("find_symbol", "Find symbols in the codebase"),
            ("get_symbols_overview", "Get overview of symbols in a file"),
            ("find_referencing_symbols", "Find symbols that reference a given symbol"),
            ("search_for_pattern", "Search for patterns in the codebase"),
            ("list_dir", "List directory contents"),
            ("find_file", "Find files in the project"),
            ("edit_symbol", "Edit a symbol in the codebase"),
            ("create_file", "Create a new file"),
            ("delete_file", "Delete a file"),
            ("analyze_code", "Analyze code quality and structure"),
            ("generate_report", "Generate analysis reports")
        ]
        
        for name, description in builtin_tools:
            tool = PlaceholderTool(name, description)
            self.register_tool(tool)
    
    def register_tool(self, tool: Tool) -> None:
        """
        Register a tool.
        
        :param tool: Tool to register
        """
        self.tools[tool.name] = tool
        log.debug(f"Registered tool: {tool.name}")
    
    def unregister_tool(self, name: str) -> None:
        """
        Unregister a tool.
        
        :param name: Name of tool to unregister
        """
        if name in self.tools:
            del self.tools[name]
            log.debug(f"Unregistered tool: {name}")
    
    def get_tool(self, name: str) -> Optional[Tool]:
        """
        Get a tool by name.
        
        :param name: Tool name
        :return: Tool instance or None
        """
        return self.tools.get(name)
    
    def list_tools(self) -> List[str]:
        """
        List all registered tool names.
        
        :return: List of tool names
        """
        return list(self.tools.keys())
    
    def get_tools_by_category(self, category: str) -> List[Tool]:
        """
        Get tools by category.
        
        :param category: Tool category
        :return: List of tools in the category
        """
        # This would filter tools by category if they had category metadata
        return list(self.tools.values())


class PlaceholderTool(Tool):
    """Placeholder tool for demonstration purposes."""
    
    def __init__(self, name: str, description: str):
        super().__init__(name, description)
        
        # Add some common parameters
        self.add_parameter(ToolParameter(
            name="query",
            type=str,
            description="Query or search term",
            required=False,
            default=""
        ))
        
        self.add_parameter(ToolParameter(
            name="path",
            type=str,
            description="File or directory path",
            required=False,
            default="."
        ))
    
    async def execute(self, context: Any, **kwargs) -> str:
        """
        Execute the placeholder tool.
        
        :param context: Execution context
        :param kwargs: Tool parameters
        :return: Placeholder result
        """
        validated_params = self.validate_parameters(**kwargs)
        
        return f"Placeholder tool '{self.name}' executed with parameters: {validated_params}"


# Global tool registry instance
_global_registry = ToolRegistry()


def get_global_registry() -> ToolRegistry:
    """
    Get the global tool registry.
    
    :return: Global tool registry instance
    """
    return _global_registry


def register_tool(tool: Tool) -> None:
    """
    Register a tool in the global registry.
    
    :param tool: Tool to register
    """
    _global_registry.register_tool(tool)


def get_tool(name: str) -> Optional[Tool]:
    """
    Get a tool from the global registry.
    
    :param name: Tool name
    :return: Tool instance or None
    """
    return _global_registry.get_tool(name)