from fastapi import FastAPI
from app.invoice.models import InvoiceRequest
from app.invoice.generator import generate_invoice_pdf
from app.proposal.models import ProposalRequest
from app.proposal.generator import generate_proposal_pdf

app = FastAPI()

# ---------- Invoice Endpoint ----------
@app.post("/generate/invoice-premium")
def invoice_endpoint(data: InvoiceRequest):
    url = generate_invoice_pdf(data.dict())
    return {"url": url}

# ---------- Proposal Endpoint ----------
@app.post("/generate/proposal")
def proposal_endpoint(data: ProposalRequest):
    url = generate_proposal_pdf(data.dict())
    return {"url": url}
