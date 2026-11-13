# Clinical Safety Guardrails & Regulatory Compliance Engine

**Document:** `docs/06b-safety-rules.md`  
**Associated Documents:** `docs/05-prd.md`, `docs/06-architecture.md`, `docs/03-scope.md`  
**Governing Statutory Frameworks:**  
* National Medical Commission (NMC) Telemedicine Practice Guidelines, 2020  
* CDSCO Medical Devices Rules (SaMD Guidance Doc No. CDSCO/MD/GD/MDSW/01/2026)  
* Digital Personal Data Protection Act (DPDP Act), 2023  
* Drugs and Magic Remedies (Objectionable Advertisements) Act, 1954  
**Date:** November 2026  

---

## 1. Safety Architecture & Multi-Layer Defense

Clinical safety in ReportSaathi is not left to conversational prompting alone. It is enforced through a **Four-Stage Defense-in-Depth Pipeline**:

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               FOUR-STAGE CLINICAL SAFETY PIPELINE                                 │
├─────────────────────┬─────────────────────┬─────────────────────┬─────────────────────────────────┤
│ STAGE 1: INGESTION  │ STAGE 2: PARSING    │ STAGE 3: SYNTHESIS  │ STAGE 4: OUTPUT AUDIT           │
│ Input Classification│ Range Normalization │ Controlled LLM      │ Deterministic Regex Gate        │
│ & Prescription Gate │ & Lab Interval Lock │ Bounded Prompting   │ & Blacklist Guardrail           │
├─────────────────────┼─────────────────────┼─────────────────────┼─────────────────────────────────┤
│ • Rejects doctor    │ • Locks strictly to │ • Non-diagnostic    │ • Scans generated text for      │
│   handwriting.      │   printed lab       │   system prompt.    │   forbidden words.              │
│ • Rejects blurry    │   reference range.  │ • Fixed Kannada     │ • Strips clinical diagnoses.    │
│   or cut-off files. │ • Rejects guessing. │   metaphor anchors. │ • Strips dosage advice.         │
└─────────────────────┴─────────────────────┴─────────────────────┴─────────────────────────────────┘
```

---

## 2. Stage 1: Document Classification & Prescription Rejection Rules

### 2.1 The Prescription Rejection Rule (Rule SR-DOC-1)
* **Rule:** If an uploaded image or document is classified as a handwritten doctor prescription, outpatient clinic consultation sheet, or medication dispensing slip, it **must be rejected immediately without attempting OCR or interpretation**.
* **Detection Criteria (Multi-Factor Scoring):**
  1. *Cursive Handwriting Ratio:* If handwriting detector identifies > 30% cursive stroke patterns.
  2. *Rx Symbol / Clinic Letterhead:* Visual detection of `Rx`, `Dr.`, `MBBS`, `MD`, `Clinic`, `Hospital OPD` headers paired with handwritten medicine lines.
  3. *Absence of Lab Grid Headers:* Lack of standard tabular columns (`Test Name`, `Observed Value`, `Biological Reference Interval`, `Units`).
* **Trigger Action:**
  * Immediate HTTP redirect to Screen 5 (`/rejection/{session_id}`).
  * Playback of standardized Kannada Audio Rejection Notice (Audio Script KS-REJ-01).
  * Logging of document type as `PRESCRIPTION_BLOCKED` (zero PII logged).

### 2.2 Image Quality & Legibility Thresholds (Rule SR-DOC-2)
* **Blur Threshold:** Laplacian variance algorithm score < 100.0 flags image as severely blurred.
* **Resolution Threshold:** Minimum image width/height of 800px × 800px; DPI equivalent ≥ 150 DPI.
* **Cut-Off Detection:** If parameter names are detected but corresponding value/unit columns fall outside the visible image frame, flag as `IMAGE_TRUNCATED`.
* **Trigger Action:**
  * Displays friendly camera guideline frame in Screen 5.
  * Audio prompt: *"ವರದಿಯ ಅಕ್ಷರಗಳು ಸ್ಪಷ್ಟವಾಗಿ ಕಾಣಿಸುತ್ತಿಲ್ಲ. ದಯವಿಟ್ಟು ಬೆಳಕಿರುವ ಜಾಗದಲ್ಲಿ ಕ್ಯಾಮೆರಾವನ್ನು ನೇರವಾಗಿ ಹಿಡಿದು ಮತ್ತೊಮ್ಮೆ ಫೋಟೋ ತೆಗೆಯಿರಿ."*

---

## 3. Stage 2: Biomarker Extraction & Range Normalization Rules

### 3.1 Strict Adherence to Lab Reference Intervals (Rule SR-RNG-1)
* **Rule:** An observed value shall **only** be evaluated against the printed reference range explicitly provided by the testing laboratory on that specific document.
* **Deterministic Logic:**
  ```python
  if observed_value < lab_reference_low:
      range_status = "BELOW_RANGE"
      status_label_kn = "ಸಾಮಾನ್ಯಕ್ಕಿಂತ ಕಡಿಮೆ"
  elif observed_value > lab_reference_high:
      range_status = "ABOVE_RANGE"
      status_label_kn = "ಸಾಮಾನ್ಯಕ್ಕಿಂತ ಹೆಚ್ಚು"
  else:
      range_status = "IN_RANGE"
      status_label_kn = "ಸಾಮಾನ್ಯ ಮಿತಿಯಲ್ಲಿದೆ"
  ```
* **Fallback Protocol (Missing Lab Limits):**
  * If the laboratory report fails to print a reference interval for an extracted parameter, the system **shall not invent arbitrary numbers**.
  * It shall fall back strictly to published ICMR clinical reference intervals, explicitly tagging the output with: *"ಲ್ಯಾಬ್ ಮಿತಿ ಮುದ್ರಿತವಾಗಿಲ್ಲ; ಸಾಮಾನ್ಯ ವೈದ್ಯಕೀಯ ಮಾನದಂಡ ಬಳಸಲಾಗಿದೆ"* (*Standard ICMR interval used*).

### 3.2 Look-Alike Parameter Sanitization (Rule SR-RNG-2)
* The system shall deterministically differentiate look-alike lab parameters using regex alias mapping:
  * `Fasting Blood Sugar (FBS)` MUST NOT be confused with `Post-Prandial Blood Sugar (PPBS)` or `Random Blood Sugar (RBS)`.
  * `Urine Microalbumin` MUST NOT be confused with `Serum Albumin`.
  * `Serum Creatinine` MUST NOT be confused with `Creatinine Clearance (eGFR)`.
* If a parameter name is ambiguous or confidence score is < 0.85, the parameter must be discarded from the output card and marked as `UNRESOLVED`.

---

## 4. Stage 3: Prompt Injection Defense & Bounded LLM Generation

To prevent malicious prompts embedded within uploaded documents from hijacking the LLM (e.g., prompt injection attacks printed on medical headers), ReportSaathi enforces strict input isolation.

### 4.1 System Prompt Architecture & Delimiter Isolation
The LLM is provided **only structured JSON key-value pairs** extracted by deterministic code, never raw unparsed OCR text:

```markdown
You are an educational health literacy assistant for the ReportSaathi platform in Karnataka, India.
Your SOLE duty is to explain laboratory test parameters in plain, conversational spoken Kannada.

STRICT CLINICAL BOUNDARIES:
1. You MUST NOT diagnose any medical condition. NEVER say "You have diabetes", "You have hypertension", or "Your kidneys are diseased".
2. You MUST NOT prescribe, recommend, adjust, or comment on medications or insulin doses.
3. You MUST NOT suggest home remedies, herbal cures, or alternative therapies.
4. You MUST describe parameters purely in terms of everyday metaphors and compare observed numbers to the lab reference range.
5. You MUST generate exactly three simple questions for the patient to ask their doctor.

INPUT DATA (Structured JSON Only):
```json
{
  "hba1c": {"value": 7.8, "unit": "%", "range": "4.0 - 5.6", "status": "ABOVE_RANGE"},
  "fbs": {"value": 142, "unit": "mg/dL", "range": "70 - 100", "status": "ABOVE_RANGE"},
  "creatinine": {"value": 0.9, "unit": "mg/dL", "range": "0.7 - 1.2", "status": "IN_RANGE"}
}
```

REQUIRED OUTPUT FORMAT (JSON Only):
{
  "kannada_audio_script": "...",
  "parameter_explanations": [...],
  "doctor_questions": ["Question 1", "Question 2", "Question 3"]
}
```

---

## 5. Stage 4: Deterministic Post-Generation Output Filter (The Blacklist Gate)

Before any LLM-generated text or audio script is passed to the frontend or speech synthesis engine, it must pass through an automated **Deterministic Regex Audit Gate**. If a single blacklisted word or pattern is detected, the payload is immediately rejected, sanitized, and regenerated using fallback pre-approved template text.

### 5.1 Blacklisted Word & Pattern Registry (English & Kannada)

```python
FORBIDDEN_CLINICAL_PATTERNS = [
    # Autonomous Diagnosis Triggers
    r"(?i)\b(you have|diagnosed with|suffering from|you are diabetic|kidney failure|hypertensive)\b",
    r"(ನಿಮಗೆ ಮಧುಮೇಹವಿದೆ|ನಿಮಗೆ ಸಕ್ಕರೆ ಕಾಯಿಲೆ ಇದೆ|ಕಿಡ್ನಿ ವೈಫಲ್ಯ|ಹೃದಯಾಘಾತದ ಲಕ್ಷಣ)",
    
    # Medication & Prescription Triggers
    r"(?i)\b(take|increase|decrease|stop|start|dosage|dose|mg|tablet|capsule|injection|insulin)\b",
    r"(ಮಾತ್ರೆ ತೆಗೆದುಕೊಳ್ಳಿ|ಪ್ರಮಾಣ ಹೆಚ್ಚು ಮಾಡಿ|ಮಾತ್ರೆ ನಿಲ್ಲಿಸಿ|ಇನ್ಸುಲಿನ್ ಪ್ರಮಾಣ|ಔಷಧಿ ಸೇವಿಸಿ)",
    
    # Alternative / Unscientific Cures (Magic Remedies Act)
    r"(?i)\b(cure|remedy|karela|bitter gourd|neem|fenugreek|miracle|reverse diabetes)\b",
    r"(ಸಂಪೂರ್ಣ ಗುಣಪಡಿಸಬಹುದು|ಮನೆಮದ್ದು|ಹಾಗಲಕಾಯಿ ರಸ|ಮೆಂತ್ಯ ನೀರು|ಚಮತ್ಕಾರ)",
    
    # Doctor Dismissal Triggers
    r"(?i)\b(no need to see a doctor|cancel appointment|everything is fine|doctor is wrong)\b",
    r"(ವೈದ್ಯರನ್ನು ಕಾಣುವ ಅಗತ್ಯವಿಲ್ಲ|ಅಪಾಯಿಂಟ್‌ಮೆಂಟ್ ರದ್ದುಮಾಡಿ|ಚಿಂತಿಸುವ ಅಗತ್ಯವೇ ಇಲ್ಲ)"
]
```

### 5.2 Deterministic Replacement Protocol
If an AI output fails regex validation:
1. The generation is dropped.
2. The system falls back to **Static Pre-Approved Kannada Templates**:
   * *Template HbA1c:* *"ನಿಮ್ಮ ಕಳೆದ 3 ತಿಂಗಳ ರಕ್ತದಲ್ಲಿನ ಸಕ್ಕರೆ ಪ್ರಮಾಣದ ಸರಾಸರಿ {value}% ಬಂದಿದೆ. ಲ್ಯಾಬ್ ನಿಗದಿಪಡಿಸಿದ ಸಾಮಾನ್ಯ ಮಿತಿ {range} ಆಗಿದೆ. ನಿಮ್ಮ ಅಳತೆ ಮಿತಿಗಿಂತ ಹೆಚ್ಚಾಗಿದೆ."*
   * *Template FBS:* *"ನಿಮ್ಮ ಬೆಳಗಿನ ಉಪವಾಸದ ರಕ್ತದಲ್ಲಿನ ಸಕ್ಕರೆ ಮಟ್ಟ {value} {unit} ಬಂದಿದೆ. ಸಾಮಾನ್ಯ ಲ್ಯಾಬ್ ಮಿತಿ {range} ಆಗಿದೆ."*
3. The fallback template guarantees 100% regulatory compliance.

---

## 6. Critical Physiological Values & Emergency Escalation Protocol

Certain laboratory test values indicate an immediate, life-threatening metabolic crisis (*e.g., hyperosmolar hyperglycemic state, severe renal shutdown*). While ReportSaathi does not diagnose or prescribe, it must protect patient life.

### 6.1 Critical Physiological Thresholds

| Biomarker Parameter | Critical High Alert Threshold | Clinical Crisis Risk | Required Immediate Safety Action |
| :--- | :--- | :--- | :--- |
| **Fasting Blood Sugar** | **> 350 mg/dL** | Diabetic Ketoacidosis / Hyperosmolar Crisis | Highlight Amber + High-Priority Doctor Alert Badge |
| **Random / Post-Prandial Sugar** | **> 400 mg/dL** | Acute Hyperglycemic Coma | Highlight Amber + High-Priority Doctor Alert Badge |
| **Blood Sugar (Hypoglycemia)** | **< 60 mg/dL** | Acute Neuroglycopenia / Hypoglycemic Shock | Highlight Amber + Immediate Sugar Intake Warning |
| **Serum Creatinine** | **> 3.5 mg/dL** | Acute Kidney Injury / Uremia | Highlight Amber + Immediate Nephrology Consultation Alert |
| **Systolic Blood Pressure** | **> 180 mmHg** | Hypertensive Crisis / Stroke Risk | Highlight Amber + Immediate Emergency Clinical Evaluation |
| **Diastolic Blood Pressure** | **> 120 mmHg** | Hypertensive Emergency | Highlight Amber + Immediate Emergency Clinical Evaluation |

### 6.2 Critical Value Script Protocol (Rule SR-EMG-1)
* **Rule:** When a critical threshold is breached, the system **shall not trigger red alarm bells or screaming siren graphics** (which induce panic and dangerous blood pressure spikes in older patients).
* **Action:**
  1. The parameter card renders in high-contrast Amber with an alert icon: `⚠️ ತುರ್ತು ಗಮನ ಅಗತ್ಯ (Immediate Medical Attention Advised)`.
  2. The Kannada audio script prepends the following calm, urgent directive:  
     *"ಗಮನಿಸಿ: ನಿಮ್ಮ ಈ ಪರೀಕ್ಷೆಯ ಅಳತೆಯು ತಕ್ಷಣದ ವೈದ್ಯಕೀಯ ಗಮನವನ್ನು ಬಯಸುತ್ತದೆ. ದಯವಿಟ್ಟು ಸ್ವಯಂ ಚಿಕಿತ್ಸೆ ಮಾಡಬೇಡಿ, ಇಂದು ಅಥವಾ ಆದಷ್ಟು ಬೇಗ ನಿಮ್ಮ ವೈದ್ಯರನ್ನು ಅಥವಾ ಸಮೀಪದ ಆಸ್ಪತ್ರೆಯನ್ನು ಸಂಪರ್ಕಿಸಿ."*  
     (*"Notice: This test measurement requires immediate medical attention. Please do not self-treat; consult your doctor or nearest hospital today as soon as possible."*)
  3. Doctor Question #1 is automatically locked to: *"ನನ್ನ ಈ ಅಳತೆಯು ತೀರಾ ಹೆಚ್ಚಿರುವುದರಿಂದ ನನಗೆ ತುರ್ತು ಚಿಕಿತ್ಸೆ ಅಥವಾ ತಪಾಸಣೆ ಅಗತ್ಯವಿದೆಯೇ?"* (*Given this extreme measurement, do I need immediate emergency medical care?*)

---

## 7. Plain-Language Conversational Kannada Medical Anchors

To ensure that Kannada explanations are culturally comforting, accurate, and completely non-patronizing, the system enforces a dictionary of **Pre-Approved Vernacular Analogy Anchors**:

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               VERIFIED KANNADA ANALOGY DICTIONARY                                 │
├───────────────────────┬───────────────────────────────────┬───────────────────────────────────────┤
│ BIOMARKER (ENGLISH)   │ VERIFIED KANNADA METAPHOR         │ DAILY-LIFE PATIENT ANALOGY            │
├───────────────────────┼───────────────────────────────────┼───────────────────────────────────────┤
│ HbA1c (Glycated Hgb)  │ ಕಳೆದ ಮೂರು ತಿಂಗಳ ರಕ್ತದಲ್ಲಿನ ಸಕ್ಕರೆ    │ "ಕಳೆದ ೯೦ ದಿನಗಳಲ್ಲಿ ರಕ್ತದಲ್ಲಿ ಸಕ್ಕರೆ   │
│                       │ ಪ್ರಮಾಣದ ಸರಾಸರಿ (ಸಕ್ಕರೆ ನೆನಪು)     │ ಎಷ್ಟು ಇತ್ತು ಎಂಬುದರ ನೆನಪಿನ ಅಳತೆ"       │
├───────────────────────┼───────────────────────────────────┼───────────────────────────────────────┤
│ Fasting Blood Glucose │ ಬೆಳಿಗ್ಗೆ ಉಪವಾಸವಿದ್ದಾಗ ರಕ್ತದಲ್ಲಿರುವ   │ "ರಾತ್ರಿ ಊಟದ ನಂತರ ಬೆಳಿಗ್ಗೆ ದೇಹವು      │
│ (FBS)                 │ ಸಕ್ಕರೆಯ ಸಹಜ ಮಟ್ಟ                  │ ಸಕ್ಕರೆಯನ್ನು ಹೇಗೆ ನಿರ್ವಹಿಸಿದೆ ಎಂಬ ಪರೀಕ್ಷೆ"│
├───────────────────────┼───────────────────────────────────┼───────────────────────────────────────┤
│ Post-Prandial Glucose │ ಊಟವಾದ ೨ ಗಂಟೆಗಳ ನಂತರದ              │ "ಆಹಾರ ಸೇವಿಸಿದ ನಂತರ ರಕ್ತದಲ್ಲಿ ಸಕ್ಕರೆ   │
│ (PPBS)                │ ರಕ್ತದಲ್ಲಿನ ಸಕ್ಕರೆ ಪ್ರಮಾಣ          │ ಎಷ್ಟು ಏರಿಕೆಯಾಗಿದೆ ಎಂಬ ಅಳತೆ"            │
├───────────────────────┼───────────────────────────────────┼───────────────────────────────────────┤
│ Serum Creatinine      │ ಮೂತ್ರಪಿಂಡಗಳ (ಕಿಡ್ನಿ) ರಕ್ತ ಶುದ್ಧೀಕರಣ  │ "ಮೂತ್ರಪಿಂಡಗಳು ರಕ್ತದ ಕಲ್ಮಶಗಳನ್ನು ಎಷ್ಟು  │
│                       │ ಸಾಮರ್ಥ್ಯದ ಅಳತೆ                    │ ಸರಿಯಾಗಿ ಸೋಸುತ್ತಿವೆ ಎಂಬ ಅಳತೆ"          │
├───────────────────────┼───────────────────────────────────┼───────────────────────────────────────┤
│ Blood Pressure (BP)   │ ರಕ್ತನಾಳಗಳಲ್ಲಿ ರಕ್ತ ಹರಿಯುವ ಒತ್ತಡ     │ "ಹೃದಯವು ರಕ್ತವನ್ನು ದೇಹದ ಅಂಗಗಳಿಗೆ       │
│                       │                                   │ ಪಂಪ್ ಮಾಡುವಾಗ ಉಂಟಾಗುವ ನೈಸರ್ಗಿಕ ಒತ್ತಡ"  │
├───────────────────────┼───────────────────────────────────┼───────────────────────────────────────┤
│ LDL Cholesterol       │ ರಕ್ತನಾಳಗಳಲ್ಲಿ ಜಿಡ್ಡು ಕಟ್ಟುವ        │ "ರಕ್ತ ಸಂಚಾರಕ್ಕೆ ಅಡ್ಡಿಯಾಗುವ ಜಿಡ್ಡಿನ    │
│                       │ ಕೊಲೆಸ್ಟ್ರಾಲ್                      │ ಅಂಶ"                                  │
├───────────────────────┼───────────────────────────────────┼───────────────────────────────────────┤
│ HDL Cholesterol       │ ಹೃದಯಕ್ಕೆ ರಕ್ಷಣೆ ನೀಡುವ ಉತ್ತಮ        │ "ರಕ್ತನಾಳಗಳನ್ನು ಸ್ವಚ್ಛವಾಗಿಡುವ          │
│                       │ ಕೊಲೆಸ್ಟ್ರಾಲ್                      │ ಸಹಾಯಕ ಜಿಡ್ಡು"                         │
└───────────────────────┴───────────────────────────────────┴───────────────────────────────────────┘
```

---

## 8. Regulatory Compliance Verification Checklists

### 8.1 National Medical Commission (NMC) Telemedicine Verification
* [x] **No Independent AI Prescribing:** The system contains zero capability to emit drug names, doses, or frequencies.
* [x] **No Independent AI Counseling:** The system provides educational health literacy summaries rather than therapeutic counseling.
* [x] **Human Doctor Centrality:** Every screen and audio note explicitly instructs the patient to consult their licensed Registered Medical Practitioner (RMP).

### 8.2 CDSCO Software as a Medical Device (SaMD) Exemption Checklist
* [x] **No Clinical Diagnosis Claims:** The software does not diagnose, treat, prevent, or alleviate any disease.
* [x] **Non-Diagnostic Informational Carve-Out:** In accordance with CDSCO Guidance Doc No. *CDSCO/MD/GD/MDSW/01/2026*, standalone health education software that visually translates and summarizes lab-provided data without clinical decision support remains exempt from Class B/C licensing.
* [x] **Prominent Informational Disclaimers:** Visible and audible notifications that the tool does not provide medical opinions.

### 8.3 Digital Personal Data Protection Act (DPDP Act 2023) Checklist
* [x] **Section 5(3) & 6(3) Multilingual Consent:** Full privacy notice and consent mechanism provided in spoken and written Kannada (8th Schedule Language).
* [x] **Section 8(5) Data Security & Ephemeral Purging:** Automated 15-minute hard garbage collection of all patient documents and extracted values.
* [x] **Zero Secondary Use:** Zero patient health data used for training AI models or commercial profiling.
* [x] **Zero Persistent Cookies / Cross-Site Trackers:** No third-party ad pixels, analytics trackers, or social media scripts.
