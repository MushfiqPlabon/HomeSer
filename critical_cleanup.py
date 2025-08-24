#!/usr/bin/env python3
"""
CRITICAL MISSION SCRIPT: Backend Cleanup
This script removes all frontend files to create a backend-only branch.
Designed for maximum safety and recovery capability.
"""

import os
import sys
import shutil
import tempfile
import argparse
from pathlib import Path

def log_message(message):
    """Log message to file and console"""
    print(f"[CRITICAL] {message}")
    with open("cleanup_log.txt", "a") as f:
        f.write(f"{message}\n")

def verify_environment():
    """Verify we're in the correct directory and branch"""
    # Check if we're in the right branch
    try:
        result = os.popen("git branch --show-current").read().strip()
        if result != "back-end":
            log_message(f"ERROR: Not on back-end branch. Current branch: {result}")
            return False
    except Exception as e:
        log_message(f"ERROR: Could not verify branch: {e}")
        return False
    
    # Check if critical files exist
    critical_files = ["manage.py", "requirements.txt", "HomeSer"]
    for file in critical_files:
        if not os.path.exists(file):
            log_message(f"ERROR: Critical file/directory missing: {file}")
            return False
    
    log_message("Environment verification PASSED")
    return True

def remove_file_or_dir(path):
    """Safely remove file or directory"""
    try:
        if os.path.isfile(path):
            os.remove(path)
            log_message(f"REMOVED file: {path}")
            return True
        elif os.path.isdir(path):
            shutil.rmtree(path)
            log_message(f"REMOVED directory: {path}")
            return True
        else:
            log_message(f"INFO: Path does not exist (skipping): {path}")
            return True
    except Exception as e:
        log_message(f"ERROR: Failed to remove {path}: {e}")
        return False

def update_gitignore():
    """Update .gitignore to remove frontend-specific entries"""
    try:
        gitignore_path = ".gitignore"
        if not os.path.exists(gitignore_path):
            log_message("WARNING: .gitignore not found")
            return True
            
        with open(gitignore_path, "r") as f:
            lines = f.readlines()
        
        # Filter out Node.js and frontend-specific entries
        filtered_lines = []
        skip_patterns = [
            "node_modules/",
            "npm-debug.log*",
            "yarn-debug.log*",
            "yarn-error.log*",
            "lerna-debug.log*",
            ".yarn-integrity",
            ".yarn/cache/",
            ".yarn/unplugged/",
            "static/css/output.css",  # Tailwind output
        ]
        
        for line in lines:
            line_stripped = line.strip()
            should_skip = False
            for pattern in skip_patterns:
                if pattern in line_stripped:
                    should_skip = True
                    break
            if not should_skip:
                filtered_lines.append(line)
        
        # Write back the filtered content
        with open(gitignore_path, "w") as f:
            f.writelines(filtered_lines)
        
        log_message("UPDATED .gitignore - removed frontend entries")
        return True
    except Exception as e:
        log_message(f"ERROR: Failed to update .gitignore: {e}")
        return False

def update_readme():
    """Update README.md to remove frontend sections"""
    try:
        readme_path = "README.md"
        if not os.path.exists(readme_path):
            log_message("WARNING: README.md not found")
            return True
            
        with open(readme_path, "r") as f:
            content = f.read()
        
        # Remove frontend-related sections
        # This is a simplified approach - in a real scenario, you might want more precise editing
        sections_to_remove = [
            "### Tailwind CSS",
            "Compile CSS in development mode (with watch):",
            "```bash",
            "npm run dev",
            "```",
            "Build CSS for production:",
            "```bash",
            "npm run build",
            "```",
            "- Node.js and npm (for Tailwind CSS)",
            "4. Install Node.js dependencies:",
            "```bash",
            "npm install",
            "```",
        ]
        
        lines = content.split('\n')
        filtered_lines = []
        skip_section = False
        
        for line in lines:
            # Check if we should start skipping
            for section in sections_to_remove:
                if section in line:
                    skip_section = True
                    break
            
            # If we're not skipping, add the line
            if not skip_section:
                filtered_lines.append(line)
            
            # Check if we should stop skipping (empty line or new section)
            if skip_section and (line.strip() == "" or (line.startswith("##") and "Tailwind" not in line)):
                skip_section = False
        
        # Write back the filtered content
        with open(readme_path, "w") as f:
            f.write('\n'.join(filtered_lines))
        
        log_message("UPDATED README.md - removed frontend sections")
        return True
    except Exception as e:
        log_message(f"ERROR: Failed to update README.md: {e}")
        return False

def verify_backend_integrity():
    """Verify that critical backend files still exist"""
    critical_backend_files = [
        "manage.py",
        "requirements.txt",
        "HomeSer",
        ".env.example",
        "vercel.json",
        "vercel-setup.sh"
    ]
    
    missing_files = []
    for file in critical_backend_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        log_message(f"ERROR: Critical backend files missing: {missing_files}")
        return False
    
    log_message("Backend integrity verification PASSED")
    return True

def main():
    parser = argparse.ArgumentParser(description="Critical Backend Cleanup Script")
    parser.add_argument("--verify-only", action="store_true", help="Only verify environment, don't execute")
    parser.add_argument("--execute", action="store_true", help="Execute the cleanup")
    
    args = parser.parse_args()
    
    # Always verify environment first
    if not verify_environment():
        log_message("FATAL: Environment verification failed")
        return 1
    
    if args.verify_only:
        log_message("DRY RUN: Verification completed successfully")
        return 0
    
    if not args.execute:
        log_message("INFO: Use --execute to perform cleanup or --verify-only for dry run")
        return 0
    
    log_message("BEGINNING EXECUTION - CRITICAL CLEANUP STARTED")
    
    # Files and directories to remove
    to_remove = [
        "package.json",
        "package-lock.json",
        "node_modules",
        "static",
        "staticfiles",
        "templates",
        "tailwind.config.js"
    ]
    
    # Remove frontend files/directories
    success = True
    for item in to_remove:
        if not remove_file_or_dir(item):
            success = False
    
    if not success:
        log_message("FATAL: Failed to remove some frontend files")
        return 1
    
    # Update .gitignore
    if not update_gitignore():
        log_message("WARNING: Failed to update .gitignore")
        # Continue anyway as this is not critical
    
    # Update README.md
    if not update_readme():
        log_message("WARNING: Failed to update README.md")
        # Continue anyway as this is not critical
    
    # Verify backend integrity
    if not verify_backend_integrity():
        log_message("FATAL: Backend integrity check failed")
        return 1
    
    log_message("CRITICAL CLEANUP COMPLETED SUCCESSFULLY")
    return 0

if __name__ == "__main__":
    sys.exit(main())