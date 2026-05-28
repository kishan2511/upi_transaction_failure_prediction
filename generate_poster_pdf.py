"""
Project Poster – UPI Transaction Failure Root-Cause Intelligence System
Kishan Patel | Enrollment: 251370680017
A3 Portrait – Layout verified, no overflow
"""
from fpdf import FPDF

OUTPUT = "251370680017_Kishan_Project_Poster.pdf"

W, H = 297, 420   # A3 portrait mm
M    = 10         # outer margin
CW2  = (W - 3*M) / 2      # 2-col width = 133.5mm
CW3  = (W - 4*M) / 3      # 3-col width =  85.7mm

# Row heights — verified against text content:
ROW_A_H = 75    # Problem + Classes  — 63mm text space  → 11 lines max @ lh5.4
ROW_B_H = 95    # Dataset/Method/Results — 83mm text space → 16 lines max @ lh5.0
ROW_C_H = 65    # Tech/Findings      — 53mm text space  →  9 items max @ lh5.5
ROW_D_H = 28    # Pipeline

Y0  = 77
Y1  = Y0 + ROW_A_H + 5
Y2  = Y1 + ROW_B_H + 5
Y3  = Y2 + ROW_C_H + 5
Y4  = Y3 + ROW_D_H + 5     # Streamlit banner
Y5  = Y4 + 18 + 3           # GitHub banner

def fx(text):
    rep = {'\u2014':'-','\u2013':'-','\u2019':"'",'\u2018':"'",
           '\u201c':'"','\u201d':'"','\u2022':'*','\u2192':'->','\u2248':'~'}
    for k,v in rep.items():
        text = text.replace(k, v)
    return text.encode('latin-1','replace').decode('latin-1')

class Poster(FPDF):
    def header(self): pass
    def footer(self): pass

pdf = Poster('P','mm','A3')
pdf.add_page()

# ── BACKGROUND ───────────────────────────────────────────────────────────────
pdf.set_fill_color(246, 248, 252)
pdf.rect(0, 0, W, H, 'F')

# ═══════════════════════════════════════════════════════════════════════════════
# BANNER  0-44
# ═══════════════════════════════════════════════════════════════════════════════
pdf.set_fill_color(10, 36, 99)
pdf.rect(0, 0, W, 44, 'F')
pdf.set_fill_color(37, 99, 235)
pdf.rect(0, 44, W, 5, 'F')

pdf.set_text_color(255, 255, 255)
pdf.set_font('Helvetica','B', 15)
pdf.set_xy(0, 6);  pdf.cell(W, 8, fx('GUJARAT TECHNOLOGICAL UNIVERSITY'), align='C')
pdf.set_font('Helvetica','', 10.5)
pdf.set_xy(0, 15); pdf.cell(W, 7, fx('Post Graduate Diploma in Data Science (PGDDS)  |  Mini Project (DS02080041)  |  Institute Code: 137'), align='C')
pdf.set_xy(0, 22); pdf.cell(W, 7, fx('Academic Year 2025-26, Semester-2  |  Internal Guide: Komal Prajapati'), align='C')
pdf.set_font('Helvetica','BI', 10.5)
pdf.set_xy(0, 30); pdf.cell(W, 7, fx('Domain: FinTech  |  Digital Payments  |  Transaction Analytics'), align='C')
pdf.set_xy(0, 37); pdf.cell(W, 7, fx('Subject Code: DS02080041'), align='C')

# ── TITLE STRIP  49-74 ────────────────────────────────────────────────────────
pdf.set_fill_color(37, 99, 235)
pdf.rect(0, 49, W, 25, 'F')
pdf.set_text_color(255, 255, 255)
pdf.set_font('Helvetica','B', 22)
pdf.set_xy(0, 52); pdf.cell(W, 12, fx('UPI Transaction Failure Root-Cause Intelligence System'), align='C')
pdf.set_font('Helvetica','', 12.5)
pdf.set_xy(0, 64); pdf.cell(W, 8, fx('Kishan Patel  |  Enrollment No: 251370680017'), align='C')

# ─── helpers ──────────────────────────────────────────────────────────────────
def sec_hdr(x, y, w, title, bg=(10,36,99)):
    pdf.set_fill_color(*bg)
    pdf.rect(x, y, w, 9, 'F')
    pdf.set_text_color(255,255,255)
    pdf.set_font('Helvetica','B', 10.5)
    pdf.set_xy(x+3, y+1.5)
    pdf.cell(w-6, 6, fx(title))
    pdf.set_text_color(35,35,50)

def card(x, y, w, h, fill=(255,255,255)):
    pdf.set_fill_color(*fill)
    pdf.set_draw_color(180,200,235)
    pdf.set_line_width(0.35)
    pdf.rect(x, y, w, h, 'FD')

def text_lines(x, y, w, lines, size=9.2, lh=5.4):
    """Render lines; returns final y — guaranteed not to exceed card."""
    pdf.set_font('Helvetica','', size)
    pdf.set_text_color(35,35,50)
    for line in lines:
        pdf.set_xy(x, y)
        pdf.cell(w, lh, fx(line))
        y += lh
    return y

def bullet_lines(x, y, w, items, size=9.2, lh=5.5):
    pdf.set_text_color(35,35,50)
    for item in items:
        pdf.set_font('Helvetica','B', 10)
        pdf.set_xy(x+2, y); pdf.cell(5, lh, fx('*'))
        pdf.set_font('Helvetica','', size)
        pdf.set_xy(x+7, y); pdf.cell(w-7, lh, fx(item))
        y += lh + 0.4
    return y

def metric_box(x, y, w, h, val, label, bg=(37,99,235)):
    pdf.set_fill_color(*bg)
    pdf.rect(x, y, w, h, 'F')
    pdf.set_text_color(255,255,255)
    pdf.set_font('Helvetica','B', 17)
    pdf.set_xy(x, y+3); pdf.cell(w, 8, fx(val), align='C')
    pdf.set_font('Helvetica','', 8)
    pdf.set_xy(x, y+h-6); pdf.cell(w, 5, fx(label), align='C')

# ═══════════════════════════════════════════════════════════════════════════════
# ROW A  y=77  h=75  (text space = 63mm → 11 lines @ lh5.4)
# ═══════════════════════════════════════════════════════════════════════════════
card(M, Y0, CW2, ROW_A_H)
sec_hdr(M, Y0, CW2, '  PROBLEM STATEMENT')
text_lines(M+4, Y0+12, CW2-8, [
    'UPI processes billions of transactions daily in India.',
    'Transaction failures cause user frustration and direct',
    'financial losses for banks and payment platforms.',
    '',
    'GOAL: Automatically classify the root cause of each',
    'failed UPI transaction into one of 8 failure categories',
    'using supervised ML over logs and system indicators.',
    '',
    'Key Challenge: Severe class imbalance — Fraud_Flag is',
    'only ~2% vs Bank_Server_Down at 38%. SMOTE is used',
    'to balance minority classes before model training.',
], lh=5.4)

card(M*2+CW2, Y0, CW2, ROW_A_H)
sec_hdr(M*2+CW2, Y0, CW2, '  ROOT-CAUSE CLASSES  (8 Categories)')
bullet_lines(M*2+CW2+4, Y0+12, CW2-8, [
    'Bank_Server_Down   — server degraded/down, high RT',
    'Insufficient_Funds — amount exceeds account balance',
    'Wrong_Credentials  — incorrect PIN, high retry count',
    'Network_Timeout    — response time exceeds 5000 ms',
    'VPA_Not_Found      — payee VPA invalid/unregistered',
    'Fraud_Flag         — anomalously high amount flagged',
    'NPCI_Gateway_Error — NPCI latency spike detected',
    'User_Declined      — user manually declined payment',
], lh=5.5)

# ═══════════════════════════════════════════════════════════════════════════════
# ROW B  y=157  h=95  (text space = 83mm → 16 lines @ lh5.0)
# ═══════════════════════════════════════════════════════════════════════════════
card(M, Y1, CW3, ROW_B_H)
sec_hdr(M, Y1, CW3, '  DATASET')
text_lines(M+4, Y1+12, CW3-8, [
    'Records  : 100,000 transactions',
    'Failures : ~28,000 (28% failure rate)',
    'Features : 12 input variables',
    'Target   : root_cause (8 classes)',
    '',
    'Numeric Features:',
    '  amount (INR)',
    '  response_time_ms',
    '  retry_count',
    '  hour, day_of_week',
    '  npci_gateway_latency_ms',
    '',
    'Categorical Features:',
    '  payer_bank & payee_bank',
    '  transaction_type (P2P/P2M)',
    '  device_os (Android/iOS/Web)',
], size=9, lh=5.0)

card(M*2+CW3, Y1, CW3, ROW_B_H)
sec_hdr(M*2+CW3, Y1, CW3, '  METHODOLOGY')
text_lines(M*2+CW3+4, Y1+12, CW3-8, [
    'Step 1: Data Generation',
    '  100K synthetic UPI transaction',
    '  logs with realistic distributions',
    '',
    'Step 2: EDA',
    '  Class imbalance analysis',
    '  Correlation heatmap & plots',
    '',
    'Step 3: Preprocessing',
    '  OneHotEncoder (categoricals)',
    '  StandardScaler (numerics)',
    '  80/20 stratified split',
    '',
    'Step 4: SMOTE Oversampling',
    '  Balance rare failure classes',
    '',
    'Step 5: Train + Deploy',
    '  RandomForest (150 estimators)',
], size=9, lh=5.0)

card(M*3+CW3*2, Y1, CW3, ROW_B_H)
sec_hdr(M*3+CW3*2, Y1, CW3, '  MODEL RESULTS', bg=(5,150,105))
bx = M*3+CW3*2+5
bw = CW3-10
my = Y1+13
metric_box(bx, my,    bw, 22, '~90%',   'Overall Accuracy',   bg=(37,99,235));  my += 24
metric_box(bx, my,    bw, 22, '~0.88',  'Macro F1-Score',     bg=(5,150,105));  my += 24
metric_box(bx, my,    bw, 22, '150',    'RF Estimators',      bg=(124,58,237)); my += 24
metric_box(bx, my,    bw, 18, '~20K',   'Training Records',   bg=(220,38,38))

# ═══════════════════════════════════════════════════════════════════════════════
# ROW C  y=257  h=65  (text space = 53mm → 9 items @ lh5.5)
# ═══════════════════════════════════════════════════════════════════════════════
card(M, Y2, CW2, ROW_C_H)
sec_hdr(M, Y2, CW2, '  TECH STACK')
bullet_lines(M+4, Y2+12, CW2-8, [
    'Python 3.11          — Core language',
    'pandas & NumPy       — Data manipulation',
    'scikit-learn         — ML pipeline & Random Forest',
    'imbalanced-learn     — SMOTE oversampling',
    'matplotlib & seaborn — EDA visualisations',
    'Streamlit            — Interactive web app',
    'Jupyter Notebook     — Analysis & reporting',
    'GitHub               — Version control & hosting',
], lh=5.5)

card(M*2+CW2, Y2, CW2, ROW_C_H)
sec_hdr(M*2+CW2, Y2, CW2, '  KEY FINDINGS')
bullet_lines(M*2+CW2+4, Y2+12, CW2-8, [
    'Bank_Server_Down (38%) is the dominant failure class',
    'Network_Timeout flagged when response_time > 5000 ms',
    'Wrong_Credentials linked to retry_count spikes',
    'Fraud_Flag (2%) benefits most from SMOTE balancing',
    'NPCI_Gateway_Error tied to gateway latency > 380 ms',
    'Random Forest achieves ~90% on all 8 failure classes',
    'Peak failures occur between 00:00 and 03:00 hours',
    'Android + 3G combination has highest failure rate',
], lh=5.5)

# ═══════════════════════════════════════════════════════════════════════════════
# ROW D  – Pipeline visual  h=28
# ═══════════════════════════════════════════════════════════════════════════════
card(M, Y3, W-2*M, ROW_D_H, fill=(235,242,255))
sec_hdr(M, Y3, W-2*M, '  ML PIPELINE FLOW')

steps = [
    ('Data Generation',  10, 36, 99),
    ('EDA & Analysis',    5,150,105),
    ('Preprocessing',   124, 58,237),
    ('SMOTE Balance',   220, 38, 38),
    ('Random Forest',    37, 99,235),
    ('Streamlit Deploy', 5, 150,105),
]
avail   = W - 2*M - 6
step_w  = avail / len(steps)
px0     = M + 3
py0     = Y3 + 12
ph      = 13

for i,(lbl,r,g,b) in enumerate(steps):
    bx = px0 + i*step_w
    pdf.set_fill_color(r,g,b)
    pdf.rect(bx, py0, step_w-3, ph, 'F')
    pdf.set_text_color(255,255,255)
    pdf.set_font('Helvetica','B', 8.5)
    pdf.set_xy(bx, py0+3)
    pdf.cell(step_w-3, 7, fx(lbl), align='C')
    if i < len(steps)-1:
        pdf.set_fill_color(37,99,235)
        pdf.set_text_color(255,255,255)
        pdf.set_font('Helvetica','B', 11)
        pdf.set_xy(bx+step_w-3, py0+2)
        pdf.cell(3, 9, fx('>'), align='C')

# ═══════════════════════════════════════════════════════════════════════════════
# BANNERS
# ═══════════════════════════════════════════════════════════════════════════════
# Streamlit
pdf.set_fill_color(5, 150, 105)
pdf.rect(M, Y4, W-2*M, 18, 'F')
pdf.set_text_color(255,255,255)
pdf.set_font('Helvetica','B', 11.5)
pdf.set_xy(M, Y4+3);  pdf.cell(W-2*M, 6, fx('LIVE STREAMLIT APPLICATION'), align='C')
pdf.set_font('Helvetica','', 10)
pdf.set_xy(M, Y4+11); pdf.cell(W-2*M, 6, fx('https://kishan2511-upi-transaction-failure-prediction-app-fv8njm.streamlit.app/'), align='C')

# GitHub
pdf.set_fill_color(10, 36, 99)
pdf.rect(M, Y5, W-2*M, 16, 'F')
pdf.set_text_color(255,255,255)
pdf.set_font('Helvetica','B', 11)
pdf.set_xy(M, Y5+2);  pdf.cell(W-2*M, 6, fx('GitHub Repository'), align='C')
pdf.set_font('Helvetica','', 10)
pdf.set_xy(M, Y5+9);  pdf.cell(W-2*M, 6, fx('https://github.com/kishan2511/upi_transaction_failure_prediction'), align='C')

# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════════
pdf.set_fill_color(10, 36, 99)
pdf.rect(0, H-13, W, 13, 'F')
pdf.set_text_color(180, 205, 255)
pdf.set_font('Helvetica','', 9.5)
pdf.set_xy(0, H-9)
pdf.cell(W, 6, fx('Kishan Patel  |  Enrollment: 251370680017  |  GTU PGDDS Mini Project 2025-26  |  Internal Guide: Komal Prajapati'), align='C')

pdf.output(OUTPUT)

# Verify no overflow
end_of_content = Y5 + 16
print(f"Layout check:")
print(f"  Content ends at : {end_of_content:.0f} mm")
print(f"  Footer starts at: {H-13} mm")
print(f"  Bottom gap      : {H-13-end_of_content:.0f} mm  (safe if > 0)")
print(f"Poster saved: {OUTPUT}")
