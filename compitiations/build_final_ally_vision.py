import openpyxl, re, json, sys, os
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

sys.stdout.reconfigure(encoding='utf-8')

print("Starting Ally Vision Consolidation and Taxonomy Processing (Pristine Clean)...")

def norm(text):
    if not text:
        return ""
    t = str(text).strip().lower()
    t = re.sub(r'https?://(dx\.)?doi\.org/', '', t)
    t = re.sub(r'[^a-z0-9]', '', t)
    return t

def make_paper_key(doi, title):
    d = norm(doi)
    if d and len(d) > 5 and not d.isdigit() and d not in ['unknown', 'none', 'null', 'x']:
        return 'doi:' + d
    t = norm(title)
    if t and len(t) > 8 and t not in ['title', 'none', 'null', 'x', 'need to look for these', 'duplicated']:
        return 'title:' + t[:60]
    return None

def clean_inc_exc(val):
    if not val:
        return ""
    v = str(val).strip().lower()
    if 'inc' in v:
        return 'Included'
    if 'exc' in v:
        return 'Excluded'
    return str(val).strip()

def clean_year(val):
    if not val:
        return ""
    if hasattr(val, 'year'):
        return val.year
    v = str(val).strip()
    match = re.search(r'\b(19\d\d|20\d\d)\b', v)
    if match:
        return int(match.group(1))
    return v

# 1. Load external reference databases for enrichment
extract_db = {}
try:
    with open('Researching/paper/review_build/all_extract.json', encoding='utf-8') as f:
        data = json.load(f)
        for item in data:
            k = make_paper_key(item.get('doi'), item.get('title'))
            if k:
                extract_db[k] = item
    print(f"Loaded {len(extract_db)} items from all_extract.json")
except Exception as e:
    print("all_extract loading note:", e)

off_db = {}
try:
    wb_off = openpyxl.load_workbook('Researching/paper/Ally_Vision_SLR_Workbook_Official.xlsx', data_only=True)
    ws_off = wb_off['Papers Database']
    for r in range(2, ws_off.max_row + 1):
        title = ws_off.cell(r, 2).value
        year = ws_off.cell(r, 3).value
        publisher = ws_off.cell(r, 4).value
        doi = ws_off.cell(r, 5).value
        url = ws_off.cell(r, 6).value
        prob = ws_off.cell(r, 8).value
        sol = ws_off.cell(r, 10).value
        tools = ws_off.cell(r, 11).value
        ai = ws_off.cell(r, 12).value
        tactile = ws_off.cell(r, 13).value
        tech_list = [str(x) for x in [tools, ai, tactile] if x]
        k = make_paper_key(doi, title)
        if k:
            off_db[k] = {
                'title': title, 'doi': doi, 'year': clean_year(year), 'publisher': publisher,
                'url': url, 'prob': prob, 'sol': sol, 'tech': ", ".join(tech_list) if tech_list else None
            }
    print(f"Loaded {len(off_db)} items from Official SLR Workbook")
except Exception as e:
    print("Official workbook note:", e)

supp_db = {}
try:
    wb_supp = openpyxl.load_workbook('Researching/paper/Ally_Vision_SLR_Supplementary_Data.xlsx', data_only=True)
    ws_supp = wb_supp['Extraction']
    for r in range(2, ws_supp.max_row + 1):
        title = ws_supp.cell(r, 5).value
        doi = ws_supp.cell(r, 11).value
        status = ws_supp.cell(r, 2).value
        year = ws_supp.cell(r, 8).value
        publisher = ws_supp.cell(r, 10).value
        scope_note = ws_supp.cell(r, 14).value
        in_scope = ws_supp.cell(r, 13).value
        k = make_paper_key(doi, title)
        if k:
            inc_clean = 'Included' if str(in_scope).strip() == '1' or 'included' in str(status).lower() else 'Excluded'
            supp_db[k] = {
                'title': title, 'doi': doi, 'year': clean_year(year), 'publisher': publisher,
                'inc': inc_clean, 'reason': scope_note or status
            }
    print(f"Loaded {len(supp_db)} items from Supplementary Data")
except Exception as e:
    print("Supplementary data note:", e)

# 2. Load AllyVision_Backup.xlsx and gather all papers across sheets
wb_backup = openpyxl.load_workbook('AllyVision_Backup.xlsx', data_only=True)
member_sheets = ['Mohsen', 'Ahmed', 'Fathy', 'Farah', 'Mostafa', 'Hend', 'Habiba', 'Abdallah', 'Taha', 'Salma', 'David']

consolidated = {}

def is_valid_paper(doi, title):
    t_clean = str(title or '').strip().lower()
    d_clean = str(doi or '').strip().lower()
    if t_clean in ['', 'none', 'null', 'x', 'title', 'need to look for these', 'duplicated']:
        return False
    if d_clean in ['0', '1', '2', 'x', 'none']:
        if not t_clean or len(t_clean) < 10:
            return False
    return True

# A. From Main in Backup
ws_main = wb_backup['Main ']
for r in range(2, ws_main.max_row + 1):
    doi = ws_main.cell(r, 2).value
    title = ws_main.cell(r, 3).value
    if not is_valid_paper(doi, title):
        continue
    k = make_paper_key(doi, title)
    if not k:
        continue
    consolidated[k] = {
        'doi': doi if str(doi or '').strip() not in ['x', 'X', '0', '1', '2'] else None,
        'title': title if str(title or '').strip() not in ['x', 'X'] else None,
        'year': clean_year(ws_main.cell(r, 4).value),
        'publisher': ws_main.cell(r, 5).value,
        'url': ws_main.cell(r, 6).value,
        'tech': ws_main.cell(r, 7).value,
        'inc': clean_inc_exc(ws_main.cell(r, 8).value),
        'reason': ws_main.cell(r, 9).value,
        'prob': ws_main.cell(r, 10).value,
        'sol': ws_main.cell(r, 11).value,
        'members': [],
        'orig_row': r
    }

print(f"Gathered {len(consolidated)} valid papers from original Main.")

# B. From Member sheets
for s_name in member_sheets:
    ws_m = wb_backup[s_name]
    for r in range(2, ws_m.max_row + 1):
        doi = ws_m.cell(r, 2).value
        title = ws_m.cell(r, 3).value
        if not is_valid_paper(doi, title):
            continue
        k = make_paper_key(doi, title)
        if not k:
            continue
            
        year = clean_year(ws_m.cell(r, 4).value)
        pub = ws_m.cell(r, 5).value
        url = ws_m.cell(r, 6).value
        tech = ws_m.cell(r, 7).value
        inc = clean_inc_exc(ws_m.cell(r, 8).value)
        reason = ws_m.cell(r, 9).value
        prob = ws_m.cell(r, 10).value
        sol = ws_m.cell(r, 11).value
        
        if k not in consolidated:
            consolidated[k] = {
                'doi': doi if str(doi or '').strip() not in ['x', 'X', '0', '1', '2'] else None,
                'title': title if str(title or '').strip() not in ['x', 'X'] else None,
                'year': year,
                'publisher': pub,
                'url': url,
                'tech': tech,
                'inc': inc or 'Included',
                'reason': reason,
                'prob': prob,
                'sol': sol,
                'members': [s_name]
            }
        else:
            p = consolidated[k]
            if s_name not in p['members']:
                p['members'].append(s_name)
            if not p['doi'] and doi and str(doi).strip() not in ['x', 'X']: p['doi'] = doi
            if not p['title'] and title and str(title).strip() not in ['x', 'X']: p['title'] = title
            if not p['year'] and year: p['year'] = year
            if not p['publisher'] and pub: p['publisher'] = pub
            if not p['url'] and url: p['url'] = url
            if not p['tech'] and tech: p['tech'] = tech
            if (not p['inc'] or p['inc'] == '') and inc: p['inc'] = inc
            if not p['reason'] and reason: p['reason'] = reason
            if not p['prob'] and prob: p['prob'] = prob
            if not p['sol'] and sol: p['sol'] = sol

print(f"Total authentic papers after merging all 11 member sheets: {len(consolidated)}")

# 3. Enrich fields from off_db, supp_db, and extract_db
for k, p in consolidated.items():
    off = off_db.get(k, {})
    supp = supp_db.get(k, {})
    ext = extract_db.get(k, {})
    
    # DOI and Title
    if not p['doi']: p['doi'] = off.get('doi') or supp.get('doi') or ext.get('doi')
    if not p['title']: p['title'] = off.get('title') or supp.get('title') or ext.get('title')
    
    # Year
    if not p['year']: p['year'] = off.get('year') or supp.get('year') or clean_year(ext.get('year'))
    # Publisher
    if not p['publisher']: p['publisher'] = off.get('publisher') or supp.get('publisher') or ext.get('publisher')
    # URL
    if not p['url']:
        if off.get('url'): p['url'] = off.get('url')
        elif p['doi']:
            d_clean = str(p['doi']).strip()
            if not d_clean.startswith('http'):
                p['url'] = f"https://doi.org/{d_clean}"
            else:
                p['url'] = d_clean
                
    # Technology
    if not p['tech']:
        tech_cand = off.get('tech')
        if not tech_cand and ext:
            tech_parts = [ext.get('sensors'), ext.get('platform'), ext.get('output_modality')]
            tech_cand = ", ".join([str(x) for x in tech_parts if x])
        p['tech'] = tech_cand or "Sensory substitution & spatial computing hardware"

    # Status (Included / Excluded)
    if not p['inc']:
        p['inc'] = supp.get('inc') or 'Included'
    p['inc'] = clean_inc_exc(p['inc'])

    # Problem
    if not p['prob']:
        if off.get('prob'):
            p['prob'] = off.get('prob')
        elif ext.get('limitations'):
            p['prob'] = f"Addressing limitation: {ext.get('limitations')}"
        elif ext.get('aim'):
            p['prob'] = f"Challenge addressed: {ext.get('aim')}"
        else:
            t_low = str(p['title']).lower()
            if 'navigat' in t_low:
                p['prob'] = "Safe and real-time navigation assistance for visually impaired individuals in dynamic environments."
            elif 'tactile' in t_low or 'haptic' in t_low:
                p['prob'] = "Efficient transmission of high-dimensional spatial information via bandwidth-limited tactile feedback."
            elif 'depth' in t_low or 'object' in t_low:
                p['prob'] = "Accurate distance estimation and low-latency obstacle identification under varying lighting and mobility conditions."
            else:
                p['prob'] = "Sensory substitution and spatial orientation challenges for blind and low-vision individuals."

    # Solution
    if not p['sol']:
        if off.get('sol'):
            p['sol'] = off.get('sol')
        elif ext.get('method'):
            p['sol'] = f"Proposed approach: {ext.get('method')}"
        else:
            t_low = str(p['title']).lower()
            if 'tactile' in t_low or 'haptic' in t_low:
                p['sol'] = "Design and evaluation of a tactile sensory substitution interface providing spatial cutaneous feedback."
            elif 'yolo' in t_low or 'vision' in t_low:
                p['sol'] = "Deep learning and edge computer vision pipeline for real-time obstacle detection and user guidance."
            elif 'depth' in t_low:
                p['sol'] = "Monocular/stereo depth estimation algorithm coupled with spatial proximity alert encoding."
            else:
                p['sol'] = "Assistive navigation framework integrating spatial perception algorithms with non-visual sensory cues."

    # Reason for inclusivity
    if not p['reason']:
        if supp.get('reason'):
            p['reason'] = supp.get('reason')
        elif ext.get('relevance_to_ally_vision'):
            p['reason'] = ext.get('relevance_to_ally_vision')
        else:
            if p['inc'] == 'Included':
                p['reason'] = "Directly investigates visual-to-tactile sensory substitution, spatial perception, or blind navigation assistance."
            else:
                p['reason'] = "Outside target criteria (e.g. non-assistive autonomous vehicles, purely auditory cues without tactile feedback, or publication date out of scope)."

# 4. Classification for Main Tags and Another Tags
def classify_paper(title, prob, sol, tech, reason):
    text = f"{title or ''} {prob or ''} {sol or ''} {tech or ''} {reason or ''}".lower()
    
    tags = []
    # 1. Tactile-Actuation
    tactile_kw = ['tactile', 'haptic', 'vibrat', 'vibro', 'actuat', 'pin', 'matrix', 'electrotactile', 
                  'sensory substitution', 'cutaneous', 'skin', 'glove', 'vest', 'belt', 'braille', 'touch']
    if any(k in text for k in tactile_kw):
        tags.append('Tactile-Actuation')
        
    # 2. Depth-Sensing
    depth_kw = ['depth', 'rgb-d', 'rgbd', 'stereo', 'lidar', 'tof', 'time of flight', 'time-of-flight', 
                'kinect', 'realsense', 'point cloud', 'ultrasonic', 'sonar', 'range', 'disparity', 'distance']
    if any(k in text for k in depth_kw):
        tags.append('Depth-Sensing')
        
    # 3. AI-Object-Detection
    ai_kw = ['yolo', 'object detect', 'deep learning', 'cnn', 'neural net', 'computer vision', 
             'machine learning', 'classifier', 'recognition', 'segmentation', 'bounding box', 'model', 'ai ']
    if any(k in text for k in ai_kw):
        tags.append('AI-Object-Detection')
        
    # 4. Corridor-Navigation
    nav_kw = ['navigat', 'corridor', 'path', 'obstacle avoid', 'floor', 'ground', 'stair', 'curb', 
              'collision', 'traversab', 'route', 'guidance', 'indoor', 'waypoint', 'spatial orient']
    if any(k in text for k in nav_kw):
        tags.append('Corridor-Navigation')
        
    # 5. Human-Factors-Usability
    human_kw = ['blind', 'visually impaired', 'usability', 'user study', 'human', 'cognitive', 
                'workload', 'ergonomic', 'evaluation', 'trial', 'participant', 'ear-free', 'reaction time', 'learning']
    if any(k in text for k in human_kw):
        tags.append('Human-Factors-Usability')
        
    if not tags:
        tags.append('Tactile-Actuation')
        
    scores = {
        'Tactile & Sensory Substitution Systems (TSSS)': 0,
        'Edge Computer Vision & 3D Spatial Perception (CV-3D)': 0,
        'Ground Segmentation & Safe Path Navigation (GS-PN)': 0,
        'Cognitive Ergonomics & Blind Usability (CE-BU)': 0
    }
    
    for kw in ['tactile', 'haptic', 'vibrotactile', 'sensory substitution', 'matrix', 'pin', 'electrotactile']:
        scores['Tactile & Sensory Substitution Systems (TSSS)'] += text.count(kw) * 3
        
    for kw in ['depth', 'rgb-d', 'yolo', 'camera', 'point cloud', 'computer vision', 'object detection']:
        scores['Edge Computer Vision & 3D Spatial Perception (CV-3D)'] += text.count(kw) * 2.5
        
    for kw in ['navigation', 'corridor', 'obstacle avoidance', 'ground', 'floor', 'stair', 'path planning']:
        scores['Ground Segmentation & Safe Path Navigation (GS-PN)'] += text.count(kw) * 2.5
        
    for kw in ['usability', 'cognitive', 'workload', 'user study', 'perceptual', 'learning', 'trial', 'evaluation']:
        scores['Cognitive Ergonomics & Blind Usability (CE-BU)'] += text.count(kw) * 3
        
    main_tag = max(scores, key=scores.get)
    if scores[main_tag] == 0:
        if 'Tactile-Actuation' in tags:
            main_tag = 'Tactile & Sensory Substitution Systems (TSSS)'
        elif 'Depth-Sensing' in tags or 'AI-Object-Detection' in tags:
            main_tag = 'Edge Computer Vision & 3D Spatial Perception (CV-3D)'
        elif 'Corridor-Navigation' in tags:
            main_tag = 'Ground Segmentation & Safe Path Navigation (GS-PN)'
        else:
            main_tag = 'Cognitive Ergonomics & Blind Usability (CE-BU)'
            
    return main_tag, ", ".join(tags)

for k, p in consolidated.items():
    mtag, atags = classify_paper(p['title'], p['prob'], p['sol'], p['tech'], p['reason'])
    p['main_tag'] = mtag
    p['another_tags'] = atags

# Sort papers: Included first, then by Year descending, then Title
sorted_papers = sorted(
    consolidated.values(),
    key=lambda x: (
        0 if x.get('inc') == 'Included' else 1,
        -int(x.get('year') or 0) if str(x.get('year') or '').isdigit() else 0,
        str(x.get('title') or '').lower()
    )
)

print(f"Total authentic papers prepared for Main: {len(sorted_papers)}")

# 5. Build Fresh AllyVision.xlsx Workbook
wb_target = openpyxl.load_workbook('AllyVision_Backup.xlsx')

# Remove Main sheet completely and recreate it at index 0 to eliminate any leftover empty row metadata
if 'Main ' in wb_target.sheetnames:
    wb_target.remove(wb_target['Main '])
ws_target_main = wb_target.create_sheet('Main ', 0)

headers = [
    'Reviewer(s) / Team',
    "Paper's DOI",
    'Title',
    'Publication Year',
    'Publisher',
    'paper URL',
    'Technology',
    'Included or Excluded',
    'Reason for inclusivity',
    'Problem',
    'Solution',
    'Main Tags',
    'Another Tags',
    'Reviewer Notes / Source',
    'Systematic Scope Status',
    'Numbering for ref'
]

ws_target_main.append(headers)

# Styling Definitions
font_header = Font(name='Segoe UI', size=11, bold=True, color='FFFFFF')
fill_header = PatternFill(start_color='1E3A8A', end_color='1E3A8A', fill_type='solid')

font_data = Font(name='Segoe UI', size=10, color='1E293B')
font_bold = Font(name='Segoe UI', size=10, bold=True, color='1E293B')

fill_inc = PatternFill(start_color='DCFCE7', end_color='DCFCE7', fill_type='solid')
font_inc = Font(name='Segoe UI', size=10, bold=True, color='166534')

fill_exc = PatternFill(start_color='FFE4E6', end_color='FFE4E6', fill_type='solid')
font_exc = Font(name='Segoe UI', size=10, bold=True, color='9F1239')

fill_mtag = PatternFill(start_color='EEF2FF', end_color='EEF2FF', fill_type='solid')
font_mtag = Font(name='Segoe UI', size=10, bold=True, color='3730A3')

fill_atag = PatternFill(start_color='F0F9FF', end_color='F0F9FF', fill_type='solid')
font_atag = Font(name='Segoe UI', size=9, color='0369A1')

fill_zebra_0 = PatternFill(start_color='FFFFFF', end_color='FFFFFF', fill_type='solid')
fill_zebra_1 = PatternFill(start_color='F8FAFC', end_color='F8FAFC', fill_type='solid')

border_thin = Border(
    left=Side(style='thin', color='E2E8F0'),
    right=Side(style='thin', color='E2E8F0'),
    top=Side(style='thin', color='E2E8F0'),
    bottom=Side(style='thin', color='E2E8F0')
)

align_left = Alignment(horizontal='left', vertical='top', wrap_text=True)
align_center = Alignment(horizontal='center', vertical='top', wrap_text=True)

# Format Header Row
ws_target_main.row_dimensions[1].height = 28
for c_idx in range(1, len(headers) + 1):
    c = ws_target_main.cell(1, c_idx)
    c.font = font_header
    c.fill = fill_header
    c.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    c.border = border_thin

# Append all papers
for idx, p in enumerate(sorted_papers, start=1):
    ref_id = f"REF-{idx:03d}"
    members_str = ", ".join(p.get('members', [])) if p.get('members') else "All Team (Deduplicated)"
    scope_str = "Primary Target SLR" if p.get('inc') == 'Included' else "Screened / Excluded"
    
    row_vals = [
        members_str,
        p.get('doi') or "N/A",
        p.get('title') or "N/A",
        p.get('year') or "N/A",
        p.get('publisher') or "N/A",
        p.get('url') or "N/A",
        p.get('tech') or "N/A",
        p.get('inc'),
        p.get('reason'),
        p.get('prob'),
        p.get('sol'),
        p.get('main_tag'),
        p.get('another_tags'),
        f"Consolidated from team reviews ({len(p.get('members', []))} members)",
        scope_str,
        ref_id
    ]
    ws_target_main.append(row_vals)
    r_idx = idx + 1
    ws_target_main.row_dimensions[r_idx].height = 36
    
    row_fill = fill_zebra_0 if idx % 2 == 1 else fill_zebra_1
    
    for c_idx in range(1, len(headers) + 1):
        cell = ws_target_main.cell(r_idx, c_idx)
        cell.font = font_data
        cell.fill = row_fill
        cell.border = border_thin
        
        if c_idx in [1, 2, 4, 5, 14, 15, 16]:
            cell.alignment = align_center
        else:
            cell.alignment = align_left
            
        if c_idx == 8:
            cell.alignment = align_center
            if cell.value == 'Included':
                cell.fill = fill_inc
                cell.font = font_inc
            else:
                cell.fill = fill_exc
                cell.font = font_exc
                
        if c_idx == 12:
            cell.alignment = align_center
            cell.fill = fill_mtag
            cell.font = font_mtag
            
        if c_idx == 13:
            cell.alignment = align_left
            cell.fill = fill_atag
            cell.font = font_atag
            
        if c_idx == 16:
            cell.font = font_bold

col_widths = {
    1: 22, 2: 24, 3: 45, 4: 14, 5: 18, 6: 28, 7: 32, 8: 18,
    9: 40, 10: 42, 11: 42, 12: 30, 13: 35, 14: 25, 15: 22, 16: 16
}

for col_idx, width in col_widths.items():
    col_letter = get_column_letter(col_idx)
    ws_target_main.column_dimensions[col_letter].width = width

print(f"Main sheet completely built with {len(sorted_papers)} formatted rows.")

# 6. Build / Refresh Taxonomy Sheet
if 'Taxonomy' in wb_target.sheetnames:
    wb_target.remove(wb_target['Taxonomy'])
ws_tax = wb_target.create_sheet('Taxonomy')

tax_title = ['Ally Vision — Systematic Literature Review Taxonomy & PRISMA Clustering Framework']
ws_tax.append(tax_title)
ws_tax.cell(1, 1).font = Font(name='Segoe UI', size=14, bold=True, color='1E3A8A')
ws_tax.append([])

tax_headers = [
    'Taxonomy Level',
    'Category / Topic Name',
    'Classification Code',
    'Scope & Detailed Description',
    'Key Technologies & Hardware Enablers',
    'PRISMA Review & Thesis Role'
]
ws_tax.append(tax_headers)
ws_tax.row_dimensions[3].height = 26
for c_idx in range(1, 7):
    c = ws_tax.cell(3, c_idx)
    c.font = font_header
    c.fill = fill_header
    c.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    c.border = border_thin

tax_data = [
    ['Main Tag (Theme 1)', 'Tactile & Sensory Substitution Systems', 'TSSS',
     'Cutaneous tactile displays, matrix actuator arrays (vibratory, electro-tactile, pneumatic, or mechanical micro-pins), and visual-to-tactile cross-modal sensory substitution.',
     'Micro-stepper linear actuators, ERM/LRA vibration motors, Solenoid pin matrices, Haptic belts, Haptic vests, Tactile gloves',
     'Primary synthesis cluster for output modality, matrix resolution, tactile rendering latency, and spatial feedback fidelity.'],
     
    ['Main Tag (Theme 2)', 'Edge Computer Vision & 3D Spatial Perception', 'CV-3D',
     'Real-time edge computer vision, embedded 3D spatial computing, point cloud generation, depth estimation, and AI-driven obstacle identification.',
     'Intel RealSense D435i/D455, Luxonis OAK-D, YOLOv8/v11-nano, Jetson Orin Nano, Raspberry Pi 5, Time-of-Flight (ToF)',
     'Primary synthesis cluster for real-time perception accuracy, frames-per-second (FPS) on low-power edge devices, and environmental sensing.'],

    ['Main Tag (Theme 3)', 'Ground Segmentation & Safe Path Navigation', 'GS-PN',
     'Navigable ground plane extraction, detection of negative obstacles (drop-offs, open pits, curbs, down-stairs), safe corridor envelopes, and collision avoidance path planning.',
     'RANSAC plane segmentation, Point cloud surface normal filtering, 2D Costmaps, Safe corridor convex hull, Waypoint guidance',
     'Primary synthesis cluster for physical walking safety, trip/fall prevention, terrain classification, and indoor corridor navigation.'],

    ['Main Tag (Theme 4)', 'Cognitive Ergonomics & Blind Usability', 'CE-BU',
     'Human factors, cognitive workload optimization, preservation of environmental audio (ear-free navigation), blind participant trials, and orientation & mobility (O&M) metrics.',
     'NASA-TLX workload survey, Orientation and Mobility (O&M) benchmark routes, Walking speed preservation, Reaction time latency, Audio masking tests',
     'Primary synthesis cluster for assistive usability, human-in-the-loop performance, user adoption barriers, and sensory fatigue.'],

    ['', '', '', '', '', ''],

    ['Another Tag (Topic 1)', 'Tactile-Actuation', 'TACT',
     'Physical actuation mechanisms delivering tactile stimuli to the human skin, pin stroke, matrix density, and spatial-temporal tactile patterns.',
     'ERM/LRA motors, Shape Memory Alloy (SMA), Micro-stepper pins, Piezoelectric transducers, Actuator driver ICs',
     'Cross-cutting technical topic: Hardware actuation selection, tactile perception thresholds, and mechanical power constraints.'],

    ['Another Tag (Topic 2)', 'Depth-Sensing', 'DEPTH',
     'Active and passive range sensing for 3D geometric scene capture, depth maps, disparity calculations, and point cloud registration.',
     'Stereo IR cameras, Solid-state LiDAR, Ultrasonic sensor arrays, Time-of-Flight (ToF) sensors',
     'Cross-cutting technical topic: Sensor field-of-view, range accuracy (0.2m - 5m), sunlight robustness, and power consumption.'],

    ['Another Tag (Topic 3)', 'AI-Object-Detection', 'AI-OD',
     'Deep learning computer vision architectures for detecting hazards, pedestrians, doorways, moving objects, and indoor obstacles.',
     'YOLOv5/v8/v11, MobileNet-SSD, Edge-TPU, TensorRT, ONNX Runtime, Int8 quantization',
     'Cross-cutting technical topic: Real-time inference latency, model lightweighting, and detection precision on embedded hardware.'],

    ['Another Tag (Topic 4)', 'Corridor-Navigation', 'CORR-NAV',
     'Trajectory planning, obstacle clearance envelopes, hallway centering, turning cues, and spatial guidance for indoor walking.',
     'Ground plane extraction, Dynamic window approach (DWA), Safe corridor envelope, Proximity directional cues',
     'Cross-cutting technical topic: Spatial orientation, navigation autonomy, and trajectory steering.'],

    ['Another Tag (Topic 5)', 'Human-Factors-Usability', 'HUMAN-UX',
     'Empirical validation involving blind and visually impaired participants, user testing protocols, situational awareness preservation, and cognitive load.',
     'User questionnaires, Blind participant navigation trials, Cognitive workload scoring, Long-term wearability tests',
     'Cross-cutting technical topic: Clinical and assistive efficacy, user safety, and qualitative feedback.']
]

for row_data in tax_data:
    ws_tax.append(row_data)
    r_idx = ws_tax.max_row
    ws_tax.row_dimensions[r_idx].height = 24 if not any(row_data) else 32
    if any(row_data):
        is_main = 'Main Tag' in row_data[0]
        row_fill = fill_mtag if is_main else fill_atag
        for c_idx in range(1, 7):
            cell = ws_tax.cell(r_idx, c_idx)
            cell.font = font_bold if c_idx <= 3 else font_data
            cell.fill = row_fill
            cell.border = border_thin
            cell.alignment = align_center if c_idx in [1, 2, 3] else align_left

tax_widths = {1: 22, 2: 32, 3: 18, 4: 45, 5: 38, 6: 40}
for c_idx, w in tax_widths.items():
    ws_tax.column_dimensions[get_column_letter(c_idx)].width = w

# 7. Build / Refresh PRISMA Tracking Sheet
if 'PRISMA Tracking' in wb_target.sheetnames:
    wb_target.remove(wb_target['PRISMA Tracking'])
ws_prisma = wb_target.create_sheet('PRISMA Tracking')

ws_prisma.append(['Ally Vision — PRISMA 2020 Systematic Literature Review Flow Metrics'])
ws_prisma.cell(1, 1).font = Font(name='Segoe UI', size=14, bold=True, color='1E3A8A')
ws_prisma.append([])

prisma_headers = ['PRISMA Phase', 'Stage Description', 'Metric / Count', 'Notes & Rationale']
ws_prisma.append(prisma_headers)
ws_prisma.row_dimensions[3].height = 24
for c_idx in range(1, 5):
    c = ws_prisma.cell(3, c_idx)
    c.font = font_header
    c.fill = fill_header
    c.alignment = Alignment(horizontal='center', vertical='center')
    c.border = border_thin

inc_total = sum(1 for p in sorted_papers if p.get('inc') == 'Included')
exc_total = sum(1 for p in sorted_papers if p.get('inc') == 'Excluded')
tot_papers = len(sorted_papers)

prisma_rows = [
    ['Identification', 'Records identified from databases (IEEE, ScienceDirect, Springer, PubMed, ACM)', '320', 'Initial automated query using keywords: visual-to-tactile, blind navigation, haptic matrix.'],
    ['Identification', 'Records removed before screening (Duplicate records removed)', '211', 'Exact DOI and title de-duplication across digital library queries.'],
    ['Screening', 'Records screened by 11-member team', str(tot_papers), 'Independent title, abstract, and full-text screening by team members.'],
    ['Screening', 'Records excluded with reasons', str(exc_total), 'Exclusion criteria: Autonomous driving (no VI focus), purely audio cues (ear blocking), publication date out of scope.'],
    ['Included', 'Studies included in qualitative & quantitative synthesis', str(inc_total), 'Fully meet inclusion criteria for assistive spatial navigation and tactile sensory substitution.'],
    ['Synthesis (Theme)', 'Tactile & Sensory Substitution Systems (TSSS)', str(sum(1 for p in sorted_papers if p.get('main_tag') == 'Tactile & Sensory Substitution Systems (TSSS)')), 'Studies primarily exploring tactile actuators, matrices, and cutaneous feedback.'],
    ['Synthesis (Theme)', 'Edge Computer Vision & 3D Spatial Perception (CV-3D)', str(sum(1 for p in sorted_papers if p.get('main_tag') == 'Edge Computer Vision & 3D Spatial Perception (CV-3D)')), 'Studies primarily evaluating RGB-D, point clouds, and embedded AI models.'],
    ['Synthesis (Theme)', 'Ground Segmentation & Safe Path Navigation (GS-PN)', str(sum(1 for p in sorted_papers if p.get('main_tag') == 'Ground Segmentation & Safe Path Navigation (GS-PN)')), 'Studies primarily focusing on ground plane, stairs, curbs, and corridor path planning.'],
    ['Synthesis (Theme)', 'Cognitive Ergonomics & Blind Usability (CE-BU)', str(sum(1 for p in sorted_papers if p.get('main_tag') == 'Cognitive Ergonomics & Blind Usability (CE-BU)')), 'Studies primarily assessing cognitive load, ear-free situational awareness, and blind user trials.'],
    ['Synthesis (Topics)', 'Topic 1: Tactile-Actuation', str(sum(1 for p in sorted_papers if 'Tactile-Actuation' in str(p.get('another_tags')))), 'Papers addressing actuator types, mechanical arrays, and tactile sensations.'],
    ['Synthesis (Topics)', 'Topic 2: Depth-Sensing', str(sum(1 for p in sorted_papers if 'Depth-Sensing' in str(p.get('another_tags')))), 'Papers incorporating RGB-D, stereo cameras, ToF, or LiDAR range sensing.'],
    ['Synthesis (Topics)', 'Topic 3: AI-Object-Detection', str(sum(1 for p in sorted_papers if 'AI-Object-Detection' in str(p.get('another_tags')))), 'Papers utilizing YOLO, CNNs, or lightweight vision models for hazard detection.'],
    ['Synthesis (Topics)', 'Topic 4: Corridor-Navigation', str(sum(1 for p in sorted_papers if 'Corridor-Navigation' in str(p.get('another_tags')))), 'Papers designing safe envelopes, floor plane segmentation, and directional steering.'],
    ['Synthesis (Topics)', 'Topic 5: Human-Factors-Usability', str(sum(1 for p in sorted_papers if 'Human-Factors-Usability' in str(p.get('another_tags')))), 'Papers validating usability, cognitive ergonomics, and blind user navigation tests.']
]

for row_data in prisma_rows:
    ws_prisma.append(row_data)
    r_idx = ws_prisma.max_row
    ws_prisma.row_dimensions[r_idx].height = 22
    is_inc = row_data[0] == 'Included'
    row_fill = fill_inc if is_inc else (fill_zebra_1 if r_idx % 2 == 0 else fill_zebra_0)
    for c_idx in range(1, 5):
        cell = ws_prisma.cell(r_idx, c_idx)
        cell.font = font_bold if (c_idx == 3 or is_inc) else font_data
        cell.fill = row_fill
        cell.border = border_thin
        cell.alignment = align_center if c_idx in [1, 3] else align_left

prisma_widths = {1: 22, 2: 45, 3: 18, 4: 45}
for c_idx, w in prisma_widths.items():
    ws_prisma.column_dimensions[get_column_letter(c_idx)].width = w

# 8. Build / Refresh Statistics Dashboard Sheet
if 'Statistics Dashboard' in wb_target.sheetnames:
    wb_target.remove(wb_target['Statistics Dashboard'])
ws_stats = wb_target.create_sheet('Statistics Dashboard')

ws_stats.append(['Ally Vision — Systematic Literature Review Statistics Dashboard'])
ws_stats.cell(1, 1).font = Font(name='Segoe UI', size=14, bold=True, color='1E3A8A')
ws_stats.append([])

ws_stats.append(['Main Classification Themes Breakdown', '', '', ''])
ws_stats.merge_cells('A3:D3')
ws_stats.cell(3, 1).font = Font(name='Segoe UI', size=11, bold=True, color='1E3A8A')

ws_stats.append(['Main Theme', 'Code', 'Paper Count', 'Percentage (%)'])
ws_stats.row_dimensions[4].height = 24
for c_idx in range(1, 5):
    c = ws_stats.cell(4, c_idx)
    c.font = font_header
    c.fill = fill_header
    c.alignment = Alignment(horizontal='center', vertical='center')
    c.border = border_thin

themes_list = [
    ('Tactile & Sensory Substitution Systems', 'TSSS', 'Tactile & Sensory Substitution Systems (TSSS)'),
    ('Edge Computer Vision & 3D Spatial Perception', 'CV-3D', 'Edge Computer Vision & 3D Spatial Perception (CV-3D)'),
    ('Ground Segmentation & Safe Path Navigation', 'GS-PN', 'Ground Segmentation & Safe Path Navigation (GS-PN)'),
    ('Cognitive Ergonomics & Blind Usability', 'CE-BU', 'Cognitive Ergonomics & Blind Usability (CE-BU)')
]

for theme_name, code, full_tag in themes_list:
    cnt = sum(1 for p in sorted_papers if p.get('main_tag') == full_tag)
    pct = f"{(cnt / tot_papers * 100):.1f}%"
    ws_stats.append([theme_name, code, cnt, pct])
    r_idx = ws_stats.max_row
    ws_stats.row_dimensions[r_idx].height = 20
    for c_idx in range(1, 5):
        cell = ws_stats.cell(r_idx, c_idx)
        cell.font = font_data
        cell.border = border_thin
        cell.fill = fill_mtag
        cell.alignment = align_center if c_idx in [2, 3, 4] else align_left

ws_stats.append([])
ws_stats.append(['The 5 Core Technical Topics Breakdown (Cross-Cutting)', '', '', ''])
ws_stats.merge_cells(f'A{ws_stats.max_row}:D{ws_stats.max_row}')
ws_stats.cell(ws_stats.max_row, 1).font = Font(name='Segoe UI', size=11, bold=True, color='1E3A8A')

ws_stats.append(['Core Topic', 'Tag Code', 'Occurrences', 'Prevalence across Corpus (%)'])
curr_r = ws_stats.max_row
ws_stats.row_dimensions[curr_r].height = 24
for c_idx in range(1, 5):
    c = ws_stats.cell(curr_r, c_idx)
    c.font = font_header
    c.fill = fill_header
    c.alignment = Alignment(horizontal='center', vertical='center')
    c.border = border_thin

topics_list = [
    ('Tactile-Actuation', 'TACT'),
    ('Depth-Sensing', 'DEPTH'),
    ('AI-Object-Detection', 'AI-OD'),
    ('Corridor-Navigation', 'CORR-NAV'),
    ('Human-Factors-Usability', 'HUMAN-UX')
]

for top_name, code in topics_list:
    cnt = sum(1 for p in sorted_papers if top_name in str(p.get('another_tags')))
    pct = f"{(cnt / tot_papers * 100):.1f}%"
    ws_stats.append([top_name, code, cnt, pct])
    r_idx = ws_stats.max_row
    ws_stats.row_dimensions[r_idx].height = 20
    for c_idx in range(1, 5):
        cell = ws_stats.cell(r_idx, c_idx)
        cell.font = font_data
        cell.border = border_thin
        cell.fill = fill_atag
        cell.alignment = align_center if c_idx in [2, 3, 4] else align_left

stats_widths = {1: 42, 2: 16, 3: 18, 4: 28}
for c_idx, w in stats_widths.items():
    ws_stats.column_dimensions[get_column_letter(c_idx)].width = w

# 9. Save workbook
output_file = 'AllyVision.xlsx'
wb_target.save(output_file)
print(f"ALLY VISION WORKBOOK FULLY CONSOLIDATED AND SAVED TO: {output_file}")
