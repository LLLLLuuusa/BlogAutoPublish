"""
Qiniu cloud storage client for image uploads.
"""

import os
import hashlib
from typing import Dict, Any
import qiniu


class QiniuClient:
    """Qiniu cloud storage client."""
    
    def __init__(self, config: Dict[str, str]):
        """
        Initialize Qiniu client.
        
        Args:
            config: Qiniu configuration dictionary
        """
        self.config = config
        self.auth = qiniu.Auth(config['access_key'], config['secret_key'])
    
    def upload_file(self, local_path: str) -> str:
        """
        Upload a file to Qiniu cloud storage.
        
        Args:
            local_path: Local file path to upload
            
        Returns:
            Public URL of the uploaded file
            
        Raises:
            Exception: If upload fails
        """
        if not os.path.exists(local_path):
            raise FileNotFoundError(f"File not found: {local_path}")
        
        key = self._generate_file_key(local_path)
        token = self.auth.upload_token(self.config['bucket_name'], key, 3600)
        
        ret, info = qiniu.put_file(token, key, local_path)
        
        if info.status_code == 200:
            return f"{self.config['show']}/{key}"
        else:
            raise Exception(f"Upload failed: {info}")
    
    def _generate_file_key(self, file_path: str) -> str:
        """
        Generate a unique key for the file based on its content.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Unique file key
        """
        with open(file_path, 'rb') as f:
            data = f.read()
            return hashlib.md5(data).hexdigest() + os.path.splitext(file_path)[1]
    
    def replace_local_images(self, md_content: str, md_file_path: str) -> str:
        """
        Replace local image references with Qiniu URLs.
        
        Args:
            md_content: Markdown content
            md_file_path: Path to the markdown file
            
        Returns:
            Markdown content with replaced image URLs
        """
        import re
        
        dir_path = os.path.dirname(md_file_path)
        
        def replace_image(match):
            alt_text, img_path = match.groups()
            
            # Skip if already a URL
            if img_path.startswith(("http://", "https://")):
                return match.group(0)
            
            full_path = os.path.join(dir_path, img_path)
            if not os.path.exists(full_path):
                print(f"Warning: Image file not found {full_path}")
                return match.group(0)
            
            try:
                qiniu_url = self.upload_file(full_path)
                return f"![{alt_text}]({qiniu_url})"
            except Exception as e:
                print(f"Upload failed for {full_path}: {e}")
                return match.group(0)
        
        # Match ![alt](path) pattern
        return re.sub(r'!\[(.*?)\]\((.*?)\)', replace_image, md_content) 