# LoanDesk – Home Loan Application Management System

LoanDesk is a Python-based home loan application management system built using **FastAPI and Streamlit**. It provides REST APIs for managing customer records and loan applications, along with an interactive admin dashboard for monitoring applications, calculating EMIs, and performing basic loan eligibility analysis.

## Features

### Backend – FastAPI
- Register and retrieve customer records.
- Create and track home loan applications.
- Calculate monthly loan EMIs.
- Validate loan amounts and customer details.
- Update loan application statuses.
- Enforce valid loan status transitions.
- Prevent duplicate customer email registrations.
- Store customer and loan information using SQLite.
- Automated API testing using Pytest.

### Frontend – Streamlit Dashboard
- Interactive admin dashboard with KPI metrics.
- Light Mode and Dark Mode.
- Customer registration through the dashboard.
- Loan application submission and management.
- Search and filter loan applications by status.
- Update loan application statuses.
- Application status distribution visualization.
- Monthly loan application trends.
- EMI calculator.
- Indicative loan eligibility and risk analysis using LTV and DTI calculations.

> **Note:** The eligibility analysis is a demonstration feature based on illustrative LTV and DTI thresholds. It does not represent an actual financial institution's loan approval decision.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| FastAPI | REST API development |
| SQLAlchemy | Database ORM |
| SQLite | Database |
| Pydantic | Data validation |
| Streamlit | Interactive dashboard |
| Pandas | Data processing |
| Plotly | Data visualization |
| Requests | API communication |
| Pytest | Automated testing |

## Project Structure

```text
LoanDesk/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── services.py
│
├── tests/
│   └── test_api.py
│
├── .streamlit/
│   └── config.toml
│
├── dashboard.py
├── requirements.txt
├── pytest.ini
├── .gitignore
└── README.md
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Aryangupta192005/LoanDesk.git
cd LoanDesk
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the FastAPI backend

```bash
uvicorn app.main:app --reload
```

The backend will run at:

`http://127.0.0.1:8000`

### 5. Access API documentation

Open the following URL in your browser:

`http://127.0.0.1:8000/docs`

FastAPI provides interactive Swagger documentation for testing the available endpoints.

### 6. Start the Streamlit dashboard

Open a second terminal, activate the virtual environment, and run:

```bash
streamlit run dashboard.py
```

The dashboard will be available at:

`http://localhost:8501`

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API welcome endpoint |
| GET | `/health` | Health check |
| POST | `/customers` | Register a customer |
| GET | `/customers` | Retrieve all customers |
| GET | `/customers/{customer_id}` | Retrieve a customer |
| POST | `/loans` | Create a loan application |
| GET | `/loans` | Retrieve loan applications |
| GET | `/loans/{loan_id}` | Retrieve a loan application |
| PATCH | `/loans/{loan_id}/status` | Update loan status |
| GET | `/calculate-emi` | Calculate monthly EMI |

## Loan Status Workflow

Loan applications follow a controlled status transition process:

```text
PENDING
   |
   ├── UNDER_REVIEW
   |       |
   |       ├── NEEDS_INFO
   |       |      |
   |       |      ├── UNDER_REVIEW
   |       |      └── REJECTED
   |       |
   |       ├── APPROVED
   |       └── REJECTED
   |
   └── REJECTED
```

Approved and rejected applications are treated as terminal states.

## Running Automated Tests

Run the test suite using:

```bash
python -m pytest -v
```

The tests cover important API functionality, validation, and loan application workflows.

## Future Improvements

- User authentication and role-based access control.
- Loan document upload and verification.
- Detailed loan status history and audit tracking.
- Database migration support.
- More comprehensive automated testing.
- Deployment and production configuration.

## Author

**Aryan Gupta**

B.Tech – Information Technology  
National Institute of Technology, Raipur

- GitHub: https://github.com/Aryangupta192005
- LinkedIn: https://www.linkedin.com/in/aryan-gupta-a0631631a/

---

*LoanDesk – A home loan application management project built with Python, FastAPI, and Streamlit.*