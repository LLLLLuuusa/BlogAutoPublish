"""
Utility functions for Typecho Markdown Sync Tool.
"""

import os
import re
import json
import hashlib
import urllib.parse
from typing import Dict, List, Any
import pypinyin


def slugify(text: str) -> str:
    """
    Convert Chinese text to URL-friendly slug.
    
    Args:
        text: Input text to convert
        
    Returns:
        URL-friendly slug
    """
    py = pypinyin.lazy_pinyin(text)
    joined = ''.join(py)
    return re.sub(r'[^a-zA-Z0-9\-]', '', joined)


def get_sha1(filename: str) -> str:
    """
    Calculate SHA1 hash of a file.
    
    Args:
        filename: Path to the file
        
    Returns:
        SHA1 hash string
    """
    sha1_obj = hashlib.sha1()
    with open(filename, 'rb') as f:
        sha1_obj.update(f.read())
    return sha1_obj.hexdigest()


def write_dict_to_file(dict_info: Dict[str, Any], file_path: str) -> bool:
    """
    Write dictionary to JSON file.
    
    Args:
        dict_info: Dictionary to write
        file_path: Path to the output file
        
    Returns:
        True if successful
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(dict_info, f, ensure_ascii=False, indent=2)
        return True
    except IOError as e:
        print(f"Error writing to file {file_path}: {e}")
        return False


def read_dict_from_file(file_path: str) -> Dict[str, Any]:
    """
    Read dictionary from JSON file.
    
    Args:
        file_path: Path to the input file
        
    Returns:
        Dictionary from file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error reading from file {file_path}: {e}")
        return {}


def get_markdown_files(directory: str) -> List[str]:
    """
    Get all markdown files in a directory recursively.
    
    Args:
        directory: Directory to search
        
    Returns:
        List of markdown file paths
    """
    md_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))
    return md_files


def ensure_directory_exists(directory: str) -> None:
    """
    Ensure a directory exists, create if it doesn't.
    
    Args:
        directory: Directory path to ensure exists
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe file operations.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove or replace unsafe characters
    unsafe_chars = '<>:"/\\|?*'
    for char in unsafe_chars:
        filename = filename.replace(char, '_')
    return filename


def format_timestamp() -> str:
    """
    Get current timestamp in a formatted string.
    
    Returns:
        Formatted timestamp string
    """
    from datetime import datetime
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S') 