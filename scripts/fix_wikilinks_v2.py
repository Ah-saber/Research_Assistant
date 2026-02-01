#!/usr/bin/env python3
"""
Script to validate and fix Wikilink references in markdown files v2.
Handles both markdown files and asset files (images, videos, etc.).
"""

import os
import re
from pathlib import Path

# Configuration
LOG_DIR = r"C:\Note\MyNote_Obs\日志"


def find_all_files(log_dir):
    """Find all files (markdown and assets) in the directory."""
    return list(Path(log_dir).rglob("*"))


def find_file_by_name(target_name, all_files, current_file=None):
    """
    Find a file by name using fuzzy matching.
    Returns the actual file path if found, None otherwise.
    """
    # Clean the target name (remove quotes and extra spaces)
    target_name = target_name.strip('"').strip()

    # Exact match
    for f in all_files:
        if f.stem == target_name or f.name == target_name:
            return f

    # Case-insensitive match
    target_lower = target_name.lower()
    for f in all_files:
        if f.stem.lower() == target_lower or f.name.lower() == target_lower:
            return f

    # Check in attach directory for assets
    attach_dir = Path(LOG_DIR) / "杂项" / "attach"
    if attach_dir.exists():
        # Look for exact match in attach
        for f in attach_dir.rglob("*"):
            if f.is_file():
                if f.stem.lower() == target_lower or f.name.lower() == target_lower:
                    return f

    # Partial match (for safety)
    for f in all_files:
        if f.is_file() and (target_lower in f.stem.lower() or target_lower in f.name.lower()):
            return f

    return None


def extract_wikilinks(content):
    """Extract all Wikilinks from markdown content."""
    # Match [[filename]] or [[filename|display]]
    pattern = r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]'
    matches = re.findall(pattern, content)
    return [(m[0].strip(), m[1].strip() if m[1] else None) for m in matches]


def fix_wikilinks_in_file(filepath, all_files):
    """Fix all Wikilinks in a single file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        wikilinks = extract_wikilinks(content)
        if not wikilinks:
            return False, 0

        modified = False
        fix_count = 0

        for link_target, display_text in wikilinks:
            # Skip external links
            if '://' in link_target:
                continue

            # Find the actual file
            actual_file = find_file_by_name(link_target, all_files, filepath)

            if actual_file:
                # Get the relative path from current file to target file
                try:
                    rel_path = os.path.relpath(actual_file, filepath.parent)

                    # Convert to forward slashes for Obsidian
                    rel_path = rel_path.replace('\\', '/')

                    # Build new link
                    if display_text:
                        new_link = f"[[{rel_path}|{display_text}]]"
                    else:
                        # Use filename stem as display text
                        display = actual_file.stem
                        new_link = f"[[{rel_path}|{display}]]"

                    # Replace the old link with new link
                    old_pattern = r'\[\[' + re.escape(link_target) + r'(?:\|[^\]]+)?\]\]'
                    content = re.sub(old_pattern, new_link, content)
                    modified = True
                    fix_count += 1

                except ValueError:
                    # Can't compute relative path (different drives on Windows)
                    pass

        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

        return modified, fix_count

    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False, 0


def check_broken_links(filepath, all_files):
    """Check for broken Wikilinks in a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        wikilinks = extract_wikilinks(content)
        broken_links = []

        for link_target, display_text in wikilinks:
            # Skip external links
            if '://' in link_target:
                continue

            # Check if the linked file exists
            actual_file = find_file_by_name(link_target, all_files, filepath)
            if not actual_file:
                broken_links.append(link_target)

        return broken_links

    except Exception as e:
        print(f"Error checking {filepath}: {e}")
        return []


def main():
    """Main function to validate and fix Wikilinks."""
    print("Finding all files...")
    all_files = find_all_files(LOG_DIR)
    # Filter only actual files
    all_files = [f for f in all_files if f.is_file()]
    print(f"Found {len(all_files)} files.")

    # Find only markdown files for processing
    md_files = [f for f in all_files if f.suffix == '.md']

    print("\nChecking for broken links...")
    all_broken = {}
    total_broken = 0

    for filepath in md_files:
        broken = check_broken_links(filepath, all_files)
        if broken:
            all_broken[str(filepath.relative_to(LOG_DIR))] = broken
            total_broken += len(broken)

    if all_broken:
        print(f"\nFound {total_broken} broken links in {len(all_broken)} files:")
        for file_path, links in list(all_broken.items())[:5]:  # Show first 5
            print(f"  {file_path}: {', '.join(links[:3])}")  # Show first 3 links per file
        if len(all_broken) > 5:
            print(f"  ... and {len(all_broken) - 5} more files.")

        print("\nAttempting to fix broken links...")
        fixed_files = 0
        total_fixes = 0

        for filepath in md_files:
            modified, count = fix_wikilinks_in_file(filepath, all_files)
            if modified:
                fixed_files += 1
                total_fixes += count

        print(f"Fixed {total_fixes} links in {fixed_files} files.")

        # Re-check
        print("\nRe-checking for broken links...")
        all_broken = {}
        for filepath in md_files:
            broken = check_broken_links(filepath, all_files)
            if broken:
                all_broken[str(filepath.relative_to(LOG_DIR))] = broken

        if all_broken:
            print(f"Still {sum(len(v) for v in all_broken.values())} broken links in {len(all_broken)} files:")
            for file_path, links in list(all_broken.items())[:5]:
                print(f"  {file_path}: {', '.join(links[:3])}")
            if len(all_broken) > 5:
                print(f"  ... and {len(all_broken) - 5} more files.")
            print("\nNote: Some broken links may be due to:")
            print("  - Files that were deleted or moved outside the vault")
            print("  - Links to external resources")
            print("  - Malformed link syntax")
        else:
            print("All links fixed successfully!")
    else:
        print("No broken links found!")

    print("\n" + "=" * 60)
    print("Summary:")
    print(f"Total markdown files: {len(md_files)}")
    print(f"Total files (including assets): {len(all_files)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
