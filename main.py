#!/usr/bin/env python3
"""
Typecho Markdown Sync Tool

A tool for synchronizing Markdown files with Typecho blog platform.
Supports automatic image upload to Qiniu cloud storage.

Usage:
    python main.py [config_file]
"""

import sys
import argparse
from src.sync_manager import SyncManager


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Synchronize Markdown files with Typecho blog"
    )
    parser.add_argument(
        "config_file",
        nargs="?",
        help="Path to configuration file (optional)"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="Typecho Markdown Sync Tool 1.0.0"
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize sync manager
        sync_manager = SyncManager(args.config_file)
        
        # Start synchronization
        stats = sync_manager.sync_posts()
        
        # Exit with appropriate code
        if stats['failed'] > 0:
            sys.exit(1)
        else:
            sys.exit(0)
            
    except KeyboardInterrupt:
        print("\nSynchronization interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
  
