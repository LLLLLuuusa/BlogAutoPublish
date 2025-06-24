"""
Markdown file processing module.
"""

import os
import frontmatter
from datetime import datetime
from typing import Tuple, Dict, Any, List
from .utils import get_sha1, slugify


class MarkdownProcessor:
    """Markdown file processor."""
    
    def __init__(self, qiniu_client=None):
        """
        Initialize markdown processor.
        
        Args:
            qiniu_client: Optional Qiniu client for image processing
        """
        self.qiniu_client = qiniu_client
    
    def read_markdown_file(self, file_path: str) -> Tuple[str, Dict[str, Any]]:
        """
        Read markdown file and extract content and metadata.
        
        Args:
            file_path: Path to the markdown file
            
        Returns:
            Tuple of (content, metadata)
        """
        try:
            with open(file_path, encoding='utf-8') as f:
                post = frontmatter.load(f)
                content = post.content
                metadata = post.metadata
            
            # Get file modification time
            mod_timestamp = os.path.getmtime(file_path)
            publish_date = datetime.fromtimestamp(mod_timestamp)
            metadata['date'] = publish_date
            
            # Process images if Qiniu client is available
            if self.qiniu_client:
                content = self.qiniu_client.replace_local_images(content, file_path)
            
            return content, metadata
            
        except Exception as e:
            print(f"Error reading markdown file {file_path}: {e}")
            return "", {}
    
    def get_file_slug(self, file_path: str) -> str:
        """
        Generate slug from filename.
        
        Args:
            file_path: Path to the markdown file
            
        Returns:
            Generated slug
        """
        filename = os.path.basename(file_path)
        name_without_ext = os.path.splitext(filename)[0]
        return slugify(name_without_ext)
    
    def get_file_hash(self, file_path: str) -> str:
        """
        Get SHA1 hash of file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            SHA1 hash string
        """
        return get_sha1(file_path)
    
    def validate_metadata(self, metadata: Dict[str, Any], 
                         default_tags: str, default_category: str) -> Dict[str, Any]:
        """
        Validate and fill in missing metadata.
        
        Args:
            metadata: Original metadata
            default_tags: Default tags
            default_category: Default category
            
        Returns:
            Validated metadata
        """
        validated = metadata.copy()
        
        # Ensure required fields exist
        if 'title' not in validated:
            validated['title'] = "Untitled"
        
        if 'tags' not in validated:
            validated['tags'] = [default_tags]
        elif isinstance(validated['tags'], str):
            validated['tags'] = [validated['tags']]
        
        if 'categories' not in validated:
            validated['categories'] = [default_category]
        elif isinstance(validated['categories'], str):
            validated['categories'] = [validated['categories']]
        
        if 'date' not in validated:
            validated['date'] = datetime.now()
        
        return validated
    
    def format_tags(self, tags: List[str]) -> str:
        """
        Format tags list to string.
        
        Args:
            tags: List of tags
            
        Returns:
            Comma-separated tags string
        """
        return ', '.join(tags)
    
    def format_categories(self, categories: List[str]) -> str:
        """
        Format categories list to string.
        
        Args:
            categories: List of categories
            
        Returns:
            Comma-separated categories string
        """
        return ', '.join(categories) 