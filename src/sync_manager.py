"""
Synchronization manager for Typecho blog posts.
"""

import os
import re
from datetime import datetime
from typing import Dict, List, Any, Tuple
from .config import Config
from .typecho_client import TypechoClient
from .qiniu_client import QiniuClient
from .markdown_processor import MarkdownProcessor
from .utils import (
    get_markdown_files, write_dict_to_file, read_dict_from_file,
    format_timestamp
)


class SyncManager:
    """Manages synchronization between markdown files and Typecho blog."""
    
    def __init__(self, config_path: str = None):
        """
        Initialize sync manager.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = Config(config_path)
        self.typecho_client = TypechoClient(self.config.typecho)
        self.qiniu_client = QiniuClient(self.config.qiniu)
        self.markdown_processor = MarkdownProcessor(self.qiniu_client)
        self.domain_name = self.config.get_domain_name()
        
        # Statistics
        self.stats = {
            'unchanged': 0,
            'created': 0,
            'updated': 0,
            'failed': 0
        }
    
    def sync_posts(self) -> Dict[str, int]:
        """
        Synchronize markdown files with Typecho blog.
        
        Returns:
            Dictionary with synchronization statistics
        """
        print(f"=== {format_timestamp()} Starting synchronization ===")
        
        # Get existing posts from Typecho
        existing_posts = self._get_existing_posts()
        
        # Get local markdown files
        posts_dir = self.config.posts['directory']
        markdown_files = get_markdown_files(posts_dir)
        
        # Load hash cache
        hash_cache_file = os.path.join(os.getcwd(), ".md_sha1")
        hash_cache = self._load_hash_cache(hash_cache_file)
        
        # Process each markdown file
        successful_files = []
        for md_file in markdown_files:
            try:
                success = self._process_markdown_file(
                    md_file, existing_posts, hash_cache
                )
                if success:
                    successful_files.append(md_file)
            except Exception as e:
                print(f"Error processing {md_file}: {e}")
                self.stats['failed'] += 1
        
        # Update hash cache
        self._update_hash_cache(hash_cache_file, successful_files)
        
        # Update README index
        self._update_readme_index(markdown_files)
        
        # Print statistics
        self._print_statistics()
        
        return self.stats
    
    def _get_existing_posts(self) -> Dict[str, int]:
        """
        Get existing posts from Typecho and create URL to ID mapping.
        
        Returns:
            Dictionary mapping post URLs to post IDs
        """
        posts = self.typecho_client.get_posts()
        url_to_id = {}
        for post in posts:
            url_to_id[post["link"]] = post["id"]
        return url_to_id
    
    def _load_hash_cache(self, cache_file: str) -> Dict[str, Any]:
        """
        Load hash cache from file.
        
        Args:
            cache_file: Path to cache file
            
        Returns:
            Hash cache dictionary
        """
        if os.path.exists(cache_file):
            return read_dict_from_file(cache_file)
        else:
            write_dict_to_file({}, cache_file)
            return {}
    
    def _process_markdown_file(self, md_file: str, existing_posts: Dict[str, int],
                             hash_cache: Dict[str, Any]) -> bool:
        """
        Process a single markdown file.
        
        Args:
            md_file: Path to markdown file
            existing_posts: Dictionary of existing posts
            hash_cache: Hash cache dictionary
            
        Returns:
            True if processing was successful
        """
        # Get file slug and hash
        slug = self.markdown_processor.get_file_slug(md_file)
        current_hash = self.markdown_processor.get_file_hash(md_file)
        
        # Check if file needs synchronization
        if self._is_file_unchanged(slug, current_hash, hash_cache):
            print(f"{md_file} - No changes detected")
            self.stats['unchanged'] += 1
            return True
        
        # Read and process markdown file
        content, metadata = self.markdown_processor.read_markdown_file(md_file)
        if not content:
            print(f"{md_file} - Failed to read content")
            self.stats['failed'] += 1
            return False
        
        # Validate metadata
        validated_metadata = self.markdown_processor.validate_metadata(
            metadata,
            self.config.posts['default_tags'],
            self.config.posts['default_category']
        )
        
        # Prepare post data
        title = validated_metadata['title']
        tags = self.markdown_processor.format_tags(validated_metadata['tags'])
        categories = self.markdown_processor.format_categories(
            validated_metadata['categories']
        )
        date = validated_metadata['date']
        
        # Convert markdown to HTML
        html_content = self.typecho_client.convert_markdown_to_html(content)
        
        # Build post URL
        post_url = self.typecho_client.build_post_url(slug, self.domain_name)
        
        # Create or update post
        success = False
        if post_url in existing_posts:
            # Update existing post
            post_id = existing_posts[post_url]
            success = self.typecho_client.update_post(
                post_id, title, html_content, slug, tags, categories, date
            )
            if success:
                self.stats['updated'] += 1
                print(f"{md_file} - Updated successfully")
            else:
                self.stats['failed'] += 1
                print(f"{md_file} - Update failed")
        else:
            # Create new post
            success = self.typecho_client.create_post(
                title, html_content, slug, tags, categories, date
            )
            if success:
                self.stats['created'] += 1
                print(f"{md_file} - Created successfully")
            else:
                self.stats['failed'] += 1
                print(f"{md_file} - Creation failed")
        
        return success
    
    def _is_file_unchanged(self, slug: str, current_hash: str,
                          hash_cache: Dict[str, Any]) -> bool:
        """
        Check if file has changed based on hash.
        
        Args:
            slug: File slug
            current_hash: Current file hash
            hash_cache: Hash cache dictionary
            
        Returns:
            True if file is unchanged
        """
        return (slug in hash_cache and 
                "hash_value" in hash_cache[slug] and
                current_hash == hash_cache[slug]["hash_value"])
    
    def _update_hash_cache(self, cache_file: str, successful_files: List[str]) -> None:
        """
        Update hash cache with successful files.
        
        Args:
            cache_file: Path to cache file
            successful_files: List of successfully processed files
        """
        hash_cache = {}
        
        for md_file in successful_files:
            slug = self.markdown_processor.get_file_slug(md_file)
            file_hash = self.markdown_processor.get_file_hash(md_file)
            
            hash_cache[slug] = {
                "hash_value": file_hash,
                "file_name": slug,
                "encode_file_name": slug.lower()
            }
        
        hash_cache["update_time"] = format_timestamp()
        write_dict_to_file(hash_cache, cache_file)
        
        print(f"=== {format_timestamp()} Hash cache updated, "
              f"articles count: {len(successful_files)} ===")
    
    def _update_readme_index(self, markdown_files: List[str]) -> None:
        """
        Update README.md with article index.
        
        Args:
            markdown_files: List of markdown files
        """
        print(f"=== {format_timestamp()} Updating README index ===")
        
        readme_path = os.path.join(os.getcwd(), "README.md")
        if not os.path.exists(readme_path):
            print("README.md not found, skipping index update")
            return
        
        # Generate index content
        index_content = self._generate_index_content(markdown_files)
        
        # Update README
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                readme_content = f.read()
            
            # Replace existing index
            pattern = r'---start---(.|\n)*---end---'
            new_content = re.sub(pattern, index_content, readme_content)
            
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"=== {format_timestamp()} README index updated ===")
            
        except Exception as e:
            print(f"Error updating README: {e}")
    
    def _generate_index_content(self, markdown_files: List[str]) -> str:
        """
        Generate index content for README.
        
        Args:
            markdown_files: List of markdown files
            
        Returns:
            Generated index content
        """
        index_lines = [f"---start---"]
        index_lines.append(f"## 目录({datetime.now().strftime('%Y年%m月%d日')}更新)")
        index_lines.append("")
        
        # Sort files by modification time (newest first)
        files_with_time = []
        for md_file in markdown_files:
            mod_time = os.path.getmtime(md_file)
            files_with_time.append((md_file, mod_time))
        
        files_with_time.sort(key=lambda x: x[1], reverse=True)
        
        for md_file, _ in files_with_time:
            try:
                content, metadata = self.markdown_processor.read_markdown_file(md_file)
                title = metadata.get("title", "Untitled")
                slug = self.markdown_processor.get_file_slug(md_file)
                url = f"https://{self.domain_name}/index.php/p/{slug}.html"
                index_lines.append(f"[{title}]({url})")
                index_lines.append("")
            except Exception as e:
                print(f"Error processing {md_file} for index: {e}")
        
        index_lines.append("---end---")
        return "\n".join(index_lines)
    
    def _print_statistics(self) -> None:
        """Print synchronization statistics."""
        print(f"\n=== Synchronization Complete ===")
        print(f"Unchanged: {self.stats['unchanged']}")
        print(f"Created: {self.stats['created']}")
        print(f"Updated: {self.stats['updated']}")
        print(f"Failed: {self.stats['failed']}")
        print(f"Total: {sum(self.stats.values())}") 