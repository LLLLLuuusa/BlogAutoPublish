#!/usr/bin/env python3
"""
Setup script for Typecho Markdown Sync Tool
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="typecho-markdown-sync",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool for synchronizing Markdown files with Typecho blog platform",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/typecho-markdown-sync",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Content Management System",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "typecho-sync=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="typecho, markdown, blog, sync, qiniu",
    project_urls={
        "Bug Reports": "https://github.com/your-username/typecho-markdown-sync/issues",
        "Source": "https://github.com/your-username/typecho-markdown-sync",
        "Documentation": "https://github.com/your-username/typecho-markdown-sync#readme",
    },
) 