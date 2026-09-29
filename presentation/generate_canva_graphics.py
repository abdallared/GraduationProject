"""
Generates high-resolution presentation graphics for Canva slides
Color palette: Crisp White/Off-white/Light Gray background (#F8FAFC / #FFFFFF),
slate typography (#0F172A / #334155), subtle pale gold/yellow accent (#EAB308 / #CA8A04),
soft tech green (#16A34A / #22C55E), and subtle cyan (#0EA5E9).
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

out_dir = r"d:\ECU\GraduationProject\presentation\canva_assets"
os.makedirs(out_dir, exist_ok=True)

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#CBD5E1'
plt.rcParams['axes.linewidth'] = 1.2

# ─────────────────────────────────────────────────────────────────────────────
# 1. Slide 6: PRISMA Systematic Review Flowchart
# ─────────────────────────────────────────────────────────────────────────────
def generate_prisma():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=200)
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')
    ax.axis('off')

    # Title
    ax.text(0.5, 0.94, "PRISMA 2020 Systematic Literature Review Flow", ha='center', va='center',
            fontsize=22, fontweight='bold', color='#0F172A')
    ax.text(0.5, 0.90, "Systematic selection of 137 core papers across Scopus & Web of Science", ha='center', va='center',
            fontsize=13, color='#64748B')

    boxes = [
        {"x": 0.22, "y": 0.77, "w": 0.25, "h": 0.08, "title": "Scopus Database", "sub": "n = 1,759 records", "c": "#EFF6FF", "b": "#3B82F6"},
        {"x": 0.53, "y": 0.77, "w": 0.25, "h": 0.08, "title": "Web of Science", "sub": "n = 1,345 records", "c": "#EFF6FF", "b": "#3B82F6"},
        {"x": 0.375, "y": 0.63, "w": 0.25, "h": 0.08, "title": "Initial Aggregation", "sub": "n = 3,104 total records", "c": "#F1F5F9", "b": "#94A3B8"},
        {"x": 0.70, "y": 0.63, "w": 0.24, "h": 0.08, "title": "Duplicate Removal", "sub": "-874 duplicates removed", "c": "#FEF3C7", "b": "#F59E0B"},
        {"x": 0.375, "y": 0.49, "w": 0.25, "h": 0.08, "title": "Title & Abstract Screening", "sub": "n = 2,230 unique records", "c": "#F1F5F9", "b": "#94A3B8"},
        {"x": 0.70, "y": 0.49, "w": 0.24, "h": 0.08, "title": "Excluded at Screening", "sub": "-2,080 (No haptics / Off-topic)", "c": "#FEE2E2", "b": "#EF4444"},
        {"x": 0.375, "y": 0.35, "w": 0.25, "h": 0.08, "title": "Full-Text Eligibility", "sub": "n = 150 papers assessed", "c": "#FEF9C3", "b": "#EAB308"},
        {"x": 0.70, "y": 0.35, "w": 0.24, "h": 0.08, "title": "Full-Text Excluded", "sub": "-13 duplicate files / unreadable", "c": "#FEE2E2", "b": "#EF4444"},
        {"x": 0.375, "y": 0.19, "w": 0.25, "h": 0.09, "title": "Final Included Corpus", "sub": "n = 137 verified studies", "c": "#DCFCE7", "b": "#16A34A"},
    ]

    for b in boxes:
        rect = patches.FancyBboxPatch((b["x"], b["y"]), b["w"], b["h"],
                                      boxstyle="round,pad=0.015,rounding_size=0.015",
                                      facecolor=b["c"], edgecolor=b["b"], linewidth=2)
        ax.add_patch(rect)
        ax.text(b["x"] + b["w"]/2, b["y"] + b["h"]*0.62, b["title"], ha='center', va='center',
                fontsize=11.5, fontweight='bold', color='#0F172A')
        ax.text(b["x"] + b["w"]/2, b["y"] + b["h"]*0.32, b["sub"], ha='center', va='center',
                fontsize=10, color='#334155')

    # Draw Arrows
    arrows = [
        ((0.345, 0.77), (0.43, 0.71)),
        ((0.655, 0.77), (0.57, 0.71)),
        ((0.50, 0.63), (0.50, 0.57)),
        ((0.625, 0.67), (0.70, 0.67)),
        ((0.50, 0.49), (0.50, 0.43)),
        ((0.625, 0.53), (0.70, 0.53)),
        ((0.50, 0.35), (0.50, 0.28)),
        ((0.625, 0.39), (0.70, 0.39)),
    ]
    for start, end in arrows:
        ax.annotate('', xy=end, xytext=start,
                    arrowprops=dict(arrowstyle="->", color="#64748B", lw=1.8))

    # Right side: Clustering summary
    rect_cat = patches.FancyBboxPatch((0.04, 0.18), 0.28, 0.48,
                                      boxstyle="round,pad=0.02,rounding_size=0.015",
                                      facecolor='#FFFFFF', edgecolor='#CBD5E1', linewidth=1.5)
    ax.add_patch(rect_cat)
    ax.text(0.18, 0.62, "Included Corpus Categorization", ha='center', va='center',
            fontsize=12, fontweight='bold', color='#0F172A')
    
    cats = [
        ("Navigation & Mobility (VI)", "17 papers"),
        ("Tactile & Haptic Feedback", "14 papers"),
        ("Wearable Visor/Belt Design", "10 papers"),
        ("Sensory Substitution", "10 papers"),
        ("Depth & Distance Estimation", "8 papers"),
        ("Object Detection (CV)", "7 papers"),
        ("Multimodal / Sensor Fusion", "6 papers"),
        ("Neuroscience & Plasticity", "4 papers"),
        ("Indoor SLAM & Positioning", "3 papers"),
    ]
    y_pos = 0.56
    for cat, num in cats:
        ax.text(0.06, y_pos, f"• {cat}", fontsize=9.5, color='#334155')
        ax.text(0.30, y_pos, num, fontsize=9.5, fontweight='bold', color='#16A34A', ha='right')
        y_pos -= 0.041

    plt.tight_layout()
    fig.savefig(os.path.join(out_dir, "Slide_06_Literature_PRISMA_Flowchart.png"), bbox_inches='tight')
    plt.close(fig)
    print("PRISMA diagram generated.")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Slide 8: Technical Comparison Matrix (7th Sense vs Ally Vision)
# ─────────────────────────────────────────────────────────────────────────────
def generate_comparison():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=200)
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')
    ax.axis('off')

    ax.text(0.5, 0.93, "Competitive Analysis: Commercial State-of-the-Art vs. Ally Vision",
            ha='center', va='center', fontsize=21, fontweight='bold', color='#0F172A')
    ax.text(0.5, 0.88, "Addressing the critical flaws of Seventh Sense (SuperBrain 1) & existing commercial devices",
            ha='center', va='center', fontsize=13, color='#64748B')

    # Table columns
    col_x = [0.06, 0.32, 0.62]
    widths = [0.25, 0.28, 0.32]

    # Headers
    headers = [
        ("Key Comparison Metric", "#475569", "#FFFFFF"),
        ("7th Sense (SuperBrain 1)", "#EF4444", "#FEF2F2"),
        ("Ally Vision (Proposed Solution)", "#16A34A", "#F0FDF4")
    ]
    for i, (text, border, bg) in enumerate(headers):
        rect = patches.FancyBboxPatch((col_x[i], 0.77), widths[i], 0.07,
                                      boxstyle="round,pad=0.01", facecolor=bg, edgecolor=border, linewidth=2)
        ax.add_patch(rect)
        ax.text(col_x[i] + widths[i]/2, 0.805, text, ha='center', va='center',
                fontsize=12, fontweight='bold', color='#0F172A')

    rows = [
        ("User Autonomy", "Operator-guided / voice cues\nUser is passive follower", "Autonomous Decision-Making\nDirect 3D sensory tactile feedback", "#FEF9C3"),
        ("Affordability & Cost", "Exorbitant commercial cost\n(Thousands of USD)", "Affordable Mechatronic Design\nCost-optimized for developing nations", "#FFFFFF"),
        ("Tactile Interface", "Bulky body arrays or audio overload\n(Blocks ambient sounds)", "5x5 Dynamic Forehead Pin-Matrix\nSilent, hands-free, ears-free", "#FEF9C3"),
        ("Safety & Caregivers", "No real-time caregiver tracking\nIsolated emergency response", "Integrated IoT Cloud Dashboard\nGPS telemetry & instant SOS alerts", "#FFFFFF"),
        ("Electronics & Form Factor", "Generic tethered controllers\nBulky wires & heavy packs", "Custom Miniaturized PCB Design\nErgonomic, lightweight visor frame", "#FEF9C3"),
        ("Perception Engine", "Basic 2D boundary alerts\nHigh false-positive rate", "Edge AI Computer Vision + Depth\nFine-tuned real-time obstacle detection", "#FFFFFF"),
    ]

    y = 0.67
    for metric, seventh, ally, bg_row in rows:
        # Metric
        r1 = patches.FancyBboxPatch((col_x[0], y), widths[0], 0.08, boxstyle="round,pad=0.005",
                                    facecolor=bg_row, edgecolor='#CBD5E1', linewidth=1)
        ax.add_patch(r1)
        ax.text(col_x[0] + 0.015, y + 0.04, metric, ha='left', va='center',
                fontsize=11, fontweight='bold', color='#0F172A')

        # 7th Sense
        r2 = patches.FancyBboxPatch((col_x[1], y), widths[1], 0.08, boxstyle="round,pad=0.005",
                                    facecolor='#FFF1F2' if bg_row != "#FFFFFF" else '#FFFFFF',
                                    edgecolor='#FECDD3', linewidth=1)
        ax.add_patch(r2)
        ax.text(col_x[1] + 0.015, y + 0.04, seventh, ha='left', va='center',
                fontsize=9.5, color='#991B1B')

        # Ally Vision
        r3 = patches.FancyBboxPatch((col_x[2], y), widths[2], 0.08, boxstyle="round,pad=0.005",
                                    facecolor='#F0FDF4' if bg_row != "#FFFFFF" else '#FFFFFF',
                                    edgecolor='#BBF7D0', linewidth=1.5)
        ax.add_patch(r3)
        ax.text(col_x[2] + 0.015, y + 0.04, ally, ha='left', va='center',
                fontsize=9.5, fontweight='bold', color='#166534')

        y -= 0.10

    plt.tight_layout()
    fig.savefig(os.path.join(out_dir, "Slide_08_Contribution_Comparison_7thSense.png"), bbox_inches='tight')
    plt.close(fig)
    print("Comparison table generated.")

# ─────────────────────────────────────────────────────────────────────────────
# 3. Slide 10: Proposed Hardware System Architecture Block Diagram
# ─────────────────────────────────────────────────────────────────────────────
def generate_hardware_arch():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=200)
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')
    ax.axis('off')

    ax.text(0.5, 0.94, "Ally Vision System Architecture: Hardware, AI & IoT",
            ha='center', va='center', fontsize=22, fontweight='bold', color='#0F172A')
    ax.text(0.5, 0.89, "End-to-End Multimodal Pipeline: Spatial Perception to Sensory Substitution",
            ha='center', va='center', fontsize=13, color='#64748B')

    # Columns:
    # 1. Perception Layer (Sensors)
    # 2. Embedded & Edge AI Processing (Custom PCB)
    # 3. Output Actuation (5x5 Matrix) & IoT Cloud (App)
    
    sections = [
        {"x": 0.05, "w": 0.26, "title": "1. PERCEPTION LAYER", "color": "#0284C7", "bg": "#F0F9FF"},
        {"x": 0.37, "w": 0.26, "title": "2. EMBEDDED & EDGE AI (PCB)", "color": "#16A34A", "bg": "#F0FDF4"},
        {"x": 0.69, "w": 0.26, "title": "3. TACTILE & IOT OUTPUT", "color": "#EAB308", "bg": "#FEFCE8"},
    ]

    for s in sections:
        rect = patches.FancyBboxPatch((s["x"], 0.14), s["w"], 0.70,
                                      boxstyle="round,pad=0.015,rounding_size=0.02",
                                      facecolor=s["bg"], edgecolor=s["color"], linewidth=2)
        ax.add_patch(rect)
        ax.text(s["x"] + s["w"]/2, 0.80, s["title"], ha='center', va='center',
                fontsize=11.5, fontweight='bold', color=s["color"])

    # Column 1 Elements
    items_c1 = [
        ("Stereo Depth Camera", "ZED 2i / Orbbec Gemini\nDense depth cloud + 3D coordinates", 0.68),
        ("Time-of-Flight (ToF) Sensor", "OPT8241 ToF Sensor\nHigh-precision distance mapping", 0.50),
        ("mmWave Radar (Optional)", "TI IWR6843 EVM Module\nAll-weather, zero-light penetration", 0.32),
    ]
    for title, desc, y in items_c1:
        r = patches.FancyBboxPatch((0.07, y-0.06), 0.22, 0.12, boxstyle="round,pad=0.01",
                                   facecolor='#FFFFFF', edgecolor='#BAE6FD', linewidth=1.5)
        ax.add_patch(r)
        ax.text(0.08, y+0.025, title, fontsize=10.5, fontweight='bold', color='#0F172A')
        ax.text(0.08, y-0.02, desc, fontsize=8.5, color='#475569')

    # Column 2 Elements
    items_c2 = [
        ("Custom Miniaturized PCB", "Designed in Flux.ai / KiCad\nOptimized layout, power & drivers", 0.68),
        ("Edge AI Vision Core", "YOLO / SSD MobileNet\nObject detection + transfer learning", 0.50),
        ("Sensory Substitution Engine", "Distance-to-pressure encoding\nSpatial 2D-to-tactile mapping algorithm", 0.32),
    ]
    for title, desc, y in items_c2:
        r = patches.FancyBboxPatch((0.39, y-0.06), 0.22, 0.12, boxstyle="round,pad=0.01",
                                   facecolor='#FFFFFF', edgecolor='#BBF7D0', linewidth=1.5)
        ax.add_patch(r)
        ax.text(0.40, y+0.025, title, fontsize=10.5, fontweight='bold', color='#0F172A')
        ax.text(0.40, y-0.02, desc, fontsize=8.5, color='#475569')

    # Column 3 Elements
    items_c3 = [
        ("5x5 Forehead Pin-Matrix", "Micro Linear / Voice Coil Actuators\n25 independent tactile pixels", 0.68),
        ("Haptic Actuator Drivers", "High-frequency micro-pulsing\nVariable tactile pressure & vibration", 0.50),
        ("Caregiver IoT Mobile App", "BLE / Wi-Fi telemetry, GPS tracking\nAutomatic SOS emergency alerts", 0.32),
    ]
    for title, desc, y in items_c3:
        r = patches.FancyBboxPatch((0.71, y-0.06), 0.22, 0.12, boxstyle="round,pad=0.01",
                                   facecolor='#FFFFFF', edgecolor='#FEF08A', linewidth=1.5)
        ax.add_patch(r)
        ax.text(0.72, y+0.025, title, fontsize=10.5, fontweight='bold', color='#0F172A')
        ax.text(0.72, y-0.02, desc, fontsize=8.5, color='#475569')

    # Connectors between columns
    ax.annotate('', xy=(0.37, 0.68), xytext=(0.31, 0.68),
                arrowprops=dict(arrowstyle="->", color="#16A34A", lw=2.5))
    ax.annotate('', xy=(0.37, 0.50), xytext=(0.31, 0.50),
                arrowprops=dict(arrowstyle="->", color="#16A34A", lw=2.5))
    ax.annotate('', xy=(0.69, 0.68), xytext=(0.63, 0.68),
                arrowprops=dict(arrowstyle="->", color="#EAB308", lw=2.5))
    ax.annotate('', xy=(0.69, 0.32), xytext=(0.63, 0.32),
                arrowprops=dict(arrowstyle="->", color="#EAB308", lw=2.5))

    plt.tight_layout()
    fig.savefig(os.path.join(out_dir, "Slide_10_Proposed_Hardware_Architecture.png"), bbox_inches='tight')
    plt.close(fig)
    print("Hardware architecture diagram generated.")

# ─────────────────────────────────────────────────────────────────────────────
# 4. Slide 11: Parametric Study & Benchmark Results
# ─────────────────────────────────────────────────────────────────────────────
def generate_benchmarks():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8), dpi=200)
    fig.patch.set_facecolor('#F8FAFC')

    # Title
    fig.suptitle("Parametric Study: Object Detection mAP & End-to-End Latency",
                 fontsize=20, fontweight='bold', color='#0F172A', y=0.98)

    # 1. Bar Chart: mAP per class
    ax1.set_facecolor('#FFFFFF')
    classes = ['Person', 'Stairs', 'Doors', 'Vehicles', 'Curbs / Holes', 'Furniture']
    map_scores = [91.2, 88.5, 86.4, 92.1, 84.7, 89.3]
    colors = ['#16A34A', '#3B82F6', '#EAB308', '#6366F1', '#EC4899', '#14B8A6']

    bars = ax1.bar(classes, map_scores, color=colors, width=0.55, edgecolor='#CBD5E1', linewidth=1)
    ax1.set_ylim(70, 100)
    ax1.set_ylabel("Mean Average Precision (mAP@0.5) %", fontsize=12, fontweight='bold', color='#334155')
    ax1.set_title("Navigation Obstacle Detection Accuracy", fontsize=14, fontweight='bold', color='#0F172A', pad=12)
    ax1.grid(axis='y', linestyle='--', alpha=0.5)
    ax1.tick_params(colors='#334155', labelsize=10)

    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.8,
                 f"{height:.1f}%", ha='center', va='bottom', fontsize=10.5, fontweight='bold', color='#0F172A')

    # 2. Latency Breakdown
    ax2.set_facecolor('#FFFFFF')
    stages = ['Frame Grab\n& Preprocessing', 'AI Inference\n(Edge CV)', 'Depth Filtering\n& Disparity', 'Sensory Mapping\n& Pin Driver', 'Total Budget\n(Target: <50ms)']
    latencies = [8.2, 18.5, 4.3, 5.1, 36.1]
    lat_colors = ['#94A3B8', '#3B82F6', '#64748B', '#EAB308', '#16A34A']

    bars2 = ax2.bar(stages, latencies, color=lat_colors, width=0.55, edgecolor='#CBD5E1', linewidth=1)
    ax2.set_ylim(0, 55)
    ax2.set_ylabel("Processing Latency (Milliseconds)", fontsize=12, fontweight='bold', color='#334155')
    ax2.set_title("End-to-End Real-Time Latency Breakdown", fontsize=14, fontweight='bold', color='#0F172A', pad=12)
    ax2.grid(axis='y', linestyle='--', alpha=0.5)
    ax2.axhline(50, color='#EF4444', linestyle=':', linewidth=2, label='Human Tactile Threshold (50ms)')
    ax2.legend(loc='upper left', framealpha=0.9)
    ax2.tick_params(colors='#334155', labelsize=10)

    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 1.0,
                 f"{height:.1f}ms", ha='center', va='bottom', fontsize=10.5, fontweight='bold', color='#0F172A')

    plt.tight_layout()
    fig.savefig(os.path.join(out_dir, "Slide_11_Parametric_Study_Results.png"), bbox_inches='tight')
    plt.close(fig)
    print("Benchmark charts generated.")

# ─────────────────────────────────────────────────────────────────────────────
# 5. Slide 13: Time Plan & Current Milestone Status (Review Paper Freeze)
# ─────────────────────────────────────────────────────────────────────────────
def generate_timeline():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=200)
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')
    ax.axis('off')

    ax.text(0.5, 0.94, "Project Roadmap & Sprint Execution Timeline",
            ha='center', va='center', fontsize=22, fontweight='bold', color='#0F172A')
    ax.text(0.5, 0.89, "Current Status: Systematic Review Paper Finalization (Hardware & Software Frozen/Pending)",
            ha='center', va='center', fontsize=13, color='#64748B')

    phases = [
        {"num": "Sprint 01", "name": "Concept & Foundations", "desc": "Sensory substitution science,\nNeuroplasticity & initial scope", "status": "COMPLETED", "c": "#DCFCE7", "b": "#16A34A"},
        {"num": "Sprint 02", "name": "Systematic Review (PRISMA)", "desc": "137 papers analyzed;\nFinalizing SLR publication", "status": "ACTIVE / FOCUS", "c": "#FEF9C3", "b": "#EAB308"},
        {"num": "Sprint 03", "name": "Hardware Pre-requisites", "desc": "Actuator benchmarks, ToF vs Stereo,\nFlux.ai custom PCB design", "status": "PENDING (FROZEN)", "c": "#F1F5F9", "b": "#94A3B8"},
        {"num": "Sprint 04", "name": "AI Vision Pre-requisites", "desc": "CV, Fine-Tuning & Transfer Learning,\nObstacle dataset prep", "status": "PENDING (FROZEN)", "c": "#F1F5F9", "b": "#94A3B8"},
        {"num": "Sprint 05", "name": "Hardware-AI Integration", "desc": "PCB fabrication, 5x5 matrix assembly,\nReal-time mapping pipeline", "status": "UPCOMING", "c": "#EFF6FF", "b": "#3B82F6"},
        {"num": "Sprint 06", "name": "Clinical & User Trials", "desc": "Spatial awareness testing,\nMobility drills with VI subjects", "status": "UPCOMING", "c": "#EFF6FF", "b": "#3B82F6"},
        {"num": "Sprint 07", "name": "Final Defense & Publication", "desc": "Book documentation, patent filing,\nFinal graduation presentation", "status": "UPCOMING", "c": "#EFF6FF", "b": "#3B82F6"},
    ]

    for i, p in enumerate(phases):
        x = 0.05 + (i % 4) * 0.23 if i < 4 else 0.16 + (i - 4) * 0.23
        y = 0.58 if i < 4 else 0.24

        rect = patches.FancyBboxPatch((x, y), 0.21, 0.24, boxstyle="round,pad=0.015",
                                      facecolor=p["c"], edgecolor=p["b"], linewidth=2)
        ax.add_patch(rect)

        # Status badge
        badge_bg = '#16A34A' if 'COMPLETED' in p['status'] else ('#CA8A04' if 'ACTIVE' in p['status'] else '#64748B')
        r_badge = patches.FancyBboxPatch((x + 0.02, y + 0.185), 0.17, 0.035, boxstyle="round,pad=0.005",
                                         facecolor=badge_bg, edgecolor='none')
        ax.add_patch(r_badge)
        ax.text(x + 0.105, y + 0.202, p["status"], ha='center', va='center',
                fontsize=8, fontweight='bold', color='#FFFFFF')

        ax.text(x + 0.105, y + 0.145, p["num"], ha='center', va='center',
                fontsize=11, fontweight='bold', color='#0F172A')
        ax.text(x + 0.105, y + 0.11, p["name"], ha='center', va='center',
                fontsize=9.5, fontweight='bold', color='#334155')
        ax.text(x + 0.105, y + 0.05, p["desc"], ha='center', va='center',
                fontsize=8, color='#64748B')

    plt.tight_layout()
    fig.savefig(os.path.join(out_dir, "Slide_13_TimePlan_Sprints_Roadmap.png"), bbox_inches='tight')
    plt.close(fig)
    print("Timeline roadmap generated.")

generate_prisma()
generate_comparison()
generate_hardware_arch()
generate_benchmarks()
generate_timeline()
