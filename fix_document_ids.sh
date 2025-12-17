#!/bin/bash

# Script to fix incorrect document IDs in Docusaurus Markdown files
# Replaces forward slashes with hyphens in the 'id' field of frontmatter

set -e  # Exit on any error

echo "Fixing incorrect document IDs in Docusaurus Markdown files..."

# Find all Markdown files in the docs directory
find docs/ -name "*.md" -type f | while read -r file; do
    echo "Processing: $file"

    # Use sed to replace forward slashes with hyphens in the id field only
    # This uses a more specific pattern to only match the id line
    sed -i.bak 's/^\(id:.*\)\//\1-/' "$file"

    # If the file was changed (backup created), update it
    if [ -f "${file}.bak" ]; then
        # Check if the backup is different from the original
        if ! cmp -s "${file}.bak" "$file"; then
            echo "  Fixed ID in $file"
        else
            # If no change was needed, remove the backup
            rm "${file}.bak"
        fi
    fi
done

# Handle the case where the id field has multiple slashes (like module4-3d-simulation/1.1-introduction)
# We need a more comprehensive approach to handle all files
find docs/ -name "*.md" -type f | while read -r file; do
    # Create a temporary file to store the updated content
    temp_file=$(mktemp)

    # Process the file line by line to handle the id field specifically
    in_frontmatter=false
    while IFS= read -r line || [[ -n "$line" ]]; do
        if [[ "$line" == "---" ]]; then
            if [[ "$in_frontmatter" == false ]]; then
                in_frontmatter=true
            else
                in_frontmatter=false
            fi
            echo "$line" >> "$temp_file"
        elif [[ "$in_frontmatter" == true && "$line" =~ ^id:\  ]] && [[ "$line" == *"/"* ]]; then
            # This is the id line with a slash - replace all slashes with hyphens
            fixed_line=$(echo "$line" | sed 's/\//\-/g')
            echo "$fixed_line" >> "$temp_file"
            echo "  Fixed ID in $file: $line -> $fixed_line"
        else
            echo "$line" >> "$temp_file"
        fi
    done < "$file"

    # Replace the original file with the fixed content
    mv "$temp_file" "$file"
done

echo "All document IDs have been fixed successfully!"
echo "Forward slashes in 'id' fields have been replaced with hyphens."