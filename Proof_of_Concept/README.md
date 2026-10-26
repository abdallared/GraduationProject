# Ally Vision — Official Proof of Concept & Prototype Dossier

> **Project:** Ally Vision (Next-Generation Visual-to-Tactile Spatial Navigation System)  
> **Institution:** Egyptian-Chinese University (ECU) — Faculty of Engineering & Technology  
> **Academic Supervisor:** Dr. Islam Mohamed  
> **Engineering Team:** 11 Engineers (AI, Embedded Systems, Mechatronics, Software)  
> **Contact / Lead:** Abdallah Reda (`abdreda4444@gmail.com` // `+20 101 957 1158`)  
> **Repository:** [https://github.com/abdallared/GraduationProject](https://github.com/abdallared/GraduationProject)  
> **Status:** Working Prototype & Simulation Validated (Hardware-in-the-Loop)

---

## 1. Executive Prototype Overview

**Ally Vision** is an ear-free, hands-free wearable spatial navigation system for the blind and visually impaired. It replaces traditional surface vibrations with **dynamic physical pin displacement (height profiles 0 to 5)** against the user's forehead, guided by an Edge AI depth camera.

![All-in-One Wearable Visor Prototype](./images/1_all_in_one_visor_prototype.jpg)

### Key Validated Metrics
* **End-to-End Latency:** `< 92 ms` (Camera capture to micro-pin mechanical actuation).
* **AI Inference Speed:** `16.4 ms` per frame on Edge Host using YOLOv8n ONNX FP16.
* **Collision Avoidance Rate:** `> 91.5%` across simulated indoor/outdoor obstacle courses.
* **Safe Walking Corridor:** `80 cm` wide clearance envelope with dynamic steering guidance ($\theta$).
* **Tactile Resolution:** $5 \times 5$ Matrix (25 independent linear displacement nodes).
* **Target Retail Price:** `< $400` (<20% of European competitor costs such as 7Sense at $4,000+).

---

## 2. Hardware Architecture & Actuation Prototype

### 2.1 The $5 \times 5$ Mechanical Tactile Pin Matrix
Unlike existing vibrotactile devices that cause sensory adaptation and skin numbness within minutes, Ally Vision modulates **true mechanical pin height** directly against the forehead.

![Tactile Pin Matrix Actuation Prototype](./images/2_tactile_pin_matrix_actuation.png)

* **Actuator Technology:** Miniature Precision Linear Steppers / Voice Coil Actuators.
* **Stroke Height Range:** 0.0 mm (Flush = Safe Free Space) up to 5.0 mm (Maximum hazard displacement).
* **Response Time:** `< 18 ms` per pin displacement step.
* **Controller:** Arduino Uno R4 running a non-blocking hardware timer step generator with PySerial USB link at 115,200 baud.

### 2.2 Wearable Ergonomic Visor Housing
* **Chassis Design:** Custom 3D printed ultra-lightweight enclosure with counterbalanced rear battery pack.
* **Sensory Modality:** 100% Ear-Free (Zero bone-conduction or acoustic headphones) and 100% Hands-Free.

![Side View of Device Ergonomics](./images/6_device_side_view.png)

---

## 3. Computer Vision & Edge AI Pipeline

### 3.1 Real-Time 3D Metric Coordinate Transformation
For each obstacle detected in the RGB stream, a synchronized depth ROI extraction calculates metric camera-space coordinates $(X, Y, Z)$ using intrinsic camera pinhole geometry:

$$\bar{Z} = \text{Median}(Depth[v, u]), \quad X = \frac{(u_{mid} - c_x) \cdot \bar{Z}}{f_x}, \quad Y = \frac{(v_{mid} - c_y) \cdot \bar{Z}}{f_y}$$

![YOLO 3D Object Localization and Depth Fusion](./images/3_yolo_3d_depth_fusion.jpg)

### 3.2 Safe Walking Corridor & RANSAC Ground Clearance
1. **RANSAC 3D Plane Extraction:** Fits $ax + by + cz + d = 0$ on the floor surface with a 3cm inlier tolerance.
2. **Walkable Envelope:** Establishes an 80 cm clearance envelope along the forward vector.
3. **Sector Scan & Steering:** Scans Left $(-30^\circ)$, Center $(0^\circ)$, and Right $(+30^\circ)$ sectors to provide steering cues (`STEER_LEFT`, `CLEAR_STRAIGHT`, `STEER_RIGHT`).

![Safe Path Planning and Ground Extraction](./images/4_ransac_safe_corridor_planning.jpg)

### 3.3 Navigation-Critical Dataset
Trained on 2,000 real-world navigation images (annotated via Roboflow in 8 navigation classes: `person`, `chair`, `table`, `door`, `stairs`, `vehicle`, `pole`, `generic_obstacle`).

![Dataset Pipeline and Training Strategy](./images/5_dataset_pipeline.jpg)

---

## 4. Software & Simulation Proof of Concept

Before physical fabrication of 25 micro-steppers, the complete system was verified through our **Interactive Real-Time 2D/3D Haptic Simulator** (`tactile/virtual_simulator.py`):

```text
                        TACTILE MATRIX ENCODING (5 x 5)
                            Columns (Lateral Space: -1.5m to +1.5m)
                      Col 1      Col 2      Col 3      Col 4      Col 5
                     (Left)               (Center)               (Right)
                  ┌─────────────────────────────────────────────────────┐
   Row 1 (Far 4m) │    0          0          0          0          0    │
   Row 2 (3m)     │    3          1          0          0          0    │  <- Left Hazard
   Row 3 (2m)     │    4          2          0          2          4    │  <- Clear Corridor
   Row 4 (1.2m)   │    5          3          0          0          0    │
   Row 5 (Close)  │    0          0          0          0          0    │  <- Body Clearance
                  └─────────────────────────────────────────────────────┘
                                             ▲
                                  [WALKABLE CORRIDOR: COL 3]
                                    (Level 0 = Safe Path)
```

---

## 5. Summary of System Assets & Verification

| Asset | Verification Status | Source Link |
|---|---|---|
| **Live Web Platform** | Fully Developed (React + Vite) | [`website/`](../website) |
| **Edge AI Engine & ONNX Models** | Sub-20ms Inference Validated | [`AI/Ally_Vision_Documentation.md`](../AI/Ally_Vision_Documentation.md) |
| **System Proposal & Architecture** | Academic Board Approved | [`Proposal (1).pdf`](../Proposal%20(1).pdf) |
| **Pitch Deck (2026 Edition)** | 12 Minimalist Slides | [`Business Model/ally_vision_pitch_deck.md`](../Business%20Model/ally_vision_pitch_deck.md) |
| **Startup Lean Canvas** | Validated Unit Economics | [`Business Model/ally_vision_lean_canvas.md`](../Business%20Model/ally_vision_lean_canvas.md) |
| **Micro-Actuator Control Code** | Serial JSON Protocol Ready | [`arduino/`](../AI) |

---

*Ally Vision — Empowering Visual Independence through Tactile Depth Perception.*  
*Egyptian-Chinese University (ECU) // 2026*
