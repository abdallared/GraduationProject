import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

def build_tracker():
    wb = openpyxl.Workbook()
    
    # -------------------------------------------------------------------------
    # Styling Palette: Deep Slate Navy, Crisp Borders, Tech Colors
    # -------------------------------------------------------------------------
    font_family = "Segoe UI"
    
    header_fill = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid") # Slate 900
    header_font = Font(name=font_family, size=10, bold=True, color="FFFFFF")
    
    title_font = Font(name=font_family, size=15, bold=True, color="0F172A")
    subtitle_font = Font(name=font_family, size=9, italic=True, color="475569")
    section_font = Font(name=font_family, size=11, bold=True, color="1E293B")
    
    reg_font = Font(name=font_family, size=9, color="0F172A")
    bold_font = Font(name=font_family, size=9, bold=True, color="0F172A")
    link_font = Font(name=font_family, size=9, color="0284C7", underline="single")
    
    zebra_fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
    white_fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
    
    # Status Fills & Fonts
    status_styles = {
        "مفتوحة للتقديم (Open)": (PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid"), Font(name=font_family, size=9, bold=True, color="166534")),
        "لم تفتح بعد - متابعة (Pending)": (PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid"), Font(name=font_family, size=9, bold=True, color="92400E")),
        "قيد التجهيز والمراجعة (In Progress)": (PatternFill(start_color="E0F2FE", end_color="E0F2FE", fill_type="solid"), Font(name=font_family, size=9, bold=True, color="075985")),
        "تم التقديم بنجاح (Submitted)": (PatternFill(start_color="E0E7FF", end_color="E0E7FF", fill_type="solid"), Font(name=font_family, size=9, bold=True, color="3730A3")),
    }
    
    # Priority Fills
    prio_vhigh = (PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid"), Font(name=font_family, size=9, bold=True, color="991B1B"))
    prio_high  = (PatternFill(start_color="FFEDD5", end_color="FFEDD5", fill_type="solid"), Font(name=font_family, size=9, bold=True, color="9A3412"))
    prio_med   = (PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid"), Font(name=font_family, size=9, bold=True, color="334155"))
    
    thin_side = Side(border_style="thin", color="CBD5E1")
    border = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)
    
    align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
    align_left = Alignment(horizontal="left", vertical="center", wrap_text=True)
    align_right = Alignment(horizontal="right", vertical="center", wrap_text=True)

    # =========================================================================
    # SHEET 1: Master Competitions Tracker (متابعة المسابقات الـ 26)
    # =========================================================================
    ws1 = wb.active
    ws1.title = "متابعة المسابقات (Tracker)"
    ws1.views.sheetView[0].showGridLines = True
    
    # Titles
    ws1.merge_cells("A1:L1")
    ws1["A1"] = "Ally Vision — Master Competitions & Grants Live Tracker (2026 / 2027)"
    ws1["A1"].font = title_font
    ws1["A1"].alignment = Alignment(horizontal="left", vertical="center")
    
    ws1.merge_cells("A2:L2")
    ws1["A2"] = "شيت المتابعة التفاعلي الشامل لجميع مسابقات ومنح وحاضنات مشروع تخرج Ally Vision (قابل للإضافة والتعديل المستمر)"
    ws1["A2"].font = subtitle_font
    
    headers1 = [
        "م",
        "اسم المسابقة / البرنامج",
        "الجهة المنظمة",
        "الرابط المباشر",
        "تاريخ فتح التقديم\n(Start Date)",
        "الموعد النهائي\n(Deadline / End)",
        "حالة التقديم الحالية\n(Status)",
        "المستندات والمخرجات المطلوبة للتقديم\n(Required Deliverables)",
        "المسار المناسب لـ Ally Vision\n(Target Track)",
        "حجم التمويل والدعم المتوقع\n(Grants & Prizes)",
        "الأولوية\n(Priority)",
        "خطة التحرك والملاحظات الخاصة بالمشروع\n(Action Plan & Strategy)"
    ]
    
    for c_idx, h in enumerate(headers1, 1):
        cell = ws1.cell(row=4, column=c_idx, value=h)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = align_center
        cell.border = border
    ws1.row_dimensions[4].height = 36

    # Data for the 26 entries from links.txt
    competitions = [
        (
            1,
            "برنامج حاضنة Start-IT",
            "مركز الإبداع التكنولوجي وريادة الأعمال (TIEC / ITIDA)",
            "https://tiec.gov.eg/Arabic/Programs/Start-IT/pages/default.aspx?utm_source=chatgpt.com",
            "مفتوح على دورات ربع سنوية (يناير / أبريل / يوليو / أكتوبر)",
            "دورة الربع الحالي: 30 نوفمبر 2026",
            "مفتوحة للتقديم (Open)",
            "1. عرض تقديمي للمشروع (Pitch Deck 10-12 Slides)\n2. نموذج العمل التجاري (Lean Canvas / BMC)\n3. فيديو توضيحي للنموذج الأولي (Demo Video 2-3 min)\n4. السير الذاتية لأعضاء الفريق والبطاقات القومية",
            "ICT / DeepTech Hardware & Assistive Startups",
            "منحة احتضان نقدية تصل إلى 180,000+ جنيه بدون اقتطاع حصة + مقر عمل سحابي واستشارات قانونية وتسويقية",
            "أولوية قصوى (Very High)",
            "التقديم بـ Ally Vision كشركة ناشئة وليس مجرد مشروع تخرج، والتركيز على نموذج الـ B2B2C ورعايات الـ CSR."
        ),
        (
            2,
            "برنامج الاستثمار لرواد الأعمال (EIP)",
            "EgyptInnovate & أكاديمية البحث العلمي (ASRT)",
            "https://egyptinnovate.com/en/challenge-center/entrepreneurs-investment-program-eip?utm_source=chatgpt.com",
            "مستمر على دفعات سنوية",
            "دفعة 2026: 15 ديسمبر 2026",
            "قيد التجهيز والمراجعة (In Progress)",
            "1. خطة عمل متكاملة (Business Plan Summary)\n2. العرض التقديمي للمستثمرين (Investor Pitch Deck)\n3. دراسة الجدوى وتكلفة الـ BOM والنموذج المالي\n4. فيديو تجربة النموذج الأولي الحقيقي",
            "Assistive Technology & HealthTech Investment Track",
            "فرص ربط مباشر وجلسات استثمار مع صناديق رأس المال الجريء (VCs) وملاك الاستثمار (Angel Investors) لتمويل التوسع",
            "أولوية عالية (High)",
            "استخدام الـ Deck المرفق بالمشروع، والتركيز على حجم السوق الضخم (31.4 مليار دولار) وتكلفة التصنيع التنافسية (<400$)."
        ),
        (
            3,
            "تحدي Meta Open-Weights AI للمطورين",
            "Meta for Developers & Hugging Face",
            "https://www.linkedin.com/posts/meta-for-developers_open-weights-meet-your-favorite-stack-activity-7518735872792428544-o7vM?utm_medium=ios_app&rcm=ACoAAFjgIIsBbj54GaV-16oGSKlVzFkVmXglr9U&utm_source=social_share_send&utm_campaign=copy_link",
            "مفتوح عالمياً عبر LinkedIn و Devpost",
            "الموعد النهائي: 10 ديسمبر 2026",
            "مفتوحة للتقديم (Open)",
            "1. مستودع GitHub عام للكود مع ملف README موثق\n2. فيديو ديمو تجريبي على يوتيوب مدته 3 دقائق\n3. وصف هندسي لكيفية توظيف النماذج مفتوحة الأوزان على الأجهزة الطرفية",
            "Open-Source Edge AI & Multimodal Accessibility",
            "جوائز مالية بالدولار للمراكز الأولى + أرصدة سحابية (Cloud Compute Credits) ودعم فني من مهندسي Meta",
            "أولوية متوسطة (Medium)",
            "التركيز على منظومة الرؤية الطرفية السريعة (Sub-20ms ONNX inference) واستخدام الأدوات مفتوحة المصدر."
        ),
        (
            4,
            "دليل مسابقات الروبوتات والذكاء الاصطناعي في مصر",
            "منصة مصر تبتكر (EgyptInnovate)",
            "https://egyptinnovate.com/articles/%D8%A3%D9%87%D9%85-7-%D9%85%D8%B3%D8%A7%D8%A8%D9%82%D8%A7%D8%AA-%D8%B1%D9%88%D8%A8%D9%88%D8%AA%D8%A7%D8%AA-%D9%84%D9%84%D8%B7%D9%84%D8%A7%D8%A8-%D9%81%D9%8A-%D9%85%D8%B5%D8%B1",
            "دليل دوري سنوي للمسابقات الوطنية",
            "مواعيد متفاوتة خلال العام الدراسي",
            "لم تفتح بعد - متابعة (Pending)",
            "المتطلبات تختلف بحسب كل مسابقة (Minesweepers, ROV, Robocon, ARC, IRC) وتشمل تقريراً هندسياً وعرضاً للروبوت",
            "Robotics, Autonomous Navigation & Assistive Devices",
            "جوائز نقدية من 20,000 إلى 100,000 جنيه + تمثيل مصر في النهائيات العالمية للمسابقات",
            "أولوية عالية (High)",
            "الرجوع للدليل لاقتناص أي مسابقة تنفتح فجأة، خصوصاً مسار الروبوتات الخدمية وتطبيقات خدمة المكفوفين."
        ),
        (
            5,
            "التحدي الدولي للروبوتات (IRC Egypt)",
            "الاتحاد الدولي للروبوتات ومؤسسات الابتكار",
            "https://www.ircrobot.org/ar/",
            "موسم 2026 / 2027",
            "التصفيات المصرية: يناير 2027",
            "لم تفتح بعد - متابعة (Pending)",
            "1. تقرير التصميم الهندسي (Technical Design Report)\n2. فيديو لاختبارات التحرك وتفادي العوائق\n3. إثبات القيد الجامعي للطلاب",
            "Service Robotics & AI Navigation Track",
            "ميداليات وكؤوس رسمية + جوائز مالية للمراكز الأولى + تأهيل لبطولة آسيا للروبوتات",
            "أولوية متوسطة (Medium)",
            "التركيز على الجانب الميكاترونكس لمصفوفة الدبابيس (5x5 Actuator Matrix) ودقة التحكم بمحركات الخطوة."
        ),
        (
            6,
            "مسابقة صندوق رعاية المبتكرين والنوابغ (ISF)",
            "وزارة التعليم العالي والبحث العلمي وصندوق ISF",
            "https://www.facebook.com/share/p/1HLUjVr3yo/",
            "أكتوبر 2026",
            "المرحلة الأولى: 25 نوفمبر 2026",
            "مفتوحة للتقديم (Open)",
            "1. استمارة التسجيل الرسمية في بوابة ISF\n2. المقترح الفني للمشروع وخطة التنفيذ الأكاديمية\n3. موافقة المشرف الأكاديمي والجامعة المصرية الصينية",
            "مسار دعم مشاريع التخرج الابتكارية لطلاب الجامعات",
            "تمويل ودعم مالي مباشر لشراء قطع الهاردوير يصل إلى 50,000 إلى 100,000 جنيه + إرشاد وتوجيه ريادي",
            "أولوية قصوى (Very High)",
            "التقديم الفوري عبر بوابة الصندوق مع خطاب رسمي من كلية الهندسة بالجامعة المصرية الصينية لتسهيل القبول."
        ),
        (
            7,
            "مسابقة مركز الابتكار والريادة (ASU iHub)",
            "جامعة عين شمس & مركز الابتكار iHub",
            "https://www.asu.edu.eg/ar/10290/news",
            "نوفمبر 2026",
            "الموعد النهائي: 20 ديسمبر 2026",
            "قيد التجهيز والمراجعة (In Progress)",
            "1. ملخص المشروع من صفحتين (Executive Summary)\n2. عرض تقديمي للمشروع (Pitch Deck)\n3. فيديو تجريبي للنموذج الأولي",
            "Healthcare & Assistive Technology Track",
            "جوائز مالية تحفيزية + إمكانية الاحتضان في حاضنة أعمال الجامعة والاستفادة من معامل التصنيع الرقمي",
            "أولوية عالية (High)",
            "إبراز الشراكة العلمية والهندسية والأثر المجتمعي المباشر لخدمة 1.5 مليون كفيف في مصر."
        ),
        (
            8,
            "برنامج إبتكار لدعم مشاريع التخرج (IbTIECar - Round 1)",
            "هيئة تنمية صناعة تكنولوجيا المعلومات (ITIDA) & TIEC",
            "https://tiec.gov.eg/Arabic/Programs/IBTIECAR/Pages/default.aspx",
            "دورة التخرج السنوية (نوفمبر 2026)",
            "الموعد النهائي: 15 ديسمبر 2026",
            "مفتوحة للتقديم (Open)",
            "1. مقترح المشروع الفني وتوصيف النظام المدمج والـ AI\n2. جدول الميزانية التفصيلي لقطع الهاردوير والمستشعرات\n3. بيانات الطلاب والمشرف الأكاديمي الرسمية بالجامعة",
            "ICT Graduation Projects (AI, IoT & Embedded Systems)",
            "تمويل نقدي 10,000 إلى 30,000 جنيه لشراء المكونات + برمجيات مجانية ودورات ريادة أعمال واحتضان لاحق",
            "أولوية قصوى (Very High)",
            "هذه المنحة الحكومية الأساسية؛ جهز جدول الميزانية المرفق في صفحة (الفريق والميزانية) وارفعه مباشرة."
        ),
        (
            9,
            "مسابقة صنع في مصر (Made In Egypt - MIE)",
            "جمعية مهندسي الكهرباء والإلكترونيات (IEEE Egypt) ومؤسسة مصر الخير",
            "https://www.facebook.com/share/1LHYYWqeH1/",
            "ديسمبر 2026",
            "الموعد النهائي: 10 يناير 2027",
            "لم تفتح بعد - متابعة (Pending)",
            "1. مقترح المشروع الهندسي (Engineering Project Proposal)\n2. خطة التصنيع المحلي وإحلال الواردات\n3. خطاب توصية وتزكية من كلية الهندسة",
            "Industrial & Assistive Graduation Projects Track",
            "تمويل تصنيع النموذج الأولي الصناعي + ربط مع مصانع وشركات محلية + جوائز نقدية في الحفل السنوي",
            "أولوية عالية (High)",
            "التركيز على ريادة التصنيع المحلي (Frugal Engineering) وتخفيض تكلفة الجهاز لأقل من 20% من المنتج الأوروبي."
        ),
        (
            10,
            "أولمبياد الابتكار المصري (Egyptian Innovation Olympiad)",
            "وزارة التعليم العالي وصندوق رعاية المبتكرين والنوابغ (ISF)",
            "https://www.facebook.com/share/p/1Epy7TcMCz/",
            "موسم الجامعات المصرية 2026 / 2027",
            "التصفيات التمهيدية: 15 يناير 2027",
            "لم تفتح بعد - متابعة (Pending)",
            "1. تسجيل بيانات الفريق والجامعة والمشروع عبر البوابة\n2. فيديو 3 دقائق يشرح المشكلة والحل والنموذج الأولي\n3. ملف العرض التقديمي للمشروع",
            "الابتكارات الهندسية والتكنولوجيا الصحية والخدمية",
            "جوائز مالية ضخمة تصل لمئات الآلاف للمراكز الأولى + تمويل تحويل المشروع إلى شركة رسمية برعاية حكومية",
            "أولوية عالية (High)",
            "تجهيز فيديو قوي يستعرض محاكي الدبابيس اللمسية وردود الفعل الحية لاجتياز مرحلة التحكيم الأولى بسهولة."
        ),
        (
            11,
            "رالي مصر لريادة الأعمال (Egypt Entrepreneurship Rally)",
            "الأكاديمية العربية للعلوم والتكنولوجيا (AASTMT) وصندوق ISF",
            "https://www.facebook.com/share/p/19d1S9VSP9/",
            "ديسمبر 2026",
            "الموعد النهائي: 31 يناير 2027",
            "لم تفتح بعد - متابعة (Pending)",
            "1. استمارة التقديم لمسار رواد الأعمال الجامعيين\n2. العرض التقديمي (Pitch Deck)\n3. خطة تحويل النموذج الهندسي إلى منتج تجاري بالسوق",
            "General Tech & Social Impact Startups Track",
            "جوائز مالية تتجاوز 1,000,000 جنيه إجمالي جوائز الرالي + معسكر تدريبي مكثف في شرم الشيخ/الإسكندرية",
            "أولوية قصوى (Very High)",
            "أكبر مسابقة ريادية للجامعات في مصر؛ مجهزة تماماً بمستندات الـ Pitch Deck والـ Lean Canvas الموجودين بالمشروع."
        ),
        (
            12,
            "مسابقة CEDARE للابتكار والحلول الذكية المستدامة",
            "مركز البيئة والتنمية للإقليم العربي وأوروبا (CEDARE)",
            "https://www.facebook.com/share/17jBa1SBBg/",
            "مفتوح دورياً",
            "الموعد النهائي المتوقع: 28 فبراير 2027",
            "لم تفتح بعد - متابعة (Pending)",
            "1. مقترح تقني يوضح الأثر الاجتماعي والبيئي للمشروع\n2. ملف العرض التقديمي\n3. بيانات الفريق الأكاديمي",
            "Assistive Living, Smart Cities & Inclusive Communities",
            "شهادات تقديرية دولية + منح دعم فني + تشبيك مع منظمات التنمية الدولية في أوروبا والعالم العربي",
            "أولوية متوسطة (Medium)",
            "التركيز على إتاحة المدن الذكية الشاملة لجميع الفئات (Inclusive Smart Cities) وتسهيل حركة المكفوفين بالمباني."
        ),
        (
            13,
            "تحدي مصر والعرب للـ IoT والـ AI (Arab IoT & AI Challenge)",
            "IEEE & مجمع الإبداع ببرج العرب & الجهاز القومي للاتصالات",
            "https://egypt.arabiotai.org/",
            "موسم 2026 / 2027",
            "الموعد النهائي: 30 ديسمبر 2026",
            "مفتوحة للتقديم (Open)",
            "1. استمارة التسجيل لمسار مشاريع التخرج (Graduation Projects Track)\n2. مقترح المشروع الفني وتوصيف دمج الذكاء الاصطناعي وإنترنت الأشياء\n3. فيديو تجريبي لاختبار النظام المدمج والمحاكاة",
            "Graduation Projects Track (AI / Smart Devices / Assistive Tech)",
            "جوائز مالية + تأهيل لنهائيات جيتكس دبي (GITEX Dubai) وعرض المشروع أمام المستثمرين الإقليميين",
            "أولوية قصوى (Very High)",
            "فرصة ذهبية للوصول لدبي؛ استخدم الإجابات الجاهزة باللغة الإنجليزية في صفحة (إجابات الاستمارات) للتقديم."
        ),
        (
            14,
            "إعلان منحة تصنيع GraduTech Round 2 (LinkedIn)",
            "EME Innovation Labs",
            "https://lnkd.in/p/d8hYyyK8",
            "أكتوبر 2026",
            "الموعد النهائي: 15 نوفمبر 2026",
            "مفتوحة للتقديم (Open)",
            "التسجيل عبر رابط الاستمارة المباشر (الرابط 15) ورفع مستندات المشروع على جوجل درايف",
            "Hardware Prototyping & FabLab / IoT Mentorship",
            "دعم تصنيع كامل للنماذج الأولية الهندسية مجاناً داخل مختبرات فاب لاب وإنترنت الأشياء بالجيزة",
            "أولوية قصوى (Very High)",
            "الإعلان الترويجي الرسمي للمنحة؛ استخدم بيانات الفورم (الرابط 15) للتقديم الفوري بدون أي تأخير."
        ),
        (
            15,
            "استمارة منحة معامل EME Innovation Labs Giza",
            "EME Innovation Labs Giza",
            "https://forms.gle/ansiLbxGNXWFQcQT9",
            "أكتوبر 2026",
            "الموعد النهائي: 15 نوفمبر 2026",
            "مفتوحة للتقديم (Open)",
            "1. استمارة Google Form كاملة\n2. رابط فولدر جوجل درايف يحوي: البطاقات القومية للطلاب، السير الذاتية، مقترح المشروع\n3. تحديد متطلبات الفاب لاب ومعامل الـ IoT بدقة",
            "FabLab & IoT Lab Graduation Support Program",
            "تصنيع مجاني لشاسيه النظارة بالطباعة ثلاثية الأبعاد + تصنيع لوحات الـ PCB + توفير معامل اختبارات الدوائر والأردوينو",
            "أولوية قصوى (Very High)",
            "جاهز للتقديم الفوري؛ انسخ الإجابات مباشرة من صفحة (إجابات الاستمارات) لتعبئة الاستمارة في 5 دقائق."
        ),
        (
            16,
            "تحدي الروبوتات من أجل الخير (Robotics for Good 2027)",
            "الاتحاد الدولي للاتصالات (ITU) & الأمم المتحدة (AI for Good)",
            "https://www.itu.int/ (Robotics for Good)",
            "الربع الأول 2027",
            "الموعد النهائي: 15 مارس 2027",
            "لم تفتح بعد - متابعة (Pending)",
            "1. مقترح المشروع باللغة الإنجليزية (English Project Dossier)\n2. فيديو 3 دقائق على يوتيوب مترجم بالإنجليزية\n3. إثبات الالتزام بأهداف التنمية المستدامة للأمم المتحدة",
            "Robotics for Assistive Living & Accessibility (UN SDGs)",
            "دعوة رسمية لعرض الابتكار في القمة العالمية للذكاء الاصطناعي بجنيف (جنيف - سويسرا) + شهادات عالمية",
            "أولوية عالية (High)",
            "التركيز على تحقيق الهدف 3 (الصحة الجيدة والرفاه) والهدف 10 (الحد من أوجه عدم المساواة) للأمم المتحدة."
        ),
        (
            17,
            "مسابقة تصميم الطلاب في مؤتمر التفاعل (HRI 2027)",
            "ACM / IEEE International Conference on Human-Robot Interaction",
            "https://humanrobotinteraction.org/",
            "يناير 2027",
            "الموعد النهائي لتسليم الأوراق: 15 أبريل 2027",
            "لم تفتح بعد - متابعة (Pending)",
            "1. ورقة بحثية قصيرة (Short Paper 4 pages IEEE format)\n2. فيديو تفاعلي للتفاعل بين الإنسان والجهاز اللمسي\n3. موافقة لجنة الأخلاقيات وتجارب المستخدمين",
            "Student Design Competition: Wearable Haptics & Sensory Substitution",
            "نشر البحث العلمي رسمياً في مكتبة IEEE Xplore / ACM Digital Library + جوائز تكريمية دولية",
            "أولوية عالية (High)",
            "فرصة أكاديمية لا تعوض؛ تنسيق كتابة البحث العلمي مع المشرف الأكاديمي د. إسلام محمد استناداً لوثائق المشروع."
        ),
        (
            18,
            "بطولة RoboCup العالمية (Open Challenge)",
            "RoboCup Federation",
            "https://www.robocup.org/",
            "يناير 2027",
            "التسجيل الأولي: 15 فبراير 2027",
            "لم تفتح بعد - متابعة (Pending)",
            "1. ورقة توصيف النظام التقني (Team Description Paper - TDP)\n2. فيديو يثبت كفاءة تفادي العوائق الحية\n3. مستودع الكود البرمجي المفتوح",
            "@Home / Open Assistive Technology Track",
            "اعتراف دولي من نخبة مجتمع الروبوتات العالمي ورعايات من شركات كبرى ومصنعي الأجهزة المدمجة",
            "أولوية متوسطة (Medium)",
            "استعراض سيناريو الملاحة الحية وتجاوز العقبات الديناميكية الثابتة والمتحركة بدون أي تلامس."
        ),
        (
            19,
            "منافسات كاجل للرؤية الحاسوبية والطب الحيوي (Kaggle)",
            "Kaggle / Google",
            "https://www.kaggle.com/competitions",
            "مستمر على مدار العام",
            "تحديات متجددة شهرياً",
            "مفتوحة للتقديم (Open)",
            "1. رفع الكود البرمجي والنماذج عبر Jupyter Notebooks على منصة Kaggle\n2. تحقيق درجات تقييم عالية على داتا سيت الاختبار",
            "Computer Vision, Depth Estimation & Assistive AI Benchmarks",
            "جوائز مالية بالدولار للمراكز الأولى + تصنيف عالمي معترف به (Kaggle Grandmaster Points)",
            "أولوية متوسطة (Medium)",
            "مشاركة نتائج تدريب نموذج YOLOv8 المخصص للعوائق ومحاذاة العمق مع صور كاميرا Orbbec."
        ),
        (
            20,
            "التحدي الدولي للروبوتات 2027 (IRC Final)",
            "الاتحاد الدولي للروبوتات والذكاء الاصطناعي",
            "https://www.ircrobot.org/ar/",
            "فبراير 2027",
            "الموعد النهائي: 30 أبريل 2027",
            "لم تفتح بعد - متابعة (Pending)",
            "1. اجتياز التصفيات الإقليمية المحلية\n2. تقديم النموذج الهندسي النهائي المتكامل (Hard & Soft)\n3. تجربة حية أمام لجان التحكيم",
            "Autonomous Service & Assistive Robotics",
            "جوائز مالية كبرى ودروع وشهادات تقديرية للمراكز الفائزة على المستوى الإقليمي والدولي",
            "أولوية متوسطة (Medium)",
            "التركيز على ميكانيكا مصفوفة الدبابيس والتحكم الدقيق عبر محركات الخطوة (Precision Stepper Actuation)."
        ),
        (
            21,
            "برنامج ومسرعة TechForward للمشاريع العميقة",
            "TechForward Innovation Hub",
            "TechForward Official Portal",
            "الربع الأول 2027",
            "الموعد النهائي: 10 مايو 2027",
            "لم تفتح بعد - متابعة (Pending)",
            "1. ملف العرض التقديمي (Pitch Deck)\n2. فيديو لاختبارات المستخدمين المكفوفين\n3. هيكل تكلفة المنتج وتوقعات المبيعات",
            "DeepTech Hardware & AI Solutions",
            "احتضان وتمويل تأسيسي من 100,000 إلى 250,000 جنيه + مساحات عمل ومعامل فحص هندسي متطورة",
            "أولوية متوسطة (Medium)",
            "إبراز جاهزية الفريق المكون من 11 مهندساً يغطون الهاردوير والبرمجيات والميكانيكا والتصميم."
        ),
        (
            22,
            "تحدي TechnoGeeks Future Challenge 2027",
            "TechnoGeeks Community & Tech Partners",
            "TechnoGeeks Community Channels",
            "الربع الأول 2027",
            "الموعد النهائي: 25 مايو 2027",
            "لم تفتح بعد - متابعة (Pending)",
            "1. استمارة التسجيل الإلكترونية للفريق\n2. كود المشروع والنموذج الأولي التفاعلي\n3. عرض توضيحي حي للمحاكي الافتراضي",
            "Embedded Systems, Robotics & AI",
            "جوائز مادية وأجهزة هاردوير متقدمة لتطوير النماذج الأولية ورعايات من شركات الإلكترونيات",
            "أولوية متوسطة (Medium)",
            "التركيز على سرعة المعالجة (Latency < 100ms) ومعدل دقة رصد العوائق العالي (>90%)."
        ),
        (
            23,
            "برنامج دعم مشاريع التخرج السنوي من ITIDA",
            "هيئة تنمية صناعة تكنولوجيا المعلومات (ITIDA)",
            "https://itida.gov.eg/Arabic/Programs/Graduation/Pages/default.aspx",
            "نوفمبر 2026",
            "الموعد النهائي: 20 ديسمبر 2026",
            "مفتوحة للتقديم (Open)",
            "1. استمارة التقديم الرسمية المعتمدة من عميد الكلية والمشرف الأكاديمي\n2. التوصيف التقني للمشروع والجدول الزمني ومؤشرات الأداء\n3. كشف مفصل بالمكونات الإلكترونية والمستشعرات وعروض الأسعار",
            "Electronics Design, Robotics, AI & Embedded Systems",
            "تمويل شراء المكونات الهاردوير والمستشعرات والمحركات حتى 30,000 جنيه لكل مشروع تخرج فائز",
            "أولوية قصوى (Very High)",
            "المنحة الحكومية الأكثر رسوخاً في كليات الهندسة المصرية؛ استخدم جدول الميزانية وبيانات الفريق المرفقة هنا."
        ),
        (
            24,
            "برنامج إبتكار IbTIECar (جولة دعم التصنيع المتقدم)",
            "مركز الإبداع التكنولوجي وريادة الأعمال (TIEC)",
            "https://tiec.gov.eg/Arabic/Programs/IBTIECAR/Pages/default.aspx",
            "يناير 2027",
            "الموعد النهائي: 28 فبراير 2027",
            "لم تفتح بعد - متابعة (Pending)",
            "1. تقرير مرحلي عن النموذج الأولي (Progress Report Milestone)\n2. نتائج اختبارات المحاكاة والـ 3D Point Clouds\n3. مراجعة فواتير شراء المكونات",
            "ICT Hardware / Software Acceleration",
            "دعم تصنيع إضافي للمشاريع المتميزة واستشارات إرشادية وتأهيل للتأسيس القانوني للشركة",
            "أولوية عالية (High)",
            "متابعة دورية لتسليمات الدورة الأولى من إبتكار للمحافظة على موقع متميز في التصفيات المتقدمة."
        ),
        (
            25,
            "برنامج إبتكار IbTIECar (معسكر التدريب الصيفي)",
            "مركز الإبداع التكنولوجي وريادة الأعمال (TIEC)",
            "https://tiec.gov.eg/Arabic/Programs/IBTIECAR/Pages/default.aspx",
            "مايو 2027",
            "الموعد النهائي: 15 يونيو 2027",
            "لم تفتح بعد - متابعة (Pending)",
            "1. النموذج الأولي الكامل المختبر مع مستخدمين حقيقيين\n2. الأطروحة الهندسية للمشروع (Graduation Thesis Draft)\n3. فيديو احترافي للحل النهائي",
            "Startup Ready Prototypes Track",
            "فرصة الاحتضان المباشر في حاضنة Start-IT وتحويل المشروع مباشرة لشركة ناشئة بتمويل تأسيسي",
            "أولوية عالية (High)",
            "مرحلة ما بعد مناقشة مشروع التخرج؛ نقلة نوعية من أروقة الجامعة إلى السوق التجاري مباشرة."
        ),
        (
            26,
            "متابعة تسليمات ومخرجات حاضنة إبتكار (IbTIECar Demo Day)",
            "TIEC / ITIDA",
            "https://tiec.gov.eg/Arabic/Programs/IBTIECAR/Pages/default.aspx",
            "يونيو / يوليو 2027",
            "يوم العرض النهائي (Demo Day): يوليو 2027",
            "لم تفتح بعد - متابعة (Pending)",
            "1. العرض التقديمي النهائي أمام لجان التحكيم وكبار رجال الأعمال (Final Pitch)\n2. البوسترات العلمية والنموذج الصناعي النهائي القابل للارتداء\n3. ملخص براءة الاختراع وحماية الملكية الفكرية (IP File)",
            "Best Graduation Project of the Year & Innovation Awards",
            "جوائز التفوق لمشاريع التخرج على مستوى الجمهورية وتغطية إعلامية موسعة وفرص تمويل استثماري",
            "أولوية قصوى (Very High)",
            "الهدف الختامي لعام التخرج؛ تمثيل الجامعة المصرية الصينية والفوز بالمركز الأول على مستوى مصر."
        )
    ]
    
    for row_idx, comp in enumerate(competitions, 5):
        fill = zebra_fill if row_idx % 2 == 0 else white_fill
        ws1.row_dimensions[row_idx].height = 65
        
        for col_idx, val in enumerate(comp, 1):
            cell = ws1.cell(row=row_idx, column=col_idx, value=val)
            cell.font = reg_font
            cell.border = border
            cell.fill = fill
            
            # Formats
            if col_idx in [1, 5, 6]:
                cell.alignment = align_center
                if col_idx == 1:
                    cell.font = bold_font
            elif col_idx == 4: # Link
                cell.alignment = align_left
                cell.font = link_font
                if str(val).startswith("http"):
                    cell.hyperlink = str(val)
            elif col_idx == 7: # Status
                cell.alignment = align_center
                for k, (s_fill, s_font) in status_styles.items():
                    if k in str(val):
                        cell.fill = s_fill
                        cell.font = s_font
                        break
            elif col_idx == 11: # Priority
                cell.alignment = align_center
                if "قصوى" in str(val):
                    cell.fill = prio_vhigh[0]
                    cell.font = prio_vhigh[1]
                elif "عالية" in str(val):
                    cell.fill = prio_high[0]
                    cell.font = prio_high[1]
                else:
                    cell.fill = prio_med[0]
                    cell.font = prio_med[1]
            else:
                cell.alignment = align_left

    # Auto Filter for Sheet 1
    ws1.auto_filter.ref = f"A4:L{len(competitions) + 4}"
    
    # Add Data Validation for Status Column (Col G, rows 5 to 30)
    dv_status = DataValidation(type="list", formula1='"مفتوحة للتقديم (Open),لم تفتح بعد - متابعة (Pending),قيد التجهيز والمراجعة (In Progress),تم التقديم بنجاح (Submitted)"', allow_blank=True)
    ws1.add_data_validation(dv_status)
    dv_status.add(f"G5:G{len(competitions) + 4}")

    # Column Widths
    ws1.column_dimensions["A"].width = 5
    ws1.column_dimensions["B"].width = 28
    ws1.column_dimensions["C"].width = 24
    ws1.column_dimensions["D"].width = 30
    ws1.column_dimensions["E"].width = 22
    ws1.column_dimensions["F"].width = 22
    ws1.column_dimensions["G"].width = 24
    ws1.column_dimensions["H"].width = 42
    ws1.column_dimensions["I"].width = 26
    ws1.column_dimensions["J"].width = 32
    ws1.column_dimensions["K"].width = 18
    ws1.column_dimensions["L"].width = 40


    # =========================================================================
    # SHEET 2: Deliverables Checklist (قائمة تجهيز المخرجات)
    # =========================================================================
    ws2 = wb.create_sheet(title="تجهيز المخرجات (Checklist)")
    ws2.views.sheetView[0].showGridLines = True
    
    ws2.merge_cells("A1:G1")
    ws2["A1"] = "Ally Vision — Master Application Deliverables & Assets Kit"
    ws2["A1"].font = title_font
    ws2["A1"].alignment = Alignment(horizontal="left", vertical="center")
    
    ws2.merge_cells("A2:G2")
    ws2["A2"] = "قائمة الأصول والمستندات الهندسية والتسويقية الجاهزة في المشروع لرفعها في استمارات التقديم"
    ws2["A2"].font = subtitle_font
    
    deliv_headers = [
        "م",
        "المخرج / الأصل المطلوب للتقديم",
        "الصيغة المعتمدة",
        "الحالة الحالية في المشروع",
        "مسار الملف في المشروع (File Location)",
        "المسابقات التي تطلبه",
        "ملاحظات التجهيز والتحديث"
    ]
    
    for c_idx, h in enumerate(deliv_headers, 1):
        cell = ws2.cell(row=4, column=c_idx, value=h)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = align_center
        cell.border = border
    ws2.row_dimensions[4].height = 28
    
    deliverables_data = [
        (1, "العرض التقديمي الرسمي للمشروع (Pitch Deck)", "PDF & PPTX", "جاهز ومعتمد (12 شريحة)", "Business Model/ally_vision_pitch_deck.md & Ally_Vision_AI_Navigation.pptx", "جميع المسابقات بدون استثناء", "نسخة Uber/Slidebean باللون الأبيض وتصميم سويسري أنيق"),
        (2, "المقترح الفني الأكاديمي (Technical Proposal)", "PDF (9 صفحات)", "جاهز ومعتمد أكاديمياً", "Proposal (1).pdf & AI/Ally_Vision_Documentation.md", "ITIDA, IbTIECar, EME Labs, ISF", "يحتوي على تفصيل معمارية النظام ومعادلات الـ RANSAC و ByteTrack"),
        (3, "مخطط نموذج العمل التجاري (Lean Canvas & BMC)", "Markdown & PDF & JPG", "جاهز ومعتمد", "Business Model/ally_vision_lean_canvas.md & BMC.pdf", "Start-IT, EIP, رالي ريادة الأعمال", "يوضح هيكل الـ B2B2C ورعايات الـ CSR وحجم السوق 31.4 مليار دولار"),
        (4, "الموقع الإلكتروني الرسمي للمشروع", "Live Web Platform", "مطور بالكامل (React + Vite)", "website/ directory (index.html, src/)", "جميع المسابقات (كإثبات احترافية)", "يحتوي على رادار ثلاثي الأبعاد، استعراض الفريق، وبنك الأبحاث العلمية"),
        (5, "التصميم الصناعي والصور ثلاثية الأبعاد (3D Renders)", "High-Res PNG Images", "جاهز بدقة استوديو عالية", "render_visor_product.py & Gemini_Generated_Image_.png", "Start-IT, EME Labs, ITU Robotics for Good", "صور ثلاثية الأبعاد لنظارة الرأس المدمجة ومصفوفة الـ 5x5 Pins"),
        (6, "فيديو العرض التوضيحي والمحاكاة (Video Demo)", "MP4 (2-3 Minutes)", "قيد التسجيل والرفع", "AI/ virtual_simulator.py (Pygame Real-time HUD)", "Meta AI, EME Labs, Olympiad, Arab IoT", "تسجيل الشاشة أثناء تشغيل المحاكي التفاعلي ومسار المشي الآمن الأخضر"),
        (7, "أوراق التوثيق وبيانات الفريق والمشرف الأكاديمي", "PDF / Drive Folder", "جاهزة ومجمعة", "Google Drive Folder (الرقم القومي، الكارنيهات، السير الذاتية)", "EME Labs, ITIDA GP, IbTIECar", "مطلوب وضعها في فولدر جوجل درايف بوضع View-only ومشاركته"),
        (8, "مستودع الكود البرمجي الموثق (GitHub Repo)", "Git Repository", "مهيكل وفق معمارية السبرنتات", "ally-vision-ai/ (contracts.py, main.py, yolo_detector.py)", "Meta Challenge, Kaggle, RoboCup, HRI", "يحتوي على Data Contracts صارمة وتوثيق كامل لتشغيل الكود")
    ]
    
    for row_idx, d_data in enumerate(deliverables_data, 5):
        fill = zebra_fill if row_idx % 2 == 0 else white_fill
        ws2.row_dimensions[row_idx].height = 42
        
        for col_idx, val in enumerate(d_data, 1):
            cell = ws2.cell(row=row_idx, column=col_idx, value=val)
            cell.font = reg_font
            cell.border = border
            cell.fill = fill
            
            if col_idx in [1, 3]:
                cell.alignment = align_center
                if col_idx == 1:
                    cell.font = bold_font
            elif col_idx == 4:
                cell.alignment = align_center
                if "جاهز" in str(val):
                    cell.fill = status_styles["مفتوحة للتقديم (Open)"][0]
                    cell.font = status_styles["مفتوحة للتقديم (Open)"][1]
                else:
                    cell.fill = status_styles["قيد التجهيز والمراجعة (In Progress)"][0]
                    cell.font = status_styles["قيد التجهيز والمراجعة (In Progress)"][1]
            else:
                cell.alignment = align_left

    for col in ws2.columns:
        col_letter = get_column_letter(col[0].column)
        ws2.column_dimensions[col_letter].width = 25
    ws2.column_dimensions["A"].width = 5
    ws2.column_dimensions["B"].width = 30
    ws2.column_dimensions["C"].width = 16
    ws2.column_dimensions["D"].width = 22
    ws2.column_dimensions["E"].width = 38
    ws2.column_dimensions["F"].width = 30
    ws2.column_dimensions["G"].width = 38


    # =========================================================================
    # SHEET 3: Master Q&A Application Bank (بنك إجابات الاستمارات)
    # =========================================================================
    ws3 = wb.create_sheet(title="إجابات الاستمارات (Q&A)")
    ws3.views.sheetView[0].showGridLines = True
    
    ws3.merge_cells("A1:E1")
    ws3["A1"] = "Ally Vision — Master Application Q&A (Application Answer Bank)"
    ws3["A1"].font = title_font
    ws3["A1"].alignment = Alignment(horizontal="left", vertical="center")
    
    ws3.merge_cells("A2:E2")
    ws3["A2"] = "إجابات نموذجية معتمدة باللغتين العربية والإنجليزية لملء استمارات المسابقات والمنح وحاضنات الأعمال"
    ws3["A2"].font = subtitle_font
    
    headers3 = [
        "السؤال الشائع في استمارات المسابقات",
        "المجال / الفئة",
        "الإجابة النموذجية باللغة العربية (Standard Arabic Answer)",
        "الإجابة النموذجية باللغة الإنجليزية (Standard English Answer)",
        "أهم الأرقام ونقاط القوة (Proof Points & Metrics)"
    ]
    
    for c_idx, h in enumerate(headers3, 1):
        cell = ws3.cell(row=4, column=c_idx, value=h)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = align_center
        cell.border = border
    ws3.row_dimensions[4].height = 28
    
    qa_data = [
        (
            "ما هو عنوان وفكرة المشروع باختصار؟\n(Project Title & Elevator Pitch)",
            "عام (General)",
            "Ally Vision هو جهاز رأس ذكي قابل للارتداء مخصص للمكفوفين وضعاف البصر، يقوم بتحويل العالم البصري المحيط إلى تضاريس لمسية فيزيائية حية على جبهة المستخدم بواسطة مصفوفة دبابيس ميكانيكية (5×5) وكاميرا عمق ثلاثية الأبعاد، مما يتيح استقلالية تنقل كاملة بدون استخدام اليدين ودون حجب حاسة السمع.",
            "Ally Vision is a next-generation visual-to-tactile spatial navigation headset for the blind. It translates 3D environmental geometry into intuitive physical height profiles on the forehead using a 5x5 micro-pin actuator matrix and edge AI depth camera, delivering complete hands-free and ear-free mobility independence.",
            "• 100% Ear-Free\n• 100% Hands-Free\n• Latency < 100ms\n• 5x5 Physical Pin Matrix"
        ),
        (
            "ما هي المشكلة المحددة التي يعالجها المشروع؟\n(The Problem Statement)",
            "المشكلة (Problem)",
            "1. العصا البيضاء التقليدية لا تكشف العوائق العلوية في مستوى الصدر والرأس (مثل الفروع المرتفعة والنوافذ واللافتات).\n2. النظارات الذكية الصوتية تحجب حاسة السمع الأساسية التي يعتمد عليها الكفيف لإدراك الشارع وحركة المرور.\n3. البدائل العالمية عالية التقنية (مثل 7Sense الإستوني) باهظة الثمن (3,000$ إلى 5,000$+)، مما يجعلها خارج متناول مستخدمي الدول النامية.",
            "1. White canes miss head- and chest-level hazards (e.g. low-hanging branches, open windows, signage).\n2. Audio smart glasses mask ambient street sounds and vehicle noise, creating severe safety risks.\n3. Existing high-tech European solutions (like 7Sense and BrainPort) cost $3,000 to $5,000+, putting them completely out of reach for users in developing markets.",
            "• 285 مليون كفيف عالمياً\n• 1.5 مليون كفيف في مصر\n• 70% من حوادث الكفيف بسبب عوائق الرأس"
        ),
        (
            "ما هو الحل والابتكار التقني الفريد؟\n(Solution & Technical Innovation)",
            "الحل التقني (Solution)",
            "منظومة متكاملة من 3 مراحل: \n1. الإدخال: كاميرا عمق RGB-D تلتقط البيئة ثلاثية الأبعاد.\n2. المعالجة: خوارزمية ذكاء اصطناعي (YOLOv8 + RANSAC) تستخرج الأرضية وترسم ممر سير آمن بعرض 80 سم وتتعقب العوائق وتحدد سرعة اقترابها عبر ByteTrack.\n3. الإخراج: مصفوفة ميكانيكية 5×5 تعطي ارتفاعات فيزيائية ملموسة (0 إلى 5) بدلاً من الاهتزاز السطحي لتجنب خدر الجلد اللمسي، بزمن استجابة أقل من 100ms.",
            "A seamless 3-stage light-to-touch pipeline:\n1. Input: RGB-D depth sensor capturing 3D point clouds at 30 FPS.\n2. Edge AI Brain: YOLOv8 ONNX real-time object detection + RANSAC ground plane fitting to establish an 80cm clear walking corridor, coupled with ByteTrack velocity tracking.\n3. Output: 5x5 micro-actuator matrix modulating physical height displacement (levels 0-5) on the forehead, eliminating tactile sensory fatigue with <100ms end-to-end latency.",
            "• RANSAC Ground Clearance\n• ByteTrack Velocity (dZ/dt)\n• Dynamic Pin Height (No Numbness)\n• sub-20ms ONNX inference"
        ),
        (
            "من هي الشريحة المستهدفة وما حجم السوق؟\n(Target Market & Customer Segments)",
            "السوق (Market)",
            "• السوق الإجمالي (TAM): 31.4 مليار دولار عالمياً (285 مليون فرد يعانون من ضعف بصري).\n• السوق المتاح إقليمياً (SAM): أكثر من 40 مليون فرد في منطقة الشرق الأوسط وأفريقيا.\n• السوق المستهدف الأولي (SOM): 1.5 مليون كفيف في مصر كقاعدة تدريب وإطلاق.\n• العملاء: المستخدمون النهائيون (طلاب وموظفون مكفوفون)، والمؤسسات المعنية (جمعيات رعاية المكفوفين ومراكز التأهيل)، ورعايات المسؤولية المجتمعية (CSR) للبنوك والشركات.",
            "• TAM (Global): $31.4 Billion (285M visually impaired individuals worldwide).\n• SAM (Regional): 40M+ visually impaired individuals across MENA.\n• SOM (Initial): 1.5M visually impaired people in Egypt as validation launchpad.\n• Target Segments: Active visually impaired students and professionals (B2C), Blind Welfare NGOs and rehabilitation hubs (B2G/B2B), and Corporate Social Responsibility (CSR) donors.",
            "• TAM: $31.4B\n• SAM: 40M+\n• SOM: 1.5M (Egypt)\n• B2B2C Procurement Model"
        ),
        (
            "ما هي الميزة التنافسية؟ ولماذا يتفوق مشروعكم؟\n(Competitive Advantage & Moat)",
            "التنافسية (Advantage)",
            "1. الحفاظ التام على السمع (100% Ear-Free) لضمان أمان المستخدم في الشارع.\n2. الترميز اللمسي بالارتفاع الميكانيكي الحقيقي لمنع تكيف وخدر الجلد الناتج عن الاهتزاز.\n3. استخراج الممر الآمن لحظياً وخفض التشتيت الذهني (Transmit only essential data).\n4. ريادة التكلفة (Cost Leadership): تقليل تكلفة المكونات بنسبة 80% مقارنة بالبدائل الأوروبية، مع سعر استهداف أقل من 400 دولار للجهاز.",
            "1. 100% Ear-Free: Zero audio interference, preserving vital ambient sound cues.\n2. True Physical Displacement: Pin heights (0-5) instead of surface vibrations prevent sensory adaptation and numbness.\n3. Intelligent Safe Corridor: 80cm navigable path extracted in real time to minimize cognitive load.\n4. Frugal Engineering: Custom BOM and PCB architecture lowering production cost to <20% of Western competitors (retail target <$400 vs $4,000+).",
            "• تكلفة < 20% من 7Sense\n• تفادي خدر الجلد (No Sensory Fatigue)\n• كشف العوائق العلوية والجانبية"
        ),
        (
            "ما هو نموذج العمل وتوليد الإيرادات؟\n(Business Model & Revenue Streams)",
            "البيزنس (Business)",
            "1. عقود التوريد المؤسسي (B2B / B2G): توريد كميات لجمعيات رعاية المكفوفين ومراكز التأهيل بأسعار مدعومة.\n2. برامج الرعاية المجتمعية (CSR Sponsorships): تعاقد مع البنوك والشركات الكبرى لتمويل شراء أجهزة للمستحقين مجاناً.\n3. البيع التجاري المباشر (B2C): بسعر اقتصادي في متناول الأفراد والتأمين الصحي.\n4. نموذج الجهاز كخدمة (HaaS): اشتراك صيانة اختياري يشمل استبدال الدبابيس التالفة وتحديثات الذكاء الاصطناعي السحابية.",
            "1. Institutional Procurement (B2G/B2B): Bulk sales to blind welfare associations and rehabilitation centers at subsidized rates.\n2. Corporate CSR Sponsorships: Partnerships with banks and corporations funding device batches for underserved users.\n3. Direct Commercial Sales (B2C): Affordable retail pricing (<$400) for capable individuals and private medical insurance.\n4. Hardware-as-a-Service (HaaS): Optional annual subscription for mechanical pin maintenance, warranty, and over-the-air AI upgrades.",
            "• B2B2C Framework\n• CSR Funding Contracts\n• HaaS Annual Maintenance\n• Hardware Target < $400"
        ),
        (
            "ما هي المرحلة الحالية للمشروع وما الذي تم إنجازه؟\n(Current Traction & Milestones)",
            "الإنجازات (Traction)",
            "1. تدريب وتصدير نموذج YOLOv8n ONNX وتحقيق زمن استنتاج أقل من 20ms على الأجهزة الطرفية.\n2. بناء وتطوير محاكي برمجيات تفاعلي حقيقي (Virtual 5x5 Haptic Simulator) لعرض تضاريس الدبابيس في نفس اللحظة.\n3. صياغة عقود البيانات البرمجية المشتركة (Data Contracts) واختبار دمج الكاميرا مع الأردوينو.\n4. جمع وتصنيف مجموعة بيانات مخصصة تحتوي على 2,000 صورة لعوائق المشي الحقيقية، ومراجعة 137 ورقة بحثية في الاستبدال الحسي.",
            "1. Trained and validated YOLOv8n ONNX obstacle detection running sub-20ms on edge hardware.\n2. Developed an interactive split-screen real-time 5x5 tactile simulator and safe path planner.\n3. Established robust immutable data contracts between camera, AI, and Arduino Uno R4 serial drivers.\n4. Curated a custom 2,000-image navigation dataset and synthesized 137 academic papers on sensory substitution and tactile neuroscience.",
            "• 2,000 Annotated Images\n• sub-20ms AI Inference\n• Working Virtual 5x5 Simulator\n• 137 Synthesized Research Papers"
        ),
        (
            "ما هي احتياجات المعامل والدعم الفني المطلوب؟\n(FabLab & IoT Lab Support Needs)",
            "احتياجات الدعم (Needs)",
            "1. معمل الفاب لاب (FabLab): طباعة ثلاثية الأبعاد (SLA/FDM) لهيكل النظارة/الخوذة (Visor Case)، تصنيع لوحات الدوائر الإلكترونية المطبوعة (PCB Milling/Fabrication)، وتقطيع ليزر/CNC لأجزاء مصفوفة الدبابيس.\n2. معمل إنترنت الأشياء (IoT Lab): متحكمات دقيقة (Arduino Uno R4, ESP32)، أدوات فحص الإشارات ورسم موجات المحركات (Oscilloscopes)، ومحركات خطوة متناهية الصغر (Micro Steppers).\n3. الإرشاد الفني: توجيه في هندسة تصغير الحجم (Miniaturization)، وإدارة استهلاك الطاقة للبطاريات، وتسجيل براءات الاختراع.",
            "1. FabLab Needs: High-precision 3D printing (SLA/FDM) for wearable visor chassis, custom PCB milling and assembly, and CNC/laser cutting for mechanical pin matrices.\n2. IoT Lab Needs: Advanced microcontrollers (Arduino Uno R4, ESP32), signal testing tools and oscilloscopes for actuator latency profiling, and micro-stepper motor drivers.\n3. Mentorship Needs: Guidance on hardware miniaturization, battery power management, ergonomic compliance, and intellectual property (IP) filing.",
            "• 3D Printing (Visor Enclosure)\n• Custom Multi-layer PCB Milling\n• Micro-actuator Calibration\n• IP Filing & DFM Mentorship"
        )
    ]
    
    for row_idx, r_data in enumerate(qa_data, 5):
        fill = zebra_fill if row_idx % 2 == 0 else white_fill
        ws3.row_dimensions[row_idx].height = 95
        
        for col_idx, val in enumerate(r_data, 1):
            cell = ws3.cell(row=row_idx, column=col_idx, value=val)
            cell.font = reg_font
            cell.border = border
            cell.fill = fill
            
            if col_idx == 1:
                cell.font = bold_font
                cell.alignment = align_left
            elif col_idx == 2:
                cell.alignment = align_center
            elif col_idx == 5:
                cell.alignment = align_left
                cell.font = bold_font
            else:
                cell.alignment = align_left

    ws3.column_dimensions["A"].width = 28
    ws3.column_dimensions["B"].width = 16
    ws3.column_dimensions["C"].width = 50
    ws3.column_dimensions["D"].width = 50
    ws3.column_dimensions["E"].width = 28


    # =========================================================================
    # SHEET 4: Team ECU & Official Data (الفريق والميزانية)
    # =========================================================================
    ws4 = wb.create_sheet(title="الفريق والميزانية (Team)")
    ws4.views.sheetView[0].showGridLines = True
    
    ws4.merge_cells("A1:G1")
    ws4["A1"] = "Ally Vision — Team Roster, University Data & Budget Breakdown"
    ws4["A1"].font = title_font
    ws4["A1"].alignment = Alignment(horizontal="left", vertical="center")
    
    ws4.merge_cells("A2:G2")
    ws4["A2"] = "بيانات الفريق الرسمي من الجامعة المصرية الصينية (ECU) وجدول توزيع الميزانية لملء الاستمارات"
    ws4["A2"].font = subtitle_font
    
    inst_data = [
        ("الجامعة (University)", "الجامعة المصرية الصينية - Egyptian Chinese University (ECU)"),
        ("الكلية (College / Faculty)", "كلية الهندسة والتكنولوجيا - Faculty of Engineering and Technology"),
        ("المشرف الأكاديمي (Academic Supervisor)", "د. إسلام محمد (Dr. Islam Mohamed)"),
        ("عنوان المشروع الرسمي (Official Title)", "Ally Vision: AI-Powered Assistive Vision & Navigation System for the Blind"),
        ("المجال التقني (Domain)", "الذكاء الاصطناعي، الروبوتات، التكنولوجيا المساعدة، والأنظمة المدمجة (AI, Robotics & Assistive Tech)"),
        ("المرحلة الحالية (Current Stage)", "نموذج أولي متقدم ومختبر برمجياً (Advanced Working Prototype & Simulation)"),
        ("حجم الفريق (Team Size)", "11 مهندساً (Multidisciplinary Engineering Team)"),
        ("رابط مجلد الملفات (Google Drive Folder)", "https://drive.google.com/drive/folders/ally-vision-ecu (يحوي البطاقات، السير الذاتية، المقترح، والـ Deck)")
    ]
    
    ws4.cell(row=4, column=1, value="بيانات المؤسسة والمشروع الأكاديمي").font = section_font
    
    for row_idx, (k, v) in enumerate(inst_data, 5):
        c1 = ws4.cell(row=row_idx, column=1, value=k)
        c2 = ws4.cell(row=row_idx, column=2, value=v)
        c1.font = bold_font
        c2.font = reg_font
        c1.fill = zebra_fill
        c2.fill = white_fill
        c1.border = border
        c2.border = border
        c1.alignment = align_left
        c2.alignment = align_left
        ws4.merge_cells(start_row=row_idx, start_column=2, end_row=row_idx, end_column=5)
        ws4.row_dimensions[row_idx].height = 22

    # Team Members Table
    team_start_row = 15
    ws4.cell(row=team_start_row - 1, column=1, value="قائمة أعضاء الفريق (11 مهندساً)").font = section_font
    
    team_headers = [
        "م",
        "اسم الطالب (Student Name)",
        "الكود الجامعي (Student ID)",
        "الدور والمسؤولية الهندسية في المشروع",
        "البريد الإلكتروني الجامعي",
        "رقم الهاتف",
        "ملاحظات التقديم"
    ]
    
    for c_idx, h in enumerate(team_headers, 1):
        cell = ws4.cell(row=team_start_row, column=c_idx, value=h)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = align_center
        cell.border = border
    ws4.row_dimensions[team_start_row].height = 26
    
    team_members = [
        (1, "عبدالله رضا (Abdallah Reda)", "192200212", "قائد الفريق / مهندس أنظمة الرؤية الحاسوبية والذكاء الاصطناعي (Team Lead & Edge AI)", "abdallah.reda@ecu.edu.eg", "01xxxxxxxxx", "ممثل الفريق في استمارات المسابقات"),
        (2, "فرح تامر (Farah Tamer)", "192200073", "مهندسة معالجة الصور الرقمية والعمق المكاني (Spatial Vision & Depth)", "farah.tamer@ecu.edu.eg", "01xxxxxxxxx", "عضو الفريق"),
        (3, "طه محمد (Taha Mohamed)", "192200144", "مهندس الأنظمة المدمجة وبروتوكولات الاتصال (Embedded Systems & Serial)", "taha.mohamed@ecu.edu.eg", "01xxxxxxxxx", "عضو الفريق"),
        (4, "مصطفى محمد (Mostafa Mohamed)", "192200167", "مهندس تدريب نماذج الذكاء الاصطناعي (YOLOv8 & Model Training)", "mostafa.mohamed@ecu.edu.eg", "01xxxxxxxxx", "عضو الفريق"),
        (5, "ديفيد هاني (David Hany)", "192200193", "مهندس ميكاترونكس والمحركات الدقيقة (Mechatronics & Actuators)", "david.hany@ecu.edu.eg", "01xxxxxxxxx", "عضو الفريق"),
        (6, "سلمى محمد (Salma Mohamed)", "192200198", "مهندسة تصميم مصفوفة اللمس والتحكم الفيزيائي (Tactile Matrix Design)", "salma.mohamed@ecu.edu.eg", "01xxxxxxxxx", "عضو الفريق"),
        (7, "فتحي أحمد (Fathy Ahmed)", "192200211", "مهندس تخطيط الممر الآمن وحساب الزوايا (RANSAC & Path Planning)", "fathy.ahmed@ecu.edu.eg", "01xxxxxxxxx", "عضو الفريق"),
        (8, "محمد محسن (Mohamed Mohsen)", "192200233", "مهندس تصميم الدوائر وتوزيع الطاقة (PCB Layout & Power Management)", "mohamed.mohsen@ecu.edu.eg", "01xxxxxxxxx", "عضو الفريق"),
        (9, "أحمد رجب (Ahmed Ragab)", "192200247", "مهندس تصميم الشاسيه والمحاكاة الميكانيكية (Ergonomics & CAD)", "ahmed.ragab@ecu.edu.eg", "01xxxxxxxxx", "عضو الفريق"),
        (10, "حبيبة سعد (Habiba Saad)", "192300005", "مهندسة واجهات المستخدم والمحاكي الافتراضي (GUI Simulator & Testing)", "habiba.saad@ecu.edu.eg", "01xxxxxxxxx", "عضو الفريق"),
        (11, "هند السيد (Hend Elsayed)", "192300146", "مهندسة توثيق الأبحاث وتجارب المستخدمين (Research & User Testing)", "hend.elsayed@ecu.edu.eg", "01xxxxxxxxx", "عضو الفريق")
    ]
    
    for row_idx, m_data in enumerate(team_members, team_start_row + 1):
        fill = zebra_fill if row_idx % 2 == 0 else white_fill
        ws4.row_dimensions[row_idx].height = 22
        
        for col_idx, val in enumerate(m_data, 1):
            cell = ws4.cell(row=row_idx, column=col_idx, value=val)
            cell.font = reg_font
            cell.border = border
            cell.fill = fill
            
            if col_idx in [1, 3]:
                cell.alignment = align_center
            else:
                cell.alignment = align_left

    # Budget Table
    budget_start_row = 29
    ws4.cell(row=budget_start_row - 1, column=1, value="جدول الميزانية التقديرية المطلوبة للمشروع (Budget Breakdown)").font = section_font
    
    budget_headers = [
        "بند الميزانية (Category)",
        "المكونات والمواصفات التفصيلية",
        "الكمية",
        "التكلفة بالجنيه المصري (EGP)",
        "النسبة من الميزانية",
        "الأهمية والأثر الهندسي"
    ]
    
    for c_idx, h in enumerate(budget_headers, 1):
        cell = ws4.cell(row=budget_start_row, column=c_idx, value=h)
        cell.fill = PatternFill(start_color="334155", end_color="334155", fill_type="solid")
        cell.font = header_font
        cell.alignment = align_center
        cell.border = border
    ws4.row_dimensions[budget_start_row].height = 26
    
    budget_items = [
        ("حساسات الرؤية والعمق (Vision Sensors)", "مستشعر وكاميرا عمق RGB-D (Orbbec Gemini Series / Zed 2i / RealSense) لمسح البيئة ثلاثية الأبعاد بدقة 30 FPS", "1", "20,000 ج", "23.5%", "المكون الأساسي لإدخال البيانات المكانية وكشف العوائق"),
        ("مصفوفة المحركات الدقيقة (Actuator Matrix)", "25 محرك خطوة مصغر فائق الدقة (Miniature Precision Steppers / Voice Coils) لدبابيس مصفوفة الجبهة 5x5", "25", "40,000 ج", "47.0%", "جوهر الابتكار الفيزيائي لتوليد ارتفاعات اللمس الملموسة"),
        ("لوحات التحكم والدوائر (PCBs & Controllers)", "متحكمات Arduino Uno R4 + شرائح قيادة المحركات (DRV8834 Arrays) وتصنيع لوحات PCB مخصصة", "مجموعة", "10,000 ج", "11.8%", "المعالجة المدمجة وتوزيع نبضات المحركات بأقل استهلاك طاقة"),
        ("الهيكل والبطاريات (Ergonomics & Power)", "طباعة هيكل النظارة 3D وحزام الرأس المريح وبطاريات ليثيوم أيون مع دوائر الحماية والشحن", "مجموعة", "7,000 ج", "8.2%", "ضمان راحة الارتداء وخفة الوزن واستمرارية التشغيل الميداني"),
        ("التجارب الميدانية والتأهيل (Field Trials)", "أدوات مسار العوائق، جلسات تدريب المكفوفين، واستمارات تقييم تجربة المستخدم والموثوقية", "مجموعة", "8,000 ج", "9.5%", "التحقق الميداني السريري وجمع النتائج للأطروحة والمسابقات")
    ]
    
    for row_idx, b_data in enumerate(budget_items, budget_start_row + 1):
        fill = zebra_fill if row_idx % 2 == 0 else white_fill
        ws4.row_dimensions[row_idx].height = 24
        
        for col_idx, val in enumerate(b_data, 1):
            cell = ws4.cell(row=row_idx, column=col_idx, value=val)
            cell.font = reg_font
            cell.border = border
            cell.fill = fill
            
            if col_idx in [3, 4, 5]:
                cell.alignment = align_center
                if col_idx == 4:
                    cell.font = bold_font
            else:
                cell.alignment = align_left

    total_row = budget_start_row + len(budget_items) + 1
    ws4.cell(row=total_row, column=1, value="إجمالي الميزانية المطلوبة (Total Required Budget)").font = Font(name=font_family, size=9, bold=True, color="FFFFFF")
    ws4.cell(row=total_row, column=1).fill = header_fill
    ws4.cell(row=total_row, column=1).border = border
    ws4.merge_cells(start_row=total_row, start_column=1, end_row=total_row, end_column=3)
    
    ws4.cell(row=total_row, column=4, value="85,000 ج (~ $1,750)").font = Font(name=font_family, size=10, bold=True, color="FFFFFF")
    ws4.cell(row=total_row, column=4).fill = header_fill
    ws4.cell(row=total_row, column=4).alignment = align_center
    ws4.cell(row=total_row, column=4).border = border
    
    ws4.cell(row=total_row, column=5, value="100%").font = Font(name=font_family, size=10, bold=True, color="FFFFFF")
    ws4.cell(row=total_row, column=5).fill = header_fill
    ws4.cell(row=total_row, column=5).alignment = align_center
    ws4.cell(row=total_row, column=5).border = border
    
    ws4.cell(row=total_row, column=6, value="ميزانية نموذج أولي كامل جاهز للاختبارات السريرية الميدانية").font = Font(name=font_family, size=9, italic=True, color="FFFFFF")
    ws4.cell(row=total_row, column=6).fill = header_fill
    ws4.cell(row=total_row, column=6).border = border

    ws4.column_dimensions["A"].width = 28
    ws4.column_dimensions["B"].width = 38
    ws4.column_dimensions["C"].width = 20
    ws4.column_dimensions["D"].width = 38
    ws4.column_dimensions["E"].width = 28
    ws4.column_dimensions["F"].width = 25

    out_file = r"d:\ECU\GraduationProject\compitiations\Ally_Vision_Competitions_Master_Tracker.xlsx"
    wb.save(out_file)
    print(f"Workbook successfully saved to: {out_file}")

if __name__ == "__main__":
    build_tracker()
