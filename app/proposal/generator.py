import os, uuid, traceback
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from ..config import s3, R2_BUCKET, R2_PUBLIC_URL

def generate_proposal_pdf(data):
    try:
        # Get absolute path to the project root
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        template_dir = os.path.join(base_dir, "proposalPages")
        css_path = os.path.join(base_dir, "css", "base.css")
        output_dir = os.path.join(base_dir, "output")

        print(f"DEBUG: Base dir: {base_dir}")
        print(f"DEBUG: Template dir: {template_dir}")
        print(f"DEBUG: CSS path: {css_path}")

        env = Environment(loader=FileSystemLoader(template_dir))
        with open(css_path, "r") as f:
            css = f.read()

        html = f"""<!DOCTYPE html>
    <html>
    <head><meta charset="UTF-8"><style>{css}</style></head>
    <body>
    """
        for page in [
            "page1_cover.html",
            "page2_about.html",
            "page3_solution.html",
            "page4_pricing.html"
        ]:
            html += env.get_template(page).render(**data)

        html += "</body></html>"

        os.makedirs(output_dir, exist_ok=True)
        file_id = str(uuid.uuid4())
        html_path = os.path.join(output_dir, f"{file_id}.html")
        pdf_path = os.path.join(output_dir, f"{file_id}.pdf")

        with open(html_path, "w") as f:
            f.write(html)
            
        print(f"DEBUG: HTML written to {html_path}")

        print("DEBUG: Generating PDF with WeasyPrint...")
        # base_url is set to template_dir so that relative paths like "../assets/logo.jpg" work correctly.
        HTML(string=html, base_url=template_dir).write_pdf(pdf_path)
        print("DEBUG: PDF generated")

        key = f"proposals/{file_id}.pdf"
        print(f"DEBUG: Uploading to {key}")
        s3.upload_file(pdf_path, R2_BUCKET, key, ExtraArgs={"ContentType": "application/pdf"})

        return f"{R2_PUBLIC_URL}/{key}"
    
    except Exception as e:
        print(f"ERROR in generate_proposal_pdf: {str(e)}")
        traceback.print_exc()
        raise e
