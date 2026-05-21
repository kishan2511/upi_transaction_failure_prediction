import streamlit as st
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="UPI Failure Analyser",
    page_icon="💳",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
/* ── Base ── */
.stApp { background: #f5f7ff; }
h1, h2, h3 { color: #1e3a8a; }

/* ── Header ── */
.app-header {
    background: linear-gradient(135deg, #0a2463 0%, #1e40af 70%, #3b82f6 100%);
    color: white; padding: 2rem 2rem 1.6rem;
    border-radius: 16px; text-align: center;
    box-shadow: 0 6px 24px rgba(10,36,99,.28);
    margin-bottom: 1.8rem;
}
.app-header h1 { font-size: 1.8rem; font-weight: 800; margin: 0; color: white; }
.app-header p  { font-size: 0.9rem; opacity: .82; margin: .5rem 0 0; color: white; }

/* ── Step pill ── */
.step-pill {
    display: inline-flex; align-items: center; gap: 8px;
    background: #e0e7ff; color: #1e40af;
    padding: 5px 14px; border-radius: 99px;
    font-size: .82rem; font-weight: 700;
    margin-bottom: .7rem;
}

/* ── Card ── */
.card {
    background: white; border-radius: 14px;
    padding: 1.4rem 1.6rem; margin-bottom: 1.2rem;
    box-shadow: 0 2px 12px rgba(0,0,0,.07);
}
.card-title {
    font-size: .78rem; font-weight: 800;
    text-transform: uppercase; letter-spacing: 1.2px;
    color: #1e40af; margin-bottom: 1rem;
    padding-bottom: 6px; border-bottom: 2px solid #e0e7ff;
}

/* ── Scenario buttons ── */
.scenario-grid { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: .4rem; }
.sc-btn {
    background: #eff6ff; color: #1d4ed8;
    border: 1.5px solid #bfdbfe; border-radius: 8px;
    padding: 6px 14px; font-size: .82rem; font-weight: 600;
    cursor: pointer; transition: all .15s;
}
.sc-btn:hover { background: #dbeafe; }

/* ── Predict button ── */
div.stButton > button {
    background: linear-gradient(135deg, #1e40af, #3b82f6);
    color: white; font-weight: 800; font-size: 1.1rem;
    border-radius: 12px; padding: .75rem 2rem;
    border: none; width: 100%;
    box-shadow: 0 4px 16px rgba(30,64,175,.35);
    letter-spacing: .5px;
}
div.stButton > button:hover {
    background: linear-gradient(135deg, #1e3a8a, #2563eb);
    box-shadow: 0 6px 20px rgba(30,64,175,.45);
}

/* ── Result ── */
.result-box {
    background: linear-gradient(135deg, #0a2463, #1e40af);
    color: white; border-radius: 16px; padding: 2rem 1.8rem;
    text-align: center; margin-bottom: 1.2rem;
    box-shadow: 0 6px 28px rgba(30,64,175,.32);
}
.result-icon { font-size: 3rem; margin-bottom: .4rem; }
.result-cause{ font-size: 1.8rem; font-weight: 800; margin: .2rem 0; }
.result-conf { font-size: 1rem; opacity: .85; }
.conf-track  { background: rgba(255,255,255,.25); border-radius: 99px; height: 8px; margin: .8rem 0 .3rem; }
.conf-fill   { background: #93c5fd; border-radius: 99px; height: 8px; }

/* ── Action box ── */
.action-ok     { background:#f0fdf4; border-left:4px solid #16a34a; border-radius:0 10px 10px 0; padding:1rem 1.2rem; }
.action-warn   { background:#fff7ed; border-left:4px solid #f97316; border-radius:0 10px 10px 0; padding:1rem 1.2rem; }
.action-danger { background:#fef2f2; border-left:4px solid #dc2626; border-radius:0 10px 10px 0; padding:1rem 1.2rem; }

/* ── Tip ── */
.tip { background:#eff6ff; border-radius:8px; padding:.6rem 1rem; font-size:.83rem; color:#1e40af; margin-top:.5rem; }

/* ── Metric strip ── */
.mstrip { display:flex; gap:10px; margin-bottom:1.4rem; }
.mc {
    flex:1; background:white; border-radius:10px; padding:.9rem;
    text-align:center; box-shadow:0 2px 8px rgba(0,0,0,.07);
    border-top:3px solid #3b82f6;
}
.mc .v { font-size:1.4rem; font-weight:800; color:#1e40af; }
.mc .l { font-size:.72rem; color:#64748b; margin-top:2px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  DATA & MODEL
# ─────────────────────────────────────────────
ROOT_CAUSES = [
    'Bank_Server_Down','Insufficient_Funds','Wrong_Credentials',
    'Network_Timeout','VPA_Not_Found','Fraud_Flag',
    'NPCI_Gateway_Error','User_Declined'
]
BANKS    = ['SBI','HDFC','ICICI','AXIS','PNB','BOB','Canara','Kotak','Yes Bank','IDFC First']
CAUSE_ICONS = {
    'Bank_Server_Down':   '🏦',
    'Insufficient_Funds': '💰',
    'Wrong_Credentials':  '🔐',
    'Network_Timeout':    '📡',
    'VPA_Not_Found':      '❓',
    'Fraud_Flag':         '🚨',
    'NPCI_Gateway_Error': '🔌',
    'User_Declined':      '🙅',
}
ADVICE = {
    'Bank_Server_Down':   ('warn',  '🏦  Bank servers are down/degraded. Wait 10–15 min and retry. Contact your bank if it persists.'),
    'Insufficient_Funds': ('warn',  '💰  Balance is too low. Top up your account and retry.'),
    'Wrong_Credentials':  ('danger','🔐  Wrong UPI PIN detected. Verify your PIN — multiple failures can lock your account.'),
    'Network_Timeout':    ('warn',  '📡  Poor signal caused a timeout. Switch to WiFi or better coverage and retry.'),
    'VPA_Not_Found':      ('warn',  '❓  The UPI ID (VPA) is not registered. Double-check the payee address.'),
    'Fraud_Flag':         ('danger','🚨  Flagged as suspicious. Contact your bank immediately if this is a genuine payment.'),
    'NPCI_Gateway_Error': ('warn',  '🔌  NPCI backend is slow. This is a system issue — retry in 5 minutes.'),
    'User_Declined':      ('ok',    '🙅  Payee declined the payment. Confirm with them and ask to accept.'),
}

# ── Quick scenarios ──────────────────────────
SCENARIOS = {
    "Network Drop": dict(amount=1200.0, payer_bank="HDFC", payee_bank="SBI",
                         txn_type="P2P", network_type="3G", device_os="Android",
                         response_time=4200, retry_count=2, latency=45,
                         hour=21, day_of_week=4, server_status="Healthy"),
    "Low Balance":  dict(amount=95000.0, payer_bank="SBI", payee_bank="ICICI",
                         txn_type="P2M", network_type="4G", device_os="iOS",
                         response_time=320, retry_count=0, latency=30,
                         hour=11, day_of_week=1, server_status="Healthy"),
    "Server Down":  dict(amount=3500.0, payer_bank="AXIS", payee_bank="PNB",
                         txn_type="P2P", network_type="WiFi", device_os="Android",
                         response_time=2800, retry_count=1, latency=55,
                         hour=9, day_of_week=2, server_status="Down"),
    "Wrong PIN":    dict(amount=750.0, payer_bank="Kotak", payee_bank="HDFC",
                         txn_type="P2M", network_type="4G", device_os="iOS",
                         response_time=280, retry_count=4, latency=28,
                         hour=14, day_of_week=0, server_status="Healthy"),
    "Fraud Alert":  dict(amount=320000.0, payer_bank="Yes Bank", payee_bank="ICICI",
                         txn_type="P2P", network_type="WiFi", device_os="Android",
                         response_time=410, retry_count=0, latency=40,
                         hour=2, day_of_week=6, server_status="Healthy"),
}

@st.cache_resource(show_spinner="Training AI model on 30,000 UPI transactions...")
def train_model():
    np.random.seed(42)
    n = 30000
    FAIL_P = np.array([0.38,0.10,0.08,0.27,0.07,0.02,0.05,0.03])
    is_success = (np.random.rand(n) < 0.72)
    root = np.array(['Success']*n, dtype=object)
    fail_idx = np.where(~is_success)[0]
    root[fail_idx] = np.random.choice(ROOT_CAUSES, size=len(fail_idx), p=FAIL_P)

    svr = np.random.choice(['Healthy','Degraded','Down'], n, p=[0.88,0.09,0.03])
    net = np.random.choice(['4G','WiFi','3G','5G'], n, p=[0.50,0.32,0.10,0.08])
    txn = np.random.choice(['P2P','P2M'], n, p=[0.62,0.38])

    data = pd.DataFrame({
        'amount':                   np.clip(np.random.lognormal(4.2,1.1,n),1,500000).round(2),
        'payer_bank':               np.random.choice(BANKS, n),
        'payee_bank':               np.random.choice(BANKS, n),
        'transaction_type':         txn,
        'device_os':                np.random.choice(['Android','iOS','Web'], n, p=[0.72,0.25,0.03]),
        'network_type':             net,
        'response_time_ms':         np.random.gamma(2.0,450,n),
        'retry_count':              np.random.poisson(0.35,n),
        'hour':                     np.random.randint(0,24,n),
        'day_of_week':              np.random.randint(0,7,n),
        'bank_server_status':       svr,
        'npci_gateway_latency_ms':  np.random.gamma(1.5,32,n),
        'root_cause':               root,
    })
    for cls in ROOT_CAUSES:
        m = data['root_cause'] == cls
        if cls == 'Network_Timeout':
            data.loc[m,'response_time_ms'] += np.random.uniform(2200,5500,m.sum())
        elif cls == 'Bank_Server_Down':
            data.loc[m,'bank_server_status'] = np.random.choice(['Degraded','Down'],m.sum(),p=[0.35,0.65])
            data.loc[m,'response_time_ms']   += np.random.uniform(700,3000,m.sum())
        elif cls == 'Wrong_Credentials':
            data.loc[m,'retry_count'] += np.random.randint(2,6,m.sum())
        elif cls == 'Fraud_Flag':
            data.loc[m,'amount'] *= np.random.uniform(2.0,4.0,m.sum())
        elif cls == 'NPCI_Gateway_Error':
            data.loc[m,'npci_gateway_latency_ms'] += np.random.uniform(150,400,m.sum())
            data.loc[m,'response_time_ms']         += np.random.uniform(500,2000,m.sum())

    df_fail = data[data['root_cause']!='Success'].copy()
    X = df_fail.drop('root_cause',axis=1)
    y = df_fail['root_cause']
    X_tr,X_te,y_tr,y_te = train_test_split(X,y,test_size=0.2,random_state=42,stratify=y)

    cat_cols = ['payer_bank','payee_bank','transaction_type','device_os','network_type','bank_server_status']
    ct = ColumnTransformer([('ohe',OneHotEncoder(handle_unknown='ignore'),cat_cols)],remainder='passthrough')
    pipe = Pipeline([('pre',ct),('clf',RandomForestClassifier(n_estimators=150,random_state=42,n_jobs=-1))])
    pipe.fit(X_tr,y_tr)
    acc = pipe.score(X_te,y_te)
    return pipe, acc


model, accuracy = train_model()

# ─────────────────────────────────────────────
#  SESSION STATE – store selected scenario
# ─────────────────────────────────────────────
if "scenario" not in st.session_state:
    st.session_state.scenario = None

# ─────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <h1>💳 UPI Transaction Failure Analyser</h1>
    <p>Fill in the transaction details → click Analyse → get the root cause instantly</p>
    <p style="margin-top:.6rem;opacity:.65;font-size:.78rem">
        GTU PGDDS Mini Project &nbsp;|&nbsp; Kishan Patel · 251370680017 &nbsp;|&nbsp; Guide: Komal Prajapati
    </p>
</div>
""", unsafe_allow_html=True)

# ── Metric strip ──
st.markdown(f"""
<div class="mstrip">
  <div class="mc"><div class="v">🤖 RF</div><div class="l">Model</div></div>
  <div class="mc"><div class="v">{accuracy*100:.1f}%</div><div class="l">Accuracy</div></div>
  <div class="mc"><div class="v">8</div><div class="l">Failure Types</div></div>
  <div class="mc"><div class="v">30K</div><div class="l">Transactions</div></div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  STEP 1 – Quick Fill
# ─────────────────────────────────────────────
st.markdown('<div class="step-pill">⚡ Quick Fill — try a sample scenario</div>', unsafe_allow_html=True)
sc_cols = st.columns(len(SCENARIOS))
for i, (label, vals) in enumerate(SCENARIOS.items()):
    if sc_cols[i].button(label, key=f"sc_{label}", use_container_width=True):
        st.session_state.scenario = label

sc = SCENARIOS.get(st.session_state.scenario, {})

def sv(key, default):
    return sc.get(key, default)

# ─────────────────────────────────────────────
#  STEP 2 – Transaction Details
# ─────────────────────────────────────────────
st.markdown('<div class="step-pill">📋 Step 1 · Transaction Details</div>', unsafe_allow_html=True)
with st.container():
    c1, c2 = st.columns(2)
    with c1:
        amount = st.number_input(
            "Amount (₹)", min_value=1.0, max_value=500000.0,
            value=float(sv("amount", 1200.0)), step=100.0, format="%.2f",
            help="Transaction amount in Indian Rupees"
        )
        payer_bank = st.selectbox(
            "Your Bank (Payer)", BANKS,
            index=BANKS.index(sv("payer_bank","HDFC")),
            help="Bank from which money is being sent"
        )
        payee_bank = st.selectbox(
            "Recipient's Bank (Payee)", BANKS,
            index=BANKS.index(sv("payee_bank","SBI")),
            help="Bank receiving the money"
        )
    with c2:
        txn_label  = "P2P (Person to Person)" if sv("txn_type","P2P")=="P2P" else "P2M (Person to Merchant)"
        txn_type   = st.selectbox(
            "Transaction Type",
            ["P2P (Person to Person)","P2M (Person to Merchant)"],
            index=0 if sv("txn_type","P2P")=="P2P" else 1,
            help="P2P = sending to another person · P2M = paying a merchant/shop"
        )
        device_os  = st.selectbox(
            "Device Used", ["Android","iOS","Web"],
            index=["Android","iOS","Web"].index(sv("device_os","Android")),
            help="Phone or device used for the transaction"
        )
        network_type = st.selectbox(
            "Network / Connection", ["4G","WiFi","3G","5G"],
            index=["4G","WiFi","3G","5G"].index(sv("network_type","4G")),
            help="Internet connection type at the time of payment"
        )

# ─────────────────────────────────────────────
#  STEP 3 – Technical Details (collapsible)
# ─────────────────────────────────────────────
st.markdown('<div class="step-pill">⚙️ Step 2 · Technical Details <span style="font-weight:400;opacity:.7">(optional – expand for advanced inputs)</span></div>', unsafe_allow_html=True)

with st.expander("Show technical / advanced fields", expanded=(st.session_state.scenario is not None)):
    t1, t2, t3 = st.columns(3)
    with t1:
        response_time = st.number_input(
            "Response Time (ms)", min_value=50, max_value=10000,
            value=int(sv("response_time", 450)), step=100,
            help="How long the server took to respond. >3000 ms is usually a timeout."
        )
        server_status = st.selectbox(
            "Bank Server Status", ["Healthy","Degraded","Down"],
            index=["Healthy","Degraded","Down"].index(sv("server_status","Healthy")),
            help="Current health of your bank's server"
        )
    with t2:
        retry_count = st.number_input(
            "Retry Count", min_value=0, max_value=10,
            value=int(sv("retry_count", 0)),
            help="How many times the transaction was retried before failing"
        )
        latency = st.number_input(
            "NPCI Gateway Latency (ms)", min_value=5, max_value=700,
            value=int(sv("latency", 48)), step=5,
            help="Latency of the NPCI payment network"
        )
    with t3:
        hour = st.slider(
            "Hour of Day (0–23)", 0, 23,
            value=int(sv("hour", 14)),
            help="Hour when the transaction was attempted (24-hr)"
        )
        day_label = st.select_slider(
            "Day of Week",
            options=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
            value=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"][int(sv("day_of_week",1))],
        )

# ─────────────────────────────────────────────
#  STEP 4 – Predict
# ─────────────────────────────────────────────
st.markdown('<div class="step-pill">🔍 Step 3 · Get Root Cause</div>', unsafe_allow_html=True)
predict = st.button("🔍  Analyse Transaction Failure", use_container_width=True)

# ─────────────────────────────────────────────
#  RESULT
# ─────────────────────────────────────────────
if predict:
    txn_map = {"P2P (Person to Person)":"P2P","P2M (Person to Merchant)":"P2M"}
    day_map = {d:i for i,d in enumerate(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])}

    input_df = pd.DataFrame([{
        'amount':                   amount,
        'payer_bank':               payer_bank,
        'payee_bank':               payee_bank,
        'transaction_type':         txn_map[txn_type],
        'device_os':                device_os,
        'network_type':             network_type,
        'response_time_ms':         float(response_time),
        'retry_count':              int(retry_count),
        'hour':                     int(hour),
        'day_of_week':              day_map[day_label],
        'bank_server_status':       server_status,
        'npci_gateway_latency_ms':  float(latency),
    }])

    pred       = model.predict(input_df)[0]
    proba      = model.predict_proba(input_df)[0]
    confidence = round(max(proba)*100, 1)
    icon       = CAUSE_ICONS.get(pred,'⚠️')
    adv_type, adv_text = ADVICE.get(pred,('warn','Contact your bank for further support.'))
    adv_css = f"action-{adv_type if adv_type else 'ok'}"

    st.markdown("---")
    st.markdown("#### 📊 Diagnosis Result")

    # ── Main result card ──
    st.markdown(f"""
    <div class="result-box">
        <div class="result-icon">{icon}</div>
        <div class="result-cause">{pred.replace('_',' ')}</div>
        <div class="result-conf">Confidence: <strong>{confidence}%</strong></div>
        <div class="conf-track">
            <div class="conf-fill" style="width:{confidence}%"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Action advice ──
    st.markdown(f'<div class="{adv_css}"><strong>What to do:</strong> {adv_text}</div>',
                unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Probability breakdown ──
    with st.expander("📈 See probability breakdown across all failure types"):
        classes = model.classes_
        prob_df = pd.DataFrame({
            'Failure Type': [f"{CAUSE_ICONS[c]}  {c.replace('_',' ')}" for c in classes],
            'Confidence %': [round(p*100,1) for p in proba],
        }).sort_values('Confidence %', ascending=False).reset_index(drop=True)
        st.dataframe(prob_df, hide_index=True, use_container_width=True)

    # ── Input summary ──
    with st.expander("📋 View transaction inputs used for analysis"):
        labels = {
            'amount':'Amount (₹)','payer_bank':'Payer Bank','payee_bank':'Payee Bank',
            'transaction_type':'Transaction Type','device_os':'Device','network_type':'Network',
            'response_time_ms':'Response Time (ms)','retry_count':'Retry Count',
            'hour':'Hour','day_of_week':'Day of Week','bank_server_status':'Server Status',
            'npci_gateway_latency_ms':'NPCI Latency (ms)'
        }
        display = {labels[k]: v for k,v in input_df.iloc[0].items()}
        st.dataframe(pd.DataFrame(display,index=['Value']).T, use_container_width=True)

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center;color:#94a3b8;font-size:.8rem;padding-bottom:.5rem">
💳 UPI Transaction Failure Root-Cause Intelligence System &nbsp;|&nbsp;
GTU PGDDS Mini Project 2025-26 &nbsp;|&nbsp; Educational Use Only
</div>
""", unsafe_allow_html=True)
