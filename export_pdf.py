#!/usr/bin/env python3
import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

def make_pdf(output_dir="output", pdf_file="final_report.pdf"):
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("NETWORK ANALYSIS REPORT", styles['Title']))
    story.append(Spacer(1, 20))

    # Loop through files in output/
    for fname in sorted(os.listdir(output_dir)):
        fpath = os.path.join(output_dir, fname)

        # Text files (report, recommendations, etc.)
        if fname.endswith(".txt") or fname.endswith(".json"):
            story.append(Paragraph(f"File: {fname}", styles['Heading2']))
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            # Prevent text overflow: split into chunks
            for line in content.splitlines():
                story.append(Paragraph(line.replace(" ", "&nbsp;"), styles['Code']))
            story.append(PageBreak())

        # Images (topology.png, etc.)
        elif fname.endswith(".png") or fname.endswith(".jpg"):
            story.append(Paragraph(f"Image: {fname}", styles['Heading2']))
            try:
                img = Image(fpath, width=500, height=350)
                story.append(img)
            except Exception as e:
                story.append(Paragraph(f"⚠️ Could not insert image {fname}: {e}", styles['Normal']))
            story.append(PageBreak())

    # Build PDF
    pdf_path = os.path.join(output_dir, pdf_file)
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    doc.build(story)
    print(f"✅ PDF generated at {pdf_path}")

if __name__ == "__main__":
    make_pdf()

