#!/usr/bin/env python3
"""
Generate a clean project structure tree and save to docs/project_structure.txt
"""

import os
from pathlib import Path
from datetime import datetime

def get_file_size(path):
    """Get human-readable file size"""
    size = path.stat().st_size
    if size < 1024:
        return f"{size}B"
    elif size < 1024 * 1024:
        return f"{size / 1024:.1f}KB"
    else:
        return f"{size / (1024 * 1024):.1f}MB"

def should_include_file(filename, filepath):
    """Determine if a file should be included in the tree"""
    # Always include important files
    important = ['README.md', 'requirements.txt', 'setup.py', '.gitignore', 'Dockerfile', 'docker-compose.yml']
    if filename in important:
        return True
    
    # Include Python files (but not __pycache__)
    if filename.endswith('.py') and '__pycache__' not in str(filepath):
        return True
    
    # Include config files
    if filename.endswith(('.yaml', '.yml', '.json', '.toml', '.cfg', '.ini')):
        return True
    
    # Include shell scripts
    if filename.endswith('.sh'):
        return True
    
    # Include docs
    if filename.endswith(('.md', '.rst', '.txt')):
        return True
    
    # Exclude large binary files
    large_extensions = ['.pyc', '.parquet', '.so', '.dylib', '.pkl', '.joblib']
    for ext in large_extensions:
        if filename.endswith(ext):
            return False
    
    # Exclude venv and cache directories
    exclude_dirs = ['venv', 'venv311', '__pycache__', '.pytest_cache', '.ipynb_checkpoints', 'node_modules']
    for d in exclude_dirs:
        if d in str(filepath):
            return False
    
    return True

def print_tree_to_file(path, file_handle, prefix="", ignore_dirs=None, max_depth=4, current_depth=0):
    """Write project tree to file handle"""
    if ignore_dirs is None:
        ignore_dirs = {'.git', '__pycache__', 'venv', 'venv311', '.idea', '.vscode', '__MACOSX', '.DS_Store', '.pytest_cache', '.ipynb_checkpoints'}
    
    if current_depth > max_depth:
        return
    
    path = Path(path)
    if not path.exists():
        return
    
    items = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name))
    
    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        
        # Skip ignored directories
        if item.is_dir() and item.name in ignore_dirs:
            continue
        
        # For files, check if we should include
        if not item.is_dir() and not should_include_file(item.name, item):
            continue
        
        if item.is_dir():
            file_handle.write(f"{prefix}{'└── ' if is_last else '├── '}{item.name}/\n")
            new_prefix = prefix + ('    ' if is_last else '│   ')
            print_tree_to_file(item, file_handle, new_prefix, ignore_dirs, max_depth, current_depth + 1)
        else:
            size_str = get_file_size(item)
            file_handle.write(f"{prefix}{'└── ' if is_last else '├── '}{item.name} ({size_str})\n")

def main():
    # Create docs directory if it doesn't exist
    docs_dir = Path(__file__).parent
    docs_dir.mkdir(exist_ok=True)
    
    # Get project root (parent of docs)
    project_root = docs_dir.parent
    
    output_file = docs_dir / 'project_structure.txt'
    
    print("="*70)
    print(f"📁 Generating project structure for: {project_root}")
    print("="*70)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write(f"JOB SCAM DETECTOR - PROJECT STRUCTURE\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*70 + "\n\n")
        f.write(f"Root: {project_root}\n\n")
        
        # Write the tree
        print_tree_to_file(project_root, f, max_depth=5)
        
        # Add summary section
        f.write("\n" + "="*70 + "\n")
        f.write("📊 PROJECT SUMMARY\n")
        f.write("="*70 + "\n\n")
        
        # Count files by type
        py_files = list(project_root.rglob("*.py"))
        data_files = list(project_root.rglob("*.csv")) + list(project_root.rglob("*.parquet"))
        model_files = list(project_root.rglob("*.pkl")) + list(project_root.rglob("*.joblib"))
        
        # Filter out venv
        py_files = [f for f in py_files if 'venv' not in str(f) and '__pycache__' not in str(f)]
        data_files = [f for f in data_files if 'venv' not in str(f)]
        model_files = [f for f in model_files if 'venv' not in str(f)]
        
        f.write(f"📄 Python files: {len(py_files)}\n")
        f.write(f"📊 Data files: {len(data_files)}\n")
        f.write(f"🤖 Model files: {len(model_files)}\n")
        
        # Calculate total size of important files (excluding venv)
        total_size = 0
        for file in project_root.rglob("*"):
            if 'venv' not in str(file) and '__pycache__' not in str(file) and file.is_file():
                if should_include_file(file.name, file):
                    total_size += file.stat().st_size
        f.write(f"💾 Total size (excluding venv): {total_size / (1024*1024):.1f}MB\n")
    
    print(f"\n✅ Structure saved to: {output_file}")
    print(f"📏 File size: {get_file_size(output_file)}")
    print("\n📋 Preview:")
    print("-" * 50)
    
    # Print preview to console
    with open(output_file, 'r') as f:
        lines = f.readlines()
        for line in lines[:50]:  # Show first 50 lines
            print(line.rstrip())
        if len(lines) > 50:
            print(f"\n... and {len(lines) - 50} more lines")
    
    print("\n" + "="*70)
    print("✅ Done! Check docs/project_structure.txt")
    print("="*70)

if __name__ == "__main__":
    main()
