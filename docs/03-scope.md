# Core Flow & Scope Definition: ReportSaathi

**Project:** ReportSaathi  
**References:** `docs/01-problem.md`, `docs/02-research.md`  
**Target Demographic:** Kannada-speaking Type 2 Diabetes & Hypertension patients (and their family caregivers) in Karnataka, India  
**Date:** November 2026  

---

## 1. The Single Core Flow

### 1.1 Core Value Proposition
The fundamental value of ReportSaathi is **turning an incomprehensible English diagnostic lab report into a 60-second, comforting, spoken Kannada audio explanation with 3 plain-language questions to ask the doctor—without diagnosing, prescribing, or altering treatment.**

### 1.2 Step-by-Step User Journey

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   THE SINGLE CORE FLOW                                          │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                 │
                                                 ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│ STEP 1: REPORT CAPTURE / UPLOAD                                                                 │
│ • Patient or family caregiver uploads a lab report PDF or takes a clear phone photo.             │
│ • Zero app download or account creation required (operates via WhatsApp bot or lightweight web). │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                 │
                                                 ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│ STEP 2: STATUTORY CONSENT & DOCUMENT CLASSIFICATION                                             │
│ • Displays mandatory 1-tap consent notice in spoken & written Kannada (DPDP Act Sec 5/6).        │
│ • Computer vision classifies the document:                                                      │
│   - Valid Lab Report (Blood/Urine panel) ➔ PROCEED.                                            │
│   - Handwritten Prescription / X-Ray / Other ➔ GRACEFUL REJECTION with safety message.         │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                 │
                                                 ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│ STEP 3: STRUCTURED BIOMARKER EXTRACTION & SAFETY SANITIZATION                                   │
│ • Extracts standardized parameters: Fasting Sugar, PPBS, HbA1c, Blood Pressure, Lipid, Kidney.  │
│ • Deterministic parsing: Parameter Name, Observed Value, Unit, Standard Biological Range.        │
│ • Guardrail Check: Discards any treatment modification triggers or clinical diagnostic labels.   │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                 │
                                                 ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│ STEP 4: COLLOQUIAL KANNADA TRANSLATION & EXPLANATION GENERATION                                 │
│ • Translates biochemical jargon into everyday spoken Kannada (avoiding archaic Sanskrit terms).  │
│ • Explains what the test measures in daily-life terms (e.g., HbA1c = "3-month sugar memory").    │
│ • Contextualizes values neutrally against the printed lab range (Within Range / Higher / Lower). │
│ • Generates exactly 3 tailored questions for the patient to ask their doctor at the next visit. │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                 │
                                                 ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│ STEP 5: AUDIO SYNTHESIS & DUAL DELIVERY                                                         │
│ • High-quality vernacular Text-to-Speech (slow cadence, warm tone, colloquial Kannada).         │
│ • Patient receives:                                                                             │
│   1. A 60-second playable voice note (listenable immediately without reading).                  │
│   2. A simple, color-coded visual summary card (Green = In Range, Amber = Outside Range).       │
│   3. A 3-bullet text checklist of questions for the doctor.                                     │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Feature & Sub-Feature Decomposition

### 2.1 Ingestion & Document Verification
* **2.1.1 WhatsApp & Web PDF/Image Receiver:** Frictionless ingestion via WhatsApp chat message attachment or single-screen mobile web uploader.
* **2.1.2 Document Type Classifier:** Algorithmic verification that the uploaded image/file is a diagnostic laboratory report and NOT a doctor's handwritten prescription, invoice, discharge summary, or non-medical document.
* **2.1.3 Image Quality & Legibility Assessor:** Checks blur, lighting, resolution, and angle. If illegible or cut off, immediately prompts the user in Kannada audio/text to retake the photo.

### 2.2 Extraction & Deterministic Parsing
* **2.2.1 Bounded Biomarker Extraction:** Focuses strictly on core Type 2 Diabetes and Hypertension parameters:
  * Fasting Blood Sugar (FBS), Post-Prandial Blood Sugar (PPBS), HbA1c.
  * Lipid Profile (Total Cholesterol, Triglycerides, HDL, LDL).
  * Renal Safety Markers (Serum Creatinine, Blood Urea, Urine Microalbumin).
  * Blood Pressure (Systolic / Diastolic).
* **2.2.2 Value, Unit & Reference Interval Normalization:** Deterministically extracts the patient's observed value, measurement units (e.g., `mg/dL`, `%`), and the specific lab's reference range.
* **2.2.3 Range State Evaluator:** Compares the observed value strictly against the printed lab interval to assign one of three neutral states: `Within Normal Range`, `Higher than Reference Range`, or `Lower than Reference Range`.

### 2.3 Non-Diagnostic Plain-Language Engine
* **2.3.1 Jargon-to-Metaphor Simplifier:** Converts complex terms into accessible real-world concepts in conversational Kannada:
  * *HbA1c:* "Last 90 days' sugar memory in your blood" (*ಕಳೆದ ಮೂರು ತಿಂಗಳ ರಕ್ತದಲ್ಲಿನ ಸಕ್ಕರೆ ಪ್ರಮಾಣದ ಸರಾಸರಿ*).
  * *Creatinine:* "Kidney waste filtration efficiency" (*ಮೂತ್ರಪಿಂಡಗಳು ರಕ್ತವನ್ನು ಎಷ್ಟು ಚೆನ್ನಾಗಿ ಸ್ವಚ್ಛಗೊಳಿಸುತ್ತಿವೆ ಎಂಬ ಅಳತೆ*).
  * *LDL Cholesterol:* "Sticky fat that can narrow blood vessels" (*ರಕ್ತನಾಳಗಳಲ್ಲಿ ಜಿಡ್ಡು ಕಟ್ಟುವ ಕೊಲೆಸ್ಟ್ರಾಲ್*).
* **2.3.2 Strict Non-Diagnostic Guardrail (Safety Filter):** Ensures generated content NEVER says "You have diabetes", "Your kidneys are failing", or "You need to take medicine". The phrasing is strictly descriptive: *"Your HbA1c is 8.2%, which is higher than the standard lab range of 4.0% to 5.6%."*
* **2.3.3 Doctor-Discussion Prompt Generator:** Formulates exactly 3 simple, non-threatening questions for the patient's doctor visit:
  1. *"What does my current HbA1c level mean for my daily routine?"*
  2. *"Do my current food habits or medicines need any review based on these numbers?"*
  3. *"When should I repeat this test?"*

### 2.4 Voice & Audio Synthesis
* **2.4.1 Vernacular Spoken Kannada TTS:** Text-to-Speech tuned specifically for spoken regional Kannada (Southern Karnataka dialect / Bengaluru-Mysuru vernacular) with natural pacing, clear pauses, and respectful intonation suited for elderly listeners.
* **2.4.2 Audio Speed & Replay Controls:** 1-tap playback with options for 0.8x slow speed and instant replay.

### 2.5 Visual Companion Card & Output
* **2.5.1 Visual "Traffic Light" Range Display:** Clean, high-contrast mobile summary card using universal colors:
  * Green bar: Parameter is within standard reference range.
  * Amber bar: Parameter is above or below standard reference range.
  * Explicit avoidance of red/alarmist graphics that induce panic.
* **2.5.2 Bilingual Toggle:** Kannada audio/text with side-by-side English biomarker names so English-literate adult children or doctors can cross-verify.

### 2.6 Privacy, Consent & Ephemeral Storage
* **2.6.1 Section 5/6 DPDP Kannada Consent Screen:** 1-tap affirmative consent presented in plain, spoken and written Kannada before processing begins.
* **2.6.2 Ephemeral Data Processing:** Uploaded images and extracted values are purged from operational memory within 15 minutes of audio delivery; zero model fine-tuning on patient data.

---

## 3. The Ruthless MVP Challenge: What the Core Flow Can Live Without

To ensure zero bloat, immediate clinical safety, and swift execution, every candidate feature for the MVP was challenged against the test: **"Can the patient understand their lab report and know what to ask their doctor without this feature?"**

| Candidate Feature | Initial Temptation | The Challenge Verdict | Disposition | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **User Accounts, Passwords & Profiles** | "Users need to log in to save their history." | **REJECTED FROM MVP** | **Later** | Account creation and OTP loops are the #1 complaint in lab apps. The core value is delivered immediately upon report upload. A session-based or phone-number link is sufficient. |
| **Longitudinal Trend Graphs (History over years)** | "Patients should see if their sugar went up or down compared to last year." | **REJECTED FROM MVP** | **Later** | Adds database complexity, user authentication, and data retention liability under the DPDP Act. The patient's urgent problem is understanding the report in their hand *today*. |
| **Interactive AI Chatbot (Q&A Conversational Agent)** | "Let the patient ask follow-up questions to the AI." | **REJECTED FROM MVP** | **Later / Restricted** | Conversational back-and-forth dramatically increases the risk of hallucination, medical advice drift, and regulatory violation under NMC guidelines. A one-way structured explanation is 100x safer. |
| **Multiple Languages (Hindi, Telugu, Tamil, Marathi)** | "We should serve all of India from Day 1." | **REJECTED FROM MVP** | **Later** | Every added language multiplies translation review, dialect validation, and clinical liability. Proving clinical accuracy in Kannada first creates a validated, repeatable blueprint. |
| **Expanding to Other Diseases (Thyroid, Liver, Oncology)** | "Why only diabetes and hypertension?" | **REJECTED FROM MVP** | **Later** | Diabetes and hypertension blood panels (FBS, PPBS, HbA1c, Lipid, Creatinine) follow highly standardized formats across 90%+ of labs. Oncology and pathology reports require subjective histopathology interpretation that cannot be automated safely. |
| **Handwritten Prescription OCR** | "Patients have prescriptions attached to their lab tests." | **REJECTED FROM MVP** | **NEVER (Autonomous)** | Indian doctor handwriting is notoriously illegible; LLMs hallucinate look-alike drug names (e.g., Metformin vs Metoprolol), creating lethal medication errors. Completely unviable without an RMP in the loop. |
| **Medicine Refill & Phlebotomy Booking Integrations** | "We can monetize by selling medicine or booking tests." | **REJECTED FROM MVP** | **Later (B2B)** | Commercial integrations turn a trusted health literacy tool into an aggressive e-commerce sales funnel, triggering negative user reviews like 1mg/PharmEasy. |

---

## 4. Scope Categorization: MVP vs. Later vs. Never

```
                                  REPORT SAATHI SCOPE MATRIX
                                                │
         ┌──────────────────────────────┬───────┴──────────────────────┬──────────────────────────────┐
         ▼                              ▼                              ▼                              ▼
        MVP                           LATER                         NEVER
    (Build Now)                (Post-Validation)             (Strict Red Lines)
 • Structured lab PDF/photo     • Multi-report history &      • Autonomous clinical diagnosis
   ingestion (Diabetes/HTN).      trend analytics.              or staging.
 • Kannada 60s spoken audio     • Expanding to Hindi,         • Recommending, stopping, or
   explanation (TTS).             Telugu, Tamil, Marathi.       modifying drug dosages.
 • 3 questions for doctor.      • Thyroid & Liver panels.     • Reading handwritten scripts
 • 3-state range indicator.     • E-prescription integration    autonomously to order drugs.
 • Ephemeral DPDP consent.        via hospital EMRs.          • Suggesting unverified home/
 • Graceful rejection of        • B2B clinician portal for      herbal miracle cures.
   prescriptions & non-labs.      doctor review & sign-off.   • Storing PII for AI training.
```

---

### 4.1 MVP (Minimum Viable Product — Deliver Now)
*The absolute minimal, clinically safeguarded feature set required to achieve the core value.*

1. **Structured Diagnostic Lab Ingestion (PDF & Clear Photos):** Supports standard digital lab reports and clean photos from major chains (Dr Lal, Agilus, Metropolis, Orange Health, Manipal Labs, Apollo Diagnostics) covering Diabetes and Hypertension panels.
   * *Reason:* Digitally formatted lab reports provide high-fidelity character recognition (>99% accuracy), avoiding extraction errors.
2. **Automated Document Rejection Filter:** Rejects prescriptions, blurry photos, radiology scans, and non-lab documents with an immediate polite explanation in Kannada.
   * *Reason:* Prevents out-of-scope files from entering the pipeline and eliminates the risk of misinterpreting dangerous documents.
3. **Deterministic Parameter & Range Extraction:** Accurately parses Fasting Sugar, PPBS, HbA1c, Lipid Profile, and Serum Creatinine alongside their specific laboratory reference intervals.
   * *Reason:* Ground truth extraction prevents the AI from inventing or assuming standard ranges that contradict the specific testing lab.
4. **Colloquial Kannada Plain-Language Explanation Engine:** Converts parameters into relatable, everyday Kannada analogies without medical jargon or patronizing phrasing.
   * *Reason:* Overcomes the primary barrier of literacy and linguistic exclusion.
5. **Neutral Range Status ("Within Range", "Higher", "Lower"):** Clearly indicates where the patient's number sits relative to the lab's printed interval without declaring whether it is "dangerous" or "good".
   * *Reason:* Prevents panic and defensive over-triage while keeping the information accurate and factual.
6. **60-Second Spoken Kannada Voice Note (Audio Player):** High-clarity, warm, slow-cadence spoken audio that delivers the explanation audibly in 60 seconds or less.
   * *Reason:* Serves elderly, visually impaired, or illiterate patients who cannot consume written text.
7. **"3 Questions for Your Doctor" Prompt Generator:** Automatically produces 3 specific, context-aware questions for the patient to ask their physician during their next visit.
   * *Reason:* Empowers the patient and strengthens the patient-doctor relationship instead of circumventing it.
8. **Dual-View Visual Summary Card:** Clean, high-contrast mobile screen displaying green and amber status bars with side-by-side Kannada and English parameter names.
   * *Reason:* Enables family members or caregivers to verify values and share them easily with attending doctors.
9. **Mandatory Ephemeral DPDP Consent:** 1-tap consent screen in spoken and written Kannada with automated data purging within 15 minutes.
   * *Reason:* Mandatory compliance with Sections 5, 6, and 8 of the Indian DPDP Act 2023.

---

### 4.2 Later (Post-MVP Roadmap — Post Validation)
*High-value features to incorporate once the core Kannada literacy engine is clinically validated and defensible.*

1. **B2B Doctor/Clinic Verification Portal ("Clinician-in-the-Loop"):** A web dashboard allowing attending doctors or clinic nurses to preview and approve the generated Kannada audio explanation with a single tap before dispatching to the patient.
   * *Reason:* Fully unlocks the B2B commercial model with hospitals and diagnostic chains; not required for standalone consumer usability testing.
2. **Expansion to Additional Regional Languages (Hindi, Telugu, Tamil, Marathi):** Extending the plain-language engine and localized TTS to other major Indian linguistic populations.
   * *Reason:* High market value, but requires dedicated regional linguistic reviews to prevent awkward or inaccurate translations.
3. **Expanded Chronic Disease Panels (Thyroid, Liver Function, Complete Blood Count):** Extending parameter definitions to TSH, T3/T4, SGOT/SGPT, Bilirubin, Hemoglobin, and Platelets.
   * *Reason:* Natural clinical progression once diabetes and hypertension are perfected.
4. **Longitudinal Biomarker History & Trend Comparison:** Allowing users to opt into secure profile creation to track their HbA1c or blood pressure changes over successive tests (*e.g., "Your HbA1c was 8.5% in August and is 7.4% today"*).
   * *Reason:* Adds substantial long-term value, but requires persistent encrypted storage, user account management, and DPDP compliance infrastructure.
5. **Ayushman Bharat Digital Mission (ABDM) / ABHA Integration:** Connecting with the national health grid (M1, M2, M3 milestones) to fetch lab records directly via government-approved consent managers.
   * *Reason:* Exceptional distribution channel, but introduces extensive government sandbox certification timelines.
6. **WhatsApp Interactive Audio Bot (Voice Note in, Voice Note out):** Native integration enabling patients to simply forward a PDF or photo to a verified WhatsApp Business number and receive a voice message back.
   * *Reason:* Superior user experience; can launch as soon as WhatsApp Business API compliance and phone verification are established.
7. **Caregiver Forwarding & Family Notification:** 1-click option to forward the generated audio note and visual card to an adult son or daughter residing in another city.
   * *Reason:* Alleviates family anxiety and facilitates shared caregiving.

---

### 4.3 Never (Strict Red Lines & Regulatory Guardrails)
*Features that are permanently prohibited because they violate clinical safety, cross into unauthorized medical practice, trigger severe medical device liability, or compromise patient rights under Indian law.*

```
+───────────────────────────────────────────────────────────────────────────────────────────────────+
|                                    PROHIBITED PRODUCT BOUNDARIES                                  |
+───────────────────────────────────────────────────────────────────────────────────────────────────+
| [X] NO Autonomous Clinical Diagnoses ("You have diabetic kidney disease")                         |
| [X] NO Medication Alterations or Dose Recommendations ("Increase Metformin to 1000mg")           |
| [X] NO Advising Patients to Start, Stop, or Skip Any Prescribed Medicine                          |
| [X] NO Autonomous Handwritten Prescription Decoding for Direct Drug Ordering                      |
| [X] NO Promoting or Suggesting Unscientific Home Remedies or Alternative "Cures"                  |
| [X] NO Overriding Doctor Advice or Triage Instructions ("You do not need to see your doctor")     |
| [X] NO Retaining Patient Health Records or PII for Training AI Models                             |
| [X] NO Generating Commercial Advertisements for Specific Drug Brands or Pharmaceutical Companies  |
+───────────────────────────────────────────────────────────────────────────────────────────────────+
```

1. **NEVER Provide an Autonomous Clinical Diagnosis:**
   * *Prohibited Example:* *"Your high creatinine and microalbumin mean you have Stage 3 Chronic Kidney Disease."*
   * *Reason:* Violates the National Medical Commission (NMC) Act and Telemedicine Practice Guidelines (2020), which state that only a Registered Medical Practitioner (RMP) can diagnose illness. It also triggers CDSCO Class C Medical Device regulation (Doc No. CDSCO/MD/GD/MDSW/01/2026).
2. **NEVER Recommend, Modify, or Adjust Medication Dosages:**
   * *Prohibited Example:* *"Your fasting sugar is 180 mg/dL, so you should increase your insulin dose by 4 units."*
   * *Reason:* Prescribing or modifying medication autonomously is a severe criminal offense under the NMC Act, Drugs and Cosmetics Act (1940), and Indian Penal Code / Bharatiya Nyaya Sanhita (causing hurt by negligence).
3. **NEVER Advise a Patient to Discontinue or Skip Prescribed Medicines:**
   * *Prohibited Example:* *"Your blood pressure is normal today (120/80), so you can stop taking your Telmisartan."*
   * *Reason:* Patients who discontinue chronic maintenance medications experience rebound crises (e.g., hypertensive stroke). The app must emphasize adherence to existing doctor instructions.
4. **NEVER Autonomously Interpret Handwritten Prescriptions for Direct Dispensing:**
   * *Prohibited Example:* Using multimodal OCR to read messy cursive handwriting and pushing cart items directly into an online pharmacy.
   * *Reason:* Look-alike, sound-alike (LASA) drug errors (e.g., Metformin vs. Metoprolol, Losartan vs. Lotensin) in handwritten Indian prescriptions carry lethal risk when unverified by a licensed pharmacist.
5. **NEVER Suggest or Validate Unscientific Home Remedies or "Miracle Cures":**
   * *Prohibited Example:* Recommending bitter gourd (karela) juice, fenugreek water, or herbal concoctions as a replacement for standard diabetes therapy.
   * *Reason:* Violates the Drugs and Magic Remedies (Objectionable Advertisements) Act (1954) and replicates the exact medical misinformation epidemic documented in family WhatsApp groups.
6. **NEVER Tell a Patient They Do Not Need to See a Doctor:**
   * *Prohibited Example:* *"All your test results are in normal range, so you can cancel your doctor appointment."*
   * *Reason:* Lab tests are only one component of a clinical assessment. A patient with normal blood tests may still have acute cardiac ischemia or other occult symptoms requiring physical examination.
7. **NEVER Retain Identifiable Patient Health Data or Use It for Public Model Training:**
   * *Prohibited Example:* Sending unredacted lab reports to public commercial LLM APIs that retain data for model training.
   * *Reason:* Direct violation of Section 8(5) of the Digital Personal Data Protection Act (DPDP Act) 2023, exposing the entity to fines up to ₹250 crore.
8. **NEVER Host Sponsored Drug Advertisements or Brand Promotions:**
   * *Prohibited Example:* Displaying banner ads for specific pharma brands or alternative clinics alongside report explanations.
   * *Reason:* Violates medical ethics standards and destroys patient trust, creating commercial conflict of interest.
