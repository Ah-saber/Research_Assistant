#!/usr/bin/env python3
"""
Script to validate and fix Wikilink references in markdown files.
"""

import os
import re
from pathlib import Path

# Configuration
LOG_DIR = r"C:\Note\MyNote_Obs\日志"


def find_all_md_files(log_dir):
    """Find all markdown files in the directory."""
    return list(Path(log_dir).rglob("*.md"))


def find_file_by_name(target_name, all_files):
    """
    Find a file by name using fuzzy matching.
    Returns the actual file path if found, None otherwise.
    """
    # Exact match
    for f in all_files:
        if f.stem == target_name:
            return f

    # Case-insensitive match
    target_lower = target_name.lower()
    for f in all_files:
        if f.stem.lower() == target_lower:
            return f

    # Partial match (for safety)
    for f in all_files:
        if target_lower in f.stem.lower():
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
            actual_file = find_file_by_name(link_target, all_files)

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
            actual_file = find_file_by_name(link_target, all_files)
            if not actual_file:
                broken_links.append(link_target)

        return broken_links

    except Exception as e:
        print(f"Error checking {filepath}: {e}")
        return []


def main():
    """Main function to validate and fix Wikilinks."""
    print("Finding all markdown files...")
    all_files = find_all_md_files(LOG_DIR)
    print(f"Found {len(all_files)} files.")

    print("\nChecking for broken links...")
    all_broken = {}
    total_broken = 0

    for filepath in all_files:
        broken = check_broken_links(filepath, all_files)
        if broken:
            all_broken[str(filepath.relative_to(LOG_DIR))] = broken
            total_broken += len(broken)

    if all_broken:
        print(f"\nFound {total_broken} broken links in {len(all_broken)} files:")
        for file_path, links in all_broken.items():
            print(f"  {file_path}: {', '.join(links)}")

        response = input("\nDo you want to try fixing these links? (y/n): ")
        if response.lower() == 'y':
            print("\nFixing Wikilinks...")
            fixed_files = 0
            total_fixes = 0

            for filepath in all_files:
                modified, count = fix_wikilinks_in_file(filepath, all_files)
                if modified:
                    fixed_files += 1
                    total_fixes += count

            print(f"Fixed {total_fixes} links in {fixed_files} files.")
    else:
        print("No broken links found!")

    print("\nValidating all Wikilinks...")
    print("=" * 60)

    # Second pass to verify all links are valid
    invalid_links = []
    for filepath in all_files:
        broken = check_broken_links(filepath, all_files)
        if broken:
            invalid_links.append((str(filepath.relative_to(LOG_DIR)), broken))

    if invalid_links:
        print(f"\nWarning: {len(invalid_links)} files still have broken links:")
        for file_path, links in invalid_links[:10]:  # Show first 10
            print(f"  {file_path}: {', '.join(links)}")
        if len(invalid_links) > 10:
            print(f"  ... and {len(invalid_links) - 10} more files.")
    else:
        print("All Wikilinks are valid!")

    print("=" * 60)


if __name__ == "__main__":
    main()
