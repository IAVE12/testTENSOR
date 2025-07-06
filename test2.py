import random
import sys
from functools import cmp_to_key

def generate_version_numbers(template):
    """Generate two version numbers based on the template"""
    parts = template.split('.')
    versions = []

    for _ in range(2):
        version = []
        for part in parts:
            if part == '*':
                version.append(str(random.randint(0, 9)))
            else:
                version.append(part)
        versions.append('.'.join(version))

    return versions

def version_compare(v1, v2):
    """Compare two version strings"""
    v1_parts = list(map(int, v1.split('.')))
    v2_parts = list(map(int, v2.split('.')))

    max_len = max(len(v1_parts), len(v2_parts))

    for i in range(max_len):
        v1_part = v1_parts[i] if i < len(v1_parts) else 0
        v2_part = v2_parts[i] if i < len(v2_parts) else 0

        if v1_part < v2_part:
            return -1
        elif v1_part > v2_part:
            return 1

    return 0

def task2(target_version, config_file):
    try:
        # Read config file
        with open(config_file, 'r') as f:
            content = f.read()

        # Parse config (very simple parser for this specific format)
        # This assumes format like { Sh1:"3.7.*", Sh2:"3.*.1", Sh3:"1.2.3.*" }
        templates = []
        entries = content.strip()[1:-1].split(',')
        for entry in entries:
            template = entry.split(':')[1].strip().strip('"')
            templates.append(template)

        # Generate versions
        all_versions = []
        for template in templates:
            versions = generate_version_numbers(template)
            all_versions.extend(versions)

        # Sort all versions
        sorted_versions = sorted(all_versions, key=cmp_to_key(version_compare))

        print("All generated versions (sorted):")
        for version in sorted_versions:
            print(version)

        # Find versions older than target
        older_versions = [v for v in all_versions if version_compare(v, target_version) < 0]

        print("\nVersions older than", target_version)
        for version in sorted(older_versions