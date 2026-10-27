# Ally Vision — Comprehensive Project State & Session Memory
> **Memory Snapshot Date:** 2026-10-27  
> **Repository:** `d:\ECU\GraduationProject`  
> **Git Remote:** `https://github.com/abdallared/GraduationProject.git` (Branch: `main`)  
> **Purpose:** Persistent restoration of full context, architectural decisions, and deliverables across agent sessions.

---

## 1. Project Overview & Core Mission

* **Project Title:** **Ally Vision** — Assistive Visual-to-Tactile Spatial Navigation System.
* **Domain:** Assistive Technology, Computer Vision, Edge AI, Sensory Substitution (SSD), Cutaneous Haptics.
* **Core Problem:** Visually impaired individuals face high collision risks, drop-off hazards (stairs, curbs), and spatial disorientation. Existing aids either occupy hands (white canes) or block hearing (audio headphones), sacrificing natural acoustic situational awareness.
* **Solution Architecture:**
  1. **Spatial Perception (Input):** RGB-D depth sensing (Intel RealSense / OAK-D) + lightweight Edge AI (YOLO) for obstacle & ground plane segmentation (RANSAC).
  2. **Encoding Engine (Processing):** Dynamic safe corridor envelope extraction, hazard prioritization, depth-to-intensity mapping.
  3. **Tactile Display (Output):** Cutaneous haptic matrix (micro-stepper pins / ERM-LRA vibration motors) placed on the torso/abdomen/wrist, providing ear-free directional guidance.
* **11-Member Graduation Team:** David, Salma, Taha, Abdallah, Habiba, Hend, Mostafa, Farah, Fathy, Ahmed, Mohsen.

---

## 2. Key Deliverables & Achievements (October 27, 2026)

### A. Master Systematic Literature Review (SLR) & Workbook Alignment
* **Files:**
  * [`AllyVision.xlsx`](file:///d:/ECU/GraduationProject/AllyVision.xlsx) / [`AllyVision_Updated.xlsx`](file:///d:/ECU/GraduationProject/AllyVision_Updated.xlsx)
  * Backup: [`AllyVision_Backup.xlsx`](file:///d:/ECU/GraduationProject/AllyVision_Backup.xlsx)
* **Row-by-Row 1-to-1 Sequence Structure (Rows 2 to 136 in `Main `):**
  * `Row 002 - 013`: **David** (12 papers)
  * `Row 014 - 025`: **Salma** (12 papers)
  * `Row 026 - 037`: **Taha** (12 papers)
  * `Row 038 - 049`: **Abdallah** (12 papers)
  * `Row 050 - 061`: **Habiba** (12 papers)
  * `Row 062 - 073`: **Hend** (12 papers, including 4 template slots)
  * `Row 074 - 085`: **Mostafa** (12 papers)
  * `Row 086 - 097`: **Farah** (12 papers, including 8 template slots)
  * `Row 098 - 109`: **Fathy** (12 papers, including 8 Nature Scientific Reports papers)
  * `Row 110 - 121`: **Ahmed** (12 papers)
  * `Row 122 - 136`: **Mohsen** (15 papers, including 6 template slots)
* **Preservation Strategy:** Empty template slots are explicitly retained as `[Reserved Template Slot / Excluded]` so that row indices never shift across sheets.
* **Columns in `Main `:** Member, DOI, Title, Year, Publisher, URL, Technology, Status (Included/Excluded), Reason, Problem, Solution, Main Tags, Another Tags, Reviewer Notes, Systematic Scope Status, Reference ID.

---

### B. Standardized Taxonomy & Tagging Framework

#### 1. The 4 Main Tags (Primary Synthesis Themes — 1 per paper):
1. **`Tactile & Sensory Substitution Systems (TSSS)`** (74 papers):
   Cutaneous tactile displays, actuator matrices, vibrotactile/electrotactile feedback, sensory substitution devices (SSDs).
2. **`Edge Computer Vision & 3D Spatial Perception (CV-3D)`** (26 papers):
   RGB-D cameras, point clouds, real-time depth estimation, and embedded AI object detection (YOLO).
3. **`Ground Segmentation & Safe Path Navigation (GS-PN)`** (9 papers):
   Ground plane extraction, stairs/curbs detection, safe corridor envelope, collision avoidance trajectory planning.
4. **`Cognitive Ergonomics & Blind Usability (CE-BU)`** (7 papers):
   Cognitive workload (NASA-TLX), orientation & mobility (O&M) trials, user testing with blind participants, ear-free preservation.

#### 2. The 6 Another Tags (Controlled Technical Topics — Multi-label):
1. **`Human-Factors-Usability`** (99 papers): User studies, usability evaluation, cognitive load, accessibility.
2. **`Tactile-Actuation`** (88 papers): Physical actuator types, vibration motors, pin arrays, tactile resolution.
3. **`Corridor-Navigation`** (64 papers): Hallway tracking, safe path planning, steering cues.
4. **`Wearable-Embedded`** (58 papers): Body-worn integration, form factor (head/vest/wrist), Raspberry Pi, ESP32, Jetson, battery budget.
5. **`AI-Object-Detection`** (50 papers): Deep learning models, YOLO, lightweight CNNs, real-time inference.
6. **`Depth-Sensing`** (50 papers): Stereo IR, ToF, LiDAR, ultrasonic range sensing.

---

### C. Master Paper Reviews Markdown Tracker
* **File:** [`AllyVision_Papers_Review_and_Taxonomy_Tracker.md`](file:///d:/ECU/GraduationProject/AllyVision_Papers_Review_and_Taxonomy_Tracker.md)
* **Structure:**
  * Interactive Table of Contents linking to each member's section.
  * Summary matrix per member: Row number, paper title, inclusion badge, Main Tag, Another Tags.
  * Detailed paper cards: Clickable DOI, Publication Year, Publisher, Technology, Status & Reason, Research Problem, Proposed Solution.
  * 100% synchronized with the row numbers in `AllyVision.xlsx`.

---

### D. Proof of Concept (PoC) & Interactive Showcase
* **Files:**
  * [`Proof_of_Concept/README.md`](file:///d:/ECU/GraduationProject/Proof_of_Concept/README.md)
  * [`Proof_of_Concept/index.html`](file:///d:/ECU/GraduationProject/Proof_of_Concept/index.html)
* **Features:**
  * Live webcam integration with synthetic RGB-D depth colormap overlay.
  * Real-time $10 \times 10$ tactile pin matrix simulation.
  * Directional steering cues and hazard proximity audio alerts.
  * Pushed to GitHub `origin main`.

---

### E. Business Model Canvas (BMC)
* **Files:**
  * [`Business_Model_Canvas/README.md`](file:///d:/ECU/GraduationProject/Business_Model_Canvas/README.md)
  * [`Business_Model_Canvas/business model canvas.png`](file:///d:/ECU/GraduationProject/Business_Model_Canvas/business%20model%20canvas.png)
  * [`Business_Model_Canvas/BMC.pdf`](file:///d:/ECU/GraduationProject/Business_Model_Canvas/BMC.pdf)
* **Content:** All 9 Osterwalder blocks thoroughly documented (Customer Segments: B2C blind individuals, B2B rehabilitation centers & NGOs; Revenue: Hardware sales, subscription maintenance, NGO grants; Value Prop: Ear-free, hands-free 3D spatial awareness).

---

### F. Competitions Master Tracker & Pitch Deck
* **Files:**
  * [`compitiations/Ally_Vision_Competitions_Master_Tracker_Updated.xlsx`](file:///d:/ECU/GraduationProject/compitiations/Ally_Vision_Competitions_Master_Tracker_Updated.xlsx)
  * [`Business Model/ally_vision_pitch_deck_prompts_and_spec.md`](file:///d:/ECU/GraduationProject/Business%20Model/ally_vision_pitch_deck_prompts_and_spec.md)
* **Content:** 26 international & national startup competitions tracked. Submissions confirmed for DEDI Challenge and GENOVATE Hackathon.

---

## 3. Important Implementation Notes & Gotchas

1. **Excel File Lock (`PermissionError [Errno 13]`):**
   * When Microsoft Excel has `AllyVision.xlsx` open, Python scripts cannot overwrite it.
   * `compitiations/align_exact_excel_and_md.py` is configured with a fallback to save to `AllyVision_Updated.xlsx`.
   * **Action required:** When Excel is closed, copy `AllyVision_Updated.xlsx` over `AllyVision.xlsx` or re-run `python compitiations/align_exact_excel_and_md.py`.
2. **Template Slots Stability:**
   * Do NOT delete the blank rows (Hend rows 69-72, Farah rows 90-97, Mohsen rows 122-127) as they anchor the team's 12-row per member indexing convention.
3. **Re-generating Markdown & Excel:**
   * Script to execute full alignment: `python compitiations/align_exact_excel_and_md.py`.

---

## 4. Key File Map

| Path | Purpose |
| :--- | :--- |
| [`AllyVision.xlsx`](file:///d:/ECU/GraduationProject/AllyVision.xlsx) | Master Excel database with team member sequence (Row 2–136). |
| [`AllyVision_Updated.xlsx`](file:///d:/ECU/GraduationProject/AllyVision_Updated.xlsx) | Latest updated Excel copy including the 6th tag (`Wearable-Embedded`). |
| [`AllyVision_Backup.xlsx`](file:///d:/ECU/GraduationProject/AllyVision_Backup.xlsx) | Untouched original backup of the workbook before script operations. |
| [`AllyVision_Papers_Review_and_Taxonomy_Tracker.md`](file:///d:/ECU/GraduationProject/AllyVision_Papers_Review_and_Taxonomy_Tracker.md) | Exhaustive Markdown documentation of all 135 papers/slots. |
| [`Proof_of_Concept/index.html`](file:///d:/ECU/GraduationProject/Proof_of_Concept/index.html) | Interactive web-based simulation and prototype demonstration. |
| [`Business_Model_Canvas/README.md`](file:///d:/ECU/GraduationProject/Business_Model_Canvas/README.md) | Complete Business Model Canvas documentation. |
| [`compitiations/align_exact_excel_and_md.py`](file:///d:/ECU/GraduationProject/compitiations/align_exact_excel_and_md.py) | Master synchronization script between Excel and Markdown. |
| [`SESSION_MEMORY.md`](file:///d:/ECU/GraduationProject/SESSION_MEMORY.md) | Local repository snapshot of session state. |
