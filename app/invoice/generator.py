import os, uuid
from jinja2 import Environment, FileSystemLoader
from playwright.sync_api import sync_playwright
from ..config import s3, R2_BUCKET, R2_PUBLIC_URL

    try:
        # Get absolute path to the project root
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        template_dir = os.path.join(base_dir, "invoicePages")
        css_path = os.path.join(base_dir, "css", "base.css")
        output_dir = os.path.join(base_dir, "output")
        
        print(f"DEBUG: Base dir: {base_dir}")
        print(f"DEBUG: Template dir: {template_dir}")
        print(f"DEBUG: CSS path: {css_path}")

        env = Environment(loader=FileSystemLoader(template_dir))
        with open(css_path, "r") as f:
            css = f.read()

        html = f"""
        <!DOCTYPE html>
        <html>
        <head><meta charset="UTF-8"><style>{css}</style></head>
        <body>
        """

        html += env.get_template("invoice.html").render(
            **data,
            invoice_number=str(uuid.uuid4())[:8],
            date="2026-01-01",
            due_date="2026-01-07"
        )
        html += "</body></html>"

        os.makedirs(output_dir, exist_ok=True)
        file_id = str(uuid.uuid4())
        html_path = os.path.join(output_dir, f"{file_id}.html")
        pdf_path = os.path.join(output_dir, f"{file_id}.pdf")

        with open(html_path, "w") as f:
            f.write(html)
        
        print(f"DEBUG: HTML written to {html_path}")

        with sync_playwright() as p:
            print("DEBUG: Launching browser...")
            browser = p.chromium.launch(args=['--no-sandbox', '--disable-setuid-sandbox'])
            page = browser.new_page()
            print(f"DEBUG: Navigating to {html_path}")
            page.goto("file://" + html_path)
            print("DEBUG: Generating PDF...")
            page.pdf(path=pdf_path, format="A4", print_background=True,
                     margin={"top": "0px", "bottom": "0px", "left": "0px", "right": "0px"})
            browser.close()
            print("DEBUG: PDF generated")

        key = f"invoices/{file_id}.pdf"
        print(f"DEBUG: Uploading to {key}")
        s3.upload_file(pdf_path, R2_BUCKET, key, ExtraArgs={"ContentType": "application/pdf"})

        return f"{R2_PUBLIC_URL}/{key}"

    except Exception as e:
        print(f"ERROR in generate_invoice_pdf: {str(e)}")
        import traceback
        traceback.print_exc()
        raise e
