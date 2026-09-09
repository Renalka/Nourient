# Archived Scripts

This directory contains legacy, one-off automation scripts used during the active development and prototyping phases of the Nourient platform. 

To declutter the active workspace, these files were moved here from the project root and `frontend/` directories.

## Directory Structure
- `/patch_` : Scripts used to dynamically patch code (e.g., swapping API models, rewriting imports, automating mass find-and-replace).
- `/fix_` : Targeted scripts written to resolve specific bugs or syntax errors (e.g., fixing duplicate imports, patching broken layout files).
- `/test_` : Throwaway scripts used to test specific features in isolation (e.g., testing Pinecone distances, Gemini API limits, or filesystem permissions).

## ⚠️ Important Note on Execution

These scripts were written as **one-time operations**. 

They contain hardcoded relative paths that assume they are being executed directly from the project root (e.g., `open('backend/services/...')`). **If you attempt to run them from within this `archived_scripts` directory, they will throw "File Not Found" errors.**

If you *must* run one of these scripts again (which is highly discouraged, as the codebase has evolved past them), you must either:
1. Move the specific script back to the project root directory before executing it.
2. Manually edit the file paths inside the script to include `../`.

Otherwise, treat these files strictly as a historical reference.
