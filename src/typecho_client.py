"""
Typecho blog platform client for post management.
"""

import ssl
import urllib.parse
from datetime import datetime
from typing import Dict, List, Any, Optional
from pytypecho import Typecho, Post
import markdown

from .utils import slugify


class TypechoClient:
    """Typecho blog platform client."""
    
    def __init__(self, config: Dict[str, str]):
        """
        Initialize Typecho client.
        
        Args:
            config: Typecho configuration dictionary
        """
        self.config = config
        self.client = Typecho(
            config['xmlrpc_php'],
            username=config['username'],
            password=config['password'],
            debug=False
        )
        
        # Disable SSL verification for compatibility
        ssl._create_default_https_context = ssl._create_unverified_context
    
    def get_posts(self) -> List[Dict[str, Any]]:
        """
        Get all posts from Typecho.
        
        Returns:
            List of post dictionaries with id and link
        """
        try:
            posts = self.client.get_posts(num=1000)
            post_list = []
            for post in posts:
                post_list.append({
                    "id": post["postid"],
                    "link": post["link"].replace("http://", "https://")
                })
            return post_list
        except Exception as e:
            print(f"Error getting posts: {e}")
            return []
    
    def get_categories(self) -> List[Dict[str, Any]]:
        """
        Get all categories from Typecho.
        
        Returns:
            List of category dictionaries with id, name, and slug
        """
        try:
            categories = self.client.get_categories()
            category_list = []
            for category in categories:
                category_list.append({
                    "id": category["categoryId"],
                    "name": category["categoryName"],
                    "slug": category.get("categorySlug", ""),
                    "description": category.get("categoryDescription", "")
                })
            return category_list
        except Exception as e:
            print(f"Error getting categories: {e}")
            return []
    
    def create_post(self, title: str, content: str, slug: str, 
                   tags: str, category_ids: List[int], date: datetime) -> bool:
        """
        Create a new post.
        
        Args:
            title: Post title
            content: Post content (HTML)
            slug: Post slug
            tags: Post tags
            category_ids: List of category IDs
            date: Post date
            
        Returns:
            True if successful, False otherwise
        """
        try:
            post_obj = self._create_post_object(
                title, content, slug, "publish", tags, category_ids, date
            )
            post_obj.type = 'markdown'
            
            result = self.client.new_post(post_obj, True)
            
            if result and isinstance(result, int):
                print(f"Post created successfully: {result}")
                return True
            else:
                print(f"Post creation failed: {result}")
                return False
                
        except Exception as e:
            print(f"Error creating post: {e}")
            return False
    
    def update_post(self, post_id: int, title: str, content: str, slug: str,
                   tags: str, category_ids: List[int], date: datetime) -> bool:
        """
        Update an existing post.
        
        Args:
            post_id: Post ID to update
            title: Post title
            content: Post content (HTML)
            slug: Post slug
            tags: Post tags
            category_ids: List of category IDs
            date: Post date
            
        Returns:
            True if successful, False otherwise
        """
        try:
            post_obj = self._create_post_object(
                title, content, slug, "publish", tags, category_ids, date
            )
            
            result = self.client.edit_post(post_obj, post_id=post_id, publish=True)
            
            if result and isinstance(result, int) and result == post_id:
                print(f"Post updated successfully: {result}")
                return True
            else:
                print(f"Post update failed: {result}")
                return False
                
        except Exception as e:
            print(f"Error updating post: {e}")
            return False
    
    def _create_post_object(self, title: str, content: str, slug: str,
                          status: str, tags: str, category_ids: List[int], 
                          date: datetime) -> Post:
        """
        Create a Post object for Typecho.
        
        Args:
            title: Post title
            content: Post content
            slug: Post slug
            status: Post status
            tags: Post tags
            category_ids: List of category IDs
            date: Post date
            
        Returns:
            Post object
        """
        post_obj = Post(
            title=title,
            description=content,
            slug=slug,
            post_status=status,
            mt_keywords=tags,
            categories=category_ids,
            dateCreated=date,
        )
        post_obj.__dict__['markdown'] = 1
        return post_obj
    
    def convert_markdown_to_html(self, markdown_content: str) -> str:
        """
        Convert markdown content to HTML.
        
        Args:
            markdown_content: Markdown content
            
        Returns:
            HTML content
        """
        return markdown.markdown(markdown_content)
    
    def build_post_url(self, slug: str, domain: str) -> str:
        """
        Build post URL from slug and domain.
        
        Args:
            slug: Post slug
            domain: Domain name
            
        Returns:
            Complete post URL
        """
        encoded_slug = urllib.parse.quote(slug, safe='').lower()
        return f"https://{domain}/index.php/p/{encoded_slug}.html" 