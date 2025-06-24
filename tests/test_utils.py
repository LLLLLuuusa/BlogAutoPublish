"""
Tests for utility functions
"""

import unittest
import tempfile
import os
from src.utils import slugify, get_sha1, write_dict_to_file, read_dict_from_file


class TestUtils(unittest.TestCase):
    """Test utility functions."""
    
    def test_slugify(self):
        """Test slugify function."""
        self.assertEqual(slugify("Hello World"), "HelloWorld")
        self.assertEqual(slugify("你好世界"), "nihao")
        self.assertEqual(slugify("Test-123"), "Test123")
    
    def test_get_sha1(self):
        """Test SHA1 hash function."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("test content")
            temp_file = f.name
        
        try:
            hash_value = get_sha1(temp_file)
            self.assertIsInstance(hash_value, str)
            self.assertEqual(len(hash_value), 40)  # SHA1 is 40 characters
        finally:
            os.unlink(temp_file)
    
    def test_write_and_read_dict(self):
        """Test dictionary file operations."""
        test_data = {"key1": "value1", "key2": 123}
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            temp_file = f.name
        
        try:
            # Test write
            success = write_dict_to_file(test_data, temp_file)
            self.assertTrue(success)
            
            # Test read
            read_data = read_dict_from_file(temp_file)
            self.assertEqual(read_data, test_data)
        finally:
            os.unlink(temp_file)


if __name__ == '__main__':
    unittest.main() 