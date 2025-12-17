---
id: 6
title: "Fix Sidebars IDs Script"
stage: "general"
date: "2025-12-08"
model: "Claude Sonnet 4.5"
surface: "agent"
feature: "none"
branch: "master"
user: "user"
command: "/sp.implement"
labels: ["docusaurus", "documentation", "automation", "script", "bug-fix"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "fix_sidebars_ids.sh"
tests: []
---

# Fix Sidebars Document IDs Script Implementation

## User Input
```
"The Docusaurus server still crashes because the 'sidebars.js' file contains incorrect document IDs (using '/' separators) while the actual Markdown files and available document IDs use the correct hyphenated format ('-') after Task 5.15.

**Task 5.16: Fix `sidebars.js` Document IDs (Automation)**

Generate a **shell script** (compatible with Bash/PowerShell) that specifically targets and fixes the `sidebars.js` file:

1.  **Goal:** Modify the content of the `sidebars.js` file to replace all occurrences of forward slash (`/`) within document ID strings with a hyphen (`-`).
2.  **Method:** Use the `sed` command (if Bash is available) or equivalent functionality (like `(Get-Content | ForEach-Object { $_ -replace '/' , '-' } | Set-Content)` in PowerShell) to perform a global find-and-replace operation *only* on the content of the `sidebars.js` file.
3.  **Target:** The script must run the replacement on the `sidebars.js` file located in the root directory.

This script will synchronize the document IDs in the sidebar configuration with the actual file IDs, allowing the Docusaurus server to start successfully."
```

## Implementation Summary

Successfully created and executed a shell script that fixes the document IDs in the sidebars.js file by replacing forward slashes with hyphens. The script:

1. **Created a backup** of the original sidebars.js file
2. **Used sed command** to perform global find-and-replace operations on document ID strings
3. **Replaced all forward slashes** within single-quoted document IDs with hyphens
4. **Processed the file multiple times** to handle cases with multiple slashes in one line
5. **Removed the backup file** after successful completion

The script successfully transformed all document IDs from the incorrect slash format to the correct hyphenated format:
- `'module1-embodied-intelligence/1.1-introduction'` → `'module1-embodied-intelligence-1.1-introduction'`
- `'module4-3d-simulation/4.1-introduction'` → `'module4-3d-simulation-4.1-introduction'`
- And all other similar ID patterns

## Files Created/Modified
- `fix_sidebars_ids.sh` - The automation script to fix sidebars document IDs
- `sidebars.js` - Updated to have synchronized document IDs matching file names

## Outcome
The document IDs in sidebars.js are now synchronized with the actual file IDs, resolving the Docusaurus server startup error caused by ID mismatches.