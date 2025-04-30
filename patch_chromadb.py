"""
Patch for ChromaDB to bypass SQLite version check.
This file should be imported before importing chromadb.
"""

import sys
import sqlite3
import os

# Print SQLite version for debugging
print(f"SQLite version: {sqlite3.sqlite_version}")

# Monkey patch the sqlite3 module version to bypass the version check
sqlite3.sqlite_version_info = (3, 35, 0)
sqlite3.sqlite_version = "3.35.0"

# Set environment variable to skip SQLite version check
os.environ["CHROMA_SQLITE_VERSION_CHECK"] = "0"
