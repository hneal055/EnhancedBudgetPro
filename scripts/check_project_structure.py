import os
import sys

REQUIRED_STRUCTURE = {
    "pages": [
        "__init__.py",
        # Add your expected page files here, e.g. "storytelling_insights_helpers.py"
    ],
    "tests": [
        "__init__.py",
        # Add your expected test files here, e.g. "test_storytelling_insights_prereqs.py"
    ],
    "src": [
        "IngestEngine",
        "AnalysisEngine",
        "ProductionBudgetEngine",
        "ExportEngine",
        # Add other core modules as needed
    ],
    ".github": [
        "workflows",
    ],
    "samples": [],
    "output": [],
    "batch_output": [],
    "web_output": [],
    # Top-level files
    "pytest.ini": None,
    "requirements.txt": None,
    "Makefile": None,
    "pyproject.toml": None,
}


def check_dir_exists(path):
    if not os.path.isdir(path):
        print(f"❌ Missing directory: {path}")
        return False
    print(f"✅ Found directory: {path}")
    return True


def check_file_exists(path):
    if not os.path.isfile(path):
        print(f"❌ Missing file: {path}")
        return False
    print(f"✅ Found file: {path}")
    return True


def check_structure(base_path, structure):
    all_ok = True
    for name, contents in structure.items():
        full_path = os.path.join(base_path, name)
        if contents is None:
            # It's a file
            if not check_file_exists(full_path):
                all_ok = False
        elif isinstance(contents, list):
            # It's a directory
            if not check_dir_exists(full_path):
                all_ok = False
                continue
            for item in contents:
                item_path = os.path.join(full_path, item)
                # If item ends with .py, check as file, else as dir
                if item.endswith(".py"):
                    if not check_file_exists(item_path):
                        all_ok = False
                else:
                    if not check_dir_exists(item_path):
                        all_ok = False
    return all_ok


if __name__ == "__main__":
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(f"Checking project structure in: {base}\n")
    ok = check_structure(base, REQUIRED_STRUCTURE)
    if ok:
        print("\n🎉 Project structure is OK!")
        sys.exit(0)
    else:
        print(
            "\n⚠️  Project structure has missing elements. Please review the output above."
        )
        sys.exit(1)
