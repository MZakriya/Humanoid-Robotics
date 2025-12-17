---
id: 1
title: "Create Physical AI Humanoid Robotics Constitution"
stage: constitution
date_iso: "2025-12-07"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "none"
branch: "master"
user: "user"
command: "/sp.constitution"
labels: ["constitution", "spec-driven-development", "documentation"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - ".specify/memory/constitution.md"
  - ".specify/templates/plan-template.md"
  - ".specify/templates/spec-template.md"
  - ".specify/templates/tasks-template.md"
tests_yaml: []
---

# Create Physical AI Humanoid Robotics Constitution

## User Input

```
"You are a specialized Spec-Kit Plus agent. The project is 'Physical AI & Humanoid Robotics Textbook & Platform,' a comprehensive 10-module course on Embodied Intelligence. The final deliverable must be an integrated, personalized, and interactive learning platform built on **Docusaurus** and hosted on **GitHub Pages**, featuring a robust **RAG-based Chatbot**.

The 10-module course covers: Embodied Intelligence, ROS 2, Kinematics, 3D Simulation (Gazebo/Unity), VSLAM, Motion Planning, DRL (Isaac Sim), Manipulation (HRI), VLA/Cognitive Robotics, and Capstone/Ethics.

The mandatory core deliverables are:
1. A complete, deployable Docusaurus textbook (AI/Spec-Driven creation).
2. Deployment to a public URL (GitHub Pages/Vercel).
3. An integrated RAG Chatbot using **FastAPI** (backend), **Neon Serverless Postgres** (storage), and **Qdrant Cloud** (vector DB).
4. Chatbot functionality: answer general content questions AND questions based only on user-selected text.

Establish the project's foundational charter, outlining the high-level scope, the primary technology stack, and the non-negotiable core features that must be in the final product."
```

## Response Summary

Created the foundational constitution for the Physical AI & Humanoid Robotics Textbook & Platform project, establishing core principles, technical requirements, and governance structure. The constitution includes:

- Six core principles: Docusaurus-First Documentation, RAG-Based Intelligence Integration, Test-Driven Content Development, Multi-Module Educational Coherence, Open Source Accessibility, and Technology Stack Compliance
- Technical requirements for deployment to GitHub Pages, RAG chatbot performance, and mobile responsiveness
- Development workflow requirements for peer review and testing
- Governance structure with compliance verification requirements

Updated template files to align with the new constitution:
- Modified plan-template.md to include constitution checks for all principles
- Updated spec-template.md to include functional requirements aligned with project goals
- Modified tasks-template.md to include foundational tasks for the required technology stack

## Outcome

The project constitution has been successfully created and template files updated to ensure all future development aligns with the established principles and requirements. This provides a clear foundation for the Physical AI & Humanoid Robotics Textbook & Platform project.

## Evaluation

The constitution addresses all requirements specified by the user, establishing clear principles for the Docusaurus-based educational platform with RAG chatbot functionality using the specified technology stack. Template files have been updated to ensure consistency across the development process.