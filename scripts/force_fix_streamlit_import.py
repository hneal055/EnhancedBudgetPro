import os
import re


def fix_streamlit_imports_in_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Remove all existing 'import streamlit as st' lines
    new_lines = [
        line
        for line in lines
        if not re.match(r"^\s*import\s+streamlit\s+as\s+st\s*$", line)
    ]

    # Check if 'st.' is used in the file
    uses_st = any("st." in line for line in new_lines)
    if uses_st:
        # Insert a single import at the top (after any shebang or encoding lines)
        insert_at = 0
        while insert_at < len(new_lines) and (
            new_lines[insert_at].startswith("#!")
            or new_lines[insert_at].lower().startswith("# -*- coding")
        ):
            insert_at += 1
        new_lines.insert(insert_at, "import streamlit as st\n")

        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        print(f"Fixed: {filepath}")


def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                fix_streamlit_imports_in_file(os.path.join(root, file))


if __name__ == "__main__":
    # Change 'pages' to the directory you want to process, or add more as needed
    process_directory("pages")
    process_directory(".")
