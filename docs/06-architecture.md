# Technical Architecture & Systems Specification: ReportSaathi

**Document:** `docs/06-architecture.md`  
**Reference PRD:** `docs/05-prd.md`  
**Target Platform:** Lightweight Mobile Web / WhatsApp Webhook  
**Constraints:** Free and Open-Source Software (FOSS) only, zero vendor lock-in, low compute overhead  
**Date:** November 2026  

---

## 1. System Architecture Overview

ReportSaathi uses a **Single-Process Modular Architecture** designed for extreme simplicity, low latency, and zero operational data retention. The system is split strictly into **Deterministic Code** (for document validation, data parsing, range evaluation, and safety guardrails) and **AI Models** (for vision OCR of varied lab formats, plain-language metaphor synthesis, and Kannada speech generation).

```
                                  REPORTSAATHI SYSTEM TOPOLOGY
                                                │
                 [User Smartphone: 360px Mobile Browser or WhatsApp Client]
                                                │
                                         HTTPS / TLS 1.3
                                                ▼
         ┌─────────────────────────────────────────────────────────────────────────────┐
         │                       FASTAPI BACKEND SERVICE                               │
         │  ┌───────────────────────────────────────────────────────────────────────┐  │
         │  │ 1. Ingestion & File Type Verification (MIME, Magic Bytes, Blur Check)  │  │ [DETERMINISTIC]
         │  └───────────────────────────────────┬───────────────────────────────────┘  │
         │                                      ▼                                      │
         │  ┌───────────────────────────────────────────────────────────────────────┐  │
         │  │ 2. Document Classifier (Detects Prescription vs. Lab Report)          │  │ [DETERMINISTIC + AI]
         │  └───────────────────────────────────┬───────────────────────────────────┘  │
         │                                      ▼                                      │
         │  ┌───────────────────────────────────────────────────────────────────────┐  │
         │  │ 3. Text & Table Extraction (PyMuPDF / pdfplumber / Tesseract OCR)     │  │ [DETERMINISTIC + OCR]
         │  └───────────────────────────────────┬───────────────────────────────────┘  │
         │                                      ▼                                      │
         │  ┌───────────────────────────────────────────────────────────────────────┐  │
         │  │ 4. Deterministic Parameter & Lab Range Normalizer (Regex Engine)      │  │ [DETERMINISTIC]
         │  └───────────────────────────────────┬───────────────────────────────────┘  │
         │                                      ▼                                      │
         │  ┌───────────────────────────────────────────────────────────────────────┐  │
         │  │ 5. Vernacular Metaphor & Question Synthesizer (Open-Source LLM Engine)│  │ [AI MODEL]
         │  └───────────────────────────────────┬───────────────────────────────────┘  │
         │                                      ▼                                      │
         │  ┌───────────────────────────────────────────────────────────────────────┐  │
         │  │ 6. Clinical Safety Boundary Validator (Rule-Based Regex Guardrail)    │  │ [DETERMINISTIC]
         │  └───────────────────────────────────┬───────────────────────────────────┘  │
         │                                      ▼                                      │
         │  ┌───────────────────────────────────────────────────────────────────────┐  │
         │  │ 7. Kannada Speech Synthesizer (edge-tts / Piper TTS / Coqui)          │  │ [AI / TTS MODEL]
         │  └───────────────────────────────────┬───────────────────────────────────┘  │
         │                                      ▼                                      │
         │  ┌───────────────────────────────────────────────────────────────────────┐  │
         │  │ 8. Ephemeral Session Manager (In-Memory TTL Cache - 15-Minute Purge)  │  │ [DETERMINISTIC]
         │  └───────────────────────────────────────────────────────────────────────┘  │
         └─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Technology Stack Evaluation & Recommendation

To maintain maximum development velocity, zero cloud lock-in, and minimal runtime complexity, we evaluate two full-stack options:

### Stack Option A: Python FastAPI + HTMX / TailwindCSS (Recommended)
* **Backend:** Python 3.12+ with FastAPI (Async, Pydantic validation, native support for Python scientific and NLP libraries).
* **Frontend:** Server-Rendered HTML via Jinja2 + HTMX (rich dynamic swaps without SPA JavaScript bloat) + TailwindCSS (compiled utility CSS < 15 KB).
* **Data Processing & OCR:** `PyMuPDF` (fitz) for instant vector PDF parsing + `pdfplumber` for tabular data + `pytesseract` / Open-Source Tesseract for scanned photos.
* **LLM / Generation:** Local open-source Ollama (Llama-3-8B-Instruct or Gemma-2-9B) OR Free-Tier Gemini API / Groq API (Llama 3 70B fast inference).
* **Audio Synthesis:** `edge-tts` (Free, high-quality neural Kannada voice `kn-IN-GaganNeural` / `kn-IN-SapnaNeural`) with local `Piper TTS` fallback.
* **State / Cache:** Python in-memory `cachetools.TTLCache` (Zero database required for MVP).

### Stack Option B: Next.js (React) + Node.js + Python Microservice
* **Frontend:** Next.js 15 (React, TypeScript, App Router).
* **Backend:** Node.js API routes delegating OCR and NLP tasks to a secondary Python FastAPI microservice.
* **Data Processing:** Tesseract.js in Node, or external OCR APIs.
* **Database:** PostgreSQL with Prisma ORM.

### Comparison & Selection Rationale

| Evaluation Criteria | Option A: FastAPI + HTMX | Option B: Next.js + Python Microservice | Verdict |
| :--- | :--- | :--- | :--- |
| **Architectural Simplicity** | **Single process, single language (Python).** Zero API glue, zero microservice networking overhead. | Two runtimes (Node.js + Python), multiple deployment targets, cross-service RPC overhead. | **Option A wins decisively.** |
| **Client Bundle Size (Low-End Android)** | **< 35 KB total payload.** Pure HTML streamed over the wire; no React hydration lag on slow 2GB RAM phones. | 250 KB – 500 KB JavaScript bundle; high initial parsing delay on cheap budget processors. | **Option A wins decisively.** |
| **Python Ecosystem Synergy** | Native integration with `PyMuPDF`, `PIL`, `tesseract`, `edge-tts`, and local LLM runtimes in one memory space. | Requires serializing files and images over internal HTTP bridges between Node and Python. | **Option A wins.** |
| **Cost & Hosting Footprint** | Can run comfortably on a single free or $4/mo virtual server (Docker container, 1GB RAM). | Requires multi-container orchestration or multiple serverless hosting environments. | **Option A wins.** |

> **Recommendation:** **Stack Option A (FastAPI + HTMX + Tailwind)** is selected. It completely eliminates client-side JavaScript execution lag on older Android devices, provides native access to Python's medical NLP and PDF extraction libraries, and runs as a single lightweight container.

---

## 3. Deterministic Code vs. AI Model Partitioning

A foundational architectural requirement is maintaining strict boundaries between deterministic procedural logic and probabilistic AI inference.

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                          DETERMINISTIC CODE vs. AI MODEL PARTITIONING                             │
├─────────────────────────────────────────────────┬─────────────────────────────────────────────────┤
│ DETERMINISTIC PROCEDURAL CODE (100% Predictable)│ PROBABILISTIC AI MODELS (Controlled & Bounded)  │
├─────────────────────────────────────────────────┼─────────────────────────────────────────────────┤
│ • File upload validation & magic-byte check     │ • Document Classifier: Lab Report vs.           │
│ • Image blur, glare & aspect ratio thresholds   │   Handwritten Prescription vision check.        │
│ • Digital PDF text extraction & grid alignment  │ • Multimodal OCR: Parsing non-standard scanned  │
│ • Biomarker regex matching (FBS, HbA1c, etc.)   │   paper lab sheets with distorted tables.       │
│ • Normalization of units (mg/dL, %, mmol/L)     │ • Colloquial Jargon Translation: Converting     │
│ • Range comparison: Observed vs Printed Limit   │   extracted terms into Kannada analogies.       │
│ • Safety Rule Engine: Regex blocking of         │ • Doctor Question Generator: Generating 3 visit │
│   diagnostic claims and dosage instructions.    │   questions based on extracted range states.    │
│ • DPDP 15-minute ephemeral memory purging.      │ • Neural TTS: Synthesizing natural spoken       │
│ • Audio file serving & rate-limiting.           │   Kannada audio voice notes.                    │
└─────────────────────────────────────────────────┴─────────────────────────────────────────────────┘
```

---

## 4. Ephemeral Data Model (In-Memory Only)

Under India's DPDP Act (2023) and privacy-by-design principles, ReportSaathi **does not persist patient health data in a database**. All session data is stored in an ephemeral, memory-safe data structure backed by a strict **15-minute Time-To-Live (TTL)**.

### 4.1 In-Memory Session Entity (`SessionState`)

```python
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class BiomarkerResult(BaseModel):
    parameter_id: str                      # e.g., "hba1c", "fbs", "creatinine"
    canonical_name_en: str                 # e.g., "Glycated Hemoglobin"
    display_name_kn: str                   # e.g., "HbA1c (ಕಳೆದ 3 ತಿಂಗಳ ಸಕ್ಕರೆ ನೆನಪು)"
    observed_value: float                  # e.g., 7.8
    unit: str                              # e.g., "%"
    reference_low: Optional[float] = None  # e.g., 4.0
    reference_high: Optional[float] = None # e.g., 5.6
    range_status: str                      # "IN_RANGE" | "ABOVE_RANGE" | "BELOW_RANGE" | "UNKNOWN"
    plain_language_explanation_kn: str     # e.g., "ನಿಮ್ಮ 3 ತಿಂಗಳ ಸಕ್ಕರೆ ಸರಾಸರಿ ಮಿತಿಗಿಂತ ಹೆಚ್ಚಾಗಿದೆ."

class DoctorQuestion(BaseModel):
    question_id: int                       # 1, 2, 3
    question_kn: str                       # e.g., "ನನ್ನ ಆಹಾರ ಪದ್ಧತಿಯಲ್ಲಿ ಏನು ಬದಲಾವಣೆ ಬೇಕು?"
    question_en: str                       # Clinical translation for doctor review

class SessionState(BaseModel):
    session_id: str                        # UUID4 string
    created_at: datetime = Field(default_factory=datetime.utcnow)
    consent_granted: bool = False
    consent_timestamp: Optional[datetime] = None
    document_type: str = "UNKNOWN"         # "LAB_REPORT" | "PRESCRIPTION" | "UNREADABLE"
    is_prescription_detected: bool = False
    rejection_reason_kn: Optional[str] = None
    biomarkers: List[BiomarkerResult] = []
    doctor_questions: List[DoctorQuestion] = []
    audio_file_path: Optional[str] = None  # Ephemeral path in /tmp/
    audio_duration_seconds: float = 0.0
```

### 4.2 Ephemeral Lifecycle (15-Minute Garbage Collection Worker)
* Uploaded raw files are staged in `/tmp/reportsaathi_ephemeral/{session_id}/`.
* Once processing finishes, the client receives the generated response and audio stream.
* An asynchronous background thread (`asyncio.create_task`) monitors the cache:
  ```python
  # Every 60 seconds, purge all sessions older than 15 minutes:
  # 1. Delete /tmp/ file directory from disk.
  # 2. Invalidate SessionState in in-memory TTLCache.
  # 3. Explicitly overwrite memory references to ensure zero data retention.
  ```

---

## 5. API Routes & Endpoints Specification

All endpoints communicate over HTTPS with standard JSON or streaming multipart responses.

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   REPORTSAATHI REST API SURFACE                                   │
├────────┬─────────────────────────────┬────────────────────────────────────────────────────────────┤
│ METHOD │ ROUTE                       │ PURPOSE & PAYLOAD                                          │
├────────┼─────────────────────────────┼────────────────────────────────────────────────────────────┤
│ GET    │ /                           │ Render Screen 1 (Welcome & Upload UI via Jinja2/HTMX).     │
│ POST   │ /api/v1/upload              │ Multipart file upload; executes validation & returns ID.   │
│ GET    │ /consent/{session_id}       │ Render Screen 2 (DPDP Consent screen & thumbnail).         │
│ POST   │ /api/v1/consent/confirm     │ Affirmative consent payload; triggers processing pipeline. │
│ GET    │ /process/{session_id}       │ Render Screen 3 (Processing progress hub with polling).    │
│ GET    │ /api/v1/status/{session_id} │ Polling endpoint checking extraction & audio status.       │
│ GET    │ /result/{session_id}        │ Render Screen 4 (Final explanation, cards & questions).    │
│ GET    │ /api/v1/audio/{session_id}  │ Stream synthesized Opus/AAC Kannada audio file.            │
│ GET    │ /rejection/{session_id}     │ Render Screen 5 (Safety rejection UI for prescriptions).   │
│ POST   │ /api/v1/whatsapp/webhook    │ Ingestion webhook for WhatsApp Business API integration.   │
└────────┴─────────────────────────────┴────────────────────────────────────────────────────────────┘
```

### Detailed Route Specifications

#### 1. `POST /api/v1/upload`
* **Request:** `multipart/form-data` containing `file: Binary`, `file_type: string`.
* **Processing:** Validates magic bytes, checks file size (≤ 10 MB), generates `session_id`, runs quick document classifier.
* **Response (Success - 200 OK):**
  ```json
  {
    "status": "SUCCESS",
    "session_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
    "document_type": "LAB_REPORT",
    "redirect_url": "/consent/9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d"
  }
  ```
* **Response (Prescription Detected - 200 OK):**
  ```json
  {
    "status": "REJECTED",
    "session_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
    "document_type": "PRESCRIPTION",
    "redirect_url": "/rejection/9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d"
  }
  ```

#### 2. `POST /api/v1/consent/confirm`
* **Request:** `application/json`
  ```json
  {
    "session_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
    "consent_granted": true,
    "language": "kn"
  }
  ```
* **Processing:** Records consent timestamp, triggers async extraction & speech generation task in background.
* **Response:** `{"status": "PROCESSING", "next_url": "/process/{session_id}"}`

#### 3. `GET /api/v1/status/{session_id}`
* **Response (In Progress):** `{"progress_step": 2, "message_kn": "ಅಳತೆಗಳನ್ನು ಪರಿಶೀಲಿಸಲಾಗುತ್ತಿದೆ..."}`
* **Response (Completed):** `{"progress_step": 3, "status": "COMPLETED", "result_url": "/result/{session_id}"}`

#### 4. `GET /api/v1/audio/{session_id}`
* **Response:** Binary audio stream `audio/ogg; codecs=opus` or `audio/mp4` with `Accept-Ranges: bytes` support.

---

## 6. Third-Party Services & FOSS Tool Integrations

Strict adherence to free and open-source software (FOSS) and free-tier compliant services:

| Capability | Recommended Open-Source Tool / Free Service | License / Tier | Role in ReportSaathi |
| :--- | :--- | :--- | :--- |
| **PDF Extraction** | `PyMuPDF` (Fitz) & `pdfplumber` | AGPL-3.0 / MIT | Extracts native digital text and tabular coordinates with 99.8% fidelity from digital lab PDFs. |
| **OCR (Scanned Images)** | `Tesseract OCR 5.x` (`pytesseract`) | Apache-2.0 | Free, self-hosted open-source OCR engine for scanned paper photos. |
| **LLM Inference** | **Local:** `Ollama` (Llama-3-8B-Instruct or Gemma-2-9B)<br>**Cloud Fallback:** Groq Free Tier / Gemini API Free Tier | FOSS / Free developer tier | Transforms structured tabular parameters into plain conversational Kannada explanations and questions. |
| **Kannada Speech (TTS)** | `edge-tts` (Microsoft Neural TTS wrapper) with local `Piper TTS` fallback | MIT / FOSS | Generates human-like, warm spoken Kannada audio (`kn-IN-GaganNeural`, `kn-IN-SapnaNeural`) with zero API cost. |
| **Messaging (WhatsApp)** | Meta WhatsApp Cloud API | Free 1,000 service conversations/month | Delivers audio voice notes and visual report cards directly to patient WhatsApp chats. |
| **Maps & Geolocation** | **NONE NEEDED (Explicitly Excluded)** | N/A | Maps and user location tracking are strictly excluded to preserve privacy and minimize data scope. |

---

## 7. Deployment, Hosting & Environment Configuration

### 7.1 Containerized Deployment (`Dockerfile`)
The entire application builds as a single self-contained Docker container (~450 MB compressed) that can run on any Linux environment:

```dockerfile
FROM python:3.12-slim-bookworm

# Install system dependencies (Tesseract OCR, Kannada font packages, ffmpeg)
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-kan \
    fonts-noto-core \
    fonts-noto-ui-core \
    fonts-noto-extra \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
```

### 7.2 Hosting Options (Zero-Cost / Low-Cost)
1. **Render.com (Free Tier) / Fly.io (Free Tier):** Easily hosts the containerized FastAPI web app with HTTPS and auto-sleep/wake capabilities for initial user testing.
2. **Hugging Face Spaces (Free Docker Space):** Provides free 16 GB RAM CPU instances suitable for running both FastAPI and local Ollama/Piper TTS models.
3. **Cheap Self-Hosted VPS (Hetzner / DigitalOcean $4–$6/mo):** Ideal for pilot production in Karnataka with full data sovereignty within Indian geography.

### 7.3 Environment Variables Specification (`.env.example`)

```bash
# ==========================================
# ReportSaathi Environment Configuration
# ==========================================

# Application Settings
ENVIRONMENT=production
DEBUG=false
APP_HOST=0.0.0.0
APP_PORT=8000
SECRET_KEY=change-this-to-a-secure-random-32-char-string

# Ephemeral Storage Settings
EPHEMERAL_STORAGE_PATH=/tmp/reportsaathi_ephemeral
SESSION_TTL_MINUTES=15
MAX_UPLOAD_SIZE_MB=10

# AI & LLM Inference Settings
# Options: "gemini_free", "groq_free", "ollama_local"
LLM_PROVIDER=gemini_free
GEMINI_API_KEY=your_free_tier_gemini_api_key_here
GROQ_API_KEY=your_free_tier_groq_api_key_here
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=gemma2:9b

# Speech Synthesis (TTS) Settings
# Options: "edge_tts", "piper_local"
TTS_PROVIDER=edge_tts
KANNADA_VOICE=kn-IN-GaganNeural
KANNADA_DEFAULT_SPEED=+0%
KANNADA_SLOW_SPEED=-15%

# WhatsApp Cloud API (Optional - for WhatsApp Bot Mode)
WHATSAPP_ENABLED=false
WHATSAPP_VERIFY_TOKEN=your_custom_webhook_verify_token
WHATSAPP_API_TOKEN=your_meta_cloud_api_token
WHATSAPP_PHONE_NUMBER_ID=your_meta_phone_id
```

---

## 8. Open Questions & Technical Unknowns

Rather than guessing or making assumptions, the following questions are flagged for engineering resolution during Phase 1 sprint testing:

1. **OCR Reliability on Thermal Paper & Carbon Copies:** While digital PDFs from Dr Lal or Agilus parse with >99% accuracy, many rural government clinics in Karnataka issue lab results on low-contrast thermal paper slips or carbon copies. *We need to benchmark Tesseract vs. lightweight vision models on a test set of 50 physical clinic slips.*
2. **Offline Audio Playback on Ultra-Low-End Android Browsers:** Certain budget Android Go devices disable MediaSource Extensions or restrict audio playback codecs. *We must test whether raw WAV or compressed AAC (.m4a) streams more reliably across ancient versions of Android Chrome.*
3. **Edge-TTS Availability & Rate Limiting:** While `edge-tts` provides exceptional Kannada voices for free, it depends on public endpoint uptime. *We must benchmark the audio quality and inference latency of fully self-hosted Piper TTS models running on CPU as an air-gapped backup.*
4. **WhatsApp Interactive Media Webhook Latency:** If WhatsApp bot mode is deployed, Meta's webhook requires an immediate 200 OK within 3 seconds, while extraction and speech synthesis takes 6–10 seconds. *We must implement an asynchronous two-message workflow (Message 1: "ವರದಿ ಓದಲಾಗುತ್ತಿದೆ...", Message 2: Voice Note + Summary Card).*
