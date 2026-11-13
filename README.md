# ReportSaathi
### Making Healthcare Information Simple, Accessible, and Understandable.

**ReportSaathi** is a healthcare technology platform designed to bridge the gap between complex medical information and patient understanding.

Medical reports and prescriptions often contain technical terminology, unfamiliar abbreviations, and language barriers that make it difficult for patients to understand their health information.

ReportSaathi aims to simplify this experience by transforming complex healthcare information into clear, accessible, and patient-friendly explanations.

---

## 01. The Problem

Understanding medical reports should not be a privilege limited by medical knowledge or language proficiency.

Millions of patients face challenges such as:

- Difficulty interpreting laboratory test results.
- Unfamiliarity with medical terminology and abbreviations.
- Language barriers when reading medical documents.
- Limited understanding of prescriptions and medical instructions.
- Difficulty identifying information that requires professional medical attention.

These challenges can affect patients' ability to understand and communicate about their healthcare.

## 02. Our Solution

ReportSaathi aims to make healthcare information easier to understand through a simple, accessible, and patient-focused platform.

The project focuses on:

- Simplifying complex medical terminology.
- Making laboratory report information easier to interpret.
- Improving accessibility through language support.
- Presenting healthcare information in a structured format.
- Helping patients prepare informed questions for healthcare professionals.

## 03. Core Objectives

1. **Accessibility:** Reduce language and information barriers in healthcare.
2. **Simplicity:** Present complex medical information in understandable language.
3. **Awareness:** Help patients become more familiar with their health reports.
4. **Usability:** Provide a simple and intuitive user experience.
5. **Safety:** Encourage responsible interpretation and professional medical consultation.

## 04. Key Features

| Feature | Description |
|---|---|
| Medical Report Assistance | Helps users understand laboratory report information. |
| Simplified Explanations | Makes complex medical terminology easier to understand. |
| Language Accessibility | Aims to support users facing language barriers. |
| Patient-Friendly Interface | Provides a simple and accessible experience. |
| Health Information Awareness | Helps users understand relevant information in their documents. |

## 05. Technology Stack

| Layer | Technologies |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, FastAPI |
| Database | SQLite, SQLAlchemy |
| PDF Processing | PyPDF |
| Dependency Management | Poetry |
| Testing | Pytest |
| Code Quality | Ruff, MyPy |
| Version Control | Git, GitHub |
| Continuous Integration | GitHub Actions |
| Containerization | Docker |

## 06. System Architecture

The project follows a modular architecture that separates the frontend, backend, data management, and supporting services.

```text
              USER
                |
                v
       FRONTEND INTERFACE
                |
                v
          FASTAPI BACKEND
                |
        +-------+-------+
        |               |
        v               v
    API ROUTERS     BUSINESS LOGIC
        |               |
        +-------+-------+
                |
                v
          DATABASE LAYER
                |
                v
          STORED DATA
```

## 07. Repository Structure

```text
reportsaathi/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── backend/
│   ├── app/
│   │   ├── models/
│   │   │   ├── database.py
│   │   │   └── value.py
│   │   ├── routers/
│   │   │   ├── health.py
│   │   │   └── value.py
│   │   └── main.py
│   │
│   ├── tests/
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── poetry.lock
│
├── frontend/
│   └── index.html
│
├── docs/
│   ├── 01-problem.md
│   ├── 02-research.md
│   ├── 03-scope.md
│   ├── 04-design.md
│   ├── 05-prd.md
│   ├── 06-architecture.md
│   ├── 06a-api-contract.md
│   ├── 06b-safety-rules.md
│   ├── 07-test-plan.md
│   └── 08-tasks.md
│
├── tests/
│   └── fixtures/
│
├── .gitignore
└── README.md
```

## 08. Getting Started

### Prerequisites

Ensure the following are installed:

- Python 3.10 or later (below 3.13)
- Git
- Poetry
- Visual Studio Code (recommended)

### Installation

**Step 1 – Clone the repository**

```bash
git clone https://github.com/shettysakshi0901/reportsaathi.git
```

**Step 2 – Navigate to the project**

```bash
cd reportsaathi/backend
```

**Step 3 – Install dependencies**

```bash
python -m pip install poetry
poetry install
```

**Step 4 – Start the backend**

```bash
poetry run uvicorn app.main:app --reload
```

**Step 5 – Access the application API**

Backend:

http://127.0.0.1:8000

Interactive API documentation:

http://127.0.0.1:8000/docs

## 09. Testing and Code Quality

Run the following commands from the backend directory.

**Run automated tests**

```bash
poetry run pytest
```

**Run lint checks**

```bash
poetry run ruff check .
```

**Run static type checking**

```bash
poetry run mypy .
```

## 10. Project Documentation

The `docs/` directory contains the detailed technical and planning documentation.

- Problem Definition
- Research and Analysis
- Project Scope
- UI/UX Design
- Product Requirements Document
- System Architecture
- API Contract
- Safety Rules
- Test Plan
- Development Tasks

## 11. Future Enhancements

- Multilingual medical report explanations.
- Voice-based healthcare assistance.
- Improved prescription understanding.
- More comprehensive laboratory report interpretation.
- Accessible patient dashboards.
- Secure document management.
- Enhanced patient-focused healthcare communication.

## 12. Medical Disclaimer

ReportSaathi is intended to improve understanding of healthcare information. It is not a substitute for professional medical advice, diagnosis, or treatment. Users should consult qualified healthcare professionals before making medical decisions.

---

## Project Information

**Project Name:** ReportSaathi

**Domain:** Healthcare Technology

**Category:** Patient Information Accessibility

**Repository:** [GitHub – ReportSaathi](https://github.com/shettysakshi0901/reportsaathi)

---

<div align="center">

### ReportSaathi

**Understand Better. Stay Informed. Make Healthcare Accessible.**

*Bridging the gap between medical complexity and patient understanding.*

</div>
