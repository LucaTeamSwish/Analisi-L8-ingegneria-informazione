import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="L-8 Ingegneria dell'Informazione",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS stile L-2, sfondo verde scuro profondo ────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
:root {
    --bg-primary: #041A1A; --bg-secondary: #0A2828; --bg-card: #0F3333; --bg-card-hover: #0D3030;
    --border: rgba(255,255,255,0.08); --border-accent:  rgba(20,184,166,0.4);
    --text-primary: #F5F5F7;
    --text-secondary: #C8C8C8;
    --accent-green: #14B8A6;
    --font-display: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}
[data-testid="collapsedControl"] { display: block !important; visibility: visible !important; }
[data-testid="stSidebar"] { display: block !important; visibility: visible !important; }
html, body, [data-testid="stAppViewContainer"] { background-color: var(--bg-primary) !important; color: var(--text-primary) !important; font-family: var(--font-display) !important; }
[data-testid="stSidebar"] { background-color: var(--bg-secondary) !important; border-right: 1px solid var(--border) !important; }
[data-testid="stSidebar"] > div { background-color: var(--bg-secondary) !important; }
[data-testid="stHeader"] { background-color: var(--bg-primary) !important; border-bottom: 1px solid var(--border) !important; }
[data-testid="block-container"] { padding: 2rem 3rem !important; max-width: 1400px !important; }
h1 { font-size: 2.8rem !important; font-weight: 700 !important; letter-spacing: -0.04em !important; color: var(--text-primary) !important; line-height: 1.1 !important; }
h2 { font-size: 1.6rem !important; font-weight: 600 !important; letter-spacing: -0.02em !important; color: var(--text-primary) !important; }
h3 { font-size: 1.1rem !important; font-weight: 500 !important; color: var(--text-secondary) !important; text-transform: uppercase !important; letter-spacing: 0.08em !important; }
p { color: var(--text-secondary) !important; font-size: 0.95rem !important; line-height: 1.7 !important; font-weight: 300 !important; }
.section-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 16px; padding: 2rem; margin-bottom: 1.5rem; }
hr { border-color: var(--border) !important; margin: 2rem 0 !important; }
.sidebar-title { font-size: 0.65rem; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; color: var(--text-secondary); padding: 1rem 1rem 0.5rem; }
[data-testid="stSidebar"] .stRadio > label { color: var(--text-secondary) !important; font-size: 0.9rem !important; }
[data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] p { color: var(--text-secondary) !important; font-size: 0.9rem !important; }
.stButton > button { background: var(--accent-green) !important; color: white !important; border: none !important; border-radius: 8px !important; font-weight: 500 !important; padding: 0.5rem 1.5rem !important; }
[data-testid="metric-container"] { background: var(--bg-card) !important; border: 1px solid var(--border) !important; border-radius: 12px !important; padding: 1rem !important; }
[data-testid="stMetricValue"] { color: var(--accent-green) !important; font-size: 1.8rem !important; font-weight: 600 !important; }
[data-testid="stMetricLabel"] { color: var(--text-secondary) !important; }
.chart-instructions { background: rgba(20,184,166,0.06); border: 1px solid rgba(20,184,166,0.15)); border-radius: 10px; padding: 0.75rem 1rem; margin-bottom: 1rem; font-size: 0.82rem; color: #14B8A6; }
.chart-description { color: var(--text-secondary); font-size: 0.9rem; line-height: 1.65; margin-bottom: 1rem; font-weight: 300; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }
[data-testid="stForm"] button { background: #14B8A6 !important; color: white !important; font-weight: 700 !important; border-radius: 10px !important; }
[data-testid="stForm"] button:hover { background: #0D9488 !important; transform: translateY(-1px) !important; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
[data-testid="stToolbarActions"] { display: none !important; }
.kpi-card { background: var(--bg-card); border: 1px solid var(--accent-green); border-radius: 10px; padding: 1rem 1.2rem; text-align: center; }
.kpi-label { font-size: 0.72rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 1px; }
.kpi-value { font-size: 2rem; font-weight: 700; color: var(--accent-green); line-height: 1.1; }
.kpi-sub { font-size: 0.75rem; color: #9CA3AF; margin-top: 0.2rem; }
</style>
""", unsafe_allow_html=True)

# ── COSTANTI ──────────────────────────────────────────────────────────────────
BG_PLOT   = '#0A2828'
BG_PAPER  = '#0A2828'
BG_CARD   = '#0F3333'
VERDE_MAIN  = '#14B8A6'
VERDE_LIGHT = '#99F6E4'
# Colori macro aree identici a L-2: Nord=blu, Centro=verde teal, Sud=arancio, Isole=viola
COLORI_MACRO = {'Nord': '#3B82F6', 'Centro': '#10B981', 'Sud': '#F59E0B', 'Isole': '#8B5CF6'}

TELEMATICHE_LIST = [
    'Telematica Universitas Mercatorum', 'Telematica Uninettuno',
    'Telematica Guglielmo Marconi', 'Telematica Niccolò Cusano',
    'Telematica Giustino Fortunato', 'Telematica e-Campus', 'Link Campus',
]

ATENEO_REG_L8 = {
    'Politecnico di Torino': 'Piemonte', 'Politecnico di Milano': 'Lombardia',
    'Università di Bergamo': 'Lombardia', 'Università di Brescia': 'Lombardia',
    'Università di Pavia': 'Lombardia', 'Università di Bolzano': 'Trentino-Alto Adige/Südtirol',
    'Università di Trento': 'Trentino-Alto Adige/Südtirol', 'Università di Padova': 'Veneto',
    'Università di Verona': 'Veneto', 'Università di Udine': 'Friuli-Venezia Giulia',
    'Università di Trieste': 'Friuli-Venezia Giulia', 'Università di Genova': 'Liguria',
    'Università di Bologna': 'Emilia-Romagna', 'Università di Ferrara': 'Emilia-Romagna',
    'Università di Modena e Reggio Emilia': 'Emilia-Romagna', 'Università di Parma': 'Emilia-Romagna',
    'Università di Firenze': 'Toscana', 'Università di Pisa': 'Toscana',
    'Università di Siena': 'Toscana', 'Università di Perugia': 'Umbria',
    'Politecnica delle Marche': 'Marche', 'La Sapienza': 'Lazio',
    'Tor Vergata': 'Lazio', 'Roma Tre': 'Lazio', 'Campus Biomedico': 'Lazio',
    'Link Campus': 'Lazio', "Università de L'Aquila": 'Abruzzo',
    'Università di Cassino e del Lazio Meridionale': 'Lazio',
    'Kore': 'Sicilia', 'Federico II': 'Campania', 'Università Vanvitelli': 'Campania',
    'Parthenope': 'Campania', 'Università del Sannio': 'Campania',
    'Magna Graecia': 'Calabria', 'Mediterranea': 'Calabria',
    'Università della Calabria': 'Calabria', 'Politecnico di Bari': 'Puglia',
    'Università del SALENTO': 'Puglia', 'Università di Foggia': 'Puglia',
    'Università di Messina': 'Sicilia', 'Università di Palermo': 'Sicilia',
    'Università di Catania': 'Sicilia', 'Università di Cagliari': 'Sardegna',
    'Università di Sassari': 'Sardegna', "Università Ca' Foscari": 'Veneto',
    'LUM "Degennaro"': 'Puglia', 'Università di Salerno': 'Campania',
    'Telematica Niccolò Cusano': 'Lazio', 'Telematica Guglielmo Marconi': 'Lazio',
    'Telematica Giustino Fortunato': 'Campania', 'Telematica Uninettuno': 'Lazio',
    'Telematica Universitas Mercatorum': 'Lazio', 'Telematica e-Campus': 'Lombardia',
}
REGIONE_MACRO = {
    'Piemonte': 'Nord', 'Lombardia': 'Nord', 'Veneto': 'Nord',
    'Friuli-Venezia Giulia': 'Nord', 'Liguria': 'Nord',
    'Emilia-Romagna': 'Nord', 'Trentino-Alto Adige/Südtirol': 'Nord',
    'Toscana': 'Centro', 'Umbria': 'Centro', 'Marche': 'Centro',
    'Lazio': 'Centro', 'Abruzzo': 'Centro',
    'Campania': 'Sud', 'Puglia': 'Sud', 'Basilicata': 'Sud',
    'Calabria': 'Sud', 'Molise': 'Sud',
    'Sicilia': 'Isole', 'Sardegna': 'Isole',
}
MACRO_FAMIGLIE = {
    'Ingegneria Informatica': 'Informatica',
    "Ingegneria Informatica E Dell'Automazione": 'Informatica',
    "Ingegneria Informatica E Dell'Intelligenza Artificiale": 'Informatica',
    'Ingegneria Informatica Ed Elettronica': 'Informatica',
    'Ingegneria Informatica E Automatica': 'Informatica',
    'Ingegneria Informatica E Delle Telecomunicazioni': 'Informatica',
    'Ingegneria Informatica E Biomedica': 'Informatica',
    "Ingegneria Informatica E Dell'Informazione": 'Informatica',
    'Ingegneria Informatica Per La Transizione Digitale': 'Informatica',
    'Ingegneria  Informatica': 'Informatica',
    'Ingegneria Delle Tecnologie Informatiche': 'Informatica',
    'Ingegneria E Scienze Informatiche': 'Informatica',
    'Ingegneria E Scienze Informatiche Per La Cybersecurity': 'Informatica',
    'Ingegneria Informatica, Elettronica E Delle Telecomunicazioni': 'Informatica',
    'Ingegneria Informatica, Delle Comunicazioni Ed Elettronica': 'Informatica',
    'Ingegneria Informatica, Biomedica E Delle Telecomunicazioni': 'Informatica',
    "Ingegneria Delle Tecnologie Per L'Impresa Digitale": 'Informatica',
    "Ingegneria Dell'Innovazione Per Le Imprese Digitali": 'Informatica',
    'Ingegneria Di Internet': 'Informatica',
    'Ingegneria Elettronica': 'Elettronica',
    'Ingegneria Elettronica E Informatica': 'Elettronica',
    'Ingegneria Elettronica E Biomedica': 'Elettronica',
    'Ingegneria Elettronica E Delle Tecnologie Digitali': 'Elettronica',
    'Ingegneria Elettronica E Delle Tecnologie Internet': 'Elettronica',
    'Ingegneria Elettronica E Telecomunicazioni': 'Elettronica',
    "Ingegneria Elettronica E Tecnologie Dell'Informazione": 'Elettronica',
    'Ingegneria Elettronica E Delle Telecomunicazioni': 'Elettronica',
    'Ingegneria Elettronica, Informatica E Delle Telecomunicazioni': 'Elettronica',
    'Ingegneria Elettronica E Dei Sistemi Ciberfisici': 'Elettronica',
    'Electronic And Communications Engineering (Ingegneria Elettronica E Delle Comunicazioni)': 'Elettronica',
    'Ingegneria Biomedica': 'Biomedica',
    'Bioingegneria': 'Biomedica',
    'Ingegneria Dei Sistemi Medicali': 'Biomedica',
    'Ingegneria Dei Sistemi Medicali Per La Persona': 'Biomedica',
    "Ingegneria Dell'Informazione Per La Medicina Digitale": 'Biomedica',
    'Ingegneria Gestionale': 'Gestionale',
    'Ingegneria Delle Telecomunicazioni': 'Telecomunicazioni',
    'Ingegneria Delle Comunicazioni': 'Telecomunicazioni',
    'Ingegneria Delle Telecomunicazioni E Dei Media Digitali': 'Telecomunicazioni',
    'Ingegneria Delle Telecomunicazioni, Internet E Multimedia': 'Telecomunicazioni',
    "Ingegneria Dell'Automazione": 'Automazione',
    "Ingegneria Dell'Automazione E Dei Sistemi": 'Automazione',
    "Ingegneria Dell'Automazione Industriale": 'Automazione',
    "Corso Di Laurea In Ingegneria Dell'Automazione": 'Automazione',
    'Ingegneria Robotica': 'Automazione',
    'Ingegneria Dei Sistemi Robotici E Intelligenti': 'Automazione',
    'Ingegneria Cibernetica': 'Automazione',
    "Ingegneria Dell'Informazione": 'Informazione',
    "Ingegneria Dell' Informazione: Elettronica, Informatica E Telecomunicazioni": 'Informazione',
}
MACRO_FAMIGLIE_CLEAN = {k: ('Multidisciplinare' if v in ['Altro', 'Multidisciplinare'] else v) for k, v in MACRO_FAMIGLIE.items()}
COLORI_FAMIGLIE = {
    'Informatica': '#14B8A6', 'Elettronica': '#0D9488',
    'Biomedica': '#99F6E4', 'Gestionale': '#0F766E',
    'Telecomunicazioni': '#2DD4BF'', 'Automazione': '#115E59',
    'Informazione': '#134E4A', 'Multidisciplinare': '#6B7280',
}

# ── DATI ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv('PENTAHO(L8).csv', sep=',', encoding='latin-1', quotechar='"', on_bad_lines='skip')
    df['Ateneo'] = df['Ateneo'].str.encode('latin-1').str.decode('utf-8', errors='replace')
    df['Numeratore'] = df['Numeratore'].astype(str).str.replace('.000', '', regex=False).str.replace(',', '.', regex=False)
    df['Numeratore'] = pd.to_numeric(df['Numeratore'], errors='coerce')
    df['corso_nome'] = (df['Nome Corso'].str.split(' - ', n=1).str[1].str.strip()
        .str.encode('latin-1', errors='replace').str.decode('utf-8', errors='replace')
        .str.title().str.strip().str.replace(r'\s+', ' ', regex=True))
    df['macro_famiglia'] = df['corso_nome'].map(MACRO_FAMIGLIE_CLEAN).fillna('Multidisciplinare')
    df['regione'] = df['Ateneo'].map(ATENEO_REG_L8)
    df['macro'] = df['regione'].map(REGIONE_MACRO)
    mur_l = pd.read_csv('MUR_laureatixclasse.csv', sep=';', encoding='latin-1')
    mur_i = pd.read_csv('MURiscrittixcorsodistudi.csv', sep=';', encoding='latin-1')
    mur_l_l8 = mur_l[mur_l['ClasseNUMERO'] == 'L-8'].copy()
    mur_i_l8 = mur_i[mur_i['ClasseNUMERO'] == 'L-8'].copy()
    tasse = pd.read_csv('TasseUniversitarieL8.csv', sep=';', encoding='cp1252')
    tasse = tasse[['Ateneo', 'Tipo', 'Contributo max']].copy()
    tasse['Ateneo'] = tasse['Ateneo'].str.strip()
    tasse['Contributo max'] = (tasse['Contributo max'].astype(str)
        .str.replace('€', '', regex=False).str.replace('.', '', regex=False)
        .str.replace(',', '.', regex=False).str.strip())
    tasse['Contributo max'] = pd.to_numeric(tasse['Contributo max'], errors='coerce')
    return df, mur_l_l8, mur_i_l8, tasse

@st.cache_data
def prep_indicatori(df):
    ic14    = df[df['ID Indicatore'] == 'iC14'].copy()
    ic21    = df[df['ID Indicatore'] == 'iC21'].copy()
    ic00b   = df[df['ID Indicatore'] == 'iC00b'].copy()
    ic16bis = df[df['ID Indicatore'] == 'iC16BIS'].copy()
    ic02    = df[df['ID Indicatore'] == 'iC02'].copy()
    merge14 = ic14.merge(ic00b, on=['Ateneo', 'Anno accademico', 'Nome Corso'], suffixes=('_14', '_00b'))
    merge14['perc_iC14'] = merge14['Numeratore_14'] / merge14['Numeratore_00b'] * 100
    merge21 = ic21.merge(ic00b, on=['Ateneo', 'Anno accademico', 'Nome Corso'], suffixes=('_21', '_00b'))
    merge21['perc_iC21'] = merge21['Numeratore_21'] / merge21['Numeratore_00b'] * 100
    merge14_var = merge14.copy()
    merge14_var['corso_pulito'] = merge14_var['Nome Corso'].str.split(' - ', n=1).str[1].str.strip()\
        .str.encode('latin-1', errors='replace').str.decode('utf-8', errors='replace')\
        .str.title().str.strip().str.replace(r'\s+', ' ', regex=True)
    merge14_var['macro_famiglia'] = merge14_var['corso_pulito'].map(MACRO_FAMIGLIE_CLEAN).fillna('Multidisciplinare')
    ic14_naz = merge14.groupby('Anno accademico')['perc_iC14'].mean().reset_index()
    ic14_naz.columns = ['anno', 'ic14']
    ic21_naz = merge21.groupby('Anno accademico')['perc_iC21'].mean().reset_index()
    ic21_naz.columns = ['anno', 'ic21']
    df_destino = ic14_naz.merge(ic21_naz, on='anno')
    df_destino['prosegue_stesso'] = df_destino['ic14'].round(1)
    df_destino['cambia_corso']    = (df_destino['ic21'] - df_destino['ic14']).round(1)
    df_destino['abbandona']       = (100 - df_destino['ic21']).round(1)
    df_destino['anno'] = df_destino['anno'].astype(str)
    merge16 = ic16bis.merge(ic00b, on=['Ateneo', 'Anno accademico', 'Nome Corso'], suffixes=('_16', '_00b'))
    merge16['perc_iC16'] = merge16['Numeratore_16'] / merge16['Numeratore_00b'] * 100
    ic16_naz = merge16.groupby('Anno accademico')['perc_iC16'].mean().reset_index()
    ic16_naz.columns = ['anno', 'pct']
    ic16_naz['pct'] = ic16_naz['pct'].round(1)
    return ic14, ic21, ic00b, ic02, merge14, merge14_var, df_destino, ic16_naz

df, mur_l_l8, mur_i_l8, tasse = load_data()
ic14, ic21, ic00b, ic02, merge14, merge14_var, df_destino, ic16_naz = prep_indicatori(df)

anni_alma = [2020, 2021, 2022, 2023, 2024, 2025]
alma_profilo = pd.DataFrame({
    'anno':             anni_alma,
    'pct_soddisfatti':  [91.1, 90.1, 90.1, 90.6, 90.2, 88.7],
    'pct_riiscrizione': [74.8, 75.1, 74.1, 74.9, 74.8, 73.1],
    'pct_magistrale':   [85.1, 84.9, 85.0, 84.5, 84.7, 82.7],
    'pct_lavora':       [22.1, 24.3, 30.3, 27.6, 32.9, 36.1],
    'retribuzione':     [1135, 1164, 1226, 1264, 1393, 1327],
})

def get_key_exact(dizionario, parola):
    for k, v in dizionario.items():
        k_clean = k.encode('latin-1', errors='replace').decode('utf-8', errors='replace').strip()
        if parola.lower() in k_clean.lower():
            return v
    return None

def parse_almalaurea_csv(filepath):
    data = {}
    try:
        with open(filepath, 'r', encoding='latin-1') as f:
            for line in f:
                line = line.strip().strip('"')
                parts = line.split(';')
                if len(parts) >= 2:
                    chiave = parts[0].strip().strip('"')
                    valore = parts[1].strip().strip('"')
                    if chiave and valore:
                        try: data[chiave] = float(valore.replace('.', '').replace(',', '.'))
                        except: data[chiave] = valore
    except: pass
    return data

try:
    profili = {a: parse_almalaurea_csv(f'datialmalaureaPROFILO{a}(L8).csv') for a in anni_alma}
    dest_data = {
        'Stesso Ateneo':   [get_key_exact(profili[a], 'Stesso Ateneo della laurea') for a in anni_alma],
        'Altro Nord':      [get_key_exact(profili[a], 'Ateneo del Nord') for a in anni_alma],
        'Altro Centro':    [get_key_exact(profili[a], 'Ateneo del Centro') for a in anni_alma],
        'Altro Sud-Isole': [get_key_exact(profili[a], 'Ateneo del Sud') for a in anni_alma],
        'Telematico':      [get_key_exact(profili[a], 'italiano telematico') for a in anni_alma],
        'Estero':          [get_key_exact(profili[a], 'Ateneo estero') for a in anni_alma],
    }
    df_dest = pd.DataFrame(dest_data)
    df_dest['anno'] = [str(a) for a in anni_alma]
    alma_ok = True
except:
    alma_ok = False
    df_dest = pd.DataFrame()

# ── HELPER ────────────────────────────────────────────────────────────────────
def chart_header(titolo, descrizione, istruzioni):
    st.markdown(f"### {titolo}")
    st.markdown(f'<p class="chart-description">{descrizione}</p>', unsafe_allow_html=True)
    if istruzioni:
        st.markdown(f'<div class="chart-instructions">{istruzioni}</div>', unsafe_allow_html=True)

def fonte_ann(testo):
    return dict(x=0.99, y=-0.13, xref='paper', yref='paper', text=testo, showarrow=False,
                font=dict(size=10, color='#9CA3AF'), align='right', xanchor='right')

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 1.5rem 0 1rem 0;'>
        <div style='font-size:1.0rem; font-weight:600; color:#F5F5F7; letter-spacing:-0.02em;'>L-8 Ingegneria dell'Informazione</div>
        <div style='font-size:0.75rem; color:#C8C8C8; margin-top:0.25rem; font-weight:400;'>Analisi Nazionale</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">Sezioni</div>', unsafe_allow_html=True)
    sezione = st.radio(label="", options=[
        "Panoramica", "Iscritti", "Profilo Studenti", "Percorso Accademico",
        "Varianti del Corso", "Tasse e Contributi", "Analisi Avanzata", "Sintesi",
    ], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("""<div style='font-size:0.72rem; color:#4D7A5A; line-height:1.6;'>
        Fonti: MUR-USTAT, ANVUR,<br>AlmaLaurea · Dati 2010–2025</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PANORAMICA
# ══════════════════════════════════════════════════════════════════════════════
if sezione == "Panoramica":
    st.markdown("# Analisi Nazionale\nL-8 Ingegneria dell'Informazione")
    st.markdown("---")
    st.markdown("""<p>Questa analisi documenta il panorama nazionale del Corso di Laurea in Ingegneria dell'Informazione (Classe L-8)
    attraverso dati ufficiali MUR-USTAT, ANVUR e AlmaLaurea. I dati coprono il periodo 2010–2025
    e includono avvii di carriera al primo anno, iscritti, laureati, distribuzione geografica,
    profilo degli studenti e indicatori di qualità della didattica.</p>""", unsafe_allow_html=True)
    st.markdown("### Indicatori chiave")
    avvi_2025 = int(df[(df['ID Indicatore'] == 'iC00a') & (df['Anno accademico'] == 2025)]['Numeratore'].sum())
    n_atenei = df['Ateneo'].nunique()
    kpi = [
        {'label': 'Avvii di carriera 2025', 'value': f'{avvi_2025:,}', 'delta': '↑ trend crescita', 'color': '#14B8A6'},
        {'label': 'Atenei attivi L-8',      'value': str(n_atenei),    'delta': 'incluse telematiche', 'color': '#2DD4BF''},
        {'label': 'Soddisfatti del corso',  'value': '88.7%',          'delta': 'AlmaLaurea 2025',    'color': '#F59E0B'},
        {'label': 'Prosegue magistrale',    'value': '82.7%',          'delta': 'AlmaLaurea 2025',    'color': '#34D399'},
    ]
    cols = st.columns(4)
    for col, k in zip(cols, kpi):
        with col:
            st.markdown(f"""<div class="section-card" style="border-top:3px solid {k['color']};padding:1.25rem;">
                <div style="font-size:0.75rem;color:#C8C8C8;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.5rem;">{k['label']}</div>
                <div style="font-size:2rem;font-weight:700;color:{k['color']};letter-spacing:-0.03em;">{k['value']}</div>
                <div style="font-size:0.78rem;color:#C8C8C8;margin-top:0.25rem;">{k['delta']}</div>
            </div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### Struttura dell'analisi")
    sezioni_info = [
        ("Iscritti", "Avvii di carriera al primo anno, distribuzione geografica, top atenei, focus sul Lazio e totale iscritti.", "#14B8A6"),
        ("Profilo Studenti", "Soddisfazione, riiscrizione e destinazione alla magistrale.", "#2DD4BF'"),
        ("Percorso Accademico", "Laureati, laureati in corso e tasso di prosecuzione al II anno.", "#EF4444"),
        ("Varianti del Corso", "Tasso di prosecuzione per famiglia di corso L-8.", "#818CF8"),
        ("Tasse e Contributi", "Confronto contributo massimo annuo tra atenei statali e non statali.", "#EF4444"),
        ("Analisi Avanzata", "iC16BIS e correlazione tra dimensione del corso e prosecuzione.", "#60A5FA"),
        ("Sintesi", "Riepilogo dei risultati principali dell'analisi.", "#F59E0B"),
    ]
    for nome, desc, col in sezioni_info:
        st.markdown(f"""<div class="section-card" style="display:flex;align-items:flex-start;gap:1rem;padding:1.25rem;">
            <div style="width:3px;background:{col};border-radius:2px;min-height:40px;flex-shrink:0;"></div>
            <div>
                <div style="font-size:0.9rem;font-weight:600;color:#F5F5F7;margin-bottom:0.25rem;">{nome}</div>
                <div style="font-size:0.82rem;color:#C8C8C8;font-weight:300;">{desc}</div>
            </div></div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ISCRITTI
# ══════════════════════════════════════════════════════════════════════════════
elif sezione == "Iscritti":
    st.markdown("## Iscritti")
    st.markdown("---")

    # G1 — Avvii nazionali
    chart_header("Avvii di carriera nazionali — L-8 (2020–2025)",
        "Numero totale di immatricolati puri al primo anno (iC00a). La barra più chiara indica l'ultimo anno disponibile. Le variazioni percentuali rispetto all'anno precedente sono indicate all'interno delle barre.",
        "Passa il cursore sulle barre per vedere il valore esatto.")
    avvi_naz = df[df['ID Indicatore'] == 'iC00a'].groupby('Anno accademico')['Numeratore'].sum().reset_index()
    avvi_naz.columns = ['anno', 'avvii']
    media_avvi = avvi_naz['avvii'].mean()
    colori_avvi = [VERDE_LIGHT if a == avvi_naz['anno'].max() else VERDE_MAIN for a in avvi_naz['anno']]
    fig_avvi = go.Figure()
    fig_avvi.add_trace(go.Scatter(x=[avvi_naz['anno'].min()-0.5, avvi_naz['anno'].max()+0.5], y=[media_avvi, media_avvi],
        mode='lines', line=dict(color='#F59E0B', width=2, dash='dash'), name=f'Media: {media_avvi:,.0f}', hoverinfo='skip'))
    fig_avvi.add_trace(go.Bar(x=avvi_naz['anno'], y=avvi_naz['avvii'],
        marker=dict(color=colori_avvi, line=dict(width=0), cornerradius=6),
        text=avvi_naz['avvii'].apply(lambda x: f'{x:,.0f}'), textposition='outside',
        textfont=dict(color='#F5F5F7', size=14, family='Inter'),
        hovertemplate='<b>%{x}</b><br>Avvii: <b>%{y:,.0f}</b><extra></extra>', name='Avvii di carriera'))
    for i, row in avvi_naz.iterrows():
        if i == 0: continue
        var = (row['avvii'] - avvi_naz.loc[i-1, 'avvii']) / avvi_naz.loc[i-1, 'avvii'] * 100
        colore = '#34D399' if var >= 0 else '#F87171'
        simbolo = '▲' if var >= 0 else '▼'
        fig_avvi.add_annotation(x=row['anno'], y=row['avvii']*0.5, text=f"{simbolo} {abs(var):.1f}%",
            showarrow=False, font=dict(size=13, color=colore, family='Inter'))
    fig_avvi.update_layout(font=dict(family='Inter', size=13), plot_bgcolor=BG_PLOT, paper_bgcolor=BG_PAPER,
        showlegend=True, legend=dict(font=dict(color='#C8C8C8', size=13), bgcolor='rgba(0,0,0,0)',
            orientation='h', x=0.5, xanchor='center', y=1.08),
        margin=dict(t=80, b=60, l=60, r=80), height=480,
        annotations=[fonte_ann('Fonte: ANVUR Cruscotto PENTAHO — Avvii di carriera al primo anno (iC00a)')])
    fig_avvi.update_xaxes(showgrid=False, tickfont=dict(color='#C8C8C8', size=14), linecolor='#2D5A5A', tickmode='linear', dtick=1)
    fig_avvi.update_yaxes(gridcolor='#1A3A3A', tickfont=dict(color='#C8C8C8'), linecolor='#2D5A5A', rangemode='tozero',
        title=dict(text='N° avvii di carriera', font=dict(color='#C8C8C8')), range=[0, avvi_naz['avvii'].max()*1.2])
    st.plotly_chart(fig_avvi, use_container_width=True)
    st.markdown("---")

    # G2 — Treemap famiglie
    chart_header("Avvii di carriera per famiglia di corso",
        "Distribuzione degli avvii per macro-famiglia di corso L-8. Clicca su una famiglia per espandere le varianti al suo interno.",
        "Seleziona l'anno con i pulsanti. Clicca su un rettangolo per entrare nel dettaglio.")
    anni_tree = sorted(df[df['ID Indicatore'] == 'iC00a']['Anno accademico'].unique())
    fig_tree = go.Figure()
    for i, anno in enumerate(anni_tree):
        subset = df[(df['ID Indicatore'] == 'iC00a') & (df['Anno accademico'] == anno)].copy()
        macro = subset.groupby('macro_famiglia').agg(avvii=('Numeratore','sum'), n_atenei=('Ateneo','nunique')).reset_index()
        varianti = subset.groupby(['macro_famiglia','corso_nome']).agg(avvii=('Numeratore','sum'), n_atenei=('Ateneo','nunique')).reset_index()
        labels=[]; parents=[]; values=[]; colors=[]; hovers=[]
        for _, row in macro.iterrows():
            labels.append(row['macro_famiglia']); parents.append(''); values.append(row['avvii'])
            colors.append(COLORI_FAMIGLIE.get(row['macro_famiglia'], '#6B7280'))
            hovers.append(f"<b>{row['macro_famiglia']}</b><br>Avvii: <b>{int(row['avvii']):,}</b><br>N° atenei: <b>{row['n_atenei']}</b>")
        for _, row in varianti.iterrows():
            labels.append(row['corso_nome']); parents.append(row['macro_famiglia']); values.append(row['avvii'])
            colors.append(COLORI_FAMIGLIE.get(row['macro_famiglia'], '#6B7280'))
            hovers.append(f"<b>{row['corso_nome']}</b><br>Avvii: <b>{int(row['avvii']):,}</b><br>N° atenei: <b>{row['n_atenei']}</b>")
        fig_tree.add_trace(go.Treemap(labels=labels, parents=parents, values=values, customdata=hovers,
            hovertemplate='%{customdata}<extra></extra>', branchvalues='total',
            marker=dict(colors=colors, line=dict(color='#041A1A', width=2)),
            textfont=dict(size=13, color='white', family='Inter'),
            pathbar=dict(visible=True, thickness=24, textfont=dict(size=12, color='white', family='Inter')),
            visible=(i == 0)))
    buttons_tree = [dict(label=str(a), method='update',
        args=[{'visible': [j==i for j in range(len(anni_tree))]},
              {'title': dict(text=f'Avvii per Famiglia L-8 — {a}', font=dict(size=18, color='#F5F5F7', family='Inter'), x=0.5, xanchor='center')}])
        for i, a in enumerate(anni_tree)]
    fig_tree.update_layout(title=dict(text=f'Avvii per Famiglia L-8 — {anni_tree[0]}', font=dict(size=18, color='#F5F5F7', family='Inter'), x=0.5, xanchor='center'),
        updatemenus=[dict(type='buttons', direction='right', x=0.5, xanchor='center', y=1.10, yanchor='top',
            buttons=buttons_tree, bgcolor=BG_CARD, bordercolor=VERDE_MAIN, borderwidth=1,
            font=dict(size=12, family='Inter', color='#F5F5F7'), active=0, pad=dict(r=6,l=6,t=6,b=6))],
        height=560, margin=dict(t=120, b=40, l=20, r=20), font=dict(family='Inter', size=12), paper_bgcolor=BG_PAPER)
    st.plotly_chart(fig_tree, use_container_width=True)
    st.markdown("---")

    # G3 — Mappa
    chart_header("Distribuzione geografica degli avvii per regione",
        "La mappa mostra la distribuzione degli avvii di carriera al primo anno per regione, dal 2020 al 2025. Le regioni in grigio scuro non ospitano atenei con corsi L-8 attivi.",
        "Seleziona l'anno con i pulsanti. Passa il cursore sulla regione per il dettaglio per ateneo e corso.")
    GRIGIO_SCURO = ["Valle d'Aosta/Vallée d'Aoste", 'Molise', 'Basilicata']
    avvi_map = df[df['ID Indicatore'] == 'iC00a'].copy()
    df_hover_map = avvi_map.groupby(['Anno accademico','regione','Ateneo','corso_nome'])['Numeratore'].sum().reset_index()
    def crea_hover(regione, anno):
        subset = df_hover_map[(df_hover_map['regione']==regione)&(df_hover_map['Anno accademico']==anno)].sort_values(['Ateneo','Numeratore'],ascending=[True,False])
        totale = int(subset['Numeratore'].sum())
        testo = f"<b>{regione}</b><br>Anno: {anno}<br>Avvii: <b>{totale:,}</b><br><br>"
        ateneo_corrente = None
        for _, row in subset.iterrows():
            if row['Ateneo'] != ateneo_corrente:
                ateneo_corrente = row['Ateneo']
                testo += f"<b>{ateneo_corrente}</b><br>"
            testo += f"&nbsp;&nbsp;{row['corso_nome']}: {int(row['Numeratore']):,}<br>"
        return testo
    df_mappa = avvi_map.groupby(['Anno accademico','regione'])['Numeratore'].sum().reset_index()
    df_mappa.columns = ['anno','regione','avvii']
    df_mappa['hover'] = df_mappa.apply(lambda r: crea_hover(r['regione'], r['anno']), axis=1)
    anni_map = sorted(df_mappa['anno'].unique())
    GEOJSON_URL = "https://raw.githubusercontent.com/openpolis/geojson-italy/master/geojson/limits_IT_regions.geojson"
    fig_map = go.Figure()
    for i, anno in enumerate(anni_map):
        subset = df_mappa[df_mappa['anno']==anno]
        fig_map.add_trace(go.Choropleth(geojson=GEOJSON_URL, locations=subset['regione'], featureidkey='properties.reg_name',
            z=subset['avvii'], colorscale=[[0.0,'#D4F1D4'],[0.25,'#99F6E4'],[0.5,'#2DD4BF''],[0.75,'#0D9488'],[1.0,'#134E4A']],
            zmin=df_mappa['avvii'].min(), zmax=df_mappa['avvii'].max(),
            colorbar=dict(title=dict(text='Avvii', font=dict(color='#C8C8C8')), tickfont=dict(color='#C8C8C8'), x=1.0, thickness=15),
            marker_line_color='#041A1A', marker_line_width=1.5,
            text=subset['hover'], hovertemplate='%{text}<extra></extra>', name=str(anno), visible=(i==0)))
        fig_map.add_trace(go.Choropleth(geojson=GEOJSON_URL, locations=GRIGIO_SCURO, featureidkey='properties.reg_name',
            z=[0]*len(GRIGIO_SCURO), colorscale=[[0,'#3A3A3A'],[1,'#3A3A3A']], showscale=False,
            marker_line_color='#041A1A', marker_line_width=1.5,
            hovertemplate='<b>%{location}</b><br>Nessun corso L-8 attivo<extra></extra>',
            visible=(i==0), showlegend=False))
    n_layers = 2
    buttons_map = []
    for i, anno in enumerate(anni_map):
        vis = []
        for j in range(len(anni_map)): vis += [j==i]*n_layers
        buttons_map.append(dict(label=str(anno), method='update',
            args=[{'visible': vis}, {'title': dict(text=f'Avvii L-8 per Regione — {anno}', font=dict(size=18, color='#F5F5F7', family='Inter'), x=0.5, xanchor='center')}]))
    fig_map.update_layout(title=dict(text=f'Avvii L-8 per Regione — {anni_map[0]}', font=dict(size=18, color='#F5F5F7', family='Inter'), x=0.5, xanchor='center'),
        updatemenus=[dict(type='buttons', direction='right', x=0.5, xanchor='center', y=1.08, yanchor='top',
            buttons=buttons_map, bgcolor=BG_CARD, bordercolor=VERDE_MAIN, borderwidth=1,
            font=dict(size=12, family='Inter', color='#F5F5F7'), active=0, pad=dict(r=6,l=6,t=6,b=6))],
        annotations=[dict(x=0.01, y=-0.02, xref='paper', yref='paper', text="Grigio scuro: Valle d'Aosta, Molise, Basilicata — nessun corso attivo",
                showarrow=False, font=dict(size=10, color='#9CA3AF'), align='left'),
            dict(x=0.99, y=-0.02, xref='paper', yref='paper', text='Fonte: ANVUR — iC00a',
                showarrow=False, font=dict(size=10, color='#9CA3AF'), xanchor='right')],
        margin=dict(r=20, t=110, l=0, b=40), height=620, font=dict(family='Inter', size=12), paper_bgcolor=BG_PAPER, geo=dict(bgcolor=BG_PAPER))
    fig_map.update_geos(fitbounds='locations', visible=False)
    st.plotly_chart(fig_map, use_container_width=True)
    st.markdown("---")

    # G4 — Top 15
    chart_header("Top 15 atenei per avvii di carriera",
        "I 15 atenei con il maggior numero di avvii di carriera L-8 per anno accademico. I colori indicano la macro area geografica: blu = Nord, verde = Centro, arancio = Sud, viola = Isole.",
        "Seleziona l'anno con i pulsanti. Passa il cursore sulle barre per il dettaglio per corso.")
    df_top15 = df[df['ID Indicatore'] == 'iC00a'].copy()
    corsi_hover = df_top15.groupby(['Anno accademico','Ateneo']).apply(
        lambda x: '<br>'.join([f"&nbsp;&nbsp;• {row['corso_nome']}: <b>{int(row['Numeratore']):,}</b>"
            for _, row in x.sort_values('Numeratore', ascending=False).iterrows()]),
        include_groups=False).reset_index().rename(columns={0:'lista_corsi'})
    n_corsi = df_top15.groupby(['Anno accademico','Ateneo'])['corso_nome'].nunique().reset_index().rename(columns={'corso_nome':'n_corsi'})
    g_top15 = df_top15.groupby(['Anno accademico','Ateneo','regione','macro'])['Numeratore'].sum().reset_index()
    g_top15 = g_top15.merge(n_corsi, on=['Anno accademico','Ateneo'], how='left')
    g_top15 = g_top15.merge(corsi_hover, on=['Anno accademico','Ateneo'], how='left')
    anni_top = sorted(g_top15['Anno accademico'].unique())
    fig_top = go.Figure()
    for i, anno in enumerate(anni_top):
        subset = g_top15[g_top15['Anno accademico']==anno].sort_values('Numeratore', ascending=False).head(15).sort_values('Numeratore', ascending=True).reset_index(drop=True)
        fig_top.add_trace(go.Bar(x=subset['Numeratore'], y=subset['Ateneo'], orientation='h',
            marker=dict(color=[COLORI_MACRO.get(m,'#6B7280') for m in subset['macro']], line=dict(width=0), opacity=0.9, cornerradius=4),
            text=subset['Numeratore'].astype(int).apply(lambda x: f'{x:,}'), textposition='outside',
            textfont=dict(size=11, color='#C8C8C8'),
            customdata=subset[['macro','n_corsi','lista_corsi']].values,
            hovertemplate='<b>%{y}</b><br>Avvii: <b>%{x:,}</b><br>Macro: %{customdata[0]}<br>Corsi: <b>%{customdata[1]}</b><br>%{customdata[2]}<extra></extra>',
            visible=(i==0), showlegend=False))
    for macro, colore in COLORI_MACRO.items():
        fig_top.add_trace(go.Bar(x=[None], y=[None], orientation='h', marker_color=colore, name=macro, visible=True))
    buttons_top = [dict(label=str(a), method='update',
        args=[{'visible': [j==i for j in range(len(anni_top))]+[True]*len(COLORI_MACRO)},
              {'title': dict(text=f'Top 15 Atenei — L-8 {a}', font=dict(size=18, color='#F5F5F7', family='Inter'), x=0.5, xanchor='center')}])
        for i, a in enumerate(anni_top)]
    fig_top.update_layout(font=dict(family='Inter', size=12), plot_bgcolor=BG_PLOT, paper_bgcolor=BG_PAPER,
        title=dict(text=f'Top 15 Atenei — L-8 {anni_top[0]}', font=dict(size=18, color='#F5F5F7', family='Inter'), x=0.5, xanchor='center'),
        updatemenus=[dict(type='buttons', direction='right', x=0.5, xanchor='center', y=1.10, yanchor='top',
            buttons=buttons_top, bgcolor=BG_CARD, bordercolor=VERDE_MAIN, borderwidth=1,
            font=dict(size=12, family='Inter', color='#F5F5F7'), active=0, pad=dict(r=6,l=6,t=6,b=6))],
        legend=dict(title=dict(text='Macro area', font=dict(color='#C8C8C8')), font=dict(color='#C8C8C8'), bgcolor='rgba(0,0,0,0)', x=0.78, y=0.05),
        margin=dict(t=120, b=60, l=220, r=120), height=560, barmode='overlay')
    fig_top.update_xaxes(title=dict(text='N° avvii', font=dict(color='#C8C8C8')), showgrid=False, tickfont=dict(color='#C8C8C8'), linecolor='#2D5A5A')
    fig_top.update_yaxes(showgrid=False, tickfont=dict(size=12, color='#C8C8C8'), linecolor='#2D5A5A')
    st.plotly_chart(fig_top, use_container_width=True)
    st.markdown("---")

    # G5 — Trend Lazio
    chart_header("Trend avvii nel Lazio — Tradizionali vs Telematiche",
        "Andamento degli avvii di carriera nei due sottogruppi di atenei laziali: tradizionali (La Sapienza, Tor Vergata, Roma Tre, Campus Biomedico, Cassino) e telematici. Il pannello di sinistra mostra i tradizionali, quello di destra le telematiche.",
        "Passa il cursore sulle linee per vedere i valori anno per anno e il dettaglio per corso.")
    lazio = df[(df['ID Indicatore']=='iC00a') & (df['regione']=='Lazio')].copy()
    lazio_agg = lazio.groupby(['Anno accademico','Ateneo'])['Numeratore'].sum().reset_index()
    lazio_agg['tipo'] = lazio_agg['Ateneo'].apply(lambda x: 'Telematica' if x in TELEMATICHE_LIST else 'Tradizionale')
    lazio_corsi = lazio.groupby(['Anno accademico','Ateneo','corso_nome'])['Numeratore'].sum().reset_index()
    def build_hover(ateneo, anno):
        corsi = lazio_corsi[(lazio_corsi['Ateneo']==ateneo)&(lazio_corsi['Anno accademico']==anno)].sort_values('Numeratore',ascending=False)
        testo = f"<b>{ateneo}</b><br>Anno: {anno}<br>Corsi L-8: <b>{len(corsi)}</b><br>"
        for _, r in corsi.iterrows():
            testo += f"&nbsp;&nbsp;• {r['corso_nome']}: <b>{int(r['Numeratore']):,}</b><br>"
        return testo
    lazio_agg['hover'] = lazio_agg.apply(lambda r: build_hover(r['Ateneo'], r['Anno accademico']), axis=1)
    trad = lazio_agg[lazio_agg['tipo']=='Tradizionale'].copy()
    tele = lazio_agg[lazio_agg['tipo']=='Telematica'].copy()
    PALETTE_TRAD = {'La Sapienza':'#14B8A6','Tor Vergata':'#60A5FA','Roma Tre':'#FB923C',
        'Campus Biomedico':'#C084FC','Università di Cassino e del Lazio Meridionale':'#F472B6'}
    PALETTE_TELE = {'Telematica Universitas Mercatorum':'#99F6E4','Telematica Uninettuno':'#93C5FD',
        'Telematica Guglielmo Marconi':'#FCD34D','Telematica Niccolò Cusano':'#F9A8D4','Link Campus':'#A3E635'}
    NOMI_BREVI = {'Università di Cassino e del Lazio Meridionale':'Cassino',
        'Telematica Universitas Mercatorum':'Universitas Mercatorum',
        'Telematica Uninettuno':'Uninettuno','Telematica Guglielmo Marconi':'G. Marconi',
        'Telematica Niccolò Cusano':'N. Cusano'}
    fig_lazio = make_subplots(rows=1, cols=2, column_widths=[0.5,0.5], horizontal_spacing=0.08)
    for ateneo in trad.groupby('Ateneo')['Numeratore'].sum().sort_values(ascending=False).index:
        colore = PALETTE_TRAD.get(ateneo,'#14B8A6')
        nome = NOMI_BREVI.get(ateneo, ateneo)
        df_lab = trad[trad['Ateneo']==ateneo].sort_values('Anno accademico')
        fig_lazio.add_trace(go.Scatter(x=df_lab['Anno accademico'].astype(str), y=df_lab['Numeratore'],
            mode='lines+markers', name=nome, legendgroup='trad',
            legendgrouptitle=dict(text='Tradizionali', font=dict(color='#99F6E4', size=12)),
            line=dict(color=colore, width=2.5), marker=dict(size=8, color=colore, line=dict(color='#041A1A', width=1.5)),
            text=df_lab['hover'], hovertemplate='%{text}<extra></extra>'), row=1, col=1)
        ultimo = df_lab.iloc[-1]
        fig_lazio.add_annotation(x=str(int(ultimo['Anno accademico'])), y=ultimo['Numeratore'],
            text=f"<b>{int(ultimo['Numeratore'])}</b>", showarrow=False, font=dict(size=9, color=colore), xanchor='left', xshift=8, row=1, col=1)
    for ateneo in tele.groupby('Ateneo')['Numeratore'].sum().sort_values(ascending=False).index:
        colore = PALETTE_TELE.get(ateneo,'#99F6E4')
        nome = NOMI_BREVI.get(ateneo, ateneo)
        df_lab = tele[tele['Ateneo']==ateneo].sort_values('Anno accademico')
        fig_lazio.add_trace(go.Scatter(x=df_lab['Anno accademico'].astype(str), y=df_lab['Numeratore'],
            mode='lines+markers', name=nome, legendgroup='tele',
            legendgrouptitle=dict(text='Telematiche', font=dict(color='#FCD34D', size=12)),
            line=dict(color=colore, width=2.5), marker=dict(size=8, color=colore, line=dict(color='#041A1A', width=1.5)),
            text=df_lab['hover'], hovertemplate='%{text}<extra></extra>'), row=1, col=2)
        ultimo = df_lab.iloc[-1]
        fig_lazio.add_annotation(x=str(int(ultimo['Anno accademico'])), y=ultimo['Numeratore'],
            text=f"<b>{int(ultimo['Numeratore'])}</b>", showarrow=False, font=dict(size=9, color=colore), xanchor='left', xshift=8, row=1, col=2)
    fig_lazio.update_layout(font=dict(family='Inter', size=12), plot_bgcolor=BG_PLOT, paper_bgcolor=BG_PAPER,
        title=dict(text='Avvii L-8 nel Lazio — Tradizionali vs Telematiche', font=dict(size=18, color='#F5F5F7', family='Inter'), x=0.5, xanchor='center'),
        annotations=[dict(x=0.22, y=1.10, xref='paper', yref='paper', text='<b>Atenei Tradizionali</b>', showarrow=False, font=dict(size=14, color='#99F6E4', family='Inter'), xanchor='center'),
            dict(x=0.78, y=1.10, xref='paper', yref='paper', text='<b>Atenei Telematici</b>', showarrow=False, font=dict(size=14, color='#FCD34D', family='Inter'), xanchor='center'),
            dict(x=0.99, y=-0.12, xref='paper', yref='paper', text='Fonte: ANVUR — iC00a', showarrow=False, font=dict(size=10, color='#9CA3AF'), xanchor='right')],
        legend=dict(font=dict(color='#C8C8C8', size=11), bgcolor='rgba(0,0,0,0)', groupclick='toggleitem', x=1.01, y=1, xanchor='left', yanchor='top'),
        height=500, margin=dict(t=130, b=80, l=60, r=160))
    for col in [1, 2]:
        fig_lazio.update_xaxes(showgrid=False, tickfont=dict(color='#C8C8C8'), linecolor='#2D5A5A', row=1, col=col)
        fig_lazio.update_yaxes(gridcolor='#1A3A3A', tickfont=dict(color='#C8C8C8'), linecolor='#2D5A5A',
            rangemode='tozero', title=dict(text='N° avvii', font=dict(color='#C8C8C8')), row=1, col=col)
    st.plotly_chart(fig_lazio, use_container_width=True)
    st.markdown("---")

    # G6 — Bubble macro aree
    chart_header("Quota avvii di carriera per macro area — trend 2020–2025",
        "Ogni bolla rappresenta la quota percentuale di avvii di carriera per macro area. La dimensione della bolla è proporzionale al numero assoluto di avvii.",
        "Passa il cursore sulle bolle per vedere quota e numero assoluto.")
    OFFSET_MACRO = {'Nord': 2, 'Centro': 1, 'Sud': -1, 'Isole': -2}
    avvi_macro = df[df['ID Indicatore']=='iC00a'].copy()
    macro_agg = avvi_macro.groupby(['Anno accademico','macro'])['Numeratore'].sum().reset_index()
    totale_anno = macro_agg.groupby('Anno accademico')['Numeratore'].sum().reset_index()
    totale_anno.columns = ['Anno accademico','totale']
    macro_pct = macro_agg.merge(totale_anno, on='Anno accademico')
    macro_pct['pct'] = (macro_pct['Numeratore'] / macro_pct['totale'] * 100).round(1)
    macro_pct = macro_pct.dropna(subset=['macro'])
    fig_bubble = go.Figure()
    for macro in ['Nord','Centro','Sud','Isole']:
        subset = macro_pct[macro_pct['macro']==macro].sort_values('Anno accademico').copy()
        subset['pct_offset'] = subset['pct'] + OFFSET_MACRO.get(macro, 0)
        fig_bubble.add_trace(go.Scatter(x=subset['Anno accademico'].astype(str), y=subset['pct_offset'],
            mode='markers+text', name=macro,
            marker=dict(size=subset['Numeratore']/macro_pct['Numeratore'].max()*80+20,
                color=COLORI_MACRO[macro], opacity=0.85, line=dict(color='#041A1A', width=2)),
            text=subset['pct'].apply(lambda x: f'{x:.1f}%'), textposition='middle center',
            textfont=dict(size=10, color='white', family='Inter'),
            customdata=list(zip(subset['pct'], subset['Numeratore'].astype(int))),
            hovertemplate=f'<b>{macro}</b><br>Anno: %{{x}}<br>Quota: <b>%{{customdata[0]:.1f}}%</b><br>Avvii: <b>%{{customdata[1]:,}}</b><extra></extra>'))
    fig_bubble.update_layout(font=dict(family='Inter', size=12), plot_bgcolor=BG_PLOT, paper_bgcolor=BG_PAPER,
        title=dict(text='Quota Avvii di Carriera per Macro Area — L-8 (2020–2025)', font=dict(size=18, color='#F5F5F7', family='Inter'), x=0.5, xanchor='center'),
        annotations=[dict(x=0.99, y=-0.10, xref='paper', yref='paper', text='Fonte: ANVUR — Dimensione bolla = avvii assoluti', showarrow=False, font=dict(size=10, color='#9CA3AF'), xanchor='right')],
        legend=dict(font=dict(color='#C8C8C8', size=12), bgcolor='rgba(0,0,0,0)', x=0.01, y=0.99),
        height=500, margin=dict(t=80, b=80, l=60, r=30))
    fig_bubble.update_xaxes(title=dict(text='Anno accademico', font=dict(color='#C8C8C8')), showgrid=False, tickfont=dict(color='#C8C8C8'), linecolor='#2D5A5A')
    fig_bubble.update_yaxes(title=dict(text='Quota (%)', font=dict(color='#C8C8C8')), gridcolor='#1A3A3A', ticksuffix='%', tickfont=dict(color='#C8C8C8'), linecolor='#2D5A5A', range=[0, 70])
    st.plotly_chart(fig_bubble, use_container_width=True)
    st.markdown("---")

    # G7 — Lollipop iscritti
    chart_header("Iscritti L-8 Ingegneria dell'Informazione — Italia (2019–2025)",
        "Numero totale di studenti iscritti a corsi L-8 Ingegneria dell'Informazione in Italia per anno accademico.",
        "Passa il cursore sui pallini per vedere il valore esatto.")
    isc_naz = mur_i_l8.groupby('AnnoA')['Isc'].sum().reset_index()
    isc_naz = isc_naz[isc_naz['AnnoA'].str[:4].astype(int) >= 2019].copy()
    isc_naz['anno_short'] = isc_naz['AnnoA'].str[:4] + '/' + isc_naz['AnnoA'].str[7:9]
    media_isc = isc_naz['Isc'].mean()
    fig_isc = go.Figure()
    for _, row in isc_naz.iterrows():
        fig_isc.add_shape(type='line', x0=row['anno_short'], x1=row['anno_short'], y0=0, y1=row['Isc'], line=dict(color=VERDE_MAIN, width=3))
    fig_isc.add_trace(go.Scatter(x=isc_naz['anno_short'], y=isc_naz['Isc'], mode='markers+text',
        marker=dict(size=20, color=[VERDE_LIGHT if a == isc_naz['anno_short'].iloc[-1] else VERDE_MAIN for a in isc_naz['anno_short']], line=dict(color='white', width=2)),
        text=isc_naz['Isc'].apply(lambda x: f'{x:,.0f}'), textposition='top center',
        textfont=dict(color='#F5F5F7', size=12, family='Inter'),
        hovertemplate='<b>%{x}</b><br>Iscritti: <b>%{y:,.0f}</b><extra></extra>', name='Iscritti L-8'))
    fig_isc.add_hline(y=media_isc, line=dict(color='#F59E0B', width=2, dash='dash'),
        annotation_text=f'Media: {media_isc:,.0f}', annotation_position='right',
        annotation_font=dict(color='#F59E0B', size=11))
    fig_isc.add_trace(go.Scatter(x=[None], y=[None], mode='lines',
        line=dict(color='#F59E0B', width=2, dash='dash'), name=f'Media periodo: {media_isc:,.0f}', showlegend=True))
    fig_isc.update_layout(font=dict(family='Inter', size=12), plot_bgcolor=BG_PLOT, paper_bgcolor=BG_PAPER,
        title=dict(text="Iscritti L-8 Ingegneria dell'Informazione — Italia (2019–2025)", font=dict(size=18, color='#F5F5F7', family='Inter'), x=0.5, xanchor='center'),
        showlegend=True, legend=dict(font=dict(color='#C8C8C8', size=11), bgcolor='rgba(0,0,0,0)', orientation='h', x=0.5, xanchor='center', y=1.08),
        margin=dict(t=100, b=80, l=70, r=100), height=520,
        annotations=[fonte_ann('Fonte: MUR-USTAT — Iscritti L-8 per anno accademico')])
    fig_isc.update_xaxes(showgrid=False, tickfont=dict(color='#C8C8C8', size=13), linecolor='#2D5A5A')
    fig_isc.update_yaxes(gridcolor='#1A3A3A', tickfont=dict(color='#C8C8C8'), linecolor='#2D5A5A', rangemode='tozero',
        title=dict(text='N° iscritti', font=dict(color='#C8C8C8')), range=[0, isc_naz['Isc'].max()*1.2])
    st.plotly_chart(fig_isc, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PROFILO STUDENTI
# ══════════════════════════════════════════════════════════════════════════════
elif sezione == "Profilo Studenti":
    st.markdown("## Profilo Studenti")
    st.markdown("---")

    # G8 — Gauge
    chart_header("Indicatori chiave del profilo laureati L-8",
        "I tre indicatori riportano i valori del 2025 confrontati con un anno di riferimento selezionabile. I dati provengono dall'indagine AlmaLaurea sul Profilo dei Laureati.",
        "Seleziona l'anno di riferimento per il confronto con i pulsanti in alto.")
    val_2025 = {'pct_soddisfatti': 88.7, 'pct_riiscrizione': 73.1, 'pct_magistrale': 82.7}
    indicatori_gauge = [('pct_soddisfatti','Soddisfatti del corso','#14B8A6'),('pct_riiscrizione','Si reiscriverebbero','#60A5FA'),('pct_magistrale','Prosegue magistrale','#C084FC')]
    anni_ref = [2020,2021,2022,2023,2024]
    fig_gauge = go.Figure()
    for anno_ref in anni_ref:
        visible = (anno_ref == 2024)
        for col_idx, (col, titolo, colore) in enumerate(indicatori_gauge):
            val_ref = float(alma_profilo[alma_profilo['anno']==anno_ref][col].values[0])
            fig_gauge.add_trace(go.Indicator(mode='gauge+number+delta', value=val_2025[col],
                delta={'reference': val_ref, 'suffix': '%', 'relative': False, 'increasing': {'color':'#14B8A6'}, 'decreasing': {'color':'#F87171'}},
                number={'suffix':'%','font':{'size':40,'color':colore}},
                title={'text':f"<b style='color:#F5F5F7'>{titolo}</b><br><span style='font-size:11px;color:#9CA3AF'>2025 vs {anno_ref}</span>"},
                gauge={'axis':{'range':[0,100],'ticksuffix':'%','tickfont':{'color':'#9CA3AF'},'tickcolor':'#9CA3AF'},
                    'bar':{'color':colore,'thickness':0.25},'bgcolor':BG_CARD,'borderwidth':0,
                    'steps':[{'range':[0,50],'color':BG_PLOT},{'range':[50,75],'color':'#133A3A'},{'range':[75,100],'color':'#1A4040'}],
                    'threshold':{'line':{'color':'#F59E0B','width':3},'thickness':0.75,'value':val_ref}},
                domain={'x':[col_idx*0.34, col_idx*0.34+0.30],'y':[0,1]}, visible=visible))
    n_per_anno = len(indicatori_gauge)
    buttons_gauge = []
    for i, anno_ref in enumerate(anni_ref):
        vis = []
        for j in range(len(anni_ref)): vis += [j==i]*n_per_anno
        buttons_gauge.append(dict(label=f'vs {anno_ref}', method='update',
            args=[{'visible': vis}, {'title': dict(text=f'Profilo laureati L-8 — 2025 vs {anno_ref}', font=dict(size=20, color='#F5F5F7', family='Inter'), x=0.5, xanchor='center')}]))
    fig_gauge.update_layout(title=dict(text='Profilo Laureati L-8 — 2025 vs 2024', font=dict(size=20, color='#F5F5F7', family='Inter'), x=0.5, xanchor='center'),
        updatemenus=[dict(type='buttons', direction='right', x=0.5, xanchor='center', y=1.55, yanchor='top',
            buttons=buttons_gauge, bgcolor=BG_CARD, bordercolor=VERDE_MAIN, borderwidth=1,
            font=dict(size=12, family='Inter', color='#F5F5F7'), active=len(anni_ref)-1, pad=dict(r=6,l=6,t=6,b=6))],
        height=420, margin=dict(t=195, b=60, l=30, r=30), font=dict(family='Inter', size=12), paper_bgcolor=BG_PAPER,
        annotations=[dict(x=0.5, y=-0.12, xref='paper', yref='paper', text="La linea arancione indica il valore dell'anno di riferimento selezionato",
                showarrow=False, font=dict(size=11, color='#9CA3AF'), align='center'),
            fonte_ann('Fonte: AlmaLaurea — Profilo dei Laureati L-8')])
    st.plotly_chart(fig_gauge, use_container_width=True)
    st.markdown("---")

    # G9 — Destinazione magistrale
    if alma_ok and not df_dest.empty:
        chart_header("Destinazione alla magistrale — dove proseguono gli studi",
            "Distribuzione percentuale degli studenti L-8 che si iscrivono alla laurea magistrale per destinazione geografica. 'Altro' include Sud-Isole, atenei telematici e atenei esteri.",
            "Passa il cursore sulle barre per vedere la percentuale esatta di ciascun segmento. Hover su 'Altro' per il dettaglio.")
        df_dest2 = df_dest.copy()
        df_dest2['Altro'] = df_dest2['Altro Sud-Isole'].fillna(0) + df_dest2['Telematico'].fillna(0) + df_dest2['Estero'].fillna(0)
        df_dest2['hover_altro'] = df_dest2.apply(lambda r: f"<b>Altro</b><br>Anno {r['anno']}<br>&nbsp;&nbsp;Sud-Isole: <b>{(r['Altro Sud-Isole'] or 0):.1f}%</b><br>&nbsp;&nbsp;Telematico: <b>{(r['Telematico'] or 0):.1f}%</b><br>&nbsp;&nbsp;Estero: <b>{(r['Estero'] or 0):.1f}%</b><br>Totale: <b>{r['Altro']:.1f}%</b>", axis=1)
        DEST_PLOT = {'Stesso Ateneo':'#14B8A6','Altro Nord':'#60A5FA','Altro Centro':'#FB923C','Altro':'#9CA3AF'}
        media_stesso = df_dest2['Stesso Ateneo'].mean()
        media_nord = df_dest2['Altro Nord'].mean()
        fig_dest = go.Figure()
        for col, colore in DEST_PLOT.items():
            if col == 'Altro':
                fig_dest.add_trace(go.Bar(x=df_dest2['anno'], y=df_dest2[col], name=col,
                    marker=dict(color=colore, line=dict(color='#041A1A', width=1), opacity=0.92),
                    text=df_dest2[col].apply(lambda x: f'{x:.1f}%'), textposition='inside',
                    textfont=dict(size=11, color='white', family='Inter'),
                    customdata=df_dest2['hover_altro'], hovertemplate='%{customdata}<extra></extra>'))
            else:
                fig_dest.add_trace(go.Bar(x=df_dest2['anno'], y=df_dest2[col], name=col,
                    marker=dict(color=colore, line=dict(color='#041A1A', width=1), opacity=0.92),
                    text=df_dest2[col].apply(lambda x: f'{x:.1f}%'), textposition='inside',
                    textfont=dict(size=11, color='white', family='Inter'),
                    hovertemplate=f'<b>{col}</b><br>Anno %{{x}}<br><b>%{{y:.1f}}%</b><extra></extra>'))
        fig_dest.update_layout(barmode='stack', bargap=0.20, font=dict(family='Inter', size=12), plot_bgcolor=BG_PLOT, paper_bgcolor=BG_PAPER,
            title=dict(text='Destinazione alla Magistrale — Laureati L-8 (2020–2025)', font=dict(size=18, color='#F5F5F7', family='Inter'), x=0.5, xanchor='center'),
            legend=dict(orientation='h', y=1.10, x=0.5, xanchor='center', bgcolor='rgba(0,0,0,0)', font=dict(color='#C8C8C8', size=12)),
            annotations=[dict(x=0.5, y=-0.20, xref='paper', yref='paper',
                    text=f"<b style='color:#14B8A6'>{media_stesso:.1f}%</b><span style='color:#C8C8C8'> resta nello stesso ateneo · </span><b style='color:#60A5FA'>{media_nord:.1f}%</b><span style='color:#C8C8C8'> sceglie un ateneo del Nord</span>",
                    showarrow=False, font=dict(size=12, family='Inter'), align='center'),
                dict(x=0.99, y=-0.26, xref='paper', yref='paper', text='Fonte: AlmaLaurea · "Altro" include Sud-Isole, Telematico, Estero',
                    showarrow=False, font=dict(size=10, color='#9CA3AF'), xanchor='right')],
            height=540, margin=dict(t=100, b=100, l=60, r=30))
        fig_dest.update_xaxes(title=dict(text='Anno di laurea', font=dict(color='#C8C8C8')), showgrid=False, tickfont=dict(color='#C8C8C8', size=14), linecolor='#2D5A5A')
        fig_dest.update_yaxes(title=dict(text='%', font=dict(color='#C8C8C8')), range=[0,100], ticksuffix='%', gridcolor='#1A3A3A', tickfont=dict(color='#C8C8C8'), linecolor='#2D5A5A')
        st.plotly_chart(fig_dest, use_container_width=True)
    else:
        st.info("Dati AlmaLaurea non disponibili per la destinazione magistrale.")

# ══════════════════════════════════════════════════════════════════════════════
# PERCORSO ACCADEMICO
# ══════════════════════════════════════════════════════════════════════════════
elif sezione == "Percorso Accademico":
    st.markdown("## Percorso Accademico")
    st.markdown("---")

    # G10 — Laureati
    chart_header("Laureati L-8 Ingegneria dell'Informazione — Italia (2010–2024)",
        "Numero totale di laureati per anno solare. Le barre rosse corrispondono agli anni 2020 e 2021, durante i quali le sessioni di laurea hanno subito variazioni legate all'emergenza sanitaria.",
        "Passa il cursore sulle barre per vedere il valore esatto.")
    lau_naz = mur_l_l8.groupby('AnnoS')['Lau'].sum().reset_index()
    lau_naz.columns = ['anno','laureati']
    lau_naz = lau_naz[lau_naz['anno'] >= 2010].reset_index(drop=True)
    lau_naz['covid'] = lau_naz['anno'].isin([2020,2021])
    primo = lau_naz[lau_naz['anno']==2010]['laureati'].values[0]
    ultimo_lau = lau_naz['laureati'].iloc[-1]
    crescita = (ultimo_lau - primo) / primo * 100
    fig_lau = go.Figure()
    fig_lau.add_trace(go.Bar(x=lau_naz['anno'], y=lau_naz['laureati'],
        marker=dict(color=['#F87171' if c else '#14B8A6' for c in lau_naz['covid']], line=dict(width=0), opacity=0.9, cornerradius=4),
        text=lau_naz['laureati'].apply(lambda x: f'{x:,.0f}'),
        textposition='outside', textfont=dict(size=10, color='#F5F5F7', family='Inter'),
        hovertemplate='<b>%{x}</b><br>Laureati: <b>%{y:,.0f}</b><extra></extra>', showlegend=False))
    fig_lau.update_layout(font=dict(family='Inter', size=12), plot_bgcolor=BG_PLOT, paper_bgcolor=BG_PAPER,
        title=dict(text="Laureati L-8 Ingegneria dell'Informazione — Italia (2010–2024)", font=dict(size=18, color='#F5F5F7', family='Inter'), x=0.5, xanchor='center'),
        showlegend=False,
        annotations=[dict(x=0.01, y=0.97, xref='paper', yref='paper',
                text=f"<b style='color:#14B8A6'>+{crescita:.0f}%</b><span style='color:#C8C8C8'> dal 2010 al 2024</span>",
                showarrow=False, font=dict(size=13, family='Inter'), align='left'),
            fonte_ann('Fonte: MUR-USTAT — Laureati L-8 per anno solare')],
        margin=dict(t=100, b=80, l=60, r=30), height=500)
    fig_lau.update_xaxes(showgrid=False, tickfont=dict(color='#C8C8C8', size=12), linecolor='#2D5A5A', tickmode='linear', dtick=1, tickangle=-45)
    fig_lau.update_yaxes(gridcolor='#1A3A3A', tickfont=dict(color='#C8C8C8'), linecolor='#2D5A5A', rangemode='tozero',
        title=dict(text='N° laureati', font=dict(color='#C8C8C8')), range=[0, lau_naz['laureati'].max()*1.18])
    st.plotly_chart(fig_lau, use_container_width=True)
    st.markdown("---")

    # G11 — Donut
    chart_header("Cosa succede dopo il primo anno — iC14 + iC21",
        "Il grafico mostra la distribuzione degli immatricolati puri L-8 al termine del primo anno: chi prosegue nello stesso corso (iC14 ANVUR), chi cambia corso o ateneo ma resta nel sistema universitario (differenza iC21-iC14), e chi lascia l'università (complemento a 1 di iC21).",
        "Seleziona l'anno con i pulsanti. Passa il cursore sulle fette per vedere le percentuali esatte.")
    anni_donut = sorted(df_destino['anno'].unique())
    fig_donut = go.Figure()
    for i, anno in enumerate(anni_donut):
        row = df_destino[df_destino['anno']==anno].iloc[0]
        fig_donut.add_trace(go.Pie(labels=['Proseguono nello stesso corso','Cambiano corso o ateneo',"Lasciano l'università"],
            values=[row['prosegue_stesso'], row['cambia_corso'], row['abbandona']], hole=0.60,
            marker=dict(colors=['#14B8A6','#F59E0B','#F87171'], line=dict(color='#041A1A', width=3)),
            textinfo='percent', textposition='outside', textfont=dict(size=13, color='#F5F5F7', family='Inter'),
            hovertemplate='<b>%{label}</b><br><b>%{value:.1f}%</b> degli immatricolati puri<extra></extra>',
            visible=(i==0), sort=False, pull=[0.03,0.03,0.03]))
    buttons_donut = []
    for i, anno in enumerate(anni_donut):
        row = df_destino[df_destino['anno']==anno].iloc[0]
        vis = [j==i for j in range(len(anni_donut))]
        buttons_donut.append(dict(label=anno, method='update',
            args=[{'visible': vis}, {'title': dict(text=f"Cosa succede dopo il primo anno — L-8 {anno}", font=dict(size=18, color='#F5F5F7', family='Inter'), x=0.5, xanchor='center'),
                'annotations': [dict(text=f"<b>{row['prosegue_stesso']:.1f}%</b><br><span style='color:#C8C8C8;font-size:11px'>resta nello<br>stesso corso</span>",
                        x=0.5, y=0.5, xref='paper', yref='paper', showarrow=False, font=dict(size=24, color='white', family='Inter'), align='center'),
                    dict(x=0.99, y=-0.08, xref='paper', yref='paper', text='Fonte: ANVUR iC14 + iC21 · Media nazionale corsi L-8',
                        showarrow=False, font=dict(size=10, color='#9CA3AF'), align='right', xanchor='right')]}]))
    row0 = df_destino[df_destino['anno']==anni_donut[0]].iloc[0]
    fig_donut.update_layout(title=dict(text=f"Cosa succede dopo il primo anno — L-8 {anni_donut[0]}", font=dict(size=18, color='#F5F5F7', family='Inter'), x=0.5, xanchor='center'),
        updatemenus=[dict(type='buttons', direction='right', x=0.5, xanchor='center', y=1.12, yanchor='top',
            buttons=buttons_donut, bgcolor=BG_CARD, bordercolor=VERDE_MAIN, borderwidth=1,
            font=dict(size=12, family='Inter', color='#F5F5F7'), active=0, pad=dict(r=6,l=6,t=6,b=6))],
        annotations=[dict(text=f"<b>{row0['prosegue_stesso']:.1f}%</b><br><span style='color:#C8C8C8;font-size:11px'>resta nello<br>stesso corso</span>",
                x=0.5, y=0.5, xref='paper', yref='paper', showarrow=False, font=dict(size=24, color='white', family='Inter'), align='center'),
            dict(x=0.99, y=-0.08, xref='paper', yref='paper', text='Fonte: ANVUR iC14 + iC21 · Media nazionale corsi L-8',
                showarrow=False, font=dict(size=10, color='#9CA3AF'), align='right', xanchor='right')],
        height=560, margin=dict(t=120, b=80, l=80, r=80), font=dict(family='Inter', size=12), paper_bgcolor=BG_PAPER, showlegend=True,
        legend=dict(font=dict(color='#C8C8C8', size=12), bgcolor='rgba(0,0,0,0)', orientation='h', x=0.5, xanchor='center', y=-0.08))
    st.plotly_chart(fig_donut, use_container_width=True)
    st.markdown("---")

    # G12 — iC02
    chart_header("% Laureati entro la durata normale del corso — iC02",
        "Percentuale media nazionale di studenti L-8 che si laureano entro i tempi standard previsti dal corso. Il dato più recente è evidenziato in verde chiaro.",
        "Passa il cursore sulle barre per vedere il valore esatto per anno.")
    ic02_clean = ic02[ic02['Numeratore'] <= 100].copy()
    ic02_naz = ic02_clean.groupby('Anno accademico')['Numeratore'].mean().reset_index()
    ic02_naz.columns = ['anno','pct']
    ic02_naz['pct'] = ic02_naz['pct'].round(1)
    media_ic02 = ic02_naz['pct'].mean()
    fig_ic02 = go.Figure()
    for _, row in ic02_naz.iterrows():
        colore = VERDE_LIGHT if row['anno']==ic02_naz['anno'].max() else VERDE_MAIN
        fig_ic02.add_trace(go.Bar(x=[row['pct']], y=[str(int(row['anno']))], orientation='h',
            marker=dict(color=colore, cornerradius=4, line=dict(width=0)),
            text=f"{row['pct']:.1f}%", textposition='outside',
            textfont=dict(color='#F5F5F7', size=13),
            hovertemplate=f"<b>{int(row['anno'])}</b><br>Laureati in corso: <b>{row['pct']:.1f}%</b><extra></extra>",
            showlegend=False, width=0.5))
    fig_ic02.add_trace(go.Scatter(x=[media_ic02, media_ic02], y=[str(int(ic02_naz['anno'].min())), str(int(ic02_naz['anno'].max()))],
        mode='lines', line=dict(color='#F59E0B', width=2, dash='dash'), name=f'Media: {media_ic02:.1f}%', hoverinfo='skip'))
    fig_ic02.update_layout(font=dict(family='Inter', size=12), plot_bgcolor=BG_PLOT, paper_bgcolor=BG_PAPER,
        title=dict(text='% Laureati entro la Durata Normale — iC02 L-8', font=dict(size=18, color='#F5F5F7', family='Inter'), x=0.5, xanchor='center'),
        showlegend=True, legend=dict(font=dict(color='#C8C8C8', size=11), bgcolor='rgba(0,0,0,0)', orientation='h', x=0.5, xanchor='center', y=1.08),
        barmode='overlay', margin=dict(t=100, b=80, l=80, r=120), height=420,
        annotations=[dict(x=media_ic02, y=1.02, xref='x', yref='paper', text=f'Media: {media_ic02:.1f}%',
                showarrow=False, font=dict(size=11, color='#F59E0B'), align='center'),
            fonte_ann('Fonte: ANVUR — % laureati entro durata normale (iC02) · Esclusi valori >100%')])
    fig_ic02.update_xaxes(showgrid=False, tickfont=dict(color='#C8C8C8'), linecolor='#2D5A5A', ticksuffix='%', range=[0, 50])
    fig_ic02.update_yaxes(tickfont=dict(color='#C8C8C8', size=13), linecolor='#2D5A5A')
    st.plotly_chart(fig_ic02, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# VARIANTI DEL CORSO
# ══════════════════════════════════════════════════════════════════════════════
elif sezione == "Varianti del Corso":
    st.markdown("## Varianti del Corso")
    st.markdown("---")
    chart_header("Tasso di prosecuzione al II anno per famiglia di corso — iC14",
        "Confronto del tasso medio di prosecuzione al II anno (iC14 ANVUR) per ciascuna macro-famiglia di corso L-8, usando 'Informatica' come baseline. Verde = superiore alla baseline, rosso = inferiore.",
        "Passa il cursore sulle barre per vedere il tasso di abbandono e il numero di atenei. Hover su Multidisciplinare per le varianti incluse.")
    ic14_var = merge14_var.groupby('macro_famiglia')['perc_iC14'].mean().reset_index()
    ic14_var.columns = ['famiglia','prosecuzione']
    ic14_var['prosecuzione'] = ic14_var['prosecuzione'].round(1)
    ic14_var['abbandono'] = (100 - ic14_var['prosecuzione']).round(1)
    n_atenei_var = merge14_var.groupby('macro_famiglia')['Ateneo'].nunique().reset_index()
    n_atenei_var.columns = ['famiglia','n_atenei']
    ic14_var = ic14_var.merge(n_atenei_var, on='famiglia').sort_values('prosecuzione', ascending=True).reset_index(drop=True)
    multi_detail = merge14_var[merge14_var['macro_famiglia']=='Multidisciplinare']\
        .groupby('corso_pulito').agg(pct=('perc_iC14','mean'), n_at=('Ateneo','nunique')).round(1).sort_values('pct', ascending=False).reset_index()
    hover_multi = "<b>Multidisciplinare</b><br>Varianti incluse:<br>" + "<br>".join([f"&nbsp;&nbsp;• {row['corso_pulito']}: <b>{row['pct']:.1f}%</b> ({row['n_at']} atenei)" for _, row in multi_detail.iterrows()])
    baseline_val = ic14_var[ic14_var['famiglia']=='Informatica']['prosecuzione'].values
    baseline = baseline_val[0] if len(baseline_val) > 0 else 65.0
    def get_colore_var(row):
        if row['famiglia'] == 'Informatica': return '#9CA3AF'
        elif row['prosecuzione'] > baseline: return '#14B8A6'
        else: return '#F87171'
    ic14_var['colore'] = ic14_var.apply(get_colore_var, axis=1)
    def build_hover_var(row):
        if row['famiglia'] == 'Multidisciplinare': return hover_multi
        return f"<b>{row['famiglia']}</b><br>Prosecuzione: <b>{row['prosecuzione']:.1f}%</b><br>Abbandono: <b>{row['abbandono']:.1f}%</b><br>N° atenei: <b>{row['n_atenei']}</b>"
    ic14_var['hover'] = ic14_var.apply(build_hover_var, axis=1)
    fig_var = go.Figure()
    fig_var.add_trace(go.Bar(x=ic14_var['prosecuzione'], y=ic14_var['famiglia'], orientation='h',
        marker=dict(color=ic14_var['colore'], line=dict(width=0), opacity=0.9, cornerradius=4),
        text=ic14_var.apply(lambda r: f"{r['prosecuzione']:.1f}%  ({r['n_atenei']} aten{'eo' if r['n_atenei']==1 else 'ei'})", axis=1),
        textposition='outside', textfont=dict(size=11, color='#C8C8C8'),
        customdata=ic14_var['hover'], hovertemplate='%{customdata}<extra></extra>'))
    fig_var.add_vline(x=baseline, line=dict(color='#9CA3AF', width=2, dash='dash'))
    fig_var.update_layout(font=dict(family='Inter', size=12), plot_bgcolor=BG_PLOT, paper_bgcolor=BG_PAPER,
        title=dict(text='Tasso di Prosecuzione per Famiglia di Corso — iC14 L-8', font=dict(size=18, color='#F5F5F7', family='Inter'), x=0.5, xanchor='center'),
        annotations=[dict(x=baseline, y=1.02, xref='x', yref='paper', text=f'Baseline Informatica: {baseline:.1f}%',
                showarrow=False, font=dict(size=10, color='#9CA3AF'), align='center'),
            dict(x=0.5, y=-0.20, xref='paper', yref='paper',
                text="<b style='color:#14B8A6'>Verde</b> = sopra baseline · <b style='color:#F87171'>Rosso</b> = sotto baseline · Hover su Multidisciplinare per le varianti",
                showarrow=False, font=dict(size=11, color='#C8C8C8'), align='center'),
            dict(x=0.99, y=-0.26, xref='paper', yref='paper', text='Fonte: ANVUR iC14 · Media 2020–2024 per famiglia di corso',
                showarrow=False, font=dict(size=10, color='#9CA3AF'), xanchor='right')],
        height=520, margin=dict(t=80, b=100, l=160, r=180))
    fig_var.update_xaxes(title=dict(text='% prosecuzione al II anno', font=dict(color='#C8C8C8')), showgrid=False, ticksuffix='%', tickfont=dict(color='#C8C8C8'), linecolor='#2D5A5A', range=[0, 100])
    fig_var.update_yaxes(showgrid=False, tickfont=dict(size=12, color='#C8C8C8'), linecolor='#2D5A5A')
    st.plotly_chart(fig_var, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TASSE E CONTRIBUTI
# ══════════════════════════════════════════════════════════════════════════════
elif sezione == "Tasse e Contributi":
    st.markdown("## Tasse e Contributi")
    st.markdown("---")
    chart_header("Contributo massimo annuo — L-8 Ingegneria dell'Informazione",
        "Il grafico confronta il contributo onnicomprensivo massimo annuo (fascia ISEE più alta) per un campione di atenei statali e non statali. I colori indicano la macro area geografica. Le linee tratteggiate rosse indicano gli atenei non statali.",
        "Passa il cursore sulle barre per vedere il contributo esatto. Le linee orizzontali indicano il contributo degli atenei non statali.")
    statali_t = tasse[tasse['Tipo']=='Statale'].sort_values('Contributo max', ascending=False).reset_index(drop=True)
    non_statali_t = tasse[tasse['Tipo']=='Non Statale'].sort_values('Contributo max', ascending=False).reset_index(drop=True)
    media_statali_t = statali_t['Contributo max'].mean()
    def get_macro_t(ateneo):
        nord   = ['Politecnico Milano','Politecnico Torino','Università di Padova','Università di Bologna','Politecnica delle Marche']
        centro = ['Sapienza','Roma 3','Tor Vergata']
        sud    = ['Federico II','Politecnico di Bari']
        for n in nord:
            if n.lower() in ateneo.lower(): return 'Nord'
        for c in centro:
            if c.lower() in ateneo.lower(): return 'Centro'
        for s in sud:
            if s.lower() in ateneo.lower(): return 'Sud'
        return 'Nord'
    statali_t = statali_t.copy()
    statali_t['Macro'] = statali_t['Ateneo'].apply(get_macro_t)
    max_row_t = statali_t.iloc[0]
    min_row_t = statali_t.iloc[-1]
    n_t = len(statali_t)
    C_NONST_T = '#F87171'; C_TESTO_T = '#C8C8C8'; C_TESTO2_T = '#D1D5DB'; C_GRIGIO_T = '#6B7280'
    COLORI_MACRO_T = {'Nord': '#3B82F6', 'Centro': '#10B981', 'Sud': '#F59E0B'}
    fig_tasse_chart = make_subplots(rows=2, cols=1, row_heights=[0.28, 0.72], vertical_spacing=0.04, specs=[[{'type':'xy'}],[{'type':'xy'}]])
    fig_tasse_chart.add_trace(go.Scatter(x=[0], y=[0], mode='markers', marker=dict(opacity=0), showlegend=False, hoverinfo='skip'), row=1, col=1)
    for macro in ['Nord','Centro','Sud']:
        sub = statali_t[statali_t['Macro']==macro]
        if len(sub) > 0:
            fig_tasse_chart.add_trace(go.Bar(x=sub['Ateneo'], y=sub['Contributo max'], name=macro,
                marker=dict(color=COLORI_MACRO_T[macro], line=dict(width=0), opacity=0.9, cornerradius=4),
                text=sub['Contributo max'].apply(lambda v: f'€{v:,.0f}'.replace(',','.')),
                textposition='outside', textfont=dict(color=C_TESTO_T, size=11, family='Inter'),
                hovertemplate='<b>%{x}</b><br>Contributo max: <b>€%{y:,.0f}</b><extra></extra>'), row=2, col=1)
    colori_ns = ['#F87171','#FCA5A5']
    for i, (_, row) in enumerate(non_statali_t.iterrows()):
        fig_tasse_chart.add_trace(go.Scatter(x=[-0.5, n_t-0.5], y=[row['Contributo max'], row['Contributo max']],
            mode='lines', name=row['Ateneo'].strip(),
            line=dict(color=colori_ns[i % len(colori_ns)], width=2.5, dash='dash'),
            showlegend=True, xaxis='x3', yaxis='y2',
            hovertemplate=f"<b>{row['Ateneo'].strip()}: €{row['Contributo max']:,.0f}</b><extra></extra>"))
    fig_tasse_chart.add_trace(go.Scatter(x=[-0.5, n_t-0.5], y=[media_statali_t, media_statali_t],
        mode='lines', name='Media statali', line=dict(color=C_TESTO2_T, width=2, dash='dot'),
        showlegend=False, xaxis='x3', yaxis='y2', hoverinfo='skip'))
    cards_t = [
        {'titolo': 'STATALE PIÙ CARO', 'valore': f"€{max_row_t['Contributo max']:,.0f}".replace(',','.'),
         'sub1': max_row_t['Ateneo'].strip(), 'sub2': f"Macro area: {max_row_t['Macro']}", 'colore': COLORI_MACRO_T.get(max_row_t['Macro'], '#3B82F6')},
        {'titolo': 'MEDIA STATALI', 'valore': f"€{media_statali_t:,.0f}".replace(',','.'),
         'sub1': f'{n_t} atenei nel campione', 'sub2': 'su 48 atenei L-8 totali', 'colore': C_GRIGIO_T},
        {'titolo': 'STATALE MENO CARO', 'valore': f"€{min_row_t['Contributo max']:,.0f}".replace(',','.'),
         'sub1': min_row_t['Ateneo'].strip(), 'sub2': f"Macro area: {min_row_t['Macro']}", 'colore': COLORI_MACRO_T.get(min_row_t['Macro'], '#10B981')},
    ]
    shapes_t = []; annotations_t = []
    card_y0_t=0.76; card_y1_t=0.99; gaps_t=[0.01,0.34,0.67]; card_w_t=0.31
    for i_t, card_t in enumerate(cards_t):
        x0_t=gaps_t[i_t]; x1_t=x0_t+card_w_t; cx_t=(x0_t+x1_t)/2; cy_t=(card_y0_t+card_y1_t)/2
        shapes_t.append(dict(type='rect', xref='paper', yref='paper', x0=x0_t, x1=x1_t, y0=card_y0_t, y1=card_y1_t, fillcolor=BG_CARD, line=dict(color=card_t['colore'], width=2.5), layer='below', opacity=1))
        shapes_t.append(dict(type='rect', xref='paper', yref='paper', x0=x0_t, x1=x1_t, y0=card_y1_t-0.032, y1=card_y1_t, fillcolor=card_t['colore'], line=dict(width=0), layer='above', opacity=1))
        annotations_t.append(dict(x=cx_t, y=card_y1_t-0.02, xref='paper', yref='paper', text=f"<b>{card_t['titolo']}</b>", font=dict(size=13, color='white', family='Inter'), showarrow=False, xanchor='center', yanchor='middle'))
        annotations_t.append(dict(x=cx_t, y=cy_t+0.055, xref='paper', yref='paper', text=f"<b>{card_t['valore']}</b>", font=dict(size=36, color=card_t['colore'], family='Inter'), showarrow=False, xanchor='center', yanchor='middle'))
        annotations_t.append(dict(x=cx_t, y=cy_t-0.04, xref='paper', yref='paper', text=f"<b>{card_t['sub1']}</b>", font=dict(size=13, color='#F5F5F7', family='Inter'), showarrow=False, xanchor='center', yanchor='middle'))
        annotations_t.append(dict(x=cx_t, y=card_y0_t+0.025, xref='paper', yref='paper', text=card_t['sub2'], font=dict(size=12, color=C_TESTO2_T, family='Inter'), showarrow=False, xanchor='center', yanchor='bottom'))
    for i, (_, row) in enumerate(non_statali_t.iterrows()):
        annotations_t.append(dict(x=0.5, y=row['Contributo max'], xref='paper', yref='y2',
            text=f"<b>{row['Ateneo'].strip()} (non statale): €{row['Contributo max']:,.0f}</b>".replace(',','.'),
            showarrow=False, font=dict(size=13, color=colori_ns[i % len(colori_ns)], family='Inter'),
            xanchor='center', yanchor='bottom', yshift=10,
            bgcolor='rgba(7,26,13,0.92)', bordercolor=colori_ns[i % len(colori_ns)], borderwidth=1.5, borderpad=12))
    annotations_t.append(dict(x=0.99, y=media_statali_t, xref='paper', yref='y2',
        text=f"<b>Media statali: €{media_statali_t:,.0f}</b>".replace(',','.'),
        showarrow=False, font=dict(size=13, color=C_TESTO2_T, family='Inter'),
        xanchor='right', yanchor='bottom', yshift=8, bgcolor='rgba(7,26,13,0.9)', borderpad=8))
    annotations_t.append(dict(x=0.99, y=-0.08, xref='paper', yref='paper',
        text='Fonte: siti ufficiali atenei · Contributo massimo a.a. 2025/26 · Fascia ISEE più alta · Escluse telematiche',
        showarrow=False, font=dict(size=10, color='#9CA3AF', family='Inter'), align='right', xanchor='right'))
    fig_tasse_chart.update_layout(title=dict(text="Contributo Massimo Annuo — L-8 Ingegneria dell'Informazione",
            font=dict(size=20, color='white', family='Inter'), x=0.5, xanchor='center'),
        shapes=shapes_t, annotations=annotations_t, barmode='group', plot_bgcolor=BG_PAPER, paper_bgcolor=BG_PAPER,
        font=dict(family='Inter', size=12), legend=dict(font=dict(color=C_TESTO_T, size=12), bgcolor='rgba(0,0,0,0)',
            orientation='h', x=0.5, xanchor='center', y=0.73),
        height=800, margin=dict(t=80, b=80, l=20, r=20), xaxis3=dict(overlaying='x2', range=[-0.5, n_t-0.5], visible=False, anchor='y2'))
    fig_tasse_chart.update_xaxes(visible=False, row=1, col=1)
    fig_tasse_chart.update_yaxes(visible=False, row=1, col=1)
    fig_tasse_chart.update_xaxes(showgrid=False, tickfont=dict(color=C_TESTO_T, size=11), linecolor='#2D5A5A', tickangle=-20, row=2, col=1)
    fig_tasse_chart.update_yaxes(showgrid=True, gridcolor='#1A3A3A', tickfont=dict(color=C_TESTO2_T), linecolor='#2D5A5A', tickprefix='€', range=[0, tasse['Contributo max'].max()*1.2], row=2, col=1)
    st.plotly_chart(fig_tasse_chart, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# ANALISI AVANZATA
# ══════════════════════════════════════════════════════════════════════════════
elif sezione == "Analisi Avanzata":
    st.markdown("## Analisi Avanzata")
    st.markdown("---")

    # G15 — Radiale iC16BIS
    chart_header("Studenti al II anno con ≥ 2/3 CFU — iC16BIS",
        "Grafico radiale che mostra la percentuale media nazionale di studenti che al II anno hanno acquisito almeno 2/3 dei CFU previsti (indicatore iC16BIS ANVUR). Ogni arco rappresenta un anno accademico.",
        "Passa il cursore sugli archi per vedere il valore per anno.")
    anni_ic16 = ic16_naz['anno'].tolist()
    valori_ic16 = ic16_naz['pct'].tolist()
    media_ic16 = ic16_naz['pct'].mean()
    colori_radial = ['#99F6E4','#2DD4BF'','#FACC15','#EAB308','#CA8A04']
    fig_radial = go.Figure()
    for i, (anno, val) in enumerate(zip(anni_ic16, valori_ic16)):
        raggio_interno = 0.55 + i*0.07
        raggio_esterno = raggio_interno + 0.055
        theta = np.linspace(0, val/100*360, 100)
        theta_rad = np.radians(theta)
        x_outer = raggio_esterno * np.cos(theta_rad)
        y_outer = raggio_esterno * np.sin(theta_rad)
        x_inner = raggio_interno * np.cos(theta_rad[::-1])
        y_inner = raggio_interno * np.sin(theta_rad[::-1])
        c = colori_radial[i % len(colori_radial)]
        fig_radial.add_trace(go.Scatter(x=np.concatenate([x_outer, x_inner]), y=np.concatenate([y_outer, y_inner]),
            fill='toself', fillcolor=c, line=dict(color=c, width=0), name=f'{anno}: {val:.1f}%',
            hovertemplate=f'<b>{anno}</b><br>iC16BIS: <b>{val:.1f}%</b><extra></extra>', mode='lines'))
        angolo_label = np.radians(val/100*360 + 3)
        r_label = raggio_esterno + 0.04
        fig_radial.add_annotation(x=r_label*np.cos(angolo_label), y=r_label*np.sin(angolo_label),
            text=f'{val:.1f}%', showarrow=False, font=dict(size=11, color=c, family='Inter'))
    fig_radial.update_layout(font=dict(family='Inter', size=12), plot_bgcolor=BG_PLOT, paper_bgcolor=BG_PAPER,
        title=dict(text='Studenti al II Anno con ≥ 2/3 CFU — iC16BIS L-8', font=dict(size=18, color='#F5F5F7', family='Inter'), x=0.5, xanchor='center'),
        showlegend=True, legend=dict(font=dict(color='#C8C8C8', size=11), bgcolor='rgba(0,0,0,0)', orientation='v', x=1.02, y=0.5, xanchor='left'),
        xaxis=dict(visible=False, range=[-1.3, 1.5]), yaxis=dict(visible=False, range=[-1.3, 1.3]),
        margin=dict(t=100, b=60, l=60, r=150), height=520,
        annotations=[dict(x=0, y=0.05, text=f'<b>{media_ic16:.1f}%</b>', showarrow=False, font=dict(size=26, color='white', family='Inter')),
            dict(x=0, y=-0.12, text='media nazionale', showarrow=False, font=dict(size=11, color='#C8C8C8', family='Inter')),
            dict(x=0.99, y=-0.08, xref='paper', yref='paper', text='Fonte: ANVUR Cruscotto PENTAHO — iC16BIS',
                showarrow=False, font=dict(size=10, color='#9CA3AF'), xanchor='right')])
    st.plotly_chart(fig_radial, use_container_width=True)
    st.markdown("---")

    # G16 — Scatter correlazione
    chart_header("Correlazione tra dimensione del corso e tasso di prosecuzione",
        "L'analisi mette in relazione il numero medio di immatricolati puri per corso (2020–2024) con il tasso di prosecuzione al II anno (iC14 ANVUR). I corsi telematici (◆ rosa) sono separati dalla regressione lineare sui soli corsi tradizionali.",
        "Passa il cursore sui punti per vedere il nome del corso e dell'ateneo.")
    imm_corso = ic00b[ic00b['Anno accademico']<=2024].groupby(['Ateneo','Nome Corso'])['Numeratore'].mean().reset_index()
    imm_corso.columns = ['Ateneo','Nome Corso','imm_media']
    ic14_corso = merge14_var.groupby(['Ateneo','Nome Corso'])['perc_iC14'].mean().reset_index()
    ic14_corso.columns = ['Ateneo','Nome Corso','prosecuzione']
    df_corr = imm_corso.merge(ic14_corso, on=['Ateneo','Nome Corso'])
    df_corr['macro'] = df_corr['Ateneo'].map(ATENEO_REG_L8).map(REGIONE_MACRO)
    df_corr['corso_pulito'] = df_corr['Nome Corso'].str.split(' - ', n=1).str[1].str.strip()\
        .str.encode('latin-1', errors='replace').str.decode('utf-8', errors='replace').str.title().str.strip()
    df_corr['label'] = df_corr['corso_pulito'] + ' — ' + df_corr['Ateneo']
    df_corr = df_corr.dropna(subset=['imm_media','prosecuzione','macro'])
    df_corr['is_telematica'] = df_corr['Ateneo'].isin(TELEMATICHE_LIST)
    df_trad = df_corr[~df_corr['is_telematica']].copy()
    df_tele = df_corr[df_corr['is_telematica']].copy()
    if len(df_trad) > 1:
        slope, intercept, r, p, se = stats.linregress(df_trad['imm_media'], df_trad['prosecuzione'])
        x_line = [df_trad['imm_media'].min(), df_trad['imm_media'].max()]
        y_line = [slope*x + intercept for x in x_line]
    else:
        r, p = 0, 1; x_line, y_line = [], []
    COLORI_MACRO_SCATTER = {'Nord':'#3B82F6','Centro':'#10B981','Sud':'#F59E0B','Isole':'#8B5CF6'}
    fig_corr = go.Figure()
    for macro, colore in COLORI_MACRO_SCATTER.items():
        sub = df_trad[df_trad['macro']==macro]
        if len(sub) > 0:
            fig_corr.add_trace(go.Scatter(x=sub['imm_media'], y=sub['prosecuzione'], mode='markers', name=macro,
                marker=dict(color=colore, size=10, opacity=0.85, line=dict(color='#041A1A', width=1.5)),
                hovertemplate='<b>%{customdata}</b><br>Immatricolati medi: <b>%{x:.0f}</b><br>Prosecuzione: <b>%{y:.1f}%</b><extra></extra>',
                customdata=sub['label'].values))
    if len(df_tele) > 0:
        fig_corr.add_trace(go.Scatter(x=df_tele['imm_media'], y=df_tele['prosecuzione'], mode='markers', name='Telematiche',
            marker=dict(color='#F472B6', size=10, opacity=0.85, symbol='diamond', line=dict(color='#041A1A', width=1.5)),
            hovertemplate='<b>%{customdata}</b><br>Immatricolati medi: <b>%{x:.0f}</b><br>Prosecuzione: <b>%{y:.1f}%</b><extra></extra>',
            customdata=df_tele['label'].values))
    if len(x_line) > 0:
        fig_corr.add_trace(go.Scatter(x=x_line, y=y_line, mode='lines', name='Trend (tradizionali)',
            line=dict(color='#9CA3AF', width=1.5, dash='dash'), hoverinfo='skip'))
    fig_corr.update_layout(font=dict(family='Inter', size=12), plot_bgcolor=BG_PLOT, paper_bgcolor=BG_PAPER,
        title=dict(text='Correlazione Dimensione Corso vs Tasso di Prosecuzione — L-8', font=dict(size=18, color='#F5F5F7', family='Inter'), x=0.5, xanchor='center'),
        annotations=[dict(x=0.98, y=0.98, xref='paper', yref='paper',
                text=f'r = {r:.3f} · p = {p:.3f} · n = {len(df_trad)} (tradizionali)',
                showarrow=False, font=dict(size=12, color='#C8C8C8'), align='right', xanchor='right', bgcolor=BG_CARD, bordercolor='#2D5A5A', borderwidth=1),
            dict(x=0.99, y=-0.10, xref='paper', yref='paper', text='Fonte: ANVUR iC00b + iC14 · Ogni punto = un corso · Media 2020–2024 · ◆ = Telematiche',
                showarrow=False, font=dict(size=10, color='#9CA3AF'), xanchor='right')],
        legend=dict(font=dict(color='#C8C8C8'), bgcolor='rgba(0,0,0,0)', x=0.01, y=0.01),
        height=540, margin=dict(t=80, b=80, l=70, r=30))
    fig_corr.update_xaxes(title=dict(text='Immatricolati medi per anno (2020–2024)', font=dict(color='#C8C8C8')), showgrid=True, gridcolor='#1A3A3A', tickfont=dict(color='#C8C8C8'), linecolor='#2D5A5A', rangemode='tozero')
    fig_corr.update_yaxes(title=dict(text='Tasso prosecuzione al II anno (%)', font=dict(color='#C8C8C8')), showgrid=True, gridcolor='#1A3A3A', ticksuffix='%', tickfont=dict(color='#C8C8C8'), linecolor='#2D5A5A')
    st.plotly_chart(fig_corr, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# SINTESI
# ══════════════════════════════════════════════════════════════════════════════
elif sezione == "Sintesi":
    st.markdown("# Sintesi dell'Analisi")
    st.markdown("---")
    chart_header("Scorecard — indicatori chiave per il sistema L-8", "", "")
    avvi_2025 = int(df[(df['ID Indicatore'] == 'iC00a') & (df['Anno accademico'] == 2025)]['Numeratore'].sum())
    n_atenei = df['Ateneo'].nunique()
    try:
        iscritti_2025 = int(mur_i_l8[mur_i_l8['AnnoA'] == '2024/2025']['Isc'].sum())
    except:
        iscritti_2025 = int(mur_i_l8.groupby('AnnoA')['Isc'].sum().iloc[-1])
    try:
        lau_2024 = int(mur_l_l8[mur_l_l8['AnnoS'] == 2024]['Lau'].sum())
    except:
        lau_2024 = int(mur_l_l8.groupby('AnnoS')['Lau'].sum().iloc[-1])
    lau_2010 = int(mur_l_l8[mur_l_l8['AnnoS'] == 2010]['Lau'].sum()) if 2010 in mur_l_l8['AnnoS'].values else 0
    crescita_lau = (lau_2024 - lau_2010) / lau_2010 * 100 if lau_2010 > 0 else 0
    kpi_full = [
        {'label':'Avvii di carriera 2025','value':f'{avvi_2025:,}','delta':'trend crescita 2020-2025','color':'#2DD4BF'','bg':'#134E4A'},
        {'label':'Crescita laureati','value':f'+{crescita_lau:.0f}%','delta':'2010 → 2024','color':'#2DD4BF'','bg':'#134E4A'},
        {'label':'Soddisfatti del corso','value':'88.7%','delta':'AlmaLaurea 2025','color':'#34D399','bg':'#064E3B'},
        {'label':'Prosegue magistrale','value':'82.7%','delta':'AlmaLaurea 2025','color':'#34D399','bg':'#064E3B'},
        {'label':'Retribuzione media 2025','value':'€1.327','delta':'+17% vs 2020','color':'#34D399','bg':'#064E3B'},
        {'label':'Occupazione a 1 anno','value':'36.1%','delta':'82.7% fa magistrale','color':'#FCD34D','bg':'#78350F'},
        {'label':'Quota Centro Italia','value':'27%','delta':'11 atenei attivi','color':'#FCD34D','bg':'#78350F'},
        {'label':'Atenei telematici L-8','value':str(len(TELEMATICHE_LIST)),'delta':'su 53 atenei totali','color':'#34D399','bg':'#064E3B'},
    ]
    fig7 = go.Figure()
    col_positions = [0.01,0.26,0.51,0.76]
    row_positions = [0.52,0.02]
    shapes = []; annotations = []
    for idx, k in enumerate(kpi_full):
        r = idx // 4; c = idx % 4
        x0=col_positions[c]; x1=x0+0.23; y0=row_positions[r]; y1=y0+0.44; cx=(x0+x1)/2
        shapes.append(dict(type='rect',xref='paper',yref='paper',x0=x0,x1=x1,y0=y0,y1=y1,fillcolor=k['bg'],line=dict(color=k['color'],width=1.5),layer='below'))
        shapes.append(dict(type='rect',xref='paper',yref='paper',x0=x0,x1=x1,y0=y1-0.025,y1=y1,fillcolor=k['color'],line=dict(width=0),layer='above'))
        annotations.append(dict(x=cx,y=y1-0.048,xref='paper',yref='paper',text=f"<b>{k['label']}</b>",showarrow=False,font=dict(size=11,color='white',family='Inter'),align='center',xanchor='center'))
        annotations.append(dict(x=cx,y=(y0+y1)/2+0.04,xref='paper',yref='paper',text=f"<b>{k['value']}</b>",showarrow=False,font=dict(size=30,color=k['color'],family='Inter'),align='center',xanchor='center'))
        annotations.append(dict(x=cx,y=y0+0.055,xref='paper',yref='paper',text=k['delta'],showarrow=False,font=dict(size=10,color='#C8C8C8',family='Inter'),align='center',xanchor='center'))
    fig7.update_layout(title=dict(text="Scorecard L-8 Ingegneria dell'Informazione",font=dict(size=18,color='white',family='Inter'),x=0.5,xanchor='center'),
        shapes=shapes,annotations=annotations,height=600,margin=dict(t=80,b=40,l=20,r=20),
        paper_bgcolor=BG_PAPER,plot_bgcolor=BG_PAPER,xaxis=dict(visible=False,range=[0,1]),yaxis=dict(visible=False,range=[0,1]))
    st.plotly_chart(fig7, use_container_width=True)
    st.markdown("---")
    st.markdown("## Considerazioni principali")
    st.markdown(f"""<div class="section-card"><p><b style="color:#F5F5F7">Domanda e offerta formativa.</b> In Italia sono <b style="color:#14B8A6">{n_atenei} gli atenei</b> che offrono corsi L-8 Ingegneria dell'Informazione, inclusi <b style="color:#14B8A6">{len(TELEMATICHE_LIST)} atenei telematici</b>. Gli avvii di carriera al primo anno si attestano a <b style="color:#F5F5F7">{avvi_2025:,}</b> nell'anno accademico 2024/25, in crescita rispetto al periodo post-pandemia.</p></div>""", unsafe_allow_html=True)
    st.markdown("""<div class="section-card"><p><b style="color:#F5F5F7">Distribuzione geografica.</b> Il <b style="color:#3B82F6">Nord Italia</b> concentra il 50–55% degli avvii di carriera, trainato dai Politecnici di Milano e Torino. Il <b style="color:#10B981">Centro Italia</b> conta 11 atenei attivi con circa il 27% degli avvii, forte grazie a La Sapienza e agli atenei romani. Molise, Valle d'Aosta e Basilicata non ospitano atenei con corsi L-8 attivi.</p></div>""", unsafe_allow_html=True)
    st.markdown("""<div class="section-card"><p><b style="color:#F5F5F7">Profilo e soddisfazione.</b> L'<b style="color:#34D399">88.7%</b> dei laureati si dichiara soddisfatto del corso (AlmaLaurea 2025), con il <b style="color:#34D399">73.1%</b> che si reiscriverebbe allo stesso corso. La prosecuzione alla magistrale è elevatissima: <b style="color:#F5F5F7">82.7%</b>. La retribuzione media netta mensile è di <b style="color:#14B8A6">€1.327</b>.</p></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class="section-card"><p><b style="color:#F5F5F7">Tassazione.</b> Il contributo massimo annuo per gli <b style="color:#14B8A6">atenei statali</b> varia da <b style="color:#F5F5F7">€{int(tasse[tasse['Tipo']=='Statale']['Contributo max'].min()) if not tasse[tasse['Tipo']=='Statale'].empty else 2100:,}</b> a <b style="color:#F5F5F7">€{int(tasse[tasse['Tipo']=='Statale']['Contributo max'].max()) if not tasse[tasse['Tipo']=='Statale'].empty else 4538:,}</b>, con una media di circa <b style="color:#F5F5F7">€{int(tasse[tasse['Tipo']=='Statale']['Contributo max'].mean()) if not tasse[tasse['Tipo']=='Statale'].empty else 3065:,}</b>. Gli atenei <b style="color:#EF4444">non statali</b> si collocano significativamente al di sopra, con il Campus Bio-Medico a €6.640.</p></div>""", unsafe_allow_html=True)
    st.markdown("""<div class="section-card"><p><b style="color:#F5F5F7">Percorso accademico.</b> In media il <b style="color:#14B8A6">68–70%</b> degli immatricolati prosegue nello stesso corso al secondo anno (iC14), con variazioni tra famiglie di corso. Le <b style="color:#F59E0B">università telematiche</b> mostrano tassi di prosecuzione strutturalmente inferiori rispetto alle tradizionali.</p></div>""", unsafe_allow_html=True)
    st.markdown("""<div class="section-card" style="border-top: 3px solid #14B8A6;">
    <p><b style="color:#F5F5F7">Il sistema L-8 Ingegneria dell'Informazione</b> mostra un quadro articolato: domanda in crescita nel quinquennio 2020–2025, elevata soddisfazione dei laureati e forte propensione alla prosecuzione magistrale. Un aspetto da monitorare è il divario tra atenei tradizionali e telematici, sia in termini di prosecuzione che di sbocchi lavorativi.</p>
    <p style="color:#C8C8C8; font-size:0.82rem; margin-top:1.5rem;">Analisi basata su dati MUR-USTAT, ANVUR AVA2 e AlmaLaurea · Periodo di riferimento: 2010–2025 · Elaborazione: Centro Studi</p>
    </div>""", unsafe_allow_html=True)
