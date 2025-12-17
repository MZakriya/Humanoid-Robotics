# Data Model: Physical AI & Humanoid Robotics Textbook & Platform

**Feature**: 1-content-spec
**Date**: 2025-12-07

## Core Entities

### Module
- **Description**: Educational unit covering specific Physical AI & Humanoid Robotics topics
- **Fields**:
  - id: string (unique identifier)
  - slug: string (URL-friendly identifier for Docusaurus)
  - title: string (display title)
  - description: string (brief overview)
  - order: integer (sequence in curriculum)
  - prerequisites: array of Module.id (required prior knowledge)
  - estimated_duration: integer (in minutes)
  - difficulty_level: enum (beginner, intermediate, advanced)
  - created_at: datetime
  - updated_at: datetime
  - status: enum (draft, review, published)

### Section
- **Description**: Subdivision of a module with focused learning objectives
- **Fields**:
  - id: string (unique identifier)
  - module_id: string (foreign key to Module)
  - title: string (section title)
  - slug: string (URL fragment within module)
  - content: text (main content in Markdown)
  - order: integer (sequence within module)
  - learning_objectives: array of string (specific learning goals)
  - examples: array of CodeExample.id (related code examples)
  - exercises: array of Exercise.id (practice problems)
  - created_at: datetime
  - updated_at: datetime

### CodeExample
- **Description**: Practical implementation example within sections
- **Fields**:
  - id: string (unique identifier)
  - section_id: string (foreign key to Section)
  - title: string (example title)
  - description: string (brief explanation)
  - language: string (programming language)
  - code: text (actual code content)
  - explanation: text (step-by-step breakdown)
  - created_at: datetime
  - updated_at: datetime

### Exercise
- **Description**: Practice problem or assignment for students
- **Fields**:
  - id: string (unique identifier)
  - section_id: string (foreign key to Section)
  - title: string (exercise title)
  - description: text (problem statement)
  - type: enum (quiz, coding, research, project)
  - difficulty: enum (easy, medium, hard)
  - solution: text (expected solution or answer)
  - hints: array of string (guidance for students)
  - created_at: datetime
  - updated_at: datetime

### User
- **Description**: Platform user (student, educator, developer)
- **Fields**:
  - id: string (unique identifier)
  - email: string (unique, required)
  - name: string (display name)
  - role: enum (student, educator, developer, admin)
  - created_at: datetime
  - updated_at: datetime

### UserProgress
- **Description**: Track user's progress through modules
- **Fields**:
  - id: string (unique identifier)
  - user_id: string (foreign key to User)
  - module_id: string (foreign key to Module)
  - section_id: string (foreign key to Section, nullable)
  - progress_percentage: float (0-100)
  - started_at: datetime
  - completed_at: datetime (nullable)
  - last_accessed: datetime

### ChatSession
- **Description**: RAG chatbot interaction session
- **Fields**:
  - id: string (unique identifier)
  - user_id: string (foreign key to User, nullable for anonymous)
  - created_at: datetime
  - updated_at: datetime
  - context: string (selected text context for queries)

### ChatMessage
- **Description**: Individual message in a chat session
- **Fields**:
  - id: string (unique identifier)
  - session_id: string (foreign key to ChatSession)
  - role: enum (user, assistant)
  - content: text (message content)
  - sources: array of string (document references)
  - timestamp: datetime
  - context_type: enum (general, specific_text)

## Relationships

### Module ↔ Section
- One-to-Many: A Module has many Sections
- Module.id → Section.module_id

### Section ↔ CodeExample
- One-to-Many: A Section has many CodeExamples
- Section.id → CodeExample.section_id

### Section ↔ Exercise
- One-to-Many: A Section has many Exercises
- Section.id → Exercise.section_id

### User ↔ UserProgress
- One-to-Many: A User has many UserProgress records
- User.id → UserProgress.user_id

### Module ↔ UserProgress
- One-to-Many: A Module has many UserProgress records
- Module.id → UserProgress.module_id

### ChatSession ↔ ChatMessage
- One-to-Many: A ChatSession has many ChatMessages
- ChatSession.id → ChatMessage.session_id

## Validation Rules

### Module
- title: Required, minimum 3 characters, maximum 100 characters
- slug: Required, unique, URL-safe format
- order: Required, positive integer, unique within curriculum
- difficulty_level: Required, must be one of specified enum values

### Section
- title: Required, minimum 3 characters, maximum 100 characters
- slug: Required, unique within module, URL-safe format
- order: Required, positive integer, unique within module
- module_id: Required, must reference existing Module

### User
- email: Required, unique, valid email format
- role: Required, must be one of specified enum values

## State Transitions

### Module Status
- draft → review (when content is complete for review)
- review → published (when approved for public access)
- published → review (when updates are needed)

### UserProgress
- (No progress) → started (when user begins module)
- started → in_progress (when user actively engages)
- in_progress → completed (when user finishes module)