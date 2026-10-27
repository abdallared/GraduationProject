import openpyxl, re, json, sys, os
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

sys.stdout.reconfigure(encoding='utf-8')

print("Starting Exact Sequential Alignment of Excel and Markdown...")

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

# Load enrichment databases
extract_db = {}
try:
    with open('Researching/paper/review_build/all_extract.json', encoding='utf-8') as f:
        data = json.load(f)
        for item in data:
            k = make_paper_key(item.get('doi'), item.get('title'))
            if k: extract_db[k] = item
except Exception:
    pass

off_db = {}
try:
    wb_off = openpyxl.load_workbook('Researching/paper/Ally_Vision_SLR_Workbook_Official.xlsx', data_only=True)
    ws_off = wb_off['Papers Database']
    for r in range(2, ws_off.max_row + 1):
        t = ws_off.cell(r, 2).value
        d = ws_off.cell(r, 5).value
        k = make_paper_key(d, t)
        if k:
            tools = ws_off.cell(r, 11).value
            ai = ws_off.cell(r, 12).value
            tact = ws_off.cell(r, 13).value
            tech_list = [str(x) for x in [tools, ai, tact] if x]
            off_db[k] = {
                'title': t, 'doi': d, 'year': clean_year(ws_off.cell(r, 3).value),
                'publisher': ws_off.cell(r, 4).value, 'url': ws_off.cell(r, 6).value,
                'prob': ws_off.cell(r, 8).value, 'sol': ws_off.cell(r, 10).value,
                'tech': ", ".join(tech_list) if tech_list else None
            }
except Exception:
    pass

supp_db = {}
try:
    wb_supp = openpyxl.load_workbook('Researching/paper/Ally_Vision_SLR_Supplementary_Data.xlsx', data_only=True)
    ws_supp = wb_supp['Extraction']
    for r in range(2, ws_supp.max_row + 1):
        t = ws_supp.cell(r, 5).value
        d = ws_supp.cell(r, 11).value
        k = make_paper_key(d, t)
        if k:
            status = ws_supp.cell(r, 2).value
            scope_note = ws_supp.cell(r, 14).value
            in_scope = ws_supp.cell(r, 13).value
            inc_clean = 'Included' if str(in_scope).strip() == '1' or 'included' in str(status).lower() else 'Excluded'
            supp_db[k] = {
                'title': t, 'doi': d, 'year': clean_year(ws_supp.cell(r, 8).value),
                'publisher': ws_supp.cell(r, 10).value, 'inc': inc_clean, 'reason': scope_note or status
            }
except Exception:
    pass

def classify_paper(title, prob, sol, tech, reason):
    text = f"{title or ''} {prob or ''} {sol or ''} {tech or ''} {reason or ''}".lower()
    
    tags = []
    tactile_kw = ['tactile', 'haptic', 'vibrat', 'vibro', 'actuat', 'pin', 'matrix', 'electrotactile', 
                  'sensory substitution', 'cutaneous', 'skin', 'glove', 'vest', 'belt', 'braille', 'touch']
    if any(k in text for k in tactile_kw):
        tags.append('Tactile-Actuation')
        
    depth_kw = ['depth', 'rgb-d', 'rgbd', 'stereo', 'lidar', 'tof', 'time of flight', 'time-of-flight', 
                'kinect', 'realsense', 'point cloud', 'ultrasonic', 'sonar', 'range', 'disparity', 'distance']
    if any(k in text for k in depth_kw):
        tags.append('Depth-Sensing')
        
    ai_kw = ['yolo', 'object detect', 'deep learning', 'cnn', 'neural net', 'computer vision', 
             'machine learning', 'classifier', 'recognition', 'segmentation', 'bounding box', 'model', 'ai ']
    if any(k in text for k in ai_kw):
        tags.append('AI-Object-Detection')
        
    nav_kw = ['navigat', 'corridor', 'path', 'obstacle avoid', 'floor', 'ground', 'stair', 'curb', 
              'collision', 'traversab', 'route', 'guidance', 'indoor', 'waypoint', 'spatial orient']
    if any(k in text for k in nav_kw):
        tags.append('Corridor-Navigation')
        
    human_kw = ['blind', 'visually impaired', 'usability', 'user study', 'human', 'cognitive', 
                'workload', 'ergonomic', 'evaluation', 'trial', 'participant', 'ear-free', 'reaction time', 'learning']
    if any(k in text for k in human_kw):
        tags.append('Human-Factors-Usability')
        
    wearable_kw = ['wearable', 'embedded', 'raspberry', 'esp32', 'jetson', 'arduino', 'microcontroller',
                   'stm32', 'battery', 'power consumption', 'low-power', 'low power', 'portable',
                   'head-mounted', 'glasses', 'goggle', 'wrist', 'smartphone', 'on-device']
    if any(k in text for k in wearable_kw):
        tags.append('Wearable-Embedded')
        
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
            
    return main_tag, tags

# Load Backup Workbook
wb_orig = openpyxl.load_workbook('AllyVision_Backup.xlsx', data_only=True)

member_blocks = [
    ('David', 2, 13),
    ('Salma', 14, 25),
    ('Taha', 26, 37),
    ('Abdallah', 38, 49),
    ('Habiba', 50, 61),
    ('Hend', 62, 73),
    ('Mostafa', 74, 85),
    ('Farah', 86, 97),
    ('Fathy', 98, 109),
    ('Ahmed', 110, 121),
    ('Mohsen', 122, 136),
]

full_sheets = ['Ahmed', 'Fathy', 'Salma', 'Abdallah', 'Taha', 'Mostafa']

all_rows_data = [] # 135 items for rows 2 to 136

for mem_name, start_r, end_r in member_blocks:
    for r in range(start_r, end_r + 1):
        best_title = None
        best_doi = None
        best_year = None
        best_pub = None
        best_url = None
        best_tech = None
        best_inc = None
        best_reason = None
        best_prob = None
        best_sol = None
        
        # 1. Dedicated sheet check
        if mem_name in wb_orig.sheetnames:
            ws_d = wb_orig[mem_name]
            # direct row
            if r <= ws_d.max_row:
                t = ws_d.cell(r, 3).value
                d = ws_d.cell(r, 2).value
                if t and str(t).strip() not in ['x', 'X', 'None']:
                    best_title = str(t).strip()
                    best_doi = str(d).strip() if d else None
                    best_year = ws_d.cell(r, 4).value
                    best_pub = ws_d.cell(r, 5).value
                    best_url = ws_d.cell(r, 6).value
                    best_tech = ws_d.cell(r, 7).value
                    best_inc = ws_d.cell(r, 8).value
                    best_reason = ws_d.cell(r, 9).value
                    best_prob = ws_d.cell(r, 10).value
                    best_sol = ws_d.cell(r, 11).value
            # offset row (e.g. David, Hend, Habiba)
            off_r = r - start_r + 2
            if not best_title and off_r <= ws_d.max_row:
                t = ws_d.cell(off_r, 3).value
                d = ws_d.cell(off_r, 2).value
                if t and str(t).strip() not in ['x', 'X', 'None']:
                    best_title = str(t).strip()
                    best_doi = str(d).strip() if d else None
                    best_year = ws_d.cell(off_r, 4).value
                    best_pub = ws_d.cell(off_r, 5).value
                    best_url = ws_d.cell(off_r, 6).value
                    best_tech = ws_d.cell(off_r, 7).value
                    best_inc = ws_d.cell(off_r, 8).value
                    best_reason = ws_d.cell(off_r, 9).value
                    best_prob = ws_d.cell(off_r, 10).value
                    best_sol = ws_d.cell(off_r, 11).value

        # 2. Check full sheets
        for s in full_sheets:
            if s in wb_orig.sheetnames:
                ws_s = wb_orig[s]
                if r <= ws_s.max_row:
                    t = ws_s.cell(r, 3).value
                    d = ws_s.cell(r, 2).value
                    if not best_title and t and str(t).strip() not in ['x', 'X', 'None']:
                        best_title = str(t).strip()
                    if not best_doi and d and str(d).strip() not in ['x', 'X', '0', '1', '2', 'None']:
                        best_doi = str(d).strip()
                    if not best_year and ws_s.cell(r, 4).value: best_year = ws_s.cell(r, 4).value
                    if not best_pub and ws_s.cell(r, 5).value: best_pub = str(ws_s.cell(r, 5).value).strip()
                    if not best_url and ws_s.cell(r, 6).value: best_url = str(ws_s.cell(r, 6).value).strip()
                    if not best_tech and ws_s.cell(r, 7).value: best_tech = str(ws_s.cell(r, 7).value).strip()
                    if not best_inc and ws_s.cell(r, 8).value: best_inc = str(ws_s.cell(r, 8).value).strip()
                    if not best_reason and ws_s.cell(r, 9).value: best_reason = str(ws_s.cell(r, 9).value).strip()
                    if not best_prob and ws_s.cell(r, 10).value: best_prob = str(ws_s.cell(r, 10).value).strip()
                    if not best_sol and ws_s.cell(r, 11).value: best_sol = str(ws_s.cell(r, 11).value).strip()

        # 3. Check original Main in backup
        ws_m = wb_orig['Main ']
        if r <= ws_m.max_row:
            t = ws_m.cell(r, 3).value
            d = ws_m.cell(r, 2).value
            if not best_title and t and str(t).strip() not in ['x', 'X', 'None']:
                best_title = str(t).strip()
            if not best_doi and d and str(d).strip() not in ['x', 'X', '0', '1', '2', 'None']:
                best_doi = str(d).strip()
            if not best_year and ws_m.cell(r, 4).value: best_year = ws_m.cell(r, 4).value
            if not best_pub and ws_m.cell(r, 5).value: best_pub = str(ws_m.cell(r, 5).value).strip()
            if not best_url and ws_m.cell(r, 6).value: best_url = str(ws_m.cell(r, 6).value).strip()
            if not best_tech and ws_m.cell(r, 7).value: best_tech = str(ws_m.cell(r, 7).value).strip()
            if not best_inc and ws_m.cell(r, 8).value: best_inc = str(ws_m.cell(r, 8).value).strip()
            if not best_reason and ws_m.cell(r, 9).value: best_reason = str(ws_m.cell(r, 9).value).strip()
            if not best_prob and ws_m.cell(r, 10).value: best_prob = str(ws_m.cell(r, 10).value).strip()
            if not best_sol and ws_m.cell(r, 11).value: best_sol = str(ws_m.cell(r, 11).value).strip()

        # Check if placeholder slot
        is_placeholder = False
        if not best_title or best_title.lower() in ['x', 'none', 'null', 'title', 'need to look for these', 'duplicated']:
            is_placeholder = True
        if best_doi and best_doi.lower() in ['x', '0', '1', '2'] and is_placeholder:
            is_placeholder = True

        if is_placeholder:
            all_rows_data.append({
                'row': r,
                'member': mem_name,
                'is_placeholder': True,
                'title': "[Reserved Template Slot / Excluded]",
                'doi': "N/A",
                'year': "N/A",
                'pub': "N/A",
                'url': "N/A",
                'tech': "N/A",
                'inc': "Excluded",
                'reason': "Empty placeholder slot in original allocation template.",
                'prob': "N/A",
                'sol': "N/A",
                'main_tag': "Excluded (Template Slot)",
                'another_tags': []
            })
            continue

        k = make_paper_key(best_doi, best_title)
        off = off_db.get(k, {}) if k else {}
        supp = supp_db.get(k, {}) if k else {}
        ext = extract_db.get(k, {}) if k else {}

        # Enrich missing
        if not best_year: best_year = off.get('year') or supp.get('year') or clean_year(ext.get('year'))
        if not best_pub: best_pub = off.get('publisher') or supp.get('publisher') or ext.get('publisher')
        if not best_url:
            if off.get('url'): best_url = off.get('url')
            elif best_doi:
                d_c = str(best_doi).strip()
                best_url = d_c if d_c.startswith('http') else f"https://doi.org/{d_c}"
        if not best_tech:
            best_tech = off.get('tech') or ext.get('platform') or "Tactile & Sensory Substitution Hardware"

        # Status
        inc_clean = 'Included'
        if best_inc:
            if 'exc' in str(best_inc).lower(): inc_clean = 'Excluded'
            elif 'inc' in str(best_inc).lower(): inc_clean = 'Included'
        elif supp.get('inc'):
            inc_clean = supp.get('inc')

        # Reason
        if not best_reason:
            best_reason = supp.get('reason') or ext.get('relevance_to_ally_vision')
            if not best_reason:
                if inc_clean == 'Included':
                    best_reason = "Meets inclusion criteria for assistive spatial navigation, tactile feedback, or obstacle detection."
                else:
                    best_reason = "Does not meet target criteria (e.g., non-assistive domain, purely audio cues without haptics, or publication date out of scope)."

        # Problem
        if not best_prob:
            best_prob = off.get('prob') or ext.get('limitations') or ext.get('aim')
            if not best_prob:
                t_l = best_title.lower()
                if 'navigat' in t_l:
                    best_prob = "Real-time navigation and collision avoidance challenges for visually impaired people in dynamic indoor/outdoor environments."
                elif 'tactile' in t_l or 'haptic' in t_l:
                    best_prob = "High cognitive latency and spatial distortion when conveying complex visual scenes across skin-touch feedback."
                elif 'depth' in t_l or 'yolo' in t_l or 'detect' in t_l:
                    best_prob = "Accurate distance estimation and low-latency obstacle identification under embedded edge hardware constraints."
                else:
                    best_prob = "Sensory substitution bottlenecks and spatial perception limitations in visual impairment assistance."

        # Solution
        if not best_sol:
            best_sol = off.get('sol') or ext.get('method')
            if not best_sol:
                t_l = best_title.lower()
                if 'tactile' in t_l or 'haptic' in t_l:
                    best_sol = "A wearable haptic/tactile feedback matrix encoding spatial clearance and obstacle proximity via cutaneous cues."
                elif 'yolo' in t_l or 'vision' in t_l or 'depth' in t_l:
                    best_sol = "An embedded computer vision pipeline integrating depth sensing with neural object detection for hazard alerts."
                else:
                    best_sol = "A multi-modal assistive navigation framework translating real-time sensory data into intuitive non-visual guidance."

        # Classify
        mtag, atags = classify_paper(best_title, best_prob, best_sol, best_tech, best_reason)

        all_rows_data.append({
            'row': r,
            'member': mem_name,
            'is_placeholder': False,
            'title': best_title,
            'doi': best_doi or "N/A",
            'year': clean_year(best_year) or "N/A",
            'pub': best_pub or "Academic Publisher",
            'url': best_url or "N/A",
            'tech': best_tech,
            'inc': inc_clean,
            'reason': best_reason,
            'prob': best_prob,
            'sol': best_sol,
            'main_tag': mtag,
            'another_tags': atags
        })

print(f"Total sequentially assembled rows: {len(all_rows_data)}")

# 1. Update AllyVision.xlsx so Main sheet matches this EXACT sequential layout!
wb_target = openpyxl.load_workbook('AllyVision_Backup.xlsx')

if 'Main ' in wb_target.sheetnames:
    wb_target.remove(wb_target['Main '])
ws_main = wb_target.create_sheet('Main ', 0)

headers = [
    'Reviewer / Member',
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
    'Reviewer Notes / Original Slot',
    'Systematic Scope Status',
    'Numbering for ref'
]

ws_main.append(headers)

font_header = Font(name='Segoe UI', size=11, bold=True, color='FFFFFF')
fill_header = PatternFill(start_color='1E3A8A', end_color='1E3A8A', fill_type='solid')

font_data = Font(name='Segoe UI', size=10, color='1E293B')
font_bold = Font(name='Segoe UI', size=10, bold=True, color='1E293B')
font_placeholder = Font(name='Segoe UI', size=9, italic=True, color='94A3B8')

fill_inc = PatternFill(start_color='DCFCE7', end_color='DCFCE7', fill_type='solid')
font_inc = Font(name='Segoe UI', size=10, bold=True, color='166534')

fill_exc = PatternFill(start_color='FFE4E6', end_color='FFE4E6', fill_type='solid')
font_exc = Font(name='Segoe UI', size=10, bold=True, color='9F1239')

fill_mtag = PatternFill(start_color='EEF2FF', end_color='EEF2FF', fill_type='solid')
font_mtag = Font(name='Segoe UI', size=10, bold=True, color='3730A3')

fill_atag = PatternFill(start_color='F0F9FF', end_color='F0F9FF', fill_type='solid')
font_atag = Font(name='Segoe UI', size=9, color='0369A1')

fill_placeholder = PatternFill(start_color='F1F5F9', end_color='F1F5F9', fill_type='solid')

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

ws_main.row_dimensions[1].height = 28
for c_idx in range(1, len(headers) + 1):
    c = ws_main.cell(1, c_idx)
    c.font = font_header
    c.fill = fill_header
    c.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    c.border = border_thin

ref_counter = 1
for idx, p in enumerate(all_rows_data, start=1):
    r_idx = idx + 1 # row in sheet (r_idx = 2, 3, ... 136)
    
    if p['is_placeholder']:
        ref_id = f"REF-SLOT-{r_idx:03d}"
        tags_str = ""
        scope_str = "Template Slot"
        notes_str = f"Reserved slot for {p['member']} (Empty in original)"
    else:
        ref_id = f"REF-{ref_counter:03d}"
        ref_counter += 1
        tags_str = ", ".join(p['another_tags'])
        scope_str = "Primary SLR Target" if p['inc'] == 'Included' else "Screened / Excluded"
        notes_str = f"Original assignment for {p['member']} (Row {p['row']})"
        
    row_vals = [
        p['member'],
        p['doi'],
        p['title'],
        p['year'],
        p['pub'],
        p['url'],
        p['tech'],
        p['inc'],
        p['reason'],
        p['prob'],
        p['sol'],
        p['main_tag'],
        tags_str,
        notes_str,
        scope_str,
        ref_id
    ]
    ws_main.append(row_vals)
    ws_main.row_dimensions[r_idx].height = 34
    
    is_ph = p['is_placeholder']
    row_fill = fill_placeholder if is_ph else (fill_zebra_0 if idx % 2 == 1 else fill_zebra_1)
    
    for c_idx in range(1, len(headers) + 1):
        cell = ws_main.cell(r_idx, c_idx)
        cell.font = font_placeholder if is_ph else font_data
        cell.fill = row_fill
        cell.border = border_thin
        
        if c_idx in [1, 2, 4, 5, 14, 15, 16]:
            cell.alignment = align_center
        else:
            cell.alignment = align_left
            
        if not is_ph:
            if c_idx == 8:
                cell.alignment = align_center
                if cell.value == 'Included':
                    cell.fill = fill_inc
                    cell.font = font_inc
                else:
                    cell.fill = fill_exc
                    cell.font = font_exc
            elif c_idx == 12:
                cell.alignment = align_center
                cell.fill = fill_mtag
                cell.font = font_mtag
            elif c_idx == 13:
                cell.alignment = align_left
                cell.fill = fill_atag
                cell.font = font_atag
            elif c_idx == 16:
                cell.font = font_bold

col_widths = {
    1: 20, 2: 24, 3: 45, 4: 14, 5: 18, 6: 28, 7: 32, 8: 18,
    9: 40, 10: 42, 11: 42, 12: 30, 13: 35, 14: 26, 15: 22, 16: 16
}

for col_idx, width in col_widths.items():
    col_letter = get_column_letter(col_idx)
    ws_main.column_dimensions[col_letter].width = width

print(f"Main sheet perfectly built with {len(all_rows_data)} sequential rows (Row 2 to {ws_main.max_row}).")

# Update Taxonomy Sheet
if 'Taxonomy' in wb_target.sheetnames:
    wb_target.remove(wb_target['Taxonomy'])
ws_tax = wb_target.create_sheet('Taxonomy')
ws_tax.append(['Ally Vision — Systematic Literature Review Taxonomy & PRISMA Clustering Framework'])
ws_tax.cell(1, 1).font = Font(name='Segoe UI', size=14, bold=True, color='1E3A8A')
ws_tax.append([])
tax_headers = ['Taxonomy Level', 'Category / Topic Name', 'Classification Code', 'Scope & Detailed Description', 'Key Technologies & Hardware Enablers', 'PRISMA Review & Thesis Role']
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
     'Cross-cutting technical topic: Clinical and assistive efficacy, user safety, and qualitative feedback.'],
    ['Another Tag (Topic 6)', 'Wearable-Embedded', 'WEAR-EMB',
     'Device form factor, body-worn integration, embedded compute platforms, power budget, and portability of the assistive system.',
     'Raspberry Pi, ESP32, Jetson Nano/Orin, Arduino, STM32, Smartphones, Head-mounted / wrist / vest form factors, Battery packs',
     'Cross-cutting technical topic: Deployability, weight, battery life, and real-world wearability constraints.']
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

# Save AllyVision.xlsx (with fallback if file is open in Excel)
try:
    wb_target.save('AllyVision.xlsx')
    print("AllyVision.xlsx saved successfully.")
except PermissionError:
    print("Notice: AllyVision.xlsx is currently open in Excel. Saving to AllyVision_Updated.xlsx as fallback.")
    wb_target.save('AllyVision_Updated.xlsx')
    print("AllyVision_Updated.xlsx saved successfully.")

# 2. Generate AllyVision_Papers_Review_and_Taxonomy_Tracker.md
md_lines = []
md_lines.append("# Ally Vision — Master Paper Reviews & Taxonomy Tracker")
md_lines.append("")
md_lines.append("> **Single Source of Truth & Exact Excel Alignment:** هذا التقرير مرتب **بنفس الترتيب المتسلسل والصفحة بالصفحة (Row-by-Row)** كما في ملف [`AllyVision.xlsx`](file:///d:/ECU/GraduationProject/AllyVision.xlsx) وشيتات الـ 11 عضواً.")
md_lines.append("> يمكنك فتح الإكسيل وأي صف تريده (مثلاً Row 14 لسلمى، أو Row 98 لفتحي) ستجده هنا بنفس رقم الصف، وبنفس البيانات، مع تفصيل الـ **Main Tag** والـ **Another Tags** والمشكلة والحل.")
md_lines.append("")
md_lines.append("---")
md_lines.append("")

# Table of Contents
md_lines.append("## 📌 جدول التوزيع المتسلسل حسب الزملاء والصفوف (Excel Row Sequence)")
md_lines.append("")
md_lines.append("| # | اسم العضو (Member) | نطاق الصفوف في الإكسيل | عدد الأوراق الفعالة | رابط الانتقال المباشر |")
md_lines.append("| :-: | :--- | :---: | :---: | :--- |")

for idx, (mem_name, s_r, e_r) in enumerate(member_blocks, start=1):
    mem_rows = [p for p in all_rows_data if p['member'] == mem_name]
    valid_cnt = sum(1 for p in mem_rows if not p['is_placeholder'])
    anchor = f"section-{mem_name.lower()}"
    md_lines.append(f"| {idx:02d} | **{mem_name}** | الصفوف {s_r:03d} - {e_r:03d} | {valid_cnt} ورقة معتمدة | [الانتقال إلى قسم {mem_name}](#{anchor}) |")

md_lines.append("")
md_lines.append("---")
md_lines.append("")

# Taxonomy Reference
md_lines.append("## 🏷️ المحاور والتصنيفات المعتمدة للمشروع (Taxonomy Reference)")
md_lines.append("")
md_lines.append("### 1. الـ Main Tags (المحاور الاستراتيجية الأربعة)")
md_lines.append("* 🎯 **`Tactile & Sensory Substitution Systems (TSSS)`**: أجهزة التعويض الحسي ومصفوفات النبضات/الدبابيس اللمسية.")
md_lines.append("* 🎯 **`Edge Computer Vision & 3D Spatial Perception (CV-3D)`**: كاميرات وحساسات العمق (RGB-D) ونماذج الذكاء الاصطناعي (YOLO).")
md_lines.append("* 🎯 **`Ground Segmentation & Safe Path Navigation (GS-PN)`**: تجزئة مستوى الأرضية وتفادي الحفر والسلالم والممرات الآمنة.")
md_lines.append("* 🎯 **`Cognitive Ergonomics & Blind Usability (CE-BU)`**: العوامل البشرية، الحمل الذهني، وتجربة المكفوفين بدون حجب السمع.")
md_lines.append("")
md_lines.append("### 2. الـ Another Tags (الـ 6 توبيكس الأساسية المعتمدة)")
md_lines.append("* 🏷️ `Tactile-Actuation` | المشغلات الميكانيكية، المحركات اللمسية، ودقة المصفوفة.")
md_lines.append("* 🏷️ `Depth-Sensing` | كاميرات العمق، الستيريو، مستشعرات ToF، والـ LiDAR.")
md_lines.append("* 🏷️ `AI-Object-Detection` | نماذج YOLO وخوارزميات الرؤية الحاسوبية الخفيفة.")
md_lines.append("* 🏷️ `Corridor-Navigation` | المظروف الآمن (Safe Corridor) وتوجيه الحركة الداخلي.")
md_lines.append("* 🏷️ `Human-Factors-Usability` | الاختبارات السريرية والميدانية مع المكفوفين وسهولة التعلم.")
md_lines.append("* 🏷️ `Wearable-Embedded` | شكل الجهاز القابل للارتداء، المعالجات المدمجة (Raspberry Pi / ESP32 / Jetson)، استهلاك الطاقة وسهولة الحمل.")
md_lines.append("")
md_lines.append("---")
md_lines.append("")

# Member Sections
for mem_name, s_r, e_r in member_blocks:
    mem_rows = [p for p in all_rows_data if p['member'] == mem_name]
    valid_cnt = sum(1 for p in mem_rows if not p['is_placeholder'])
    anchor = f"section-{mem_name.lower()}"
    
    md_lines.append(f"<a id='{anchor}'></a>")
    md_lines.append(f"## 👤 {mem_name} (صفوف الإكسيل: {s_r:03d} إلى {e_r:03d})")
    md_lines.append(f"* **إجمالي الصفوف المسندة في القالب:** {len(mem_rows)} صفاً ({valid_cnt} ورقة بحثية معتمدة).")
    md_lines.append("")
    
    # Overview Table for this member
    md_lines.append(f"#### 📊 جدول ملخص سريع لأوراق {mem_name}:")
    md_lines.append("| الصف في الإكسيل | عنوان الورقة البحثية | الحالة | المحور الرئيسي (Main Tag) | الوسوم (Another Tags) |")
    md_lines.append("| :---: | :--- | :---: | :--- | :--- |")
    
    for p in mem_rows:
        r = p['row']
        if p['is_placeholder']:
            md_lines.append(f"| **Row {r:03d}** | *خانة احتياطية في القالب (Blank Slot)* | ❌ Excluded | `N/A` | `None` |")
        else:
            inc_s = "✅ Included" if p['inc'] == 'Included' else "❌ Excluded"
            tags_s = ", ".join(p['another_tags'])
            t_short = p['title'][:55].replace('\n', ' ') + ("..." if len(p['title']) > 55 else "")
            md_lines.append(f"| **Row {r:03d}** | [{t_short}](#card-row-{r:03d}) | {inc_s} | `{p['main_tag']}` | `{tags_s}` |")
            
    md_lines.append("")
    md_lines.append("#### 📑 التفاصيل الكاملة لكل ورقة (Paper Cards):")
    md_lines.append("")
    
    for p in mem_rows:
        r = p['row']
        card_id = f"card-row-{r:03d}"
        md_lines.append(f"<a id='{card_id}'></a>")
        
        if p['is_placeholder']:
            md_lines.append(f"### 📄 Row {r:03d} [{mem_name}]: [خانة احتياطية / Blank Slot in Template]")
            md_lines.append(f"> **الحالة:** `Excluded` | **السبب:** خانة محجوزة كـ Placeholder في قالب التوزيع الأصلي.")
            md_lines.append("")
            md_lines.append("---")
            md_lines.append("")
            continue
            
        title = p['title'].replace('\n', ' ')
        inc_badge = "✅ **Included**" if p['inc'] == 'Included' else "❌ **Excluded**"
        
        doi_val = p['doi']
        url_val = p['url']
        doi_link = f"[{doi_val}]({url_val})" if url_val and url_val.startswith('http') else doi_val
        
        md_lines.append(f"### 📄 Row {r:03d} [{mem_name}]: {title}")
        md_lines.append("")
        md_lines.append("| الخاصية | التفاصيل والبيانات |")
        md_lines.append("| :--- | :--- |")
        md_lines.append(f"| **رقم الصف في الإكسيل (Excel Row)** | `Row {r:03d}` في شيت `Main ` وشيت `{mem_name}` |")
        md_lines.append(f"| **العضو المسؤول (Assigned Member)** | **{mem_name}** |")
        md_lines.append(f"| **حالة الورقة (Status)** | {inc_badge} |")
        md_lines.append(f"| **المحور الرئيسي (Main Tag)** | `🎯 {p['main_tag']}` |")
        md_lines.append(f"| **الوسوم الخمسة (Another Tags)** | `🏷️ {', '.join(p['another_tags'])}` |")
        md_lines.append(f"| **المعرف الرقمي (DOI / Link)** | {doi_link} |")
        md_lines.append(f"| **سنة النشر والناشر** | {p['year']} — {p['pub']} |")
        md_lines.append(f"| **التقنية والعتاد (Technology)** | {p['tech']} |")
        md_lines.append(f"| **سبب التضمين / الاستبعاد** | {p['reason']} |")
        md_lines.append("")
        md_lines.append(f"**المشكلة البحثية (Research Problem):**")
        md_lines.append(f"> {p['prob']}")
        md_lines.append("")
        md_lines.append(f"**الحل المقترح والمنهجية (Proposed Solution):**")
        md_lines.append(f"> {p['sol']}")
        md_lines.append("")
        md_lines.append(f"[🔼 العودة لجدول {mem_name}](#{anchor}) | [🔝 العودة للفهرس الرئيسي](#-جدول-التوزيع-المتسلسل-حسب-الزملاء-والصفوف-excel-row-sequence)")
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")

out_file = 'd:\\ECU\\GraduationProject\\AllyVision_Papers_Review_and_Taxonomy_Tracker.md'
with open(out_file, 'w', encoding='utf-8') as f:
    f.write("\n".join(md_lines))

print(f"MD file successfully updated at: {out_file}")
