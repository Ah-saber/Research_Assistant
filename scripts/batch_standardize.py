#!/usr/bin/env python3
"""
Batch script to add Frontmatter and tags to all markdown files in the 日志 directory.
"""

import os
import re
from datetime import datetime
from pathlib import Path

# Configuration
LOG_DIR = r"C:\Note\MyNote_Obs\日志"

# Tag mapping based on directory structure
TAG_MAPPING = {
    "课业": {
        "base": ["academic", "study"],
        "subdirs": {
            "课程": ["course"],
            "学习笔记": ["notes", "study-notes"],
            "实验考试": ["experiment", "exam", "test"],
            "作业笔记": ["assignment", "homework"],
        }
    },
    "项目": {
        "base": ["project", "research"],
        "subdirs": {
            "比赛": ["competition"],
            "实验室": ["lab", "laboratory"],
            "Robocom": ["robocom", "competition"],
            "大创": ["innovation", "startup"],
            "计设": ["course-design", "design"],
            "项目": ["project"],
        }
    },
    "事务": {
        "base": ["affair", "document"],
        "subdirs": {
            "保研": ["graduate", "application", "recommendation"],
            "发展对象": ["party", "cpc", "development"],
            "事务": ["affair"],
        }
    },
    "杂项": {
        "base": ["misc", "miscellaneous"],
        "subdirs": {
            "TODO": ["todo", "task"],
            "attach": ["attachment", "asset"],
        }
    }
}

# Specific tag mappings for common keywords
KEYWORD_TAGS = {
    # Academic keywords
    "Java": ["Java", "programming"],
    "Linux": ["Linux", "os"],
    "UAV": ["uav", "drone"],
    "人工智能": ["AI", "artificial-intelligence"],
    "移动应用": ["mobile", "app", "development"],
    "算法": ["algorithm"],
    "系统结构": ["computer-architecture"],
    "计组": ["computer-organization", "hardware"],
    "汇编": ["assembly"],
    "操作系统": ["os", "operating-system"],
    "微机原理": ["microcomputer"],
    "数据库": ["database"],
    "编译原理": ["compiler"],
    "深度学习": ["deep-learning", "AI"],
    "数模": ["math-modeling", "competition"],
    "美赛": ["mcm", "competition"],
    "KDD": ["KDD", "conference", "data-mining"],
    "3DGS": ["3DGS", "gaussian-splatting"],
    "3d大赛": ["3d", "competition"],
    "Rebuttal": ["rebuttal", "conference"],
    "Shell": ["shell", "programming"],
    "MVC": ["MVC", "architecture"],
    # Project keywords
    "Robocom": ["robocom", "competition"],
    "宋韵": ["song-culture", "vr"],
    "智海": ["zhilai", "ai"],
    "金融科技": ["fintech", "finance"],
    "丹青衍界": ["danqing", "3d", "chinese-painting"],
    "水下机器人": ["underwater", "robot"],
    "医疗箱": ["medical", "smart-box"],
    "DragonDiffusion": ["diffusion", "image-editing"],
    # Document keywords
    "入党": ["party", "cpc", "application"],
    "答辩": ["defense", "presentation"],
    "简历": ["resume", "cv"],
    "奖学金": ["scholarship", "application"],
    "保研": ["graduate", "recommendation"],
    "面试": ["interview"],
    "周报": ["weekly-report", "lab"],
}


def get_category_from_path(filepath):
    """Determine category from file path."""
    parts = Path(filepath).relative_to(LOG_DIR).parts
    if parts[0] in TAG_MAPPING:
        return parts[0]
    return "杂项"


def get_tags_from_path(filepath):
    """Generate tags based on file path and name."""
    path_obj = Path(filepath).relative_to(LOG_DIR)
    parts = path_obj.parts
    filename = path_obj.stem

    # Start with category base tags
    category = get_category_from_path(filepath)
    tags = TAG_MAPPING[category]["base"].copy()

    # Add subdir tags
    for part in parts[1:]:
        # Check subdir mapping
        for subdir, subdir_tags in TAG_MAPPING[category]["subdirs"].items():
            if subdir in part:
                tags.extend(subdir_tags)

    # Add keyword tags from filename
    for keyword, keyword_tags in KEYWORD_TAGS.items():
        if keyword in filename or keyword in str(path_obj):
            tags.extend(keyword_tags)

    # Remove duplicates and return
    return sorted(list(set(tags)))


def extract_title_from_content(content, filename):
    """Extract title from markdown content or use filename."""
    # Try to find first heading
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return filename


def has_frontmatter(content):
    """Check if file already has frontmatter."""
    return content.startswith("---")


def add_frontmatter(filepath):
    """Add frontmatter to a markdown file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Skip if already has frontmatter
        if has_frontmatter(content):
            print(f"Skip (has frontmatter): {filepath}")
            return False

        # Get file info
        path_obj = Path(filepath)
        filename = path_obj.stem
        category = get_category_from_path(filepath)
        tags = get_tags_from_path(filepath)

        # Get title from content or filename
        title = extract_title_from_content(content, filename)

        # Get file modification time as date
        mtime = os.path.getmtime(filepath)
        file_date = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')

        # Build frontmatter
        frontmatter = f"""---
title: {title}
date: {file_date}
category: {category}
tags: {tags}
---

"""

        # Add frontmatter to content
        new_content = frontmatter + content

        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"Processed: {filepath}")
        return True

    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False


def main():
    """Process all markdown files in the 日志 directory."""
    log_path = Path(LOG_DIR)

    # Find all .md files
    md_files = list(log_path.rglob("*.md"))

    print(f"Found {len(md_files)} markdown files.")
    print("Starting batch processing...")
    print("=" * 60)

    processed = 0
    skipped = 0
    errors = 0

    for filepath in md_files:
        try:
            result = add_frontmatter(filepath)
            if result:
                processed += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"Error: {filepath} - {e}")
            errors += 1

    print("=" * 60)
    print(f"Processing complete!")
    print(f"Processed: {processed}")
    print(f"Skipped (already has frontmatter): {skipped}")
    print(f"Errors: {errors}")


if __name__ == "__main__":
    main()
