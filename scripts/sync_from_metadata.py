#!/usr/bin/env python3
"""
Simple script to copy modules from metadata.json and generate mkdocs.yml navigation.
Conversion logic: chapters/CHAPTER_NAME/module.md -> CHAPTER_NAME.md
"""
import json
import shutil
from pathlib import Path

SOURCE_BOOK_DIR = Path("/Users/georgekour/repositories/agentic-patterns-livebook/books/agentic-patterns-principles-practices")
METADATA_FILE = SOURCE_BOOK_DIR / "metadata.json"
TARGET_DOCS_DIR = Path(__file__).parent.parent / "docs"
MKDOCS_FILE = Path(__file__).parent.parent / "mkdocs.yml"

def get_filename_from_path(module_path):
    """Extract filename from path: chapters/CHAPTER_NAME/module.md -> CHAPTER_NAME.md"""
    parts = module_path.split('/')
    if len(parts) >= 2:
        return f"{parts[1]}.md"
    return None

def clean_docs_directory():
    """Delete all existing files from docs directory"""
    if not TARGET_DOCS_DIR.exists():
        return
    
    print("\n[Step 0] Cleaning docs directory...")
    
    deleted_count = 0
    
    # Delete all .md files
    for md_file in TARGET_DOCS_DIR.glob("*.md"):
        md_file.unlink()
        deleted_count += 1
        print(f"  Deleted: {md_file.name}")
    
    # Delete all image files in root
    for ext in ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.svg']:
        for img_file in TARGET_DOCS_DIR.glob(ext):
            img_file.unlink()
            deleted_count += 1
            print(f"  Deleted: {img_file.name}")
    
    # Delete all image files in subdirectories (e.g., figures/)
    for subdir in TARGET_DOCS_DIR.iterdir():
        if subdir.is_dir():
            for ext in ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.svg']:
                for img_file in subdir.glob(ext):
                    img_file.unlink()
                    deleted_count += 1
                    print(f"  Deleted: {subdir.name}/{img_file.name}")
            # Remove empty subdirectories
            try:
                if not any(subdir.iterdir()):
                    subdir.rmdir()
                    print(f"  Removed empty directory: {subdir.name}")
            except OSError:
                pass
    
    if deleted_count == 0:
        print("  (No files to delete)")
    else:
        print(f"  ✓ Deleted {deleted_count} file(s)")

def copy_modules():
    """Copy all module.md files from source to docs"""
    with open(METADATA_FILE, 'r') as f:
        metadata = json.load(f)
    
    TARGET_DOCS_DIR.mkdir(parents=True, exist_ok=True)
    module_mapping = {}
    
    for part in metadata['parts']:
        print(f"\nProcessing Part: {part['title']}")
        
        for module in part['modules']:
            module_path = module.get('path', '')
            if not module_path:
                continue
            
            source_path = SOURCE_BOOK_DIR / module_path
            if not source_path.exists():
                print(f"  Warning: {source_path} does not exist, skipping...")
                continue
            
            # Simple conversion: chapters/NAME/module.md -> NAME.md
            target_filename = get_filename_from_path(module_path)
            if not target_filename:
                continue
            
            target_path = TARGET_DOCS_DIR / target_filename
            
            # Copy file
            shutil.copy2(source_path, target_path)
            print(f"  Copied: {target_filename}")
            
            # Store mapping
            module_mapping[module_path] = target_filename
            
            # Copy images from chapter directory
            chapter_dir = source_path.parent
            
            # Copy images from root of chapter directory
            for ext in ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.svg']:
                for img_file in chapter_dir.glob(ext):
                    shutil.copy2(img_file, TARGET_DOCS_DIR / img_file.name)
                    print(f"    Copied image: {img_file.name}")
            
            # Copy images from subdirectories (e.g., figures/)
            for subdir in chapter_dir.iterdir():
                if subdir.is_dir():
                    target_subdir = TARGET_DOCS_DIR / subdir.name
                    target_subdir.mkdir(parents=True, exist_ok=True)
                    
                    for ext in ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.svg']:
                        for img_file in subdir.glob(ext):
                            shutil.copy2(img_file, target_subdir / img_file.name)
                            print(f"    Copied image: {subdir.name}/{img_file.name}")
    
    # Create index.md from about.md if it exists
    about_path = TARGET_DOCS_DIR / "about.md"
    index_path = TARGET_DOCS_DIR / "index.md"
    if about_path.exists():
        shutil.copy2(about_path, index_path)
        print("  Created: index.md (from about.md)")
    
    print("\n✓ Copy complete!")
    return module_mapping

def generate_nav_structure(module_mapping):
    """Generate navigation structure from metadata.json"""
    with open(METADATA_FILE, 'r') as f:
        metadata = json.load(f)
    
    nav = []
    about_filename = None
    about_title = None
    
    # Find about.md and extract its title
    for part in metadata['parts']:
        for module in part['modules']:
            module_path = module.get('path', '')
            filename = module_mapping.get(module_path)
            
            if filename == 'about.md' and (TARGET_DOCS_DIR / filename).exists():
                about_filename = filename
                about_title = module.get('title', 'About')
                break
        if about_filename:
            break
    
    # Add About as the first item (home page) using index.md
    if about_filename and (TARGET_DOCS_DIR / "index.md").exists():
        nav.append({about_title: "index.md"})
    
    # Process all parts
    for part in metadata['parts']:
        part_items = []
        
        for module in part['modules']:
            module_path = module.get('path', '')
            filename = module_mapping.get(module_path)
            
            # Skip about.md since it's already added as home
            if filename == 'about.md':
                continue
            
            if filename and (TARGET_DOCS_DIR / filename).exists():
                part_items.append({module['title']: filename})
        
        if part_items:
            nav.append({part['title']: part_items})
    
    return nav

def format_nav_yaml(nav_structure):
    """Format navigation as YAML string"""
    lines = []
    
    for item in nav_structure:
        if isinstance(item, dict):
            for key, value in item.items():
                if isinstance(value, list):
                    lines.append(f"- {key}:")
                    for subitem in value:
                        if isinstance(subitem, dict):
                            for subkey, subvalue in subitem.items():
                                needs_quotes = ':' in subkey or '(' in subkey or '&' in subkey or '/' in subkey
                                if needs_quotes:
                                    lines.append(f"    - \"{subkey}\": {subvalue}")
                                else:
                                    lines.append(f"    - {subkey}: {subvalue}")
                else:
                    lines.append(f"- {key}: {value}")
    
    return "\n".join(lines)

def update_mkdocs_yml(module_mapping):
    """Update or create mkdocs.yml navigation section"""
    # Generate nav structure
    new_nav = generate_nav_structure(module_mapping)
    nav_yaml = format_nav_yaml(new_nav)
    
    # Check if mkdocs.yml exists
    if not MKDOCS_FILE.exists():
        # Create a minimal mkdocs.yml with just the nav section
        print(f"  Creating new {MKDOCS_FILE.name}...")
        content = f"site_name: AI Agents: Patterns, Principles & Practices\n\nnav:\n{nav_yaml}\n"
        with open(MKDOCS_FILE, 'w') as f:
            f.write(content)
        print(f"  ✓ Created {MKDOCS_FILE.name}")
        return
    
    # Read existing file
    with open(MKDOCS_FILE, 'r') as f:
        content = f.read()
        lines = content.splitlines(keepends=True)
    
    # Find nav section
    nav_start = None
    for i, line in enumerate(lines):
        if line.strip() == 'nav:' or line.strip().startswith('nav:'):
            nav_start = i
            break
    
    if nav_start is None:
        # No nav section found, append it at the end
        print(f"  Adding nav section to {MKDOCS_FILE.name}...")
        with open(MKDOCS_FILE, 'a') as f:
            f.write(f"\nnav:\n{nav_yaml}\n")
        print(f"  ✓ Added nav section to {MKDOCS_FILE.name}")
        return
    
    # Find end of nav section
    nav_end = len(lines)
    for i in range(nav_start + 1, len(lines)):
        line = lines[i]
        stripped = line.lstrip()
        if stripped and not line.startswith(' ') and not line.startswith('-') and ':' in stripped and not stripped.startswith('#'):
            nav_end = i
            break
    
    # Reconstruct file
    new_lines = lines[:nav_start] + ["nav:\n"] + [nav_yaml + "\n"]
    if nav_end < len(lines):
        new_lines.extend(lines[nav_end:])
    
    # Write back
    with open(MKDOCS_FILE, 'w') as f:
        f.writelines(new_lines)
    
    print(f"  ✓ Updated {MKDOCS_FILE.name}")

def main():
    """Main: delete existing files, copy modules and update mkdocs.yml"""
    print("=" * 60)
    print("Syncing from source: delete → copy → update navigation")
    print("=" * 60)
    
    # Clean existing files
    clean_docs_directory()
    
    # Copy modules
    print("\n[Step 1] Copying module files...")
    module_mapping = copy_modules()
    
    # Update mkdocs.yml
    print("\n[Step 2] Updating mkdocs.yml...")
    update_mkdocs_yml(module_mapping)
    
    print("\n" + "=" * 60)
    print("✓ Complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
