from sqlalchemy.orm import Session
from fastapi import HTTPException

from app import models, schemas


# 1. Calculate monthly EMI
def calculate_emi(principal: float, annual_rate: float, tenure_months: int):
    if tenure_months <= 0:
        raise ValueError("Tenure must be greater than zero")

    if principal <= 0:
        raise ValueError("Loan amount must be greater than zero")

    if annual_rate == 0:
        return round(principal / tenure_months, 2)

    monthly_rate = annual_rate / (12 * 100)

    emi = (
        principal
        * monthly_rate
        * (1 + monthly_rate) ** tenure_months
        / ((1 + monthly_rate) ** tenure_months - 1)
    )

    return round(emi, 2)


# 2. Create a customer
def create_customer(db: Session, customer: schemas.CustomerCreate):
    existing_customer = (
        db.query(models.Customer)
        .filter(models.Customer.email == customer.email)
        .first()
    )

    if existing_customer:
        raise HTTPException(
            status_code=409,
            detail="A customer with this email already exists"
        )

    new_customer = models.Customer(**customer.model_dump())

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer


# 3. Create a loan application
def create_loan(db: Session, loan: schemas.LoanCreate):

    customer = (
        db.query(models.Customer)
        .filter(models.Customer.id == loan.customer_id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    if loan.requested_amount > loan.property_value:
        raise HTTPException(
            status_code=400,
            detail="Loan amount cannot exceed property value"
        )

    new_loan = models.LoanApplication(**loan.model_dump())

    db.add(new_loan)
    db.commit()
    db.refresh(new_loan)

    return new_loan


# 4. Update loan application status

def update_loan_status(
    db: Session,
    loan_id: int,
    new_status: str,
    remarks: str = None
):
    loan = (
        db.query(models.LoanApplication)
        .filter(models.LoanApplication.id == loan_id)
        .first()
    )

    if not loan:
        raise HTTPException(
            status_code=404,
            detail="Loan application not found"
        )

    allowed_transitions = {
        "PENDING": ["UNDER_REVIEW", "REJECTED"],
        "UNDER_REVIEW": ["NEEDS_INFO", "APPROVED", "REJECTED"],
        "NEEDS_INFO": ["UNDER_REVIEW", "REJECTED"],
        "APPROVED": [],
        "REJECTED": []
    }

    new_status = new_status.upper()

    if new_status not in allowed_transitions:
        raise HTTPException(
            status_code=400,
            detail="Invalid loan status"
        )

    if new_status not in allowed_transitions[loan.status]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot change status from {loan.status} to {new_status}"
        )

    history_entry = models.LoanStatusHistory(
        loan_id=loan.id,
        previous_status=loan.status,
        new_status=new_status,
        remarks=remarks
    )

    try:
        loan.status = new_status
        db.add(history_entry)
        db.commit()
        db.refresh(loan)

    except Exception:
        db.rollback()
        raise

    return loan


def get_loan_history(db: Session, loan_id: int):
    loan = (
        db.query(models.LoanApplication)
        .filter(models.LoanApplication.id == loan_id)
        .first()
    )

    if not loan:
        raise HTTPException(
            status_code=404,
            detail="Loan application not found"
        )

    return (
        db.query(models.LoanStatusHistory)
        .filter(models.LoanStatusHistory.loan_id == loan_id)
        .order_by(models.LoanStatusHistory.changed_at.desc())
        .all()
    )

def update_loan_status(
    db: Session,
    loan_id: int,
    new_status: str,
    remarks: str = None
):
    loan = (
        db.query(models.LoanApplication)
        .filter(models.LoanApplication.id == loan_id)
        .first()
    )

    if not loan:
        raise HTTPException(
            status_code=404,
            detail="Loan application not found"
        )

    allowed_transitions = {
        "PENDING": ["UNDER_REVIEW", "REJECTED"],
        "UNDER_REVIEW": ["NEEDS_INFO", "APPROVED", "REJECTED"],
        "NEEDS_INFO": ["UNDER_REVIEW", "REJECTED"],
        "APPROVED": [],
        "REJECTED": []
    }

    new_status = new_status.upper()

    if new_status not in allowed_transitions:
        raise HTTPException(
            status_code=400,
            detail="Invalid loan status"
        )

    if new_status not in allowed_transitions[loan.status]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot change status from {loan.status} to {new_status}"
        )

    history_entry = models.LoanStatusHistory(
        loan_id=loan.id,
        previous_status=loan.status,
        new_status=new_status,
        remarks=remarks
    )

    try:
        loan.status = new_status
        db.add(history_entry)
        db.commit()
        db.refresh(loan)

    except Exception:
        db.rollback()
        raise

    return loan


def get_loan_history(db: Session, loan_id: int):
    loan = (
        db.query(models.LoanApplication)
        .filter(models.LoanApplication.id == loan_id)
        .first()
    )

    if not loan:
        raise HTTPException(
            status_code=404,
            detail="Loan application not found"
        )

    return (
        db.query(models.LoanStatusHistory)
        .filter(models.LoanStatusHistory.loan_id == loan_id)
        .order_by(models.LoanStatusHistory.changed_at.desc())
        .all()
    )
