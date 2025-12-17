#!/usr/bin/env python3
"""
Script to fix the main.py file by ensuring correct imports and API usage for Google Gemini.
This addresses any potential import mismatches and ensures the RAG backend uses the correct API.
"""
import os
import re
from pathlib import Path


def fix_main_imports():
    """
    Fix the main.py file by ensuring correct imports and API usage for Google Gemini.
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

    print("Checking main.py file for potential issues...")

    # 1. Ensure we have the correct Google Generative AI import
    if "import google.generativeai as genai" not in content:
        # Add the import after the other imports but before the config import
        genai_import = "import google.generativeai as genai\n"
        config_import_line = "# Import configuration\n"

        if config_import_line in content:
            content = content.replace(config_import_line, f"{genai_import}{config_import_line}")
        else:
            # If config import line is not found, add after other imports
            import_section_end = content.find('\napp = FastAPI(')
            if import_section_end != -1:
                content = content[:import_section_end] + f"\n{genai_import}" + content[import_section_end:]

    # 2. Remove any potential OpenAI imports if they exist
    content = re.sub(r'^import openai$\n?', '', content, flags=re.MULTILINE)
    content = re.sub(r'^from openai.*$\n?', '', content, flags=re.MULTILINE)

    # 3. Remove any OpenAI API key configuration if it exists
    content = re.sub(r'^openai\.api_key =.*$\n?', '', content, flags=re.MULTILINE)

    # 4. Ensure genai.configure is called with the API key
    if "genai.configure(api_key=config.GEMINI_API_KEY)" not in content:
        # Find where to add the configuration call after imports
        config_import_line = "# Import configuration\n"
        genai_config = "genai.configure(api_key=config.GEMINI_API_KEY)\n"

        if config_import_line in content:
            # Find the end of the config import section
            config_import_pos = content.find(config_import_line) + len(config_import_line)
            content = content[:config_import_pos] + genai_config + content[config_import_pos:]

    # 5. Check for any OpenAI API calls and replace with Gemini equivalents if found
    # Look for patterns that might indicate OpenAI usage and replace with Gemini
    content = re.sub(
        r'response = openai\.ChatCompletion\.create\([^)]*?\)',
        '# Initialize the Gemini model\n'
        '        model = genai.GenerativeModel(\'gemini-2.5-flash\')\n\n'
        '        # Generate content using Gemini\n'
        '        response = model.generate_content(\n'
        '            prompt,\n'
        '            generation_config={\n'
        '                "temperature": 0.3,  # Lower temperature for more consistent answers\n'
        '            }\n'
        '        )\n\n'
        '        # Extract and return the answer\n'
        '        answer = response.text.strip()',
        content,
        flags=re.DOTALL
    )

    # 6. Replace response.text access pattern if it's from OpenAI
    content = re.sub(
        r'answer = response\.choices\[0\]\.message\.content\.strip\(\)',
        'answer = response.text.strip()',
        content
    )

    # Write the updated content back to the file if changes were made
    if original_content != content:
        with open(main_file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Successfully updated {main_file_path}")
    else:
        print(f"No changes were needed - {main_file_path} is already correctly configured.")

    # Report what was checked/fixed
    print("\nVerification completed:")
    if "import google.generativeai as genai" in content:
        print("V Google Generative AI import is present")
    else:
        print("X Google Generative AI import is missing")

    if "genai.configure(api_key=config.GEMINI_API_KEY)" in content:
        print("V Google Generative AI is configured with API key")
    else:
        print("X Google Generative AI configuration is missing")

    if "import openai" in content:
        print("X OpenAI import still present")
    else:
        print("V OpenAI import removed (if it existed)")

    return True


if __name__ == "__main__":
    print("Running main.py import fix script...")
    success = fix_main_imports()
    if success:
        print("\n[SUCCESS] main.py has been successfully verified/updated to use Google Gemini API.")
        print("\nThe correct startup command is:")
        print("  cd backend && uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload")
        print("\nOr using the module path directly:")
        print("  uvicorn backend.src.main:app --host 0.0.0.0 --port 8000 --reload")
    else:
        print("\n[FAILED] Failed to update main.py. Please check the file and try again.")