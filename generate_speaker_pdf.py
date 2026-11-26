import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#0F766E"))
        self.drawString(54, 756, "FAIRHIRE AUDIT")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(135, 756, "— High-Impact Pitch & Speaker Delivery Script")
        
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(54, 750, 558, 750)
        
        # Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 34, page_str)
        self.drawString(54, 34, "Personalized Speaker Script · Natural, Conversational Delivery · DPDP 2023")
        self.restoreState()

def create_presentation_pdf(output_filename="FairHire_Audit_Speaker_Notes.pdf"):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=50
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Typographic Hierarchy
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#0F766E'),
        spaceAfter=12
    )
    
    slide_num_style = ParagraphStyle(
        'SlideNum',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.HexColor('#0F766E'),
        textTransform='uppercase',
        spaceAfter=3
    )
    
    slide_title_style = ParagraphStyle(
        'SlideTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=6
    )
    
    section_h_style = ParagraphStyle(
        'SectionH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=4,
        spaceAfter=2
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#334155'),
        spaceAfter=4
    )

    speech_style = ParagraphStyle(
        'Speech',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14.5,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=5
    )
    
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#475569'),
        leftIndent=8,
        spaceAfter=2
    )

    cue_style = ParagraphStyle(
        'Cue',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12.5,
        textColor=colors.HexColor('#B45309'),
        spaceAfter=3
    )

    story = []
    
    # Title Header Block
    story.append(Paragraph("FairHire Audit: Live Presentation & Speaker Script", title_style))
    story.append(Paragraph("Conversational, Relatable, High-Impact Narrative Guide for Demo Day", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0F766E'), spaceAfter=10))
    
    story.append(Paragraph("<b>Speaker Strategy:</b> Speak naturally like you're talking directly to fellow engineers and recruiters. Avoid stiff corporate jargon. Anchor every point to real human experiences (applying for jobs, taking loans).", body_style))
    story.append(Spacer(1, 8))

    slides = [
        {
            "num": "SLIDE 1 · TIME: 0:00 - 0:45",
            "title": "The Hook: The Secret Gatekeeper Standing Between You & Your Job",
            "slide_content": "<b>Slide Visual:</b> Minimalist cover. Headline: <i>'See if your AI treats everyone equally.'</i> Silhouette of an applicant resume entering a black-box AI filter.",
            "what_to_say": "<b>\"Good morning everyone.</b> Today, if any of you want to give an interview at a tech company, you already know the drill: your resume doesn't go to a human recruiter first. It goes straight into an AI-powered ATS—an automated tracking system. That single algorithm decides whether a human ever reads your name or if you get rejected in 5 seconds flat.<br/><br/>The same thing happens when you apply for a credit card or a loan online—an AI underwriter decides your financial fate in milliseconds. <b>But what happens when that AI looks at two mathematically identical resumes, and rejects one simply because of the applicant's name or postal address?</b><br/><br/>Today, I am presenting <b>FairHire Audit</b>—an end-to-end governance framework that tests, proves, and fixes algorithmic bias in generative AI decision systems.\"",
            "cue": "🎯 <b>Stage Delivery Cue:</b> Make direct eye contact and ask: <i>'How many of you have submitted a resume and felt like it vanished into an AI black hole? Today, we open that black hole.'</i>"
        },
        {
            "num": "SLIDE 2 · TIME: 0:45 - 2:00",
            "title": "The Hiring Story: Rohan vs. Meera (Identical Resume, Different Fate)",
            "slide_content": "<b>Slide Visual:</b> Side-by-side resume cards. Rohan Sharma (95/100 · Shortlisted) vs. Meera Sharma (83/100 · Filtered). Same B.Tech CS, 8.4 GPA, Python, SQL, Docker.",
            "what_to_say": "<b>\"Let me show you a real experiment we ran.</b> Imagine two young developers applying for the exact same Junior Python Developer job.<br/><br/>Their resumes are <b>100% identical word-for-word</b>: same B.Tech CS degree, same 8.4 CGPA, same Python, SQL, Git, and Docker projects. Everything matches down to the punctuation.<br/><br/>The only detail we changed? On Resume A, the header says <b>Rohan Sharma</b>. On Resume B, it says <b>Meera Sharma</b>.<br/><br/>When we submitted both to an LLM recruiter: <b>Rohan scored 95</b>—the model praised his 'strong technical aptitude and containerization mastery.' But <b>Meera scored 83</b>, hedged as 'possessing foundational familiarity.'<br/><br/>In a boundary case where both omitted an optional Docker tag, Rohan got leniency and was <b>Shortlisted at 75</b>, while Meera was <b>Rejected at 63</b>. Because every single line of code and achievement was identical, that 12-point penalty was pure demographic gender bias.\"",
            "cue": "🎯 <b>Stage Delivery Cue:</b> Point with your finger at the two scores: <i>'Same resume. Same skills. But Meera gets rejected. That is what an unmonitored AI does.'</i>"
        },
        {
            "num": "SLIDE 3 · TIME: 2:00 - 3:00",
            "title": "The Lending Dilemma: Getting Rejected Because of Your Zip Code",
            "slide_content": "<b>Slide Visual:</b> Credit Dossier split: ₹85k Salary, 760 CIBIL, 30.7% DTI. Twin A (560001 Indiranagar Metro) vs. Twin B (583201 Rural District). Approved (20) vs. Denied (35).",
            "what_to_say": "<b>\"This problem isn't just in hiring—it's in lending too.</b> In credit underwriting, fairness means equal opportunity for equally creditworthy people. We tested two loan applicants with identical financial discipline: both earn ₹85,000 a month, both have a solid 760 credit score, and both have low debt.<br/><br/>The only difference? The postal pincode.<br/>Applicant A lives in <b>560001 (Indiranagar, Bangalore)</b>.<br/>Applicant B lives in <b>583201 (a rural, underbanked district)</b>.<br/><br/>The AI underwriter approved the metro applicant with a prime risk score of <b>20</b>. But it slapped a +15 penalty on the rural applicant, scoring them <b>35 and denying the loan</b>.<br/><br/>That is automated postal redlining. An applicant can manage their finances perfectly, yet get punished simply for living in a rural pincode.\"",
            "cue": "🎯 <b>Stage Delivery Cue:</b> Pause for 2 seconds. Say: <i>'Imagine doing everything right financially, and an algorithm rejects your family loan because of your zip code.'</i>"
        },
        {
            "num": "SLIDE 4 · TIME: 3:00 - 4:00",
            "title": "The Solution: How FairHire Actually Audits an AI",
            "slide_content": "<b>Slide Visual:</b> Tri-Fold Audit Engine Diagram. 1. Counterfactual Disparity Engine → 2. Factuality / Hallucination Auditor → 3. Privacy & Injection Suite.",
            "what_to_say": "<b>\"So how do we fix this without guessing?</b> We built FairHire Audit around three concrete testing pillars:<br/><br/>"
                           "<b>1. Counterfactual Matched Pairs:</b> We create exact digital twins. We hold all qualifications constant and flip just one attribute—gender, college tier, or postal code. If the score changes, we have mathematically proven bias with zero confounding noise.<br/>"
                           "<b>2. Factuality Auditor:</b> We cross-check the AI's explanation against the resume. If the model rejects someone by claiming they 'lack experience' when it's clearly on the resume, we catch that hallucination.<br/>"
                           "<b>3. PII & Privacy Defense:</b> We test whether the model leaks synthetic Aadhaar, PAN, or bank account numbers—and we hit it with adversarial jailbreak prompts to test its defenses.\"",
            "cue": "🎯 <b>Stage Delivery Cue:</b> <i>'We don't ask the model if it's fair. We run rigorous scientific experiments with counterfactual pairs to prove it.'</i>"
        },
        {
            "num": "SLIDE 5 · TIME: 4:00 - 5:15",
            "title": "The Findings: What We Discovered in the Audit",
            "slide_content": "<b>Slide Visual:</b> Clean KPI metric row: Hiring Gender Gap: 10.8 pts (High Risk) · Lending FRR Gap: 100% · Fact Hallucination: 0.0% · PII Leaks: 0.0% · Injections Defended: 10/10.",
            "what_to_say": "<b>\"Here is what our empirical audit revealed across the baseline models:</b><br/><br/>"
                           "• In Hiring, we found a statistically significant <b>10.8 point average gender gap</b> favoring male names, and a 1.5 point college halo penalty for rural colleges.<br/>"
                           "• In Lending, we discovered a massive <b>100% False Rejection Rate disparity</b>. Every single creditworthy rural borrower was rejected, while every identical metro borrower was approved.<br/>"
                           "• But look at the security metrics: <b>0.0% hallucination</b>, <b>0.0% PII leaks</b>, and <b>10 out of 10 prompt injections blocked</b>.<br/><br/>"
                           "The model wasn't broken by hackers. It wasn't making up fake facts. It was simply biased by default against women and rural applicants.\"",
            "cue": "🎯 <b>Stage Delivery Cue:</b> <i>'This is the critical takeaway: an AI can pass every cybersecurity check and still fail basic human fairness.'</i>"
        },
        {
            "num": "SLIDE 6 · TIME: 5:15 - 6:15",
            "title": "The Mitigation: Fixing Bias Without Retraining the Model",
            "slide_content": "<b>Slide Visual:</b> Before vs. After Strikethrough Cards: Gender Gap 10.8 → 0.0 pts · Redlining Gap 14.5 → 0.0 pts · FRR Gap 100% → 0%. Two fixes: Blind Token Sanitizer + Guarded System Prompt.",
            "what_to_say": "<b>\"Now, the best part of our work: we didn't just diagnose the problem, we built the fix.</b> And we did it without needing millions of dollars to retrain the foundation model.<br/><br/>"
                           "We engineered a two-stage guardrail:<br/>"
                           "<b>1. The Blind Pre-processor:</b> Before the LLM ever reads a profile, our sanitizer strips names, gender pronouns, college tiers, and 6-digit pincodes, converting them to neutral standardized tokens.<br/>"
                           "<b>2. Guarded System Prompting:</b> We inject strict constraints forcing the AI to evaluate candidates strictly on declared technical skills or financial debt-to-income ratios.<br/><br/>"
                           "The results? The gender gap dropped from <b>10.8 to 0.0 points</b>. The postal redlining penalty dropped to <b>0.0</b>. And the lending false rejection disparity collapsed from <b>100% down to 0%</b>. Complete parity.\"",
            "cue": "🎯 <b>Stage Delivery Cue:</b> <i>'We proved that with intelligent engineering, you don't have to choose between AI automation and fairness. You can have both.'</i>"
        },
        {
            "num": "SLIDE 7 · TIME: 6:15 - 7:00",
            "title": "Statutory Alignment: Conforming with India's DPDP Act (2023)",
            "slide_content": "<b>Slide Visual:</b> DPDP Controls Checklist: Sec 4 & 5 (Data Minimisation) · Sec 6 (Consent) · Sec 8(3) (Accuracy & Non-Redlining) · Sec 11 (Adverse Recourse & Grievance).",
            "what_to_say": "<b>\"We also anchored our platform in real law.</b> India's <b>Digital Personal Data Protection (DPDP) Act</b> was notified with rules in November 2025. It sets clear rules for processing digital personal data:<br/><br/>"
                           "• <b>Sections 4 & 5 (Data Minimisation):</b> Our sanitizer strips unnecessary identifiers like Aadhaar, PAN, and zip codes before inference.<br/>"
                           "• <b>Section 8(3) (Data Accuracy & Completeness):</b> Ensures credit and hiring decisions aren't distorted by discriminatory proxy variables.<br/>"
                           "• <b>Section 11 (Adverse Outcome Recourse):</b> If an applicant is rejected, our system auto-generates actionable recourse explaining the exact criteria—so an applicant knows whether learning Docker or lowering their debt ratio will qualify them.<br/><br/>"
                           "<i>(Of course, as required: this provides engineering governance tooling, not legal advice.)</i>\"",
            "cue": "🎯 <b>Stage Delivery Cue:</b> <i>'Compliance is no longer optional. FairHire gives companies the proof they need before regulators ask.'</i>"
        },
        {
            "num": "SLIDE 8 · TIME: 7:00 - 8:00",
            "title": "Tech Stack, Codebase & Live Demonstration",
            "slide_content": "<b>Slide Visual:</b> Tech Stack Badges: Python 3.11 · Groq SDK · React 19 · TypeScript · Tailwind CSS · Streamlit. Live Preview of localhost:3000.",
            "what_to_say": "<b>\"To make this usable in the real world, we engineered a clean full-stack architecture:</b><br/><br/>"
                           "• <b>Backend Engine (Python 3.11):</b> Uses the Groq LLM SDK for fast inference, paired with Pandas, NumPy, and SciPy for student t-tests and EEOC 4/5ths statistical metrics.<br/>"
                           "• <b>Dual Frontend:</b> An editorial web dashboard built with <b>React 19, TypeScript, and Tailwind CSS</b> with Fraunces serif typography for executive reports, plus a <b>Streamlit</b> interface for data scientists.<br/><br/>"
                           "Let me now open the live web app at <b>localhost:3000</b> so you can watch our counterfactual inspection matrix in action. Thank you!\"",
            "cue": "🎯 <b>Stage Delivery Cue:</b> Smooth transition: <i>'Let's switch over to the live dashboard and run a test pair right now.'</i>"
        }
    ]

    for slide in slides:
        card_content = [
            [Paragraph(slide["num"], slide_num_style)],
            [Paragraph(slide["title"], slide_title_style)],
            [Paragraph("<b>ON-SCREEN SLIDE VISUAL:</b>", section_h_style)],
            [Paragraph(slide["slide_content"], bullet_style)],
            [Spacer(1, 3)],
            [Paragraph("<b>WHAT TO SPEAK (SCRIPT):</b>", section_h_style)],
            [Paragraph(slide["what_to_say"], speech_style)],
            [Spacer(1, 3)],
            [Paragraph(slide["cue"], cue_style)]
        ]
        
        t = Table(card_content, colWidths=[504])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
            ('PADDING', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,-1), (-1,-1), 10),
        ]))
        
        story.append(t)
        story.append(Spacer(1, 12))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("Updated PDF generated successfully.")

if __name__ == "__main__":
    create_presentation_pdf()
