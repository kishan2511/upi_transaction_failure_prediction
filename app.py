import streamlit as st
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline

st.set_page_config(
    page_title="UPI Failure Root-Cause Intelligence",
    page_icon="💳",
    layout="wide"
)

st.markdown("""
<style>
    .main-header { font-size:2.4rem; font-weight:700; color:#1e40af; text-align:center; padding:1rem 0 0.3rem; }
    .sub-header  { font-size:1rem; color:#64748b; text-align:center; margin-bottom:1.5rem; }
    .result-box  { background:linear-gradient(135deg,#1e40af 0%,#3b82f6 100%); color:white;
                   padding:1.5rem 2rem; border-radius:12px; text-align:center; margin:1rem 0; }
    .result-cause{ font-size:2rem; font-weight:800; letter-spacing:1px; }
    div.stButton > button { background-color:#16a34a; color:white; font-weight:600;
                            font-size:1.1rem; border-radius:8px; padding:0.6rem 2rem;
                            border:none; width:100%; }
    div.stButton > button:hover { background-color:#15803d; }
</style>
""", unsafe_allow_html=True)

ROOT_CAUSES = [
    'Bank_Server_Down', 'Insufficient_Funds', 'Wrong_Credentials', 'Network_Timeout',
    'VPA_Not_Found', 'Fraud_Flag', 'NPCI_Gateway_Error', 'User_Declined'
]
BANKS   = ['SBI','HDFC','ICICI','AXIS','PNB','BOB','Canara','Kotak','Yes','IDFC']
OS_LIST = ['Android','iOS','Web']
NET_LIST= ['4G','WiFi','3G']
TXN_TYPES = ['P2P','P2M']
SVR_STATUS = ['healthy','degraded','down']


@st.cache_resource
def train_model():
    np.random.seed(42)
    n = 25000
    FAIL_P = np.array([0.38,0.10,0.08,0.27,0.07,0.02,0.05,0.03])
    is_success = (np.random.rand(n) < 0.72)
    root = np.array(['Success']*n, dtype=object)
    fail_idx = np.where(~is_success)[0]
    root[fail_idx] = np.random.choice(ROOT_CAUSES, size=len(fail_idx), p=FAIL_P)

    data = pd.DataFrame({
        'amount': np.clip(np.random.lognormal(4.2,1.1,n),1,500000).round(2),
        'payer_bank': np.random.choice(BANKS, n),
        'payee_bank': np.random.choice(BANKS, n),
        'transaction_type': np.random.choice(TXN_TYPES, n, p=[0.62,0.38]),
        'device_os': np.random.choice(OS_LIST, n, p=[0.72,0.25,0.03]),
        'network_type': np.random.choice(NET_LIST, n, p=[0.55,0.35,0.10]),
        'response_time_ms': np.random.gamma(2.0,450,n),
        'retry_count': np.random.poisson(0.35,n),
        'hour': np.random.randint(0,24,n),
        'day_of_week': np.random.randint(0,7,n),
        'bank_server_status': np.random.choice(SVR_STATUS, n, p=[0.88,0.09,0.03]),
        'npci_gateway_latency_ms': np.random.gamma(1.5,32,n),
        'root_cause': root
    })
    # inject signals
    for cls in ROOT_CAUSES:
        m = data['root_cause'] == cls
        if cls == 'Network_Timeout':
            data.loc[m,'response_time_ms'] += np.random.uniform(2200,5500,m.sum())
        elif cls == 'Bank_Server_Down':
            data.loc[m,'bank_server_status'] = 'down'
        elif cls == 'Wrong_Credentials':
            data.loc[m,'retry_count'] += np.random.randint(1,5,m.sum())
        elif cls == 'Fraud_Flag':
            data.loc[m,'amount'] *= np.random.uniform(2.0,4.0,m.sum())
        elif cls == 'NPCI_Gateway_Error':
            data.loc[m,'npci_gateway_latency_ms'] += np.random.uniform(120,380,m.sum())

    df_fail = data[data['root_cause'] != 'Success'].copy()
    X = df_fail.drop('root_cause', axis=1)
    y = df_fail['root_cause']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    cat_cols = ['payer_bank','payee_bank','transaction_type','device_os','network_type','bank_server_status']
    num_cols = ['amount','response_time_ms','retry_count','hour','day_of_week','npci_gateway_latency_ms']

    ct = ColumnTransformer([('ohe', OneHotEncoder(handle_unknown='ignore'), cat_cols)],
                           remainder='passthrough')
    model = Pipeline([('pre', ct),
                      ('clf', RandomForestClassifier(n_estimators=150, random_state=42))])
    model.fit(X_train, y_train)
    acc = model.score(X_test, y_test)
    return model, acc, cat_cols, num_cols


model, accuracy, cat_cols, num_cols = train_model()

st.markdown('<div class="main-header">💳 UPI Failure Root-Cause Intelligence System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">GTU PGDDS Mini Project — Kishan Patel (251370680017) | Guide: Komal Prajapati</div>', unsafe_allow_html=True)

c1,c2,c3,c4 = st.columns(4)
c1.metric("Model","Random Forest")
c2.metric("Accuracy",f"{accuracy*100:.1f}%")
c3.metric("Failure Classes","8")
c4.metric("Training Records","~20,000")

st.markdown("---")
st.subheader("Enter Transaction Details")

col1, col2 = st.columns(2)
with col1:
    amount         = st.number_input("Transaction Amount (INR)", min_value=1.0, max_value=500000.0, value=5000.0, step=100.0)
    response_time  = st.slider("Response Time (ms)", 100, 8000, 500)
    latency        = st.slider("NPCI Gateway Latency (ms)", 10, 600, 50)
    retry_count    = st.slider("Retry Count", 0, 10, 0)
    hour           = st.slider("Transaction Hour (0-23)", 0, 23, 12)
    day_of_week    = st.selectbox("Day of Week", ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"])

with col2:
    payer_bank     = st.selectbox("Payer Bank", BANKS)
    payee_bank     = st.selectbox("Payee Bank", BANKS)
    txn_type       = st.selectbox("Transaction Type", TXN_TYPES)
    device_os      = st.selectbox("Device OS", OS_LIST)
    network_type   = st.selectbox("Network Type", NET_LIST)
    server_status  = st.selectbox("Bank Server Status", SVR_STATUS)

day_map = {"Mon":0,"Tue":1,"Wed":2,"Thu":3,"Fri":4,"Sat":5,"Sun":6}

if st.button("Estimate Prediction"):
    input_df = pd.DataFrame([{
        'amount': amount,
        'payer_bank': payer_bank,
        'payee_bank': payee_bank,
        'transaction_type': txn_type,
        'device_os': device_os,
        'network_type': network_type,
        'response_time_ms': response_time,
        'retry_count': retry_count,
        'hour': hour,
        'day_of_week': day_map[day_of_week],
        'bank_server_status': server_status,
        'npci_gateway_latency_ms': latency,
    }])

    prediction  = model.predict(input_df)[0]
    proba       = model.predict_proba(input_df)[0]
    confidence  = round(max(proba)*100, 1)

    st.markdown(f"""
    <div class="result-box">
        <div style="font-size:1rem;opacity:.85;margin-bottom:.3rem;">Predicted Root Cause</div>
        <div class="result-cause">{prediction.replace('_',' ')}</div>
        <div style="margin-top:.5rem;font-size:1rem;">Confidence: {confidence}%</div>
    </div>
    """, unsafe_allow_html=True)

    advice = {
        'Bank_Server_Down':    'Contact your bank or retry after some time. Bank servers may be undergoing maintenance.',
        'Insufficient_Funds':  'Check your account balance before retrying the transaction.',
        'Wrong_Credentials':   'Verify your UPI PIN and VPA. Too many wrong attempts may block your account.',
        'Network_Timeout':     'Check your internet connection. Switch to WiFi or a stronger network and retry.',
        'VPA_Not_Found':       'Verify the payee VPA address is correct and registered.',
        'Fraud_Flag':          'Transaction flagged as suspicious. Contact your bank if this is a legitimate transaction.',
        'NPCI_Gateway_Error':  'NPCI gateway issue detected. Retry after a few minutes.',
        'User_Declined':       'Transaction was declined by the user. Confirm with the payee and retry.',
    }
    st.info(f"**Action:** {advice.get(prediction,'Contact your bank for assistance.')}")

    with st.expander("Input Summary"):
        st.write(input_df)

st.markdown("---")
st.caption("Educational tool only. Not for production financial use.")
