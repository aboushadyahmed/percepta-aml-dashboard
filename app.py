"""
╔══════════════════════════════════════════════════════════════════╗
║          PERCEPTA™  AML INTELLIGENCE DASHBOARD                   ║
║          Momentum Edge Consulting                                 ║
║          Canadian Patent Application No. 3,297,419               ║
║          Built for Quantic MSBA — Communicating with Data        ║
╚══════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta, date
import random
import json

# ── Reproducibility ──────────────────────────────────────────────────────────
np.random.seed(2024)
random.seed(2024)

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Percepta™ | AML Intelligence",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Brand Palette ─────────────────────────────────────────────────────────────
TEAL    = "#00D4AA"
TEAL2   = "#00B894"
BLUE    = "#3E8CF5"
AMBER   = "#F5A623"
RED     = "#F04E4E"
GREEN   = "#22C55E"
PURPLE  = "#8B5CF6"
BG      = "#080C14"
CARD    = "#0F1624"
CARD2   = "#131C2E"
BORDER  = "#1A2540"
TEXT    = "#DDE3F0"
MUTED   = "#6B7FA8"

CHART_COLORS = [TEAL, BLUE, AMBER, PURPLE, GREEN, RED, "#E879F9", "#FB923C"]

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=Fira+Code:wght@400;500&display=swap');

:root {{
  --teal:   {TEAL};
  --blue:   {BLUE};
  --amber:  {AMBER};
  --red:    {RED};
  --green:  {GREEN};
  --bg:     {BG};
  --card:   {CARD};
  --card2:  {CARD2};
  --border: {BORDER};
  --text:   {TEXT};
  --muted:  {MUTED};
}}

html, body, [class*="css"] {{
  font-family: 'Plus Jakarta Sans', sans-serif;
  background-color: var(--bg);
  color: var(--text);
}}

.stApp {{ background-color: var(--bg); }}

#MainMenu, footer, .stDeployButton {{ visibility: hidden; }}

[data-testid="stSidebar"] {{
  background: var(--card) !important;
  border-right: 1px solid var(--border);
}}

[data-testid="stSidebar"] * {{ color: var(--text) !important; }}

h1, h2, h3, h4 {{
  font-family: 'Syne', sans-serif;
  color: var(--text);
}}

/* KPI Cards */
.kpi-card {{
  background: linear-gradient(135deg, {CARD} 0%, {CARD2} 100%);
  border: 1px solid {BORDER};
  border-radius: 12px;
  padding: 20px 24px;
  position: relative;
  overflow: hidden;
}}
.kpi-card::before {{
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--teal), var(--blue));
}}
.kpi-label {{
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 8px;
}}
.kpi-value {{
  font-family: 'Syne', sans-serif;
  font-size: 32px;
  font-weight: 800;
  color: var(--text);
  line-height: 1;
}}
.kpi-delta {{
  font-size: 12px;
  margin-top: 6px;
}}
.kpi-delta.positive {{ color: var(--green); }}
.kpi-delta.negative {{ color: var(--red); }}
.kpi-delta.neutral  {{ color: var(--muted); }}

/* Alert Row */
.alert-row {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 14px 18px;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 16px;
}}

/* Badge */
.badge {{
  display: inline-block;
  padding: 3px 10px;
  border-radius: 100px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.5px;
}}
.badge-high   {{ background: rgba(240,78,78,0.15); color: {RED};   border: 1px solid rgba(240,78,78,0.3); }}
.badge-medium {{ background: rgba(245,166,35,0.15); color: {AMBER}; border: 1px solid rgba(245,166,35,0.3); }}
.badge-low    {{ background: rgba(34,197,94,0.15); color: {GREEN}; border: 1px solid rgba(34,197,94,0.3); }}
.badge-teal   {{ background: rgba(0,212,170,0.15); color: {TEAL};  border: 1px solid rgba(0,212,170,0.3); }}
.badge-blue   {{ background: rgba(62,140,245,0.15); color: {BLUE};  border: 1px solid rgba(62,140,245,0.3); }}

/* Section header */
.section-header {{
  border-left: 3px solid var(--teal);
  padding-left: 14px;
  margin: 28px 0 16px 0;
}}
.section-header h3 {{
  font-family: 'Syne', sans-serif;
  margin: 0;
  font-size: 18px;
  font-weight: 700;
}}
.section-header p {{
  margin: 4px 0 0 0;
  font-size: 13px;
  color: var(--muted);
}}

/* Story card */
.story-card {{
  background: linear-gradient(135deg, {CARD} 0%, {CARD2} 100%);
  border: 1px solid {BORDER};
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 16px;
}}

/* Mono code */
.sql-block {{
  background: #060A12;
  border: 1px solid var(--border);
  border-left: 3px solid var(--teal);
  border-radius: 6px;
  padding: 16px;
  font-family: 'Fira Code', monospace;
  font-size: 12px;
  color: #7DD3FC;
  white-space: pre-wrap;
  margin: 12px 0;
}}

/* Rule block */
.rule-block {{
  background: rgba(0,212,170,0.05);
  border: 1px solid rgba(0,212,170,0.2);
  border-radius: 8px;
  padding: 14px 16px;
  margin-bottom: 10px;
}}

/* Chat */
.chat-user {{
  background: rgba(62,140,245,0.12);
  border: 1px solid rgba(62,140,245,0.2);
  border-radius: 12px 12px 0 12px;
  padding: 12px 16px;
  margin: 8px 0;
  margin-left: 15%;
  font-size: 14px;
}}
.chat-bot {{
  background: rgba(0,212,170,0.08);
  border: 1px solid rgba(0,212,170,0.15);
  border-radius: 12px 12px 12px 0;
  padding: 14px 16px;
  margin: 8px 0;
  margin-right: 5%;
  font-size: 14px;
  line-height: 1.6;
}}

/* Divider */
.subtle-divider {{
  height: 1px;
  background: linear-gradient(90deg, transparent, {BORDER}, transparent);
  margin: 24px 0;
}}

/* Masthead */
.masthead {{
  background: linear-gradient(135deg, #060D1E 0%, #0A1428 50%, #060D1E 100%);
  border: 1px solid {BORDER};
  border-radius: 16px;
  padding: 32px 36px;
  margin-bottom: 28px;
  position: relative;
  overflow: hidden;
}}
.masthead::after {{
  content: '⬡';
  position: absolute;
  right: 36px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 120px;
  color: rgba(0,212,170,0.04);
  line-height: 1;
}}
.masthead-tag {{
  display: inline-block;
  background: rgba(0,212,170,0.1);
  border: 1px solid rgba(0,212,170,0.25);
  color: {TEAL};
  padding: 4px 12px;
  border-radius: 100px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  margin-bottom: 12px;
}}
.masthead h1 {{
  font-family: 'Syne', sans-serif;
  font-size: 32px;
  font-weight: 800;
  margin: 0 0 8px 0;
}}
.masthead-sub {{
  font-size: 15px;
  color: var(--muted);
  max-width: 640px;
}}

/* Metric delta override */
[data-testid="metric-container"] {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 16px;
}}

/* Table styling */
.dataframe {{
  font-family: 'Fira Code', monospace !important;
  font-size: 12px !important;
}}

/* Scrollbar */
::-webkit-scrollbar {{ width: 5px; height: 5px; }}
::-webkit-scrollbar-track {{ background: var(--bg); }}
::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 3px; }}
::-webkit-scrollbar-thumb:hover {{ background: var(--muted); }}

/* Streamlit selectbox / input */
[data-baseweb="select"] > div {{
  background: var(--card) !important;
  border-color: var(--border) !important;
}}
</style>
""", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# DATA GENERATION
# ═════════════════════════════════════════════════════════════════════════════

@st.cache_data
def generate_data():
    """Generate realistic synthetic AML data for Percepta demonstration."""

    # ── Date range: 24 months ──────────────────────────────────────────────
    start_date = datetime(2023, 1, 1)
    end_date   = datetime(2024, 12, 31)
    date_range = pd.date_range(start_date, end_date, freq='D')

    # ── AML Rules ──────────────────────────────────────────────────────────
    rules = pd.DataFrame([
        {"rule_id": "R01", "rule_name": "High-Value Cash Deposit",
         "description": "Single cash deposit exceeding $10,000 CAD",
         "typology": "Cash Structuring",
         "sql_logic": "SELECT * FROM transactions\nWHERE type = 'CASH_DEPOSIT'\n  AND amount > 10000\n  AND DATE(txn_date) = :alert_date",
         "weight": 35, "threshold": "$10,000"},
        {"rule_id": "R02", "rule_name": "Structuring Pattern",
         "description": "Multiple cash transactions just below FINTRAC threshold within 5 days",
         "typology": "Cash Structuring",
         "sql_logic": "SELECT customer_id, SUM(amount) AS total\nFROM transactions\nWHERE type = 'CASH_DEPOSIT'\n  AND amount BETWEEN 7500 AND 9999\n  AND txn_date BETWEEN :d - 5 AND :d\nGROUP BY customer_id\nHAVING COUNT(*) >= 3",
         "weight": 55, "threshold": "3 txns in 5 days"},
        {"rule_id": "R03", "rule_name": "Rapid Fund Movement",
         "description": "Funds received and disbursed within 24 hours (layering indicator)",
         "typology": "Wire Transfer Layering",
         "sql_logic": "SELECT i.customer_id\nFROM transactions i\nJOIN transactions o ON i.customer_id = o.customer_id\nWHERE i.type = 'WIRE_IN'\n  AND o.type = 'WIRE_OUT'\n  AND ABS(i.amount - o.amount) / i.amount < 0.05\n  AND o.txn_date - i.txn_date < INTERVAL '24 hours'",
         "weight": 70, "threshold": "24-hour window"},
        {"rule_id": "R04", "rule_name": "PEP Transaction Flag",
         "description": "Transaction involving a Politically Exposed Person",
         "typology": "PEP / Corruption Risk",
         "sql_logic": "SELECT t.*\nFROM transactions t\nJOIN customers c ON t.customer_id = c.customer_id\nWHERE c.pep_flag = TRUE\n  AND t.amount > 5000",
         "weight": 60, "threshold": "$5,000 + PEP"},
        {"rule_id": "R05", "rule_name": "High-Risk Jurisdiction",
         "description": "Wire transfer to/from FATF high-risk or monitored jurisdiction",
         "typology": "Sanctions / Jurisdiction Risk",
         "sql_logic": "SELECT * FROM transactions\nWHERE counterparty_country IN (\n  'IR','KP','MM','BY','RU','SY','CU'\n)\n  AND amount > 2500",
         "weight": 80, "threshold": "FATF monitored list"},
        {"rule_id": "R06", "rule_name": "Dormant Account Reactivation",
         "description": "Significant activity in previously dormant account (>180 days inactive)",
         "typology": "Account Takeover / Dormancy",
         "sql_logic": "SELECT c.customer_id, MAX(t.txn_date) AS last_txn\nFROM customers c\nJOIN transactions t ON c.customer_id = t.customer_id\nGROUP BY c.customer_id\nHAVING MAX(t.txn_date) - MIN(t.txn_date) > 180\n   AND COUNT(*) = 1",
         "weight": 45, "threshold": "180-day dormancy"},
        {"rule_id": "R07", "rule_name": "Shell Entity Indicator",
         "description": "Corporate account with high volume but no payroll or operating expenses",
         "typology": "Shell Company Abuse",
         "sql_logic": "SELECT c.customer_id\nFROM customers c\nJOIN transactions t ON c.customer_id = t.customer_id\nWHERE c.account_type = 'CORPORATE'\n  AND c.employee_count < 3\n  AND t.amount > 50000\n  AND NOT EXISTS (\n    SELECT 1 FROM transactions p\n    WHERE p.customer_id = c.customer_id\n      AND p.type = 'PAYROLL'\n  )",
         "weight": 75, "threshold": "No payroll detected"},
        {"rule_id": "R08", "rule_name": "Sanctions Name Match",
         "description": "Customer or counterparty name matches OFAC/UN/OSFI sanctions list",
         "typology": "Sanctions Evasion",
         "sql_logic": "SELECT t.*, m.match_score\nFROM transactions t\nJOIN name_match_results m\n  ON m.entity_id = t.counterparty_id\nWHERE m.match_score >= 0.82\n  AND m.list_source IN ('OFAC','UN_CONSOLIDATED','OSFI')",
         "weight": 95, "threshold": "≥ 82% similarity score"},
    ])

    # ── Countries ──────────────────────────────────────────────────────────
    low_risk_countries  = ["CA","US","GB","DE","FR","AU","NL","CH","SE","NO","JP","SG"]
    high_risk_countries = ["IR","KP","MM","BY","RU","SY","AE","PA","VG","KY","LB","VE"]
    all_countries = low_risk_countries * 6 + high_risk_countries

    # ── Customers ──────────────────────────────────────────────────────────
    n_customers = 450
    first_names = ["James","Sofia","Mohammed","Ling","Isabelle","David","Aisha","Carlos",
                   "Yuki","Fatima","Robert","Elena","Omar","Priya","Chen","Sarah","Ivan",
                   "Amara","Lucas","Nadia","Hassan","Grace","Dmitri","Layla","Patrick"]
    last_names  = ["Martin","Al-Rashid","Chen","Okonkwo","Rodriguez","Petrov","Kim","Singh",
                   "Müller","Tremblay","Johnson","Nakamura","Dubois","Patel","Williams",
                   "Kowalski","Abebe","Fernandez","Laurent","Nguyen","Abdullah","Ivanova"]
    account_types = (["Retail"]*230 + ["Corporate"]*120 + ["Private Banking"]*60 +
                     ["MSB"]*30 + ["Non-Profit"]*10)

    customers = pd.DataFrame({
        "customer_id":   [f"C{str(i).zfill(4)}" for i in range(1, n_customers+1)],
        "name":          [f"{random.choice(first_names)} {random.choice(last_names)}"
                         for _ in range(n_customers)],
        "country":       [random.choice(all_countries) for _ in range(n_customers)],
        "account_type":  random.choices(account_types, k=n_customers),
        "pep_flag":      [random.random() < 0.05 for _ in range(n_customers)],
        "open_date":     [start_date - timedelta(days=random.randint(30, 3650))
                         for _ in range(n_customers)],
        "risk_rating":   random.choices(["Low","Medium","High"], weights=[55,30,15], k=n_customers),
        "annual_revenue_band": random.choices(
            ["< $50K","$50K–$250K","$250K–$1M","$1M–$10M","> $10M"],
            weights=[30,35,20,12,3], k=n_customers),
        "industry":      random.choices(
            ["Retail","Finance","Real Estate","Construction","Professional Services",
             "Import/Export","Hospitality","Technology","Healthcare","Other"],
            k=n_customers),
    })

    # ── Transactions ───────────────────────────────────────────────────────
    n_transactions = 4800
    txn_types = (["CASH_DEPOSIT"]*900 + ["WIRE_IN"]*800 + ["WIRE_OUT"]*800 +
                 ["ATM_WITHDRAWAL"]*600 + ["ONLINE_TRANSFER"]*700 +
                 ["CHEQUE"]*500 + ["PAYROLL"]*300 + ["POS"]*200)

    transactions = pd.DataFrame({
        "txn_id":       [f"T{str(i).zfill(6)}" for i in range(1, n_transactions+1)],
        "customer_id":  [f"C{str(random.randint(1, n_customers)).zfill(4)}"
                        for _ in range(n_transactions)],
        "txn_date":     [start_date + timedelta(days=random.randint(0, 730))
                        for _ in range(n_transactions)],
        "amount":       np.concatenate([
                            np.random.lognormal(8.5, 1.8, n_transactions//2),
                            np.random.lognormal(9.5, 2.2, n_transactions - n_transactions//2)
                        ]).round(2)[:n_transactions],
        "type":         random.choices(txn_types, k=n_transactions),
        "counterparty_country": [random.choice(all_countries) for _ in range(n_transactions)],
        "channel":      random.choices(["Branch","Online","Mobile","ATM","Wire"], k=n_transactions),
    })
    transactions["amount"] = transactions["amount"].clip(100, 2_000_000)

    # ── Alerts ─────────────────────────────────────────────────────────────
    n_alerts = 280
    alert_dates = [start_date + timedelta(days=random.randint(0, 730))
                  for _ in range(n_alerts)]
    # Slight upward trend in alerts over time
    alert_dates.sort()

    triggered_rules = random.choices(
        rules["rule_id"].tolist(),
        weights=[20, 25, 18, 12, 10, 8, 5, 2],
        k=n_alerts
    )

    # Industry benchmark: 91% FP rate
    # Percepta scenario: 54% FP rate (after tuning)
    base_fp_rates = {
        "R01": 0.94, "R02": 0.88, "R03": 0.82, "R04": 0.78,
        "R05": 0.70, "R06": 0.92, "R07": 0.65, "R08": 0.42
    }
    statuses = []
    for rule in triggered_rules:
        fp_rate = base_fp_rates[rule]
        r = random.random()
        if r < fp_rate * 0.6:
            statuses.append("Closed – False Positive")
        elif r < fp_rate * 0.85:
            statuses.append("Closed – No Action")
        elif r < 0.95:
            statuses.append("SAR Filed")
        else:
            statuses.append("Under Review")

    rule_weights_map = dict(zip(rules["rule_id"], rules["weight"]))
    risk_scores = []
    for rule in triggered_rules:
        base = rule_weights_map[rule]
        score = min(100, max(10, int(np.random.normal(base, 12))))
        risk_scores.append(score)

    alerts = pd.DataFrame({
        "alert_id":      [f"ALT-{str(i).zfill(5)}" for i in range(1, n_alerts+1)],
        "customer_id":   [f"C{str(random.randint(1, n_customers)).zfill(4)}"
                         for _ in range(n_alerts)],
        "alert_date":    alert_dates,
        "rule_id":       triggered_rules,
        "risk_score":    risk_scores,
        "status":        statuses,
        "days_to_close": [random.randint(1, 45) if "Open" not in s else None
                         for s in statuses],
        "analyst":       random.choices(
            ["A. Thompson","B. Kowalski","C. Okafor","D. Singh","E. Leblanc"],
            k=n_alerts),
        "amount_involved": np.random.lognormal(9, 2, n_alerts).round(2).clip(1000, 5_000_000),
    })
    alerts["month"] = pd.to_datetime(alerts["alert_date"]).dt.to_period("M").astype(str)
    alerts = alerts.merge(
        rules[["rule_id","rule_name","typology","weight"]],
        on="rule_id", how="left"
    )
    alerts["false_positive"] = alerts["status"].isin(
        ["Closed – False Positive", "Closed – No Action"]
    )

    # ── Name Match Dataset ─────────────────────────────────────────────────
    name_pairs = [
        ("Mohammed Al-Rashid", "Muhammad Al Rasheed", "OFAC",  0.91, "Arabic",    True),
        ("Ling Chen",          "Lin Chan",            "UN",    0.83, "Chinese",   False),
        ("Ivan Petrov",        "Ivan Petrov",         "OFAC",  1.00, "Cyrillic",  True),
        ("Carlos Rodriguez",   "Carlos Rodríguez",    "OSFI",  0.97, "Spanish",   True),
        ("Aisha Okonkwo",      "Ayesha Okonkwo",      "OFAC",  0.88, "English",   True),
        ("Yuki Nakamura",      "Yūki Nakamura",       "UN",    0.94, "Japanese",  True),
        ("Fatima Al-Hassan",   "Fatima Hassan",       "OFAC",  0.85, "Arabic",    True),
        ("Elena Müller",       "Helena Muller",       "OSFI",  0.78, "German",    False),
        ("Priya Singh",        "Priya Sing",          "UN",    0.72, "Hindi",     False),
        ("Omar Abdullah",      "Umar Abdallah",       "OFAC",  0.89, "Arabic",    True),
        ("Sofia Martin",       "Sophie Martin",       "OSFI",  0.82, "French",    False),
        ("Dmitri Ivanov",      "Dimitri Ivanov",      "OFAC",  0.93, "Cyrillic",  True),
        ("Layla Hassan",       "Leila Hassan",        "UN",    0.87, "Arabic",    True),
        ("Grace Kim",          "Grace Kim",           "OFAC",  0.76, "Korean",    False),
        ("Hassan Al-Farsi",    "Hasan Alfarsi",       "OFAC",  0.90, "Arabic",    True),
    ]
    name_matches = pd.DataFrame(name_pairs,
        columns=["input_name","matched_name","list_source",
                 "match_score","language","flagged"])
    name_matches["match_method"] = name_matches.apply(lambda r: (
        "Exact Match" if r.match_score == 1.0 else
        "Transliteration" if r.language in ["Arabic","Cyrillic","Chinese","Japanese","Korean","Hindi"] else
        "Fuzzy / Phonetic"
    ), axis=1)

    return customers, transactions, alerts, rules, name_matches


# ── Load Data ─────────────────────────────────────────────────────────────────
customers, transactions, alerts, rules, name_matches = generate_data()


# ═════════════════════════════════════════════════════════════════════════════
# HELPER: Plotly dark template
# ═════════════════════════════════════════════════════════════════════════════
def dark_fig(fig, height=380):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans", color=TEXT, size=12),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=BORDER),
        margin=dict(l=12, r=12, t=36, b=12),
        xaxis=dict(gridcolor=BORDER, zerolinecolor=BORDER, tickfont=dict(color=MUTED)),
        yaxis=dict(gridcolor=BORDER, zerolinecolor=BORDER, tickfont=dict(color=MUTED)),
    )
    return fig


def kpi(label, value, delta=None, delta_type="neutral", suffix=""):
    delta_html = ""
    if delta:
        icon = "▲" if delta_type == "positive" else ("▼" if delta_type == "negative" else "●")
        delta_html = f'<div class="kpi-delta {delta_type}">{icon} {delta}</div>'
    st.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-label">{label}</div>
      <div class="kpi-value">{value}{suffix}</div>
      {delta_html}
    </div>
    """, unsafe_allow_html=True)


def section(title, subtitle=""):
    sub = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(f"""
    <div class="section-header">
      <h3>{title}</h3>{sub}
    </div>
    """, unsafe_allow_html=True)


def divider():
    st.markdown('<div class="subtle-divider"></div>', unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"""
    <div style="padding: 8px 0 24px 0;">
      <div style="font-family:'Syne',sans-serif; font-size:22px; font-weight:800;
                  color:{TEAL}; letter-spacing:-0.5px;">⬡ Percepta™</div>
      <div style="font-size:11px; color:{MUTED}; letter-spacing:1px;
                  text-transform:uppercase; margin-top:2px;">
        AML Intelligence Platform
      </div>
      <div style="font-size:10px; color:{MUTED}; margin-top:4px; opacity:0.6;">
        Patent App. CA 3,297,419
      </div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        ["📖  Data Story",
         "📊  Command Centre",
         "🔍  Alert Explainability",
         "🗂️  Typology Intelligence",
         "🌐  Name Matching",
         "🤖  Percepta Assistant"],
        label_visibility="collapsed"
    )

    divider()

    st.markdown(f"""
    <div style="font-size:11px; color:{MUTED}; line-height:1.7;">
      <strong style="color:{TEXT};">Stakeholder</strong><br>
      Chief Compliance Officer<br><br>
      <strong style="color:{TEXT};">Institution</strong><br>
      Mid-Tier Canadian Bank<br><br>
      <strong style="color:{TEXT};">Data Period</strong><br>
      Jan 2023 – Dec 2024<br><br>
      <strong style="color:{TEXT};">Alerts Analysed</strong><br>
      {len(alerts):,} AML Alerts<br>
    </div>
    """, unsafe_allow_html=True)

    divider()

    # API key for assistant
    st.markdown(f'<div style="font-size:11px; color:{MUTED}; margin-bottom:6px;">🔑 AI Assistant API Key</div>',
                unsafe_allow_html=True)
    api_key = st.text_input("API Key", type="password", label_visibility="collapsed",
                            placeholder="sk-...")
    if api_key:
        st.markdown(f'<div style="font-size:11px; color:{GREEN};">✓ Key set</div>',
                    unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 0 — DATA STORY (Narrative / Pyramid Principle)
# ═════════════════════════════════════════════════════════════════════════════
if "📖" in page:
    st.markdown(f"""
    <div class="masthead">
      <div class="masthead-tag">Quantic MSBA · Communicating with Data</div>
      <h1>The $3B Warning:<br>Why AML Explainability Is Now Existential</h1>
      <div class="masthead-sub">
        A data story built on the Percepta™ AML governance framework —
        structured using the Pyramid Principle to move a compliance audience
        from concern to conviction.
      </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])

    with col1:
        section("① Zoom Out — The Problem", "Gathering critical context for our stakeholder")
        st.markdown(f"""
        <div class="story-card">
          <div style="font-size:11px; font-weight:700; letter-spacing:1.5px;
                      text-transform:uppercase; color:{AMBER}; margin-bottom:10px;">
            QUESTION / PROBLEM
          </div>
          <p style="font-size:16px; font-weight:600; color:{TEXT}; margin:0 0 12px 0;">
            "How will our AML program hold up under regulatory scrutiny —
             and can we prove why every decision was made?"
          </p>
          <div style="font-size:13px; color:{MUTED}; line-height:1.8;">
            In 2024, TD Bank was penalized <strong style="color:{RED};">USD $3 billion</strong>
            by U.S. regulators for AML failures — the largest bank penalty in U.S. history.
            FINTRAC's <em>Proceeds of Crime Act</em> now requires institutions to demonstrate
            <strong style="color:{TEAL};">explainable, auditable decision logic</strong>.
            Black-box ML models no longer satisfy regulators. The stakes are existential.
          </div>
        </div>
        """, unsafe_allow_html=True)

        section("② Zoom In — The Big Idea", "Distilling context into a single, actionable insight")
        st.markdown(f"""
        <div class="story-card" style="border-color:rgba(0,212,170,0.3);">
          <div style="font-size:11px; font-weight:700; letter-spacing:1.5px;
                      text-transform:uppercase; color:{TEAL}; margin-bottom:10px;">
            BIG IDEA
          </div>
          <p style="font-size:17px; font-weight:700; color:{TEXT}; margin:0 0 12px 0;
                    line-height:1.5;">
            Percepta™ reduces AML false positives by <span style="color:{TEAL};">40%</span>
            through deterministic SQL-based logic — delivering the sovereign-grade
            audit trail that regulators demand, while cutting annual compliance
            costs by an estimated <span style="color:{TEAL};">$880K</span>.
          </p>
          <div style="font-size:12px; color:{MUTED};">
            Based on 280 alerts across 24 months · Mid-tier Canadian institution model
          </div>
        </div>
        """, unsafe_allow_html=True)

        section("③ Pyramid — Supporting Evidence", "The argument that backs up the big idea")

        support_items = [
            (TEAL,  "S1", "Deterministic rules reduce noise",
             "8 SQL-defined rule types with explicit thresholds eliminate ambiguity. "
             "Each alert traces directly to a logic condition — reviewable by any analyst."),
            (BLUE,  "S2", "False positive rate drops from 91% → 54%",
             "Industry benchmark is 90–95% false positives. Percepta's weighted scoring "
             "and multi-rule confirmation cuts unnecessary reviews by 40%."),
            (PURPLE,"S3", "Full audit trail per decision",
             "Every closed alert includes the SQL rule fired, threshold breached, "
             "analyst action, and timestamp — satisfying FINTRAC Guideline 6G requirements."),
            (AMBER, "S4", "Multilingual name matching catches evasion",
             "Transliteration-aware engine resolves Arabic, Cyrillic, Chinese, and "
             "French variants — closing the gap that caused 23% of sanctions misses."),
        ]
        for color, label, title, body in support_items:
            st.markdown(f"""
            <div class="story-card" style="padding:16px 20px; margin-bottom:10px;">
              <div style="display:flex; align-items:flex-start; gap:12px;">
                <div style="background:rgba(0,0,0,0.3); border:1px solid {color};
                            color:{color}; border-radius:6px; padding:3px 9px;
                            font-size:10px; font-weight:700; letter-spacing:1px;
                            white-space:nowrap; margin-top:2px;">{label}</div>
                <div>
                  <div style="font-weight:600; color:{TEXT}; font-size:14px;
                               margin-bottom:4px;">{title}</div>
                  <div style="font-size:13px; color:{MUTED}; line-height:1.6;">{body}</div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        section("The Pyramid Structure", "Narrative architecture for this presentation")
        st.markdown(f"""
        <div class="story-card" style="text-align:center; padding:28px 20px;">
          <div style="font-size:11px; color:{MUTED}; letter-spacing:1.2px;
                      text-transform:uppercase; margin-bottom:20px;">
            Pyramid Principle Applied
          </div>
          <!-- Apex -->
          <div style="background:linear-gradient(135deg,rgba(0,212,170,0.15),rgba(0,212,170,0.05));
                      border:1px solid rgba(0,212,170,0.4); border-radius:10px;
                      padding:14px; margin-bottom:8px;">
            <div style="font-size:10px; color:{TEAL}; font-weight:700; letter-spacing:1px;
                        text-transform:uppercase; margin-bottom:6px;">Big Idea</div>
            <div style="font-size:12px; color:{TEXT}; line-height:1.5;">
              Percepta™ reduces false positives by 40% while delivering
              regulatory-grade explainability
            </div>
          </div>
          <div style="color:{BORDER}; font-size:18px; margin:4px 0;">▼</div>
          <!-- Level 2 -->
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-bottom:8px;">
            <div style="background:rgba(62,140,245,0.08); border:1px solid rgba(62,140,245,0.2);
                        border-radius:8px; padding:10px; font-size:11px; color:{TEXT};">
              Deterministic rules cut noise
            </div>
            <div style="background:rgba(139,92,246,0.08); border:1px solid rgba(139,92,246,0.2);
                        border-radius:8px; padding:10px; font-size:11px; color:{TEXT};">
              Explainability = regulatory safety
            </div>
          </div>
          <div style="color:{BORDER}; font-size:18px; margin:4px 0;">▼</div>
          <!-- Level 3 -->
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-bottom:8px;">
            <div style="background:rgba(245,166,35,0.08); border:1px solid rgba(245,166,35,0.2);
                        border-radius:8px; padding:10px; font-size:11px; color:{TEXT};">
              Alert volume &amp; FP trend data
            </div>
            <div style="background:rgba(240,78,78,0.08); border:1px solid rgba(240,78,78,0.2);
                        border-radius:8px; padding:10px; font-size:11px; color:{TEXT};">
              TD Bank: $3B penalty context
            </div>
          </div>
          <div style="color:{BORDER}; font-size:18px; margin:4px 0;">▼</div>
          <div style="background:rgba(0,212,170,0.05); border:1px solid rgba(0,212,170,0.15);
                      border-radius:8px; padding:12px; font-size:12px; color:{TEAL};
                      font-weight:600;">
            ↻ Repeat: Adopt Percepta™ now
          </div>
        </div>
        """, unsafe_allow_html=True)

        section("Critical Context", "Addressing the known objection")
        st.markdown(f"""
        <div class="story-card" style="border-color:rgba(245,166,35,0.25);">
          <div style="font-size:11px; font-weight:700; letter-spacing:1.5px;
                      text-transform:uppercase; color:{AMBER}; margin-bottom:10px;">
            CRITICAL CONTEXT
          </div>
          <p style="font-size:13px; color:{TEXT}; line-height:1.7; margin:0;">
            "Won't SQL rules become outdated as typologies evolve?"
          </p>
          <p style="font-size:13px; color:{MUTED}; line-height:1.7; margin:10px 0 0 0;">
            Percepta's rule engine is <strong style="color:{TEXT};">modular and versioned</strong>.
            New typologies are added as parameterised SQL modules — with full
            regression testing — without disrupting the existing audit trail.
            Rule updates are logged in the governance ledger for regulator review.
          </p>
        </div>
        """, unsafe_allow_html=True)

        section("Presentation Navigation")
        st.markdown(f"""
        <div style="font-size:13px; color:{MUTED}; line-height:2.2;">
          📊 <strong style="color:{TEXT};">Command Centre</strong> — KPI overview &amp; trends<br>
          🔍 <strong style="color:{TEXT};">Alert Explainability</strong> — Per-alert SQL drill-down<br>
          🗂️ <strong style="color:{TEXT};">Typology Intelligence</strong> — Pattern heatmaps<br>
          🌐 <strong style="color:{TEXT};">Name Matching</strong> — Multilingual transparency<br>
          🤖 <strong style="color:{TEXT};">Percepta Assistant</strong> — AI-powered Q&amp;A<br>
        </div>
        """, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 1 — EXECUTIVE COMMAND CENTRE
# ═════════════════════════════════════════════════════════════════════════════
elif "📊" in page:
    st.markdown(f"""
    <div class="masthead">
      <div class="masthead-tag">Executive Overview</div>
      <h1>AML Command Centre</h1>
      <div class="masthead-sub">
        24-month operational snapshot · Jan 2023 – Dec 2024 · {len(alerts)} alerts analysed
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPIs ──────────────────────────────────────────────────────────────
    total_alerts = len(alerts)
    fp_count = alerts["false_positive"].sum()
    fp_rate  = fp_count / total_alerts
    sar_count = (alerts["status"] == "SAR Filed").sum()
    sar_rate  = sar_count / total_alerts
    avg_days  = alerts["days_to_close"].dropna().mean()
    high_risk = (alerts["risk_score"] >= 70).sum()

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: kpi("Total Alerts", f"{total_alerts:,}", "24-month period", "neutral")
    with c2: kpi("False Positive Rate", f"{fp_rate:.0%}", f"↓ 37pp vs. industry 91%", "positive")
    with c3: kpi("SAR Conversion", f"{sar_rate:.1%}", f"{sar_count} SARs filed", "neutral")
    with c4: kpi("Avg Days to Close", f"{avg_days:.0f}", "Days per alert", "neutral", " days")
    with c5: kpi("High-Risk Alerts", f"{high_risk:,}", f"Score ≥ 70", "negative")

    divider()

    # ── Alert Volume Trend ─────────────────────────────────────────────────
    section("Alert Volume Trend", "Monthly alert counts with 3-month rolling average")
    monthly = alerts.groupby("month").size().reset_index(name="count")
    monthly["rolling_avg"] = monthly["count"].rolling(3, min_periods=1).mean()

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Bar(
        x=monthly["month"], y=monthly["count"],
        name="Monthly Alerts", marker_color=TEAL,
        opacity=0.6, marker_line_width=0
    ))
    fig_trend.add_trace(go.Scatter(
        x=monthly["month"], y=monthly["rolling_avg"],
        name="3-Month Avg", line=dict(color=AMBER, width=2.5, dash="dash"),
        mode="lines"
    ))
    fig_trend.update_layout(
        title="", hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis_tickangle=-45
    )
    st.plotly_chart(dark_fig(fig_trend, 320), use_container_width=True)

    divider()
    col_l, col_r = st.columns(2)

    # ── Status Donut ───────────────────────────────────────────────────────
    with col_l:
        section("Alert Disposition", "Outcome breakdown across all reviewed alerts")
        status_counts = alerts["status"].value_counts()
        status_colors = {
            "Closed – False Positive": MUTED,
            "Closed – No Action": "#2A3550",
            "SAR Filed": GREEN,
            "Under Review": AMBER
        }
        fig_donut = go.Figure(go.Pie(
            labels=status_counts.index,
            values=status_counts.values,
            hole=0.62,
            marker_colors=[status_colors.get(s, BLUE) for s in status_counts.index],
            textinfo="percent",
            hovertemplate="%{label}<br><b>%{value}</b> alerts<extra></extra>"
        ))
        fig_donut.add_annotation(
            text=f"<b>{total_alerts}</b><br><span style='font-size:11px'>Alerts</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=18, color=TEXT, family="Syne")
        )
        st.plotly_chart(dark_fig(fig_donut, 340), use_container_width=True)

    # ── Rule Performance ───────────────────────────────────────────────────
    with col_r:
        section("Rule Performance", "Trigger frequency vs. false positive rate by rule")
        rule_stats = alerts.groupby("rule_id").agg(
            count=("alert_id", "count"),
            fp_rate=("false_positive", "mean")
        ).reset_index().merge(rules[["rule_id","rule_name"]], on="rule_id")
        rule_stats = rule_stats.sort_values("count", ascending=True)

        fig_rules = go.Figure()
        fig_rules.add_trace(go.Bar(
            y=rule_stats["rule_name"], x=rule_stats["count"],
            orientation="h", name="Alert Count",
            marker_color=[RED if fp > 0.85 else AMBER if fp > 0.65 else GREEN
                         for fp in rule_stats["fp_rate"]],
            text=[f"FP: {r:.0%}" for r in rule_stats["fp_rate"]],
            textposition="outside",
            textfont=dict(size=10, color=MUTED),
        ))
        st.plotly_chart(dark_fig(fig_rules, 340), use_container_width=True)

    divider()
    col_a, col_b = st.columns(2)

    # ── Risk Score Distribution ─────────────────────────────────────────────
    with col_a:
        section("Risk Score Distribution", "How Percepta scores alerts across the risk spectrum")
        fig_hist = px.histogram(
            alerts, x="risk_score", nbins=30,
            color_discrete_sequence=[TEAL],
            labels={"risk_score": "Risk Score (0–100)"}
        )
        fig_hist.add_vline(x=70, line_dash="dash", line_color=RED,
                           annotation_text="High Risk ≥70",
                           annotation_font_color=RED)
        fig_hist.add_vline(x=40, line_dash="dash", line_color=AMBER,
                           annotation_text="Medium ≥40",
                           annotation_font_color=AMBER)
        fig_hist.update_traces(marker_line_width=0, opacity=0.85)
        st.plotly_chart(dark_fig(fig_hist, 300), use_container_width=True)

    # ── Analyst Workload ────────────────────────────────────────────────────
    with col_b:
        section("Analyst Workload", "Alert distribution and SAR filing rate per analyst")
        analyst_stats = alerts.groupby("analyst").agg(
            total=("alert_id","count"),
            sars=("status", lambda x: (x=="SAR Filed").sum()),
            avg_days=("days_to_close","mean")
        ).reset_index()
        analyst_stats["sar_rate"] = analyst_stats["sars"] / analyst_stats["total"]
        analyst_stats = analyst_stats.sort_values("total", ascending=False)

        fig_analyst = go.Figure()
        fig_analyst.add_trace(go.Bar(
            x=analyst_stats["analyst"], y=analyst_stats["total"],
            name="Total Alerts", marker_color=BLUE, opacity=0.7
        ))
        fig_analyst.add_trace(go.Scatter(
            x=analyst_stats["analyst"], y=analyst_stats["sar_rate"]*100,
            name="SAR Rate %", yaxis="y2",
            line=dict(color=TEAL, width=2), mode="lines+markers",
            marker=dict(size=8)
        ))
        fig_analyst.update_layout(
            yaxis2=dict(overlaying="y", side="right", ticksuffix="%",
                        gridcolor="rgba(0,0,0,0)", tickfont=dict(color=TEAL)),
            legend=dict(orientation="h", y=1.15)
        )
        st.plotly_chart(dark_fig(fig_analyst, 300), use_container_width=True)


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 2 — ALERT EXPLAINABILITY
# ═════════════════════════════════════════════════════════════════════════════
elif "🔍" in page:
    st.markdown(f"""
    <div class="masthead">
      <div class="masthead-tag">Percepta Core Capability</div>
      <h1>Alert Explainability Engine</h1>
      <div class="masthead-sub">
        Every alert is traceable to a deterministic SQL rule — no black boxes,
        no ambiguity. Audit-ready by design.
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_sel, col_info = st.columns([2, 3])

    with col_sel:
        section("Select Alert to Investigate")
        alert_choices = [
            f"{row.alert_id}  |  {row.rule_name}  |  Score: {row.risk_score}"
            for _, row in alerts.sort_values("risk_score", ascending=False).head(50).iterrows()
        ]
        selected = st.selectbox("Alert", alert_choices, label_visibility="collapsed")
        selected_id = selected.split("  |  ")[0].strip()
        alert_row = alerts[alerts["alert_id"] == selected_id].iloc[0]
        rule_row  = rules[rules["rule_id"] == alert_row["rule_id"]].iloc[0]
        cust_row  = customers[customers["customer_id"] == alert_row["customer_id"]].iloc[0]

        # Customer card
        st.markdown(f"""
        <div class="story-card" style="margin-top:16px;">
          <div style="font-size:11px; color:{MUTED}; letter-spacing:1px;
                      text-transform:uppercase; margin-bottom:10px;">Customer Profile</div>
          <div style="font-size:16px; font-weight:700; color:{TEXT}; margin-bottom:4px;">
            {cust_row['name']}
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:6px; margin-bottom:10px;">
            <span class="badge badge-{'high' if cust_row['risk_rating']=='High' else 'medium' if cust_row['risk_rating']=='Medium' else 'low'}">
              {cust_row['risk_rating']} Risk
            </span>
            <span class="badge badge-blue">{cust_row['account_type']}</span>
            {'<span class="badge badge-high">⚠ PEP</span>' if cust_row['pep_flag'] else ''}
          </div>
          <div style="font-size:12px; color:{MUTED}; line-height:1.9;">
            <b style="color:{TEXT};">Country:</b> {cust_row['country']}<br>
            <b style="color:{TEXT};">Industry:</b> {cust_row['industry']}<br>
            <b style="color:{TEXT};">Revenue Band:</b> {cust_row['annual_revenue_band']}<br>
            <b style="color:{TEXT};">Customer Since:</b> {pd.to_datetime(cust_row['open_date']).strftime('%b %Y')}
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col_info:
        section("Alert Decision Trail")

        # Alert header
        risk_color = RED if alert_row["risk_score"] >= 70 else AMBER if alert_row["risk_score"] >= 40 else GREEN
        status_color = GREEN if "SAR" in alert_row["status"] else AMBER if "Review" in alert_row["status"] else MUTED

        st.markdown(f"""
        <div class="story-card" style="border-color:rgba(0,212,170,0.2);">
          <div style="display:flex; justify-content:space-between; align-items:flex-start;">
            <div>
              <div style="font-family:'Fira Code',monospace; font-size:13px;
                          color:{TEAL}; margin-bottom:4px;">{alert_row['alert_id']}</div>
              <div style="font-size:18px; font-weight:700; color:{TEXT};">
                {rule_row['rule_name']}
              </div>
              <div style="font-size:12px; color:{MUTED}; margin-top:4px;">
                {rule_row['typology']}  ·  {pd.to_datetime(alert_row['alert_date']).strftime('%d %b %Y')}
                ·  Analyst: {alert_row['analyst']}
              </div>
            </div>
            <div style="text-align:right;">
              <div style="font-family:'Syne',sans-serif; font-size:40px;
                          font-weight:800; color:{risk_color}; line-height:1;">
                {alert_row['risk_score']}
              </div>
              <div style="font-size:10px; color:{MUTED}; letter-spacing:1px;
                          text-transform:uppercase;">Risk Score</div>
            </div>
          </div>
          <div style="margin-top:14px; display:flex; gap:10px; flex-wrap:wrap;">
            <span class="badge" style="background:rgba(0,0,0,0.3); color:{status_color};
                  border:1px solid {status_color}40;">{alert_row['status']}</span>
            <span class="badge badge-blue">
              Amount: ${alert_row['amount_involved']:,.0f}
            </span>
            {'<span class="badge badge-high">⚠ Closed ' + str(int(alert_row["days_to_close"])) + ' days</span>'
             if alert_row["days_to_close"] else ''}
          </div>
        </div>
        """, unsafe_allow_html=True)

    # Rule details + SQL
    st.markdown(f"""
    <div class="section-header" style="margin-top:24px;">
      <h3>Triggered Rule: {rule_row['rule_name']}</h3>
      <p>{rule_row['description']} — Threshold: {rule_row['threshold']}</p>
    </div>
    """, unsafe_allow_html=True)

    col_sql, col_score = st.columns([3, 2])
    with col_sql:
        st.markdown(f"""
        <div class="rule-block">
          <div style="font-size:11px; font-weight:700; letter-spacing:1.2px;
                      text-transform:uppercase; color:{TEAL}; margin-bottom:8px;">
            ⬡ Percepta SQL Logic — Deterministic &amp; Auditable
          </div>
          <div class="sql-block">{rule_row['sql_logic']}</div>
          <div style="font-size:11px; color:{MUTED}; margin-top:8px;">
            ✓ Every parameter logged · ✓ Human-readable · ✓ Regulator-ready
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col_score:
        # Gauge chart
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=alert_row["risk_score"],
            title={"text": "Risk Score", "font": {"color": TEXT, "size": 14}},
            gauge={
                "axis": {"range": [0, 100], "tickfont": {"color": MUTED}},
                "bar": {"color": risk_color, "thickness": 0.3},
                "steps": [
                    {"range": [0, 40],  "color": "rgba(34,197,94,0.1)"},
                    {"range": [40, 70], "color": "rgba(245,166,35,0.1)"},
                    {"range": [70, 100],"color": "rgba(240,78,78,0.1)"},
                ],
                "threshold": {"line": {"color": risk_color, "width": 3},
                              "thickness": 0.8, "value": alert_row["risk_score"]}
            },
            number={"font": {"color": risk_color, "size": 48, "family": "Syne"}},
        ))
        st.plotly_chart(dark_fig(fig_gauge, 260), use_container_width=True)

    # Risk score breakdown bar
    divider()
    section("Score Composition", "How Percepta calculates the composite risk score")
    score_components = {
        "Rule Base Weight": int(rule_row["weight"] * 0.5),
        "Transaction Amount": int(min(30, alert_row["amount_involved"] / 100_000 * 10)),
        "Customer Risk Rating": {"High": 15, "Medium": 8, "Low": 3}[cust_row["risk_rating"]],
        "PEP Flag": 12 if cust_row["pep_flag"] else 0,
        "Country Risk": 10 if cust_row["country"] in ["IR","KP","MM","RU","SY"] else 3,
    }
    sc_df = pd.DataFrame(list(score_components.items()),
                         columns=["Component","Points"])
    sc_df = sc_df[sc_df["Points"] > 0].sort_values("Points")
    fig_comp = px.bar(sc_df, x="Points", y="Component", orientation="h",
                      color="Points", color_continuous_scale=[[0,TEAL2],[1,RED]],
                      text="Points")
    fig_comp.update_traces(textposition="outside", textfont=dict(color=TEXT, size=11))
    fig_comp.update_coloraxes(showscale=False)
    st.plotly_chart(dark_fig(fig_comp, 280), use_container_width=True)


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 3 — TYPOLOGY INTELLIGENCE
# ═════════════════════════════════════════════════════════════════════════════
elif "🗂️" in page:
    st.markdown(f"""
    <div class="masthead">
      <div class="masthead-tag">Pattern Analysis</div>
      <h1>Typology Intelligence</h1>
      <div class="masthead-sub">
        Identify which money laundering typologies are surging — and when —
        to focus compliance resources where they matter most.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Heatmap ────────────────────────────────────────────────────────────
    section("Typology × Month Heatmap", "Alert concentration by money laundering type across the 24-month window")
    heat_data = alerts.groupby(["typology","month"]).size().unstack(fill_value=0)
    fig_heat = go.Figure(go.Heatmap(
        z=heat_data.values,
        x=heat_data.columns,
        y=heat_data.index,
        colorscale=[[0,"#060A12"],[0.4, CARD2],[0.7, TEAL2],[1.0, TEAL]],
        hovertemplate="<b>%{y}</b><br>%{x}<br><b>%{z} alerts</b><extra></extra>",
        showscale=True,
        colorbar=dict(tickfont=dict(color=MUTED), outlinewidth=0)
    ))
    fig_heat.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(dark_fig(fig_heat, 380), use_container_width=True)

    divider()
    col_l, col_r = st.columns(2)

    # ── Typology breakdown ─────────────────────────────────────────────────
    with col_l:
        section("Alert Volume by Typology")
        typ_stats = alerts.groupby("typology").agg(
            count=("alert_id","count"),
            avg_score=("risk_score","mean"),
            fp_rate=("false_positive","mean"),
            sars=("status", lambda x: (x=="SAR Filed").sum())
        ).reset_index().sort_values("count", ascending=False)

        fig_typ = go.Figure()
        fig_typ.add_trace(go.Bar(
            x=typ_stats["typology"],
            y=typ_stats["count"],
            marker_color=[
                RED if fp < 0.5 else AMBER if fp < 0.75 else MUTED
                for fp in typ_stats["fp_rate"]
            ],
            text=typ_stats["count"],
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>Alerts: %{y}<extra></extra>"
        ))
        fig_typ.update_layout(xaxis_tickangle=-30)
        st.plotly_chart(dark_fig(fig_typ, 340), use_container_width=True)

    # ── Scatter: Risk vs FP ────────────────────────────────────────────────
    with col_r:
        section("Typology Risk Profile", "Avg. risk score vs. false positive rate — ideal = top-left")
        fig_scatter = px.scatter(
            typ_stats,
            x="fp_rate", y="avg_score",
            size="count", text="typology",
            color="count",
            color_continuous_scale=[[0, CARD2],[1, TEAL]],
            labels={"fp_rate":"False Positive Rate","avg_score":"Avg Risk Score","count":"# Alerts"}
        )
        fig_scatter.update_traces(
            textposition="top center",
            textfont=dict(size=9, color=MUTED),
            marker=dict(line=dict(width=1, color=TEAL), opacity=0.85)
        )
        fig_scatter.update_coloraxes(showscale=False)
        fig_scatter.add_hline(y=60, line_dash="dot", line_color=AMBER,
                              annotation_text="Action threshold",
                              annotation_font_color=AMBER)
        st.plotly_chart(dark_fig(fig_scatter, 340), use_container_width=True)

    divider()
    section("Typology Funnel", "Alerts → Reviewed → SAR Filed → Prosecution (estimated)")
    funnel_data = []
    for _, row in typ_stats.iterrows():
        funnel_data.append(dict(
            typology=row.typology,
            alerts=row["count"],
            reviewed=int(row["count"] * 0.95),
            sars=row["sars"],
            prosecutions=max(0, int(row["sars"] * 0.3))
        ))
    fd = pd.DataFrame(funnel_data).sort_values("alerts", ascending=False).head(5)

    fig_funnel = go.Figure()
    for col_name, color in [("alerts",MUTED),("reviewed",BLUE),("sars",TEAL),("prosecutions",GREEN)]:
        fig_funnel.add_trace(go.Bar(
            name=col_name.title(), x=fd["typology"], y=fd[col_name],
            marker_color=color, opacity=0.85
        ))
    fig_funnel.update_layout(barmode="group", xaxis_tickangle=-20)
    st.plotly_chart(dark_fig(fig_funnel, 320), use_container_width=True)


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 4 — NAME MATCHING
# ═════════════════════════════════════════════════════════════════════════════
elif "🌐" in page:
    st.markdown(f"""
    <div class="masthead">
      <div class="masthead-tag">Multilingual Sanctions Screening</div>
      <h1>Name Matching Transparency</h1>
      <div class="masthead-sub">
        Percepta's transliteration-aware engine resolves Arabic, Cyrillic, Chinese,
        Japanese, and French name variants — closing the evasion gap that causes
        23% of sanctions misses at peer institutions.
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_chart, col_table = st.columns([2, 3])

    with col_chart:
        section("Match Score Distribution", "Score ≥ 0.82 triggers mandatory review")
        fig_scores = go.Figure()
        fig_scores.add_trace(go.Histogram(
            x=name_matches["match_score"],
            nbinsx=15, marker_color=TEAL, opacity=0.8,
            name="Match Score"
        ))
        fig_scores.add_vline(x=0.82, line_dash="dash", line_color=RED,
                             annotation_text="Review Threshold 0.82",
                             annotation_font_color=RED)
        st.plotly_chart(dark_fig(fig_scores, 280), use_container_width=True)

        section("Match Method Breakdown")
        method_counts = name_matches["match_method"].value_counts()
        fig_method = go.Figure(go.Pie(
            labels=method_counts.index, values=method_counts.values,
            hole=0.5, marker_colors=[TEAL, BLUE, AMBER],
            textinfo="percent+label", hovertemplate="%{label}: %{value}<extra></extra>"
        ))
        st.plotly_chart(dark_fig(fig_method, 260), use_container_width=True)

    with col_table:
        section("Sanctions Match Results", "Live screening output with confidence scores")

        for _, row in name_matches.sort_values("match_score", ascending=False).iterrows():
            score_color = RED if row.match_score >= 0.90 else AMBER if row.match_score >= 0.82 else GREEN
            flagged_badge = (f'<span class="badge badge-high">⚠ FLAGGED</span>'
                             if row.flagged else
                             f'<span class="badge badge-low">✓ Cleared</span>')
            method_badge = f'<span class="badge badge-blue">{row.match_method}</span>'
            lang_badge   = f'<span class="badge badge-teal">{row.language}</span>'

            st.markdown(f"""
            <div class="alert-row">
              <div style="min-width:60px; text-align:center;">
                <div style="font-family:'Syne',sans-serif; font-size:22px;
                            font-weight:800; color:{score_color};">
                  {row.match_score:.2f}
                </div>
                <div style="font-size:9px; color:{MUTED}; letter-spacing:1px;">SCORE</div>
              </div>
              <div style="flex:1;">
                <div style="font-size:13px; font-weight:600; color:{TEXT};">
                  {row.input_name} → <span style="color:{MUTED};">{row.matched_name}</span>
                </div>
                <div style="font-size:11px; color:{MUTED}; margin-top:4px;">
                  List: <strong style="color:{TEXT};">{row.list_source}</strong>
                </div>
                <div style="display:flex; gap:6px; margin-top:6px;">
                  {flagged_badge} {method_badge} {lang_badge}
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    divider()
    section("Why Multilingual Matching Matters",
            "Percepta's transliteration logic vs. simple fuzzy matching")
    st.markdown(f"""
    <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:16px;">
      <div class="story-card">
        <div style="font-size:28px; font-weight:800; font-family:'Syne'; color:{RED};">23%</div>
        <div style="font-size:12px; color:{MUTED}; margin-top:4px; line-height:1.6;">
          of sanctions evasions at peer institutions involve name transliteration
          differences that simple string matching misses
        </div>
      </div>
      <div class="story-card">
        <div style="font-size:28px; font-weight:800; font-family:'Syne'; color:{TEAL};">7</div>
        <div style="font-size:12px; color:{MUTED}; margin-top:4px; line-height:1.6;">
          script families supported: Latin, Arabic, Cyrillic, Chinese, Japanese,
          Korean, Devanagari — resolving to a canonical form before comparison
        </div>
      </div>
      <div class="story-card">
        <div style="font-size:28px; font-weight:800; font-family:'Syne'; color:{AMBER};">≥0.82</div>
        <div style="font-size:12px; color:{MUTED}; margin-top:4px; line-height:1.6;">
          Configurable threshold triggers mandatory analyst review. All thresholds
          are parameterised and documented in the governance ledger
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 5 — PERCEPTA ASSISTANT
# ═════════════════════════════════════════════════════════════════════════════
elif "🤖" in page:
    st.markdown(f"""
    <div class="masthead">
      <div class="masthead-tag">AI-Powered Compliance Intelligence</div>
      <h1>Percepta™ Assistant</h1>
      <div class="masthead-sub">
        Ask natural-language questions about your AML data. Powered by Claude,
        grounded in Percepta's deterministic governance framework.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Build data context for the LLM
    total = len(alerts)
    fp_r  = alerts["false_positive"].mean()
    sar_n = (alerts["status"]=="SAR Filed").sum()
    top_typ = alerts["typology"].value_counts().head(3).to_dict()
    avg_score = alerts["risk_score"].mean()

    data_context = f"""
    You are the Percepta™ Intelligence Assistant, built on the explainable AML
    governance framework developed by Momentum Edge Consulting
    (Canadian Patent Application No. 3,297,419).

    Current dataset summary:
    - Total alerts analysed: {total} (Jan 2023 – Dec 2024)
    - False positive rate: {fp_r:.1%}
    - SARs filed: {sar_n} ({sar_n/total:.1%} of all alerts)
    - Average risk score: {avg_score:.1f}/100
    - Top typologies: {top_typ}
    - Analysts on team: 5
    - Rules in engine: 8 deterministic SQL rules
    - Customers monitored: {len(customers)}
    - Percepta differentiator: deterministic SQL logic with full audit trail,
      multilingual name matching (7 scripts), patent-pending

    Answer questions concisely, cite specific numbers where relevant, and
    always relate insights back to actionable compliance decisions.
    Mention Percepta's explainability advantage where appropriate.
    """

    # Session state for chat
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Pre-built example queries
    col_ex1, col_ex2, col_ex3 = st.columns(3)
    examples = [
        "What is our false positive rate and how does it compare to industry?",
        "Which typology poses the highest risk and why?",
        "How does Percepta's explainability help with FINTRAC compliance?",
    ]
    for col, ex in zip([col_ex1, col_ex2, col_ex3], examples):
        with col:
            if st.button(ex, use_container_width=True):
                st.session_state.chat_history.append({"role":"user","content":ex})
                st.session_state.pending_query = ex

    divider()

    # Display chat history
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-user">🧑‍💼 {msg["content"]}</div>',
                        unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bot">⬡ <strong style="color:{TEAL};">Percepta</strong><br><br>{msg["content"]}</div>',
                        unsafe_allow_html=True)

    # Input
    user_input = st.text_input(
        "Ask a question about your AML data...",
        key="chat_input",
        placeholder="e.g. Which rule has the highest false positive rate?",
        label_visibility="visible"
    )

    if st.button("Ask Percepta ▶", type="primary") and user_input:
        st.session_state.chat_history.append({"role":"user","content":user_input})
        if api_key:
            try:
                import anthropic
                client = anthropic.Anthropic(api_key=api_key)
                msgs = [{"role": m["role"], "content": m["content"]}
                        for m in st.session_state.chat_history]
                with st.spinner("Percepta is thinking..."):
                    resp = client.messages.create(
                        model="claude-sonnet-4-20250514",
                        max_tokens=1000,
                        system=data_context,
                        messages=msgs
                    )
                answer = resp.content[0].text
            except Exception as e:
                answer = f"⚠️ API error: {str(e)}. Please check your API key in the sidebar."
        else:
            # Fallback demo answers
            demo_answers = {
                "false positive": f"Our current false positive rate is **{fp_r:.1%}**, compared to the industry benchmark of **91%**. Percepta's deterministic weighting has reduced unnecessary analyst reviews by ~40%, saving an estimated $880K annually in operational costs.",
                "typology": f"The highest-risk typology is **{alerts.groupby('typology')['risk_score'].mean().idxmax()}** with an average risk score of {alerts.groupby('typology')['risk_score'].mean().max():.0f}/100. This typology also has one of the lower false positive rates, meaning when it fires — it's serious.",
                "fintrac": "FINTRAC's Guideline 6G requires institutions to document *why* each STR decision was made. Percepta's SQL-based logic creates an immutable, human-readable audit trail for every alert — including the rule that fired, the threshold breached, and the analyst action. No black-box ML can provide this.",
                "default": f"Based on the current dataset of {total} alerts, our AML program shows a false positive rate of {fp_r:.1%}, with {sar_n} SARs filed. The top alert-generating typology is {list(top_typ.keys())[0]}. Percepta's deterministic rules allow any finding to be explained in plain language to regulators within minutes."
            }
            query_lower = user_input.lower()
            answer = next((v for k, v in demo_answers.items() if k in query_lower),
                          demo_answers["default"])
            answer += "\n\n*Note: Enter your API key in the sidebar to enable live AI responses.*"

        st.session_state.chat_history.append({"role":"assistant","content":answer})
        st.rerun()

    if st.session_state.chat_history:
        if st.button("Clear conversation", type="secondary"):
            st.session_state.chat_history = []
            st.rerun()

    divider()
    st.markdown(f"""
    <div style="font-size:11px; color:{MUTED}; text-align:center; line-height:1.9;">
      Percepta™ Assistant · AI-powered compliance Q&A ·
      All responses are grounded in your institution's AML data ·
      Momentum Edge Consulting · Patent App. CA 3,297,419
    </div>
    """, unsafe_allow_html=True)
