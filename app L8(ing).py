import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Analisi Nazionale L-8 Ingegneria dell'Informazione",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="auto"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
:root {
    --bg-primary: #0A1F0F; --bg-secondary: #0D2613; --bg-card: #132E19; --bg-card-hover: #1A3D24;
    --border: rgba(255,255,255,0.08); --border-accent: rgba(34,197,94,0.4);
    --text-primary: #E8F5E9; --text-secondary: #C8C8C8; --text-tertiary: #C8C8C8;
    --accent-green: #22C55E; --accent-amber: #F59E0B; --accent-light: #86EFAC; --accent-red: #FF5A5A;
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
.sidebar-title { font-size: 0.65rem; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; color: var(--text-tertiary); padding: 1rem 1rem 0.5rem; }
[data-testid="stSidebar"] .stRadio > label { color: var(--text-secondary) !important; font-size: 0.9rem !important; }
[data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] p { color: var(--text-secondary) !important; font-size: 0.9rem !important; }
.stButton > button { background: var(--accent-green) !important; color: white !important; border: none !important; border-radius: 8px !important; font-weight: 500 !important; padding: 0.5rem 1.5rem !important; }
[data-testid="metric-container"] { background: var(--bg-card) !important; border: 1px solid var(--border) !important; border-radius: 12px !important; padding: 1rem !important; }
[data-testid="stMetricValue"] { color: var(--accent-green) !important; font-size: 1.8rem !important; font-weight: 600 !important; }
[data-testid="stMetricLabel"] { color: var(--text-secondary) !important; }
.chart-instructions { background: rgba(34,197,94,0.06); border: 1px solid rgba(34,197,94,0.15); border-radius: 10px; padding: 0.75rem 1rem; margin-bottom: 1rem; font-size: 0.82rem; color: #86EFAC; }
.chart-description { color: var(--text-secondary); font-size: 0.9rem; line-height: 1.65; margin-bottom: 1rem; font-weight: 300; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
[data-testid="stToolbarActions"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ── COSTANTI ──────────────────────────────────────────────────────────────────
BG_PLOT = '#0D2613'
BG_PAPER = '#0D2613'
PLOT_LAYOUT = dict(font=dict(family='Inter', size=12), plot_bgcolor=BG_PLOT, paper_bgcolor=BG_PAPER, title_font=dict(size=18, color='white', family='Inter'))
COLORI_MACRO = {'Nord': '#60A5FA', 'Centro': '#22C55E', 'Sud': '#FB923C', 'Isole': '#C084FC'}

TELEMATICHE_LIST = [
    'Telematica Universitas Mercatorum', 'Telematica Uninettuno',
    'Telematica Guglielmo Marconi', 'Telematica Niccolò Cusano',
    'Telematica Giustino Fortunato', 'Telematica e-Campus', 'Link Campus',
]
PRIVATE_LIST = ['Campus Biomedico', 'LUM "Degennaro"']

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
    'Ingegneria Informatica E Dell\'Automazione': 'Informatica',
    'Ingegneria Informatica E Dell\'Intelligenza Artificiale': 'Informatica',
    'Ingegneria Informatica Ed Elettronica': 'Informatica',
    'Ingegneria Informatica E Automatica': 'Informatica',
    'Ingegneria Informatica E Delle Telecomunicazioni': 'Informatica',
    'Ingegneria Informatica E Biomedica': 'Informatica',
    'Ingegneria Informatica E Dell\'Informazione': 'Informatica',
    'Ingegneria Informatica Per La Transizione Digitale': 'Informatica',
    'Ingegneria  Informatica': 'Informatica',
    'Ingegneria Delle Tecnologie Informatiche': 'Informatica',
    'Ingegneria E Scienze Informatiche': 'Informatica',
    'Ingegneria E Scienze Informatiche Per La Cybersecurity': 'Informatica',
    'Ingegneria Informatica, Elettronica E Delle Telecomunicazioni': 'Informatica',
    'Ingegneria Informatica, Delle Comunicazioni Ed Elettronica': 'Informatica',
    'Ingegneria Informatica, Biomedica E Delle Telecomunicazioni': 'Informatica',
    'Ingegneria Delle Tecnologie Per L\'Impresa Digitale': 'Informatica',
    'Ingegneria Dell\'Innovazione Per Le Imprese Digitali': 'Informatica',
    'Ingegneria Di Internet': 'Informatica',
    'Ingegneria Elettronica': 'Elettronica',
    'Ingegneria Elettronica E Informatica': 'Elettronica',
    'Ingegneria Elettronica E Biomedica': 'Elettronica',
    'Ingegneria Elettronica E Delle Tecnologie Digitali': 'Elettronica',
    'Ingegneria Elettronica E Delle Tecnologie Internet': 'Elettronica',
    'Ingegneria Elettronica E Telecomunicazioni': 'Elettronica',
    'Ingegneria Elettronica E Tecnologie Dell\'Informazione': 'Elettronica',
    'Ingegneria Elettronica E Delle Telecomunicazioni': 'Elettronica',
    'Ingegneria Elettronica, Informatica E Delle Telecomunicazioni': 'Elettronica',
    'Ingegneria Elettronica E Dei Sistemi Ciberfisici': 'Elettronica',
    'Electronic And Communications Engineering (Ingegneria Elettronica E Delle Comunicazioni)': 'Elettronica',
    'Ingegneria Biomedica': 'Biomedica',
    'Bioingegneria': 'Biomedica',
    'Ingegneria Dei Sistemi Medicali': 'Biomedica',
    'Ingegneria Dei Sistemi Medicali Per La Persona': 'Biomedica',
    'Ingegneria Dell\'Informazione Per La Medicina Digitale': 'Biomedica',
    'Ingegneria Gestionale': 'Gestionale',
    'Ingegneria Delle Telecomunicazioni': 'Telecomunicazioni',
    'Ingegneria Delle Comunicazioni': 'Telecomunicazioni',
    'Ingegneria Delle Telecomunicazioni E Dei Media Digitali': 'Telecomunicazioni',
    'Ingegneria Delle Telecomunicazioni, Internet E Multimedia': 'Telecomunicazioni',
    'Ingegneria Dell\'Automazione': 'Automazione',
    'Ingegneria Dell\'Automazione E Dei Sistemi': 'Automazione',
    'Ingegneria Dell\'Automazione Industriale': 'Automazione',
    'Corso Di Laurea In Ingegneria Dell\'Automazione': 'Automazione',
    'Ingegneria Robotica': 'Automazione',
    'Ingegneria Dei Sistemi Robotici E Intelligenti': 'Automazione',
    'Ingegneria Cibernetica': 'Automazione',
    'Ingegneria Dell\'Informazione': 'Informazione',
    'Ingegneria Dell\' Informazione: Elettronica, Informatica E Telecomunicazioni': 'Informazione',
}
MACRO_FAMIGLIE_CLEAN = {k: ('Multidisciplinare' if v in ['Altro', 'Multidisciplinare'] else v)
                         for k, v in MACRO_FAMIGLIE.items()}
COLORI_FAMIGLIE = {
    'Informatica': '#22C55E', 'Elettronica': '#16A34A',
    'Biomedica': '#86EFAC', 'Gestionale': '#15803D',
    'Telecomunicazioni': '#4ADE80', 'Automazione': '#166534',
    'Informazione': '#14532D', 'Multidisciplinare': '#6B7280',
}
GEOJSON_URL = "https://raw.githubusercontent.com/openpolis/geojson-italy/master/geojson/limits_IT_regions.geojson"
GRIGIO_SCURO = ["Valle d'Aosta/Vallée d'Aoste", 'Molise', 'Basilicata']

def fonte_annotation(testo):
    return dict(x=0.99, y=-0.13, xref='paper', yref='paper', text=testo, showarrow=False,
                font=dict(size=10, color='#6B9E7A'), align='right', xanchor='right')

def chart_header(titolo, descrizione, istruzioni):
    st.markdown(f"### {titolo}")
    st.markdown(f'<p class="chart-description">{descrizione}</p>', unsafe_allow_html=True)
    if istruzioni:
        st.markdown(f'<div class="chart-instructions">{istruzioni}</div>', unsafe_allow_html=True)

# ── CARICAMENTO DATI ──────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
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

@st.cache_data(show_spinner=False)
def prep_indicatori(df):
    ic14  = df[df['ID Indicatore'] == 'iC14'].copy()
    ic21  = df[df['ID Indicatore'] == 'iC21'].copy()
    ic00b = df[df['ID Indicatore'] == 'iC00b'].copy()
    ic16bis = df[df['ID Indicatore'] == 'iC16BIS'].copy()
    ic02  = df[df['ID Indicatore'] == 'iC02'].copy()
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

with st.spinner("Caricamento dati in corso..."):
    df, mur_l_l8, mur_i_l8, tasse = load_data()
    ic14, ic21, ic00b, ic02, merge14, merge14_var, df_destino, ic16_naz = prep_indicatori(df)

anni_alma = [2020, 2021, 2022, 2023, 2024, 2025]
alma_profilo = pd.DataFrame({
    'anno': anni_alma,
    'pct_soddisfatti':  [91.1, 90.1, 90.1, 90.6, 90.2, 88.7],
    'pct_riiscrizione': [74.8, 75.1, 74.1, 74.9, 74.8, 73.1],
    'pct_magistrale':   [85.1, 84.9, 85.0, 84.5, 84.7, 82.7],
    'pct_lavora':       [22.1, 24.3, 30.3, 27.6, 32.9, 36.1],
    'retribuzione':     [1135, 1164, 1226, 1264, 1393, 1327],
})

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

def get_key_exact(dizionario, parola):
    for k, v in dizionario.items():
        k_clean = k.encode('latin-1', errors='replace').decode('utf-8', errors='replace').strip()
        if parola.lower() in k_clean.lower():
            return v
    return None

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

avvi_2025 = int(df[(df['ID Indicatore'] == 'iC00a') & (df['Anno accademico'] == 2025)]['Numeratore'].sum())
n_atenei  = df['Ateneo'].nunique()
try:
    iscritti_2025 = int(mur_i_l8[mur_i_l8['AnnoA'] == '2024/2025']['Isc'].sum())
except:
    iscritti_2025 = int(mur_i_l8.groupby('AnnoA')['Isc'].sum().iloc[-1])
try:
    lau_2024 = int(mur_l_l8[mur_l_l8['AnnoS'] == 2024]['Lau'].sum())
except:
    lau_2024 = int(mur_l_l8.groupby('AnnoS')['Lau'].sum().iloc[-1])

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 1.5rem 0 1rem 0;'>
        <div style='font-size:1.1rem; font-weight:600; color:#E8F5E9; letter-spacing:-0.02em;'>L-8 Ingegneria</div>
        <div style='font-size:0.75rem; color:#86EFAC; margin-top:0.25rem; font-weight:400;'>dell'Informazione · Analisi Nazionale</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">Sezioni</div>', unsafe_allow_html=True)
    sezione = st.radio(label="", options=[
        "Panoramica", "Iscritti",
        "Profilo Studenti", "Percorso Accademico",
        "Varianti del Corso", "Tasse e Contributi", "Analisi Avanzata", "Sintesi",
    ], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("""<div style='font-size:0.72rem; color:#4A8A5A; line-height:1.6;'>
        Fonti: MUR-USTAT, ANVUR,<br>AlmaLaurea · Dati 2010–2025</div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PANORAMICA
# ═══════════════════════════════════════════════════════════════════════════════
if sezione == "Panoramica":
    st.markdown("# Analisi Nazionale\nL-8 Ingegneria dell'Informazione")
    st.markdown("---")
    st.markdown("""<p>Questa analisi documenta il panorama nazionale del Corso di Laurea in Ingegneria dell'Informazione (Classe L-8)
    attraverso dati ufficiali MUR-USTAT, ANVUR e AlmaLaurea. I dati coprono il periodo 2010–2025
    e includono avvii di carriera al primo anno, iscritti, laureati, distribuzione geografica,
    profilo degli studenti e indicatori di qualità della didattica.</p>""", unsafe_allow_html=True)
    st.markdown("### Indicatori chiave")
    kpi = [
        {'label': 'Avvii di carriera 2025', 'value': f'{avvi_2025:,}', 'delta': 'Immatricolati puri (iC00a)', 'color': '#22C55E'},
        {'label': 'Atenei attivi L-8', 'value': f'{n_atenei}', 'delta': 'incluse telematiche', 'color': '#86EFAC'},
        {'label': 'Soddisfatti del corso', 'value': '88.7%', 'delta': 'AlmaLaurea 2025', 'color': '#F59E0B'},
        {'label': 'Prosegue magistrale', 'value': '82.7%', 'delta': 'AlmaLaurea 2025', 'color': '#4ADE80'},
    ]
    cols = st.columns(4)
    for col, k in zip(cols, kpi):
        with col:
            st.markdown(f"""<div class="section-card" style="border-top: 3px solid {k['color']}; padding: 1.25rem;">
                <div style="font-size:0.75rem; color:#C8C8C8; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:0.5rem;">{k['label']}</div>
                <div style="font-size:2rem; font-weight:700; color:{k['color']}; letter-spacing:-0.03em;">{k['value']}</div>
                <div style="font-size:0.78rem; color:#C8C8C8; margin-top:0.25rem;">{k['delta']}</div>
            </div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### Struttura dell'analisi")
    sezioni_info = [
        ("Iscritti", "Avvii di carriera al primo anno, distribuzione geografica, top atenei, focus sul Lazio, bubble chart macro aree e totale iscritti.", "#22C55E"),
        ("Profilo Studenti", "Soddisfazione, riiscrizione e destinazione alla magistrale.", "#86EFAC"),
        ("Percorso Accademico", "Laureati, laureati in corso e tasso di prosecuzione al II anno.", "#F87171"),
        ("Varianti del Corso", "Prosecuzione per famiglia di corso L-8.", "#4ADE80"),
        ("Tasse e Contributi", "Confronto contributo massimo annuo tra atenei statali e non statali.", "#F87171"),
        ("Analisi Avanzata", "iC16BIS e correlazione tra dimensione del corso e prosecuzione.", "#60A5FA"),
        ("Sintesi", "Riepilogo dei risultati principali dell'analisi.", "#F59E0B"),
    ]
    for nome, desc, col in sezioni_info:
        st.markdown(f"""<div class="section-card" style="display:flex; align-items:flex-start; gap:1rem; padding:1.25rem;">
            <div style="width:3px; background:{col}; border-radius:2px; min-height:40px; flex-shrink:0;"></div>
            <div>
                <div style="font-size:0.9rem; font-weight:600; color:#E8F5E9; margin-bottom:0.25rem;">{nome}</div>
                <div style="font-size:0.82rem; color:#C8C8C8; font-weight:300;">{desc}</div>
            </div></div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# ISCRITTI
# ═══════════════════════════════════════════════════════════════════════════════
elif sezione == "Iscritti":
    st.markdown("## Iscritti")
    st.markdown("---")

    chart_header("Avvii di Carriera al Primo Anno — L-8 Ingegneria dell'Informazione",
        "Numero totale nazionale di avvii di carriera al primo anno per anno accademico. Le variazioni percentuali rispetto all'anno precedente sono indicate all'interno delle barre. Il 2025 è evidenziato in verde chiaro.",
        "Passa il cursore sulle barre per vedere il valore esatto.")
    avvi_naz = df[df['ID Indicatore'] == 'iC00a'].groupby('Anno accademico')['Numeratore'].sum().reset_index()
    avvi_naz.columns = ['anno', 'avvii']
    media_avvi = avvi_naz['avvii'].mean()
    colori_avvi = ['#22C55E' if a != avvi_naz['anno'].max() else '#86EFAC' for a in avvi_naz['anno']]
    fig_avvi = go.Figure()
    fig_avvi.add_trace(go.Scatter(x=[avvi_naz['anno'].min()-0.5, avvi_naz['anno'].max()+0.5], y=[media_avvi, media_avvi],
        mode='lines', line=dict(color='#F59E0B', width=2, dash='dash'),
        name=f'Media avvii di carriera: {media_avvi:,.0f}', hoverinfo='skip'))
    fig_avvi.add_trace(go.Bar(x=avvi_naz['anno'], y=avvi_naz['avvii'],
        marker=dict(color=colori_avvi, line=dict(color='rgba(0,0,0,0)', width=0), cornerradius=6),
        text=avvi_naz['avvii'].apply(lambda x: f'{x:,.0f}'), textposition='outside',
        textfont=dict(color='#D1D5DB', size=13, family='Inter'),
        hovertemplate='<b>%{x}</b><br>Avvii di carriera: <b>%{y:,.0f}</b><extra></extra>', name='Avvii di carriera'))
    for i, row in avvi_naz.iterrows():
        if i == 0: continue
        var = (row['avvii'] - avvi_naz.loc[i-1, 'avvii']) / avvi_naz.loc[i-1, 'avvii'] * 100
        colore = '#34D399' if var >= 0 else '#F87171'
        simbolo = '▲' if var >= 0 else '▼'
        fig_avvi.add_annotation(x=row['anno'], y=row['avvii']*0.5, text=f"{simbolo} {abs(var):.1f}%",
            showarrow=False, font=dict(size=11, color=colore, family='Inter'))
    fig_avvi.update_layout(**PLOT_LAYOUT, title='', showlegend=True,
        legend=dict(font=dict(color='#D1D5DB', size=11), bgcolor='rgba(0,0,0,0)', orientation='h', x=0.5, xanchor='center', y=1.08),
        margin=dict(t=100, b=80, l=70, r=30), height=520,
        annotations=[fonte_annotation('Fonte: ANVUR Cruscotto PENTAHO — Avvii di carriera al primo anno (iC00a)')])
    fig_avvi.update_xaxes(showgrid=False, tickfont=dict(color='#9CA3AF', size=13), linecolor='#2D5A3D', tickmode='linear', dtick=1)
    fig_avvi.update_yaxes(gridcolor='#1A3D24', tickfont=dict(color='#9CA3AF'), linecolor='#2D5A3D', rangemode='tozero',
        title=dict(text='N° avvii di carriera', font=dict(color='#9CA3AF')), range=[0, avvi_naz['avvii'].max()*1.2])
    st.plotly_chart(fig_avvi, use_container_width=True)
    st.markdown("---")

    chart_header("Avvii di Carriera per Famiglia di Corso — L-8",
        "Il treemap mostra la distribuzione degli avvii per macro-famiglia di corso L-8. Clicca su una famiglia per espandere le varianti.",
        "Seleziona l'anno con i pulsanti. Clicca su una famiglia per vedere le varianti.")
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
            hovers.append(f"<b>{row['macro_famiglia']}</b><br>Avvii: <b>{int(row['avvii']):,}</b><br>N° atenei: <b>{row['n_atenei']}</b><br><i>Clicca per espandere</i>")
        for _, row in varianti.iterrows():
            labels.append(row['corso_nome']); parents.append(row['macro_famiglia']); values.append(row['avvii'])
            colors.append(COLORI_FAMIGLIE.get(row['macro_famiglia'], '#6B7280'))
            hovers.append(f"<b>{row['corso_nome']}</b><br>Avvii: <b>{int(row['avvii']):,}</b><br>N° atenei: <b>{row['n_atenei']}</b>")
        fig_tree.add_trace(go.Treemap(labels=labels, parents=parents, values=values, customdata=hovers,
            hovertemplate='%{customdata}<extra></extra>', branchvalues='total',
            marker=dict(colors=colors, line=dict(color='#0A1F0F', width=2)),
            textfont=dict(size=13, color='white', family='Inter'),
            pathbar=dict(visible=True, thickness=24, textfont=dict(size=12, color='white', family='Inter')),
            visible=(i==0)))
    buttons_tree = [dict(label=str(anno), method='update',
        args=[{'visible': [j==i for j in range(len(anni_tree))]},
              {'title': dict(text=f'Avvii per Famiglia L-8 — {anno}', font=dict(size=18, color='white', family='Inter'), x=0.5, xanchor='center')}])
        for i, anno in enumerate(anni_tree)]
    fig_tree.update_layout(
        title=dict(text=f'Avvii per Famiglia L-8 — {anni_tree[0]}', font=dict(size=18, color='white', family='Inter'), x=0.5, xanchor='center'),
        updatemenus=[dict(type='buttons', direction='right', x=0.5, xanchor='center', y=1.10, yanchor='top',
            buttons=buttons_tree, bgcolor='#132E19', bordercolor='#22C55E', borderwidth=1,
            font=dict(size=12, family='Inter', color='white'), active=0, pad=dict(r=6,l=6,t=6,b=6))],
        annotations=[fonte_annotation('Fonte: ANVUR Cruscotto PENTAHO — Avvii di carriera per famiglia di corso')],
        height=580, margin=dict(t=120, b=60, l=20, r=20), font=dict(family='Inter', size=12), paper_bgcolor=BG_PAPER)
    st.plotly_chart(fig_tree, use_container_width=True)
    st.markdown("---")

    chart_header("Avvii di carriera L-8 per regione",
        "La mappa mostra la distribuzione degli avvii di carriera al primo anno per regione. Le regioni in grigio scuro non ospitano atenei con corsi L-8 attivi.",
        "Seleziona l'anno con i pulsanti. Passa il cursore sulla regione per il dettaglio per ateneo e corso.")
    avvi_map = df[df['ID Indicatore'] == 'iC00a'].copy()
    df_hm = avvi_map.groupby(['Anno accademico','regione','Ateneo','corso_nome'])['Numeratore'].sum().reset_index()
    def crea_hover(regione, anno):
        subset = df_hm[(df_hm['regione']==regione)&(df_hm['Anno accademico']==anno)].sort_values(['Ateneo','Numeratore'],ascending=[True,False])
        totale = int(subset['Numeratore'].sum())
        testo = f"<b>{regione}</b><br>Anno: {anno}<br>Avvii di carriera: <b>{totale:,}</b><br><br>"
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
    fig_map = go.Figure()
    for i, anno in enumerate(anni_map):
        subset = df_mappa[df_mappa['anno']==anno]
        fig_map.add_trace(go.Choropleth(
            geojson=GEOJSON_URL, locations=subset['regione'], featureidkey='properties.reg_name',
            z=subset['avvii'], colorscale=[[0,'#1A3D24'],[0.3,'#16A34A'],[0.6,'#22C55E'],[1,'#86EFAC']],
            zmin=df_mappa['avvii'].min(), zmax=df_mappa['avvii'].max(),
            colorbar=dict(title=dict(text='Avvii di<br>carriera', font=dict(color='#9CA3AF')), tickfont=dict(color='#9CA3AF'), x=1.0, thickness=15),
            marker_line_color='#0A1F0F', marker_line_width=1.5,
            text=subset['hover'], hovertemplate='%{text}<extra></extra>', name=str(anno), visible=(i==0)))
        fig_map.add_trace(go.Choropleth(
            geojson=GEOJSON_URL, locations=GRIGIO_SCURO, featureidkey='properties.reg_name',
            z=[0]*len(GRIGIO_SCURO), colorscale=[[0,'#3A3A3A'],[1,'#3A3A3A']], showscale=False,
            marker_line_color='#0A1F0F', marker_line_width=1.5,
            hovertemplate='<b>%{location}</b><br>Nessun corso L-8 attivo<extra></extra>', visible=(i==0), showlegend=False))
    n_layers = 2
    buttons_map = []
    for i, anno in enumerate(anni_map):
        vis = []
        for j in range(len(anni_map)):
            for _ in range(n_layers): vis.append(j==i)
        buttons_map.append(dict(label=str(anno), method='update',
            args=[{'visible': vis}, {'title': dict(text=f'Avvii di Carriera L-8 per Regione — {anno}', font=dict(size=18, color='white', family='Inter'), x=0.5, xanchor='center')}]))
    fig_map.update_layout(
        title=dict(text=f'Avvii di Carriera L-8 per Regione — {anni_map[0]}', font=dict(size=18, color='white', family='Inter'), x=0.5, xanchor='center'),
        updatemenus=[dict(type='buttons', direction='right', x=0.5, xanchor='center', y=1.08, yanchor='top',
            buttons=buttons_map, bgcolor='#132E19', bordercolor='#22C55E', borderwidth=1,
            font=dict(size=12, family='Inter', color='white'), active=0, pad=dict(r=6,l=6,t=6,b=6))],
        annotations=[
            dict(x=0.01, y=-0.02, xref='paper', yref='paper', text="Grigio: Valle d'Aosta, Molise, Basilicata — nessun corso L-8 attivo",
                showarrow=False, font=dict(size=10, color='#6B9E7A'), align='left'),
            dict(x=0.99, y=-0.02, xref='paper', yref='paper', text='Fonte: ANVUR Cruscotto PENTAHO — Avvii di carriera al primo anno (iC00a)',
                showarrow=False, font=dict(size=10, color='#6B9E7A'), xanchor='right', align='right')],
        margin=dict(r=20, t=110, l=0, b=40), height=650,
        font=dict(family='Inter', size=12), paper_bgcolor=BG_PAPER, geo=dict(bgcolor=BG_PAPER))
    fig_map.update_geos(fitbounds='locations', visible=False)
    st.plotly_chart(fig_map, use_container_width=True)
    st.markdown("---")

    chart_header("Top 15 atenei per avvii di carriera",
        "I 15 atenei con il maggior numero di avvii di carriera al primo anno per anno accademico.",
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
        subset = g_top15[g_top15['Anno accademico']==anno].sort_values('Numeratore',ascending=False).head(15).sort_values('Numeratore',ascending=True).reset_index(drop=True)
        fig_top.add_trace(go.Bar(x=subset['Numeratore'], y=subset['Ateneo'], orientation='h',
            marker=dict(color=[COLORI_MACRO.get(m,'#6B7280') for m in subset['macro']], line=dict(width=0), opacity=0.9, cornerradius=4),
            text=subset['Numeratore'].astype(int).apply(lambda x: f'{x:,}'),
            textposition='outside', textfont=dict(size=11, color='#9CA3AF'),
            customdata=subset[['macro','n_corsi','lista_corsi']].values,
            hovertemplate='<b>%{y}</b><br>Avvii: <b>%{x:,}</b><br>Macro area: %{customdata[0]}<br>N° corsi L-8: <b>%{customdata[1]}</b><br>%{customdata[2]}<extra></extra>',
            visible=(i==0), showlegend=False))
    for macro, colore in COLORI_MACRO.items():
        fig_top.add_trace(go.Bar(x=[None], y=[None], orientation='h', marker_color=colore, name=macro, visible=True))
    buttons_top = []
    for i, anno in enumerate(anni_top):
        vis = [j==i for j in range(len(anni_top))] + [True]*len(COLORI_MACRO)
        buttons_top.append(dict(label=str(anno), method='update',
            args=[{'visible': vis}, {'title': dict(text=f'Top 15 Atenei per Avvii di Carriera L-8 — {anno}', font=dict(size=18, color='white', family='Inter'), x=0.5, xanchor='center')}]))
    fig_top.update_layout(**PLOT_LAYOUT, title='',
        updatemenus=[dict(type='buttons', direction='right', x=0.5, xanchor='center', y=1.10, yanchor='top',
            buttons=buttons_top, bgcolor='#132E19', bordercolor='#22C55E', borderwidth=1,
            font=dict(size=12, family='Inter', color='white'), active=len(anni_top)-1, pad=dict(r=6,l=6,t=6,b=6))],
        annotations=[fonte_annotation('Fonte: ANVUR Cruscotto PENTAHO — Avvii di carriera al primo anno (iC00a)')],
        legend=dict(title=dict(text='Macro area', font=dict(color='#9CA3AF')), font=dict(color='#D1D5DB'), bgcolor='rgba(0,0,0,0)', x=0.75, y=0.05),
        margin=dict(t=120, b=60, l=200, r=80), height=560, barmode='overlay')
    fig_top.update_xaxes(title=dict(text='N° avvii di carriera', font=dict(color='#9CA3AF')), showgrid=False, tickfont=dict(color='#9CA3AF'), linecolor='#2D5A3D')
    fig_top.update_yaxes(showgrid=False, tickfont=dict(size=12, color='#D1D5DB'), linecolor='#2D5A3D')
    st.plotly_chart(fig_top, use_container_width=True)
    st.markdown("---")

    chart_header("Avvii di carriera L-8 nel Lazio — Tradizionali vs Telematiche",
        "Andamento degli avvii di carriera negli atenei laziali, distinti tra tradizionali e telematici.",
        "Passa il cursore sulle linee per vedere i valori anno per anno.")
    lazio = df[(df['ID Indicatore']=='iC00a') & (df['regione']=='Lazio')].copy()
    lazio_agg = lazio.groupby(['Anno accademico','Ateneo'])['Numeratore'].sum().reset_index()
    lazio_agg['tipo'] = lazio_agg['Ateneo'].apply(lambda x: 'Telematica' if x in TELEMATICHE_LIST else 'Tradizionale')
    lazio_corsi = lazio.groupby(['Anno accademico','Ateneo','corso_nome'])['Numeratore'].sum().reset_index()
    def build_hover_lazio(ateneo, anno):
        corsi = lazio_corsi[(lazio_corsi['Ateneo']==ateneo)&(lazio_corsi['Anno accademico']==anno)].sort_values('Numeratore',ascending=False)
        testo = f"<b>{ateneo}</b><br>Anno: {anno}<br>N° corsi L-8: <b>{len(corsi)}</b><br>"
        for _, r in corsi.iterrows():
            testo += f"&nbsp;&nbsp;• {r['corso_nome']}: <b>{int(r['Numeratore']):,}</b><br>"
        return testo
    lazio_agg['hover'] = lazio_agg.apply(lambda r: build_hover_lazio(r['Ateneo'], r['Anno accademico']), axis=1)
    trad = lazio_agg[lazio_agg['tipo']=='Tradizionale'].copy()
    tele = lazio_agg[lazio_agg['tipo']=='Telematica'].copy()
    PALETTE_TRAD = {'La Sapienza':'#22C55E','Tor Vergata':'#60A5FA','Roma Tre':'#FB923C','Campus Biomedico':'#C084FC','Università di Cassino e del Lazio Meridionale':'#F472B6'}
    PALETTE_TELE = {'Telematica Universitas Mercatorum':'#86EFAC','Telematica Uninettuno':'#93C5FD','Telematica Guglielmo Marconi':'#FCD34D','Telematica Niccolò Cusano':'#F9A8D4','Link Campus':'#A3E635'}
    NOMI_BREVI = {'Università di Cassino e del Lazio Meridionale':'Cassino','Telematica Universitas Mercatorum':'Universitas Mercatorum','Telematica Uninettuno':'Uninettuno','Telematica Guglielmo Marconi':'G. Marconi','Telematica Niccolò Cusano':'N. Cusano'}
    fig_lazio = make_subplots(rows=1, cols=2, column_widths=[0.5,0.5], horizontal_spacing=0.08)
    for ateneo in trad.groupby('Ateneo')['Numeratore'].sum().sort_values(ascending=False).index.tolist():
        colore = PALETTE_TRAD.get(ateneo,'#22C55E')
        nome = NOMI_BREVI.get(ateneo, ateneo)
        df_lab = trad[trad['Ateneo']==ateneo].sort_values('Anno accademico')
        fig_lazio.add_trace(go.Scatter(x=df_lab['Anno accademico'].astype(str), y=df_lab['Numeratore'],
            mode='lines+markers', name=nome, legendgroup='trad',
            legendgrouptitle=dict(text='Tradizionali', font=dict(color='#86EFAC', size=12)),
            line=dict(color=colore, width=2.5), marker=dict(size=8, color=colore, line=dict(color='#0A1F0F', width=1.5)),
            text=df_lab['hover'], hovertemplate='%{text}<extra></extra>'), row=1, col=1)
        ultimo = df_lab.iloc[-1]
        fig_lazio.add_annotation(x=str(int(ultimo['Anno accademico'])), y=ultimo['Numeratore'],
            text=f"<b>{int(ultimo['Numeratore'])}</b>", showarrow=False,
            font=dict(size=9, color=colore), xanchor='left', xshift=8, row=1, col=1)
    for ateneo in tele.groupby('Ateneo')['Numeratore'].sum().sort_values(ascending=False).index.tolist():
        colore = PALETTE_TELE.get(ateneo,'#86EFAC')
        nome = NOMI_BREVI.get(ateneo, ateneo)
        df_lab = tele[tele['Ateneo']==ateneo].sort_values('Anno accademico')
        fig_lazio.add_trace(go.Scatter(x=df_lab['Anno accademico'].astype(str), y=df_lab['Numeratore'],
            mode='lines+markers', name=nome, legendgroup='tele',
            legendgrouptitle=dict(text='Telematiche', font=dict(color='#FCD34D', size=12)),
            line=dict(color=colore, width=2.5), marker=dict(size=8, color=colore, line=dict(color='#0A1F0F', width=1.5)),
            text=df_lab['hover'], hovertemplate='%{text}<extra></extra>'), row=1, col=2)
        ultimo = df_lab.iloc[-1]
        fig_lazio.add_annotation(x=str(int(ultimo['Anno accademico'])), y=ultimo['Numeratore'],
            text=f"<b>{int(ultimo['Numeratore'])}</b>", showarrow=False,
            font=dict(size=9, color=colore), xanchor='left', xshift=8, row=1, col=2)
    fig_lazio.update_layout(**PLOT_LAYOUT, title='',
        annotations=[
            dict(x=0.22, y=1.10, xref='paper', yref='paper', text='<b>Atenei Tradizionali</b>', showarrow=False, font=dict(size=14, color='#86EFAC', family='Inter'), xanchor='center'),
            dict(x=0.78, y=1.10, xref='paper', yref='paper', text='<b>Atenei Telematici</b>', showarrow=False, font=dict(size=14, color='#FCD34D', family='Inter'), xanchor='center'),
            dict(x=0.99, y=-0.12, xref='paper', yref='paper', text='Fonte: ANVUR Cruscotto PENTAHO — Avvii di carriera al primo anno (iC00a)', showarrow=False, font=dict(size=10, color='#6B9E7A'), xanchor='right', align='right')],
        legend=dict(font=dict(color='#D1D5DB', size=11), bgcolor='rgba(0,0,0,0)', groupclick='toggleitem', x=1.01, y=1, xanchor='left', yanchor='top'),
        height=520, margin=dict(t=130, b=80, l=60, r=160))
    for c in [1, 2]:
        fig_lazio.update_xaxes(showgrid=False, tickfont=dict(color='#9CA3AF'), linecolor='#2D5A3D', row=1, col=c)
        fig_lazio.update_yaxes(gridcolor='#1A3D24', tickfont=dict(color='#9CA3AF'), linecolor='#2D5A3D', rangemode='tozero', title=dict(text='N° avvii di carriera', font=dict(color='#9CA3AF')), row=1, col=c)
    st.plotly_chart(fig_lazio, use_container_width=True)
    st.markdown("---")

    chart_header("Quota avvii di carriera per macro area — trend 2020–2025",
        "Ogni bolla rappresenta la quota percentuale di avvii di carriera per macro area. La dimensione è proporzionale al numero assoluto di avvii.",
        "Passa il cursore sulle bolle per vedere quota e numero assoluto.")
    OFFSET_MACRO = {'Nord': 2, 'Centro': 1, 'Sud': -1, 'Isole': -2}
    macro_agg = df[df['ID Indicatore']=='iC00a'].groupby(['Anno accademico','macro'])['Numeratore'].sum().reset_index().dropna(subset=['macro'])
    totale_anno = macro_agg.groupby('Anno accademico')['Numeratore'].sum().reset_index()
    totale_anno.columns = ['Anno accademico','totale']
    macro_pct = macro_agg.merge(totale_anno, on='Anno accademico')
    macro_pct['pct'] = (macro_pct['Numeratore'] / macro_pct['totale'] * 100).round(1)
    fig_bubble = go.Figure()
    for macro in ['Nord','Centro','Sud','Isole']:
        subset = macro_pct[macro_pct['macro']==macro].sort_values('Anno accademico').copy()
        subset['pct_offset'] = subset['pct'] + OFFSET_MACRO.get(macro, 0)
        fig_bubble.add_trace(go.Scatter(x=subset['Anno accademico'].astype(str), y=subset['pct_offset'],
            mode='markers+text', name=macro,
            marker=dict(size=subset['Numeratore']/macro_pct['Numeratore'].max()*80+20, color=COLORI_MACRO[macro], opacity=0.85, line=dict(color='#0A1F0F', width=2)),
            text=subset['pct'].apply(lambda x: f'{x:.1f}%'), textposition='middle center',
            textfont=dict(size=10, color='white', family='Inter'),
            hovertemplate=f'<b>{macro}</b><br>Anno: %{{x}}<br>Quota: <b>%{{customdata[0]:.1f}}%</b><br>Avvii: <b>%{{customdata[1]:,}}</b><extra></extra>',
            customdata=list(zip(subset['pct'], subset['Numeratore'].astype(int)))))
    fig_bubble.update_layout(**PLOT_LAYOUT, title='',
        annotations=[fonte_annotation('Fonte: ANVUR Cruscotto PENTAHO — Dimensione bolla = avvii assoluti')],
        legend=dict(font=dict(color='#D1D5DB'), bgcolor='rgba(0,0,0,0)', x=0.01, y=0.99),
        height=520, margin=dict(t=80, b=80, l=60, r=30))
    fig_bubble.update_xaxes(title=dict(text='Anno accademico', font=dict(color='#9CA3AF')), showgrid=False, tickfont=dict(color='#9CA3AF'), linecolor='#2D5A3D')
    fig_bubble.update_yaxes(title=dict(text='Quota (%)', font=dict(color='#9CA3AF')), gridcolor='#1A3D24', ticksuffix='%', tickfont=dict(color='#9CA3AF'), linecolor='#2D5A3D', range=[0, 70])
    st.plotly_chart(fig_bubble, use_container_width=True)
    st.markdown("---")

    chart_header("Iscritti L-8 Ingegneria dell'Informazione — Italia (2019–2025)",
        "Numero totale di studenti iscritti a corsi L-8 in Italia per anno accademico.",
        "Passa il cursore sui pallini per vedere il valore esatto.")
    isc_naz = mur_i_l8.groupby('AnnoA')['Isc'].sum().reset_index()
    isc_naz.columns = ['anno','iscritti']
    isc_naz['anno_short'] = isc_naz['anno'].str[:4] + '/' + isc_naz['anno'].str[7:9]
    media_isc = isc_naz['iscritti'].mean()
    fig_loll = go.Figure()
    for _, row in isc_naz.iterrows():
        fig_loll.add_shape(type='line', x0=row['anno_short'], x1=row['anno_short'],
            y0=0, y1=row['iscritti'], line=dict(color='#22C55E', width=3))
    fig_loll.add_trace(go.Scatter(x=isc_naz['anno_short'], y=isc_naz['iscritti'], mode='markers+text',
        marker=dict(size=20, color=['#86EFAC' if a==isc_naz['anno_short'].iloc[-1] else '#22C55E' for a in isc_naz['anno_short']], line=dict(color='white', width=2)),
        text=isc_naz['iscritti'].apply(lambda x: f'{x:,.0f}'), textposition='top center',
        textfont=dict(color='#C8C8C8', size=12, family='Inter'),
        hovertemplate='<b>%{x}</b><br>Iscritti: <b>%{y:,.0f}</b><extra></extra>', name='Iscritti L-8'))
    fig_loll.add_hline(y=media_isc, line=dict(color='#F59E0B', width=2, dash='dash'),
        annotation_text=f'Media: {media_isc:,.0f}', annotation_position='right',
        annotation_font=dict(color='#F59E0B', size=11))
    fig_loll.add_trace(go.Scatter(x=[None], y=[None], mode='lines', line=dict(color='#F59E0B', width=2, dash='dash'),
        name=f'Media periodo: {media_isc:,.0f}', showlegend=True))
    fig_loll.update_layout(**PLOT_LAYOUT, title='',
        showlegend=True, legend=dict(font=dict(color='#C8C8C8', size=11), bgcolor='rgba(0,0,0,0)', orientation='h', x=0.5, xanchor='center', y=1.08),
        margin=dict(t=100, b=80, l=70, r=100), height=520,
        annotations=[fonte_annotation('Fonte: MUR-USTAT — Iscritti L-8 per anno accademico')])
    fig_loll.update_xaxes(showgrid=False, tickfont=dict(color='#C8C8C8', size=13), linecolor='#2D5A3D')
    fig_loll.update_yaxes(gridcolor='#1A3D24', tickfont=dict(color='#C8C8C8'), linecolor='#2D5A3D', rangemode='tozero',
        title=dict(text='N° iscritti', font=dict(color='#C8C8C8')), range=[0, isc_naz['iscritti'].max()*1.2])
    st.plotly_chart(fig_loll, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PROFILO STUDENTI
# ═══════════════════════════════════════════════════════════════════════════════
elif sezione == "Profilo Studenti":
    st.markdown("## Profilo Studenti")
    st.markdown("---")
    chart_header("Indicatori chiave del profilo laureati L-8",
        "I tre indicatori riportano i valori del 2025 confrontati con un anno di riferimento selezionabile. I dati provengono dall'indagine AlmaLaurea sul Profilo dei Laureati.",
        "Seleziona l'anno di riferimento per il confronto con i pulsanti in alto.")
    anni_ref = [2020, 2021, 2022, 2023, 2024]
    indicatori_g = [('pct_soddisfatti','Soddisfatti del corso','#22C55E'),('pct_riiscrizione','Si reiscriverebbero','#86EFAC'),('pct_magistrale','Prosegue magistrale','#4ADE80')]
    val_2025 = {'pct_soddisfatti': 88.7, 'pct_riiscrizione': 73.1, 'pct_magistrale': 82.7}
    fig_gauge = go.Figure()
    for anno_ref in anni_ref:
        visible = (anno_ref == 2024)
        for col_idx, (col, titolo, colore) in enumerate(indicatori_g):
            val_ref = float(alma_profilo[alma_profilo['anno']==anno_ref][col].values[0])
            fig_gauge.add_trace(go.Indicator(mode='gauge+number+delta', value=val_2025[col],
                delta={'reference': val_ref, 'suffix': '%', 'relative': False, 'increasing': {'color': '#34D399'}, 'decreasing': {'color': '#F87171'}},
                number={'suffix': '%', 'font': {'size': 40, 'color': colore}},
                title={'text': f"<b style='color:#D1D5DB'>{titolo}</b><br><span style='font-size:11px;color:#6B7280'>2025 vs {anno_ref}</span>"},
                gauge={'axis': {'range': [0,100], 'ticksuffix': '%', 'tickfont': {'color': '#6B7280'}, 'tickcolor': '#C8C8C8'},
                    'bar': {'color': colore, 'thickness': 0.25}, 'bgcolor': '#132E19', 'borderwidth': 0,
                    'steps': [{'range': [0,50], 'color': '#0D2613'}, {'range': [50,75], 'color': '#1A3D24'}, {'range': [75,100], 'color': '#1A4D25'}],
                    'threshold': {'line': {'color': '#F59E0B', 'width': 3}, 'thickness': 0.75, 'value': val_ref}},
                domain={'x': [col_idx*0.34, col_idx*0.34+0.30], 'y': [0, 1]}, visible=visible))
    n_per_anno = len(indicatori_g)
    buttons_g = []
    for i, anno_ref in enumerate(anni_ref):
        vis = []
        for j in range(len(anni_ref)): vis += [j==i]*n_per_anno
        buttons_g.append(dict(label=f'vs {anno_ref}', method='update',
            args=[{'visible': vis}, {'title': dict(text=f'Profilo laureati L-8 — 2025 vs {anno_ref}', font=dict(size=20, color='white', family='Inter'), x=0.5, xanchor='center')}]))
    fig_gauge.update_layout(
        title=dict(text='Profilo laureati L-8 Ingegneria — 2025 vs 2024', font=dict(size=20, color='white', family='Inter'), x=0.5, xanchor='center'),
        updatemenus=[dict(type='buttons', direction='right', x=0.5, xanchor='center', y=1.55, yanchor='top',
            buttons=buttons_g, bgcolor='#132E19', bordercolor='#22C55E', borderwidth=1,
            font=dict(size=12, family='Inter', color='white'), active=len(anni_ref)-1, pad=dict(r=6,l=6,t=6,b=6))],
        height=420, margin=dict(t=195, b=60, l=30, r=30), font=dict(family='Inter', size=12), paper_bgcolor=BG_PAPER,
        annotations=[dict(x=0.5, y=-0.12, xref='paper', yref='paper',
            text="La linea arancione indica il valore dell'anno di riferimento selezionato",
            showarrow=False, font=dict(size=11, color='#6B9E7A'), align='center'),
            fonte_annotation('Fonte: AlmaLaurea — Profilo dei Laureati')])
    st.plotly_chart(fig_gauge, use_container_width=True)
    st.markdown("---")

    if alma_ok and not df_dest.empty:
        chart_header("Destinazione alla magistrale — dove proseguono gli studi",
            "Distribuzione percentuale degli studenti L-8 che si iscrivono alla laurea magistrale per destinazione geografica.",
            "Passa il cursore sulle barre per vedere la percentuale esatta di ciascun segmento.")
        df_dest2 = df_dest.copy()
        df_dest2['Altro'] = df_dest2['Altro Sud-Isole'].fillna(0) + df_dest2['Telematico'].fillna(0) + df_dest2['Estero'].fillna(0)
        df_dest2['hover_altro'] = df_dest2.apply(
            lambda r: f"<b>Altro</b><br>Anno {r['anno']}<br>"
                      f"&nbsp;&nbsp;Sud-Isole: <b>{(r['Altro Sud-Isole'] or 0):.1f}%</b><br>"
                      f"&nbsp;&nbsp;Telematico: <b>{(r['Telematico'] or 0):.1f}%</b><br>"
                      f"&nbsp;&nbsp;Estero: <b>{(r['Estero'] or 0):.1f}%</b><br>"
                      f"Totale: <b>{r['Altro']:.1f}%</b>", axis=1)
        DEST_PLOT = {'Stesso Ateneo':'#22C55E','Altro Nord':'#60A5FA','Altro Centro':'#F59E0B','Altro':'#C8C8C8'}
        media_stesso = df_dest2['Stesso Ateneo'].mean()
        media_centro = df_dest2['Altro Centro'].mean()
        fig_dest = go.Figure()
        for col, colore in DEST_PLOT.items():
            if col == 'Altro':
                fig_dest.add_trace(go.Bar(x=df_dest2['anno'], y=df_dest2[col], name=col,
                    marker=dict(color=colore, line=dict(width=0), opacity=0.92),
                    text=df_dest2[col].apply(lambda x: f'{x:.1f}%'), textposition='inside',
                    textfont=dict(size=11, color='white', family='Inter'),
                    customdata=df_dest2['hover_altro'], hovertemplate='%{customdata}<extra></extra>'))
            else:
                fig_dest.add_trace(go.Bar(x=df_dest2['anno'], y=df_dest2[col], name=col,
                    marker=dict(color=colore, line=dict(width=0), opacity=0.92),
                    text=df_dest2[col].apply(lambda x: f'{x:.1f}%'), textposition='inside',
                    textfont=dict(size=11, color='white', family='Inter'),
                    hovertemplate=f'<b>{col}</b><br>Anno %{{x}}<br><b>%{{y:.1f}}%</b><extra></extra>'))
        fig_dest.update_layout(barmode='stack', **PLOT_LAYOUT, title='',
            legend=dict(orientation='h', y=1.08, x=0.5, xanchor='center', bgcolor='rgba(0,0,0,0)', font=dict(color='#D1D5DB', size=11)),
            annotations=[
                dict(x=0.5, y=-0.18, xref='paper', yref='paper',
                    text=f"<b style='color:#22C55E'>{media_stesso:.1f}%</b><span style='color:#9CA3AF'> resta nello stesso ateneo · </span><b style='color:#F59E0B'>{media_centro:.1f}%</b><span style='color:#9CA3AF'> sceglie un ateneo del Centro Italia</span>",
                    showarrow=False, font=dict(size=12, family='Inter'), align='center'),
                fonte_annotation('Fonte: AlmaLaurea — Profilo dei Laureati')],
            height=540, margin=dict(t=80, b=100, l=60, r=30))
        fig_dest.update_xaxes(title=dict(text='Anno di laurea', font=dict(color='#9CA3AF')), showgrid=False, tickfont=dict(color='#9CA3AF'), linecolor='#2D5A3D')
        fig_dest.update_yaxes(title=dict(text='%', font=dict(color='#9CA3AF')), range=[0,100], ticksuffix='%', gridcolor='#1A3D24', tickfont=dict(color='#9CA3AF'), linecolor='#2D5A3D')
        st.plotly_chart(fig_dest, use_container_width=True)
    else:
        st.info("Dati AlmaLaurea destinazione non disponibili.")

# ═══════════════════════════════════════════════════════════════════════════════
# PERCORSO ACCADEMICO
# ═══════════════════════════════════════════════════════════════════════════════
elif sezione == "Percorso Accademico":
    st.markdown("## Percorso Accademico")
    st.markdown("---")

    chart_header("Laureati L-8 Ingegneria dell'Informazione — Italia (2010–2024)",
        "Numero totale di laureati per anno solare. Le barre rosse corrispondono agli anni 2020 e 2021, durante i quali le sessioni di laurea hanno subito variazioni legate all'emergenza sanitaria.",
        "Passa il cursore sulle barre per vedere il valore esatto.")
    lau_naz = mur_l_l8.groupby('AnnoS')['Lau'].sum().reset_index()
    lau_naz.columns = ['anno','laureati']
    lau_naz = lau_naz[lau_naz['anno'] >= 2010].reset_index(drop=True)
    lau_naz['covid'] = lau_naz['anno'].isin([2020, 2021])
    primo = lau_naz[lau_naz['anno']==2010]['laureati'].values[0]
    crescita = (lau_naz['laureati'].iloc[-1] - primo) / primo * 100
    fig_lau = go.Figure()
    fig_lau.add_trace(go.Bar(x=lau_naz['anno'], y=lau_naz['laureati'],
        marker=dict(color=['#F87171' if c else '#22C55E' for c in lau_naz['covid']], line=dict(width=0), opacity=0.9, cornerradius=4),
        text=lau_naz['laureati'].apply(lambda x: f'{x:,.0f}'),
        textposition='outside', textfont=dict(size=9, color='#9CA3AF', family='Inter'),
        hovertemplate='<b>%{x}</b><br>Laureati: <b>%{y:,.0f}</b><extra></extra>', showlegend=False))
    fig_lau.add_trace(go.Bar(x=[None], y=[None], marker_color='#22C55E', name='Normale', showlegend=True))
    fig_lau.add_trace(go.Bar(x=[None], y=[None], marker_color='#F87171', name='COVID (2020–2021)', showlegend=True))
    fig_lau.update_layout(**PLOT_LAYOUT, title='', showlegend=True,
        legend=dict(font=dict(color='#D1D5DB', size=11), bgcolor='rgba(0,0,0,0)', orientation='h', x=0.5, xanchor='center', y=1.08),
        annotations=[
            dict(x=0.01, y=0.97, xref='paper', yref='paper',
                text=f"<b style='color:#22C55E'>+{crescita:.0f}%</b><span style='color:#9CA3AF'> dal 2010 al 2024</span>",
                showarrow=False, font=dict(size=13, family='Inter'), align='left'),
            fonte_annotation('Fonte: MUR-USTAT · Laureati L-8 per anno solare')],
        margin=dict(t=100, b=80, l=60, r=30), height=500)
    fig_lau.update_xaxes(tickangle=-45, showgrid=False, tickfont=dict(color='#9CA3AF'), tickmode='linear', dtick=1, linecolor='#2D5A3D')
    fig_lau.update_yaxes(gridcolor='#1A3D24', tickfont=dict(color='#9CA3AF'), rangemode='tozero', linecolor='#2D5A3D')
    st.plotly_chart(fig_lau, use_container_width=True)
    st.markdown("---")

    chart_header("Cosa succede dopo il primo anno — L-8 Ingegneria dell'Informazione",
        "Il grafico mostra la distribuzione degli immatricolati puri L-8 al termine del primo anno: chi prosegue nello stesso corso (iC14 ANVUR), chi cambia corso o ateneo (differenza iC21-iC14), e chi lascia l'università.",
        "Seleziona l'anno con i pulsanti.")
    anni_donut = sorted(df_destino['anno'].unique())
    fig_donut = go.Figure()
    for i, anno in enumerate(anni_donut):
        row = df_destino[df_destino['anno']==anno].iloc[0]
        fig_donut.add_trace(go.Pie(
            labels=['Proseguono nello stesso corso','Cambiano corso o ateneo',"Lasciano l'università"],
            values=[row['prosegue_stesso'],row['cambia_corso'],row['abbandona']],
            hole=0.60, marker=dict(colors=['#22C55E','#F59E0B','#F87171'], line=dict(color='#0A1F0F', width=3)),
            textinfo='percent', textposition='outside', textfont=dict(size=13, color='white', family='Inter'),
            hovertemplate='<b>%{label}</b><br><b>%{value:.1f}%</b> degli immatricolati puri<extra></extra>',
            visible=(i==0), sort=False, pull=[0.03,0.03,0.03]))
    buttons_donut = []
    for i, anno in enumerate(anni_donut):
        row = df_destino[df_destino['anno']==anno].iloc[0]
        vis = [j==i for j in range(len(anni_donut))]
        buttons_donut.append(dict(label=anno, method='update', args=[{'visible': vis}, {
            'title': dict(text=f"Cosa succede dopo il primo anno — {anno}", font=dict(size=18, color='white', family='Inter'), x=0.5, xanchor='center'),
            'annotations': [
                dict(text=f"<b>{row['prosegue_stesso']:.1f}%</b><br><span style='color:#9CA3AF;font-size:11px'>resta nello<br>stesso corso</span>",
                    x=0.5, y=0.5, xref='paper', yref='paper', showarrow=False, font=dict(size=24, color='white', family='Inter'), align='center'),
                dict(x=0.99, y=-0.12, xref='paper', yref='paper', text='Fonte: ANVUR iC14 + iC21 · Media nazionale corsi L-8',
                    showarrow=False, font=dict(size=10, color='#6B9E7A'), align='right', xanchor='right')]}]))
    row0 = df_destino[df_destino['anno']==anni_donut[0]].iloc[0]
    fig_donut.update_layout(
        title=dict(text=f"Cosa succede dopo il primo anno — {anni_donut[0]}", font=dict(size=18, color='white', family='Inter'), x=0.5, xanchor='center'),
        updatemenus=[dict(type='buttons', direction='right', x=0.5, xanchor='center', y=1.12, yanchor='top',
            buttons=buttons_donut, bgcolor='#132E19', bordercolor='#22C55E', borderwidth=1,
            font=dict(size=12, family='Inter', color='white'), active=0, pad=dict(r=6,l=6,t=6,b=6))],
        annotations=[
            dict(text=f"<b>{row0['prosegue_stesso']:.1f}%</b><br><span style='color:#9CA3AF;font-size:11px'>resta nello<br>stesso corso</span>",
                x=0.5, y=0.5, xref='paper', yref='paper', showarrow=False, font=dict(size=24, color='white', family='Inter'), align='center'),
            dict(x=0.99, y=-0.12, xref='paper', yref='paper', text='Fonte: ANVUR iC14 + iC21 · Media nazionale corsi L-8',
                showarrow=False, font=dict(size=10, color='#6B9E7A'), align='right', xanchor='right')],
        height=580, margin=dict(t=120, b=80, l=80, r=80), font=dict(family='Inter', size=12), paper_bgcolor=BG_PAPER,
        showlegend=True, legend=dict(font=dict(color='#D1D5DB', size=12), bgcolor='rgba(0,0,0,0)', orientation='h', x=0.5, xanchor='center', y=-0.08))
    st.plotly_chart(fig_donut, use_container_width=True)
    st.markdown("---")

    chart_header("% Laureati entro la Durata Normale del Corso — iC02",
        "Percentuale media nazionale di studenti L-8 che si laureano entro i tempi standard. Il valore più recente è evidenziato in verde chiaro.",
        "Passa il cursore sulle barre per vedere il valore.")
    ic02_clean = ic02[ic02['Numeratore'] <= 100].copy()
    ic02_naz = ic02_clean.groupby('Anno accademico')['Numeratore'].mean().reset_index()
    ic02_naz.columns = ['anno','pct']
    ic02_naz['pct'] = ic02_naz['pct'].round(1)
    media_ic02 = ic02_naz['pct'].mean()
    fig_ic02 = go.Figure()
    for i, row in ic02_naz.iterrows():
        colore = '#86EFAC' if row['anno']==ic02_naz['anno'].max() else '#22C55E'
        fig_ic02.add_trace(go.Bar(x=[row['pct']], y=[str(int(row['anno']))], orientation='h',
            marker=dict(color=colore, cornerradius=4), text=f"{row['pct']:.1f}%", textposition='outside',
            textfont=dict(color='#D1D5DB', size=13),
            hovertemplate=f"<b>{int(row['anno'])}</b><br>Laureati in corso: <b>{row['pct']:.1f}%</b><extra></extra>",
            showlegend=False, width=0.5))
    fig_ic02.add_trace(go.Scatter(x=[media_ic02, media_ic02],
        y=[str(int(ic02_naz['anno'].min())), str(int(ic02_naz['anno'].max()))],
        mode='lines', line=dict(color='#F59E0B', width=2, dash='dash'),
        name=f'Media periodo: {media_ic02:.1f}%', hoverinfo='skip'))
    fig_ic02.update_layout(**PLOT_LAYOUT, title='', showlegend=True,
        legend=dict(font=dict(color='#D1D5DB', size=11), bgcolor='rgba(0,0,0,0)', orientation='h', x=0.5, xanchor='center', y=1.08),
        barmode='overlay', margin=dict(t=100, b=80, l=80, r=100), height=450,
        annotations=[fonte_annotation('Fonte: ANVUR Cruscotto PENTAHO — % laureati entro durata normale (iC02)')])
    fig_ic02.update_xaxes(showgrid=False, tickfont=dict(color='#9CA3AF'), linecolor='#2D5A3D', ticksuffix='%', range=[0,50])
    fig_ic02.update_yaxes(tickfont=dict(color='#9CA3AF', size=13), linecolor='#2D5A3D')
    st.plotly_chart(fig_ic02, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# VARIANTI DEL CORSO
# ═══════════════════════════════════════════════════════════════════════════════
elif sezione == "Varianti del Corso":
    st.markdown("## Varianti del Corso")
    st.markdown("---")
    chart_header("Tasso di prosecuzione al II anno per famiglia di corso — iC14",
        "Confronto del tasso medio di prosecuzione al II anno per macro-famiglia L-8, usando 'Informatica' come baseline. Verde = superiore alla baseline, rosso = inferiore. Hover su Multidisciplinare per le varianti.",
        "Passa il cursore sulle barre per vedere il tasso di abbandono e il numero di atenei.")
    ic14_var = merge14_var.groupby('macro_famiglia')['perc_iC14'].mean().reset_index()
    ic14_var.columns = ['famiglia','prosecuzione']
    ic14_var['prosecuzione'] = ic14_var['prosecuzione'].round(1)
    ic14_var['abbandono'] = (100 - ic14_var['prosecuzione']).round(1)
    n_at_var = merge14_var.groupby('macro_famiglia')['Ateneo'].nunique().reset_index()
    n_at_var.columns = ['famiglia','n_atenei']
    ic14_var = ic14_var.merge(n_at_var, on='famiglia').sort_values('prosecuzione', ascending=True).reset_index(drop=True)
    multi_detail = merge14_var[merge14_var['macro_famiglia']=='Multidisciplinare']\
        .groupby('corso_pulito').agg(pct=('perc_iC14','mean'), n_at=('Ateneo','nunique'))\
        .round(1).sort_values('pct', ascending=False).reset_index()
    hover_multi = "<b>Multidisciplinare</b><br>Varianti incluse:<br>" + \
        "<br>".join([f"&nbsp;&nbsp;• {row['corso_pulito']}: <b>{row['pct']:.1f}%</b> ({row['n_at']} atenei)" for _, row in multi_detail.iterrows()])
    baseline_val = ic14_var[ic14_var['famiglia']=='Informatica']['prosecuzione'].values
    baseline = baseline_val[0] if len(baseline_val) > 0 else 65.0
    def get_c(row):
        if row['famiglia']=='Informatica': return '#6B7280'
        elif row['prosecuzione']>baseline: return '#34D399'
        else: return '#EF4444'
    ic14_var['colore'] = ic14_var.apply(get_c, axis=1)
    def build_hv(row):
        if row['famiglia']=='Multidisciplinare': return hover_multi
        return f"<b>{row['famiglia']}</b><br>Prosecuzione: <b>{row['prosecuzione']:.1f}%</b><br>Abbandono: <b>{row['abbandono']:.1f}%</b><br>N° atenei: <b>{row['n_atenei']}</b>"
    ic14_var['hover'] = ic14_var.apply(build_hv, axis=1)
    fig_var = go.Figure()
    fig_var.add_trace(go.Bar(x=ic14_var['prosecuzione'], y=ic14_var['famiglia'], orientation='h',
        marker=dict(color=ic14_var['colore'], line=dict(width=0), opacity=0.9, cornerradius=4),
        text=ic14_var.apply(lambda r: f"{r['prosecuzione']:.1f}%  ({r['n_atenei']} aten{'eo' if r['n_atenei']==1 else 'ei'})", axis=1),
        textposition='outside', textfont=dict(size=10, color='#D1D5DB'),
        hovertemplate='%{customdata}<extra></extra>', customdata=ic14_var['hover']))
    fig_var.add_vline(x=baseline, line=dict(color='#7A9CC0', width=2, dash='dash'))
    fig_var.update_layout(**PLOT_LAYOUT, title='',
        annotations=[dict(x=baseline, y=1.02, xref='x', yref='paper', text=f'Baseline: {baseline:.1f}%', showarrow=False, font=dict(size=10, color='#9CA3AF'), align='center'),
            fonte_annotation('Fonte: ANVUR iC14 · Verde = prosecuzione maggiore · Rosso = minore')],
        height=580, margin=dict(t=80, b=80, l=180, r=140))
    fig_var.update_xaxes(title=dict(text='% prosecuzione al II anno', font=dict(color='#9CA3AF')), showgrid=False, ticksuffix='%', tickfont=dict(color='#9CA3AF'), linecolor='#2D5A3D', range=[0,110])
    fig_var.update_yaxes(showgrid=False, tickfont=dict(size=10, color='#D1D5DB'), linecolor='#2D5A3D')
    st.plotly_chart(fig_var, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TASSE E CONTRIBUTI
# ═══════════════════════════════════════════════════════════════════════════════
elif sezione == "Tasse e Contributi":
    st.markdown("## Tasse e Contributi")
    st.markdown("---")
    chart_header("Contributo massimo annuo — L-8 Ingegneria dell'Informazione",
        "Il grafico confronta il contributo massimo annuo per un campione di atenei statali e gli atenei non statali. I colori indicano la macro area geografica. Le linee tratteggiate rosse rappresentano gli atenei non statali; la linea punteggiata la media degli statali del campione.",
        "")
    statali_t = tasse[tasse['Tipo']=='Statale'].sort_values('Contributo max', ascending=False).reset_index(drop=True)
    non_statali_t = tasse[tasse['Tipo']=='Non Statale'].sort_values('Contributo max', ascending=False).reset_index(drop=True)
    media_statali_t = statali_t['Contributo max'].mean()
    max_row_t = statali_t.iloc[0]
    min_row_t = statali_t.iloc[-1]
    n_t = len(statali_t)
    def get_macro_t(ateneo):
        nord = ['Politecnico Milano','Politecnico Torino','Università di Padova','Università di Bologna','Politecnica delle Marche']
        centro = ['Sapienza','Roma 3','Roma Tre','Tor Vergata']
        sud = ['Federico II','Politecnico di Bari']
        for n in nord:
            if n.lower() in ateneo.lower(): return 'Nord'
        for c in centro:
            if c.lower() in ateneo.lower(): return 'Centro'
        for s in sud:
            if s.lower() in ateneo.lower(): return 'Sud'
        return 'Nord'
    statali_t = statali_t.copy()
    statali_t['Macro'] = statali_t['Ateneo'].apply(get_macro_t)
    C_NONST_T = '#EF4444'; C_GRIGIO_T = '#6B7280'; C_TESTO_T = '#C8C8C8'; C_TESTO2_T = '#D1D5DB'
    COLORI_MACRO_T = {'Nord': '#60A5FA', 'Centro': '#22C55E', 'Sud': '#F59E0B'}
    fig_tasse = make_subplots(rows=2, cols=1, row_heights=[0.28, 0.72], vertical_spacing=0.04, specs=[[{"type":"xy"}],[{"type":"xy"}]])
    fig_tasse.add_trace(go.Scatter(x=[0], y=[0], mode='markers', marker=dict(opacity=0), showlegend=False, hoverinfo='skip'), row=1, col=1)
    cards_t = [
        {'titolo': 'STATALE PIÙ CARO', 'valore': f"€{max_row_t['Contributo max']:,.0f}".replace(',','.'),
         'sub1': max_row_t['Ateneo'].strip(), 'sub2': f"Macro area: {max_row_t['Macro']}", 'colore': COLORI_MACRO_T.get(max_row_t['Macro'],'#60A5FA')},
        {'titolo': 'MEDIA STATALI', 'valore': f"€{media_statali_t:,.0f}".replace(',','.'),
         'sub1': f'{n_t} atenei a campione', 'sub2': f'su {n_atenei} atenei L-8 totali', 'colore': C_GRIGIO_T},
        {'titolo': 'STATALE MENO CARO', 'valore': f"€{min_row_t['Contributo max']:,.0f}".replace(',','.'),
         'sub1': min_row_t['Ateneo'].strip(), 'sub2': f"Macro area: {min_row_t['Macro']}", 'colore': COLORI_MACRO_T.get(min_row_t['Macro'],'#22C55E')},
    ]
    shapes_t = []; annotations_t = []
    card_y0_t=0.76; card_y1_t=0.99; gaps_t=[0.01,0.34,0.67]; card_w_t=0.31
    for i_t, card_t in enumerate(cards_t):
        x0_t=gaps_t[i_t]; x1_t=x0_t+card_w_t; cx_t=(x0_t+x1_t)/2; cy_t=(card_y0_t+card_y1_t)/2
        shapes_t.append(dict(type='rect',xref='paper',yref='paper',x0=x0_t,x1=x1_t,y0=card_y0_t,y1=card_y1_t,fillcolor='#132E19',line=dict(color=card_t['colore'],width=2.5),layer='below',opacity=1))
        shapes_t.append(dict(type='rect',xref='paper',yref='paper',x0=x0_t,x1=x1_t,y0=card_y1_t-0.032,y1=card_y1_t,fillcolor=card_t['colore'],line=dict(width=0),layer='above',opacity=1))
        annotations_t.append(dict(x=cx_t,y=card_y1_t-0.02,xref='paper',yref='paper',text=f"<b>{card_t['titolo']}</b>",font=dict(size=13,color='white',family='Inter'),showarrow=False,xanchor='center',yanchor='middle'))
        annotations_t.append(dict(x=cx_t,y=cy_t+0.055,xref='paper',yref='paper',text=f"<b>{card_t['valore']}</b>",font=dict(size=36,color=card_t['colore'],family='Inter'),showarrow=False,xanchor='center',yanchor='middle'))
        annotations_t.append(dict(x=cx_t,y=cy_t-0.04,xref='paper',yref='paper',text=f"<b>{card_t['sub1']}</b>",font=dict(size=13,color='#F5F5F7',family='Inter'),showarrow=False,xanchor='center',yanchor='middle'))
        annotations_t.append(dict(x=cx_t,y=card_y0_t+0.025,xref='paper',yref='paper',text=card_t['sub2'],font=dict(size=13,color=C_TESTO2_T,family='Inter'),showarrow=False,xanchor='center',yanchor='bottom'))
    for macro_t in ['Nord','Centro','Sud']:
        sub_t = statali_t[statali_t['Macro']==macro_t]
        fig_tasse.add_trace(go.Bar(x=sub_t['Ateneo'], y=sub_t['Contributo max'], name=macro_t,
            marker=dict(color=COLORI_MACRO_T[macro_t], line=dict(width=0), opacity=0.9, cornerradius=4),
            text=sub_t['Contributo max'].apply(lambda v: f'€{v:,.0f}'.replace(',','.')),
            textposition='outside', textfont=dict(color=C_TESTO_T, size=11, family='Inter'),
            hovertemplate='<b>%{x}</b><br>Contributo max: <b>€%{y:,.0f}</b><extra></extra>'), row=2, col=1)
    colori_ns = ['#EF4444','#F87171']
    for i, (_, row) in enumerate(non_statali_t.iterrows()):
        fig_tasse.add_trace(go.Scatter(
            x=[-0.5, n_t-0.5], y=[row['Contributo max'], row['Contributo max']],
            mode='lines', name=row['Ateneo'].strip(),
            line=dict(color=colori_ns[i % len(colori_ns)], width=2.5, dash='dash'),
            showlegend=True, xaxis='x3', yaxis='y2',
            hovertemplate=f"<b>{row['Ateneo'].strip()}: €{row['Contributo max']:,.0f}</b><extra></extra>"))
    fig_tasse.add_trace(go.Scatter(
        x=[-0.5, n_t-0.5], y=[media_statali_t, media_statali_t],
        mode='lines', name='Media statali',
        line=dict(color=C_TESTO2_T, width=2, dash='dot'),
        showlegend=False, xaxis='x3', yaxis='y2', hoverinfo='skip'))
    for i, (_, row) in enumerate(non_statali_t.iterrows()):
        annotations_t.append(dict(x=0.5, y=row['Contributo max'], xref='paper', yref='y2',
            text=f"<b>{row['Ateneo'].strip()} (non statale): €{row['Contributo max']:,.0f}</b>".replace(',','.'),
            showarrow=False, font=dict(size=13, color=colori_ns[i % len(colori_ns)], family='Inter'),
            xanchor='center', yanchor='bottom', yshift=10,
            bgcolor='rgba(10,31,15,0.92)', bordercolor=colori_ns[i % len(colori_ns)], borderwidth=1.5, borderpad=17))
    annotations_t.append(dict(x=0.99, y=media_statali_t, xref='paper', yref='y2',
        text=f"<b>Media statali: €{media_statali_t:,.0f}</b>".replace(',','.'),
        showarrow=False, font=dict(size=13, color=C_TESTO2_T, family='Inter'),
        xanchor='right', yanchor='bottom', yshift=8, bgcolor='rgba(10,31,15,0.9)', borderpad=8))
    annotations_t.append(dict(x=0.99, y=-0.08, xref='paper', yref='paper',
        text=f' Dati su campione di {n_t} atenei statali · Fonte: siti ufficiali atenei a.a. 2025/26',
        showarrow=False, font=dict(size=10, color='#6B9E7A', family='Inter'), align='right', xanchor='right'))
    fig_tasse.update_layout(
        title=dict(text="Contributo massimo annuo — L-8 Ingegn
