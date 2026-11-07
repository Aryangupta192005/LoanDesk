from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app import models, schemas, services
from app.database import engine, get_db, Base


# Create database tables
Base.metadata.create_all(bind=engine)


# Initialize FastAPI
app = FastAPI(
    title="LoanDesk API",
    description="A Home Loan Application Management System",
    version="1.0.0"
)


# Home route
@app.get("/")
def home():
    return {
        "message": "Welcome to LoanDesk API",
        "status": "Running"
    }


# Health check
@app.get("/health")
def health_check():
    return {"status": "healthy"}


# 1. Register a customer
@app.post("/customers", response_model=schemas.CustomerResponse, status_code=201)
def register_customer(
    customer: schemas.CustomerCreate,
    db: Session = Depends(get_db)
):
    return services.create_customer(db, customer)


# 2. Get all customers
@app.get("/customers", response_model=list[schemas.CustomerResponse])
def get_customers(db: Session = Depends(get_db)):
    return db.query(models.Customer).all()


# 3. Get a customer by ID
@app.get("/customers/{customer_id}", response_model=schemas.CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)):

    customer = db.query(models.Customer).filter(
        models.Customer.id == customer_id
    ).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return customer


# 4. Submit a loan application
@app.post("/loans", response_model=schemas.LoanResponse, status_code=201)
def submit_loan(
    loan: schemas.LoanCreate,
    db: Session = Depends(get_db)
):
    return services.create_loan(db, loan)


# 5. Get all loan applications
@app.get("/loans", response_model=list[schemas.LoanResponse])
def get_loans(
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.LoanApplication)

    if status:
        query = query.filter(
            models.LoanApplication.status == status.upper()
        )

    return query.order_by(
        models.LoanApplication.created_at.desc()
    ).all()


# 6. Get a particular loan application
@app.get("/loans/{loan_id}", response_model=schemas.LoanResponse)
def get_loan(loan_id: int, db: Session = Depends(get_db)):

    loan = db.query(models.LoanApplication).filter(
        models.LoanApplication.id == loan_id
    ).first()

    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    return loan


# 7. Update loan application status
@app.patch("/loans/{loan_id}/status", response_model=schemas.LoanResponse)
def change_loan_status(
    loan_id: int,
    update: schemas.LoanStatusUpdate,
    db: Session = Depends(get_db)
):
    return services.update_loan_status(
        db,
        loan_id,
        update.status,
        update.remarks
    )


# 8. Calculate EMI
@app.get("/calculate-emi")
def get_emi(
    principal: float,
    annual_rate: float,
    tenure_months: int
):
    try:
        emi = services.calculate_emi(
            principal,
            annual_rate,
            tenure_months
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    return {
        "principal": principal,
        "annual_interest_rate": annual_rate,
        "tenure_months": tenure_months,
        "monthly_emi": emi
    }
@app.get(
    "/loans/{loan_id}/history",
    response_model=list[schemas.LoanStatusHistoryResponse]
)
def get_loan_status_history(
    loan_id: int,
    db: Session = Depends(get_db)
):
    return services.get_loan_history(db, loan_id)