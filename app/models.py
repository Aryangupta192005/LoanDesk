
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


# Customer table
class Customer(Base):

    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(120), nullable=False)

    email = Column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    phone = Column(String(20), nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    loan_applications = relationship(
        "LoanApplication",
        back_populates="customer",
        cascade="all, delete-orphan"
    )


# Loan application table
class LoanApplication(Base):

    __tablename__ = "loan_applications"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False
    )

    property_value = Column(Float, nullable=False)

    requested_amount = Column(Float, nullable=False)

    annual_interest_rate = Column(Float, nullable=False)

    tenure_months = Column(Integer, nullable=False)

    purpose = Column(
        String(40),
        default="HOME_PURCHASE",
        nullable=False
    )

    status = Column(
        String(30),
        default="PENDING",
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    customer = relationship(
        "Customer",
        back_populates="loan_applications"
    )
