# ⬡ Percepta™ AML Intelligence Dashboard

**Momentum Edge Consulting**  
Canadian Patent Application No. 3,297,419  
Built for Quantic MSBA — Communicating with Data Presentation

---

## Overview

Percepta™ is a sovereign-grade, explainable AML governance platform that transforms compliance from a cost centre into a regulatory advantage. This Streamlit dashboard demonstrates the platform's core capabilities across five interactive sections.

### Dashboard Sections

| Page | Description |
|------|-------------|
| 📖 Data Story | Pyramid-principle narrative — problem → big idea → evidence |
| 📊 Command Centre | Executive KPIs, trend analysis, analyst workload |
| 🔍 Alert Explainability | Per-alert SQL drill-down and risk score decomposition |
| 🗂️ Typology Intelligence | Heatmaps, funnels, and typology risk profiles |
| 🌐 Name Matching | Multilingual sanctions screening with confidence scores |
| 🤖 Percepta Assistant | AI-powered compliance Q&A (requires Anthropic API key) |

---

## Quick Start (Local)

```bash
# 1. Clone or download this folder
cd percepta-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

The app opens at `http://localhost:8501`

---

## Deploy to Streamlit Cloud (Free)

1. Push this folder to a **public GitHub repo**
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select repo → branch → `app.py`
5. Click **Deploy**

Your live URL will be: `https://your-app-name.streamlit.app`

### Adding Your Anthropic API Key (Streamlit Cloud)

In Streamlit Cloud dashboard:  
`Settings → Secrets → Add secret`

```toml
ANTHROPIC_API_KEY = "sk-ant-..."
```

Then update `app.py` line where `api_key` is read to also check:
```python
api_key = st.sidebar.text_input(...) or st.secrets.get("ANTHROPIC_API_KEY", "")
```

---

## Quantic Submission Checklist

- [x] 5–10 minute recorded demo presentation
- [x] Face clearly visible on camera
- [x] Government-issued ID shown
- [x] Name stated on camera
- [x] Live app demonstrated (dashboard or Streamlit Cloud link)
- [x] Slide deck (optional supplement)
- [x] Captions / transcript enabled (Loom recommended)
- [x] Stable share link (Google Drive / Streamlit Cloud)
- [x] Single recording submitted

---

## Presentation Script Outline (7 minutes)

**[0:00–0:45] Hook**  
"In 2024, TD Bank paid $3 billion in AML penalties. The root cause? Decisions that couldn't be explained. Today I'll show you how Percepta changes that."

**[0:45–1:30] Data Story Page**  
Walk through the pyramid: problem → big idea → supporting evidence → critical context.

**[1:30–3:00] Command Centre**  
"Here are the headline numbers — 280 alerts, 54% false positive rate vs. the industry's 91%, and $880K in estimated annual savings."

**[3:00–4:30] Alert Explainability**  
Select a high-risk alert. Show the SQL rule. Show the score breakdown. "This is what a regulator sees — not a black box score, but a traceable, human-readable decision."

**[4:30–5:30] Typology Intelligence**  
Show the heatmap. "Cash structuring is surging in Q3 2024 — our team can proactively allocate resources three weeks before it peaks."

**[5:30–6:30] Name Matching**  
"23% of sanctions evasions involve name variants. Percepta's transliteration engine catches Mohammed Al-Rashid whether it's spelled five different ways."

**[6:30–7:00] Close**  
"Percepta isn't just a compliance tool — it's regulatory insurance. The question isn't whether you can afford to implement it. It's whether you can afford not to."

---

## Technical Notes

- All data is **synthetic** — generated with fixed random seed for reproducibility
- No real customer or transaction data is used
- The app runs entirely client-side with no backend database required
- For production, connect to your institution's PostgreSQL/Snowflake instance

---

*© 2025 Momentum Edge Consulting. Percepta™ is a trademark of Momentum Edge Consulting.  
Patent Application CA 3,297,419 pending.*
