from fastapi import FastAPI
from app.invoice.models import InvoiceRequest
from app.invoice.generator import generate_invoice_pdf
from app.proposal.models import ProposalRequest
from app.proposal.generator import generate_proposal_pdf
from app.nda.models import NdaRequest
from app.nda.generator import generate_nda_pdf
from app.contract.models import ContractRequest
from app.contract.generator import generate_contract_pdf

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

# ---------- NDA Endpoint ----------
@app.post("/generate/nda")
def nda_endpoint(data: NdaRequest):
    url = generate_nda_pdf(data.dict())
    return {"url": url}

# ---------- Contract Endpoint ----------
@app.post("/generate/contract")
def contract_endpoint(data: ContractRequest):
    url = generate_contract_pdf(data.dict())
    return {"url": url}
