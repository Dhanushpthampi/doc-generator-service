from fastapi import FastAPI
from app.invoice.models import InvoiceRequest
from app.invoice.generator import generate_invoice_pdf
from app.proposal.models import ProposalRequest
from app.proposal.generator import generate_proposal_pdf

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
