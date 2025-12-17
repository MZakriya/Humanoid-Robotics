<!--
Sync Impact Report:
- Version change: 1.0.0 → 1.0.0 (initial creation)
- Modified principles: All principles added (new constitution)
- Added sections: All sections added (new constitution)
- Removed sections: None
- Templates requiring updates: N/A (initial creation)
- Follow-up TODOs: None
-->
# Physical AI & Humanoid Robotics Textbook & Platform Constitution

## Core Principles

### I. Docusaurus-First Documentation
Every educational module must be implemented as a structured Docusaurus document with clear navigation, search functionality, and responsive design. All content must be accessible, well-organized, and follow consistent formatting standards with proper code examples and visual aids.

### II. RAG-Based Intelligence Integration
The platform must feature a robust Retrieval-Augmented Generation (RAG) chatbot using FastAPI backend, Neon Serverless Postgres for metadata, and Qdrant Cloud for vector storage. The chatbot must handle both general queries and context-specific questions based on user-selected text.

### III. Test-Driven Content Development (NON-NEGOTIABLE)
All educational content and platform features must follow TDD principles: Learning objectives defined → Assessment criteria approved → Content gaps identified → Then develop. Red-Green-Refactor cycle strictly enforced for both content and code.

### IV. Multi-Module Educational Coherence
All 10 modules (Embodied Intelligence, ROS 2, Kinematics, 3D Simulation, VSLAM, Motion Planning, DRL, Manipulation, VLA/Cognitive Robotics, Capstone/Ethics) must maintain pedagogical consistency, progressive complexity, and cross-module integration where applicable.

### V. Open Source Accessibility
All platform code, educational content, and deployment configurations must be open source and publicly accessible via GitHub Pages. Documentation must be comprehensive and deployment processes must be reproducible by any user.

### VI. Technology Stack Compliance
All implementations must strictly adhere to the mandated technology stack: Docusaurus for frontend, FastAPI for backend services, Neon for database storage, and Qdrant for vector databases. No alternative technologies may be substituted without explicit approval.

## Technical Requirements
<!-- Example: Additional Constraints, Security Requirements, Performance Standards, etc. -->

The platform must support the following technical specifications:
- Deployable to GitHub Pages with automated CI/CD pipeline
- RAG chatbot must respond to queries within 3-5 seconds for 95% of requests
- Educational content must be searchable and indexed
- Platform must support interactive code examples and visualizations
- All code examples must be tested and verified for accuracy
- Mobile-responsive design for all educational materials

## Development Workflow
<!-- Example: Development Workflow, Review Process, Quality Gates, etc. -->

The development process must follow these requirements:
- All educational content must undergo peer review before publication
- Code implementations must include comprehensive unit and integration tests
- Feature branches must be created for each module development
- Pull requests must include both content and code changes
- All deployments must be tested on staging before production
- Documentation updates must be synchronized with code changes

## Governance
<!-- Example: Constitution supersedes all other practices; Amendments require documentation, approval, migration plan -->

This constitution governs all development and content creation for the Physical AI & Humanoid Robotics Textbook & Platform. All PRs and reviews must verify compliance with these principles. Any deviation from the specified technology stack or educational requirements must be documented and approved. All changes must maintain backward compatibility where possible.

**Version**: 1.0.0 | **Ratified**: 2025-12-07 | **Last Amended**: 2025-12-07
