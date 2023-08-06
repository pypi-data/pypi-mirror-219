from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    README = f.read()

setup(
    name="codeclean",
    version="1.0.0",
    description="Remove comments and docstrings from Python code.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Ruu3f/cleancode",
    author="Ruu3f",
    license="GPLv2",
    keywords=[
        "clean",
        "code",
        "cleaner",
        "comments",
        "docstrings",
    ],
    python_requires=">=3",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    packages=find_packages(exclude=[".github"]),
    install_requires=[],
    project_urls={
        "Source": "https://github.com/Ruu3f/cleancode",
        "Discord": "https://discord.gg/XH6pUGkwRr",
    },
)
