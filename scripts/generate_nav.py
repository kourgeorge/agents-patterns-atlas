#!/usr/bin/env python3
"""
Script to generate MkDocs navigation structure from metadata.json
"""
import json
from pathlib import Path

SOURCE_BOOK_DIR = Path("/Users/georgekour/repositories/agentic-patterns-livebook/books/agentic-patterns-principles-practices")
METADATA_FILE = SOURCE_BOOK_DIR / "metadata.json"
TARGET_DOCS_DIR = Path(__file__).parent.parent / "docs"

def get_safe_filename(module_path):
    """Convert module path to safe filename."""
    # Extract chapter name from path like "chapters/introduction/module.md"
    parts = module_path.split('/')
    if len(parts) >= 2:
        chapter_name = parts[1]
        return f"{chapter_name}.md"
    return "unknown.md"

def generate_nav_structure():
    """Generate navigation structure for mkdocs.yml"""
    with open(METADATA_FILE, 'r') as f:
        metadata = json.load(f)
    
    nav = []
    
    for part in metadata['parts']:
        part_title = part['title']
        part_nav = [part_title]
        
        for module in part['modules']:
            module_path = module['path']
            safe_filename = get_safe_filename(module_path)
            file_path = TARGET_DOCS_DIR / safe_filename
            
            # Check if file exists, if not use the generated filename from setup
            if not file_path.exists():
                # Try to find the actual file
                module_title = module['title']
                # Generate filename similar to setup_content.py
                safe_name = module_title.lower().replace(' ', '-').replace(':', '').replace('(', '').replace(')', '')
                safe_name = ''.join(c for c in safe_name if c.isalnum() or c in ('-', '_'))
                safe_filename = f"{safe_name}.md"
                file_path = TARGET_DOCS_DIR / safe_filename
            
            if file_path.exists():
                part_nav.append({module['title']: safe_filename})
            else:
                print(f"Warning: {file_path} not found for {module['title']}")
        
        nav.append(part_nav)
    
    return nav

if __name__ == "__main__":
    nav = generate_nav_structure()
    print("Navigation structure:")
    print(json.dumps(nav, indent=2))


