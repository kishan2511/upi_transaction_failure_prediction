import streamlit as st
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline

st.set_page_config(
    page_title="UPI Failure Intelligence",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    /* Page background */
    .stApp { background-color: #f0f4ff; }

    /* Main header */
    .main-header {
        background: linear-gradient(135deg, #0a2463 0%, #1e40af 60%, #3b82f6 100%);
        color: white; padding: 1.8rem 2rem 1.4rem;
        border-radius: 14px; text-align: center; margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(10,36,99,0.25);
    }
    .main-header h1 { font-size: 2rem; font-weight: 800; margin: 0; letter-spacing: 0.5px; }
    .main-header p  { font-size: 0.95rem; opacity: 0.85; margin: 0.4rem 0 0; }

    /* Metric cards */
    .metric-row { display: flex; gap: 12px; margin-bottom: 1.2rem; }
    .metric-card {
        flex: 1; background: white; border-radius: 10px;
        padding: 1rem 1.2rem; text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-top: 4px solid #1e40af;
    }
    .metric-card .val { font-size: 1.6rem; font-weight: 800; color: #1e40af; }
    .metric-card .lbl { font-size: 0.8rem; color: #64748b; margin-top: 2px; }

    /* Section cards */
    .section-card {
        background: white; border-radius: 12px; padding: 1.2rem 1.4rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.07); margin-bottom: 1rem;
    }
    .section-title {
        font-size: 0.85rem; font-weight: 700; text-transform: uppercase;
        letter-spacing: 1px; color: #1e40af; margin-bottom: 1rem;
        padding-bottom: 6px; border-bottom: 2px solid #e0e7ff;
    }

    /* Result */
    .result-success {
        background: linear-gradient(135deg, #0a2463, #1e40af);
        color: white; border-radius: 14px; padding: 1.8rem 2rem;
        text-align: center; box-shadow: 0 6px 24px rgba(30,64,175,0.3);
    }
    .result-cause { font-size: 2rem; font-weight: 800; letter-spacing: 1px; margin: 0.3rem 0; }
    .result-conf  { font-size: 1rem; opacity: 0.85; }
    .result-label { font-size: 0.85rem; opacity: 0.7; text-transform: uppercase; letter-spacing: 1px; }

    /* Confidence bar */
    .conf-bar-bg { background: #e0e7ff; border-radius: 99px; height: 8px; margin: 8px 0; }
    .conf-bar-fg { background: #3b82f6; border-radius: 99px; height: 8px; }

    /* Action advice */
    .advice-box {
        background: #f0fdf4; border-left: 4px solid #16a34a;
        border-radius: 0 8px 8px 0; padding: 1rem 1.2rem; margin-top: 1rem;
    }
    .advice-box.warn {
        background: #fff7ed; border-left-color: #f97316;
    }
    .advice-box.danger {
        background: #fef2f2; border-left-color: #dc2626;
    }

    /* Predict button */
    div.stButton > button {
        background: linear-gradient(135deg, #1e40af, #3b82f6);
        color: white; font-weight: 700; font-size: 1.05rem;
        border-radius: 10px; padding: 0.7rem 2rem;
        border: none; width: 100%;
        box-shadow: 0 4px 14px rgba(30,64,175,0.35);
        transition: all 0.2s;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #1e3a8a, #2563eb);
        box-shadow: 0 6px 18px rgba(30,64,175,0.45);
    }

    /* Input label style */
    label { font-weight: 600 !important; color: #334155 !important; }

    /* Status badge */
    .badge {
        display:inline-block; padding:3px 10px; border-radius:99px;
        font-size:0.78rem; font-weight:700; letter-spacing:0.5px;
    }
    .badge-down   { background:#fef2f2; color:#dc2626; }
    .badge-deg    { background:#fff7ed; color:#ea580c; }
    .badge-up     { background:#f0fdf4; color:#16a34a; }
</style>
""", unsafe_allow_html=True)

ROOT_CAUSES = [
    'Bank_Server_Down','Insufficient_Funds','Wrong_Credentials','Network_Timeout',
    'VPA_Not_Found','Fraud_Flag','NPCI_Gateway_Error','User_Declined'
]
BANKS    = ['SBI','HDFC','ICICI','AXIS','PNB','BOB','Canara','Kotak','Yes Bank','IDFC First']
OS_LIST  = ['Android','iOS','Web']
NET_LIST = ['4G','WiFi','3G','5G']
TXN_TYPES= ['P2P (Person to Person)','P2M (Person to Merchant)']
SVR_LIST = ['Healthy','Degraded','Down']

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
    'Bank_Server_Down':   ('warn',  'Bank server is currently down or degraded. Wait 10–15 minutes and retry. Contact your bank if it persists.'),
    'Insufficient_Funds': ('warn',  'Account balance is insufficient for this transaction. Add funds and retry.'),
    'Wrong_Credentials':  ('danger','Incorrect UPI PIN entered multiple times. Verify your PIN. Account may be locked after repeated failures.'),
    'Network_Timeout':    ('warn',  'Transaction timed out due to poor network. Switch to WiFi or a stronger signal and retry.'),
    'VPA_Not_Found':      ('warn',  'Payee VPA address is invalid or not registered. Double-check the UPI ID before retrying.'),
    'Fraud_Flag':         ('danger','Transaction flagged as potentially fraudulent due to unusual amount. Contact your bank immediately if this is legitimate.'),
    'NPCI_Gateway_Error': ('warn',  'NPCI payment gateway is experiencing high latency. This is a system-side issue — retry in a few minutes.'),
    'User_Declined':      ('',      'The transaction was declined by the user. Confirm with the payee and request them to accept.'),
}


@st.cache_resource(show_spinner="Training model on UPI transaction data...")
def train_model():
    np.random.seed(42)
    n = 30000
    FAIL_P = np.array([0.38,0.10,0.08,0.27,0.07,0.02,0.05,0.03])
    is_success = (np.random.rand(n) < 0.72)
    root = np.array(['Success']*n, dtype=object)
    fail_idx = np.where(~is_success)[0]
    root[fail_idx] = np.random.choice(ROOT_CAUSES, size=len(fail_idx), p=FAIL_P)

    svr_raw  = np.random.choice(['Healthy','Degraded','Down'], n, p=[0.88,0.09,0.03])
    net_raw  = np.random.choice(['4G','WiFi','3G','5G'], n, p=[0.50,0.32,0.10,0.08])
    txn_raw  = np.random.choice(['P2P','P2M'], n, p=[0.62,0.38])

    data = pd.DataFrame({
        'amount':                   np.clip(np.random.lognormal(4.2,1.1,n),1,500000).round(2),
        'payer_bank':               np.random.choice(BANKS, n),
        'payee_bank':               np.random.choice(BANKS, n),
        'transaction_type':         txn_raw,
        'device_os':                np.random.choice(['Android','iOS','Web'], n, p=[0.72,0.25,0.03]),
        'network_type':             net_raw,
        'response_time_ms':         np.random.gamma(2.0,450,n),
        'retry_count':              np.random.poisson(0.35,n),
        'hour':                     np.random.randint(0,24,n),
        'day_of_week':              np.random.randint(0,7,n),
        'bank_server_status':       svr_raw,
        'npci_gateway_latency_ms':  np.random.gamma(1.5,32,n),
        'root_cause':               root,
    })
    for cls in ROOT_CAUSES:
        m = data['root_cause'] == cls
        if cls == 'Network_Timeout':
            data.loc[m,'response_time_ms'] += np.random.uniform(2200,5500,m.sum())
            data.loc[m,'network_type'] = np.random.choice(['3G','4G'],m.sum(),p=[0.6,0.4])
        elif cls == 'Bank_Server_Down':
            data.loc[m,'bank_server_status'] = np.random.choice(['Degraded','Down'],m.sum(),p=[0.35,0.65])
            data.loc[m,'response_time_ms'] += np.random.uniform(700,3000,m.sum())
        elif cls == 'Wrong_Credentials':
            data.loc[m,'retry_count'] += np.random.randint(2,6,m.sum())
        elif cls == 'Fraud_Flag':
            data.loc[m,'amount'] *= np.random.uniform(2.0,4.0,m.sum())
        elif cls == 'NPCI_Gateway_Error':
            data.loc[m,'npci_gateway_latency_ms'] += np.random.uniform(150,400,m.sum())
            data.loc[m,'response_time_ms'] += np.random.uniform(500,2000,m.sum())

    df_fail = data[data['root_cause'] != 'Success'].copy()
    X = df_fail.drop('root_cause',axis=1)
    y = df_fail['root_cause']
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=42,stratify=y)

    cat_cols = ['payer_bank','payee_bank','transaction_type','device_os','network_type','bank_server_status']
    ct = ColumnTransformer([('ohe',OneHotEncoder(handle_unknown='ignore'),cat_cols)],remainder='passthrough')
    model = Pipeline([('pre',ct),('clf',RandomForestClassifier(n_estimators=150,random_state=42,n_jobs=-1))])
    model.fit(X_train,y_train)
    acc = model.score(X_test,y_test)
    classes = model.classes_
    return model, acc, classes


model, accuracy, classes = train_model()

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>💳 UPI Transaction Failure Root-Cause Intelligence</h1>
    <p>GTU PGDDS Mini Project &nbsp;|&nbsp; Kishan Patel (251370680017) &nbsp;|&nbsp; Guide: Komal Prajapati</p>
</div>
""", unsafe_allow_html=True)

# ── METRICS ROW ───────────────────────────────────────────────────────────────
c1,c2,c3,c4,c5 = st.columns(5)
with c1: st.metric("🤖 Model","Random Forest")
with c2: st.metric("🎯 Accuracy",f"{accuracy*100:.1f}%")
with c3: st.metric("🔴 Failure Classes","8")
with c4: st.metric("📊 Train Records","~24,000")
with c5: st.metric("📁 Total Transactions","30,000")

st.markdown("---")

# ── INPUT FORM ────────────────────────────────────────────────────────────────
st.subheader("🔍 Analyse a Failed Transaction")
st.caption("Enter the transaction details below to identify the root cause of failure.")

left, right = st.columns([1.1, 0.9], gap="large")

with left:
    st.markdown('<div class="section-title">Transaction Details</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        amount = st.number_input("Amount (INR ₹)", min_value=1.0, max_value=500000.0,
                                  value=8500.0, step=500.0, format="%.2f")
        payer_bank = st.selectbox("Payer Bank", BANKS, index=1)
        txn_type_display = st.selectbox("Transaction Type", TXN_TYPES)
        device_os = st.selectbox("Device OS", OS_LIST)
    with col_b:
        response_time = st.number_input("Response Time (ms)", min_value=50, max_value=10000,
                                         value=450, step=50)
        payee_bank = st.selectbox("Payee Bank", BANKS, index=0)
        network_type_display = st.selectbox("Network Type", NET_LIST)
        server_status_display = st.selectbox("Bank Server Status", SVR_LIST)

    col_c, col_d, col_e = st.columns(3)
    with col_c:
        retry_count = st.number_input("Retry Count", min_value=0, max_value=10, value=0)
    with col_d:
        latency = st.number_input("NPCI Latency (ms)", min_value=5, max_value=700, value=48)
    with col_e:
        hour = st.slider("Hour of Day", 0, 23, 14)

    day_display = st.select_slider("Day of Week",
        options=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])

with right:
    st.markdown('<div class="section-title">Root-Cause Class Reference</div>', unsafe_allow_html=True)
    cause_data = {
        "Root Cause": [f"{CAUSE_ICONS[c]}  {c.replace('_',' ')}" for c in ROOT_CAUSES],
        "Frequency": ["38%","10%","8%","27%","7%","2%","5%","3%"],
    }
    st.dataframe(pd.DataFrame(cause_data), hide_index=True, use_container_width=True, height=300)

    st.markdown('<div class="section-title" style="margin-top:1rem">Transaction Context</div>', unsafe_allow_html=True)
    ctx1, ctx2 = st.columns(2)
    with ctx1:
        svr_badge = {"Healthy":"badge-up","Degraded":"badge-deg","Down":"badge-down"}[server_status_display]
        st.markdown(f'**Server Status:** <span class="badge {svr_badge}">{server_status_display}</span>', unsafe_allow_html=True)
        st.markdown(f"**Amount:** ₹{amount:,.2f}")
        st.markdown(f"**Retry Count:** {retry_count}")
    with ctx2:
        rt_color = "🔴" if response_time > 3000 else "🟡" if response_time > 1000 else "🟢"
        st.markdown(f"**Response Time:** {rt_color} {response_time} ms")
        st.markdown(f"**NPCI Latency:** {latency} ms")
        st.markdown(f"**Hour:** {hour:02d}:00")

st.markdown("")

# ── PREDICT ───────────────────────────────────────────────────────────────────
predict_col, _ = st.columns([1, 2])
with predict_col:
    predict_btn = st.button("🔍  Estimate Prediction", use_container_width=True)

if predict_btn:
    day_map = {"Monday":0,"Tuesday":1,"Wednesday":2,"Thursday":3,"Friday":4,"Saturday":5,"Sunday":6}
    txn_map = {"P2P (Person to Person)":"P2P","P2M (Person to Merchant)":"P2M"}
    net_map  = {"4G":"4G","WiFi":"WiFi","3G":"3G","5G":"4G"}

    input_df = pd.DataFrame([{
        'amount':                   amount,
        'payer_bank':               payer_bank,
        'payee_bank':               payee_bank,
        'transaction_type':         txn_map[txn_type_display],
        'device_os':                device_os,
        'network_type':             net_map[network_type_display],
        'response_time_ms':         float(response_time),
        'retry_count':              int(retry_count),
        'hour':                     int(hour),
        'day_of_week':              day_map[day_display],
        'bank_server_status':       server_status_display,
        'npci_gateway_latency_ms':  float(latency),
    }])

    prediction = model.predict(input_df)[0]
    proba      = model.predict_proba(input_df)[0]
    confidence = round(max(proba)*100, 1)
    icon       = CAUSE_ICONS.get(prediction,'⚠️')

    st.markdown("---")
    res_col, detail_col = st.columns([1, 1.2], gap="large")

    with res_col:
        st.markdown(f"""
        <div class="result-success">
            <div class="result-label">Root Cause Identified</div>
            <div class="result-cause">{icon} {prediction.replace('_',' ')}</div>
            <div class="result-conf">Confidence: {confidence}%</div>
            <div class="conf-bar-bg">
                <div class="conf-bar-fg" style="width:{confidence}%"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        adv_type, adv_text = ADVICE.get(prediction,('','Contact your bank.'))
        css_class = f"advice-box {adv_type}".strip()
        st.markdown(f"""
        <div class="{css_class}" style="margin-top:1rem">
            <strong>Recommended Action</strong><br>{adv_text}
        </div>
        """, unsafe_allow_html=True)

    with detail_col:
        st.markdown("**Probability across all classes:**")
        prob_df = pd.DataFrame({
            'Root Cause': [f"{CAUSE_ICONS[c]} {c.replace('_',' ')}" for c in classes],
            'Probability': [f"{p*100:.1f}%" for p in proba],
            'Confidence': proba
        }).sort_values('Confidence', ascending=False)

        st.dataframe(
            prob_df[['Root Cause','Probability']],
            hide_index=True,
            use_container_width=True,
            height=310
        )

    with st.expander("📋 Full Input Summary"):
        display_df = input_df.copy()
        display_df.columns = [c.replace('_',' ').title() for c in display_df.columns]
        st.dataframe(display_df.T.rename(columns={0:'Value'}), use_container_width=True)

st.markdown("---")
st.caption("⚠️ Educational tool only. Not for production financial use. | GTU PGDDS Mini Project 2025-26")
