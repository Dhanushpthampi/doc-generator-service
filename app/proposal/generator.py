import os, uuid
from jinja2 import Environment, FileSystemLoader
from playwright.sync_api import sync_playwright
from ..config import s3, R2_BUCKET, R2_PUBLIC_URL

def generate_proposal_pdf(data):
    env = Environment(loader=FileSystemLoader("proposalPages"))
    css = open("css/base.css").read()

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

    os.makedirs("output", exist_ok=True)
    file_id = str(uuid.uuid4())
    html_path = f"output/{file_id}.html"
    pdf_path = f"output/{file_id}.pdf"

    open(html_path, "w").write(html)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("file://" + os.path.abspath(html_path))
        page.pdf(path=pdf_path, format="A4", print_background=True,
                 margin={"top": "0px", "bottom": "0px", "left": "0px", "right": "0px"})
        browser.close()

    key = f"proposals/{file_id}.pdf"
    s3.upload_file(pdf_path, R2_BUCKET, key, ExtraArgs={"ContentType": "application/pdf"})

    return f"{R2_PUBLIC_URL}/{key}"
