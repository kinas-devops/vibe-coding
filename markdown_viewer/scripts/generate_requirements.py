#!/usr/bin/env python3
"""
Generate requirements.txt from pyproject.toml
"""

import tomllib
from pathlib import Path

def generate_requirements():
    """Generate requirements.txt from pyproject.toml"""
    
    # Read pyproject.toml
    with open('pyproject.toml', 'rb') as f:
        config = tomllib.load(f)
    
    # Extract dependencies
    dependencies = config.get('project', {}).get('dependencies', [])
    dev_dependencies = config.get('project', {}).get('optional-dependencies', {}).get('dev', [])
    
    # Generate requirements.txt content
    content = [
        "# Generated from pyproject.toml - DO NOT EDIT MANUALLY",
        "# For development, use: pip install -e '.[dev]'",
        "",
        "# Production dependencies"
    ]
    
    # Add production dependencies
    for dep in dependencies:
        content.append(dep)
    
    content.extend([
        "",
        "# Development dependencies (optional)",
        "# To install: pip install -r requirements.txt",
        "# Or better: pip install -e '.[dev]'"
    ])
    
    # Add development dependencies
    for dep in dev_dependencies:
        content.append(f"# {dep}")
    
    # Write requirements.txt
    with open('requirements.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))
    
    print("✅ requirements.txt generated from pyproject.toml")

if __name__ == "__main__":
    generate_requirements()