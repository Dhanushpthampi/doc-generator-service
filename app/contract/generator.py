from jinja2 import Environment, FileSystemLoader
import weasyprint
import boto3
import os
import uuid
from app.config import R2_ENDPOINT, R2_ACCESS_KEY, R2_SECRET_KEY, R2_BUCKET, R2_PUBLIC_URL

def generate_contract_pdf(data):
    # 1. Setup paths
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    template_dir = os.path.join(base_dir, "contractPages")
    output_dir = os.path.join(base_dir, "output")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 2. Render HTML
    try:
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template("contract.html")
        html_content = template.render(data)
    except Exception as e:
        print(f"Error rendering Contract template: {e}")
        raise e

    # 3. Generate PDF
    pdf_filename = f"contract_{uuid.uuid4()}.pdf"
    pdf_path = os.path.join(output_dir, pdf_filename)

    try:
        weasyprint.HTML(string=html_content, base_url=template_dir).write_pdf(pdf_path)
    except Exception as e:
        print(f"Error converting Contract HTML to PDF: {e}")
        raise e

    # 4. Upload to R2
    key = f"documents/{pdf_filename}"
    try:
        s3 = boto3.client(
            's3',
            endpoint_url=R2_ENDPOINT,
            aws_access_key_id=R2_ACCESS_KEY,
            aws_secret_access_key=R2_SECRET_KEY
        )
        s3.upload_file(pdf_path, R2_BUCKET, key, ExtraArgs={'ContentType': 'application/pdf'})
    except Exception as e:
        print(f"Error uploading Contract to R2: {e}")
        raise e

    # 5. Return URL
    return f"{R2_PUBLIC_URL}/{key}"
