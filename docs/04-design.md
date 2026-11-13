# Design System & UI Specification: ReportSaathi

**Document:** `docs/04-design.md`  
**Reference Scope:** `docs/03-scope.md`, `docs/02-research.md`, `docs/01-problem.md`  
**Target User:** Older adults (55–75+ years) and family caregivers in Karnataka, India  
**Target Hardware:** Budget Android devices (Redmi A-series, Samsung Galaxy M/F budget series, realme C-series, 360×800px display, low RAM)  
**Target Script & Language:** Kannada (Brahmic abugida with stacked conjuncts) + English medical subtext  
**Date:** November 2026  

---

## Visual Reference Library

All benchmark reference analyses and core flow screen mockups are located in [docs/references/](file:///c:/Users/ACER/reportsaathi/docs/references/):

* **Benchmark References:**
  1. [ref-01-whatsapp-voice.png](file:///c:/Users/ACER/reportsaathi/docs/references/ref-01-whatsapp-voice.png) — *WhatsApp audio & voice note standard.*
  2. [ref-02-ada-health.png](file:///c:/Users/ACER/reportsaathi/docs/references/ref-02-ada-health.png) — *Ada Health calm clinical card layout.*
  3. [ref-03-phonepe-vernacular.png](file:///c:/Users/ACER/reportsaathi/docs/references/ref-03-phonepe-vernacular.png) — *PhonePe / Soundbox high-contrast tactile UI.*
  4. [ref-04-tata1mg-dense-lab.png](file:///c:/Users/ACER/reportsaathi/docs/references/ref-04-tata1mg-dense-lab.png) — *Tata 1mg dense English lab report table (what to avoid).*
* **Core Flow Screen Mockups:**
  1. [screen-01-upload.png](file:///c:/Users/ACER/reportsaathi/docs/references/screen-01-upload.png) — *Screen 1: Welcome & Report Ingestion.*
  2. [screen-02-consent.png](file:///c:/Users/ACER/reportsaathi/docs/references/screen-02-consent.png) — *Screen 2: DPDP Statutory Consent & Preview.*
  3. [screen-03-loading.png](file:///c:/Users/ACER/reportsaathi/docs/references/screen-03-loading.png) — *Screen 3: Processing & Extraction.*
  4. [screen-04-result.png](file:///c:/Users/ACER/reportsaathi/docs/references/screen-04-result.png) — *Screen 4: Report Explanation, Audio Player & Doctor Questions.*
  5. [screen-05-rejection.png](file:///c:/Users/ACER/reportsaathi/docs/references/screen-05-rejection.png) — *Screen 5: Graceful Safety Rejection.*

---

## 1. Core Flow Screen Inventory & State Matrix

The core flow consists of **5 dedicated screens**. To ensure bulletproof reliability on low-cost devices and zero user frustration, every screen defines **four explicit states**: Default, Empty, Loading, and Error.

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    CORE FLOW SCREEN LIFECYCLE                                     │
├───────────────┬───────────────────┬───────────────────┬───────────────────┬───────────────────────┤
│ SCREEN 1      │ SCREEN 2          │ SCREEN 3          │ SCREEN 4          │ SCREEN 5              │
│ Welcome &     │ DPDP Consent &    │ Processing &      │ Result, Audio &   │ Safety Rejection      │
│ Ingestion     │ Document Preview  │ Extraction        │ Doctor Questions  │ (Invalid / Prescr.)   │
│               │                   │ (Loading Hub)     │ (Primary Value)   │                       │
└───────────────┴───────────────────┴───────────────────┴───────────────────┴───────────────────────┘
```

---

### Screen 1: Welcome & Report Ingestion (ಮುಖಪುಟ ಮತ್ತು ವರದಿ ಅಪ್‌ಲೋಡ್)
*Mockup Reference:* [screen-01-upload.png](file:///c:/Users/ACER/reportsaathi/docs/references/screen-01-upload.png)  
*User Objective:* Understand that the tool explains blood test reports in spoken Kannada, select a report file or take a camera picture with zero cognitive friction.

| State | UI Layout & Visual Elements | Copy / Microcopy (Kannada & English) | Interactive Actions | Accessibility & Fallback |
| :--- | :--- | :--- | :--- | :--- |
| **Default** | • App bar with dual branding.<br>• Language badge: `🗣️ ಕನ್ನಡ (Kannada)`.<br>• Prominent instruction card.<br>• Large dashed dropzone area with camera & document icons.<br>• Two 56px primary CTA buttons.<br>• Yellow bottom banner: Lab reports only. | **Heading:** ನಿಮ್ಮ ರಕ್ತ ಪರೀಕ್ಷೆ ವರದಿಯನ್ನು ಸುಲಭವಾಗಿ ತಿಳಿಯಿರಿ (*Understand your blood test easily*)<br>**Subtext:** ಮಧುಮೇಹ ಮತ್ತು ಬಿಪಿ ಪರೀಕ್ಷೆಗಳು (*Diabetes & BP tests*)<br>**Button 1:** ಕ್ಯಾಮೆರಾದಿಂದ ಫೋಟೋ ತೆಗೆಯಿರಿ (*Take Photo*)<br>**Button 2:** ಫೋನ್‌ನಿಂದ PDF ಆಯ್ಕೆಮಾಡಿ (*Choose PDF*) | • Tap Button 1: Opens native camera capture.<br>• Tap Button 2: Opens system file picker filtered to `.pdf, .jpg, .png`. | • Screen reader announcement: "ವರದಿ ಸಾಥಿ ಮುಖಪುಟ. ರಕ್ತ ಪರೀಕ್ಷೆ ಫೋಟೋ ತೆಗೆಯಿರಿ."<br>• High-contrast borders (2px). |
| **Empty** | Rendered identically to Default state. No draft files or cached uploads are shown to prevent confusing previous session remnants. | Same as Default. | System is primed and waiting for user input. | None. |
| **Loading** | Upload dropzone dims to 60% opacity. Central circular spinner with text badge. Both CTA buttons disable (`disabled="true"`). | **Status:** ವರದಿ ಅಪ್‌ಲೋಡ್ ಆಗುತ್ತಿದೆ... (*Uploading report... Please wait*) | All upload triggers disabled to prevent double-submission on slow 3G networks. | Audible subtle beep indicating upload initiation. |
| **Error** | Red-tinted alert banner inserted directly above dropzone (`#FEF2F2`, border `#F87171`). | **Alert:** ಫೈಲ್ ಗಾತ್ರ 10 MB ಗಿಂತ ಹೆಚ್ಚಾಗಿದೆ ಅಥವಾ ತೆರೆಯಲು ಸಾಧ್ಯವಿಲ್ಲ. (*File exceeds 10 MB or cannot be opened. Try again.*) | "ಮತ್ತೊಮ್ಮೆ ಪ್ರಯತ್ನಿಸಿ" (*Try Again*) button restores Default state. | Focus automatically shifts to error banner with VoiceOver/TalkBack announcement. |

---

### Screen 2: DPDP Statutory Consent & Preview (ಸಮ್ಮತಿ ಮತ್ತು ಪರಿಶೀಲನೆ)
*Mockup Reference:* [screen-02-consent.png](file:///c:/Users/ACER/reportsaathi/docs/references/screen-02-consent.png)  
*User Objective:* Verify that the uploaded document looks correct, hear or read mandatory DPDP Act consent terms in plain Kannada, and confirm processing.

| State | UI Layout & Visual Elements | Copy / Microcopy (Kannada & English) | Interactive Actions | Accessibility & Fallback |
| :--- | :--- | :--- | :--- | :--- |
| **Default** | • Document thumbnail card with green check badge (`✓ ಲ್ಯಾಬ್ ವರದಿ ಪತ್ತೆಯಾಗಿದೆ`).<br>• File metadata: Name, page count, file size.<br>• 1-tap audio player for consent terms.<br>• 4-bullet plain-language DPDP notice.<br>• Primary 56px emerald button & neutral secondary button. | **Heading:** ಸಮ್ಮತಿ ಮತ್ತು ಪರಿಶೀಲನೆ (*Consent & Review*)<br>**Audio Pill:** ಸಮ್ಮತಿ ಧ್ವನಿ ವಿವರಣೆ (0:20) (*Listen to consent in Kannada*)<br>**Points:**<br>1. 15 ನಿಮಿಷಗಳಲ್ಲಿ ವರದಿ ಅಳಿಸಲಾಗುತ್ತದೆ (*Purged in 15 mins*)<br>2. ಎಐ ತರಬೇತಿಗೆ ಬಳಸುವುದಿಲ್ಲ (*Not used for AI training*)<br>3. ಕೇವಲ ಮಾಹಿತಿ, ವೈದ್ಯರ ಸಲಹೆಯಲ್ಲ (*Informational only*)<br>**CTA:** ನಾನು ಒಪ್ಪುತ್ತೇನೆ - ವಿವರಣೆ ನೀಡಿ (*I Agree & Explain*) | • Tap Audio Pill: Plays 20-second spoken Kannada consent readout.<br>• Tap CTA: Commits consent timestamp and transitions to Screen 3.<br>• Tap Cancel: Purges document and returns to Screen 1. | • Full audio equivalence for illiterate users who cannot read the 4 clauses.<br>• Minimum touch target height: 56px. |
| **Empty** | If accessed without an uploaded file in session, immediately redirects to Screen 1. | Redirecting... | None. | Seamless back-navigation. |
| **Loading** | "I Agree" button displays inline circular spinner. Button text changes to "ಧ್ವನಿ ಸಿದ್ಧಪಡಿಸಲಾಗುತ್ತಿದೆ...". | ಸಮ್ಮತಿ ದೃಢೀಕರಿಸಲಾಗುತ್ತಿದೆ... (*Confirming consent...*) | Buttons disabled to prevent concurrent processing jobs. | Continuous progress announcement. |
| **Error** | Thumbnail fails to render (corrupted image/PDF). Red alert box replaces thumbnail. | **Error:** ಫೈಲ್ ತೆರೆಯಲು ಸಾಧ್ಯವಾಗುತ್ತಿಲ್ಲ. ದಯವಿಟ್ಟು ಸ್ಪಷ್ಟವಾದ ಫೋಟೋ ತೆಗೆಯಿರಿ. (*Cannot open file. Please upload a clear photo.*) | "ಬೇರೆ ಫೈಲ್ ಆಯ್ಕೆಮಾಡಿ" (*Choose Another File*) button returns to Screen 1. | Audio prompt: "ಫೈಲ್ ದೋಷಪೂರಿತವಾಗಿದೆ, ಬೇರೆ ಫೋಟೋ ಹಾಕಿ." |

---

### Screen 3: Processing & Extraction (ಪರಿಶೀಲಿಸಲಾಗುತ್ತಿದೆ - Loading Hub)
*Mockup Reference:* [screen-03-loading.png](file:///c:/Users/ACER/reportsaathi/docs/references/screen-03-loading.png)  
*User Objective:* Reassure the user during the 6-to-12 second AI extraction and Kannada speech synthesis window that the system is working safely.

| State | UI Layout & Visual Elements | Copy / Microcopy (Kannada & English) | Interactive Actions | Accessibility & Fallback |
| :--- | :--- | :--- | :--- | :--- |
| **Default (Loading)** | • High-contrast central pulsing circle with hourglass icon.<br>• Bold Kannada waiting headline.<br>• 3 sequential step progress cards:<br>  1. *Reading report* (Green check ✓)<br>  2. *Checking sugar & BP* (Amber pulse ⏳)<br>  3. *Synthesizing Kannada voice* (Pending ⚪)<br>• Privacy assurance box at bottom. | **Heading:** ದಯವಿಟ್ಟು ಕೆಲವು ಸೆಕೆಂಡುಗಳು ಕಾಯಿರಿ (*Please wait a few seconds*)<br>**Sub:** Generating simple Kannada voice explanation...<br>**Steps:**<br>1. ವರದಿ ದಾಖಲೆ ಓದಲಾಗಿದೆ<br>2. ಅಳತೆಗಳನ್ನು ಪರಿಶೀಲಿಸಲಾಗುತ್ತಿದೆ<br>3. ಕನ್ನಡ ಧ್ವನಿ ಸಿದ್ಧವಾಗುತ್ತಿದೆ | None (automated background processing pipeline). Screen auto-navigates upon completion. | Dynamic live region (`aria-live="polite"`) updates TalkBack as each of the 3 steps completes. |
| **Empty** | Not applicable; transient state. | N/A | N/A | N/A |
| **Timeout (Slow 3G)** | Reaches 15 seconds without completion. Yellow warning card appears under steps. | ಇಂಟರ್ನೆಟ್ ಸಂಪರ್ಕ ನಿಧಾನವಾಗಿದೆ, ದಯವಿಟ್ಟು ಕಾಯಿರಿ... (*Internet connection is slow, still working...*) | "ಮತ್ತೊಮ್ಮೆ ಪ್ರಯತ್ನಿಸಿ" (*Retry*) option appears after 25 seconds. | Prevents user from closing the browser thinking the app froze. |
| **Processing Error** | AI extraction fails (network crash or service failure). Step indicator turns red with retry card. | **Error:** ಸರ್ವರ್ ಸಂಪರ್ಕ ಕಡಿತಗೊಂಡಿದೆ. ದಯವಿಟ್ಟು 1 ನಿಮಿಷದ ನಂತರ ಪ್ರಯತ್ನಿಸಿ. (*Server disconnected. Please retry.*) | Prominent button: "ಮತ್ತೊಮ್ಮೆ ಪ್ರಯತ್ನಿಸಿ" (*Retry Processing*). | Audio chime alert with retry instruction. |

---

### Screen 4: Report Explanation, Audio & Doctor Questions (ಫಲಿತಾಂಶ ಮತ್ತು ಧ್ವನಿ ವಿವರಣೆ)
*Mockup Reference:* [screen-04-result.png](file:///c:/Users/ACER/reportsaathi/docs/references/screen-04-result.png)  
*User Objective:* Listen to the 60-second spoken Kannada explanation, scan color-coded biomarker ranges, and read/share the 3 questions for the doctor.

| State | UI Layout & Visual Elements | Copy / Microcopy (Kannada & English) | Interactive Actions | Accessibility & Fallback |
| :--- | :--- | :--- | :--- | :--- |
| **Default** | • **Top Hero:** Sticky Emerald Audio Player Card with large play/pause toggle, scrubbable waveform, time elapsed (`0:24 / 0:58`), and `0.8x ನಿಧಾನ` speed pill.<br>• **Middle:** Parameter Cards with universal status badges:<br>  - HbA1c: Amber badge (`ಸಾಮಾನ್ಯಕ್ಕಿಂತ ಹೆಚ್ಚು - 7.8%`)<br>  - Fasting Sugar: Amber badge (`142 mg/dL`)<br>  - Creatinine: Green badge (`ಸಾಮಾನ್ಯ ಮಿತಿಯಲ್ಲಿದೆ - 0.9 mg/dL`)<br>• **Bottom:** High-contrast Blue Box containing 3 doctor questions.<br>• **Footer:** WhatsApp green share button. | **Player:** ಕನ್ನಡ ಧ್ವನಿ ವಿವರಣೆ (0:58) (*Listen to 1-min audio*)<br>**Doctor Questions:**<br>1. ನನ್ನ HbA1c 7.8% ಇರುವುದರಿಂದ ದಿನಚರಿಯಲ್ಲಿ ಏನು ಬದಲಾವಣೆ ಬೇಕು?<br>2. ನನ್ನ ಊಟದ ಪದ್ಧತಿ ಅಥವಾ ಔಷಧಿ ಪರಿಶೀಲಿಸಬೇಕೇ?<br>3. ಮುಂದಿನ ರಕ್ತ ಪರೀಕ್ಷೆಯನ್ನು ಯಾವಾಗ ಮಾಡಿಸಬೇಕು?<br>**Footer CTA:** ವಾಟ್ಸಾಪ್‌ನಲ್ಲಿ ಕುಟುಂಬದವರಿಗೆ ಕಳುಹಿಸಿ (*Share to WhatsApp*) | • Tap Play/Pause: Toggles audio playback.<br>• Tap `0.8x`: Switches speech cadence to slow mode for older ears.<br>• Tap Parameter: Expands 1-sentence plain-language Kannada analogy.<br>• Tap WhatsApp: Opens native share sheet with audio clip & question text. | • Audio auto-focuses on load.<br>• Color is NEVER the sole indicator: every badge pairs color with written Kannada text and an icon.<br>• Contrast ratio > 10:1. |
| **Empty (Partial Data)** | One or more parameters missing (e.g. lab did not test Creatinine). | The card for that parameter displays: "ಈ ವರದಿಯಲ್ಲಿ ಕಿಡ್ನಿ ಪರೀಕ್ಷೆ ಲಭ್ಯವಿಲ್ಲ" (*Not tested in this report*). | The remaining tested parameters render normally; missing ones are grayed out. | Transparent disclosure prevents guessing. |
| **Loading Audio** | Voice note audio buffer is downloading over slow connection. | Audio player button shows small circular loader; waveform displays muted gray bars. | User can still read visual cards while audio finishes loading. | Seamless progressive enhancement. |
| **Audio Playback Error** | Audio codec fails or playback is interrupted. | "ಧ್ವನಿ ಪ್ಲೇ ಮಾಡಲು ಸಾಧ್ಯವಾಗುತ್ತಿಲ್ಲ. ಪಠ್ಯ ವಿವರಣೆ ಓದಿ." (*Cannot play audio. Please read text summary below.*) | "ಧ್ವನಿ ಮರುಲೋಡ್ ಮಾಡಿ" (*Reload Audio*) button. | Full visual text fallback ensures zero value loss if audio fails. |

---

### Screen 5: Graceful Safety Rejection (ಸುರಕ್ಷತಾ ಸಂದೇಶ / ತಪ್ಪು ಪತ್ತೆ)
*Mockup Reference:* [screen-05-rejection.png](file:///c:/Users/ACER/reportsaathi/docs/references/screen-05-rejection.png)  
*User Objective:* Understand with empathy why an uploaded document was rejected (e.g., doctor's handwritten prescription or blurry photo) and know what to do next.

| State | UI Layout & Visual Elements | Copy / Microcopy (Kannada & English) | Interactive Actions | Accessibility & Fallback |
| :--- | :--- | :--- | :--- | :--- |
| **Default (Prescription Detected)** | • Top red-tinted shield card (`#FEF2F2`, border `#EF4444`).<br>• Amber audio player explaining rejection reason in Kannada voice.<br>• Side-by-side visual comparison cards:<br>  - Left (Green): *What we support (Printed lab reports)*<br>  - Right (Red): *What we block (Handwritten prescriptions)*<br>• Large primary CTA to upload a real lab report. | **Alert:** ಇದು ವೈದ್ಯರ ಕೈಬರಹದ ಚೀಟಿಯಾಗಿದೆ (*Doctor's Handwritten Prescription Detected*)<br>**Audio:** ಸುರಕ್ಷತಾ ವಿವರಣೆ ಆಲಿಸಿ (0:18) (*Listen to safety explanation*)<br>**Audio Script:** "ನಮಸ್ಕಾರ, ಸುರಕ್ಷತೆಯ ದೃಷ್ಟಿಯಿಂದ ನಾವು ಕೇವಲ ಲ್ಯಾಬ್ ರಕ್ತ ಪರೀಕ್ಷೆ ವರದಿಗಳನ್ನು ಮಾತ್ರ ವಿವರಿಸುತ್ತೇವೆ..."<br>**CTA:** ಸ್ಪಷ್ಟವಾದ ಲ್ಯಾಬ್ ವರದಿ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ (*Upload Clear Lab Report*) | • Tap Audio: Explains medication risks of handwritten scripts in spoken Kannada.<br>• Tap CTA: Returns to Screen 1 with camera open. | Spoken audio explanation ensures non-literate patients understand why their file was declined rather than feeling rejected by software. |
| **Blurry / Cut-Off Photo State** | Graphic changes from shield to camera lens icon. | **Alert:** ಫೋಟೋ ಮಬ್ಬಾಗಿದೆ ಅಥವಾ ಅಕ್ಷರಗಳು ಕಾಣಿಸುತ್ತಿಲ್ಲ. (*Photo is blurry or numbers are cut off.*) | CTA: "ಮತ್ತೆ ಸ್ಪಷ್ಟವಾಗಿ ಫೋಟೋ ತೆಗೆಯಿರಿ" (*Retake Clear Photo*). | Displays an illuminated camera guideline frame showing how to hold the phone flat. |
| **Loading** | Transitioning back to camera or home screen. | ಸಿದ್ಧವಾಗುತ್ತಿದೆ... (*Preparing camera...*) | Disabled. | None. |
| **Persistent Failure State** | User fails 3 consecutive uploads. | **Card:** ದಯವಿಟ್ಟು ನಿಮ್ಮ ಕುಟುಂಬದವರ ಅಥವಾ ಲ್ಯಾಬ್ ಸಿಬ್ಬಂದಿಯ ನೆರವು ಪಡೆಯಿರಿ. (*Please ask a family member or lab staff to help take a photo.*) | Option to share WhatsApp support link. | Escalation path for vulnerable seniors. |

---

## 2. Review of Reference Benchmarks: What to Borrow & What to Avoid

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    BENCHMARK EVALUATION MATRIX                                    │
├─────────────────────┬───────────────────────────────────────┬─────────────────────────────────────┤
│ REFERENCE           │ WHAT TO BORROW                        │ WHAT TO AVOID                       │
├─────────────────────┼───────────────────────────────────────┼─────────────────────────────────────┤
│ 1. WhatsApp Voice   │ • 1-tap green audio player with wave  │ • Chaotic unstructured chat stream  │
│    (Mass Indian     │ • 0.8x / 1.5x speed toggle pill       │ • Unvalidated photo forwards        │
│     Standard)       │ • Universally familiar audio UX       │ • Unchecked medical rumors          │
├─────────────────────┼───────────────────────────────────────┼─────────────────────────────────────┤
│ 2. Ada Health       │ • Calm, non-alarmist medical cards    │ • 30-step questionnaire fatigue     │
│    (Clinical Triage)│ • Clean white containers, soft borders│ • Micro-sized English typography    │
│                     │ • Structured questions for doctors    │ • "Go to ER" panic triggers         │
├─────────────────────┼───────────────────────────────────────┼─────────────────────────────────────┤
│ 3. PhonePe / Sound- │ • High contrast (WCAG AAA)            │ • Aggressive scratch-card ads       │
│    box (FinTech)    │ • Oversized tactile buttons (≥56px)   │ • Dense 20-icon dashboard grids     │
│                     │ • Vernacular spoken audio confirmation│ • Cluttered marketing banners       │
├─────────────────────┼───────────────────────────────────────┼─────────────────────────────────────┤
│ 4. Tata 1mg / Labs  │ • Standard chronic biomarker taxonomy │ • Micro-tables requiring pinch-zoom │
│    (Diagnostic App) │ • Inclusion of official lab limits    │ • Mandatory login & OTP roadblocks  │
│                     │ • Clear test groupings (Sugar, BP)    │ • Zero regional audio explanations  │
├─────────────────────┼───────────────────────────────────────┼─────────────────────────────────────┤
│ 5. Govt ABHA/CoWIN  │ • Bilingual Kannada + English labels  │ • Cold, bureaucratic layout         │
│    (Digital Health) │ • DPDP compliance security badges     │ • Tiny 8pt legal disclaimers        │
│                     │ • High institutional trust cues       │ • Dense multi-page PDF downloads    │
└─────────────────────┴───────────────────────────────────────┴─────────────────────────────────────┘
```

### Detailed Reference Breakdown

#### Reference 1: WhatsApp Voice Note UI
*Visual Reference:* [ref-01-whatsapp-voice.png](file:///c:/Users/ACER/reportsaathi/docs/references/ref-01-whatsapp-voice.png)  
Over 500 million Indians use WhatsApp voice notes daily. It is the single most deeply ingrained digital mental model across all literacy levels.
* **What to Borrow:**
  * The familiar audio card with a play/pause circle, scrubbable waveform bars, and time duration indicator.
  * The speed toggle pill (`0.8x`, `1x`), allowing elderly ears to slow down playback without pitch distortion.
  * The green color cue associated with communication, clarity, and resolution.
* **What to Avoid:**
  * Unstructured chat feeds where critical health numbers get lost among family forwards.
  * Compressing images into unreadable low-resolution photos without checking legibility.

#### Reference 2: Ada Health Clinical Cards
*Visual Reference:* [ref-02-ada-health.png](file:///c:/Users/ACER/reportsaathi/docs/references/ref-02-ada-health.png)  
Ada Health sets the gold standard for serene clinical UI that avoids panic.
* **What to Borrow:**
  * Clean, spacious white card containers with generous 16px padding and soft rounded corners (14px).
  * The concept of preparing structured questions for the doctor instead of giving a definitive diagnosis.
  * Soft neutral color coding rather than alarming neon colors.
* **What to Avoid:**
  * Multi-step interactive branching questionnaires (30+ questions) that cause cognitive fatigue in older adults.
  * Small 12–14px English typography that fails accessibility standards for presbyopic eyes.
  * Hyper-defensive emergency escalation warnings (*"Seek immediate ER care"*) that trigger intense anxiety.

#### Reference 3: PhonePe & Paytm Soundbox Vernacular UI
*Visual Reference:* [ref-03-phonepe-vernacular.png](file:///c:/Users/ACER/reportsaathi/docs/references/ref-03-phonepe-vernacular.png)  
Indian FinTech conquered low-literacy merchant adoption by pairing bold tactile visuals with spoken vernacular audio confirmation.
* **What to Borrow:**
  * Massive touch targets: Minimum button height of 56px, spanning full container width.
  * Extreme visual contrast: Bold dark text on bright white or emerald backgrounds.
  * Immediate spoken voice readout: Reinforcing visual state with an audible announcement.
* **What to Avoid:**
  * Visual pollution: Banners for insurance, gold loans, scratch cards, and gaming rewards.
  * Dense multi-row icon grids that overwhelm users with choices.

#### Reference 4: Tata 1mg / Dr Lal PathLabs Diagnostic Apps
*Visual Reference:* [ref-04-tata1mg-dense-lab.png](file:///c:/Users/ACER/reportsaathi/docs/references/ref-04-tata1mg-dense-lab.png)  
Standard Indian diagnostic lab applications prioritize lab operations over patient comprehension.
* **What to Borrow:**
  * Logical grouping of chronic parameters (Fasting Sugar, PPBS, HbA1c, Lipid Profile, Kidney markers).
  * Always displaying the testing laboratory's printed reference range alongside the patient's observed number.
* **What to Avoid:**
  * Dense desktop-style data tables with 5 tight columns crammed into a 360px mobile screen.
  * Pure English medical terminology (*e.g., Glycosylated Hemoglobin, Microalbuminuria, eGFR*) without plain-language translation.
  * Forced account creation, password requirements, and SMS OTP loops before letting a user view their report.

#### Reference 5: Government Health Cards (ABHA & CoWIN)
* **What to Borrow:**
  * Bilingual side-by-side presentation: Primary regional script (Kannada) with secondary English medical name.
  * Clear data privacy badges and institutional trust indicators.
* **What to Avoid:**
  * Rigid, uninviting bureaucratic aesthetic with crowded margins.
  * Micro-text legal disclaimers hidden in 8pt gray font that patients ignore.

---

## 3. Design Direction: Layout, Typography, Colour, Spacing & Tone

### 3.1 Layout Architecture (Mobile-First 360px–390px Viewport)
Low-cost Indian Android phones have viewports between 360px and 390px wide (e.g., 360×800 or 390×844 resolution).

```
┌─────────────────────────────────────────┐ ◄── 0px
│ Status Bar (System)                     │
├─────────────────────────────────────────┤ ◄── 28px
│ App Bar (Branding + Language Badge)     │ (56px height)
├─────────────────────────────────────────┤ ◄── 84px
│                                         │
│ 1. HERO AUDIO CARD (Sticky at Top)      │ (110px height - Instant audio access)
│                                         │
├─────────────────────────────────────────┤
│                                         │
│ 2. PARAMETER CARDS (Single Column Stack)│ (Cards stacked vertically with 12px gap;
│    • HbA1c Card                         │  never horizontal carousels or tabs)
│    • Fasting Blood Sugar Card           │
│    • Serum Creatinine Card              │
│                                         │
├─────────────────────────────────────────┤
│                                         │
│ 3. ACTIONABLE TAKEAWAY (Doctor Box)     │ (High-contrast blue card; 3 bullet questions)
│                                         │
├─────────────────────────────────────────┤
│                                         │
│ 4. THUMB-ZONE ACTIONS (Bottom 40%)      │ (56px high primary CTA: WhatsApp Share)
│                                         │
└─────────────────────────────────────────┘ ◄── 800px / 844px
```

* **Strict Single-Column Flow:** Zero multi-column tables. Every lab parameter receives its own dedicated card with full horizontal width.
* **Zero Gesture Dependence:** No swiping, dragging, pull-to-refresh, or pinch-to-zoom. All interactions are driven by simple, explicit 1-tap buttons.
* **Thumb Zone Optimization:** Primary interactive buttons and audio controls are anchored in the lower 40% of the screen where older thumbs naturally rest.

---

### 3.2 Typography & Kannada Script Engineering

Kannada is an abugida script with complex vertical stacking (subjoined consonants / *vattugalu* and vowel *maatras* like `ರ್ಕ`, `ಷ್ಟ`, `ಷ್ಣ`). Standard Western typography rules break Kannada rendering by clipping ascenders and descenders.

```
       STANDARD ENGLISH FONT               KANNADA SCRIPT WITH STACKED VATTUGALU
       Line-height: 1.2x (OK)              Line-height: 1.65x (MANDATORY TO AVOID CLIPPING)
       ┌────────────────────────┐         ┌──────────────────────────────────────────────┐
       │ Blood Sugar: 140 mg/dL │         │ ರಕ್ತದಲ್ಲಿನ ಸಕ್ಕರೆ ಪ್ರಮಾಣ: ೧೪೦ mg/dL           │ ◄── Top Maatra (ಾ, ಿ)
       └────────────────────────┘         │ ಕಳೆದ ಮೂರು ತಿಂಗಳ ಸರಾಸರಿ (HbA1c)               │ ◄── Subjoined Vattu (್ಕ, ಷ್ಟ)
                                          └──────────────────────────────────────────────┘
```

1. **Font Family Selection:**
   * Primary Font: `Noto Sans Kannada` / `Nirmala UI` (pre-installed across 100% of Android and Windows devices in India).
   * Secondary Font: `Roboto` / `Inter` for numbers and Latin units (`mg/dL`, `%`).
2. **Generous Line Height (1.65x – 1.7x):**
   * While English uses a line-height of 1.2 to 1.3, Kannada **requires a minimum line-height of 1.65**. Anything tighter physically clips vowel diacritics and subjoined consonants.
3. **Type Scale for Presbyopic Vision:**
   * **App Bar / Title:** 18px Bold (Kannada) / 13px Regular (English).
   * **Section Headings:** 17px–18px Bold.
   * **Primary Body Text:** Minimum 16px–18px Regular (never below 16px).
   * **Biomarker Values (Numbers):** 20px–24px Bold (high visual prominence).
   * **Subtext / Reference Ranges:** 12px–13px Regular.
4. **Handling Long Words & Expansion:**
   * Kannada compound words (*sandhi/samasa*) run **35% to 50% longer than English** (*e.g., "ಮೂತ್ರಪಿಂಡಗಳ ಶುದ್ಧೀಕರಣ ಸಾಮರ್ಥ್ಯ"*).
   * *Rule:* Never use fixed-width horizontal pill containers for Kannada text. Use `white-space: normal`, flexible vertical wrapping, and avoid text truncation (`text-overflow: ellipsis`) on health descriptions.
5. **No ALL-CAPS:**
   * Kannada has no concept of capital and lowercase letters. Emphasis must be communicated using **font weight (Bold)**, a colored container badge, or subtle background elevation.

---

### 3.3 Accessible & Non-Alarmist Colour Palette

The palette is engineered for two critical constraints: **extreme contrast under harsh Indian sunlight** and **zero clinical panic ("cyberchondria")**.

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   REPORTSAATHI ACCESSIBLE PALETTE                                 │
├───────────────────────┬─────────────────────────┬───────────────────────┬─────────────────────────┤
│ CLINICAL TEAL         │ IN-RANGE GREEN          │ OUT-OF-RANGE AMBER    │ REJECTION RED           │
│ (Primary Brand)       │ (Within Lab Limits)     │ (Non-Panic Alert)     │ (Safety Shield)         │
│ #0D6E5C               │ #15803D                 │ #B45309               │ #991B1B                 │
│ Contrast vs Wht: 6.2:1│ Contrast vs Wht: 5.8:1  │ Contrast vs Wht: 5.5:1│ Contrast vs Wht: 8.5:1  │
│ Container: #ECFDF5    │ Container: #DCFCE7      │ Container: #FEF3C7    │ Container: #FEF2F2      │
└───────────────────────┴─────────────────────────┴───────────────────────┴─────────────────────────┘
```

1. **Primary Brand — Clinical Teal (`#0D6E5C`):**
   * Conveys clinical authority, calm, and healing. Used for app bars, primary audio players, and affirmative buttons.
2. **Neutral Status — In-Range Forest Green (`#15803D`, background `#DCFCE7`):**
   * Used when a biomarker falls comfortably within the lab's printed reference range. Provides immediate reassurance.
3. **Caution Status — Non-Panic Warm Amber (`#B45309`, background `#FEF3C7`):**
   * **CRITICAL DESIGN CHOICE:** Standard lab apps use flashing neon red for any out-of-range value, triggering acute panic. ReportSaathi deliberately uses **Warm Amber**. It signals *"Needs doctor discussion"* without implying *"You are having a medical emergency"*.
4. **Prohibition Status — Crimson Rose (`#991B1B`, background `#FEF2F2`):**
   * Reserved strictly for document safety rejections (Screen 5) to prevent misreading doctor handwriting.
5. **High-Contrast Text (`#0F172A` / `#1E293B`):**
   * Deep slate-black on pure white or warm off-white (`#F8FAFC`). Contrast ratio exceeds **12:1**, far surpassing WCAG AAA (7:1) for outdoor readability.

---

### 3.4 Spacing, Hit Targets & Touch Physics

Older adults and diabetic patients frequently suffer from peripheral neuropathy (reduced fingertip sensation) and resting tremors.

* **56px Minimum Touch Target Height:** All buttons, audio toggles, and expandable cards have a minimum vertical touch area of 56px (surpassing the standard 48px Material design guideline).
* **12px Minimum Separation:** Interactive buttons are separated by at least 12px of vertical dead space to prevent accidental clicks.
* **16px Screen Margins:** Content is padded by 16px from the phone's physical bezel to prevent edge-swipe conflicts.
* **Tactile Visual Feedback:** Buttons feature a distinct pressed state (darkening by 10% with a 1px downward translation) so users immediately know their tap registered on slow budget touchscreens.

---

### 3.5 Spoken Voice & Conversational Tone

The tone of ReportSaathi is that of a **knowledgeable, respectful elder family friend or community health worker (*Saathi*) speaking in clear, everyday Kannada**.

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                     TONE & VOCABULARY COMPARISON                                  │
├─────────────────────────────────────────┬─────────────────────────────────────────────────────────┤
│ AVOID (Cold, Clinical, Robotic)         │ USE (Warm, Respectful, Conversational Kannada)          │
├─────────────────────────────────────────┼─────────────────────────────────────────────────────────┤
│ "ಗ್ಲೈಕೋಸಿಲೇಟೆಡ್ ಹಿಮೋಗ್ಲೋಬಿನ್ ಶೇಕಡಾ ೭.೮     │ "ನಿಮ್ಮ ಕಳೆದ ಮೂರು ತಿಂಗಳ ರಕ್ತದಲ್ಲಿನ ಸಕ್ಕರೆ ಪ್ರಮಾಣದ ಸರಾಸರಿ  │
│ ತೀವ್ರ ಹೈಪರ್‌ಗ್ಲೈಸೀಮಿಯಾವನ್ನು ಸೂಚಿಸುತ್ತದೆ."   │ ೭.೮% ಬಂದಿದೆ. ಇದು ಲ್ಯಾಬ್‌ನ ಸಾಮಾನ್ಯ ಮಿತಿಗಿಂತ ಹೆಚ್ಚಾಗಿದೆ."  │
│ (Archaic Sanskritized / Latin jargon)   │ (Relatable daily-life explanation)                      │
├─────────────────────────────────────────┼─────────────────────────────────────────────────────────┤
│ "ನೀವು ತಕ್ಷಣ ಮಧುಮೇಹ ತಜ್ಞರನ್ನು ಕಾಣಬೇಕು."  │ "ಈ ಸಂಖ್ಯೆಯ ಬಗ್ಗೆ ನಿಮ್ಮ ವೈದ್ಯರನ್ನು ಭೇಟಿಯಾದಾಗ ಕೇಳಲು ನಾವು    │
│ (Alarmist command inducing panic)       │ ಮೂರು ಮುಖ್ಯ ಪ್ರಶ್ನೆಗಳನ್ನು ಸಿದ್ಧಪಡಿಸಿದ್ದೇವೆ."              │
│                                         │ (Empowering preparation for clinical visit)             │
├─────────────────────────────────────────┼─────────────────────────────────────────────────────────┤
│ "ನಿಮ್ಮ ಮಾತ್ರೆ ಪ್ರಮಾಣವನ್ನು ಹೆಚ್ಚು ಮಾಡಿ." │ "ನಿಮ್ಮ ಆಹಾರ ಪದ್ಧತಿ ಅಥವಾ ಔಷಧಿಗಳ ಬಗ್ಗೆ ವೈದ್ಯರ ಸಲಹೆ ಪಡೆಯಿರಿ." │
│ (UNLAWFUL: Autonomous dosage modification) (Strict adherence to existing clinician relationship)  │
└─────────────────────────────────────────┴─────────────────────────────────────────────────────────┘
```

* **Respectful Kannada Pronouns:** Uses respectful plural pronouns (*"ನಿಮ್ಮ"*, *"ಆತ್ಮೀಯರೇ"*) suited for addressing elders.
* **Slow Speech Cadence:** The default text-to-speech engine speaks at **0.9x speed** with clear pauses between sentences, and offers a 1-tap `0.8x` toggle for elderly listeners.
* **Empowering Closing:** Every audio summary concludes with the exact same comforting phrase:  
  *"ಚಿಂತಿಸಬೇಡಿ, ಈ ವಿವರಗಳನ್ನು ಮತ್ತು ಕೆಳಗಿನ ೩ ಪ್ರಶ್ನೆಗಳನ್ನು ನಿಮ್ಮ ಮುಂದಿನ ಭೇಟಿಯ ವೇಳೆ ವೈದ್ಯರಿಗೆ ತೋರಿಸಿ."*  
  (*"Do not worry, show these details and the 3 questions below to your doctor at your next visit."*)

---

## 4. Engineering for Low-Cost Android & Vernacular Script Constraints

| Constraint Domain | Real-World Hardware Reality | ReportSaathi Architectural Solution |
| :--- | :--- | :--- |
| **Low-End Memory & CPU** | Budget Android devices have 2 GB RAM and Unisoc/Helio processors that stutter on heavy web frameworks. | • Zero heavy JavaScript frameworks; static server-rendered HTML/CSS.<br>• DOM tree kept under 120 elements.<br>• Zero complex canvas or WebGL animations. |
| **Harsh Sunlight Readability** | Budget TN/LCD phone screens have low nits (<400 nits) and wash out under Indian outdoor sun. | • Pure high-contrast backgrounds (`#FFFFFF` and `#F8FAFC`).<br>• Text rendered in pure `#0F172A` (deepest slate black).<br>• Avoids low-contrast grays for body copy. |
| **Kannada Conjunct Stacking** | Kannada vowels and stacked subjoined consonants (*vattugalu*) get clipped by standard CSS line heights. | • Global CSS rule: `line-height: 1.68 !important;`<br>• Native system fonts: `Noto Sans Kannada` / `Nirmala UI`.<br>• Generous vertical card padding (minimum 14px top and bottom). |
| **Slow 2G/3G Connectivity** | Reports are uploaded from Tier-2/Tier-3 clinic corridors with erratic cellular reception. | • Initial HTML/CSS payload < 45 KB.<br>• Audio clips compressed using high-efficiency Opus/AAC codec (~60 KB for 60 seconds).<br>• Resilient automatic retry on dropped uploads. |
| **Neuropathy & Motor Tremors** | Aging diabetic patients struggle to tap small buttons or execute precision gestures. | • All hit targets oversized to ≥ 56px height.<br>• Zero swipe/pinch gestures.<br>• Audio auto-plays or activates with a massive 70px circular button. |
