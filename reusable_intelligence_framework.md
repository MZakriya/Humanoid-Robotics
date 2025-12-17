# Reusable Intelligence Framework: Claude Code Subagents for Physical AI Textbook Project

## Overview
This document defines a framework of reusable Claude Code Subagents for project maintenance and development of the Physical AI Textbook project. The framework includes two specialized agents with a shared skill for efficient task execution.

## Subagent 1: Code Review & Optimization Agent

### Purpose
Specialized in reviewing Python/C++ code snippets found in the textbook's modules (e.g., Module 3 Kinematics or Module 2 ROS 2 code) for performance, safety, and ROS 2 best practices.

### Specialized Capabilities
- **Performance Analysis**: Identifies bottlenecks, inefficient algorithms, and memory usage issues
- **Safety Review**: Checks for proper error handling, boundary conditions, and resource management
- **ROS 2 Best Practices**: Validates adherence to ROS 2 coding standards, node design, and communication patterns
- **Code Quality Assessment**: Evaluates code structure, maintainability, and documentation
- **Optimization Suggestions**: Provides specific recommendations for improving code efficiency

### Expertise Areas
- Python and C++ code review
- ROS 2 architecture and design patterns
- Real-time system considerations
- Robotics-specific performance optimization
- Safety-critical code analysis

### Configuration
```python
code_review_agent = {
    "name": "Code Review & Optimization Agent",
    "role": "Specialized in reviewing Python/C++ code for performance, safety, and ROS 2 best practices",
    "capabilities": [
        "performance_analysis",
        "safety_review",
        "ros2_best_practices",
        "code_quality_assessment",
        "optimization_suggestions"
    ],
    "focus_areas": ["kinematics", "ros2_modules", "motion_planning", "control_systems"],
    "review_criteria": {
        "performance": ["time_complexity", "memory_usage", "computational_efficiency"],
        "safety": ["error_handling", "boundary_checks", "resource_management"],
        "best_practices": ["ros2_patterns", "coding_standards", "documentation"]
    }
}
```

## Subagent 2: Module Content Generator Agent

### Purpose
Specialized in expanding or generating new supplementary content (e.g., adding a new section on a niche topic like 'Advanced Zero Moment Point Control' in Module 6) using the existing module structure as a reference.

### Specialized Capabilities
- **Content Expansion**: Creates new sections that align with existing module structure and pedagogical approach
- **Technical Accuracy**: Ensures generated content is technically correct and consistent with textbook standards
- **Style Consistency**: Maintains the same writing style, complexity level, and educational approach as existing content
- **Cross-Module Integration**: Links new content with related concepts from other modules
- **Supplementary Material Generation**: Creates examples, exercises, and practical applications

### Expertise Areas
- Educational content creation for robotics and AI
- Technical writing in robotics domains
- Module structure and organization
- Cross-referencing between textbook sections
- Practical application examples

### Configuration
```python
content_generator_agent = {
    "name": "Module Content Generator Agent",
    "role": "Specialized in expanding/generating new supplementary content using existing module structure",
    "capabilities": [
        "content_expansion",
        "technical_accuracy",
        "style_consistency",
        "cross_module_integration",
        "supplementary_material_generation"
    ],
    "content_types": ["theoretical_explanations", "practical_examples", "exercises", "applications"],
    "generation_criteria": {
        "accuracy": ["technical_correctness", "up_to_date_information", "peer_reviewed_content"],
        "consistency": ["writing_style", "complexity_level", "pedagogical_approach"],
        "integration": ["cross_references", "module_coherence", "learning_progression"]
    }
}
```

## Shared Skill: File Structure Navigator Skill

### Purpose
A reusable skill that both agents can utilize to locate and read specific files in the `docs/` or `backend/` directory.

### Functionality
- **File Discovery**: Locates files based on patterns, extensions, or content keywords
- **Directory Navigation**: Traverses the project directory structure efficiently
- **Content Reading**: Reads file contents with appropriate handling for different file types
- **Path Resolution**: Resolves relative and absolute paths within the project context
- **Filtering**: Filters files based on type, location, or other criteria

### Implementation
```python
class FileStructureNavigatorSkill:
    def __init__(self, project_root="."):
        self.project_root = project_root
        self.docs_path = f"{project_root}/docs"
        self.backend_path = f"{project_root}/backend"

    def find_files_by_pattern(self, directory, pattern, file_extension=None):
        """
        Find files in a directory matching a specific pattern
        """
        import os
        import glob

        search_path = f"{directory}/**/*{pattern}*"
        if file_extension:
            search_path += f".{file_extension}"

        return glob.glob(search_path, recursive=True)

    def find_files_by_content(self, directory, search_term, file_extensions=None):
        """
        Find files containing a specific term
        """
        import os
        import glob

        files_to_search = []
        if file_extensions:
            for ext in file_extensions:
                files_to_search.extend(glob.glob(f"{directory}/**/*.{ext}", recursive=True))
        else:
            files_to_search = glob.glob(f"{directory}/**/*", recursive=True)

        matching_files = []
        for file_path in files_to_search:
            if os.path.isfile(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if search_term.lower() in content.lower():
                            matching_files.append(file_path)
                except:
                    continue  # Skip files that can't be read

        return matching_files

    def read_file_content(self, file_path):
        """
        Read content from a specific file
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"

    def get_module_structure(self):
        """
        Get the structure of modules in the docs directory
        """
        import os
        modules = {}

        for item in os.listdir(self.docs_path):
            item_path = os.path.join(self.docs_path, item)
            if os.path.isdir(item_path) and item.startswith("module"):
                modules[item] = {
                    "path": item_path,
                    "files": os.listdir(item_path)
                }

        return modules
```

## Demonstration Orchestration Script

### Conceptual Implementation
```python
import asyncio
from typing import Dict, List, Any

class PhysicalAITextbookOrchestrator:
    def __init__(self):
        self.code_review_agent = self.initialize_code_review_agent()
        self.content_generator_agent = self.initialize_content_generator_agent()
        self.file_navigator = FileStructureNavigatorSkill()

    def initialize_code_review_agent(self):
        # Initialize the code review agent with its configuration
        return code_review_agent

    def initialize_content_generator_agent(self):
        # Initialize the content generator agent with its configuration
        return content_generator_agent

    async def review_module_code(self, module_name: str):
        """
        Task: Review all Python code in a specific module
        Example: 'Review all Python code in Module 3'
        """
        print(f"Starting code review for {module_name}")

        # Use the shared skill to find Python files in the module
        python_files = self.file_navigator.find_files_by_pattern(
            directory=f"docs/{module_name}",
            pattern="",
            file_extension="py"
        )

        # Also search in backend if the module has code there
        backend_python_files = self.file_navigator.find_files_by_pattern(
            directory="backend",
            pattern=module_name.replace("module", "").split("-")[0],  # Extract module number
            file_extension="py"
        )

        all_python_files = python_files + backend_python_files

        results = []
        for file_path in all_python_files:
            print(f"Reviewing {file_path}")

            # Read the file content using the shared skill
            content = self.file_navigator.read_file_content(file_path)

            # Perform code review using the specialized agent
            review_result = await self.execute_code_review(content, file_path)
            results.append({
                "file": file_path,
                "review": review_result
            })

        return results

    async def expand_module_content(self, module_name: str, new_topic: str):
        """
        Task: Expand a module with new content
        Example: 'Expand Module 6 with new ZMP content'
        """
        print(f"Expanding {module_name} with content about {new_topic}")

        # Use the shared skill to get the module's structure
        module_structure = self.file_navigator.get_module_structure()

        if module_name not in module_structure:
            print(f"Module {module_name} not found")
            return None

        # Get existing content for context
        module_path = module_structure[module_name]["path"]
        existing_files = module_structure[module_name]["files"]

        # Read existing content to maintain consistency
        existing_content = {}
        for file in existing_files:
            file_path = f"{module_path}/{file}"
            if file.endswith('.md'):
                content = self.file_navigator.read_file_content(file_path)
                existing_content[file] = content

        # Generate new content using the specialized agent
        new_content = await self.execute_content_generation(
            module_name,
            new_topic,
            existing_content
        )

        # Save the new content
        new_file_path = f"{module_path}/{new_topic.lower().replace(' ', '-')}.md"
        with open(new_file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"New content saved to {new_file_path}")
        return new_file_path

    async def execute_code_review(self, code_content: str, file_path: str) -> Dict[str, Any]:
        """
        Execute code review using the specialized agent
        """
        # Simulate the agent's review process
        review = {
            "file_path": file_path,
            "performance_issues": [],
            "safety_concerns": [],
            "best_practices_violations": [],
            "optimization_suggestions": [],
            "overall_score": 0,
            "recommendations": []
        }

        # In a real implementation, this would call the actual agent
        # For demonstration, we'll simulate some basic checks

        if "while True:" in code_content:
            review["performance_issues"].append("Potential infinite loop detected")

        if "print(" in code_content and "debug" in code_content.lower():
            review["best_practices_violations"].append("Debug print statement found")

        if "except:" in code_content:
            review["safety_concerns"].append("Broad exception handling detected")

        review["overall_score"] = 85  # Simulated score
        review["recommendations"] = ["Add proper error handling", "Optimize algorithm complexity"]

        return review

    async def execute_content_generation(self, module_name: str, topic: str, context: Dict[str, str]) -> str:
        """
        Execute content generation using the specialized agent
        """
        # In a real implementation, this would call the actual agent
        # For demonstration, we'll generate a template

        frontmatter = f"""---
id: {module_name}-{topic.lower().replace(' ', '-')}
title: "{topic}"
slug: /{module_name}/{topic.lower().replace(' ', '-')}
---

"""

        content = f"# {topic}\n\n"
        content += f"This section covers {topic} in the context of {module_name.replace('-', ' ').title()}.\n\n"
        content += "## Introduction\n\n"
        content += f"{topic} is an important concept in robotics and physical AI.\n\n"
        content += "## Technical Details\n\n"
        content += "The implementation of this concept involves several key considerations:\n\n"
        content += "- First consideration\n"
        content += "- Second consideration\n"
        content += "- Third consideration\n\n"
        content += "## Practical Applications\n\n"
        content += "Real-world applications of this concept include:\n\n"
        content += "- Application 1\n"
        content += "- Application 2\n\n"
        content += "## Summary\n\n"
        content += f"This section provided an overview of {topic} and its relevance to {module_name.replace('-', ' ').title()}."

        return frontmatter + content

    async def run_maintenance_task(self, task_type: str, **kwargs):
        """
        Main orchestration method to run maintenance tasks
        """
        if task_type == "review_code":
            return await self.review_module_code(kwargs["module_name"])
        elif task_type == "expand_content":
            return await self.expand_module_content(
                kwargs["module_name"],
                kwargs["new_topic"]
            )
        else:
            raise ValueError(f"Unknown task type: {task_type}")

# Example usage
async def main():
    orchestrator = PhysicalAITextbookOrchestrator()

    # Example 1: Review all Python code in Module 3
    print("=== Example 1: Code Review Task ===")
    code_review_results = await orchestrator.run_maintenance_task(
        task_type="review_code",
        module_name="module3-kinematics"
    )
    print(f"Reviewed {len(code_review_results)} files")

    # Example 2: Expand Module 6 with new ZMP content
    print("\n=== Example 2: Content Generation Task ===")
    new_content_path = await orchestrator.run_maintenance_task(
        task_type="expand_content",
        module_name="module6-motion-planning",
        new_topic="Advanced Zero Moment Point Control"
    )
    print(f"New content created at: {new_content_path}")

# Run the demonstration
if __name__ == "__main__":
    asyncio.run(main())
```

## Framework Benefits

### Reusability
- Agents can be reused across different modules and tasks
- Shared skills reduce code duplication and maintenance overhead
- Configurable agents adapt to different project needs

### Specialization
- Each agent focuses on specific tasks for better results
- Expertise is concentrated in dedicated components
- Clear separation of concerns improves maintainability

### Scalability
- New agents can be added following the same patterns
- Skills can be extended or replaced as needed
- Framework supports complex multi-agent workflows

### Integration
- Agents work together through shared skills
- Orchestration layer coordinates complex tasks
- Consistent interfaces enable easy extension

## Conclusion

This Reusable Intelligence framework provides a structured approach to automating project maintenance and development tasks for the Physical AI Textbook. The two specialized agents with their shared skill create an efficient system for code review and content generation, while the orchestration layer enables complex multi-step operations. The framework is designed to be extensible, allowing for additional agents and skills as project requirements evolve.