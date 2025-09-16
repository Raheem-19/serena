#!/usr/bin/env python3
"""
Serena Configuration - Configuration management for Serena
"""

import os
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field, asdict

from sensai.util import logging

log = logging.getLogger(__name__)


@dataclass
class SerenaSettings:
    """Global Serena settings."""
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    max_log_files: int = 10
    max_log_size: int = 10 * 1024 * 1024  # 10MB
    cache_dir: Optional[str] = None
    temp_dir: Optional[str] = None
    
    def __post_init__(self):
        if self.cache_dir is None:
            self.cache_dir = str(Path.home() / ".serena" / "cache")
        if self.temp_dir is None:
            self.temp_dir = str(Path.home() / ".serena" / "temp")


@dataclass
class ProjectConfig:
    """Project-specific configuration."""
    name: str
    path: str
    language: Optional[str] = None
    frameworks: List[str] = field(default_factory=list)
    ignore_patterns: List[str] = field(default_factory=lambda: [
        "*.pyc", "__pycache__", ".git", ".svn", "node_modules", ".venv", "venv"
    ])
    include_patterns: List[str] = field(default_factory=lambda: [
        "*.py", "*.js", "*.ts", "*.java", "*.cpp", "*.c", "*.h", "*.cs", "*.go", "*.rs"
    ])
    custom_settings: Dict[str, Any] = field(default_factory=dict)


class ConfigManager:
    """Configuration manager for Serena."""
    
    def __init__(self, config_dir: Optional[str] = None):
        self.config_dir = Path(config_dir) if config_dir else Path.home() / ".serena"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.settings_file = self.config_dir / "settings.json"
        self.projects_file = self.config_dir / "projects.json"
        
        self._settings: Optional[SerenaSettings] = None
        self._projects: Dict[str, ProjectConfig] = {}
        
        self._load_configuration()
    
    def _load_configuration(self) -> None:
        """
        Load configuration from files.
        """
        self._load_settings()
        self._load_projects()
    
    def _load_settings(self) -> None:
        """
        Load global settings.
        """
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r') as f:
                    data = json.load(f)
                self._settings = SerenaSettings(**data)
                log.debug(f"Loaded settings from {self.settings_file}")
            except Exception as e:
                log.warning(f"Failed to load settings: {e}")
                self._settings = SerenaSettings()
        else:
            self._settings = SerenaSettings()
            self._save_settings()
    
    def _load_projects(self) -> None:
        """
        Load project configurations.
        """
        if self.projects_file.exists():
            try:
                with open(self.projects_file, 'r') as f:
                    data = json.load(f)
                self._projects = {
                    name: ProjectConfig(**config) 
                    for name, config in data.items()
                }
                log.debug(f"Loaded {len(self._projects)} projects from {self.projects_file}")
            except Exception as e:
                log.warning(f"Failed to load projects: {e}")
                self._projects = {}
        else:
            self._projects = {}
    
    def _save_settings(self) -> None:
        """
        Save global settings to file.
        """
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(asdict(self._settings), f, indent=2)
            log.debug(f"Saved settings to {self.settings_file}")
        except Exception as e:
            log.error(f"Failed to save settings: {e}")
    
    def _save_projects(self) -> None:
        """
        Save project configurations to file.
        """
        try:
            data = {name: asdict(config) for name, config in self._projects.items()}
            with open(self.projects_file, 'w') as f:
                json.dump(data, f, indent=2)
            log.debug(f"Saved {len(self._projects)} projects to {self.projects_file}")
        except Exception as e:
            log.error(f"Failed to save projects: {e}")
    
    def get_settings(self) -> SerenaSettings:
        """
        Get global settings.
        
        :return: Global settings
        """
        return self._settings
    
    def update_settings(self, **kwargs) -> None:
        """
        Update global settings.
        
        :param kwargs: Settings to update
        """
        for key, value in kwargs.items():
            if hasattr(self._settings, key):
                setattr(self._settings, key, value)
        
        self._save_settings()
    
    def get_project(self, name: str) -> Optional[ProjectConfig]:
        """
        Get project configuration by name.
        
        :param name: Project name
        :return: Project configuration or None
        """
        return self._projects.get(name)
    
    def add_project(self, config: ProjectConfig) -> None:
        """
        Add or update a project configuration.
        
        :param config: Project configuration
        """
        self._projects[config.name] = config
        self._save_projects()
        log.info(f"Added/updated project: {config.name}")
    
    def remove_project(self, name: str) -> bool:
        """
        Remove a project configuration.
        
        :param name: Project name
        :return: True if removed, False if not found
        """
        if name in self._projects:
            del self._projects[name]
            self._save_projects()
            log.info(f"Removed project: {name}")
            return True
        return False
    
    def list_projects(self) -> List[str]:
        """
        List all project names.
        
        :return: List of project names
        """
        return list(self._projects.keys())
    
    def get_project_by_path(self, path: str) -> Optional[ProjectConfig]:
        """
        Get project configuration by path.
        
        :param path: Project path
        :return: Project configuration or None
        """
        path = str(Path(path).resolve())
        for config in self._projects.values():
            if str(Path(config.path).resolve()) == path:
                return config
        return None
    
    def create_project_config(self, name: str, path: str, **kwargs) -> ProjectConfig:
        """
        Create a new project configuration.
        
        :param name: Project name
        :param path: Project path
        :param kwargs: Additional configuration options
        :return: Project configuration
        """
        config = ProjectConfig(name=name, path=path, **kwargs)
        self.add_project(config)
        return config


# Global configuration manager instance
_global_config_manager: Optional[ConfigManager] = None


def get_config_manager() -> ConfigManager:
    """
    Get the global configuration manager.
    
    :return: Global configuration manager instance
    """
    global _global_config_manager
    if _global_config_manager is None:
        _global_config_manager = ConfigManager()
    return _global_config_manager


def get_settings() -> SerenaSettings:
    """
    Get global settings.
    
    :return: Global settings
    """
    return get_config_manager().get_settings()


def get_project(name: str) -> Optional[ProjectConfig]:
    """
    Get project configuration by name.
    
    :param name: Project name
    :return: Project configuration or None
    """
    return get_config_manager().get_project(name)