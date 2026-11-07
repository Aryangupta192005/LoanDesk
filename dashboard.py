import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# ============================================================
# LOANDESK ADMIN DASHBOARD
# ============================================================

st.set_page_config(
    page_title="LoanDesk Admin",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_URL = "http://127.0.0.1:8000"

# ======================== THEME =============================

if "loandesk_theme" not in st.session_state:
    st.session_state.loandesk_theme = "Light"

with st.sidebar:
    st.title("🏦 LoanDesk")
    st.caption("Admin workspace")
    st.divider()

    theme_choice = st.radio(
        "Appearance",
        ["Light", "Dark"],
        index=0 if st.session_state.loandesk_theme == "Light" else 1,
        horizontal=True,
        key="theme_radio",
    )

    st.session_state.loandesk_theme = theme_choice

    st.divider()
    st.markdown("**Navigation**")
    st.caption("Manage customers, loans and calculations.")
    st.caption("API server: `127.0.0.1:8000`")

DARK = st.session_state.loandesk_theme == "Dark"

if DARK:
    C = {
        "page": "#0e1117",
        "surface": "#171b26",
        "surface2": "#202635",
        "text": "#f1f5f9",
        "muted": "#a8b3c7",
        "border": "#30394b",
        "input": "#202635",
        "shadow": "rgba(0,0,0,0.18)",
    }
    plotly_template = "plotly_dark"
else:
    C = {
        "page": "#f5f7fb",
        "surface": "#ffffff",
        "surface2": "#f8fafc",
        "text": "#172033",
        "muted": "#64748b",
        "border": "#e2e8f0",
        "input": "#ffffff",
        "shadow": "rgba(15,23,42,0.05)",
    }
    plotly_template = "plotly_white"

# ======================== CUSTOM CSS ========================

st.markdown(
    f"""
    <style>
    :root {{
        color-scheme: {"dark" if DARK else "light"};
    }}

    .stApp {{
        background: {C["page"]};
        color: {C["text"]};
    }}

    [data-testid="stHeader"] {{
        background: transparent;
    }}

    [data-testid="stSidebar"] {{
        background: {C["surface"]};
        border-right: 1px solid {C["border"]};
    }}

    [data-testid="stSidebar"] * {{
        color: {C["text"]};
    }}

    .block-container {{
        max-width: 1500px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }}

    h1, h2, h3, h4, h5, h6,
    p, label, span, li,
    [data-testid="stMarkdownContainer"],
    [data-testid="stWidgetLabel"],
    [data-testid="stCaptionContainer"] {{
        color: {C["text"]};
    }}

    [data-testid="stCaptionContainer"] {{
        color: {C["muted"]} !important;
    }}

    [data-testid="stMetric"] {{
        background: {C["surface"]};
        border: 1px solid {C["border"]};
        border-radius: 14px;
        padding: 18px 20px;
        min-height: 112px;
        box-shadow: 0 2px 8px {C["shadow"]};
        overflow: visible;
    }}

    [data-testid="stMetricLabel"] {{
        color: {C["muted"]} !important;
        font-size: 0.9rem;
        line-height: 1.45;
        white-space: normal;
    }}

    [data-testid="stMetricValue"] {{
        color: {C["text"]} !important;
        font-size: clamp(1.25rem, 2vw, 1.8rem);
        line-height: 1.35;
        overflow-wrap: anywhere;
    }}

    [data-testid="stMetricDelta"] {{
        line-height: 1.4;
    }}

    [data-testid="stForm"] {{
        background: {C["surface"]};
        border: 1px solid {C["border"]};
        border-radius: 14px;
        padding: 22px;
    }}

    input, textarea {{
        color: {C["text"]} !important;
        background: {C["input"]} !important;
        border-color: {C["border"]} !important;
    }}

    [data-baseweb="select"] > div,
    [data-baseweb="input"] > div,
    [data-baseweb="textarea"] > div {{
        background: {C["input"]} !important;
        color: {C["text"]} !important;
        border-color: {C["border"]} !important;
    }}

    [data-baseweb="select"] *,
    [data-baseweb="popover"] *,
    [role="listbox"] * {{
        color: {C["text"]} !important;
    }}

    [data-baseweb="popover"],
    [data-baseweb="menu"] {{
        background: {C["surface"]} !important;
    }}

    /* =====================================================
       BUTTON FIX - SAME BLUE BUTTONS IN LIGHT AND DARK MODE
       ===================================================== */

    div[data-testid="stButton"] > button,
    div[data-testid="stFormSubmitButton"] > button,
    div.stButton > button,
    div.stFormSubmitButton > button,
    button[kind="primary"],
    button[kind="secondary"],
    button[data-testid^="baseButton-"] {{
        background-color: #2563eb !important;
        background: #2563eb !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        border: 1px solid #2563eb !important;
        border-radius: 9px !important;
        min-height: 44px !important;
        font-weight: 700 !important;
        opacity: 1 !important;
        box-shadow: none !important;
    }}

    div[data-testid="stButton"] > button *,
    div[data-testid="stFormSubmitButton"] > button *,
    div.stButton > button *,
    div.stFormSubmitButton > button *,
    button[kind="primary"] *,
    button[kind="secondary"] *,
    button[data-testid^="baseButton-"] * {{
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        opacity: 1 !important;
    }}

    div[data-testid="stButton"] > button:hover,
    div[data-testid="stFormSubmitButton"] > button:hover,
    div.stButton > button:hover,
    div.stFormSubmitButton > button:hover,
    button[kind="primary"]:hover,
    button[kind="secondary"]:hover,
    button[data-testid^="baseButton-"]:hover {{
        background: #1d4ed8 !important;
        background-color: #1d4ed8 !important;
        border-color: #1d4ed8 !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }}

    div[data-testid="stButton"] > button:focus,
    div[data-testid="stFormSubmitButton"] > button:focus {{
        outline: 2px solid #93c5fd !important;
        outline-offset: 2px !important;
    }}

    [data-testid="stDataFrame"],
    [data-testid="stTable"] {{
        border: 1px solid {C["border"]};
        border-radius: 10px;
        overflow: hidden;
    }}

    [data-testid="stAlert"] {{
        border-radius: 10px;
    }}

    hr {{
        border-color: {C["border"]};
        margin: 1.7rem 0;
    }}

    [data-testid="stExpander"] {{
        border: 1px solid {C["border"]};
        border-radius: 10px;
    }}

    [data-testid="stHorizontalBlock"] {{
        gap: 1rem;
    }}

    @media (max-width: 700px) {{
        .block-container {{
            padding-left: 1rem;
            padding-right: 1rem;
        }}

        [data-testid="stMetric"] {{
            padding: 14px;
            min-height: 100px;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ======================== API HELPERS =======================

def api_request(method, endpoint, **kwargs):
    try:
        response = requests.request(
            method,
            f"{API_URL}/{endpoint.lstrip('/')}",
            timeout=8,
            **kwargs,
        )
        return response
    except requests.exceptions.RequestException:
        st.error(
            "Cannot connect to LoanDesk API. Start the backend "
            "using: uvicorn app.main:app --reload"
        )
        return None


def response_detail(response, fallback):
    try:
        detail = response.json().get("detail", fallback)
        if isinstance(detail, list):
            return "; ".join(str(item) for item in detail)
        return str(detail)
    except (ValueError, AttributeError):
        return fallback


def fetch_data(endpoint):
    response = api_request("GET", endpoint)

    if response is None:
        st.stop()

    if not response.ok:
        st.error(response_detail(response, f"Could not load {endpoint}."))
        st.stop()

    try:
        data = response.json()
        return data if isinstance(data, list) else []
    except ValueError:
        st.error(f"Invalid API response for {endpoint}.")
        st.stop()


def money(value, decimals=0):
    try:
        return f"₹{float(value):,.{decimals}f}"
    except (TypeError, ValueError):
        return "₹0"


def style_chart(fig):
    fig.update_layout(
        template=plotly_template,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=C["text"]),
        margin=dict(l=15, r=15, t=55, b=15),
        title_font=dict(size=16),
        legend_title_text="",
    )
    return fig


# ======================== HEADER ============================

header_left, header_right = st.columns([4, 1])

with header_left:
    st.title("LoanDesk Admin Dashboard")
    st.caption("Home Loan Application Management System")

with header_right:
    st.write("")
    if st.button("🔄 Refresh Dashboard", use_container_width=True):
        st.rerun()

st.divider()

# ======================== LOAD DATA =========================

customers = fetch_data("customers")
loans = fetch_data("loans")

customers_df = pd.DataFrame(customers)
loans_df = pd.DataFrame(loans)

customer_columns = ["id", "full_name", "email", "phone"]

loan_columns = [
    "id", "customer_id", "property_value",
    "requested_amount", "annual_interest_rate",
    "tenure_months", "status", "purpose", "created_at",
]

for column in customer_columns:
    if column not in customers_df.columns:
        customers_df[column] = pd.Series(dtype="object")

for column in loan_columns:
    if column not in loans_df.columns:
        loans_df[column] = pd.Series(dtype="object")

for column in [
    "property_value",
    "requested_amount",
    "annual_interest_rate",
    "tenure_months",
]:
    loans_df[column] = pd.to_numeric(
        loans_df[column], errors="coerce"
    )

# ======================== KPI OVERVIEW ======================

total_customers = len(customers_df)
total_loans = len(loans_df)

status_series = (
    loans_df["status"]
    .fillna("UNKNOWN")
    .astype(str)
    .str.upper()
)

pending_loans = int((status_series == "PENDING").sum())
approved_loans = int((status_series == "APPROVED").sum())
rejected_loans = int((status_series == "REJECTED").sum())

total_requested = loans_df["requested_amount"].fillna(0).sum()

average_requested = (
    total_requested / total_loans if total_loans else 0
)

st.subheader("Business Overview")

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Customers", f"{total_customers:,}")
k2.metric("Total Applications", f"{total_loans:,}")
k3.metric("Pending Applications", f"{pending_loans:,}")
k4.metric("Approved Applications", f"{approved_loans:,}")

k5, k6, k7 = st.columns(3)
k5.metric("Rejected Applications", f"{rejected_loans:,}")
k6.metric("Total Loan Amount Requested", money(total_requested))
k7.metric("Average Loan Amount", money(average_requested))

st.divider()

# ======================== ANALYTICS =========================

st.subheader("Loan Analytics")
chart_left, chart_right = st.columns(2)

with chart_left:
    st.markdown("**Application Status Distribution**")

    if total_loans:
        status_counts = (
            status_series.value_counts()
            .rename_axis("Status")
            .reset_index(name="Applications")
        )

        fig = px.pie(
            status_counts,
            names="Status",
            values="Applications",
            hole=0.55,
        )
        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
        )
        st.plotly_chart(
            style_chart(fig),
            use_container_width=True,
        )
    else:
        st.info("No loan applications available yet.")

with chart_right:
    st.markdown("**Monthly Loan Applications**")

    if total_loans and loans_df["created_at"].notna().any():
        date_values = pd.to_datetime(
            loans_df["created_at"],
            errors="coerce",
            utc=True,
        )

        monthly_source = pd.DataFrame(
            {"created_at": date_values}
        ).dropna()

        if not monthly_source.empty:
            monthly_source["Month"] = (
                monthly_source["created_at"].dt.strftime("%Y-%m")
            )

            monthly = (
                monthly_source.groupby("Month")
                .size()
                .reset_index(name="Applications")
                .sort_values("Month")
            )

            fig = px.bar(
                monthly,
                x="Month",
                y="Applications",
                text="Applications",
                title="Applications received each month",
            )
            fig.update_traces(textposition="outside")
            st.plotly_chart(
                style_chart(fig),
                use_container_width=True,
            )
        else:
            st.info("No valid application dates available.")
    else:
        st.info("Monthly trends will appear when applications exist.")

st.divider()

# ======================== LOAN APPLICATIONS =================

st.subheader("Loan Application Management")

if total_loans:
    customer_lookup = customers_df[["id", "full_name"]].copy()

    display_df = loans_df.merge(
        customer_lookup,
        left_on="customer_id",
        right_on="id",
        how="left",
        suffixes=("", "_customer"),
    )

    display_df["Customer Name"] = (
        display_df["full_name"].fillna("Unknown")
    )

    filter1, filter2 = st.columns([1, 2])

    with filter1:
        available_statuses = sorted(status_series.unique().tolist())
        selected_status = st.selectbox(
            "Filter by Status",
            ["ALL"] + available_statuses,
        )

    with filter2:
        search_term = st.text_input(
            "Search by Customer Name or Loan ID",
            placeholder="Enter a name or loan ID",
        )

    filtered_df = display_df.copy()

    if selected_status != "ALL":
        filtered_df = filtered_df[
            filtered_df["status"].astype(str).str.upper()
            == selected_status
        ]

    if search_term.strip():
        name_match = filtered_df["Customer Name"].astype(str).str.contains(
            search_term, case=False, na=False
        )
        id_match = filtered_df["id"].astype(str).str.contains(
            search_term.strip(), case=False, na=False
        )
        filtered_df = filtered_df[name_match | id_match]

    table_columns = {
        "id": "Loan ID",
        "Customer Name": "Customer",
        "requested_amount": "Requested Amount (₹)",
        "property_value": "Property Value (₹)",
        "annual_interest_rate": "Interest Rate (%)",
        "tenure_months": "Tenure (Months)",
        "status": "Status",
        "purpose": "Purpose",
    }

    visible_columns = [
        column for column in table_columns
        if column in filtered_df.columns
    ]

    st.dataframe(
        filtered_df[visible_columns].rename(columns=table_columns),
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        f"Showing {len(filtered_df)} of {total_loans} applications."
    )
else:
    st.info("No loan applications have been submitted yet.")

st.divider()

# ======================== CUSTOMERS ========================

st.subheader("Registered Customers")

if total_customers:
    st.dataframe(
        customers_df[customer_columns].rename(
            columns={
                "id": "Customer ID",
                "full_name": "Full Name",
                "email": "Email",
                "phone": "Phone",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )
else:
    st.info("No customers registered yet.")

st.divider()

# ======================== CUSTOMER REGISTRATION ============

st.header("👤 Register New Customer")

with st.form("customer_form", clear_on_submit=True):
    customer_col1, customer_col2 = st.columns(2)

    with customer_col1:
        full_name = st.text_input("Full Name")

    with customer_col2:
        email = st.text_input("Email Address")

    phone = st.text_input("Phone Number")

    customer_submit = st.form_submit_button(
        "Register Customer",
        use_container_width=True,
    )

if customer_submit:
    if not full_name.strip() or not email.strip() or not phone.strip():
        st.error("Please fill in all customer details.")
    else:
        response = api_request(
            "POST",
            "customers",
            json={
                "full_name": full_name.strip(),
                "email": email.strip(),
                "phone": phone.strip(),
            },
        )

        if response is not None:
            if response.status_code in (200, 201):
                st.success("Customer registered successfully.")
                st.rerun()
            else:
                st.error(
                    response_detail(
                        response,
                        "Customer registration failed.",
                    )
                )

# ======================== LOAN CREATION ====================

st.header("🏠 Submit Loan Application")

if customers:
    customer_options = {
        f"{customer.get('full_name', 'Customer')} "
        f"(ID: {customer.get('id')})": customer.get("id")
        for customer in customers
    }

    with st.form("loan_form", clear_on_submit=True):
        selected_customer_label = st.selectbox(
            "Select Customer",
            list(customer_options.keys()),
        )

        loan_col1, loan_col2 = st.columns(2)

        with loan_col1:
            property_value = st.number_input(
                "Property Value (₹)",
                min_value=1,
                value=5000000,
                step=100000,
            )

            requested_amount = st.number_input(
                "Requested Loan Amount (₹)",
                min_value=1,
                value=3500000,
                step=100000,
            )

            purpose = st.selectbox(
                "Loan Purpose",
                [
                    "HOME_PURCHASE",
                    "HOME_CONSTRUCTION",
                    "HOME_RENOVATION",
                ],
            )

        with loan_col2:
            interest_rate = st.number_input(
                "Annual Interest Rate (%)",
                min_value=0.0,
                max_value=30.0,
                value=8.5,
                step=0.1,
            )

            tenure_months = st.number_input(
                "Loan Tenure (Months)",
                min_value=1,
                max_value=360,
                value=240,
            )

        loan_submit = st.form_submit_button(
            "Submit Application",
            use_container_width=True,
        )

    if loan_submit:
        if requested_amount > property_value:
            st.error(
                "Requested loan amount cannot exceed property value."
            )
        else:
            response = api_request(
                "POST",
                "loans",
                json={
                    "customer_id": customer_options[
                        selected_customer_label
                    ],
                    "property_value": property_value,
                    "requested_amount": requested_amount,
                    "annual_interest_rate": interest_rate,
                    "tenure_months": tenure_months,
                    "purpose": purpose,
                },
            )

            if response is not None:
                if response.status_code in (200, 201):
                    st.success(
                        "Loan application submitted successfully."
                    )
                    st.rerun()
                else:
                    st.error(
                        response_detail(
                            response,
                            "Loan submission failed.",
                        )
                    )
else:
    st.info(
        "Register a customer before submitting a loan application."
    )

st.divider()

# ======================== STATUS UPDATE =====================

st.header("📋 Update Loan Application Status")

allowed_transitions = {
    "PENDING": ["UNDER_REVIEW", "REJECTED"],
    "UNDER_REVIEW": ["NEEDS_INFO", "APPROVED", "REJECTED"],
    "NEEDS_INFO": ["UNDER_REVIEW", "REJECTED"],
    "APPROVED": [],
    "REJECTED": [],
}

if loans:
    loan_options = {
        (
            f"Loan #{loan.get('id')} | "
            f"{str(loan.get('status', 'UNKNOWN')).upper()} "
            f"| {money(loan.get('requested_amount', 0))}"
        ): loan
        for loan in loans
    }

    with st.form("status_form"):
        selected_loan_label = st.selectbox(
            "Select Loan Application",
            list(loan_options.keys()),
        )

        selected_loan = loan_options[selected_loan_label]

        current_status = str(
            selected_loan.get("status", "UNKNOWN")
        ).upper()

        available_transitions = allowed_transitions.get(
            current_status, []
        )

        if available_transitions:
            new_status = st.selectbox(
                "New Status",
                available_transitions,
            )

            update_submit = st.form_submit_button(
                "Update Status",
                use_container_width=True,
            )
        else:
            st.info(
                f"This application is already {current_status}."
            )
            update_submit = False
            new_status = None

    if update_submit and new_status:
        response = api_request(
            "PATCH",
            f"loans/{selected_loan['id']}/status",
            json={"status": new_status},
        )

        if response is not None:
            if response.ok:
                st.success("Loan status updated successfully.")
                st.rerun()
            else:
                st.error(
                    response_detail(
                        response,
                        "Status update failed.",
                    )
                )
else:
    st.info("No loan applications available.")

st.divider()

# ======================== EMI CALCULATOR ====================

st.header("🧮 Loan EMI Calculator")

with st.form("emi_form"):
    emi_col1, emi_col2, emi_col3 = st.columns(3)

    with emi_col1:
        emi_principal = st.number_input(
            "Loan Amount (₹)",
            min_value=1,
            value=3500000,
            step=100000,
        )

    with emi_col2:
        emi_rate = st.number_input(
            "Annual Interest Rate (%)",
            min_value=0.0,
            max_value=30.0,
            value=8.5,
            step=0.1,
        )

    with emi_col3:
        emi_tenure = st.number_input(
            "Tenure (Months)",
            min_value=1,
            max_value=360,
            value=240,
        )

    calculate_emi = st.form_submit_button(
        "Calculate EMI",
        use_container_width=True,
    )

if calculate_emi:
    response = api_request(
        "GET",
        "calculate-emi",
        params={
            "principal": emi_principal,
            "annual_rate": emi_rate,
            "tenure_months": emi_tenure,
        },
    )

    if response is not None:
        if response.ok:
            result = response.json()
            monthly_emi = float(result["monthly_emi"])
            total_payment = monthly_emi * emi_tenure
            total_interest = total_payment - emi_principal

            st.subheader("EMI Calculation Result")

            result1, result2, result3 = st.columns(3)

            result1.metric("Monthly EMI", money(monthly_emi, 2))
            result2.metric("Total Interest", money(total_interest, 2))
            result3.metric("Total Repayment", money(total_payment, 2))
        else:
            st.error(
                response_detail(
                    response,
                    "EMI calculation failed.",
                )
            )

st.divider()

# ======================== ELIGIBILITY / RISK ANALYSIS =======

st.header("📊 Loan Eligibility & Risk Analysis")

st.caption(
    "Illustrative assessment for demonstration only. "
    "It is not an actual lender approval or credit decision."
)

with st.form("eligibility_form"):
    eligibility_col1, eligibility_col2 = st.columns(2)

    with eligibility_col1:
        applicant_income = st.number_input(
            "Monthly Net Income (₹)",
            min_value=1,
            value=60000,
            step=5000,
        )

        existing_obligations = st.number_input(
            "Existing Monthly Loan EMIs (₹)",
            min_value=0,
            value=5000,
            step=1000,
        )

        requested_loan = st.number_input(
            "Requested Loan Amount (₹)",
            min_value=1,
            value=3000000,
            step=100000,
        )

    with eligibility_col2:
        eligibility_property_value = st.number_input(
            "Property Value (₹)",
            min_value=1,
            value=4000000,
            step=100000,
        )

        eligibility_rate = st.number_input(
            "Annual Interest Rate (%)",
            min_value=0.0,
            max_value=30.0,
            value=8.5,
            step=0.1,
        )

        eligibility_tenure = st.number_input(
            "Loan Tenure (Months)",
            min_value=1,
            max_value=360,
            value=240,
        )

    analyze = st.form_submit_button(
        "Analyze Eligibility",
        use_container_width=True,
    )

if analyze:
    if requested_loan > eligibility_property_value:
        st.error(
            "Requested loan amount cannot exceed property value."
        )
    else:
        response = api_request(
            "GET",
            "calculate-emi",
            params={
                "principal": requested_loan,
                "annual_rate": eligibility_rate,
                "tenure_months": eligibility_tenure,
            },
        )

        if response is not None:
            if response.ok:
                emi = float(response.json()["monthly_emi"])

                ltv = (
                    requested_loan / eligibility_property_value
                ) * 100

                total_monthly_obligation = (
                    existing_obligations + emi
                )

                dti = (
                    total_monthly_obligation / applicant_income
                ) * 100

                total_payment = emi * eligibility_tenure
                total_interest = total_payment - requested_loan

                reasons = []

                if ltv > 80:
                    reasons.append(
                        "Loan-to-Value ratio exceeds the illustrative 80% threshold."
                    )

                if dti > 40:
                    reasons.append(
                        "Monthly debt obligations exceed the illustrative 40% income threshold."
                    )

                assessment = (
                    "Needs Further Review"
                    if reasons
                    else "Indicatively Eligible"
                )

                st.subheader("Assessment Results")

                metric1, metric2, metric3 = st.columns(3)

                metric1.metric("Monthly EMI", money(emi, 2))
                metric2.metric("Loan-to-Value (LTV)", f"{ltv:.2f}%")
                metric3.metric("Debt-to-Income (DTI)", f"{dti:.2f}%")

                metric4, metric5 = st.columns(2)

                metric4.metric(
                    "Total Interest",
                    money(total_interest, 2),
                )

                metric5.metric(
                    "Total Repayment",
                    money(total_payment, 2),
                )

                if assessment == "Indicatively Eligible":
                    st.success(
                        "Indicatively Eligible — passes the demo checks."
                    )
                else:
                    st.warning("Needs Further Review")
                    st.markdown("**Reasons:**")

                    for reason in reasons:
                        st.write(f"- {reason}")

                st.caption(
                    "This demo uses simple LTV and DTI thresholds. "
                    "Actual lending decisions depend on lender policy, "
                    "credit history, income verification, property valuation "
                    "and other factors."
                )
            else:
                st.error(
                    response_detail(
                        response,
                        "Unable to calculate eligibility.",
                    )
                )

# ======================== FOOTER ============================

st.divider()

footer_left, footer_right = st.columns(2)

with footer_left:
    st.caption("LoanDesk | Admin Dashboard")

with footer_right:
    st.caption(
        "Built with Python, FastAPI, SQLAlchemy and Streamlit"
    )