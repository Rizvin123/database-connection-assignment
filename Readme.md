# University Records Management System

A desktop application developed in **Python**, **PyQt6**, and **SQLAlchemy** for managing university records. The system provides a modern graphical interface for maintaining students, lecturers, courses, staff, departments, research groups and executing analytical SQL queries against a MySQL database.

The project was developed using a layered architecture with a strong emphasis on maintainability, separation of concerns, and testability. Every layer of the application is independently tested using automated unit and GUI tests.

---

# Features

The application provides complete CRUD (Create, Read, Update, Delete) functionality for:

- Students
- Lecturers
- Courses
- Non-Academic Staff
- Research Groups

In addition, the application supports advanced reporting through five parameterised assignment queries including:

- Students enrolled in a selected course taught by a selected lecturer
- Final-year students above a selected average grade
- Students not enrolled in a selected semester
- Faculty advisor details
- Lecturer expertise search

---

# Software Architecture

The application follows a layered architecture.

```
GUI Layer
        │
        ▼
Service Layer
        │
        ▼
Repository Layer
        │
        ▼
SQLAlchemy ORM
        │
        ▼
MySQL Database
```

Each layer has a single responsibility and communicates only with the layer directly beneath it.

---

# Project Structure

```
src/
│
├── database/
│   ├── base.py
│   ├── session.py
│   ├── mixins.py
│   └── config.py
│
├── models/
│
├── repositories/
│
├── services/
│
├── gui/
│   ├── models/
│   ├── dialogs/
│   └── widgets/
│
└── main.py

tests/
├── repositories/
├── services/
└── gui/
```

---

# Installation

## Requirements
- Python 3 installed on your system  

## Steps to run the project

1. Download or clone the project  
2. Open the project folder  
3. Restore Database and ensure Mysql server is running on localhost:3306
4. Create .env with the following parameters
    DB_HOST=localhost
    DB_PORT=3306
    DB_NAME=university_records
    DB_USER=< Your SuperUser username >
    DB_PASSWORD=< Your SuperUser password >
5. Run the following command from root of the folder to use the application.

pip install -r requirements.txt (One time only, to download the dependencies)
python -m src.main (to run the application)

6. Run the following command to run each indiviual test suite.

pytest tests\test-folder\test-name.py

7. Run the following command to run all tests in the project

pytest -v

# Architectural Layers

## 1. Presentation Layer (PyQt6)

Responsible only for the graphical interface.

Contains:

- Widgets
- Dialogs
- Table Models

Responsibilities:

- Display data
- Receive user input
- Perform validation
- Call service methods
- Update tables

The GUI never communicates directly with SQLAlchemy models or executes SQL queries.

---

## 2. Service Layer

Acts as the business logic layer.

Responsibilities:

- Coordinate repository operations
- Perform validation
- Execute reporting queries
- Return domain objects to the GUI

Examples:

```
StudentService

LecturerService

CourseService

StaffService

ResearchGroupService

QueryService
```

The service layer hides all persistence logic from the user interface.

---

## 3. Repository Layer

Responsible only for data access.

Repositories encapsulate all SQLAlchemy operations.

Examples:

```
StudentRepository

LecturerRepository

CourseRepository

StaffRepository

ResearchGroupRepository
```

Responsibilities:

- CRUD operations
- Searching
- Filtering
- Persistence

The GUI never communicates directly with repositories.

---

## 4. ORM Layer

SQLAlchemy ORM maps Python objects directly to relational database tables.

Benefits include:

- Object-oriented programming
- Relationship management
- Automatic SQL generation
- Database independence

Relationships make navigation simple.

Example:

```
student.program

student.advisor

lecturer.department

course.enrollments
```

rather than manually writing joins throughout the application.

---

# Design Patterns Used

## Layered Architecture

The entire application follows a classic layered architecture.

Benefits:

- Loose coupling
- High cohesion
- Easier testing
- Easier maintenance

---

## Repository Pattern

Every entity has a dedicated repository.

Example:

```
StudentWidget

↓

StudentService

↓

StudentRepository

↓

Database
```

Benefits:

- Database logic isolated
- Easier unit testing
- Centralised queries
- Reusable persistence logic

---

## Service Layer Pattern

Business rules never exist inside the GUI.

Instead:

```
Widget

↓

Service

↓

Repository
```

This keeps business logic reusable and independent from the user interface.

---

## Model-View Architecture (Qt)

Qt's Model/View framework is used for every table.

Each module contains its own custom table model.

Examples:

```
StudentTableModel

LecturerTableModel

CourseTableModel

StaffTableModel

ResearchGroupTableModel

QueryTableModel
```

Benefits:

- Efficient rendering
- Automatic table refresh
- Separation between data and presentation

---

## Data Mapper Pattern

SQLAlchemy itself implements the Data Mapper pattern.

Unlike Active Record, ORM models contain no database logic.

Persistence is handled by the Session object.

---

## Dependency Injection

Repositories receive the database session through their constructors.

Example:

```python
StudentRepository(session)
```

Services receive repositories or sessions through constructors.

Widgets receive services.

This greatly improves testability.

---

## Composition over Inheritance

Widgets are composed from reusable Qt controls rather than relying on deep inheritance hierarchies.

Example:

```
QueriesWidget

├── QComboBox
├── QPushButton
├── QTableView
├── QLabel
└── QueryTableModel
```

---

## Single Responsibility Principle (SRP)

Every class has one clearly defined purpose.

Examples:

```
StudentRepository
```

Only accesses student data.

```
StudentService
```

Only contains student business logic.

```
StudentDialog
```

Only edits student information.

```
StudentWidget
```

Only presents student information.

---

# Object-Oriented Principles

The project follows the SOLID principles where appropriate.

## Single Responsibility Principle

Each class performs one responsibility.

## Open/Closed Principle

New modules can be added without modifying existing modules.

## Liskov Substitution Principle

Repository and service implementations maintain consistent interfaces.

## Interface Segregation Principle

Services expose only operations required by the GUI.

## Dependency Inversion Principle

The GUI depends on services rather than persistence implementations.

---

# Database Design

The database is fully normalised.

Characteristics include:

- Primary keys
- Foreign keys
- Composite primary keys
- Junction tables
- One-to-many relationships
- Many-to-many relationships
- Referential integrity
- Cascading updates
- Nullable foreign keys where appropriate

Examples include:

```
Student
    ↕
Programme

Student
    ↕
Advisor (Lecturer)

Student
    ↕
StudentCourseEnrollment
    ↕
Course

Lecturer
    ↕
ResearchGroup

Department
    ↕
ResearchGroup
```

---

# Query Module Design

The reporting subsystem differs from the CRUD modules.

```
QueriesWidget

↓

QueryService

↓

SQLAlchemy

↓

Database
```

Unlike CRUD modules, no repositories are used.

The widget dynamically changes its parameter controls based on the selected query.

The reporting table uses a generic table model capable of displaying heterogeneous result sets.

---

# Testing Strategy

Development followed a test-driven approach where possible.

Three levels of automated testing were implemented.

## Repository Tests

Validate persistence logic.

Examples:

- Create
- Read
- Update
- Delete
- Search
- Filtering

---

## Service Tests

Validate business logic independently of the GUI.

Examples:

- Student services
- Lecturer services
- Query services

---

## GUI Tests (pytest-qt)

End-to-end interaction testing.

Tests include:

- Widget creation
- Dialog behaviour
- CRUD operations
- Searching
- Filtering
- Query execution
- Table updates

The GUI is tested without manual interaction.

---

# Technologies Used

- Python 3
- PyQt6
- SQLAlchemy 2.x
- MySQL
- pytest
- pytest-qt

---

# Key Architectural Advantages

- Clear separation of responsibilities
- Highly modular design
- Easily extensible
- Minimal code duplication
- Testable at every layer
- ORM abstraction over SQL
- Consistent GUI architecture
- Reusable service and repository logic
- Scalable for additional university modules
- Clean mapping between relational data and Python objects

---

# Development Methodology

The project was developed incrementally.

For each module, the following workflow was adopted:

1. Database schema
2. SQLAlchemy ORM model
3. Repository implementation
4. Repository tests
5. Service implementation
6. Service tests
7. Dialog implementation
8. Widget implementation
9. GUI tests

This incremental process ensured that each layer was verified before progressing to the next, reducing integration issues and improving overall software quality.