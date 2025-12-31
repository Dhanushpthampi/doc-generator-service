from pydantic import BaseModel

class InvoiceItem(BaseModel):
    name: str
    price: str

class InvoiceRequest(BaseModel):
    client_name: str
    client_address: str
    items: list[InvoiceItem]
    subtotal: str
    tax: str
    total: str
