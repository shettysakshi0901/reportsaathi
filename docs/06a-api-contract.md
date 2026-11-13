# API Contract & Schema Specification: ReportSaathi

**Document:** `docs/06a-api-contract.md`  
**Reference Architecture:** `docs/06-architecture.md`  
**Target Specification:** OpenAPI 3.1 / REST JSON  
**Version:** 1.0.0 (MVP)  
**Date:** November 2026  

---

## 1. Global Specifications & Conventions

* **Base URL:** `https://api.reportsaathi.in` (Production) / `http://localhost:8000` (Local Dev)
* **Transport Protocol:** HTTPS / TLS 1.3 mandatory.
* **Content-Type:** `application/json` (default), `multipart/form-data` (file upload), `audio/ogg; codecs=opus` / `audio/mp4` (audio streams).
* **Character Encoding:** UTF-8 mandatory across all Kannada and English payloads.
* **Session Identifier:** Standard RFC 4122 UUIDv4 strings (*e.g., `9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d`*).
* **Statutory Privacy Constraint:** All session data is stored exclusively in ephemeral memory with an automated 15-minute Time-To-Live (TTL).

---

## 2. Global Error Envelope Schema

All API errors return standard RFC 7807 Problem Details JSON:

```json
{
  "type": "https://reportsaathi.in/errors/INVALID_FILE_TYPE",
  "title": "Invalid File Format",
  "status": 400,
  "detail_en": "Uploaded file must be a PDF or image (.jpg, .png, .webp).",
  "detail_kn": "ಅಪ್‌ಲೋಡ್ ಮಾಡಿದ ಫೈಲ್ PDF ಅಥವಾ ಚಿತ್ರ (.jpg, .png) ಆಗಿರಬೇಕು.",
  "session_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "timestamp": "2026-11-13T08:30:00Z"
}
```

---

## 3. Endpoints Contract Specification

### 3.1 Document Ingestion: `POST /api/v1/upload`
Accepts a digital lab report PDF or smartphone photo, validates magic bytes, verifies file size, runs initial document classification, and returns a session token.

* **Request Format:** `multipart/form-data`
* **Form Fields:**
  * `file` (Binary, Required): The lab report file. Max 10 MB.
  * `client_language` (String, Optional): Default `"kn"`. ISO 639-1 code.
* **Headers:** `Content-Type: multipart/form-data`

#### Responses

##### `200 OK` (Standard Lab Report Detected)
```json
{
  "status": "SUCCESS",
  "session_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "document_type": "LAB_REPORT",
  "file_metadata": {
    "filename": "drlal_sugar_test.pdf",
    "mime_type": "application/pdf",
    "size_bytes": 348210,
    "page_count": 1
  },
  "redirect_url": "/consent/9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "expires_at": "2026-11-13T08:45:00Z"
}
```

##### `200 OK` (Prescription Detected — Safety Trigger)
```json
{
  "status": "REJECTED",
  "session_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "document_type": "PRESCRIPTION",
  "rejection_code": "HANDWRITTEN_PRESCRIPTION_BLOCKED",
  "rejection_message_kn": "ಇದು ವೈದ್ಯರ ಕೈಬರಹದ ಚೀಟಿಯಾಗಿದೆ. ಸುರಕ್ಷತೆಯ ದೃಷ್ಟಿಯಿಂದ ನಾವು ಕೇವಲ ಲ್ಯಾಬ್ ವರದಿಗಳನ್ನು ಮಾತ್ರ ವಿವರಿಸುತ್ತೇವೆ.",
  "rejection_message_en": "Handwritten prescription detected. For clinical safety, only printed lab reports are supported.",
  "redirect_url": "/rejection/9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d"
}
```

##### `400 Bad Request` (File Format / Blur Failure)
```json
{
  "type": "https://reportsaathi.in/errors/FILE_BLURRY_OR_CORRUPT",
  "title": "Image Quality Failure",
  "status": 400,
  "detail_en": "Image is blurry or numbers are cut off. Please retake photo.",
  "detail_kn": "ಫೋಟೋ ಮಬ್ಬಾಗಿದೆ ಅಥವಾ ಅಕ್ಷರಗಳು ಕಾಣಿಸುತ್ತಿಲ್ಲ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಸ್ಪಷ್ಟವಾಗಿ ಫೋಟೋ ತೆಗೆಯಿರಿ.",
  "session_id": null
}
```

##### `413 Payload Too Large`
```json
{
  "type": "https://reportsaathi.in/errors/FILE_TOO_LARGE",
  "title": "File Exceeds Size Limit",
  "status": 413,
  "detail_en": "Uploaded file exceeds maximum limit of 10 MB.",
  "detail_kn": "ಫೈಲ್ ಗಾತ್ರವು 10 MB ಗಿಂತ ಹೆಚ್ಚಾಗಿದೆ."
}
```

---

### 3.2 Statutory Consent Confirmation: `POST /api/v1/consent/confirm`
Records affirmative consent under Section 5(3) and 6(3) of DPDP Act 2023, unlocking document processing.

* **Request Format:** `application/json`
* **Request Body:**
  ```json
  {
    "session_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
    "consent_granted": true,
    "language": "kn",
    "consent_version": "2026-v1-dpdp"
  }
  ```

#### Responses

##### `200 OK` (Processing Triggered)
```json
{
  "status": "PROCESSING",
  "session_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "consent_timestamp": "2026-11-13T08:30:15Z",
  "progress_url": "/process/9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d"
}
```

##### `403 Forbidden` (Consent Withheld or Refused)
```json
{
  "type": "https://reportsaathi.in/errors/CONSENT_REQUIRED",
  "title": "Processing Refused",
  "status": 403,
  "detail_en": "Affirmative consent required to process medical document.",
  "detail_kn": "ವರದಿಯನ್ನು ಪರಿಶೀಲಿಸಲು ನಿಮ್ಮ ಸಮ್ಮತಿ ಅಗತ್ಯವಿದೆ."
}
```

##### `404 Not Found` (Session Expired / Purged)
```json
{
  "type": "https://reportsaathi.in/errors/SESSION_EXPIRED",
  "title": "Session Purged",
  "status": 404,
  "detail_en": "Session has expired and health data has been permanently purged.",
  "detail_kn": "15 ನಿಮಿಷಗಳ ಅವಧಿ ಮೀರಿದೆ. ದಯವಿಟ್ಟು ವರದಿಯನ್ನು ಮತ್ತೆ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ."
}
```

---

### 3.3 Extraction & Synthesis Status: `GET /api/v1/status/{session_id}`
Polling endpoint used by Screen 3 to track pipeline progress.

* **Path Parameters:** `session_id` (UUIDv4)
* **Headers:** `Accept: application/json`

#### Responses

##### `200 OK` (In Progress)
```json
{
  "session_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "status": "PROCESSING",
  "step": 2,
  "total_steps": 3,
  "step_label_en": "Analyzing sugar and blood pressure markers against lab limits",
  "step_label_kn": "ಅಳತೆಗಳನ್ನು ಲ್ಯಾಬ್ ಮಿತಿಗಳಿಗೆ ಪರಿಶೀಲಿಸಲಾಗುತ್ತಿದೆ..."
}
```

##### `200 OK` (Completed Successfully)
```json
{
  "session_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "status": "COMPLETED",
  "step": 3,
  "total_steps": 3,
  "result_url": "/result/9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "audio_url": "/api/v1/audio/9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d"
}
```

---

### 3.4 Report Results Payload: `GET /api/v1/result/{session_id}`
Fetches the extracted biomarkers, plain-language explanations, range evaluations, and the 3 doctor questions.

* **Path Parameters:** `session_id` (UUIDv4)

#### Response: `200 OK`
```json
{
  "session_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "status": "COMPLETED",
  "audio": {
    "stream_url": "/api/v1/audio/9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
    "duration_seconds": 58.2,
    "language": "kn-IN",
    "voice_name": "kn-IN-GaganNeural"
  },
  "biomarkers": [
    {
      "parameter_id": "hba1c",
      "canonical_name_en": "Glycated Hemoglobin (HbA1c)",
      "display_name_kn": "HbA1c (ಕಳೆದ 3 ತಿಂಗಳ ಸಕ್ಕರೆ ನೆನಪು)",
      "observed_value": 7.8,
      "unit": "%",
      "reference_interval": {
        "low": 4.0,
        "high": 5.6,
        "source": "PRINTED_ON_LAB_REPORT"
      },
      "range_status": "ABOVE_RANGE",
      "status_label_kn": "ಸಾಮಾನ್ಯಕ್ಕಿಂತ ಹೆಚ್ಚು",
      "status_label_en": "Above Reference Range",
      "status_badge_color": "AMBER",
      "is_critical": false,
      "plain_explanation_kn": "ಕಳೆದ ೯೦ ದಿನಗಳಲ್ಲಿ ರಕ್ತದಲ್ಲಿನ ಸಕ್ಕರೆ ಸರಾಸರಿ ೭.೮% ಬಂದಿದೆ. ಇದು ಲ್ಯಾಬ್‌ನ ಸಾಮಾನ್ಯ ಮಿತಿಗಿಂತ ಹೆಚ್ಚಾಗಿದೆ."
    },
    {
      "parameter_id": "fbs",
      "canonical_name_en": "Fasting Blood Sugar (FBS)",
      "display_name_kn": "ಉಪವಾಸದ ಸಕ್ಕರೆ (Fasting Sugar)",
      "observed_value": 142.0,
      "unit": "mg/dL",
      "reference_interval": {
        "low": 70.0,
        "high": 100.0,
        "source": "PRINTED_ON_LAB_REPORT"
      },
      "range_status": "ABOVE_RANGE",
      "status_label_kn": "ಸಾಮಾನ್ಯಕ್ಕಿಂತ ಹೆಚ್ಚು",
      "status_label_en": "Above Reference Range",
      "status_badge_color": "AMBER",
      "is_critical": false,
      "plain_explanation_kn": "ಬೆಳಿಗ್ಗೆ ಉಪವಾಸವಿದ್ದಾಗ ರಕ್ತದಲ್ಲಿರುವ ಸಕ್ಕರೆ ಮಟ್ಟವು ಲ್ಯಾಬ್ ನಿಗದಿಪಡಿಸಿದ ಮಿತಿಗಿಂತ ಹೆಚ್ಚಾಗಿದೆ."
    },
    {
      "parameter_id": "creatinine",
      "canonical_name_en": "Serum Creatinine",
      "display_name_kn": "ಸೀರಮ್ ಕ್ರಿಯೇಟಿನೈನ್ (ಕಿಡ್ನಿ ಶುದ್ಧತೆ)",
      "observed_value": 0.9,
      "unit": "mg/dL",
      "reference_interval": {
        "low": 0.7,
        "high": 1.2,
        "source": "PRINTED_ON_LAB_REPORT"
      },
      "range_status": "IN_RANGE",
      "status_label_kn": "ಸಾಮಾನ್ಯ ಮಿತಿಯಲ್ಲಿದೆ",
      "status_label_en": "In Normal Range",
      "status_badge_color": "GREEN",
      "is_critical": false,
      "plain_explanation_kn": "ಮೂತ್ರಪಿಂಡಗಳು ರಕ್ತವನ್ನು ಸರಿಯಾಗಿ ಶುದ್ಧೀಕರಿಸುತ್ತಿವೆ. ಈ ಅಳತೆ ಸಾಮಾನ್ಯ ಮಿತಿಯಲ್ಲಿದೆ."
    }
  ],
  "doctor_questions": [
    {
      "id": 1,
      "question_kn": "ನನ್ನ HbA1c 7.8% ಇರುವುದರಿಂದ ನನ್ನ ಆಹಾರ ಪದ್ಧತಿ ಅಥವಾ ದಿನಚರಿಯಲ್ಲಿ ಏನು ಬದಲಾವಣೆ ಬೇಕು?",
      "question_en": "Given my HbA1c is 7.8%, what changes do I need in my daily routine or diet?"
    },
    {
      "id": 2,
      "question_kn": "ನನ್ನ ಸಕ್ಕರೆ ಮಟ್ಟ ಹೆಚ್ಚಿರುವುದರಿಂದ ಪ್ರಸ್ತುತ ತೆಗೆದುಕೊಳ್ಳುತ್ತಿರುವ ಔಷಧಿಗಳನ್ನು ಪರಿಶೀಲಿಸಬೇಕೇ?",
      "question_en": "Do my current medications need any clinical review based on these glucose numbers?"
    },
    {
      "id": 3,
      "question_kn": "ಮುಂದಿನ ರಕ್ತ ಪರೀಕ್ಷೆಯನ್ನು ನಾನು ಎಷ್ಟು ತಿಂಗಳ ನಂತರ ಮಾಡಿಸಬೇಕು?",
      "question_en": "After how many months should I repeat this HbA1c test?"
    }
  ],
  "statutory_disclaimer_kn": "ವರದಿ ಸಾಥಿ ಕೇವಲ ಶೈಕ್ಷಣಿಕ ಮಾಹಿತಿಯಾಗಿದೆ; ಇದು ವೈದ್ಯರ ವೈದ್ಯಕೀಯ ತಪಾಸಣೆ ಅಥವಾ ಚಿಕಿತ್ಸೆಗೆ ಬದಲಿಯಲ್ಲ."
}
```

---

### 3.5 Spoken Audio Streaming: `GET /api/v1/audio/{session_id}`
Streams the binary synthesized audio file directly to the client player.

* **Path Parameters:** `session_id` (UUIDv4)
* **Supported Request Headers:** `Range: bytes=0-`
* **Response Headers:**
  * `Content-Type: audio/ogg; codecs=opus` or `audio/mp4`
  * `Content-Length: 68420`
  * `Accept-Ranges: bytes`
  * `Cache-Control: no-store, no-cache, must-revalidate` (Prevents disk caching of health voice note)

---

### 3.6 WhatsApp Business Webhook: `POST /api/v1/whatsapp/webhook`
Webhook integration receiver for Meta WhatsApp Cloud API.

* **Headers:** `X-Hub-Signature-256: sha256=...` (HMAC signature verification)
* **Payload Structure:** Standard Meta WhatsApp incoming message event with media payload (`document` or `image`).
* **Behavior:**
  1. Verifies HMAC-SHA256 signature against `WHATSAPP_API_TOKEN`.
  2. Extracts media ID, downloads binary image from Meta Graph API.
  3. Returns immediate HTTP `200 OK` within 1.5 seconds.
  4. Triggers background async task to extract biomarkers and synthesize Kannada voice.
  5. Replies asynchronously to patient's WhatsApp chat with a voice note `.ogg` file and text question summary.
