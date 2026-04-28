#!/usr/bin/env python
"""
Fix static files for deployment
Run this script to ensure all static files are properly configured
"""

import os
import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AIJobMatcher.settings')
django.setup()

def fix_static_files():
    print("🔧 Fixing static files configuration...")
    
    # Collect static files
    print("📁 Collecting static files...")
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
    
    # Check if static files exist
    static_root = settings.STATIC_ROOT
    if os.path.exists(static_root):
        print(f"✅ Static files collected to: {static_root}")
        
        # List collected files
        for root, dirs, files in os.walk(static_root):
            level = root.replace(static_root, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 2 * (level + 1)
            for file in files:
                print(f"{subindent}{file}")
    else:
        print(f"❌ Static root not found: {static_root}")
    
    # Check original static directory
    static_dirs = settings.STATICFILES_DIRS
    print(f"\n📂 Original static directories: {static_dirs}")
    
    for static_dir in static_dirs:
        if os.path.exists(static_dir):
            print(f"✅ Found static directory: {static_dir}")
            for root, dirs, files in os.walk(static_dir):
                if files:
                    print(f"  📁 {os.path.relpath(root, static_dir)}/")
                    for file in files[:5]:  # Show first 5 files
                        print(f"    📄 {file}")
                    if len(files) > 5:
                        print(f"    ... and {len(files) - 5} more files")
        else:
            print(f"❌ Static directory not found: {static_dir}")

if __name__ == '__main__':
    fix_static_files()
