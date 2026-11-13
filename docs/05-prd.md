# Product Requirements Document (PRD): ReportSaathi

**Document:** `docs/05-prd.md`  
**Status:** Approved for Implementation  
**Product Version:** MVP (Phase 1)  
**Target Market:** Karnataka, India (Kannada-speaking Type 2 Diabetes & Hypertension patients & caregivers)  
**Author:** DeepMind Agentic Product Team  
**Date:** November 2026  

---

## 1. Executive Summary & Problem Context

Millions of patients in Karnataka receive diagnostic laboratory reports printed strictly in English medical terminology (*e.g., Fasting Plasma Glucose, HbA1c, Microalbuminuria, eGFR*). Overburdened outpatient clinics (OPDs) average under 3 minutes per consultation, leaving patients unable to decipher their numbers, understand what their lab values mean for their daily life, or formulate meaningful questions for their doctor.

**ReportSaathi** bridges this health-literacy divide. It is a zero-friction, vernacular companion that ingests standardized diabetes and blood pressure lab reports (PDF or photo) and generates a **60-second spoken Kannada audio explanation**, a **color-coded range card**, and **3 specific questions to ask the doctor** at their next appointment—**strictly without diagnosing, prescribing, or altering treatment.**

---

## 2. Goals & Non-Goals

### 2.1 Product Goals
* **G-1 (Health Literacy & Language Inclusion):** Translate complex English laboratory biomarker numbers and ranges into clear, colloquial, everyday Kannada analogies delivered via natural audio and simple visual cards.
* **G-2 (Zero-Friction Access for Older Adults):** Enable non-tech-savvy older adults (55–75+ years) or their family caregivers to receive explanations in under 60 seconds without mandatory app downloads, account creation, or OTP walls.
* **G-3 (Clinician Partnership & Patient Agency):** Formulate exactly 3 context-aware, non-threatening questions for the patient to ask their doctor, strengthening the patient-physician relationship.
* **G-4 (Clinical & Legal Safety by Design):** Adhere strictly to the National Medical Commission (NMC) Telemedicine Practice Guidelines (2020), CDSCO Medical Devices Rules (SaMD 2026), and DPDP Act (2023) by remaining completely non-diagnostic and non-prescriptive.
* **G-5 (Ephemeral Data Privacy):** Safeguard sensitive patient health data by enforcing 1-tap Kannada statutory consent and purging uploaded files and extracted biomarkers from operational memory within 15 minutes.

### 2.2 Non-Goals (Explicitly Out of Scope)
* **NG-1 (Autonomous Diagnosis):** ReportSaathi will NEVER diagnose diseases (*e.g., "You have diabetic nephropathy"* or *"You have Stage 2 Hypertension"*).
* **NG-2 (Treatment or Medication Modifications):** ReportSaathi will NEVER prescribe, recommend, adjust, or advise stopping any medication or insulin dose.
* **NG-3 (Handwritten Prescription OCR):** ReportSaathi will NOT attempt to read, decipher, or dispense handwritten doctor prescriptions in the MVP due to fatal look-alike drug errors (LASA).
* **NG-4 (E-Commerce & Commercial Monetization):** ReportSaathi will NOT sell medicines, book diagnostic tests, host pharmaceutical ads, or act as an e-pharmacy funnel.
* **NG-5 (Interactive Two-Way Conversational AI):** ReportSaathi will NOT provide an open-ended conversational chatbot in the MVP to prevent hallucination drift and unauthorized medical advice.
* **NG-6 (Longitudinal Health Records / EMR):** ReportSaathi will NOT store historical medical records across years or require persistent user accounts.
* **NG-7 (Geographic / Multi-Disease Expansion in MVP):** ReportSaathi will NOT support languages other than Kannada or conditions outside Diabetes and Hypertension in Phase 1.

---

## 3. User Personas & User Stories

### 3.1 Primary Personas
1. **Basavaraj (63, Retired Primary Teacher, Hubballi):** Speaks Kannada natively; reads limited English. Diagnosed with Type 2 Diabetes 4 years ago. Receives a printed blood report from a local diagnostic lab with numbers like `HbA1c: 7.9%` and `FBS: 148 mg/dL`. He feels anxious because numbers are flagged with asterisks, but cannot understand what they mean. He wants someone to explain it in simple Kannada without scaring him.
2. **Kavitha (34, Software Quality Analyst, Bengaluru):** Basavaraj’s daughter. Lives in Bengaluru while her parents reside in Hubballi. Coordinates her father's monthly tests remotely over WhatsApp. She needs an easy way to understand his report quickly so she can guide him on what to ask his local physician.

### 3.2 User Stories
* **US-1 (Report Upload):** As an elderly patient or caregiver, I want to take a photo of my lab report or select a PDF without creating an account or logging in, so that I can get immediate help without technical hurdles.
* **US-2 (Statutory Vernacular Consent):** As a patient, I want to hear and read the privacy and consent terms in spoken and written Kannada, so that I understand how my data is handled under the law before proceeding.
* **US-3 (Spoken Vernacular Explanation):** As a non-English speaking older user, I want to listen to a 60-second voice note in warm, everyday Kannada explaining what each test measures in relatable terms, so that I understand my health without struggling with medical jargon.
* **US-4 (Paced Audio Playback):** As an older user with mild hearing loss, I want to play the audio at a slower speed (`0.8x`) and replay it easily, so that I don't feel rushed or confused.
* **US-5 (Non-Alarmist Range Inspection):** As an anxious patient, I want to see a clear, high-contrast visual card showing whether my numbers are within standard lab limits using calm colors, so that I don't panic unnecessarily.
* **US-6 (Doctor Visit Preparation):** As a patient, I want a checklist of 3 simple questions tailored to my test results, so that I can walk into my next doctor consultation prepared and confident.
* **US-7 (Family Forwarding via WhatsApp):** As a caregiver, I want to forward the audio note and visual card directly to my family WhatsApp group with 1 tap, so that everyone involved in caregiving stays informed.
* **US-8 (Safety Rejection of Prescriptions):** As a patient who mistakenly uploads a handwritten prescription or blurry image, I want an empathetic voice note in Kannada explaining why it cannot be read and guiding me on what to upload, so that I am not left stranded or harmed by misread handwriting.

---

## 4. Numbered Functional Requirements (FR)

### Module 1: Document Ingestion & Quality Validation
* **FR-1.1:** The system shall accept single-page or multi-page digital documents in PDF format and image formats (`.jpg`, `.jpeg`, `.png`, `.webp`) up to a maximum file size of 10 MB.
* **FR-1.2:** The system shall execute an automated document classification filter on upload to determine document type.
  * If identified as a **standard diagnostic laboratory report**, the system proceeds to extraction.
  * If identified as a **handwritten prescription, clinical doctor note, discharge summary, or radiology scan**, the system shall immediately reject the document and transition to Screen 5.
* **FR-1.3:** The system shall evaluate image sharpness, lighting, and legibility. If the image is blurred, glare-obscured, or cut off, the system shall prompt the user to retake the photo with camera alignment framing.
* **FR-1.4:** The system shall operate completely session-based with zero user account creation, password setup, or phone OTP walls.

### Module 2: DPDP Statutory Consent & Ephemeral Processing
* **FR-2.1:** The system shall present a mandatory consent screen in Kannada (text and spoken audio) adhering to Section 5(3) and Section 6(3) of the Digital Personal Data Protection Act, 2023.
* **FR-2.2:** The system shall provide a 1-tap audio preview of the consent clauses in spoken Kannada (20 seconds) for illiterate or visually impaired users.
* **FR-2.3:** The system shall require explicit affirmative user consent (*"ನಾನು ಒಪ್ಪುತ್ತೇನೆ" / "I Agree"*) before transmitting document contents to the extraction pipeline.
* **FR-2.4:** The system shall automatically purge all uploaded documents, temporary image slices, and extracted clinical records from operational memory and disk within exactly 15 minutes of session completion.
* **FR-2.5:** The system shall strictly prohibit the retention of patient health data or personally identifiable information (PII) for AI model fine-tuning or secondary training.

### Module 3: Deterministic Biomarker Extraction & Range Normalization
* **FR-3.1:** The system shall extract the following standardized diabetes and hypertension parameters when present in the lab report:
  1. Fasting Blood Sugar (FBS / Glucose Fasting)
  2. Post-Prandial Blood Sugar (PPBS / Glucose Post-Meal)
  3. Glycosylated Hemoglobin (HbA1c)
  4. Blood Pressure (Systolic & Diastolic)
  5. Serum Creatinine
  6. Blood Urea
  7. Urine Microalbumin / Protein
  8. Total Cholesterol, Triglycerides, HDL, LDL
* **FR-3.2:** The system shall deterministically extract three core fields for each parameter:
  * `parameter_name` (Standardized label)
  * `observed_value` (Numeric value recorded by the testing laboratory)
  * `unit` (e.g., `mg/dL`, `%`, `mmHg`, `mg/g`)
  * `reference_interval` (Lower and upper biological limits printed on the lab report)
* **FR-3.3:** The system shall compare the `observed_value` strictly against the laboratory's printed `reference_interval` and assign exactly one of three deterministic states:
  * `IN_RANGE` (Observed value is within printed lower and upper bounds)
  * `ABOVE_RANGE` (Observed value strictly exceeds printed upper bound)
  * `BELOW_RANGE` (Observed value strictly falls below printed lower bound)
* **FR-3.4:** If the lab report does not print a reference interval for a recognized parameter, the system shall fall back to documented Indian Council of Medical Research (ICMR) clinical standards and append a visible disclaimer: *"ಲ್ಯಾಬ್ ಮಿತಿ ಮುದ್ರಿತವಾಗಿಲ್ಲ; ಸಾಮಾನ್ಯ ವೈದ್ಯಕೀಯ ಮಾನದಂಡ ಬಳಸಲಾಗಿದೆ"* (*Standard ICMR interval used*).

### Module 4: Non-Diagnostic Vernacular Simplification Engine
* **FR-4.1:** The system shall translate extracted biochemical metrics into established colloquial Kannada analogies:
  * `HbA1c` ➔ "ಕಳೆದ ಮೂರು ತಿಂಗಳ ರಕ್ತದಲ್ಲಿನ ಸಕ್ಕರೆ ಪ್ರಮಾಣದ ಸರಾಸರಿ" (*3-month sugar memory*)
  * `Fasting Blood Sugar` ➔ "ಬೆಳಿಗ್ಗೆ ಉಪವಾಸವಿದ್ದಾಗ ರಕ್ತದಲ್ಲಿರುವ ಸಕ್ಕರೆ ಮಟ್ಟ" (*Morning fasting sugar*)
  * `Serum Creatinine` ➔ "ಮೂತ್ರಪಿಂಡಗಳು ರಕ್ತವನ್ನು ಎಷ್ಟು ಚೆನ್ನಾಗಿ ಶುದ್ಧೀಕರಿಸುತ್ತಿವೆ ಎಂಬ ಅಳತೆ" (*Kidney waste filtration efficiency*)
  * `LDL Cholesterol` ➔ "ರಕ್ತನಾಳಗಳಲ್ಲಿ ಜಿಡ್ಡು ಕಟ್ಟುವ ಕೊಲೆಸ್ಟ್ರಾಲ್" (*Sticky vessel cholesterol*)
* **FR-4.2:** The system shall enforce deterministic safety filters that strip and block any diagnostic assertions (*e.g., "ನಿಮಗೆ ಮಧುಮೇಹವಿದೆ" / "You have diabetes"*), prognostic staging, or disease labels.
* **FR-4.3:** The system shall dynamically generate exactly three tailored questions for the patient's next clinical visit based on their specific range states (e.g., lifestyle discussion, medication review by doctor, repeat test timing).

### Module 5: Spoken Audio Synthesis & Visual Playback
* **FR-5.1:** The system shall synthesize a high-fidelity Kannada voice note of duration between 45 and 65 seconds using an everyday, warm, respectful conversational tone.
* **FR-5.2:** The audio player shall feature a prominent play/pause toggle, a visual scrubbable waveform, time elapsed, and a 1-tap `0.8x ನಿಧಾನ` (Slow Speed) toggle.
* **FR-5.3:** The visual UI shall display a single-column stack of parameter cards utilizing the non-panic color coding:
  * `IN_RANGE`: Forest Green badge (`#15803D`, background `#DCFCE7`)
  * `ABOVE_RANGE` / `BELOW_RANGE`: Warm Amber badge (`#B45309`, background `#FEF3C7`)
  * Under no circumstances shall out-of-range values be rendered in alarming neon red.
* **FR-5.4:** The system shall provide a native WhatsApp share trigger that packages the audio clip, summary text, and the 3 doctor questions into an easily shareable message.

### Module 6: Safety Guardrails & Rejection Handling
* **FR-6.1:** When a handwritten prescription or non-lab file is detected, the system shall transition to Screen 5 and play an empathetic 18-second Kannada audio message explaining the safety policy.
* **FR-6.2:** The system shall display a visual comparison card clearly differentiating supported printed lab reports from unsupported handwritten doctor slips.

---

## 5. Non-Functional Requirements (NFR)

### 5.1 Performance & Latency
* **NFR-1.1 (End-to-End Turnaround):** Total turnaround time from user consent confirmation (Screen 2) to audio readiness (Screen 4) shall not exceed **10 seconds** on a standard 4G mobile connection.
* **NFR-1.2 (Payload Optimization):** The initial frontend HTML/CSS/JS payload shall not exceed **50 KB** (uncompressed) to enable rapid loading on 2G/3G connections.
* **NFR-1.3 (Audio Streaming Size):** Synthesized 60-second Kannada audio notes shall be compressed using Opus or AAC at 24 kbps, keeping audio file size under **80 KB**.

### 5.2 Accessibility & Usability (Seniors & Presbyopia)
* **NFR-2.1 (Touch Target Dimensions):** Every interactive button, toggle, and card shall possess a minimum hit target height of **56 pixels** with at least **12 pixels** of separation between adjacent controls.
* **NFR-2.2 (Contrast Ratios):** All body text, button labels, and status badges shall meet or exceed a **7:1 contrast ratio** against their backgrounds (exceeding WCAG 2.1 Level AAA requirements) for outdoor visibility under harsh Indian sunlight.
* **NFR-2.3 (Kannada Line Height):** All Kannada script typography shall enforce a minimum CSS line-height of **1.65 to 1.70** to prevent clipping of vowel *maatras* and stacked *vattugalu*.
* **NFR-2.4 (Zero Complex Gestures):** The application shall be 100% operable via single taps. No pinch-to-zoom, swiping, double-tapping, or drag-and-drop gestures shall be required.

### 5.3 Reliability & Fault Tolerance
* **NFR-3.1 (Uptime):** Core processing endpoints shall maintain a minimum of **99.5% availability**.
* **NFR-3.2 (Network Drop Resilience):** If a network connection drops mid-upload or mid-synthesis, the client shall automatically attempt up to 3 retries with exponential backoff before displaying a friendly offline message.
* **NFR-3.3 (Graceful Fallback):** If audio synthesis fails on the server, the system shall display the full visual text card and doctor questions, ensuring zero loss of medical literacy value.

### 5.4 Privacy & Compliance
* **NFR-4.1 (Statutory Compliance):** The platform shall comply with India's Digital Personal Data Protection Act (DPDP Act 2023), Sections 5, 6, and 8.
* **NFR-4.2 (Zero Persistent Storage):** Temporary files stored in server memory or disk caches shall be hard-purged using an automated garbage-collection worker running every 5 minutes.
* **NFR-4.3 (Encryption in Transit):** All communications shall be enforced over TLS 1.3 with HTTPS.

---

## 6. Safety & Clinical Requirements (SR)

* **SR-1 (Absolute Non-Diagnostic Boundary):** The system shall NEVER generate sentences asserting that the patient has a disease, condition, syndrome, or clinical stage.
* **SR-2 (Absolute Non-Prescriptive Boundary):** The system shall NEVER recommend a medicine, suggest an alternative drug brand, instruct dose changes, or tell a patient to start or stop therapy.
* **SR-3 (Critical Value Triage Protocol):** When a biomarker exceeds critical physiological danger thresholds (*e.g., Fasting Glucose > 400 mg/dL, Diastolic BP > 120 mmHg, Serum Creatinine > 4.0 mg/dL*), the system shall:
  1. Refrain from alarming panic language.
  2. Clearly highlight the value in Amber.
  3. Prominently state in spoken Kannada audio and text: *"ಈ ಅಳತೆಯು ತಕ್ಷಣದ ವೈದ್ಯಕೀಯ ಗಮನವನ್ನು ಬಯಸುತ್ತದೆ. ದಯವಿಟ್ಟು ಇಂದು ಅಥವಾ ಆದಷ್ಟು ಬೇಗ ನಿಮ್ಮ ವೈದ್ಯರನ್ನು ಸಂಪರ್ಕಿಸಿ."* (*This measurement warrants immediate medical attention. Please consult your doctor today or as soon as possible.*)
* **SR-4 (Doctor Primacy Reinforcement):** Every synthesized audio note and visual card must explicitly conclude with the statutory disclaimer: *"ವರದಿ ಸಾಥಿ ಕೇವಲ ಶೈಕ್ಷಣಿಕ ಮಾಹಿತಿಯಾಗಿದೆ; ಇದು ವೈದ್ಯರ ವೈದ್ಯಕೀಯ ತಪಾಸಣೆ ಅಥವಾ ಸಲಹೆಗೆ ಬದಲಿಯಲ್ಲ."* (*ReportSaathi is for educational purposes only and is not a substitute for clinical doctor advice.*)
* **SR-5 (Zero Alternative / Miracle Cure Promotion):** The system shall strictly prohibit and reject any mention of unscientific home remedies, herbal cures, or unverified claims prohibited under the Drugs and Magic Remedies (Objectionable Advertisements) Act, 1954.

---

## 7. Success Metrics & Key Performance Indicators (KPIs)

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   REPORTSAATHI SUCCESS SCORECARD                                  │
├─────────────────────────┬───────────────────────────────────────┬─────────────────────────────────┤
│ METRIC CATEGORY         │ KPI / MEASUREMENT                     │ MVP TARGET BENCHMARK            │
├─────────────────────────┼───────────────────────────────────────┼─────────────────────────────────┤
│ Comprehension & UX      │ Audio Completion Rate (% 60s played)  │ ≥ 80% of users play > 75% audio │
│ Doctor Engagement       │ Doctor Questions Saved / Shared       │ ≥ 65% of completed sessions     │
│ Extraction Accuracy     │ Biomarker Extraction Fidelity         │ ≥ 99.0% on standard printed lab │
│ Safety & Rejection      │ Prescription Rejection Precision      │ 100% of prescriptions rejected  │
│ Turnaround Latency      │ Ingestion to Audio Readiness          │ < 10 seconds (P90) on 4G        │
│ User Trust / Sentiment  │ Caregiver Net Promoter Score (NPS)    │ ≥ +55 in Karnataka pilot        │
└─────────────────────────┴───────────────────────────────────────┴─────────────────────────────────┘
```

1. **Audio Completion Rate:** Target ≥ 80% of sessions play the Kannada voice explanation for at least 45 seconds, validating audio-first engagement among older users.
2. **Doctor Question Utility:** Target ≥ 65% of users tap "Share to WhatsApp" or screenshot the doctor questions card before visiting their clinic.
3. **Extraction & Safety Precision:** 0% false acceptance of handwritten prescriptions; ≥ 99.0% extraction accuracy on standardized printed diabetes/BP lab reports from major Karnataka chains (Dr Lal, Agilus, Metropolis, Manipal, Orange Health).
4. **Processing Latency:** 90th percentile latency under 10 seconds from upload confirmation to audio playback.
5. **Zero Regulatory Violations:** 0 instances of autonomous prescribing, diagnosing, or DPDP Act non-compliance.
