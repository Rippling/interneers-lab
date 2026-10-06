from datetime import datetime
from pydantic import BaseModel, Field
from week9_10.config import MAX_DISCOUNT_RATE


class QuoteInvoiceSchema(BaseModel):
    product_id: int = Field(ge=1)
    product_name: str = Field(min_length=1, max_length=100)
    brand: str = Field(min_length=1, max_length=100)
    requested_quantity: int = Field(ge=1)

    quantity: int = Field(ge=1)
    unit_price: float = Field(gt=0)
    subtotal: float = Field(ge=0)
    discount_rate: float = Field(ge=0.0, le=MAX_DISCOUNT_RATE)
    discount_label: str = Field(min_length=1)
    discount_amount: float = Field(ge=0)
    total: float = Field(ge=0)
    stock_available: int = Field(ge=0)
    # optional warning : they get displayed only when something is wrong
    stock_warning: str | None = None
    policy_warning: str | None = None
    # default factory recalls everytime a new invoice is constructed
    generated_at: datetime = Field(default_factory=datetime.now)
