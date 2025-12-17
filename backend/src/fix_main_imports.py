#!/usr/bin/env python3
"""
Script to fix the main.py file by replacing OpenAI API calls with Google Gemini API calls.
This addresses the import mismatch and API usage issues in the RAG backend.
"""

import os
import re
from pathlib import Path


def fix_main_imports():
    """
    Fix the main.py file by replacing OpenAI imports and API calls with Google Gemini equivalents.
    """
    main_file_path = Path("D:/humanoid_robotics_ai/backend/src/main.py")

    if not main_file_path.exists():
        print(f"Error: {main_file_path} does not exist!")
        return False

    # Read the current content of main.py
    with open(main_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Store the original content for comparison
    original_content = content

    print("Fixing main.py file...")

    # 1. Remove the incorrect OpenAI import if it exists alongside the correct Gemini import
    # We want to keep the Google Gemini import and remove the OpenAI import
    content = re.sub(r'^import openai$\n?', '', content, flags=re.MULTILINE)

    # 2. Remove the OpenAI API key configuration line
    content = re.sub(r'^openai\.api_key = config\.OPENAI_API_KEY$\n?', '', content, flags=re.MULTILINE)

    # 3. Replace OpenAI API calls with Google Gemini API calls
    # Find the generate_rag_answer function and replace the OpenAI API call with Gemini
    def replace_openai_with_gemini(match):
        """Replace OpenAI API call with Google Gemini API call"""
        before_call = match.group(1)
        prompt = match.group(2)

        # Create the new Gemini API call
        gemini_code = f'''{before_call}
        # Initialize the Gemini model
        model = genai.GenerativeModel('gemini-2.5-flash')

        # Generate content using Gemini
        response = model.generate_content(
            {prompt},
            generation_config={{
                "temperature": 0.3,  # Lower temperature for more consistent answers
            }}
        )

        # Extract and return the answer
        answer = response.text.strip()'''

        return gemini_code

    # Pattern to match the OpenAI API call section in generate_rag_answer function
    pattern = r'(.*?)(prompt\s*=.*?)\n\s*# Call the OpenAI API to generate the answer\n.*?response = openai\.ChatCompletion\.create\(\s*\n.*?model="gpt-3\.5-turbo"[^}]*?\n.*?\}(?=\n\s*except)'

    # Replace the OpenAI call with Gemini call
    content = re.sub(pattern, replace_openai_with_gemini, content, flags=re.DOTALL)

    # Additional fix: Replace the specific OpenAI API call if the above pattern didn't catch it
    content = re.sub(
        r'# Call the OpenAI API to generate the answer\s*\n\s*response = openai\.ChatCompletion\.create\(\s*\n\s*model="gpt-3\.5-turbo"[^}]*?\n\s*\}',
        '''        # Initialize the Gemini model
        model = genai.GenerativeModel('gemini-2.5-flash')

        # Generate content using Gemini
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.3,  # Lower temperature for more consistent answers
            }
        )

        # Extract and return the answer
        answer = response.text.strip()''',
        content
    )

    # Write the updated content back to the file
    with open(main_file_path, 'w', encoding='utf-8') as file:
        file.write(content)

    print(f"Successfully updated {main_file_path}")

    # Report what was changed
    if original_content != content:
        print("Changes made:")
        print("- Removed import openai")
        print("- Removed openai.api_key configuration")
        print("- Replaced OpenAI ChatCompletion API call with Google Gemini API call")
        return True
    else:
        print("No changes were needed.")
        return True


if __name__ == "__main__":
    success = fix_main_imports()
    if success:
        print("\nmain.py has been successfully updated to use Google Gemini API instead of OpenAI API.")
        print("You can now start the FastAPI server using the correct module path:")
        print("  cd backend && python -m src.main")
        print("Or using uvicorn:")
        print("  cd backend && uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload")
    else:
        print("\nFailed to update main.py. Please check the file and try again.")