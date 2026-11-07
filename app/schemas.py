from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime


# Customer schemas

class CustomerCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    phone: str = Field(min_length=10, max_length=20)


class CustomerResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone: str
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# Loan schemas

class LoanCreate(BaseModel):
    customer_id: int
    property_value: float = Field(gt=0)
    requested_amount: float = Field(gt=0)
    annual_interest_rate: float = Field(ge=0, le=30)
    tenure_months: int = Field(gt=0, le=360)
    purpose: str = "HOME_PURCHASE"


class LoanStatusUpdate(BaseModel):
    status: str
    remarks: Optional[str] = Field(default=None, max_length=255)

class LoanResponse(BaseModel):
    id: int
    customer_id: int
    property_value: float
    requested_amount: float
    annual_interest_rate: float
    tenure_months: int
    purpose: str
    status: str
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class LoanStatusHistoryResponse(BaseModel):
    id: int
    loan_id: int
    previous_status: str
    new_status: str
    remarks: Optional[str] = None
    changed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)    