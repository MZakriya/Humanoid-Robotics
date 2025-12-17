---
id: 4
title: "Fix Document IDs Script"
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
  - "fix_document_ids.sh"
tests: []
---

# Fix Incorrect Document IDs Script Implementation

## User Input
```
"The Docusaurus server failed because the document 'id' field cannot contain a forward slash ('/'), a common issue when generating document metadata automatically. The previous placeholder script generated incorrect 'id' values (e.g., 'moduleX/chapterY') in the frontmatter of all 49 files, causing the server crash.

**Task 5.15: Fix Incorrect Document IDs (Automation)**

Generate a **shell script** (compatible with Bash/PowerShell but using standard commands) that performs the following global fix across all Markdown files in the 'docs/' directory:

1.  **Find Files:** Recursively search and target all Markdown files (`.md`) within the `docs/` folder.
2.  **Modify Frontmatter:** For every file, find the line containing the `id:` frontmatter field.
3.  **Replace ID Value:** Replace the incorrect ID value (`id: module-name/chapter-slug`) with a correct, slash-free ID value. The easiest way to create a unique, slash-free ID is to replace all slashes (`/`) with **hyphens (`-`)**.

    * **Example Transformation:**
        `id: module10-capstone-ethics/10.1-integration-all-modules`
        **will become**
        `id: module10-capstone-ethics-10.1-integration-all-modules`

4.  **Output:** Provide the ready-to-run file correction script and clear instructions. Once this script is run, the Docusaurus server should start successfully."
```

## Implementation Summary

Successfully created and executed a comprehensive shell script that fixes all incorrect document IDs in Docusaurus Markdown files. The script:

1. **Finds all Markdown files** recursively in the `docs/` directory
2. **Identifies the frontmatter section** in each file
3. **Locates the `id:` field** within the frontmatter
4. **Replaces all forward slashes with hyphens** in the ID value
5. **Preserves all other content** in the files

The script correctly transformed IDs such as:
- `id: module4-3d-simulation/1.1-introduction` → `id: module4-3d-simulation-1.1-introduction`
- `id: module10-capstone-ethics/10.1-integration-all-modules` → `id: module10-capstone-ethics-10.1-integration-all-modules`

The fix has been verified to work across all 49 documentation files, and backup files have been cleaned up. The Docusaurus server should now start successfully without errors related to invalid ID characters.

## Files Created/Modified
- `fix_document_ids.sh` - The automation script to fix document IDs
- All Markdown files in `docs/` directory - Fixed to have slash-free IDs

## Outcome
All document IDs in the Docusaurus documentation now comply with the requirement of not containing forward slashes, resolving the server startup error.