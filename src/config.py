"""
Configuration management module for Typecho Markdown Sync Tool.
"""

import json
import os
from typing import Dict, Any
from urllib.parse import urlparse


class Config:
    """Configuration manager for the application."""
    
    def __init__(self, config_path: str = None):
        """
        Initialize configuration.
        
        Args:
            config_path: Path to configuration file. If None, will look for
                        config.json, local_config.json, or use environment variables.
        """
        self.config_path = config_path or self._find_config_file()
        self.config = self._load_config()
    
    def _find_config_file(self) -> str:
        """Find the appropriate configuration file."""
        possible_paths = [
            "config.json",
            "local_config.json",
            os.path.join(os.getcwd(), "config.json"),
            os.path.join(os.getcwd(), "local_config.json")
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        raise FileNotFoundError(
            "No configuration file found. Please create config.json or set environment variables."
        )
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or environment variables."""
        config = {}
        
        # Try to load from file first
        if self.config_path and os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load config file: {e}")
        
        # Override with environment variables
        # config = self._override_with_env(config)
        
        # Validate configuration
        self._validate_config(config)
        
        return config
    
    def _override_with_env(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Override configuration with environment variables."""
        env_mappings = {
            'USERNAME': ('typecho', 'username'),
            'PASSWORD': ('typecho', 'password'),
            'XMLRPC_PHP': ('typecho', 'xmlrpc_php'),
            'QINIU_ACCESS_KEY': ('qiniu', 'access_key'),
            'QINIU_SECRET_KEY': ('qiniu', 'secret_key'),
            'QINIU_BUCKET_NAME': ('qiniu', 'bucket_name'),
            'QINIU_DOMAIN': ('qiniu', 'domain'),
            'QINIU_SHOW': ('qiniu', 'show')
        }
        
        for env_var, (section, key) in env_mappings.items():
            env_value = os.environ.get(env_var)
            if env_value:
                if section not in config:
                    config[section] = {}
                config[section][key] = env_value.strip()
        
        return config
    
    def _validate_config(self, config: Dict[str, Any]) -> None:
        """Validate required configuration fields."""
        required_sections = ['typecho', 'qiniu', 'posts']
        
        for section in required_sections:
            if section not in config:
                raise ValueError(f"Missing required configuration section: {section}")
        
        # Validate Typecho configuration
        typecho_config = config['typecho']
        required_typecho_fields = ['username', 'password', 'xmlrpc_php']
        for field in required_typecho_fields:
            if field not in typecho_config:
                raise ValueError(f"Missing required Typecho configuration: {field}")
        
        # Validate Qiniu configuration
        qiniu_config = config['qiniu']
        required_qiniu_fields = ['access_key', 'secret_key', 'bucket_name', 'domain', 'show']
        for field in required_qiniu_fields:
            if field not in qiniu_config:
                raise ValueError(f"Missing required Qiniu configuration: {field}")
    
    @property
    def typecho(self) -> Dict[str, str]:
        """Get Typecho configuration."""
        return self.config['typecho']
    
    @property
    def qiniu(self) -> Dict[str, str]:
        """Get Qiniu configuration."""
        return self.config['qiniu']
    
    @property
    def posts(self) -> Dict[str, str]:
        """Get posts configuration."""
        return self.config['posts']
    
    def get_domain_name(self) -> str:
        """Extract domain name from XML-RPC URL."""
        url_info = urlparse(self.typecho['xmlrpc_php'])
        return url_info.netloc 