"""
VU Assessment Practice Hub — Streamlit edition
==============================================

A single Streamlit application that combines three tools used by Victoria
University learning designers:

  1. Design Generator  — a guided, backward-design wizard that builds a tailored
                         MS Copilot prompt set for assessment design.
  2. Tools             — Unit LO Builder, Course LO Builder, Rubric Builder,
                         Assessment Checker and a Standards Reference.
  3. Resources         — a curated, topic-filterable library of assessment
                         design resources.

Originally three standalone HTML pages, now unified into one accessible,
deployable web app.

Run locally:
    pip install -r requirements.txt
    streamlit run streamlit_app.py

Author: Learning Design and Innovation, Victoria University
Licence: MIT
"""

from __future__ import annotations

import streamlit as st

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG  (must be the first Streamlit call)
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VU Assessment Practice Hub",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": (
            "VU Assessment Practice Hub — a backward-design assistant, toolkit "
            "and resource library for assessment design at Victoria University."
        )
    },
)

# ─────────────────────────────────────────────────────────────────────────────
# BRAND  (VU Brand Guidelines v1.2)
# ─────────────────────────────────────────────────────────────────────────────
VU_BLUE = "#5BC2E7"
VU_AUBERGINE = "#1E1248"
VU_MELON = "#ED6B5E"
VU_GRAPE = "#B49AD2"
VU_BLUE_TINT = "#e8f7fc"

CUSTOM_CSS = f"""
<style>
  /* Headings + brand accents */
  h1, h2, h3 {{ color: {VU_AUBERGINE}; }}
  .vu-hero {{
      background: {VU_AUBERGINE}; color: #fff; padding: 28px 32px;
      border-radius: 14px; margin-bottom: 8px;
  }}
  .vu-hero h1 {{ color: #fff; margin: 0 0 6px 0; font-size: 1.7rem; }}
  .vu-hero p  {{ color: rgba(255,255,255,.9); margin: 0; font-size: 1rem; line-height: 1.55; }}
  .vu-note {{
      background: rgba(91,194,231,.15); border: 1px solid {VU_BLUE};
      border-radius: 8px; padding: 10px 14px; color: {VU_AUBERGINE};
      font-size: .9rem; line-height: 1.5; margin: 6px 0;
  }}
  .vu-warn {{
      background: #fff4e8; border: 1px solid #f0a040;
      border-radius: 8px; padding: 10px 14px; color: #7a4300;
      font-size: .9rem; line-height: 1.5; margin: 6px 0;
  }}
  .vu-badge {{
      display: inline-block; font-size: .72rem; font-weight: 700;
      padding: 2px 10px; border-radius: 10px; margin-right: 4px;
      background: {VU_BLUE_TINT}; color: #075577;
  }}
  /* Resource / reference card */
  .vu-card {{
      background: #fff; border: 1px solid #CCCCCC; border-radius: 12px;
      padding: 16px 18px; height: 100%;
  }}
  .vu-card h4 {{ color: {VU_AUBERGINE}; margin: 0 0 4px 0; font-size: .98rem; }}
  .vu-card .topic {{
      font-size: .68rem; text-transform: uppercase; letter-spacing: .04em;
      color: #6E6E6E; font-weight: 700; margin-bottom: 6px;
  }}
  .vu-card p {{ font-size: .85rem; color: #262626; line-height: 1.5; margin: 0 0 8px 0; }}
  /* Make Streamlit primary buttons VU melon CTA where used */
  div.stButton > button[kind="primary"] {{
      background: {VU_MELON}; color: {VU_AUBERGINE}; border: none; font-weight: 700;
  }}
  /* Tighten the focus ring for keyboard users (accessibility) */
  :focus-visible {{ outline: 3px solid {VU_AUBERGINE} !important; outline-offset: 2px; }}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def vu_hero(title: str, subtitle: str) -> None:
    """Render the branded hero banner at the top of a page."""
    st.markdown(
        f'<div class="vu-hero"><h1>{title}</h1><p>{subtitle}</p></div>',
        unsafe_allow_html=True,
    )


# ═════════════════════════════════════════════════════════════════════════════
# SHARED DATA
# ═════════════════════════════════════════════════════════════════════════════

TOPIC_GUIDES = [
    ("🎯", "Constructive Alignment", "Outcomes, teaching and assessment are explicitly linked — students achieve what is taught and assessed."),
    ("✏️", "Learning Outcomes", "Measurable statements of what students will know or do, written with a single Bloom's verb at the right AQF level."),
    ("🌍", "Authentic Assessment", "Tasks mirror real professional contexts, asking students to apply knowledge as they would beyond the classroom."),
    ("🪜", "Scaffolded Assessment", "Sequenced tasks build skills progressively, supporting students toward complex, independent performance."),
    ("📊", "Rubric Design", "Criterion-based rubrics define quality descriptors across grade bands, making expectations transparent and marking reliable."),
    ("💬", "Feedback & Feedforward", "Feedback addresses past performance; feedforward guides future improvement. Both should be timely and actionable."),
    ("🤖", "AI & Academic Integrity", "Designing tasks that assess genuine learning while addressing AI-assisted misconduct through secure, contextualised work."),
    ("🔒", "Assessment Security", "Mechanisms that verify individual student achievement — real-time observation, verbal questioning, process documentation."),
    ("🗣️", "Oral Assessment", "Viva voce and interactive oral assessments verify individual understanding and resist AI-assisted misconduct."),
    ("🤝", "Group Assessment", "Group tasks with embedded individual accountability mechanisms, ensuring fair and defensible assessment of each student."),
    ("🏢", "Work-Integrated Learning", "Authentic assessment approaches for WIL and simulated workplace contexts, aligned to graduate employability."),
    ("🌐", "Universal Design for Learning", "UDL reduces barriers for diverse learners by offering flexible means of engagement, representation and expression."),
    ("🌿", "First Nations Perspectives", "Integrating Aboriginal and Torres Strait Islander knowledges as substantive course content, guided by Moondani Balluk — VU's Indigenous Academic Unit."),
]

# Curated resources: (title, topic, type, description, url)
RESOURCES = [
    ("Where to Start: Backward Design (MIT)", "Constructive Alignment", "Guide",
     "MIT's Teaching + Learning Lab introduction to backward design — start with the desired outcomes, then design assessments and learning activities to get there.",
     "https://tll.mit.edu/teaching-resources/course-design/backward-design/"),
    ("Understanding by Design — Resources (McTighe & Associates)", "Constructive Alignment", "Guide",
     "The home of Wiggins & McTighe's Understanding by Design framework. Includes design and assessment tools, videos and podcasts for applying backward design in practice.",
     "https://jaymctighe.com/resources/"),
    ("Constructive Alignment (University of Tasmania)", "Constructive Alignment", "Guide",
     "Practical overview of constructive alignment principles and how to apply them in unit design.",
     "https://www.teaching-learning.utas.edu.au/unit-design/constructive-alignment"),
    ("A Guide to Constructive Alignment in Teaching", "Constructive Alignment", "Video",
     "Claire Killingback's accessible video introduction to constructive alignment for practitioners.",
     "https://youtu.be/ayfgJF0Oj-Y"),
    ("Assessing Process and Product in a Constructively Aligned Subject", "Constructive Alignment", "Article",
     "University of Melbourne case study showing constructive alignment applied in practice.",
     "https://melbourne-cshe.unimelb.edu.au/ai-aai/home/further-reading/university-resources/examples-in-practice/assessing-process-and-product-in-a-constructively-aligned-subject"),
    ("Constructive Alignment (Charles Sturt University)", "Constructive Alignment", "Guide",
     "CSU guide covering the theory and practical application of constructive alignment.",
     "https://www.csu.edu.au/division/learning-teaching/subjects/design-and-development/constructive-alignment"),

    ("AQF Second Edition — Framework Levels", "Learning Outcomes", "Framework",
     "The official AQF publication defining qualification levels; essential for selecting appropriate Bloom's verbs.",
     "https://www.aqf.edu.au/publication/aqf-second-edition"),
    ("Writing Learning Outcomes (UNSW)", "Learning Outcomes", "Guide",
     "Step-by-step guidance from UNSW on constructing clear, measurable learning outcomes.",
     "https://www.teaching.unsw.edu.au/learning-outcomes"),
    ("Creating Learning Outcomes (University of Newcastle)", "Learning Outcomes", "Guide",
     "Practical resource covering outcome structure, Bloom's verbs and alignment to assessment.",
     "https://www.newcastle.edu.au/current-staff/teaching-and-research/teaching-resources/ldti/ldti-teaching-resources/resources/creating-learning-outcomes"),

    ("Choosing Assessment Tasks (Monash University)", "Authentic Assessment", "Guide",
     "Framework for selecting assessment types that reflect professional contexts and learning goals.",
     "https://www.monash.edu/learning-teaching/TeachHQ/Assessment/choosing-assessment-tasks"),
    ("UQ Assessment Ideas Factory", "Authentic Assessment", "Tool",
     "A searchable database of assessment techniques filterable by class size, year level, identity verification, assessment type and more. Includes staff case studies showing each technique in practice.",
     "https://aif.itali.uq.edu.au/"),
    ("Assessment as Learning (UNSW)", "Authentic Assessment", "Guide",
     "UNSW guidance on designing assessment for, as and of learning — including authentic task design.",
     "https://www.teaching.unsw.edu.au/designing-assessment-learning"),
    ("Test Current Assessment Design (Monash University)", "Assessment Security", "Tool",
     "Interactive tool to evaluate how AI-resilient your current assessment tasks are.",
     "https://www.monash.edu/learning-teaching/teachhq/Teaching-practices/artificial-intelligence/ai-and-assessment"),

    ("Scaffolding Assignments (University of Melbourne)", "Scaffolded Assessment", "Article",
     "Explains the rationale for scaffolded assessment design and practical strategies for implementation.",
     "https://www.unimelb.edu.au/tli/news/articles/scaffolding-assignments-how-and-why"),
    ("Design Nested or Staged Assessments (University of Melbourne)", "Scaffolded Assessment", "Guide",
     "One of seven practical strategies for AI-resilient assessment; focuses on staged task design with examples.",
     "https://melbourne-cshe.unimelb.edu.au/ai-aai/home/ai-assessment/designing-assessment-tasks-that-are-less-vulnerable-to-ai/seven-practical-strategies/3.-design-nested-or-staged-assessments"),
    ("Designing Continuous Assessment for Experiential Learning (University of Melbourne)", "Scaffolded Assessment", "Article",
     "Case study of scaffolded, continuous assessment design responding to AI challenges.",
     "https://melbourne-cshe.unimelb.edu.au/ai-aai/home/further-reading/university-resources/examples-in-practice/designing-continuous-assessment-to-support-experiential-and-project-based-learning"),
    ("Authentic Assessment in a Highly Scaffolded Environment (University of Melbourne)", "Scaffolded Assessment", "Article",
     "Example of effective scaffolded authentic assessment design from the University of Melbourne.",
     "https://melbourne-cshe.unimelb.edu.au/ai-aai/home/further-reading/university-resources/examples-in-practice/authentic-assessment-design-in-a-highly-scaffolded-environment"),

    ("Creating and Using Rubrics (UQ)", "Rubric Design", "Guide",
     "Practical guidance on rubric design from UQ's Institute for Teaching and Learning Innovation.",
     "https://itali.uq.edu.au/teaching-guidance/assessment/creating-and-using-rubrics"),
    ("Creating an Analytic Rubric (VU Collaborate)", "Rubric Design", "Guide",
     "Step-by-step guide to building analytic rubrics directly in VU's Collaborate LMS.",
     "https://vucollaboratehelp.vu.edu.au/help-guides/assessment/rubrics/576-creating-an-analytic-rubric"),

    ("Feedback for Learning (UQ)", "Feedback & Feedforward", "Guide",
     "UQ's comprehensive guide to formative and summative feedback, including feedforward principles.",
     "https://itali.uq.edu.au/teaching-guidance/assessment/feedback-learning"),
    ("Creating Feedforward Opportunities (University of Melbourne)", "Feedback & Feedforward", "Article",
     "Explains feedforward as a concept and offers practical strategies for embedding it in assessment design.",
     "https://www.unimelb.edu.au/tli/news/articles/creating-feedforward-opportunities-in-assessment"),
    ("Grading and Giving Feedback (UNSW)", "Feedback & Feedforward", "Guide",
     "UNSW guidance on effective feedback practices, including marking and returning assessment.",
     "https://www.teaching.unsw.edu.au/grading-assessment-feedback"),

    ("VU Student AI Hub", "AI & Academic Integrity", "Guide",
     "VU's central destination for AI support, guidance and policy. Covers responsible and ethical AI use, co-intelligence principles, and the expectation that students develop AI literacy for their studies and careers.",
     "https://libraryguides.vu.edu.au/UnderstandingAI/"),
    ("Module 1 — Understanding AI (VU Library)", "AI & Academic Integrity", "Guide",
     "VU's interactive module introducing generative AI — what it is, how it works, and how to use it responsibly and ethically in studies.",
     "https://libraryguides.vu.edu.au/UnderstandingAI/"),
    ("GenAI in Research (VU Library)", "AI & Academic Integrity", "Guide",
     "VU Library guide on using generative AI tools responsibly and ethically in research contexts.",
     "https://libraryguides.vu.edu.au/GenAI-in-Research"),
    ("AI Literacy for All — Introductory Course (Digital Education Council)", "AI & Academic Integrity", "Guide",
     "Foundation AI literacy course available to all VU staff and students. Covers core AI concepts, responsible use and critical evaluation of AI outputs. VU login required.",
     "https://connect.digitaleducationcouncil.com/saml/4b0e6ea1-9642-4c3b-a215-c7c8719a8e59/login/01e0b431-5470-4e64-a4bc-35ce679c23f3"),
    ("Guide to Using Microsoft Copilot (VU Library)", "AI & Academic Integrity", "Guide",
     "How to access and use Microsoft Copilot responsibly as a VU student or staff member.",
     "https://libraryguides.vu.edu.au/UnderstandingAI/Resources"),
    ("Menus, Not Traffic Lights: AI and Assessment (University of Sydney)", "AI & Academic Integrity", "Article",
     "Influential framework for thinking about AI in assessment using a menu rather than binary allow/prohibit approach.",
     "https://educational-innovation.sydney.edu.au/teaching@sydney/menus-not-traffic-lights-a-different-way-to-think-about-ai-and-assessments/"),
    ("More Than Secure: AI-Collaborative Assessment (UTS)", "AI & Academic Integrity", "Article",
     "Argues for assessment that prepares students for AI-collaborative workplaces, not just secure conditions.",
     "https://educationexpress.uts.edu.au/blog/2025/10/21/more-than-secure-assessments-ai-collaborative-workplace/"),
    ("Guide for Markers of Open Assessments (University of Sydney)", "AI & Academic Integrity", "Guide",
     "How to approach marking polished, AI-assisted student work. Reframes the marker's role around making disciplinary standards visible, focusing on growth, and offering actionable feedback — with example rubric descriptors.",
     "https://educational-innovation.sydney.edu.au/teaching@sydney/"),
    ("Why Feedback Matters More for Open Assessments (University of Sydney)", "AI & Academic Integrity", "Article",
     "Unpacks why feedback is the mechanism that makes open assessments work in the age of generative AI, and offers practical guidance on shifting from policing provenance to developing discernment.",
     "https://educational-innovation.sydney.edu.au/teaching@sydney/"),

    ("Balanced Approach: Secure and Open Assessment (UTS)", "Assessment Security", "Article",
     "UTS resource on designing a balanced portfolio of secure and authentic open assessment tasks.",
     "https://educationexpress.uts.edu.au/blog/2025/10/21/more-than-secure-assessments-ai-collaborative-workplace/"),

    ("VFWA: Voice-First Written Assessment", "Oral Assessment", "Article",
     "Kelly Webb-Davies introduces voice-first written assessment as an AI-resilient alternative to traditional written tasks.",
     "https://kellywebbdavies.substack.com/p/vfwa-voice-first-written-assessment"),
    ("Viva Voce (Charles Sturt University)", "Oral Assessment", "Guide",
     "Guide to viva voce as an assessment method, including design considerations and student preparation.",
     "https://www.csu.edu.au/division/learning-teaching/assessments/assessment-types/viva-voce"),
    ("Interactive Oral Assessment (Curtin University)", "Oral Assessment", "Guide",
     "Curtin's Assessment 2030 resource on designing and implementing interactive oral assessments.",
     "https://www.curtin.edu.au/assessment2030/assessment-design-studio/interactive-oral-assessment/"),
    ("Interactive Oral Assessment in Practice (University of Sydney)", "Oral Assessment", "Guide",
     "University of Sydney guidance on using interactive oral assessments, including practical implementation advice.",
     "https://educational-innovation.sydney.edu.au/teaching@sydney/interactive-oral-assessment-in-practice/"),
    ("Interactive Oral Assessments (University of Melbourne)", "Oral Assessment", "Guide",
     "Melbourne overview of oral assessment design with implementation guidance and discipline case studies.",
     "https://melbourne-cshe.unimelb.edu.au/resources/topics/assessment-and-feedback/specific-help/interactive-oral-assessments"),
    ("Implementing Interactive Oral Assessments — Case Studies (University of Melbourne)", "Oral Assessment", "Guide",
     "Practical case studies showing how interactive oral assessments have been implemented across disciplines.",
     "https://melbourne-cshe.unimelb.edu.au/resources/topics/assessment-and-feedback/specific-help/implementing-interactive-oral-assessments#case-studies"),
    ("Interactive Orals — Ideas Padlet (Griffith University)", "Oral Assessment", "Tool",
     "A community-contributed Padlet of interactive oral assessment ideas across subject areas.",
     "https://padlet.com/griffithu/interactive-orals-a-journey-into-assessment-design-in-your-d-pxavruv51adnbxjj"),
    ("Scheduling Oral Assessments with MS Bookings (University of Sydney)", "Oral Assessment", "Guide",
     "Practical guide to using Microsoft Bookings to manage interactive oral assessment scheduling.",
     "https://docs.google.com/document/d/1raKJ5wQlV_PReD8xXYmlkdI2AhZ8noSjM9mN2dvqoQo/edit"),
    ("A Guide to Oral Exams in Honours (University of Sydney)", "Oral Assessment", "Guide",
     "Kalman & Wright offer a practical guide to designing oral assessments for Honours — from choosing the right format to building rubrics that keep the focus on genuine understanding.",
     "https://educational-innovation.sydney.edu.au/teaching@sydney/"),

    ("Assessing Group Work (UNSW)", "Group Assessment", "Guide",
     "UNSW guidance on designing group assessment with individual accountability and fair contribution mechanisms.",
     "https://www.teaching.unsw.edu.au/assessing-group-work"),
    ("Assessing with Role Plays and Simulations (UNSW)", "Group Assessment", "Guide",
     "UNSW Staff Teaching Gateway resource on using role plays and simulations as authentic assessment methods.",
     "https://www.teaching.unsw.edu.au/assessing-role-plays-and-simulations"),

    ("Assessment Ideas for WIL Project Units (Monash University)", "Work-Integrated Learning", "Guide",
     "A practical PDF guide to assessment equivalents and approaches for work-integrated learning units.",
     "https://www.monash.edu/__data/assets/pdf_file/0003/1654221/Assessment-Equivalents-List-for-WIL.pdf"),
    ("Assessing Work-Integrated Learning Programs (CRADLE/Deakin)", "Work-Integrated Learning", "Guide",
     "CRADLE's comprehensive guide to effective WIL assessment design, from Deakin University.",
     "https://blogs.deakin.edu.au/cradle/wp-content/uploads/sites/188/2022/11/cradle-wil-assessment-guide.pdf"),

    ("UDL Guidelines (CAST)", "Universal Design for Learning", "Framework",
     "The definitive CAST UDL framework — three principles and nine guidelines for flexible, inclusive learning.",
     "https://udlguidelines.cast.org"),
    ("UDL and Assessment in Higher Education (CAST UDL on Campus)", "Universal Design for Learning", "Guide",
     "Applies UDL principles specifically to assessment design in higher education contexts.",
     "https://udloncampus.cast.org/page/assessment_udl"),
    ("UDL in Tertiary Education: Australian Perspectives (Leif et al., 2025)", "Universal Design for Learning", "Research",
     "Recent Australian research on UDL implementation in tertiary education, with practitioner perspectives.",
     "https://research.ebsco.com/c/m7hw3i/viewer/pdf/tiojwkmj6n?route=details"),

    ("Moondani Balluk — Indigenous Academic Unit (VU)", "First Nations Perspectives", "Guide",
     "VU's Indigenous Academic Unit working across Aboriginal community and academic spaces. The first point of contact for embedding First Nations perspectives in curriculum and assessment design.",
     "https://www.vu.edu.au/about-vu/our-uni/moondani-balluk-indigenous-academic-unit"),

    ("How Padlet Supports Relational Feedback (University of Sydney)", "Feedback & Feedforward", "Article",
     "How Sophie Chao and Leanne Williams Green use Padlet to create a living mid-semester feedback conversation with students — with a four-step guide to setting one up.",
     "https://educational-innovation.sydney.edu.au/teaching@sydney/"),
]

# AQF levels for the Unit LO Builder
AQF_LEVELS = {
    5: ("AQF 5 — Diploma", "Broad knowledge with analytical skills; supervised application in a specific area.",
        ["analyse", "apply", "demonstrate", "explain", "compare", "evaluate"]),
    6: ("AQF 6 — Advanced Diploma / Associate Degree", "Technical knowledge and independent problem-solving within defined contexts.",
        ["evaluate", "apply", "design", "analyse", "develop", "interpret"]),
    7: ("AQF 7 — Bachelor", "Broad and coherent theoretical knowledge; autonomous work and learning.",
        ["analyse", "evaluate", "design", "develop", "apply", "synthesise"]),
    8: ("AQF 8 — Honours / Graduate Certificate", "Advanced knowledge; critical evaluation and original application.",
        ["evaluate", "synthesise", "design", "integrate", "develop", "critique"]),
    9: ("AQF 9 — Masters", "Specialised knowledge with high autonomy, research capability and advanced application.",
        ["synthesise", "critique", "evaluate", "generate", "design", "develop"]),
}

BLOOM_VERBS = {
    "Remember": ["define", "identify", "list", "recall", "recognise", "name", "state"],
    "Understand": ["describe", "explain", "interpret", "summarise", "classify", "compare", "illustrate"],
    "Apply": ["apply", "demonstrate", "use", "implement", "execute", "solve", "calculate"],
    "Analyse": ["analyse", "differentiate", "examine", "deconstruct", "contrast", "investigate", "map"],
    "Evaluate": ["evaluate", "critique", "justify", "assess", "argue", "defend", "appraise"],
    "Create": ["design", "develop", "synthesise", "integrate", "construct", "generate", "formulate"],
}

SCHEMES = {
    "HE — HD/D/C/P/N": ["HD", "D", "C", "P", "N"],
    "HE — Pass/Fail": ["Pass", "Fail"],
    "TAFE — S/NYS": ["S", "NYS"],
}

DESCRIPTOR_STYLES = {
    "Generic": {
        "desc": "Broad quality statements applicable to any criterion.",
        "grades": {
            "HD": "Demonstrates outstanding command of the concepts — sophisticated analysis, insightful evaluation and highly polished execution well beyond expectations.",
            "D": "Demonstrates strong understanding with thorough analysis, well-reasoned evaluation and execution that clearly exceeds core requirements.",
            "C": "Demonstrates sound understanding with competent analysis and execution that meets all core requirements.",
            "P": "Demonstrates acceptable understanding with basic analysis and execution that meets minimum requirements.",
            "N": "Does not demonstrate sufficient understanding; fails to meet minimum requirements.",
            "Pass": "Demonstrates satisfactory achievement of the required standard for this criterion.",
            "Fail": "Does not demonstrate the required standard for this criterion.",
            "S": "Satisfactory — demonstrates the required skills, knowledge and understanding to meet the standard for this criterion.",
            "NYS": "Not yet satisfactory — does not yet meet the required standard for this criterion.",
        },
    },
    "SOLO-informed": {
        "desc": "Descriptors based on the Structure of Observed Learning Outcomes (SOLO) taxonomy — focuses on the complexity and integration of student responses.",
        "grades": {
            "HD": "Extended Abstract — response goes beyond the task to generalise, theorise or transfer concepts to new and unfamiliar contexts. Shows original insight and deep structural understanding.",
            "D": "Relational — response integrates all relevant aspects into a coherent whole. Clearly demonstrates relationships between ideas, causes and implications with well-supported reasoning.",
            "C": "Multistructural — response addresses several relevant aspects accurately but without full integration. Covers the key requirements though connections between ideas remain limited.",
            "P": "Unistructural — response identifies one or two relevant aspects of the task. Demonstrates a basic, partial understanding that meets minimum requirements.",
            "N": "Prestructural — response does not engage meaningfully with the task, or is missing, irrelevant or demonstrates significant misunderstanding.",
            "Pass": "Response demonstrates relational or multistructural understanding — addresses the key requirements with adequate connections between ideas.",
            "Fail": "Response does not reach the required standard — engagement is prestructural or unistructural, with significant gaps or misunderstanding.",
            "S": "Satisfactory — response demonstrates multistructural or relational understanding, addressing the key requirements with adequate connections between relevant aspects.",
            "NYS": "Not yet satisfactory — response is prestructural or unistructural; does not yet demonstrate the required depth or integration of understanding.",
        },
    },
    "Bloom's-informed": {
        "desc": "Descriptors anchored to Bloom's Taxonomy cognitive levels — signals the depth of thinking expected at each grade band.",
        "grades": {
            "HD": "Create / Evaluate — student generates original work, synthesises ideas from multiple sources, or makes sophisticated evaluative judgements with well-justified, evidence-based reasoning.",
            "D": "Evaluate / Analyse — student critically evaluates competing perspectives, analyses complex relationships and demonstrates clear, well-supported reasoning that goes beyond description.",
            "C": "Apply / Analyse — student applies relevant concepts and procedures accurately to the given context and begins to analyse patterns, relationships or implications.",
            "P": "Understand / Apply — student demonstrates understanding of core concepts and can apply them in straightforward contexts, though analysis may be limited or partially developed.",
            "N": "Remember / below threshold — response is limited to recall or is largely incomplete; does not demonstrate sufficient understanding or application to meet the required standard.",
            "Pass": "Apply or above — student demonstrates the ability to apply relevant knowledge and skills in the required context, meeting the cognitive demands of the learning outcome.",
            "Fail": "Below Apply — student does not demonstrate sufficient application of knowledge or skills to meet the required standard.",
            "S": "Apply or above — student demonstrates the ability to apply relevant knowledge and skills to meet the competency standard for this criterion.",
            "NYS": "Below Apply — student has not yet demonstrated the required application of knowledge or skills to meet the competency standard.",
        },
    },
}

# Assessment Checker — standards
HE_STANDARDS = [
    ("Assessment Design", [
        ("1.1", "Each unit has 2–3 assessment tasks (neither too few nor excessive)"),
        ("1.2", "Assessments are constructively aligned to learning outcomes"),
        ("1.3", "Assessment tasks are authentic and reflect professional or real-world contexts"),
        ("1.4", "Assessment tasks are scaffolded and sequenced across the unit"),
        ("1.5", "An early low-stakes task is scheduled in Week 1 to support student transition"),
    ]),
    ("Assessment Security", [
        ("4.1", "At least 50% of unit marks are earned under secure, individually verified conditions"),
        ("4.2", "Group tasks include mechanisms for individual accountability"),
        ("4.3", "Security mechanisms are named explicitly in CAMS (e.g. real-time observation, viva, annotated process log)"),
        ("4.4", "All learning outcomes are assessed at least once under individual conditions"),
    ]),
    ("Feedback", [
        ("5.1", "Students receive formative feedback before the final summative task"),
        ("5.2", "Feedback is provided within 15 business days for major tasks"),
        ("5.3", "Feedforward guidance is embedded in task design or feedback processes"),
    ]),
    ("Moderation & Marking", [
        ("6.1", "A marking rubric or guide is attached to every assessed task in CAMS"),
        ("6.2", "Pre-marking calibration is conducted when multiple markers assess the same task"),
        ("6.3", "Post-marking moderation processes are in place"),
    ]),
    ("AQF & Accreditation", [
        ("7.1", "Learning outcomes are written at the cognitive level appropriate to the qualification's AQF level"),
        ("7.2", "Assessment tasks demand cognitive complexity consistent with the AQF level"),
        ("7.3", "Assessment complies with VU policy and any relevant accreditation requirements (e.g. Engineers Australia)"),
    ]),
]

TAFE_STANDARDS = [
    ("Competency Design", [
        ("T1.1", "Assessment tasks are mapped directly to unit elements and performance criteria"),
        ("T1.2", "Tasks cover all required performance evidence and knowledge evidence"),
        ("T1.3", "Tasks reflect realistic workplace contexts relevant to the qualification"),
    ]),
    ("Evidence & Judgement", [
        ("T2.1", "Assessment methods generate sufficient evidence to make a valid S/NYS decision"),
        ("T2.2", "Evidence requirements are clearly described for students"),
        ("T2.3", "Assessors have applied assessment conditions consistently"),
    ]),
    ("Validation & Moderation", [
        ("T3.1", "Assessment tools have been validated against the training package"),
        ("T3.2", "Moderation processes ensure consistent judgement across assessors"),
    ]),
]

STANDARDS_REF = [
    ("S1", "HE", "Assessment volume", "Units must have 2–3 tasks; sufficient to assess all LOs without excessive burden."),
    ("S2", "HE/TAFE", "Constructive alignment", "Tasks, LOs and teaching activities are explicitly aligned."),
    ("S3", "HE", "Authentic design", "Tasks reflect real-world professional contexts and the discipline."),
    ("S4", "HE", "Scaffolding", "Tasks are sequenced so earlier work builds capacity for later tasks."),
    ("S5", "HE", "Early assessment", "A low-stakes task is scheduled in Week 1 of the block."),
    ("S6", "HE", "50% secure mark", "At least half of all marks are earned under secure, individually verified conditions."),
    ("S7", "HE/TAFE", "Individual accountability", "Group tasks include mechanisms to verify individual contribution and understanding."),
    ("S8", "HE", "Named security mechanisms", "CAMS must name the specific mechanism: real-time observation, viva, or annotated process log."),
    ("S9", "HE/TAFE", "Timely feedback", "Feedback within 15 business days for major tasks; formative feedback before final tasks."),
    ("S10", "HE/TAFE", "Rubrics required", "Every assessed task has a criterion-based rubric or marking guide in CAMS."),
    ("S11", "HE/TAFE", "Calibration", "Pre-marking calibration is required when multiple assessors mark the same task."),
    ("S12", "HE", "AQF alignment", "LO complexity and assessment demands match the qualification's AQF level."),
    ("T1", "TAFE", "Performance criteria mapping", "Tasks directly address the elements and performance criteria of the unit of competency."),
    ("T2", "TAFE", "Evidence requirements", "Tasks capture all required performance and knowledge evidence."),
    ("T3", "TAFE", "Tool validation", "Assessment tools are validated against the training package before use."),
]

# Graduate Capabilities (CLO Builder)
GC_DATA = [
    ("GC1", "Adaptable and capable 21st century citizens", [
        ("GC1a", "Identifying, anticipating and solving problems ranging from simple to important, complex and unpredictable"),
        ("GC1b", "Accessing, evaluating and analysing information"),
        ("GC1c", "Effective communication using known and yet-to-be-developed tools in many contexts"),
        ("GC1d", "Using effective interpersonal skills, collaborating with and influencing personal, work and community networks locally and globally"),
    ]),
    ("GC2", "Confident, creative lifelong learners", [
        ("GC2a", "Understanding the role of culture, values and dispositions in affecting achievement of goals"),
        ("GC2b", "Understanding how to initiate and develop new ideas"),
        ("GC2c", "Planning and organising self and others"),
        ("GC2d", "Decision-making"),
    ]),
    ("GC3", "Responsible and ethical citizens", [
        ("GC3a", "Respecting and valuing diversity"),
        ("GC3b", "Developing capacities required to contribute to a more equitable and sustainable world, including courage and resilience"),
        ("GC3c", "Understanding the workings of local and global communities and individual responsibilities within these"),
        ("GC3d", "Understanding the intricacies of balancing individual and public good"),
    ]),
]

ESF_DATA = [
    ("💬 Communication", "Sharing ideas clearly through writing, speaking, listening and digital tools — respectfully and appropriately for the audience."),
    ("🤝 Teamwork & Collaboration", "Working well with others by listening, sharing ideas, being respectful and bringing strengths to help the group succeed."),
    ("💡 Critical Thinking & Problem Solving", "Figuring things out, breaking down complex ideas, asking thoughtful questions and using judgement to make informed decisions."),
    ("🚀 Creativity & Innovation", "Imagining new ideas and having the confidence to bring them to life through curiosity, experimentation and testing."),
    ("💻 Digital Literacy & GenAI Skills", "Confidently using digital tools and AI in smart, safe and ethical ways to research, design, communicate and solve problems."),
    ("📖 Self-Management & Lifelong Learning", "Knowing yourself, staying organised, being curious and open to growth, and managing time and energy with resilience."),
    ("🌱 Ethical & Global Citizenship", "Doing the right thing for yourself, others and the world — showing respect, understanding cultures and contributing to a fairer, sustainable world."),
]

# Heuristics for CLO analysis
WEAK_VERBS = ["understand", "know", "learn", "appreciate", "be aware", "be familiar",
              "gain", "develop an understanding", "explore"]
COMPOUND_SIGNALS = [" and ", "; ", " as well as ", " while also ", " in addition to "]
CONTENT_SIGNALS = ["introduction to", "overview of", "concepts of", "principles of",
                   "theories of", "history of", "study of"]

RESOURCE_TYPE_COLORS = {
    "Article": "#075577", "Guide": "#1a5e2a", "Framework": "#3d2278",
    "Policy": "#7a4300", "Video": "#8b2a1e", "Tool": "#1a5e2a", "Research": "#3d2278",
}


# ═════════════════════════════════════════════════════════════════════════════
# PROMPT BUILDERS  (ported from the original JavaScript)
# ═════════════════════════════════════════════════════════════════════════════

def build_master_prompt(d: dict) -> str:
    """Build the master MS Copilot prompt from collected wizard data."""
    context_str = ", ".join(d["contexts"]) if d["contexts"] else "standard classroom delivery"
    include_str = ", ".join(d["includeTypes"]) if d["includeTypes"] else "a range of appropriate task types"
    avoid_str = (f"Do not suggest the following assessment types: {', '.join(d['avoidTypes'])}."
                 if d["avoidTypes"] else "")
    esf_str = ", ".join(d["esf"]) if d["esf"] else "general graduate employability skills"

    if d["taskConfigs"]:
        task_str = "\n".join(
            f"  Task {i + 1}: {t['name']} (approx. {t['weight']}%)"
            for i, t in enumerate(d["taskConfigs"])
        )
    else:
        task_str = "  [To be determined by Copilot based on context]"

    early_str = " or ".join(d["earlyTask"]) if d["earlyTask"] else "a low-stakes introductory task"

    contexts_lower = [c.lower() for c in d["contexts"]]
    has_wil = any("wil" in c or "placement" in c or "clinical" in c for c in contexts_lower)
    has_lab = any("lab" in c for c in contexts_lower)
    is_pass_fail = "pass/fail" in d["grading"]

    hurdle_str = ""
    if d["hasHurdle"]:
        detail = f": {d['hurdleDetail']}" if d["hurdleDetail"] else ""
        hurdle_str = (
            f"\nHURDLE REQUIREMENT: This unit includes a must-pass hurdle — {d['hurdleType']}{detail}. "
            "Students must meet this requirement regardless of their overall grade. "
            "The hurdle task must be designed and assessed separately from the graded assessment structure."
        )

    overview_block = f"\n\nUnit overview:\n{d['overview']}" if d["overview"] else ""
    clos_block = f"\nMapped Course Learning Outcomes (CLOs):\n{d['clos']}" if d["clos"] else ""
    format_str = ", ".join(d["format"]) if d["format"] else "standard delivery"

    respondus_block = (
        "\nNote: Brightspace quiz with Respondus Lockdown Browser is available as a secure "
        "assessment mechanism. This locks down the student's device and supports long-answer "
        "and free-writing questions — not just multiple choice."
        if d["hasRespondus"] else ""
    )
    udl_str = ", ".join(d["udlModes"]) if d["udlModes"] else "not specified — recommend variety"
    integrity_block = (f"Security & integrity focus areas: {', '.join(d['integrityFocus'])}"
                       if d["integrityFocus"] else "")

    group_block = ""
    if d["hasGroupWork"]:
        collab = d["collabULO"] if d["collabULO"] else "[see ULOs above]"
        group_block = (
            "\nGROUP ASSESSMENT: This unit includes a group task.\n"
            f"- The ULO requiring collaboration is: {collab}\n"
            "- Individual accountability is required in line with VU's Assessment Procedure, but the "
            "mechanism is a design decision — suggest the most appropriate approach for this unit "
            "context, cohort size and delivery mode\n"
            "- Each student must be able to demonstrate they have addressed the learning outcomes "
            "mapped to this task\n"
            "- Where group assessment accounts for 50% or less of total unit marks, separate shared "
            "and individual marks are not mandatory. However, best practice is to include both: "
            "shared criteria for the group product (strengthens validity) and individual criteria for "
            "collaborative behaviours and contribution (promotes learner engagement and makes "
            "individual learning visible). Please recommend this approach and explain its benefits, "
            "while noting it is not a mandatory requirement at this weighting."
        )
    extra_block = f"\nAdditional context:\n{d['extraContext']}" if d["extraContext"] else ""

    # Build the standards list (numbered cleanly to avoid duplicate numbering)
    standards = [
        "The unit must have 2–3 assessment tasks.",
        "Each task must be constructively aligned — providing direct evidence of one or more ULOs.",
        "At least one task must be scheduled in Week 1 of the block as a low-stakes transition task.",
        "At least 50% of marks must be earned under secure, individually verified conditions.",
        "Group tasks are only valid where a ULO explicitly requires teamwork or collaboration. "
        "Individual accountability must be addressed — the mechanism is a professional judgement "
        "appropriate to the context. Where group assessment is 50% or less of total unit marks, "
        "separate shared and individual marks are not mandatory, but are best practice for validity "
        "and learner engagement. Every student must be able to demonstrate achievement of the mapped "
        "learning outcomes.",
        "Security mechanisms must be explicitly named (real-time observation, viva/verbal questioning, "
        "annotated process documentation log, or Brightspace quiz with Respondus lockdown).",
        "Assessment tasks must be authentic — reflecting real-world professional contexts relevant to "
        "the discipline.",
        "Tasks must be scaffolded so earlier tasks build capability for later ones.",
        "Apply Universal Design for Learning (UDL) principles: across the task sequence, offer multiple "
        "means of expression so students can demonstrate learning in different ways. This increases "
        "accessibility, inclusiveness and engagement, and better reflects the range of professional "
        "communication expected of graduates. Do not prescribe a single format across all tasks.",
    ]
    if is_pass_fail:
        standards.append(
            "This unit uses pass/fail grading. All tasks should be designed around a clear pass "
            "standard, and assessment criteria should describe what 'satisfactory' looks like rather "
            "than grade bands."
        )
    else:
        standards.append(
            "This unit uses graded assessment (HD/D/C/P/N). Rubric descriptors should make the quality "
            "progression visible across all grade bands."
        )
    if d["hasHurdle"]:
        standards.append(
            "HURDLE: The must-pass hurdle task must be treated as a separate, non-compensable "
            "requirement. Design it with clear, observable pass criteria and consider how it will be "
            "assessed and communicated to students."
        )
    if has_wil:
        standards.append(
            "WIL/placement assessment must connect workplace learning to ULOs and include individual "
            "reflection or verification of competency."
        )
    if has_lab:
        standards.append(
            "Laboratory assessment must include individual accountability (e.g. lab reports, vivas, or "
            "annotated lab notebooks)."
        )
    standards_block = "\n".join(f"{i + 1}. {s}" for i, s in enumerate(standards))

    hurdle_produce = ("\n   - Whether this is the hurdle task, and if so, the pass criteria"
                      if d["hasHurdle"] else "")

    sep = "━" * 35
    return f"""You are an expert higher education assessment designer with deep knowledge of backward design, constructive alignment, authentic assessment, and academic integrity in Australian higher education.

I need you to design a complete assessment structure for the following unit. Use a BACKWARD DESIGN approach throughout: start with the desired learning outcomes, design assessments that provide evidence of those outcomes, then consider the teaching and learning activities needed to prepare students.

{sep}
UNIT CONTEXT
{sep}
Unit: {d['unitName'] or '[Unit name]'}
Discipline / College: {d['discipline'] or '[Discipline]'}
AQF qualification level: {d['aqf'] or '[AQF level]'}
Year / stage of program: {d['year'] or '[Year/stage]'}
Delivery mode: {d['delivery']}
Delivery format: {format_str}
Cohort size: {d['cohort']}
Special contexts: {context_str}
Grading scheme: {d['grading']}{hurdle_str}{overview_block}

{sep}
LEARNING OUTCOMES
{sep}
Unit Learning Outcomes (ULOs):
{d['ulos'] or '[ULOs not provided — infer appropriate outcomes from the unit context and AQF level]'}
{clos_block}

VU Employability Skills this unit develops: {esf_str}

{sep}
ASSESSMENT STRUCTURE
{sep}
Number of tasks: {d['taskCount'] or '2–3 (recommend based on context)'}
Structure type: {d['structure']}
Planned tasks:
{task_str}

Early transition task (Week 1): {early_str}

Assessment emphasis: {d['approach']}
Assessment types to consider: {include_str}
UDL — means of expression across tasks: {udl_str}
{avoid_str}{respondus_block}

AI and openness approach: {d['aiApproach']}

Note on VU's AI principles: VU takes a co-intelligence approach — AI is a partner in learning, not a replacement for thinking. Students are expected to use AI responsibly, critically and ethically. Assessment design should develop students' capacity to use AI purposefully in their discipline, not simply prevent its use.
{integrity_block}{group_block}{extra_block}

{sep}
VU HE ASSESSMENT STANDARDS (must comply)
{sep}
{standards_block}

{sep}
WHAT TO PRODUCE
{sep}
Please provide:

1. ASSESSMENT STRUCTURE
   For each task, provide:
   - Task name and type
   - Weighting (%) and timing within the delivery period
   - ULOs assessed (with rationale)
   - CLOs and employability skills addressed
   - Description of the task (2–3 sentences)
   - How the task fits the scaffolding/structure type specified
   - Security mechanism — how individual understanding is verified
   - AI position for this task{hurdle_produce}

2. CONSTRUCTIVE ALIGNMENT TABLE
   Map each task to: ULOs / CLOs / Employability Skills / VU Assessment Standards met.

3. BACKWARD DESIGN RATIONALE
   Explain why this structure achieves the stated learning outcomes, how it reflects backward design, and how the scaffolding type supports student progression.

4. ADMINISTRATION & MARKING CONSIDERATIONS
   For each task:
   - Potential challenges (marking load, logistics, equity, AI misuse)
   - Strategies to address each challenge
   - Suggested marking approach and moderation strategy

5. FEEDFORWARD STRATEGY
   How feedback from each task is structured to prepare students for the next.

Be specific to the discipline and context. Avoid generic or template-like suggestions."""


def build_modular_prompts(d: dict) -> list[dict]:
    """Return the six modular follow-up prompts."""
    unit_ref = f"for {d['unitName']}" if d["unitName"] else "for this unit"
    is_pass_fail = "pass/fail" in d["grading"]
    cohort = d["cohort"] or "this cohort size"
    has_wil = any("wil" in c.lower() or "placement" in c.lower() for c in d["contexts"])
    esf_join = ", ".join(d["esf"]) if d["esf"] else "communication, critical thinking, collaboration"

    rubric_pf = ("- This is a pass/fail unit — descriptors should clearly define what satisfactory "
                 "performance looks like for each criterion, rather than using grade bands"
                 if is_pass_fail else
                 "- Include descriptors for HD, D, C, P and N that clearly distinguish quality levels")
    rubric_hurdle = ("\n- For the hurdle task, provide clear pass/fail criteria with observable "
                     "performance indicators" if d["hasHurdle"] else "")

    ai_menu = ("Provide a detailed menu-style AI permissions framework — specifying what AI use is "
               "permitted, must be disclosed, or is not permitted for each task"
               if "menu" in d["aiApproach"] else
               "How to brief students on AI expectations in a way that is educative rather than punitive")
    admin_wil = ("\n7. How to manage WIL/placement assessment variability across different workplace "
                 "contexts" if has_wil else "")

    return [
        {"icon": "📋", "title": "Rubric design",
         "desc": "Generate detailed rubric descriptors for each task.",
         "prompt": f"""Based on the assessment structure designed {unit_ref}, create detailed marking rubrics for each task.

For each rubric:
- Use criterion-based design with 4–5 criteria per task
- Write descriptors using SOLO taxonomy language (Extended Abstract → Prestructural) to make quality progression visible
{rubric_pf}
- Link each criterion explicitly to the relevant ULO(s)
- Include criterion weightings that sum to 100%
- Flag which criteria relate to the secure/verified component of the task{rubric_hurdle}

Make descriptors specific to the discipline and task — avoid generic language."""},

        {"icon": "🔒", "title": "Security & integrity",
         "desc": "Strengthen assessment security and integrity design.",
         "prompt": f"""Review the assessment structure designed {unit_ref} and provide detailed guidance on security and academic integrity.

1. For each task, describe a specific, implementable security mechanism — including how it works in practice for {cohort}. Options include:
   - Real-time observation (in class or via video)
   - Viva / verbal questioning (individual or spot-check)
   - Annotated process documentation log
   - Brightspace quiz with Respondus Lockdown Browser (supports long-answer and free writing — not just multiple choice)

2. How to design viva or oral verification to be efficient, equitable and low-anxiety for students

3. How to structure any group tasks so individual contribution is separately verifiable

4. {ai_menu}

5. How to brief students on academic integrity expectations

Reference the VU requirement that at least 50% of marks must be individually verified."""},

        {"icon": "📊", "title": "Administration & marking",
         "desc": "Address marking load, logistics and moderation.",
         "prompt": f"""For the assessment structure designed {unit_ref}, provide a practical administration and marking plan.

1. Estimated marking time per student per task, and total load for {cohort}
2. Strategies to manage marking load without compromising quality
3. A pre-marking calibration process for each task
4. A moderation plan ensuring consistency across markers
5. A feedback return timeline meeting VU's 15-business-day standard, enabling feedforward between tasks
6. Logistical risks and mitigation strategies{admin_wil}
7. Suggested Brightspace tools to support marking and feedback return"""},

        {"icon": "💬", "title": "Feedback & feedforward",
         "desc": "Design a feedback strategy that supports growth.",
         "prompt": f"""Design a comprehensive feedback and feedforward strategy {unit_ref}.

1. For each task: what to comment on, in what format, and how it links forward to the next task
2. How to structure feedback so students can act on it — not just receive a grade
3. A feedforward prompt directing students to use Task 1 feedback when completing Task 2
4. Mid-semester formative feedback opportunities that don't add marking load (e.g. Padlet, draft submissions, peer review)
5. How to tailor feedback for students who may be at risk or disengaged
6. Suggested language that is growth-oriented and discipline-appropriate

Reference: feedback is the mechanism that makes open assessment work in the age of generative AI (University of Sydney, 2024)."""},

        {"icon": "🌍", "title": "Authentic task design",
         "desc": "Deepen real-world relevance of each task.",
         "prompt": f"""Enhance the authenticity and real-world relevance of the assessment tasks designed {unit_ref}.

For each task:
1. The specific professional practice or workplace scenario the task mirrors
2. A realistic brief, client or industry context that could frame the task
3. Which VU Employability Skills ({esf_join}) are most visible, and how to make them explicit to students
4. How a practitioner or industry partner could be involved (light-touch: brief provider, reviewer, or panel member)
5. How the task prepares students for graduate employment or further study

Authentic tasks should require genuine judgement, have realistic consequences, mirror professional contexts, and resist simple AI generation."""},

        {"icon": "🌐", "title": "UDL & equity",
         "desc": "Apply UDL principles to increase accessibility and inclusiveness.",
         "prompt": f"""Apply Universal Design for Learning (UDL) principles to the assessment structure designed {unit_ref}.

UDL is built on three core principles: multiple means of ENGAGEMENT (why students learn), multiple means of REPRESENTATION (what students learn), and multiple means of EXPRESSION (how students demonstrate learning). In assessment design, the third principle is most critical: offering students varied ways to demonstrate achievement increases accessibility, inclusiveness and engagement with learning — and reduces barriers without reducing rigour.

1. For each task, 2–3 flexible options for demonstrating the same learning without reducing rigour
2. How to build student choice without creating marking inequity
3. Specific adjustments benefiting first-in-family, CALD, or students with disability — without singling them out
4. How to write task instructions that are clear, unambiguous and free of cultural or linguistic bias
5. Equity risks in the current design and how to mitigate them

Reference the CAST UDL framework: reducing barriers in design benefits all students, not just those with identified needs."""},
    ]


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: HOME
# ═════════════════════════════════════════════════════════════════════════════

def page_home() -> None:
    vu_hero(
        "Assessment Practice Hub",
        "A backward-design assistant, toolkit and resource library for assessment design at "
        "Victoria University — built for VU Higher Education delivery on Australian campuses.",
    )
    st.write("")
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.container(border=True):
            st.subheader("✨ Design Generator")
            st.write("Answer a few questions about your unit and generate a tailored MS Copilot "
                     "prompt set for a backward-designed, authentic, secure assessment structure.")
            if st.button("Open Design Generator", use_container_width=True, key="home_dg"):
                _goto("✨ Design Generator")
    with c2:
        with st.container(border=True):
            st.subheader("🛠️ Tools")
            st.write("Build unit and course learning outcomes, craft rubrics, check your design "
                     "against VU Assessment Standards, and browse the standards reference.")
            if st.button("Open Tools", use_container_width=True, key="home_tools"):
                _goto("🛠️ Tools")
    with c3:
        with st.container(border=True):
            st.subheader("📚 Resources")
            st.write("A curated, topic-filterable library of assessment design readings, guides, "
                     "frameworks and tools from VU and across the sector.")
            if st.button("Open Resources", use_container_width=True, key="home_res"):
                _goto("📚 Resources")

    st.write("")
    st.markdown(
        '<div class="vu-note">This tool is designed for VU Higher Education delivery on Australian '
        'campuses (Melbourne, Sydney and Brisbane). For VET/TAFE assessment design, use the VET '
        'pathway in the Tools section\'s Assessment Checker.</div>',
        unsafe_allow_html=True,
    )

    with st.expander("ℹ️ About this app & accessibility"):
        st.markdown(
            """
This is a Streamlit rebuild of three VU Assessment Practice Hub pages, combined into one app.

**Accessibility features**
- Logical heading structure and keyboard-navigable controls throughout.
- Every status uses **text + icon**, never colour alone, so it works for colour-blind users and screen readers.
- Copyable prompts use Streamlit's native code blocks, which expose an accessible *copy* button.
- High-contrast VU palette and a visible focus outline for keyboard users.
- A single, linear page per tool — no hidden steps — which is friendlier for assistive technology.

**Privacy** — everything runs in your browser session. Nothing you type is stored or sent anywhere.
            """
        )


def _goto(page_label: str) -> None:
    st.session_state["nav"] = page_label
    st.rerun()


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: DESIGN GENERATOR  (the 7-step wizard, rendered as a single linear page)
# ═════════════════════════════════════════════════════════════════════════════

DELIVERY_OPTIONS = {
    "4-week Block (Undergraduate) — all Australian campuses": "4-week Block Model (undergraduate)",
    "4-week Block (Postgraduate) — select programs": "4-week Block Model (postgraduate)",
    "8-week Block (Postgraduate) — select programs": "8-week Block Model (postgraduate)",
    "Other — research, intensive or compressed": "non-standard or intensive delivery (e.g. research, compressed or accelerated schedule)",
}
GRADING_OPTIONS = {
    "Graded (HD / D / C / P / N)": "graded (HD/D/C/P/N)",
    "Pass / Fail (no grade bands)": "pass/fail (no grade bands)",
}
STRUCTURE_OPTIONS = {
    "🪜 Scaffolded — each task builds on the previous": "scaffolded — each task builds capability for the next, with earlier tasks providing formative preparation for later ones",
    "🪆 Nested — earlier work feeds into the final task": "nested — a later task incorporates or synthesises evidence from earlier tasks, so earlier work feeds directly into the final submission",
    "🔄 Progressive / iterative — staged submissions, one final grade": "progressive with iterative development — students make regular staged submissions of parts of a larger work, receiving feedback on each before a single final submission and grade",
    "⚡ Parallel / independent — tasks assess different outcomes": "parallel — tasks assess different outcomes independently, each standing alone without building on the others",
}
APPROACH_OPTIONS = {
    "🌍 Open emphasis — authentic tasks + embedded secure verification": "primarily authentic open assessment tasks, with embedded secure verification mechanisms (e.g. viva, oral defence, or annotated process log) to meet the 50% individually verified requirement",
    "🔒 Secure emphasis — individually verified tasks + authentic application": "primarily secure individually verified assessment, with authentic application tasks that reflect real professional contexts",
}
AI_OPTIONS = {
    "🔒 Secure & unaided — no AI, verified conditions": "secure tasks where AI is not appropriate — students demonstrate individual disciplinary knowledge and skill under verified conditions, without AI assistance. This approach is appropriate where the outcome requires unaided professional judgement (e.g. clinical reasoning, safety-critical decisions, foundational knowledge acquisition)",
    "🌍 Open with purposeful AI use — AI as a learning partner": "open tasks with purposeful, responsible AI use — students use AI as a co-intelligence tool as they would in professional practice, developing critical AI literacy alongside disciplinary capability. Individual understanding is verified through secure mechanisms (viva, oral defence, annotated process log)",
    "📋 Menu approach — defined AI uses + mandatory disclosure": "open tasks with defined AI uses and mandatory disclosure — a menu-style approach where specific AI uses are permitted per task and must be declared by students, with individual understanding verified through secure mechanisms",
    "⚖️ Mixed approach — some AI-purposeful, some secure & unaided": "mixed approach — some tasks use AI purposefully to develop co-intelligence skills; others are secure and unaided to verify foundational disciplinary knowledge. Both types include individual verification mechanisms",
    "🤔 Not yet decided — recommend the best approach": "approach to be determined — recommend the most appropriate AI and openness approach for this unit, discipline, AQF level and cohort, consistent with VU's co-intelligence principles",
}

CONTEXT_CHIPS = [
    "Work-integrated learning (WIL) / placement", "Laboratory / practical sessions",
    "Clinical placement", "Studio / workshop", "Field work", "Industry partner involvement",
    "International students majority", "First-year / transition cohort",
]
ESF_CHIPS = [
    "Communication", "Teamwork & Collaboration", "Critical Thinking & Problem Solving",
    "Creativity & Innovation", "Digital Literacy & GenAI Skills",
    "Self-Management & Lifelong Learning", "Ethical & Global Citizenship",
]
HURDLE_CHIPS = [
    "Must-pass placement / WIL task", "Must-pass clinical or professional conduct task",
    "Must-pass safety or compliance task", "Must-pass final exam or test",
    "Other hurdle requirement",
]
EARLY_CHIPS = [
    "Short quiz or knowledge check", "Diagnostic reflection", "Initial draft or outline",
    "Professional profile or introduction", "Case study analysis (short)",
    "Lab notebook / process log entry", "Part of the progressive/iterative task",
    "Copilot / AI tool to determine best fit",
]
INCLUDE_CHIPS = [
    "Written report / essay", "Case study analysis", "Project / design artefact",
    "Portfolio / process log", "Oral / viva / presentation", "Practical demonstration",
    "Group project", "Reflective journal", "Brightspace quiz (Respondus lockdown)",
    "WIL / placement task", "Lab report", "Simulation / role play",
]
UDL_CHIPS = [
    "Written expression (report, essay, case study)",
    "Oral / verbal expression (viva, presentation, discussion)",
    "Visual / multimodal expression (diagram, poster, video)",
    "Practical / applied demonstration",
    "Reflective / process-based expression (journal, log, portfolio)",
    "Digital / technology-mediated expression",
]
AVOID_CHIPS = [
    "Closed-book invigilated exam", "Group work", "Oral assessment",
    "Time-constrained test", "Take-home essay",
]
INTEGRITY_CHIPS = [
    "Contract cheating", "AI-generated submissions", "Collusion between students",
    "Verifying student identity", "Ensuring marks reflect genuine learning",
    "Marking consistency across a large cohort",
]


def _collect_design_data() -> dict:
    ss = st.session_state
    delivery_label = ss.get("dg_delivery", list(DELIVERY_OPTIONS)[0])
    grading_label = ss.get("dg_grading", list(GRADING_OPTIONS)[0])
    structure_label = ss.get("dg_structure", list(STRUCTURE_OPTIONS)[0])
    approach_label = ss.get("dg_approach", list(APPROACH_OPTIONS)[0])
    ai_label = ss.get("dg_ai", list(AI_OPTIONS)[0])

    task_count = int(ss.get("dg_task_count", "2 tasks").split()[0])
    task_configs = []
    for i in range(task_count):
        name = ss.get(f"dg_task_name_{i}", "").strip() or f"Task {i + 1}"
        weight = ss.get(f"dg_task_weight_{i}", 0)
        task_configs.append({"name": name, "weight": weight if weight else "TBC"})

    hurdle_sel = ss.get("dg_hurdle", [])
    include_types = ss.get("dg_include", [])

    return {
        "unitName": ss.get("dg_unit_name", "").strip(),
        "discipline": ss.get("dg_discipline", "").strip(),
        "aqf": ss.get("dg_aqf", ""),
        "year": ss.get("dg_year", ""),
        "overview": ss.get("dg_overview", "").strip(),
        "delivery": DELIVERY_OPTIONS[delivery_label],
        "cohort": f"{ss.get('dg_cohort', 35)} students",
        "format": ss.get("dg_format", []),
        "contexts": ss.get("dg_contexts", []),
        "grading": GRADING_OPTIONS[grading_label],
        "hasHurdle": len(hurdle_sel) > 0,
        "hurdleType": ", ".join(hurdle_sel),
        "hurdleDetail": ss.get("dg_hurdle_detail", "").strip(),
        "ulos": ss.get("dg_ulos", "").strip(),
        "clos": ss.get("dg_clos", "").strip(),
        "esf": ss.get("dg_esf", []),
        "taskCount": task_count,
        "taskConfigs": task_configs,
        "structure": STRUCTURE_OPTIONS[structure_label],
        "earlyTask": ss.get("dg_early", []),
        "approach": APPROACH_OPTIONS[approach_label],
        "includeTypes": include_types,
        "avoidTypes": ss.get("dg_avoid", []),
        "extraContext": ss.get("dg_extra", "").strip(),
        "aiApproach": AI_OPTIONS[ai_label],
        "integrityFocus": ss.get("dg_integrity", []),
        "hasRespondus": any("respondus" in t.lower() for t in include_types),
        "udlModes": ss.get("dg_udl", []),
        "hasGroupWork": ss.get("dg_group", False),
        "collabULO": ss.get("dg_collab_ulo", "").strip(),
    }


def page_design_generator() -> None:
    vu_hero(
        "Assessment Design Generator",
        "Answer a few questions about your unit and we'll build a tailored MS Copilot prompt to "
        "generate a backward-designed, authentic, secure assessment structure aligned to VU standards.",
    )

    # ── Step 1: Unit context ────────────────────────────────────────────────
    with st.expander("**Step 1 — Unit context**", expanded=True):
        st.caption("Tell us about your unit. This grounds the assessment design in your discipline and level.")
        c1, c2 = st.columns(2)
        c1.text_input("Unit name & code", key="dg_unit_name",
                      placeholder="e.g. NEC2005 Geospatial Engineering")
        c2.text_input("Discipline / College", key="dg_discipline",
                      placeholder="e.g. Engineering, Nursing, Business")
        c3, c4 = st.columns(2)
        c3.selectbox("AQF level of qualification", ["", "AQF 5 (Diploma)",
                     "AQF 6 (Advanced Diploma / Associate Degree)", "AQF 7 (Bachelor)",
                     "AQF 8 (Honours / Graduate Certificate)", "AQF 9 (Masters)"], key="dg_aqf")
        c4.selectbox("Year / stage of program", ["", "First year / introductory",
                     "Second year / developing", "Third year / advanced",
                     "Final year / capstone", "Postgraduate"], key="dg_year")
        st.text_area("Unit overview", key="dg_overview", height=110,
                     help="Paste your unit description or a brief summary of what students study.",
                     placeholder="e.g. This unit introduces students to geospatial data collection, "
                                 "analysis and visualisation using industry-standard tools…")

    # ── Step 2: Delivery & students ─────────────────────────────────────────
    with st.expander("**Step 2 — Delivery & students**", expanded=True):
        st.caption("Understanding your delivery context shapes what assessment structures are realistic and fair.")
        st.markdown('<div class="vu-note">All VU Higher Education delivery on Australian campuses uses '
                    'the VU Block Model®.</div>', unsafe_allow_html=True)
        st.radio("Delivery mode", list(DELIVERY_OPTIONS), key="dg_delivery")
        st.slider("Approximate cohort size", 1, 300, 35, 5, key="dg_cohort")
        st.multiselect("Delivery format", ["On-campus", "Online", "Blended / hybrid", "Multi-campus"],
                       key="dg_format")
        st.multiselect("Special delivery contexts (select all that apply)", CONTEXT_CHIPS, key="dg_contexts")

    # ── Step 3: Learning outcomes ───────────────────────────────────────────
    with st.expander("**Step 3 — Learning outcomes**", expanded=True):
        st.caption("The foundation of backward design — assessment tasks should measure what students are meant to learn.")
        st.markdown('<div class="vu-note">💡 <strong>Backward design principle:</strong> Design assessments '
                    'that provide evidence students have achieved these outcomes — not the other way around.</div>',
                    unsafe_allow_html=True)
        st.text_area("Unit Learning Outcomes (ULOs) — one per line", key="dg_ulos", height=120,
                     placeholder="1. Analyse geospatial datasets to identify patterns…\n"
                                 "2. Apply industry-standard GIS software to collect, process and visualise spatial data")
        st.text_area("Mapped Course Learning Outcomes (CLOs)", key="dg_clos", height=90,
                     placeholder="CLO2: Apply analytical thinking to solve complex problems")
        st.multiselect("VU Employability Skills addressed", ESF_CHIPS, key="dg_esf")
        st.radio("Grading scheme", list(GRADING_OPTIONS), key="dg_grading")
        if "Graded" in st.session_state.get("dg_grading", ""):
            st.multiselect("Hurdle requirements (must-pass)", HURDLE_CHIPS, key="dg_hurdle",
                           help="A hurdle is a requirement students must meet regardless of overall grade.")
            st.text_input("Describe the hurdle (optional)", key="dg_hurdle_detail",
                          placeholder="e.g. Students must achieve a satisfactory rating on all placement competencies")

    # ── Step 4: Scaffolding & structure ─────────────────────────────────────
    with st.expander("**Step 4 — Scaffolding & structure**", expanded=True):
        st.caption("Think about how assessment builds across your unit so it feels purposeful rather than isolated.")
        st.markdown('<div class="vu-note">📐 Earlier tasks should build capability and confidence for later '
                    'ones. 🌐 Offering varied formats (written, oral, practical, visual) across the sequence '
                    'increases accessibility and engagement.</div>', unsafe_allow_html=True)
        st.radio("How many assessment tasks? (VU standards require 2–3)",
                 ["2 tasks", "3 tasks"], key="dg_task_count", horizontal=True)
        count = int(st.session_state.get("dg_task_count", "2 tasks").split()[0])
        roles = (["Early / foundational", "Culminating"] if count == 2
                 else ["Early / foundational", "Developing", "Culminating"])
        default_weights = ([30, 70] if count == 2 else [20, 30, 50])
        st.markdown("**Name and describe the role of each task**")
        cols = st.columns(count)
        for i in range(count):
            with cols[i]:
                st.markdown(f"*Task {i + 1} — {roles[i]}*")
                st.text_input(f"Working name (Task {i + 1})", key=f"dg_task_name_{i}",
                              label_visibility="collapsed", placeholder=f"Task {i + 1} name")
                st.number_input(f"Weighting % (Task {i + 1})", 0, 100, default_weights[i],
                                key=f"dg_task_weight_{i}", label_visibility="collapsed")
        st.radio("Assessment structure type", list(STRUCTURE_OPTIONS), key="dg_structure")
        st.multiselect("Early transition task (Week 1)", EARLY_CHIPS, key="dg_early")

    # ── Step 5: Assessment preferences ──────────────────────────────────────
    with st.expander("**Step 5 — Assessment preferences**", expanded=True):
        st.markdown('<div class="vu-note">VU Assessment Standards require at least 50% of marks to be earned '
                    'under secure, individually verified conditions — all designs will comply with this.</div>',
                    unsafe_allow_html=True)
        st.radio("Assessment emphasis (both meet the 50% secure standard)",
                 list(APPROACH_OPTIONS), key="dg_approach")
        st.multiselect("Assessment types to include", INCLUDE_CHIPS, key="dg_include",
                       help="Leave blank for an open suggestion from Copilot.")
        if any("respondus" in t.lower() for t in st.session_state.get("dg_include", [])):
            st.markdown('<div class="vu-note">💻 Brightspace quiz with Respondus Lockdown Browser supports '
                        'long-answer and free-writing questions — a valid secure mechanism, not just '
                        'multiple choice.</div>', unsafe_allow_html=True)
        st.multiselect("UDL — multiple means of expression across tasks", UDL_CHIPS, key="dg_udl")
        if len(st.session_state.get("dg_udl", [])) == 1:
            st.markdown('<div class="vu-warn">⚠️ Consider including at least one additional expression mode '
                        'across your tasks — this supports students who may struggle with a single format.</div>',
                        unsafe_allow_html=True)
        st.multiselect("Assessment types to avoid", AVOID_CHIPS, key="dg_avoid")
        st.text_area("Anything else to consider?", key="dg_extra", height=90,
                     placeholder="Marking load constraints, accreditation requirements, accessibility needs…")

    # ── Step 6: Openness, security & integrity ──────────────────────────────
    with st.expander("**Step 6 — Openness, security & integrity**", expanded=True):
        st.markdown('<div class="vu-note">🤖 <strong>VU\'s approach to AI:</strong> a co-intelligence stance — '
                    'AI is a partner in learning, not a replacement for thinking. The question is not whether AI '
                    'is permitted, but how tasks are designed so AI use develops capability rather than bypassing it.</div>',
                    unsafe_allow_html=True)
        st.radio("Assessment openness & AI approach", list(AI_OPTIONS), key="dg_ai")
        st.checkbox("Unit includes group assessment", key="dg_group")
        if st.session_state.get("dg_group"):
            st.markdown('<div class="vu-warn">⚠️ Group assessment is only appropriate when a learning outcome '
                        'explicitly requires teamwork or collaboration.</div>', unsafe_allow_html=True)
            st.text_input("Which ULO requires teamwork / collaboration?", key="dg_collab_ulo",
                          placeholder="e.g. Collaborate with peers to develop and present a design solution")
        st.multiselect("Security & integrity focus areas", INTEGRITY_CHIPS, key="dg_integrity")

    # ── Step 7: Review & generate ───────────────────────────────────────────
    st.markdown("### Step 7 — Review & generate")
    d = _collect_design_data()
    with st.container(border=True):
        st.markdown("**Your unit summary**")
        s1, s2, s3 = st.columns(3)
        s1.markdown(f"**Unit**\n\n{d['unitName'] or '—'}")
        s1.markdown(f"**Discipline**\n\n{d['discipline'] or '—'}")
        s1.markdown(f"**AQF level**\n\n{d['aqf'] or '—'}")
        s2.markdown(f"**Delivery**\n\n{d['delivery']}")
        s2.markdown(f"**Cohort**\n\n{d['cohort']}")
        s2.markdown(f"**Tasks**\n\n" + (" → ".join(f"{t['name']} ({t['weight']}%)"
                    for t in d['taskConfigs']) or "—"))
        s3.markdown(f"**Grading**\n\n{d['grading']}")
        s3.markdown(f"**Group work**\n\n{'Yes' if d['hasGroupWork'] else 'No'}")
        s3.markdown(f"**Employability skills**\n\n{', '.join(d['esf']) or '—'}")

    st.markdown('<div class="vu-note">✅ Your prompt uses a <strong>backward design</strong> approach and is '
                'aligned to VU Higher Education Assessment Standards.</div>', unsafe_allow_html=True)

    if st.button("✨ Generate my Copilot prompts", type="primary", use_container_width=True):
        st.session_state["dg_generated"] = True

    if st.session_state.get("dg_generated"):
        st.divider()
        st.markdown("## Your prompts are ready")
        st.caption("Copy the master prompt into MS Copilot to generate a complete assessment design. "
                   "Use the modular prompts for targeted follow-up in the same conversation.")
        st.markdown("##### 🗂️ Master prompt — complete assessment design")
        st.code(build_master_prompt(d), language="text")

        st.markdown("##### 🧩 Modular prompts (follow-ups)")
        for m in build_modular_prompts(d):
            with st.expander(f"{m['icon']}  {m['title']} — {m['desc']}"):
                st.code(m["prompt"], language="text")


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: TOOLS
# ═════════════════════════════════════════════════════════════════════════════

def page_tools() -> None:
    vu_hero("Assessment Tools",
            "Practical tools for designing learning outcomes, rubrics and assessments aligned to VU standards.")
    tabs = st.tabs(["✏️ Unit LO Builder", "🎓 Course LO Builder", "📋 Rubric Builder",
                    "✅ Assessment Checker", "📄 Standards Reference"])
    with tabs[0]:
        _tool_lo_builder()
    with tabs[1]:
        _tool_clo_builder()
    with tabs[2]:
        _tool_rubric_builder()
    with tabs[3]:
        _tool_checker()
    with tabs[4]:
        _tool_standards_ref()


# ── Unit Learning Outcome Builder ───────────────────────────────────────────
def _tool_lo_builder() -> None:
    st.subheader("Unit Learning Outcome Builder")
    st.caption("Write well-formed outcomes using the action verb + content + context formula, "
               "aligned to AQF levels and Bloom's Taxonomy.")

    st.text_area("Course Learning Outcomes (CLOs) this unit contributes to", key="lo_clo_ref",
                 height=90, help="Your alignment anchor — each ULO should contribute to at least one CLO.",
                 placeholder="CLO1: Apply discipline knowledge to solve complex professional problems")

    aqf_label_to_level = {v[0]: k for k, v in AQF_LEVELS.items()}
    aqf_choice = st.selectbox("AQF level", list(aqf_label_to_level), index=2, key="lo_aqf")
    level = aqf_label_to_level[aqf_choice]
    recommended = AQF_LEVELS[level][2]
    st.markdown(f'<div class="vu-note">{AQF_LEVELS[level][1]}<br><strong>Recommended verbs:</strong> '
                f'{", ".join(recommended)} ⭐</div>', unsafe_allow_html=True)

    # Flatten Bloom verbs, marking recommended ones
    all_verbs = []
    for lvl, verbs in BLOOM_VERBS.items():
        for v in verbs:
            label = f"{v}  ⭐ ({lvl})" if v in recommended else f"{v}  ({lvl})"
            all_verbs.append((label, v))
    verb_label = st.selectbox("Choose a Bloom's action verb (one per outcome)",
                              [lbl for lbl, _ in all_verbs], key="lo_verb")
    verb = dict(all_verbs)[verb_label]

    c1, c2 = st.columns(2)
    content = c1.text_input("Content — what students engage with", key="lo_content",
                            placeholder="e.g. geotechnical design principles")
    context = c2.text_input("Context — setting or purpose", key="lo_context",
                            placeholder="e.g. in complex civil engineering projects")
    qualifier = st.text_input("Optional qualifier", key="lo_qualifier",
                              placeholder="e.g. collaboratively with peers")

    # Live preview
    parts = []
    if qualifier.strip():
        parts.append(qualifier.strip().lower() + ",")
    parts.append(verb.capitalize())
    if content.strip():
        parts.append(content.strip().lower())
    if context.strip():
        parts.append(context.strip().lower())
    preview = " ".join(parts).strip()
    st.markdown(f'<div class="vu-note"><em>{preview or "Your learning outcome will appear here."}</em></div>',
                unsafe_allow_html=True)

    if "saved_los" not in st.session_state:
        st.session_state["saved_los"] = []
    b1, b2 = st.columns([1, 3])
    if b1.button("Save LO", key="lo_save"):
        if not content.strip():
            st.warning("Please enter the content field before saving.")
        else:
            st.session_state["saved_los"].append(preview)

    los = st.session_state["saved_los"]
    if los:
        st.markdown("**Saved Learning Outcomes**")
        st.markdown('<div class="vu-note">📋 Each CLO should be addressed by at least one ULO. '
                    'If a CLO has no matching ULO, add one.</div>', unsafe_allow_html=True)
        for i, lo in enumerate(los):
            cc1, cc2 = st.columns([10, 1])
            cc1.write(f"{i + 1}. {lo}")
            if cc2.button("✕", key=f"lo_del_{i}", help="Remove this outcome"):
                st.session_state["saved_los"].pop(i)
                st.rerun()
        st.code("\n".join(f"{i + 1}. {lo}" for i, lo in enumerate(los)), language="text")

    # Copilot prompt
    if st.button("✨ Generate Copilot prompt", type="primary", key="lo_prompt_btn"):
        clo_ref = st.session_state.get("lo_clo_ref", "").strip()
        clo_section = (f"The unit must align to the following fixed Course Learning Outcomes (CLOs):\n"
                       f"{clo_ref}\n\nEach ULO should contribute to at least one CLO.\n\n" if clo_ref else "")
        draft = (f"I have drafted the following Unit Learning Outcomes (ULOs):\n"
                 + "\n".join(f"{i + 1}. {lo}" for i, lo in enumerate(los)) + "\n\n") if los else ""
        clo_line = ("- Ensure each ULO contributes to at least one of the CLOs listed above\n"
                    if clo_ref else "")
        if los:
            task = ("For my drafted outcomes above, please:\n"
                    "1. Identify any issues with verb choice, structure or cognitive level\n"
                    "2. Suggest an improved version of each\n"
                    "3. Confirm which are already well-formed\n"
                    "4. Check alignment against the CLOs — does the full set collectively address all CLOs?\n"
                    "5. Suggest 1–2 additional outcomes if there are gaps in CLO coverage")
        else:
            task = ("Please suggest 3–5 well-formed learning outcomes based on the draft above, with a "
                    "brief rationale for each verb choice and confirmation of which CLO each contributes to.")
        prompt = (f"You are an expert higher education curriculum designer specialising in learning "
                  f"outcome design for Australian universities.\n\n{clo_section}{draft}"
                  f"Please help me write well-formed, measurable Unit Learning Outcomes (ULOs) for a unit "
                  f"at {aqf_choice}.\n\n"
                  f"For each outcome:\n"
                  f"- Use a single, strong Bloom's Taxonomy action verb appropriate to {aqf_choice}\n"
                  f"- Follow the formula: [action verb] + [content] + [context]\n"
                  f"- Avoid compound verbs (do not join two actions with 'and')\n"
                  f"- Avoid weak or unmeasurable verbs such as 'understand', 'know' or 'appreciate'\n"
                  f"- Ensure the cognitive demand matches {aqf_choice} expectations\n"
                  f"{clo_line}\n{task}\n\n"
                  f"Also confirm whether the full set covers an appropriate range of Bloom's levels for {aqf_choice}.")
        st.code(prompt, language="text")


# ── Course Learning Outcome Builder ─────────────────────────────────────────
def _tool_clo_builder() -> None:
    st.subheader("Course Learning Outcome Builder")
    st.caption("Write, review and map CLOs aligned to VU's Graduate Capabilities, the Employability "
               "Skills Framework and AQF level.")

    raw = st.text_area("Enter your Course Learning Outcomes — one per line", key="clo_input", height=140,
                       placeholder="Critically evaluate evidence to inform professional decision-making\n"
                                   "Communicate effectively across diverse professional settings")
    if st.button("Analyse CLOs", type="primary", key="clo_analyse"):
        st.session_state["clo_analysed"] = True

    if not st.session_state.get("clo_analysed"):
        return

    clos = [l.strip() for l in raw.split("\n") if l.strip()]
    if not clos:
        st.warning("Please enter at least one CLO.")
        return

    count = len(clos)
    if count < 3:
        st.error(f"⚠️ Only {count} CLO{'s' if count != 1 else ''} — likely too few to cover the full "
                 "range of graduate capabilities.")
    elif count <= 8:
        st.success(f"✅ {count} CLOs — a well-sized set.")
    else:
        st.error(f"⚠️ {count} CLOs — may be too many. Consider consolidating to 5–8.")

    for i, clo in enumerate(clos):
        lower = clo.lower()
        issues, suggestions = [], []
        weak = next((v for v in WEAK_VERBS if lower.startswith(v) or f" {v} " in lower), None)
        if weak:
            issues.append(f'weak/unmeasurable verb ("{weak}")')
            suggestions.append(f'Replace "{weak}" with a measurable verb (evaluate, analyse, design, '
                               f'apply, critique, synthesise).')
        if next((s for s in COMPOUND_SIGNALS if s in lower), None):
            issues.append("multiple actions in one outcome")
            suggestions.append("Split into two CLOs, or reframe so one verb captures the capability.")
        if next((s for s in CONTENT_SIGNALS if s in lower), None):
            issues.append("describes a content topic rather than a capability")
            suggestions.append('Reframe to "students will [verb] [capability] in [context]".')
        has_context = any(f" {w} " in lower for w in ["in", "to", "within", "across", "for"])
        if not has_context and not issues:
            issues.append("may lack a professional or disciplinary context")
            suggestions.append('Add a context phrase, e.g. "…in professional practice".')

        if not issues:
            st.success(f"✅ **CLO {i + 1}:** {clo}\n\nWell-formed — clear verb, capability-framed, contextualised.")
        elif len(issues) == 1:
            st.warning(f"⚠️ **CLO {i + 1}:** {clo}\n\n**Issues:** {issues[0]}\n\n**Suggestion:** {suggestions[0]}")
        else:
            st.error(f"❌ **CLO {i + 1}:** {clo}\n\n**Issues:** {' · '.join(issues)}\n\n"
                     + "\n".join(f"- {s}" for s in suggestions))

    st.divider()
    st.markdown("**Graduate Capability & Employability Skills coverage**")
    gc_col, esf_col = st.columns(2)
    with gc_col:
        st.markdown("*Graduate Capabilities*")
        covered = 0
        for gc, label, subs in GC_DATA:
            with st.expander(f"{gc}: {label}"):
                any_checked = False
                for sid, text in subs:
                    if st.checkbox(text, key=f"gc_{sid}"):
                        any_checked = True
                if any_checked:
                    covered += 1
        if covered == 3:
            st.success("✅ All three GCs addressed.")
        elif covered == 0:
            st.caption("Tick sub-points to check GC coverage.")
        else:
            st.warning(f"⚠️ {3 - covered} GC(s) not yet addressed.")
    with esf_col:
        st.markdown("*Employability Skills Framework*")
        esf_count = 0
        for label, desc in ESF_DATA:
            if st.checkbox(label, key=f"esf_{label}", help=desc):
                esf_count += 1
        if esf_count == 7:
            st.success("✅ All 7 employability skills addressed.")
        elif esf_count == 0:
            st.caption("Tick skills addressed by your CLO set.")
        elif esf_count >= 4:
            st.success(f"✅ {esf_count}/7 skills addressed.")
        else:
            st.warning(f"⚠️ Only {esf_count}/7 skills addressed — broaden coverage if possible.")

    st.markdown('<div class="vu-warn">⚠️ <strong>Accreditation reminder:</strong> if this course carries '
                'professional accreditation (Engineers Australia, AHPRA, CPA, TEQSA), verify your CLOs reflect '
                'the relevant graduate competency standards before finalising.</div>', unsafe_allow_html=True)


# ── Rubric Builder ──────────────────────────────────────────────────────────
def _tool_rubric_builder() -> None:
    import pandas as pd

    st.subheader("Rubric Builder")
    st.caption("Create assessment rubrics with weighted criteria and graded descriptors aligned to "
               "VU's grading schemes.")
    st.markdown('<div class="vu-note">🌐 Focus criteria on the <em>quality of learning demonstrated</em>, '
                'not the format — this makes rubrics more inclusive and supports diverse learners.</div>',
                unsafe_allow_html=True)

    title = st.text_input("Assessment title", key="rub_title", placeholder="e.g. Network Design Project")
    c1, c2 = st.columns(2)
    scheme = c1.selectbox("Grading scheme", list(SCHEMES), key="rub_scheme")
    style = c2.selectbox("Descriptor style", list(DESCRIPTOR_STYLES), key="rub_style")
    st.caption(DESCRIPTOR_STYLES[style]["desc"])

    st.markdown("**Criteria** — edit the table below (weights must total 100%).")
    default_df = pd.DataFrame([
        {"Criterion": "", "Weight (%)": 50, "Linked LOs": ""},
        {"Criterion": "", "Weight (%)": 50, "Linked LOs": ""},
    ])
    edited = st.data_editor(
        st.session_state.get("rub_df", default_df), num_rows="dynamic",
        use_container_width=True, key="rub_editor",
        column_config={
            "Weight (%)": st.column_config.NumberColumn(min_value=0, max_value=100, step=5),
        },
    )

    total = int(edited["Weight (%)"].fillna(0).sum())
    if total == 100:
        st.success(f"✅ Total weighting: {total}%")
    else:
        st.error(f"⚠️ Total weighting: {total}% — must equal 100% before generating.")

    if st.button("Generate rubric", type="primary", key="rub_gen"):
        valid = edited[edited["Criterion"].astype(str).str.strip() != ""]
        if valid.empty:
            st.warning("Please enter at least one criterion.")
        elif total != 100:
            st.warning("Weights must total 100% before generating the rubric.")
        else:
            grades = SCHEMES[scheme]
            descs = DESCRIPTOR_STYLES[style]["grades"]
            rows = []
            for _, r in valid.iterrows():
                row = {"Criterion": r["Criterion"], "Linked LOs": r["Linked LOs"] or "—",
                       "Weight": f'{int(r["Weight (%)"] or 0)}%'}
                for g in grades:
                    row[g] = descs.get(g, "")
                rows.append(row)
            st.markdown(f"#### {title or 'Assessment'} — Marking Rubric  ·  *{style}*")
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # Copilot prompt
    if st.button("✨ Generate Copilot prompt", key="rub_prompt_btn"):
        valid = edited[edited["Criterion"].astype(str).str.strip() != ""]
        if valid.empty:
            st.warning("Please enter at least one criterion before generating a Copilot prompt.")
        else:
            grades = SCHEMES[scheme]
            criteria_str = "\n".join(
                f'- Criterion {i + 1}: {r["Criterion"]} ({int(r["Weight (%)"] or 0)}%'
                + (f' | linked to {r["Linked LOs"]}' if str(r["Linked LOs"]).strip() else "") + ")"
                for i, (_, r) in enumerate(valid.iterrows())
            )
            is_tafe = "S/NYS" in scheme
            tafe_line = ("\n- This is a TAFE/VET unit using S/NYS — descriptors should define what "
                         "satisfactory (competent) performance looks like, not grade bands" if is_tafe else "")
            prompt = (f"You are an expert higher education assessment designer with deep knowledge of "
                      f"rubric design and discipline-specific assessment practice.\n\n"
                      f"Write detailed, high-quality rubric descriptors for the following assessment task.\n\n"
                      f"ASSESSMENT DETAILS\n"
                      f"Task: {title or 'Assessment task'}\n"
                      f"Grading scheme: {scheme}\n"
                      f"Descriptor style requested: {style}\n"
                      f"Total criteria weighting: {total}%\n\n"
                      f"Criteria and weightings:\n{criteria_str}\n\n"
                      f"WHAT TO PRODUCE\n"
                      f"For each criterion, write descriptors for: {', '.join(grades)}\n\n"
                      f"Requirements:\n"
                      f"- Make descriptors specific to the task and discipline — avoid generic language\n"
                      f"- Ensure each descriptor is clearly distinguishable from adjacent grade bands\n"
                      f'- Write from the student perspective ("The student demonstrates…")\n'
                      f"- Keep descriptors concise but detailed enough to guide marking{tafe_line}\n\n"
                      f"Present the rubric as a table with criteria as rows and grade bands as columns.")
            st.code(prompt, language="text")


# ── Assessment Checker ──────────────────────────────────────────────────────
def _tool_checker() -> None:
    st.subheader("Assessment Checker")
    st.caption("Check your assessment design against VU's Assessment Standards before CAMS submission.")
    mode = st.radio("Mode", ["Higher Education (HE)", "Vocational Education (TAFE)"],
                    key="check_mode", horizontal=True)
    standards = HE_STANDARDS if mode.startswith("Higher") else TAFE_STANDARDS

    all_items = [item for _, items in standards for item in items]
    checked = sum(1 for num, _ in all_items if st.session_state.get(f"chk_{num}"))
    total = len(all_items)
    pct = checked / total if total else 0
    st.progress(pct, text=(f"✅ All {total} standards addressed — ready for CAMS submission."
                           if checked == total else f"{checked} of {total} standards addressed ({int(pct * 100)}%)"))

    for group, items in standards:
        done = sum(1 for num, _ in items if st.session_state.get(f"chk_{num}"))
        with st.expander(f"**{group}**  ·  {done}/{len(items)}", expanded=True):
            for num, text in items:
                st.checkbox(f"**{num}** — {text}", key=f"chk_{num}")


# ── Standards Reference ─────────────────────────────────────────────────────
def _tool_standards_ref() -> None:
    st.subheader("Standards Reference")
    st.caption("VU Assessment Standards at a glance. Use alongside the Assessment Checker for CAMS preparation.")
    cols = st.columns(3)
    for idx, (num, scope, title, desc) in enumerate(STANDARDS_REF):
        with cols[idx % 3]:
            st.markdown(
                f'<div class="vu-card"><div><span class="vu-badge">{scope}</span>'
                f'<span class="topic" style="display:inline">{num}</span></div>'
                f'<h4>{title}</h4><p>{desc}</p></div>',
                unsafe_allow_html=True,
            )
            st.write("")


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: RESOURCES
# ═════════════════════════════════════════════════════════════════════════════

def page_resources() -> None:
    vu_hero("Assessment Resource Hub",
            "Curated readings, guides, tools and frameworks for assessment design practice at Victoria University.")

    st.markdown(
        '<div class="vu-warn">🔄 <strong>Assessment Refresh Project</strong> — VU\'s whole-of-institution '
        'assessment redesign initiative. '
        '<a href="https://vustaff.sharepoint.com/sites/i0147/SitePages/Assessment%20Refresh.aspx" '
        'target="_blank">Visit the project page →</a></div>',
        unsafe_allow_html=True,
    )

    topics = ["All topics"] + [t[1] for t in TOPIC_GUIDES]
    c1, c2 = st.columns([2, 3])
    topic = c1.selectbox("Filter by topic", topics, key="res_topic")
    search = c2.text_input("Search resources", key="res_search", placeholder="Search title or description…")

    # Topic guide quick-glance grid
    with st.expander("📖 Topic guide — what each theme means", expanded=False):
        gcols = st.columns(3)
        for i, (icon, ttitle, tdesc) in enumerate(TOPIC_GUIDES):
            with gcols[i % 3]:
                st.markdown(f"**{icon} {ttitle}**")
                st.caption(tdesc)

    # Filter resources
    results = RESOURCES
    if topic != "All topics":
        results = [r for r in results if r[1] == topic]
    if search.strip():
        q = search.lower().strip()
        results = [r for r in results if q in r[0].lower() or q in r[3].lower()]

    st.caption(f"Showing {len(results)} resource{'s' if len(results) != 1 else ''}.")
    if not results:
        st.info("No resources found for this filter.")
        return

    cols = st.columns(3)
    for idx, (title, rtopic, rtype, desc, url) in enumerate(results):
        color = RESOURCE_TYPE_COLORS.get(rtype, "#075577")
        with cols[idx % 3]:
            st.markdown(
                f'<div class="vu-card">'
                f'<div class="topic">{rtopic}</div>'
                f'<h4>{title} <span class="vu-badge" style="background:#eee;color:{color}">{rtype}</span></h4>'
                f'<p>{desc}</p>'
                f'<a href="{url}" target="_blank" rel="noopener">Open resource ↗</a>'
                f'</div>',
                unsafe_allow_html=True,
            )
            st.write("")


# ═════════════════════════════════════════════════════════════════════════════
# NAVIGATION / ROUTER
# ═════════════════════════════════════════════════════════════════════════════

PAGES = {
    "🏠 Home": page_home,
    "✨ Design Generator": page_design_generator,
    "🛠️ Tools": page_tools,
    "📚 Resources": page_resources,
}


def main() -> None:
    with st.sidebar:
        st.markdown(f"### <span style='color:{VU_AUBERGINE}'>◆ Assessment Practice Hub</span>",
                    unsafe_allow_html=True)
        st.caption("Victoria University · Learning Design & Innovation")
        choice = st.radio("Navigate", list(PAGES), key="nav", label_visibility="collapsed")
        st.divider()
        st.caption("Designed for VU Higher Education delivery on Australian campuses "
                   "(Melbourne, Sydney, Brisbane).")
        st.caption("Built with Streamlit · Powered by Copilot Cowork")

    PAGES[choice]()


if __name__ == "__main__":
    main()
