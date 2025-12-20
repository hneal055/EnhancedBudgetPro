import os
import re


def needs_streamlit_import(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    # Check if 'st.' is used and 'import streamlit as st' is missing
    uses_st = re.search(r"\bst\.", content)
    has_import = re.search(r"^\s*import\s+streamlit\s+as\s+st", content, re.MULTILINE)
    return uses_st and not has_import


def add_streamlit_import(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    # Insert after any shebang or encoding line, else at top
    insert_at = 0
    for i, line in enumerate(lines[:2]):
        if line.startswith("#!"):
            insert_at = i + 1
        elif "coding" in line:
            insert_at = i + 1
    lines.insert(insert_at, "import streamlit as st\n")
    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"Added import to {filepath}")


def scan_and_fix(root_dir):
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".py"):
                filepath = os.path.join(dirpath, filename)
                if needs_streamlit_import(filepath):
                    add_streamlit_import(filepath)


if __name__ == "__main__":
    scan_and_fix(".")
