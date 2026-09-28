from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
                                 ListFlowable, ListItem, Table, TableStyle)
from reportlab.lib import colors
import json

ST = json.load(open("docs/stats.json"))
LC, GF = ST["leetcode"], ST["gfg"]
TOTAL = LC["solved"] + GF["solved"]
MH = LC["medium"] + LC["hard"] + GF["medium"] + GF["hard"]

doc = SimpleDocTemplate(
    "docs/Sankar_Resume.pdf",
    pagesize=letter,
    topMargin=0.35*inch,
    bottomMargin=0.35*inch,
    leftMargin=0.55*inch,
    rightMargin=0.55*inch,
)

styles = getSampleStyleSheet()

name_style = ParagraphStyle('Name', parent=styles['Normal'], fontName='Helvetica-Bold',
                             fontSize=17, leading=21, alignment=TA_CENTER, spaceAfter=4)
contact_style = ParagraphStyle('Contact', parent=styles['Normal'], fontName='Helvetica',
                                fontSize=9.5, alignment=TA_CENTER, spaceAfter=6)
section_style = ParagraphStyle('Section', parent=styles['Normal'], fontName='Helvetica-Bold',
                                fontSize=11, spaceBefore=5, spaceAfter=1)
body_style = ParagraphStyle('Body', parent=styles['Normal'], fontName='Helvetica',
                             fontSize=9.5, leading=13)
bullet_style = ParagraphStyle('Bullet', parent=styles['Normal'], fontName='Helvetica',
                               fontSize=9.3, leading=12.3, leftIndent=12)
row_bold = ParagraphStyle('RowBold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9.8, leading=12)
row_normal = ParagraphStyle('RowNormal', parent=styles['Normal'], fontName='Helvetica', fontSize=9.5, leading=12)
row_normal_r = ParagraphStyle('RowNormalR', parent=styles['Normal'], fontName='Helvetica', fontSize=9.5,
                               leading=12, alignment=2)
row_bold_r = ParagraphStyle('RowBoldR', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9.8,
                             leading=12, alignment=2)

story = []

story.append(Paragraph("Juturi Lakshmi Anantha Sankar", name_style))
story.append(Paragraph(
    '(+91) 7013608048 | <link href="mailto:juturisankar2@gmail.com" color="blue">juturisankar2@gmail.com</link> | '
    '<link href="https://github.com/SANKARJUTURI" color="blue">GitHub</link> | '
    '<link href="https://www.linkedin.com/in/juturi-lakshmi-anantha-sankar-42046b337/" color="blue">LinkedIn</link>',
    contact_style
))
story.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceAfter=4))

def section(title):
    story.append(Paragraph(title, section_style))
    story.append(HRFlowable(width="100%", thickness=0.6, color=colors.grey, spaceAfter=4))

def bullets(items):
    story.append(ListFlowable(
        [ListItem(Paragraph(it, bullet_style), bulletColor=colors.black) for it in items],
        bulletType='bullet', start='•', leftIndent=14, bulletFontSize=8, spaceBefore=0, spaceAfter=0
    ))

def two_col_row(left, right, bold_left=True):
    style_l = row_bold if bold_left else row_normal
    style_r = row_bold_r if bold_left else row_normal_r
    t = Table([[Paragraph(left, style_l), Paragraph(right, style_r)]],
              colWidths=[5.0*inch, 1.9*inch])
    t.setStyle(TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t)

# Professional Summary
section("PROFESSIONAL SUMMARY")
story.append(Paragraph(
    "Aspiring Web Developer with strong expertise in Data Structures &amp; Algorithms and modern web development. "
    "Proficient in building responsive, scalable, and user-friendly web applications with clean, intuitive interfaces. "
    "Passionate about creating high-quality web experiences and delivering impactful software solutions.",
    body_style
))

# Education
section("EDUCATION")
two_col_row("B.Tech – CSE", "Aug 2023 - Present", bold_left=True)
two_col_row("SRKR Engineering College, Bhimavaram", "CGPA: 9.31/10", bold_left=False)
story.append(Spacer(1, 1.5))
two_col_row("Intermediate (MPC)", "2021 - 2023", bold_left=True)
two_col_row("Vagdevi Junior College, Narasaraopet", "985/1000", bold_left=False)
story.append(Spacer(1, 1.5))
two_col_row("SSC", "2020 - 2021", bold_left=True)
two_col_row("Blooms High School, Vinukonda", "594/600", bold_left=False)

# Technical Skills
section("TECHNICAL SKILLS")
story.append(Paragraph("<b>Programming Languages:</b> C, Java, Python", body_style))
story.append(Paragraph("<b>Web Technologies:</b> HTML, CSS, JavaScript", body_style))
story.append(Paragraph("<b>Database:</b> SQL", body_style))
story.append(Paragraph("<b>Tools:</b> Git, GitHub, VS Code", body_style))
story.append(Paragraph("<b>Concepts:</b> OOP", body_style))

# Projects
section("PROJECTS")
story.append(Paragraph("<b>Clean Campus – Smart Waste Reporting Web Application</b>", row_bold))
bullets([
    "Built a responsive campus cleanliness web application with secure authentication and controlled session management",
    "Implemented waste reporting with validation, structured data handling, and a leaderboard for tracking and engagement",
    "Designed a responsive and intuitive user interface to provide a seamless experience across desktop and mobile devices",
])
story.append(Spacer(1, 2))
story.append(Paragraph("<b>Movie Stub – Online Movie Ticket Booking Application</b>", row_bold))
bullets([
    "Developed an online movie ticket booking web application with seat selection, reservations, and structured booking logic",
    "Built availability tracking, cancellations, and booking count display",
    "Designed responsive user interfaces with dynamic seat visualization to improve the overall booking experience",
])

# Problem Solving & DSA (UPDATED with current stats from LeetCode + GFG screenshots)
section("PROBLEM SOLVING & DSA")
bullets([
    f"Solved {TOTAL:,} coding problems across LeetCode ({LC['solved']:,}) and GeeksforGeeks ({GF['solved']:,}), including {MH:,} Medium/Hard problems",
    "Strengthened problem-solving skills by applying advanced algorithms and data structures to optimize time and space complexity",
    "Gained strong proficiency in Arrays, Strings, Trees, Graphs, Dynamic Programming, Greedy Algorithms, Hashing, Two Pointers, and Sliding Window techniques",
    "LeetCode: <link href=\"https://leetcode.com/u/SANKAR_JUTURI/\" color=\"blue\">leetcode.com/u/SANKAR_JUTURI</link>",
    "GeeksforGeeks: <link href=\"https://www.geeksforgeeks.org/profile/juturisankar\" color=\"blue\">geeksforgeeks.org/profile/juturisankar</link>",
])

# Certifications
section("CERTIFICATIONS")
cert_bullet_style = ParagraphStyle('CertBullet', parent=bullet_style)
for label, year in [
    ("CLA: Programming Essentials in C", "2024"),
    ("Cisco: Python Essentials 1", "2024"),
    ("Cisco: Python Essentials 2", "2025"),
    ("HackerRank: Java (Basic)", "2026"),
]:
    t = Table([[Paragraph("•&nbsp;&nbsp;" + label, bullet_style), Paragraph(year, row_normal_r)]],
              colWidths=[5.6*inch, 1.3*inch])
    t.setStyle(TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t)

# Soft Skills
section("SOFT SKILLS")
story.append(Paragraph(
    "Problem-Solving | Analytical Thinking | Logical Reasoning | Team Collaboration | Communication Skills",
    body_style
))

doc.build(story)
print("done")
