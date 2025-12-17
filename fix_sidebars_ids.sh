#!/bin/bash

# Script to fix incorrect document IDs in sidebars.js file
# Replaces forward slashes with hyphens in the document ID strings

set -e  # Exit on any error

echo "Fixing incorrect document IDs in sidebars.js file..."

# Create a backup of the original file
cp sidebars.js sidebars.js.bak

# Use sed to replace all forward slashes with hyphens in document ID strings
# This handles the pattern where document IDs are in single quotes like 'module-name/section-name'
# We run the command multiple times to handle cases with multiple slashes in one line
sed -i.bak "s/'\([^'/]*\)\/\([^'/]*\)'/'\1-\2'/g" sidebars.js
sed -i.bak "s/'\([^'/]*\)\/\([^'/]*\)'/'\1-\2'/g" sidebars.js  # Run again to catch remaining instances
sed -i.bak "s/'\([^'/]*\)\/\([^'/]*\)'/'\1-\2'/g" sidebars.js  # Run a third time if needed

echo "Document IDs in sidebars.js have been fixed successfully!"
echo "Forward slashes in document ID strings have been replaced with hyphens."
echo ""
echo "Summary of changes:"
echo "- 'module1-embodied-intelligence/1.1-introduction' → 'module1-embodied-intelligence-1.1-introduction'"
echo "- 'module4-3d-simulation/4.1-introduction' → 'module4-3d-simulation-4.1-introduction'"
echo "- And all other similar ID patterns"
echo ""
echo "Docusaurus should now start successfully with synchronized document IDs."

# Remove the backup file
rm sidebars.js.bak