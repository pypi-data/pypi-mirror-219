"""
codeclean

Remove comments and docstrings from Python code.
"""

import os
import re
import argparse


def remove_comments(code):
    """
    Removes comments from the code.
    """
    lines_list = []
    lines = code.split("\n")
    for line in lines:
        line = re.sub(r"\s*#.*$", "", line)
        lines_list.append(line)
    return "\n".join(lines_list)


def remove_docstrings(code):
    """
    Removes docstrings from the code.
    """
    code = re.sub(r'(?<!\\)"""[^"]*"""', "", code, flags=re.DOTALL)
    code = re.sub(r"(?<!\\)'''[^']*'''", "", code, flags=re.DOTALL)
    return code


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Remove comments and docstrings from Python files."
    )
    parser.add_argument(
        "files", metavar="file", type=str, nargs="+", help="File(s) to process"
    )
    parser.add_argument("--comments", action="store_true", help="Remove comments")
    parser.add_argument("--docstrings", action="store_true", help="Remove docstrings")

    args = parser.parse_args()

    modified_code = {}

    for file in args.files:
        if os.path.isfile(file):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    code = f.read()
            except IOError as e:
                print(f"Error while processing file {file}: {str(e)}")
                continue

            if args.comments:
                code = remove_comments(code)

            if args.docstrings:
                code = remove_docstrings(code)

            modified_code[file] = code
        else:
            print(f"Error: {file} is not a valid file.")

    for file, code in modified_code.items():
        try:
            with open(file, "w", encoding="utf-8") as f:
                f.write(code)
        except IOError as e:
            print(f"Error while writing to file {file}: {str(e)}")
