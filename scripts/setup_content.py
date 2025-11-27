#!/usr/bin/env python3
"""
Script to copy and organize book content from source to docs directory.
"""
import json
import os
import shutil
from pathlib import Path

SOURCE_BOOK_DIR = Path("/Users/georgekour/repositories/agentic-patterns-livebook/books/agentic-patterns-principles-practices")
TARGET_DOCS_DIR = Path(__file__).parent.parent / "docs"
METADATA_FILE = SOURCE_BOOK_DIR / "metadata.json"

def ensure_dir(path):
    """Ensure directory exists."""
    path.mkdir(parents=True, exist_ok=True)

def copy_file(src, dst):
    """Copy file from source to destination."""
    ensure_dir(dst.parent)
    shutil.copy2(src, dst)
    print(f"Copied: {src} -> {dst}")

def copy_image_if_exists(chapter_dir, target_dir):
    """Copy images from chapter directory if they exist."""
    for ext in ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.svg']:
        for img_file in chapter_dir.glob(ext):
            copy_file(img_file, target_dir / img_file.name)

def main():
    """Main function to organize content."""
    # Read metadata
    with open(METADATA_FILE, 'r') as f:
        metadata = json.load(f)
    
    # Ensure docs directory exists
    ensure_dir(TARGET_DOCS_DIR)
    
    # Copy all markdown files and organize by parts
    for part in metadata['parts']:
        part_title = part['title']
        print(f"\nProcessing Part: {part_title}")
        
        for module in part['modules']:
            source_path = SOURCE_BOOK_DIR / module['path']
            if not source_path.exists():
                print(f"Warning: {source_path} does not exist, skipping...")
                continue
            
            # Create a clean filename from module title
            module_title = module['title']
            # Replace problematic characters for filename
            safe_filename = module_title.lower().replace(' ', '-').replace(':', '').replace('(', '').replace(')', '')
            safe_filename = ''.join(c for c in safe_filename if c.isalnum() or c in ('-', '_'))
            target_path = TARGET_DOCS_DIR / f"{safe_filename}.md"
            
            # Copy markdown file
            copy_file(source_path, target_path)
            
            # Copy images from the chapter directory
            chapter_dir = source_path.parent
            copy_image_if_exists(chapter_dir, TARGET_DOCS_DIR)
    
    # Copy any additional images that might be in subdirectories
    source_chapters_dir = SOURCE_BOOK_DIR / "chapters"
    if source_chapters_dir.exists():
        for chapter_dir in source_chapters_dir.iterdir():
            if chapter_dir.is_dir():
                copy_image_if_exists(chapter_dir, TARGET_DOCS_DIR)
    
    print("\nContent setup complete!")

if __name__ == "__main__":
    main()


