import openpyxl, re, json, sys, os

sys.stdout.reconfigure(encoding='utf-8')

print("Generating AllyVision_Papers_Review_and_Taxonomy_Tracker.md...")

from verify_member_blocks import processed_members

md_lines = []

# Title & Header
md_lines.append("# Ally Vision — Master Systematic Paper Reviews & Taxonomy Tracker")
md_lines.append("")
md_lines.append("> **Single Source of Truth:** هذا المستند يُمثّل المرجع الشامل والمفصل لكافة الأوراق البحثية الموزعة على أعضاء الفريق الـ 11 بالترتيب الدقيق المطابق لصفوف ملف الإكسيل [`AllyVision.xlsx`](file:///d:/ECU/GraduationProject/AllyVision.xlsx).")
md_lines.append("> كل ورقة تم فحصها، وتحديد حالتها (`Included` / `Excluded`)، وربطها بـ **Main Tag** (من بين 4 محاور استراتيجية) و **Another Tags** (من بين الـ 5 مواضيع التقنية المعتمدة للمشروع) لتسهيل تصنيف الـ PRISMA Flow وكتابة الـ Systematic Literature Review Paper.")
md_lines.append("")
md_lines.append("---")
md_lines.append("")

# Taxonomy Summary Guide
md_lines.append("## 🏷️ دليل نظام التصنيف المعتمد (Taxonomy & PRISMA Guide)")
md_lines.append("")
md_lines.append("### 1. الـ Main Tags (المحاور الاستراتيجية الأربعة الكبرى)")
md_lines.append("| المحور الرئيسي (Main Tag) | الكود | النطاق والمجال البحثي | دور المحور في ورقة الـ Review والـ PRISMA |")
md_lines.append("| :--- | :---: | :--- | :--- |")
md_lines.append("| **Tactile & Sensory Substitution Systems** | `TSSS` | أجهزة التعويض الحسي ومصفوفات النبضات اللمسية (Actuator Matrices / Haptics / Micro-pins). | دراسة وسائط الإخراج اللمسي، دقة المصفوفات، وزمن الاستجابة الحسي. |")
md_lines.append("| **Edge Computer Vision & 3D Spatial Perception** | `CV-3D` | كاميرات وحساسات العمق (RGB-D / ToF / LiDAR) وخوارزميات الرؤية الحاسوبية على الحافة (Edge AI / YOLO). | دراسة دقة الإدراك المكاني ثلاثي الأبعاد واكتشاف العوائق ومعدل الإطارات (FPS). |")
md_lines.append("| **Ground Segmentation & Safe Path Navigation** | `GS-PN` | خوارزميات تجزئة مستوى الأرضية (Floor Plane / RANSAC) واكتشاف السلالم والانحدارات والممرات الآمنة. | دراسة أمان الحركة الفيزيائية وتفادي السقوط وتخطيط المسارات الحرة. |")
md_lines.append("| **Cognitive Ergonomics & Blind Usability** | `CE-BU` | العوامل البشرية، الحمل الذهني (NASA-TLX)، والحفاظ على السمع الحر (Ear-free Navigation)، وتجارب المكفوفين. | قياس كفاءة الاستخدام السريري والميداني، وسهولة التدريب والتكيف. |")
md_lines.append("")

md_lines.append("### 2. الـ Another Tags (الـ 5 توبيكس الأساسية المعتمدة لكامل المشروع)")
md_lines.append("| الموضوع المعتمد (Controlled Topic) | الكود | التوصيف والتقنيات التمثيلية |")
md_lines.append("| :--- | :---: | :--- |")
md_lines.append("| `Tactile-Actuation` | `TACT` | المشغلات الميكانيكية، المحركات اللمسية (ERM/LRA)، الدبابيس الخطية، تردد النبضات، وقوة التحفيز. |")
md_lines.append("| `Depth-Sensing` | `DEPTH` | استشعار المدى والعمق، كاميرات الستيريو، كاميرات RealSense، مستشعرات ToF، والـ LiDAR. |")
md_lines.append("| `AI-Object-Detection` | `AI-OD` | نماذج الذكاء الاصطناعي (YOLOv8/v11, CNNs)، الشبكات العصبية الخفيفة، وكشف العوائق الديناميكية. |")
md_lines.append("| `Corridor-Navigation` | `CORR-NAV` | المظروف الآمن (Safe Corridor Envelope)، تتبع المسار الداخلي، وتوجيه الحركة الحركي. |")
md_lines.append("| `Human-Factors-Usability` | `HUMAN-UX` | الاختبارات الميدانية مع المكفوفين، زمن الاستجابة، منحنى التعلم، وتفادي الإجهاد الحسي. |")
md_lines.append("")
md_lines.append("---")
md_lines.append("")

# Quick Navigation Index
md_lines.append("## 📌 فهرس الوصول السريع حسب توزيع الزملاء (Quick Navigation Index)")
md_lines.append("")
md_lines.append("| # | اسم الزميل (Team Member) | نطاق الصفوف في الإكسيل | عدد الأوراق الفعالة | رابط الانتقال السريع |")
md_lines.append("| :-: | :--- | :---: | :---: | :--- |")

for idx, (mem_name, start_r, end_r, papers) in enumerate(processed_members, start=1):
    valid_cnt = sum(1 for p in papers if not p.get('is_placeholder'))
    anchor = f"section-{mem_name.lower().strip()}"
    md_lines.append(f"| {idx} | **{mem_name}** | الصفوف {start_r} - {end_r} | {valid_cnt} ورقة | [الانتقال إلى قسم {mem_name}](#{anchor}) |")

md_lines.append("")
md_lines.append("---")
md_lines.append("")

# Detailed Sections
for mem_name, start_r, end_r, papers in processed_members:
    anchor = f"section-{mem_name.lower().strip()}"
    valid_papers = [p for p in papers if not p.get('is_placeholder')]
    md_lines.append(f"<a id='{anchor}'></a>")
    md_lines.append(f"## 👤 {mem_name} (صفوف الإكسيل: {start_r} إلى {end_r})")
    md_lines.append(f"* **إجمالي الصفوف المسندة في القالب:** {len(papers)} صفاً ({len(valid_papers)} ورقة بحثية معتمدة).")
    md_lines.append("")
    
    for p in papers:
        r = p['row']
        if p.get('is_placeholder'):
            md_lines.append(f"### 📄 Row {r:03d} [{mem_name}]: [خانات احتياطية / Blank Slot in Template]")
            md_lines.append(f"> **الحالة:** `Excluded` | **ملاحظة:** صف فارغ مخصص كخانة احتياطية في قالب الإكسيل الأصلي ولم يُسجل فيه بحث.")
            md_lines.append("")
            continue
            
        title = str(p.get('title') or '').replace('\n', ' ')
        inc_clean = p.get('inc') or 'Included'
        inc_badge = "✅ **Included**" if inc_clean == 'Included' else "❌ **Excluded**"
        
        doi_val = p.get('doi') or 'N/A'
        url_val = p.get('url')
        doi_link = f"[{doi_val}]({url_val})" if url_val and url_val.startswith('http') else (doi_val or 'N/A')
        
        pub_val = p.get('publisher') or p.get('pub') or 'Academic Publisher'
        year_val = p.get('year') or 'N/A'
        tech_val = p.get('tech') or 'Sensory substitution hardware'
        
        tags_list = p.get('another_tags') or []
        if isinstance(tags_list, list):
            tags_str = ", ".join(tags_list)
        else:
            tags_str = str(tags_list)
            
        md_lines.append(f"### 📄 Row {r:03d} [{mem_name}]: {title}")
        md_lines.append("")
        md_lines.append("| الخاصية | التفاصيل والبيانات |")
        md_lines.append("| :--- | :--- |")
        md_lines.append(f"| **حالة الورقة (Status)** | {inc_badge} |")
        md_lines.append(f"| **المحور الرئيسي (Main Tag)** | `🎯 {p.get('main_tag')}` |")
        md_lines.append(f"| **الوسوم الخمسة (Another Tags)** | `🏷️ {tags_str}` |")
        md_lines.append(f"| **المعرف الرقمي (DOI / Link)** | {doi_link} |")
        md_lines.append(f"| **سنة النشر والناشر** | {year_val} — {pub_val} |")
        md_lines.append(f"| **التقنية والعتاد (Technology)** | {tech_val} |")
        md_lines.append(f"| **سبب التضمين / الاستبعاد** | {p.get('reason')} |")
        md_lines.append("")
        md_lines.append(f"**المشكلة البحثية (Research Problem):**")
        md_lines.append(f"> {p.get('prob')}")
        md_lines.append("")
        md_lines.append(f"**الحل المقترح والمنهجية (Proposed Solution):**")
        md_lines.append(f"> {p.get('sol')}")
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")

output_md_path = 'd:\\ECU\\GraduationProject\\AllyVision_Papers_Review_and_Taxonomy_Tracker.md'
with open(output_md_path, 'w', encoding='utf-8') as f:
    f.write("\n".join(md_lines))

print(f"File successfully created: {output_md_path}")
print(f"Total lines written: {len(md_lines)}")
