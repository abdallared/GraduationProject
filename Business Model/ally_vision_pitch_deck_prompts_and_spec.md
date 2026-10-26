# Ally Vision — Complete Executive Pitch Deck Specification & Prompt Bible (2026 Edition)

> **Design Style:** Executive Minimal (Uber / Slidebean Minimalist Redesign)  
> **Aesthetic Language:** Swiss International Typographic Style, Pure White Canvas, Hairline Borders, Monochrome Vector Line Icons  
> **Presentation Year:** **2026** (All copyrights, projections, and roadmap milestones calibrated to 2026–2027)

---

## 1. Master Design System & Style Guide

### 🎨 Color Palette & Design Tokens

| Token Name | Hex Code | Role & Usage |
| :--- | :--- | :--- |
| **Canvas / Background** | `#FFFFFF` | Pure absolute white background. Zero gray tint, zero gradients. |
| **Primary Text / Headings** | `#000000` | Jet black for headlines, metrics, titles, and active icons. High contrast ratio (21:1). |
| **Secondary / Subtitles** | `#64748B` | Slate gray for subtitles, body descriptions, and secondary metadata. |
| **Ghost Border / Dividers** | `#E2E8F0` | Subtle 1px solid hairline borders defining structural cards and divider rules. |
| **Tracking / Label Accent** | `#71717A` | Neutral zinc for uppercase category tags (`tracking-widest`, 10px–12px). |
| **Surface Alt (Optional)** | `#F8FAFC` | Light slate tint used only for subtle container backgrounds or card hovers. |

### 🔤 Typography & Hierarchy
- **Font Family:** `Inter`, `-apple-system`, `Helvetica Neue`, sans-serif.
- **Tracking Label:** `11px`, Uppercase, `letter-spacing: 0.15em`, Semibold (`600`). Format: `EXECUTIVE PITCH DECK // 01`
- **Slide Title (H1):** `36px – 44px`, Bold (`700`), `letter-spacing: -0.02em`, `#000000`.
- **Slide Subtitle:** `15px – 17px`, Regular (`400`), Line height `1.5`, `#64748B`.
- **Card Title (H3):** `13px – 15px`, Semibold (`600`), `#000000`.
- **Card Body / Bullets:** `11px – 13px`, Regular (`400`), Line height `1.45`, `#475569`.
- **Giant Data Metric:** `40px – 56px`, Bold (`700`), `letter-spacing: -0.03em`, `#000000`.
- **Card Category Tag:** `10px – 11px`, Uppercase, `letter-spacing: 0.1em`, Medium (`500`), `#64748B`.

### 📐 Card Architecture & Icon Rules
- **Aspect Ratio:** `16:9` widescreen presentation format (1920×1080 or 2560×1440 canvas).
- **Cards:** Flat cards with `1px solid #E2E8F0`, `border-radius: 0px` (or ultra-subtle `2px`), clean internal padding (`p-5` to `p-6`).
- **Iconography Rule:**
  - **STRICTLY Monochrome Black SVG Line Art** (Lucide / Feather icon style).
  - Attributes: `fill="none"`, `stroke="#000000"`, `stroke-width="1.75px"`, `stroke-linecap="round"`, `stroke-linejoin="round"`, size `20x20px` to `24x24px`.
  - **Zero colors, zero filled silhouettes, zero 3D clipart, zero emoji.**

### 🏷️ Standard Header & Footer Template
- **Header:**
  - Tracking Label: `EXECUTIVE PITCH DECK // [SLIDE_NUMBER]`
  - Main Title: `[Slide Action Title]`
  - Subtitle: `[One-sentence executive summary]`
- **Footer:**
  - Left: `Ally Vision`
  - Center: `© 2026 Executive Presentation. All rights reserved.`
  - Right: `Slide [XX] // 10`

---

## 2. Slide-by-Slide Detailed Prompts & Content (1 to 10)

```
================================================================================
SLIDE 01: COVER & HERO
================================================================================
Tracking: EXECUTIVE PITCH DECK // 01
Title: Ally Vision
Subtitle: Visual-to-Tactile Spatial Navigation for the Blind

Layout:
3 equal feature cards side-by-side with 1px hairline slate borders (#E2E8F0):

Card 1:
- Icon: <svg> Person / Accessibility line icon
- Title: Hands-Free
- Body: Unrestricted physical movement enabled by wearable spatial mapping arrays.
- Sub-Tag: CORE ARCHITECTURE

Card 2:
- Icon: <svg> Ear-Off / Volume-X line icon
- Title: Ear-Free
- Body: Preserves full auditory situational awareness without audio prompts or headphones.
- Sub-Tag: COGNITIVE SAFETY

Card 3:
- Icon: <svg> Zap / Lightning line icon
- Title: <100ms Latency
- Body: Real-time on-device edge processing translating visual obstacles into instant haptic feedback.
- Sub-Tag: PERFORMANCE BENCHMARK

Footer:
Ally Vision | © 2026 Executive Presentation. All rights reserved. | Slide 01 // 10
```

```
================================================================================
SLIDE 02: THE PROBLEM
================================================================================
Tracking: EXECUTIVE PITCH DECK // 02
Title: The Problem: Spatial Isolation & Tool Failure
Subtitle: 285 million visually impaired individuals face severe sensory barriers with existing tools.

Layout:
3 column analytical breakdown cards (01, 02, 03):

Card 1:
- Icon: <svg> Alert-Triangle line icon
- Big Number: 01
- Title: White Canes Miss Head-Level Hazards
- Details:
  * Only sweeps ground level within a 1-meter radius.
  * Completely blind to hanging tree branches, scaffolding, street signs, and open windows.
  * 64% of blind travelers report regular head and chest collisions.
- Sub-Tag: GROUND RESTRICTION

Card 2:
- Icon: <svg> Ear-Off line icon
- Big Number: 02
- Title: Talking Audio Aids Block Vital Hearing
- Details:
  * Audio headsets and talking screen readers mask ambient urban soundscapes.
  * Prevents users from hearing vehicle engines, pedestrian flow, and crosswalk signals.
  * Causes severe cognitive auditory fatigue during daily commutes.
- Sub-Tag: SENSORY OCCLUSION

Card 3:
- Icon: <svg> Dollar-Sign line icon
- Big Number: 03
- Title: Western Assistive Tech is Prohibitively Expensive
- Details:
  * European devices like 7Sense SuperBrain cost $12,000+; BrainPort costs $10,000+.
  * 89% of the world's visually impaired live in developing regions with zero subsidy.
  * Guide dogs exceed $40,000 with a 2-year waiting list.
- Sub-Tag: COST BARRIER

Footer:
Ally Vision | © 2026 Executive Presentation. All rights reserved. | Slide 02 // 10
```

```
================================================================================
SLIDE 03: THE SOLUTION
================================================================================
Tracking: EXECUTIVE PITCH DECK // 03
Title: The Solution: Spatial Sight Through Touch
Subtitle: An autonomous sensory substitution wearable translating 3D depth into silent tactile intuition.

Layout:
3 sequential solution pillar cards:

Card 1:
- Icon: <svg> Eye / Camera line icon
- Title: 3D Depth Perception
- Details:
  * Dual wide-angle stereo depth sensors capturing a 120° spatial field of view.
  * Simultaneous ground depression (stairs/holes) and overhead hazard tracking.
  * Low-light active IR illumination enables 24/7 day and night navigation.
- Sub-Tag: SENSORY ACQUISITION

Card 2:
- Icon: <svg> Cpu line icon
- Title: Real-Time Edge Intelligence
- Details:
  * On-device embedded neural inference engine operating at 30 FPS.
  * Sub-100ms latency converts raw depth point clouds into obstacle danger vectors.
  * 100% offline edge processing guarantees total privacy and zero cellular lag.
- Sub-Tag: EDGE PROCESSING

Card 3:
- Icon: <svg> Grid / Radio line icon
- Title: 5×5 Abdominal Haptic Matrix
- Details:
  * 25 micro-vibration actuators positioned in a flexible ergonomic belt.
  * Frequency denotes proximity; pin location maps obstacle azimuth.
  * Silent, intuitive spatial awareness without occupying the user's ears or hands.
- Sub-Tag: TACTILE CONVERSION

Footer:
Ally Vision | © 2026 Executive Presentation. All rights reserved. | Slide 03 // 10
```

```
================================================================================
SLIDE 04: LEAN CANVAS (BUSINESS ARCHITECTURE)
================================================================================
Tracking: EXECUTIVE PITCH DECK // 04
Title: Lean Canvas: Business Architecture
Subtitle: Validated B2B2C economic engine and distribution model for visual-to-tactile assistive tech.

Layout:
Classic 9-Box Lean Canvas grid layout with 1px slate borders (#E2E8F0) and monochrome line icons:

Box 1 (Problem):
- Icon: <svg> Alert-Triangle line icon
- Bullets: Severe spatial isolation (285M) • Audio fatigue masks road traffic • Traditional canes miss overhead obstacles.
- Existing Alternatives: White cane ($30), Guide dog ($40k+), 7Sense SuperBrain ($12,000+).

Box 2 (Solution):
- Icon: <svg> Cpu line icon
- Bullets: Dual stereo vision depth sensing • Edge AI obstacle detection (<100ms) • 5×5 abdominal vibrotactile haptic matrix.

Box 3 (Value Proposition):
- Icon: <svg> Sparkles line icon
- Primary: 'Spatial Sight Through Touch' — Real-time 3D spatial awareness translated into silent tactile feedback.
- High-Level Concept: Autonomous Spatial Awareness for the Blind — Ear-Free, Hands-Free.

Box 4 (Unfair Advantage):
- Icon: <svg> Shield-Check line icon
- Bullets: Ear-Free patent-pending spatial haptic mapping • 95%+ lower cost than European 7Sense ($299 vs $12,000) • Proprietary sub-100ms tactile encoding.

Box 5 (Customer Segments):
- Icon: <svg> Users line icon
- Bullets: Primary: Blind individuals (40M worldwide) • Institutional: Rehabilitation NGOs, Special Education institutions, Ministry of Social Solidarity • Early Adopters: Tech-literate blind students & professionals.

Box 6 (Key Metrics):
- Icon: <svg> Trending-Up line icon
- Bullets: Obstacle Avoidance Success Rate (>95%) • Navigation Speed (+40% faster) • End-to-End Latency (<100ms) • Active Monthly Usage.

Box 7 (Channels):
- Icon: <svg> Share-2 line icon
- Bullets: B2B partnerships with blindness NGOs (Al Nour Wal Amal, Resala, Baseera) • Direct assistive tech e-commerce • Government disability subsidy & medical device inclusion programs.

Box 8 (Cost Structure):
- Icon: <svg> Layers line icon
- Bullets: BOM: ERM/LRA actuators, edge MCU/SoC, stereo camera (~$85 at volume) • Local fabrication & assembly • Edge AI optimization R&D.

Box 9 (Revenue Streams):
- Icon: <svg> Dollar-Sign line icon
- Bullets: Core Hardware Kit ($299 target retail, subsidized via NGOs) • Ally Cloud SaaS navigation updates ($9.99/mo) • Institutional B2B maintenance contracts.

Footer:
Ally Vision | © 2026 Executive Presentation. All rights reserved. | Slide 04 // 10
```

```
================================================================================
SLIDE 05: MARKET OPPORTUNITY (TAM / SAM / SOM)
================================================================================
Tracking: EXECUTIVE PITCH DECK // 05
Title: Market Opportunity: Global Assistive TAM
Subtitle: Addressing a $31.4B global assistive transition toward autonomous, ear-free spatial sensory systems.

Layout:
3 prominent structural metric cards, plus a bottom strategic catalyst card:

Card 1 (TAM):
- Icon: <svg> Globe line icon
- Metric: $31.4B
- Title: Total Addressable Market (TAM)
- Body: Global assistive technology & mobility devices market projected by 2030, growing at an 8.4% CAGR.
- Tag: MACRO INDUSTRY SIZE

Card 2 (SAM):
- Icon: <svg> Users line icon
- Metric: 40M
- Title: Serviceable Addressable Market (SAM)
- Body: Totally blind individuals worldwide actively requiring independent daily indoor and outdoor navigation.
- Tag: TARGET USER BASE

Card 3 (SOM):
- Icon: <svg> Target line icon
- Metric: 1.5M
- Title: Serviceable Obtainable Market (SOM)
- Body: 5-year initial market in MENA & Southern Europe accessible through partnered blindness NGOs and disability funds.
- Tag: 5-YEAR BEACHHEAD

Bottom Strategic Card:
- Icon: <svg> Trending-Up line icon
- Body: Market Inflection Point: 78% of visually impaired users reject talking navigation aids due to cognitive fatigue and urban traffic danger. Ally Vision captures the silent tactile transition.
- Tag: STRATEGIC CATALYST

Footer:
Ally Vision | © 2026 Executive Presentation. All rights reserved. | Slide 05 // 10
```

```
================================================================================
SLIDE 06: BUSINESS MODEL & MONETIZATION
================================================================================
Tracking: EXECUTIVE PITCH DECK // 06
Title: Business Model: B2B2C Commercial Engine
Subtitle: Dual-track monetization combining subsidized hardware distribution with high-margin recurring SaaS.

Layout:
3 structural revenue cards, plus a bottom unit economics banner card:

Card 1 (Hardware Distribution):
- Icon: <svg> Credit-Card line icon
- Metric: $299
- Title: Subsidized Hardware Kit
- Body: Vision sensor unit + 5x5 haptic matrix belt sold via partnered blindness NGOs, medical device subsidies, and direct web portal.
- Sub-Metric: COGS: ~$85 at scale | 71% Gross Margin
- Tag: HARDWARE DISTRIBUTION

Card 2 (Recurring SaaS):
- Icon: <svg> Cloud line icon
- Metric: $9.99 / mo
- Title: Ally Cloud Spatial Navigation
- Body: Cloud-synced high-precision indoor venue maps, over-the-air AI obstacle detection updates, and transit beacon integration.
- Sub-Metric: 85%+ Software Gross Margin
- Tag: RECURRING REVENUE

Card 3 (Enterprise & Institutional):
- Icon: <svg> Building-2 line icon
- Metric: $5k – $25k / yr
- Title: Institutional Deployments
- Body: Dedicated spatial mapping contracts for universities, transit authorities, and specialized rehabilitation institutes.
- Sub-Metric: Multi-year service contracts
- Tag: ENTERPRISE & PUBLIC SECTOR

Bottom Banner Card:
- Icon: <svg> Trending-Up line icon
- Body: Target Unit Economics at 5,000 Units: LTV: $890 | Blended CAC: $42 (via NGO distribution partners) | LTV/CAC Ratio: 21.1x
- Tag: SCALABILITY BENCHMARK

Footer:
Ally Vision | © 2026 Executive Presentation. All rights reserved. | Slide 06 // 10
```

```
================================================================================
SLIDE 07: COMPETITIVE MATRIX & UNFAIR ADVANTAGE
================================================================================
Tracking: EXECUTIVE PITCH DECK // 07
Title: Competitive Matrix: 10x Price & Safety Moat
Subtitle: Disrupting prohibitive $12,000 European hardware with an accessible, ear-free wearable architecture.

Layout:
4-column comparative breakdown cards, plus a bottom defensibility card:

Column 1:
- Price: $30
- Title: White Cane
- Weakness: Ground only. Zero head-level hazard alerts. Blocks hands.
- Latency: Physical contact only
- Rating: Low Safety, Low Tech

Column 2:
- Price: $40,000+
- Title: Guide Dog
- Weakness: 2-3 yr waitlist. Heavy upkeep ($3k/yr). Not scalable.
- Latency: Animal reflex
- Rating: High Cost, Inaccessible

Column 3:
- Price: $12,000+
- Title: 7Sense (Estonia)
- Weakness: Extreme cost barrier. Bulky chest rig. Restricted to EU grant recipients.
- Latency: ~150ms
- Rating: Elite Direct Competitor

Column 4 (Ally Vision - Highlighted):
- Price: $299
- Title: Ally Vision
- Advantage: Ear-Free safety. 5x5 abdominal matrix. Edge AI. 95%+ cheaper.
- Latency: <100ms real-time
- Rating: Global Scalable Standard

Bottom Defensibility Card:
- Icon: <svg> Shield-Check line icon
- Title: Core Defensibility & Moat:
  1. Proprietary Spatial-to-Tactile Encoding Algorithms (<10ms point cloud conversion).
  2. Zero-Auditory Occlusion (critical safety in road traffic).
  3. Ultra-Low BOM Economics (~$85 target at volume vs $3,000+ EU assembly).
- Tag: COMPETITIVE MOAT

Footer:
Ally Vision | © 2026 Executive Presentation. All rights reserved. | Slide 07 // 10
```

```
================================================================================
SLIDE 08: TECHNOLOGY PIPELINE & EDGE ARCHITECTURE
================================================================================
Tracking: EXECUTIVE PITCH DECK // 08
Title: Technology Architecture: Edge Perception to Touch
Subtitle: End-to-end real-time visual-to-tactile transformation pipeline operating strictly on-device under 100ms.

Layout:
3 sequential pipeline cards, plus a bottom technical benchmarks bar:

Card 1 (Perception Layer):
- Icon: <svg> Eye line icon
- Title: 01 // Spatial Perception
- Details: Dual wide-angle stereo depth sensors with 120° FOV and IR night illumination. Captures both ground pitfalls and head-level overhangs.
- Tag: STEREO VISION SENSING

Card 2 (Inference Layer):
- Icon: <svg> Cpu line icon
- Title: 02 // Edge Neural Inference
- Details: On-device embedded neural network calculates obstacle proximity, motion vectors, and hazard classification in under 15ms without cloud connectivity.
- Tag: ZERO-LATENCY EDGE AI

Card 3 (Tactile Layer):
- Icon: <svg> Layers / Grid line icon
- Title: 03 // 5×5 Tactile Matrix
- Details: 25 ERM/LRA haptic motors across abdominal belt convey obstacle azimuth (position) and distance (frequency) silently through human skin.
- Tag: SENSORY SUBSTITUTION

Bottom Technical Benchmarks Bar:
- 4 Metrics in a row:
  * Benchmark 1: <100ms (End-to-End Latency)
  * Benchmark 2: 8+ Hours (All-Day Battery)
  * Benchmark 3: <320g (Discreet Wearable)
  * Benchmark 4: 100% Offline (Local Privacy)
- Tag: TECHNICAL BENCHMARKS

Footer:
Ally Vision | © 2026 Executive Presentation. All rights reserved. | Slide 08 // 10
```

```
================================================================================
SLIDE 09: EXECUTION ROADMAP & MILESTONES (2026–2027)
================================================================================
Tracking: EXECUTIVE PITCH DECK // 09
Title: Execution Roadmap: Path to Commercial Scale
Subtitle: Disciplined 18-month execution from validated hardware prototype to regional market leadership.

Layout:
4 sequential milestone cards in a timeline row, plus a bottom executive targets banner:

Card 1 (Phase 1):
- Icon: <svg> Check-Circle line icon
- Timeline: Q1-Q2 2026
- Title: Phase 01: Prototype Validation
- Details: Benchtop system integration, <100ms latency verification, and 5x5 haptic perceptual acuity mapping in lab trials.
- Tag: LAB VERIFICATION

Card 2 (Phase 2):
- Icon: <svg> Users line icon
- Timeline: Q3-Q4 2026
- Title: Phase 02: NGO Clinical Pilots
- Details: Structured 50-participant user testing with Egyptian blindness associations (Al Nour Wal Amal, Resala). Feedback loop on belt ergonomics.
- Tag: USER VALIDATION

Card 3 (Phase 3):
- Icon: <svg> Shield-Check line icon
- Timeline: Q1-Q2 2027
- Title: Phase 03: DFM & Compliance
- Details: Design for Manufacturing with local electronics assembly lines. Medical assistive CE / ISO 13485 compliance documentation.
- Tag: PRODUCTION TOOLING

Card 4 (Phase 4):
- Icon: <svg> Trending-Up / Rocket line icon
- Timeline: Q3+ 2027
- Title: Phase 04: Commercial Launch
- Details: Initial production batch of 1,000 subsidized units deployed across Egypt & GCC through NGO subsidy contracts and Ally Cloud launch.
- Tag: COMMERCIAL SCALE

Bottom Targets Banner:
- Icon: <svg> Target line icon
- Content: 18-Month Target Milestones: 1,000 Active Units Deployed | $350k Revenue Run-Rate | Institutional NGO Backing | Series Seed Preparedness.
- Tag: EXECUTIVE TARGETS

Footer:
Ally Vision | © 2026 Executive Presentation. All rights reserved. | Slide 09 // 10
```

```
================================================================================
SLIDE 10: THE ASK & CAPITAL ALLOCATION (2026)
================================================================================
Tracking: EXECUTIVE PITCH DECK // 10
Title: The Ask: $20,000 Seed Grant Allocation
Subtitle: Strategic capital deployment to complete clinical trials, secure IP, and prepare pilot commercialization.

Layout:
4-column row of allocation cards, plus a bottom runway banner card:

Card 1 (45% // $9,000):
- Icon: <svg> Cpu / Layers line icon
- Metric: 45% // $9,000
- Title: Hardware Tooling & Actuator Array
- Details: Custom flexible PCB fabrication for 5x5 matrix, micro-actuator procurement, and ergonomic wearable belt housing.
- Tag: PROTOTYPE TOOLING

Card 2 (30% // $6,000):
- Icon: <svg> Users line icon
- Metric: 30% // $6,000
- Title: NGO Clinical Pilots & Field Trials
- Details: Structured 50-subject mobility trials across Egyptian blindness associations, user stipends, and feedback synthesis.
- Tag: USER VALIDATION

Card 3 (15% // $3,000):
- Icon: <svg> Zap line icon
- Metric: 15% // $3,000
- Title: Edge AI Acceleration & Embedded Port
- Details: Model quantization on ultra-low-power NPU hardware, reducing latency from 100ms down to sub-60ms.
- Tag: ALGORITHM OPTIMIZATION

Card 4 (10% // $2,000):
- Icon: <svg> Shield-Check line icon
- Metric: 10% // $2,000
- Title: IP Protection & Regulatory Filing
- Details: Tactile sensory substitution patent filings and medical assistive device regulatory pre-certification.
- Tag: PATENTS & COMPLIANCE

Bottom Runway Banner Card:
- Icon: <svg> Flag line icon
- Content: 9-Month Runway: Unlocks 100 pilot units deployed with partner NGOs, validated clinical efficacy data, and prepares Ally Vision for Series Seed financing in 2027.
- Tag: STRATEGIC OUTCOME

Footer:
Ally Vision | © 2026 Executive Presentation. All rights reserved. | Slide 10 // 10
```

---

## 3. Master Copy-Paste Prompt for AI Tools (Gamma / Stitch / ChatGPT / Claude)

If you want to paste a single master prompt into an AI presentation generator, copy the block below:

```markdown
Create an ultra-minimalist, 10-slide executive pitch deck for "Ally Vision" (Visual-to-Tactile Spatial Navigation for the Blind) following the Swiss International Typographic style and the Uber Pitch Deck redesign template.

DESIGN SYSTEM SPECIFICATIONS:
- Canvas: Pure white background (#FFFFFF). Absolutely NO dark mode, NO gradients.
- Typography: Inter / Helvetica. High-contrast pure black (#000000) for headlines and metrics, slate gray (#64748B) for body and subtitles.
- Borders: Subtle 1px solid hairline borders (#E2E8F0) around all cards. Zero border radius (or 2px).
- Iconography: Strictly minimalist, monochrome black line SVG icons (stroke-width 1.75px, stroke="#000000", fill="none"). NO colors, NO cartoon clipart.
- Presentation Year: 2026. Footer on all slides: "Ally Vision | © 2026 Executive Presentation. All rights reserved. | Slide [XX] // 10".
- Header on all slides: Small uppercase tracking label "EXECUTIVE PITCH DECK // [XX]" followed by bold Title and 1-sentence Subtitle.

SLIDE DECK OUTLINE (10 SLIDES):
- Slide 01: Cover — "Ally Vision" with 3 cards: Hands-Free (Person icon), Ear-Free (Ear-Off icon), <100ms Latency (Zap icon).
- Slide 02: The Problem — "Spatial Isolation & Tool Failure" with 3 columns: 01 Canes Miss Overhead Hazards, 02 Audio Aids Block Hearing, 03 Western Devices Unaffordable ($12,000+).
- Slide 03: The Solution — "Spatial Sight Through Touch" with 3 pillars: 3D Depth Perception, Real-Time Edge AI, 5x5 Abdominal Tactile Matrix.
- Slide 04: Lean Canvas — 9-box business architecture: Problem, Solution, Value Proposition, Unfair Advantage, Customer Segments, Key Metrics, Channels, Cost Structure, Revenue Streams.
- Slide 05: Market Opportunity — 3 metric cards: TAM $31.4B (Global Assistive Tech), SAM 40M (Blind Population), SOM 1.5M (MENA/EU Beachhead), plus Strategic Catalyst banner.
- Slide 06: Business Model — 3 revenue cards: Hardware ($299, 71% margin), Ally Cloud SaaS ($9.99/mo, 85% margin), Enterprise Institutional ($5k-$25k/yr), plus Unit Economics banner (LTV/CAC 21.1x).
- Slide 07: Competitive Matrix — 4 comparative columns: White Cane ($30), Guide Dog ($40k+), 7Sense Estonia ($12,000+), Ally Vision ($299 Highlighted), plus 3-pillar Moat card.
- Slide 08: Technology Pipeline — 3 stages: 01 Perception (120° Stereo IR), 02 Edge AI (<15ms CNN), 03 Tactile (25 Haptic Motors), plus Specs Bar (<100ms, 8h battery, <320g, 100% offline).
- Slide 09: Execution Roadmap (2026–2027) — 4 timeline cards: Q1-Q2 2026 (Prototype Lab Validation), Q3-Q4 2026 (50-Subject NGO Pilots), Q1-Q2 2027 (DFM & Compliance), Q3+ 2027 (Commercial Launch 1,000 Units), plus 18-month targets.
- Slide 10: The Ask ($20,000 Seed Grant) — 4 allocation cards: 45% Tooling & Haptics ($9,000), 30% Clinical NGO Pilots ($6,000), 15% Edge AI Port ($3,000), 10% IP & Compliance ($2,000), plus 9-month runway banner.
```
