"""
PDF resume generation engine with multi-template support.

Provides three professional templates with proper text wrapping,
dynamic spacing, multi-page overflow, and clean typography.

Templates:
- Tech Minimalist: Clean lines, blue accents, developer-focused
- Corporate Executive: Navy/gold, traditional structure
- Modern Developer: Purple/pink gradients, creative layout
"""

from __future__ import annotations

import os
import tempfile
from datetime import datetime

from fpdf import FPDF

from app.models.resume_schema import ResumeData
from app.utils.constants import (
    PDF_MARGIN_LEFT,
    PDF_MARGIN_RIGHT,
    PDF_MARGIN_TOP,
    PDF_CONTENT_WIDTH,
    TEMPLATE_COLORS,
)


class ResumePDF(FPDF):
    """Extended FPDF with resume-specific helpers."""

    def __init__(self, template: str = "tech_minimalist"):
        super().__init__()
        self.template = template
        self.colors = TEMPLATE_COLORS.get(template, TEMPLATE_COLORS["tech_minimalist"])
        self.set_margins(PDF_MARGIN_LEFT, PDF_MARGIN_TOP, PDF_MARGIN_RIGHT)
        self.set_auto_page_break(auto=True, margin=20)

    def _set_color(self, color_key: str) -> None:
        """Set text color from template palette."""
        r, g, b = self.colors.get(color_key, (0, 0, 0))
        self.set_text_color(r, g, b)

    def _set_draw_color(self, color_key: str) -> None:
        """Set draw color from template palette."""
        r, g, b = self.colors.get(color_key, (0, 0, 0))
        self.set_draw_color(r, g, b)

    def _set_fill_color(self, color_key: str) -> None:
        """Set fill color from template palette."""
        r, g, b = self.colors.get(color_key, (200, 200, 200))
        self.set_fill_color(r, g, b)

    def section_title(self, title: str) -> None:
        """Render a section header with template-appropriate styling."""
        self.ln(4)
        self._set_color("primary")
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 8, title.upper(), ln=True)
        self._set_draw_color("primary")
        self.set_line_width(0.5)
        self.line(
            self.l_margin, self.get_y(),
            self.w - self.r_margin, self.get_y()
        )
        self.ln(3)
        self._set_color("text")

    def safe_multi_cell(self, w: float, h: float, txt: str, **kwargs) -> None:
        """Write multi-cell text with overflow safety."""
        if not txt or not txt.strip():
            return
        # Ensure we don't exceed page bounds
        if self.get_y() > 270:
            self.add_page()
        self.multi_cell(w, h, txt, **kwargs)

    def bullet_point(self, text: str, indent: float = 5) -> None:
        """Render a bullet point with proper indentation."""
        if not text.strip():
            return
        x = self.get_x()
        self.set_x(x + indent)
        self.set_font("Helvetica", "", 9)
        self._set_color("text")
        bullet_char = "-"
        self.multi_cell(PDF_CONTENT_WIDTH - indent - 5, 5, f"{bullet_char}  {text.strip()}")
        self.ln(1)

    def contact_line(self, items: list[str]) -> None:
        """Render contact info as a centered pipe-separated line."""
        clean = [i for i in items if i.strip()]
        if not clean:
            return
        self.set_font("Helvetica", "", 9)
        self._set_color("secondary")
        self.cell(0, 5, "  |  ".join(clean), ln=True, align="C")


def generate_resume_pdf(
    resume: ResumeData,
    template: str = "tech_minimalist",
) -> tuple[str, str]:
    """
    Generate a professional PDF resume.
    
    Args:
        resume: Validated resume data
        template: Template key from AVAILABLE_TEMPLATES
        
    Returns:
        Tuple of (file_path, filename)
    """
    pdf = ResumePDF(template=template)
    pdf.add_page()

    # Dispatch to the appropriate template renderer
    renderers = {
        "tech_minimalist": _render_tech_minimalist,
        "corporate_executive": _render_corporate_executive,
        "modern_developer": _render_modern_developer,
    }
    renderer = renderers.get(template, _render_tech_minimalist)
    renderer(pdf, resume)

    filename = f"resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join(tempfile.gettempdir(), filename)
    pdf.output(filepath)

    return filepath, filename


# ---------------------------------------------------------------------------
# Template: Tech Minimalist
# ---------------------------------------------------------------------------

def _render_tech_minimalist(pdf: ResumePDF, r: ResumeData) -> None:
    """Clean, blue-accented template for tech professionals."""
    pi = r.personal_info

    # Header
    pdf._set_color("primary")
    pdf.set_font("Helvetica", "B", 22)
    pdf.cell(0, 12, pi.name or "Your Name", ln=True, align="C")

    contact_items = [pi.email, pi.phone, pi.location]
    pdf.contact_line(contact_items)

    link_items = [pi.linkedin, pi.github]
    link_items = [l for l in link_items if l]
    if link_items:
        pdf.set_font("Helvetica", "", 8)
        pdf._set_color("primary")
        pdf.cell(0, 5, "  |  ".join(link_items), ln=True, align="C")

    pdf.ln(3)

    # Summary
    if pi.summary:
        pdf.section_title("Professional Summary")
        pdf.set_font("Helvetica", "", 10)
        pdf._set_color("text")
        pdf.safe_multi_cell(PDF_CONTENT_WIDTH, 5, pi.summary)
        pdf.ln(2)

    # Experience
    if r.experience:
        pdf.section_title("Experience")
        for exp in r.experience:
            pdf.set_font("Helvetica", "B", 10)
            pdf._set_color("text")
            pdf.cell(0, 6, f"{exp.job_title}", ln=False)
            if exp.duration:
                pdf.set_font("Helvetica", "", 9)
                pdf._set_color("secondary")
                pdf.cell(0, 6, exp.duration, ln=True, align="R")
            else:
                pdf.ln()

            pdf.set_font("Helvetica", "I", 9)
            pdf._set_color("secondary")
            company_line = exp.company
            if exp.location:
                company_line += f"  -  {exp.location}"
            pdf.cell(0, 5, company_line, ln=True)

            if exp.description:
                for line in exp.description.split("\n"):
                    line = line.strip().lstrip("•-").strip()
                    if line:
                        pdf.bullet_point(line)
            pdf.ln(2)

    # Education
    if r.education:
        pdf.section_title("Education")
        for edu in r.education:
            pdf.set_font("Helvetica", "B", 10)
            pdf._set_color("text")
            pdf.cell(0, 6, edu.degree, ln=False)
            if edu.year:
                pdf.set_font("Helvetica", "", 9)
                pdf._set_color("secondary")
                pdf.cell(0, 6, edu.year, ln=True, align="R")
            else:
                pdf.ln()
            pdf.set_font("Helvetica", "I", 9)
            pdf._set_color("secondary")
            inst_line = edu.institution
            if edu.gpa:
                inst_line += f"  |  GPA: {edu.gpa}"
            pdf.cell(0, 5, inst_line, ln=True)
            if edu.highlights:
                pdf.set_font("Helvetica", "", 9)
                pdf._set_color("text")
                pdf.safe_multi_cell(PDF_CONTENT_WIDTH, 5, edu.highlights)
            pdf.ln(2)

    # Skills
    if r.skills:
        pdf.section_title("Skills")
        pdf.set_font("Helvetica", "", 10)
        pdf._set_color("text")
        pdf.safe_multi_cell(PDF_CONTENT_WIDTH, 5, "  |  ".join(r.skills))
        pdf.ln(2)

    # Projects
    if r.projects:
        pdf.section_title("Projects")
        for proj in r.projects:
            pdf.set_font("Helvetica", "B", 10)
            pdf._set_color("text")
            pdf.cell(0, 6, proj.title, ln=False)
            if proj.technologies:
                pdf.set_font("Helvetica", "", 8)
                pdf._set_color("secondary")
                pdf.cell(0, 6, proj.technologies, ln=True, align="R")
            else:
                pdf.ln()
            if proj.link:
                pdf.set_font("Helvetica", "", 8)
                pdf._set_color("primary")
                pdf.cell(0, 4, proj.link, ln=True)
            if proj.description:
                for line in proj.description.split("\n"):
                    line = line.strip().lstrip("•-").strip()
                    if line:
                        pdf.bullet_point(line)
            pdf.ln(2)

    # Certifications
    if r.certifications:
        pdf.section_title("Certifications")
        for cert in r.certifications:
            pdf.set_font("Helvetica", "", 10)
            pdf._set_color("text")
            cert_line = cert.title
            if cert.issuer:
                cert_line += f" - {cert.issuer}"
            if cert.year:
                cert_line += f" ({cert.year})"
            pdf.cell(0, 6, cert_line, ln=True)


# ---------------------------------------------------------------------------
# Template: Corporate Executive
# ---------------------------------------------------------------------------

def _render_corporate_executive(pdf: ResumePDF, r: ResumeData) -> None:
    """Traditional navy/gold template for corporate roles."""
    pi = r.personal_info

    # Header bar
    pdf._set_fill_color("primary")
    pdf.rect(0, 0, 210, 35, "F")
    pdf.set_y(8)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 24)
    pdf.cell(0, 12, pi.name or "Your Name", ln=True, align="C")
    pdf.set_font("Helvetica", "", 10)
    contact_parts = [p for p in [pi.email, pi.phone, pi.location] if p]
    pdf.cell(0, 6, "  |  ".join(contact_parts), ln=True, align="C")
    pdf.set_y(40)
    pdf._set_color("text")

    # Links
    link_parts = [l for l in [pi.linkedin, pi.github] if l]
    if link_parts:
        pdf.set_font("Helvetica", "", 8)
        pdf._set_color("accent")
        pdf.cell(0, 5, "  |  ".join(link_parts), ln=True, align="C")
        pdf.ln(2)

    # Summary
    if pi.summary:
        pdf.section_title("Executive Summary")
        pdf.set_font("Helvetica", "", 10)
        pdf._set_color("text")
        pdf.safe_multi_cell(PDF_CONTENT_WIDTH, 5, pi.summary)
        pdf.ln(2)

    # Experience
    if r.experience:
        pdf.section_title("Professional Experience")
        for exp in r.experience:
            pdf.set_font("Helvetica", "B", 10)
            pdf._set_color("text")
            title_line = exp.job_title
            if exp.company:
                title_line += f"  |  {exp.company}"
            pdf.cell(0, 6, title_line, ln=False)
            if exp.duration:
                pdf.set_font("Helvetica", "", 9)
                pdf._set_color("secondary")
                pdf.cell(0, 6, exp.duration, ln=True, align="R")
            else:
                pdf.ln()
            if exp.description:
                for line in exp.description.split("\n"):
                    line = line.strip().lstrip("•-").strip()
                    if line:
                        pdf.bullet_point(line)
            pdf.ln(2)

    # Education
    if r.education:
        pdf.section_title("Education")
        for edu in r.education:
            pdf.set_font("Helvetica", "B", 10)
            pdf._set_color("text")
            pdf.cell(0, 6, f"{edu.degree} - {edu.institution}", ln=False)
            if edu.year:
                pdf.set_font("Helvetica", "", 9)
                pdf._set_color("secondary")
                pdf.cell(0, 6, edu.year, ln=True, align="R")
            else:
                pdf.ln()
            pdf.ln(1)

    # Skills
    if r.skills:
        pdf.section_title("Core Competencies")
        pdf.set_font("Helvetica", "", 10)
        pdf._set_color("text")
        pdf.safe_multi_cell(PDF_CONTENT_WIDTH, 5, "  |  ".join(r.skills))
        pdf.ln(2)

    # Projects
    if r.projects:
        pdf.section_title("Key Projects")
        for proj in r.projects:
            pdf.set_font("Helvetica", "B", 10)
            pdf._set_color("text")
            pdf.cell(0, 6, proj.title, ln=True)
            if proj.description:
                pdf.set_font("Helvetica", "", 9)
                pdf.safe_multi_cell(PDF_CONTENT_WIDTH, 5, proj.description)
            pdf.ln(2)

    # Certifications
    if r.certifications:
        pdf.section_title("Certifications & Awards")
        for cert in r.certifications:
            pdf.set_font("Helvetica", "", 10)
            pdf._set_color("text")
            cert_line = cert.title
            if cert.issuer:
                cert_line += f" - {cert.issuer}"
            if cert.year:
                cert_line += f" ({cert.year})"
            pdf.cell(0, 6, cert_line, ln=True)


# ---------------------------------------------------------------------------
# Template: Modern Developer
# ---------------------------------------------------------------------------

def _render_modern_developer(pdf: ResumePDF, r: ResumeData) -> None:
    """Purple/pink creative template for developers."""
    pi = r.personal_info

    # Gradient-style header
    pdf._set_fill_color("primary")
    pdf.rect(0, 0, 210, 32, "F")
    pr, pg, pb = pdf.colors["accent"]
    pdf.set_fill_color(pr, pg, pb)
    pdf.rect(0, 32, 210, 3, "F")

    pdf.set_y(8)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 22)
    pdf.cell(0, 10, pi.name or "Your Name", ln=True, align="C")
    pdf.set_font("Helvetica", "", 9)
    contact_parts = [p for p in [pi.email, pi.phone, pi.location] if p]
    pdf.cell(0, 5, "  |  ".join(contact_parts), ln=True, align="C")
    pdf.set_y(40)
    pdf._set_color("text")

    # Links
    link_parts = [l for l in [pi.linkedin, pi.github] if l]
    if link_parts:
        pdf.set_font("Helvetica", "", 8)
        pdf._set_color("primary")
        pdf.cell(0, 5, "  |  ".join(link_parts), ln=True, align="C")
        pdf.ln(2)

    # Summary
    if pi.summary:
        pdf.section_title("About Me")
        pdf.set_font("Helvetica", "", 10)
        pdf._set_color("text")
        pdf.safe_multi_cell(PDF_CONTENT_WIDTH, 5, pi.summary)
        pdf.ln(2)

    # Skills — tag style
    if r.skills:
        pdf.section_title("Tech Stack")
        pdf.set_font("Helvetica", "", 10)
        pdf._set_color("text")
        pdf.safe_multi_cell(PDF_CONTENT_WIDTH, 5, "  |  ".join(r.skills))
        pdf.ln(2)

    # Experience
    if r.experience:
        pdf.section_title("Experience")
        for exp in r.experience:
            pdf.set_font("Helvetica", "B", 10)
            pdf._set_color("primary")
            pdf.cell(0, 6, exp.job_title, ln=False)
            if exp.duration:
                pdf.set_font("Helvetica", "", 9)
                pdf._set_color("secondary")
                pdf.cell(0, 6, exp.duration, ln=True, align="R")
            else:
                pdf.ln()
            pdf.set_font("Helvetica", "I", 9)
            pdf._set_color("secondary")
            pdf.cell(0, 5, exp.company, ln=True)
            if exp.description:
                for line in exp.description.split("\n"):
                    line = line.strip().lstrip("•-").strip()
                    if line:
                        pdf.bullet_point(line)
            pdf.ln(2)

    # Projects
    if r.projects:
        pdf.section_title("Projects")
        for proj in r.projects:
            pdf.set_font("Helvetica", "B", 10)
            pdf._set_color("primary")
            proj_header = proj.title
            if proj.technologies:
                proj_header += f"  [{proj.technologies}]"
            pdf.cell(0, 6, proj_header, ln=True)
            if proj.link:
                pdf.set_font("Helvetica", "", 8)
                pdf._set_color("accent")
                pdf.cell(0, 4, proj.link, ln=True)
            if proj.description:
                for line in proj.description.split("\n"):
                    line = line.strip().lstrip("•-").strip()
                    if line:
                        pdf.bullet_point(line)
            pdf.ln(2)

    # Education
    if r.education:
        pdf.section_title("Education")
        for edu in r.education:
            pdf.set_font("Helvetica", "B", 10)
            pdf._set_color("text")
            pdf.cell(0, 6, edu.degree, ln=False)
            if edu.year:
                pdf.set_font("Helvetica", "", 9)
                pdf._set_color("secondary")
                pdf.cell(0, 6, edu.year, ln=True, align="R")
            else:
                pdf.ln()
            pdf.set_font("Helvetica", "I", 9)
            pdf._set_color("secondary")
            pdf.cell(0, 5, edu.institution, ln=True)
            pdf.ln(1)

    # Certifications
    if r.certifications:
        pdf.section_title("Certifications")
        for cert in r.certifications:
            pdf.set_font("Helvetica", "", 10)
            pdf._set_color("text")
            cert_line = cert.title
            if cert.issuer:
                cert_line += f" - {cert.issuer}"
            if cert.year:
                cert_line += f" ({cert.year})"
            pdf.cell(0, 6, cert_line, ln=True)
