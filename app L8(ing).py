import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="L-8 Ingegneria dell'Informazione",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="auto"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
:root {
    --bg-primary: #051A0A; --bg-secondary: #0A2010; --bg-card: #0F2D16; --bg-card-hover: #133A13;
    --border: rgba(255,255,255,0.08); --border-accent: rgba(34,197,94,0.4);
    --text-primary: #DCFCE7; --text-secondary: #A7F3D0; --text-tertiary: #A7F3D0;
    --accent-blue: #22C55E; --accent-amber: #FFB020; --accent-green: #22C55E; --accent-red: #FF5A5A;
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
.stButton > button { background: var(--accent-blue) !important; color: white !important; border: none !important; border-radius: 8px !important; font-weight: 500 !important; padding: 0.5rem 1.5rem !important; }
.stTextInput > div > div > input { background: var(--bg-card) !important; border: 1px solid var(--border) !important; color: var(--text-primary) !important; border-radius: 8px !important; }
[data-testid="metric-container"] { background: var(--bg-card) !important; border: 1px solid var(--border) !important; border-radius: 12px !important; padding: 1rem !important; }
[data-testid="stMetricValue"] { color: var(--accent-blue) !important; font-size: 1.8rem !important; font-weight: 600 !important; }
[data-testid="stMetricLabel"] { color: var(--text-secondary) !important; }
.chart-instructions { background: rgba(34,197,94,0.06); border: 1px solid rgba(34,197,94,0.15); border-radius: 10px; padding: 0.75rem 1rem; margin-bottom: 1rem; font-size: 0.82rem; color: #4ADE80; }
.chart-description { color: var(--text-secondary); font-size: 0.9rem; line-height: 1.65; margin-bottom: 1rem; font-weight: 300; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }
[data-testid="stForm"] button { background: #22C55E !important; color: white !important; font-weight: 700 !important; border-radius: 10px !important; font-size: 1rem !important; letter-spacing: 0.02em !important; }
[data-testid="stForm"] button:hover { background: #16A34A !important; transform: translateY(-1px) !important; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
[data-testid="stToolbarActions"] { display: none !important; }
</style>
""", unsafe_allow_html=True)




ATENEO_REG_L8 = {
    'Politecnico di Torino': 'Piemonte', 'Politecnico di Milano': 'Lombardia',
    'Università di Bergamo': 'Lombardia', 'Università di Brescia': 'Lombardia',
    'Università di Pavia': 'Lombardia', 'Università di Trento': 'Trentino-Alto Adige/Südtirol',
    'Università di Padova': 'Veneto', 'Università di Verona': 'Veneto',
    'Università di Udine': 'Friuli-Venezia Giulia', 'Università di Trieste': 'Friuli-Venezia Giulia',
    'Università di Genova': 'Liguria', 'Università di Bologna': 'Emilia-Romagna',
    'Università di Ferrara': 'Emilia-Romagna', 'Università di Modena e Reggio Emilia': 'Emilia-Romagna',
    'Università di Parma': 'Emilia-Romagna', 'Università di Firenze': 'Toscana',
    'Università di Pisa': 'Toscana', 'Università di Siena': 'Toscana',
    'Università di Perugia': 'Umbria', 'Politecnica delle Marche': 'Marche',
    'La Sapienza': 'Lazio', 'Tor Vergata': 'Lazio', 'Roma Tre': 'Lazio',
    'Campus Biomedico': 'Lazio', 'Link Campus': 'Lazio',
    "Università de L'Aquila": 'Abruzzo', 'Università di Cassino e del Lazio Meridionale': 'Lazio',
    'Federico II': 'Campania', 'Università Vanvitelli': 'Campania',
    'Parthenope': 'Campania', 'Università del Sannio': 'Campania',
    'Magna Graecia': 'Calabria', 'Mediterranea': 'Calabria',
    'Università della Calabria': 'Calabria', 'Politecnico di Bari': 'Puglia',
    'Università del SALENTO': 'Puglia', 'Università di Foggia': 'Puglia',
    'Università di Messina': 'Sicilia', 'Università di Palermo': 'Sicilia',
    'Università di Catania': 'Sicilia', 'Kore': 'Sicilia',
    'Università di Cagliari': 'Sardegna', 'Università di Sassari': 'Sardegna',
    "Università Ca' Foscari": 'Veneto', 'Università di Salerno': 'Campania',
    'Telematica Niccolò Cusano': 'Lazio', 'Telematica Guglielmo Marconi': 'Lazio',
    'Telematica Giustino Fortunato': 'Campania', 'Telematica Uninettuno': 'Lazio',
    'Telematica Universitas Mercatorum': 'Lazio', 'Telematica e-Campus': 'Lombardia',
    'LUM "Degennaro"': 'Puglia',
}
REGIONE_MACRO_L8 = {
    'Piemonte': 'Nord', 'Lombardia': 'Nord', 'Veneto': 'Nord',
    'Friuli-Venezia Giulia': 'Nord', 'Liguria': 'Nord',
    'Emilia-Romagna': 'Nord', 'Trentino-Alto Adige/Südtirol': 'Nord',
    'Toscana': 'Centro', 'Umbria': 'Centro', 'Marche': 'Centro',
    'Lazio': 'Centro', 'Abruzzo': 'Centro',
    'Campania': 'Sud', 'Puglia': 'Sud', 'Basilicata': 'Sud',
    'Calabria': 'Sud', 'Molise': 'Sud',
    'Sicilia': 'Isole', 'Sardegna': 'Isole',
}

@st.cache_data(show_spinner=False)
def load_data():
    BASE = os.path.dirname(os.path.abspath(__file__)) + "/"
    def load(f):
        for enc in ['utf-8', 'latin-1']:
            try:
                return pd.read_csv(BASE + f, sep=None, engine='python', encoding=enc)
            except:
                continue
    df_imm = load('MURiscrittixcorsodistudi.csv')
    if df_imm is None: df_imm = pd.DataFrame(columns=['ClasseNUMERO'])
    df_lau = load('MUR_laureatixclasse.csv')
    df_corso = load('MURiscrittixcorsodistudi.csv')
    imm_l2 = pd.DataFrame()
    anno1_l2 = pd.DataFrame()
    lau_l2 = df_lau[df_lau['ClasseNUMERO'].astype(str).str.strip() == 'L-8'].copy()
    corso_l2 = df_corso[df_corso['ClasseNUMERO'].astype(str).str.strip() == 'L-8'].copy()
    MACRO = {
        'Torino': 'Nord', 'Piemonte Orientale': 'Nord', 'Milano': 'Nord', 'Milano Bicocca': 'Nord',
        'Vita-Salute': 'Nord', 'Pavia': 'Nord', 'Brescia': 'Nord', 'Insubria': 'Nord', 'Trento': 'Nord',
        'Padova': 'Nord', 'Verona': 'Nord', 'Trieste': 'Nord', 'Udine': 'Nord', 'Genova': 'Nord',
        'Bologna': 'Nord', 'Ferrara': 'Nord', 'Modena': 'Nord', 'Parma': 'Nord',
        'Firenze': 'Centro', 'Pisa': 'Centro', 'Siena': 'Centro', 'Perugia': 'Centro',
        'Camerino': 'Centro', 'Urbino': 'Centro', 'Sapienza': 'Centro', 'Tor Vergata': 'Centro',
        'Tuscia': 'Centro', "L'Aquila": 'Centro', 'Teramo': 'Centro',
        'Napoli': 'Sud', 'Salerno': 'Sud', 'Sannio': 'Sud', 'Bari': 'Sud', 'Lecce': 'Sud',
        'Foggia': 'Sud', 'Salento': 'Sud', 'Basilicata': 'Sud', 'Calabria': 'Sud',
        'Catanzaro': 'Sud', 'Magna Graecia': 'Sud', 'Molise': 'Sud',
        'Palermo': 'Isole', 'Catania': 'Isole', 'Messina': 'Isole', 'Cagliari': 'Isole', 'Sassari': 'Isole',
    }
    def get_macro(nome):
        for key, area in MACRO.items():
            if key.lower() in str(nome).lower(): return area
        return 'Non classificato'
    corso_l2['macro'] = corso_l2['AteneoNOME'].apply(get_macro)
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
    anni = [2020, 2021, 2022, 2023, 2024, 2025]
    profili = {a: parse_almalaurea_csv(BASE + f'datialmalaureaPROFILO{a}(L8).csv') for a in anni}
    occupazioni = {a: parse_almalaurea_csv(BASE + f'datialmalaureaOCCUPAZIONE{a}(L8).csv') for a in anni}
    alma_profilo = pd.DataFrame({
        'anno': [2020, 2021, 2022, 2023, 2024, 2025],
        'pct_soddisfatti':              [91.1, 90.1, 90.1, 90.6, 90.2, 88.7],
        'pct_riiscrizione':             [74.8, 75.1, 74.1, 74.9, 74.8, 73.1],
        'pct_magistrale':               [85.1, 84.9, 85.0, 84.5, 84.7, 82.7],
        'pct_stesso_ateneo_magistrale': [profili[a].get('Stesso Ateneo della laurea di primo livello') for a in anni],
        'pct_magistrale_nord':          [profili[a].get('Altro Ateneo del Nord') for a in anni],
        'pct_magistrale_centro':        [profili[a].get('Altro Ateneo del Centro') for a in anni],
    })
    lau_naz = lau_l2.groupby('AnnoS')['Lau'].sum().reset_index()
    lau_naz['AnnoS'] = lau_naz['AnnoS'].astype(int)
    lau_naz = lau_naz[lau_naz['AnnoS'] >= 2010].reset_index(drop=True)
    lau_naz['COVID'] = lau_naz['AnnoS'].isin([2020, 2021])
    imm_naz = pd.DataFrame(columns=['AnnoA', 'Imm', 'anno_short', 'delta'])
    imm_naz = imm_naz[imm_naz['AnnoA'].str[:4].astype(int) >= 2010].copy()
    imm_naz['anno_short'] = imm_naz['AnnoA'].str[:4] + '/' + imm_naz['AnnoA'].str[7:9]
    imm_naz['delta'] = imm_naz['Imm'].pct_change() * 100
    df_anvur = pd.read_csv(BASE + 'PENTAHO(L8).csv', sep=None, engine='python', encoding='latin-1')
    df_anvur['imm'] = pd.to_numeric(df_anvur['Numeratore'].astype(str).str.replace(',', '').str.replace('.000', ''), errors='coerce')
    df_anvur['corso_nome'] = df_anvur['Nome Corso'].str.split(' - ', n=1).str[1].str.strip()
    df_anvur['ateneo_clean'] = df_anvur['Ateneo'].str.encode('latin-1').str.decode('utf-8', errors='replace').str.strip()
    df_anvur['ateneo_short'] = (df_anvur['ateneo_clean']
        .str.replace("Università di ", "", regex=False).str.replace("Università della ", "", regex=False)
        .str.replace("Università del ", "", regex=False).str.replace("Università degli Studi di ", "", regex=False)
        .str.replace("Università", "", regex=False).str.strip())
    ATENEO_REG_ANVUR = {
        'Torino': 'Piemonte', 'Piemonte Orientale': 'Piemonte', 'Milano': 'Lombardia', 'Bicocca': 'Lombardia',
        'San Raffaele': 'Lombardia', 'Pavia': 'Lombardia', 'Brescia': 'Lombardia', "dell'Insubria": 'Lombardia',
        'Trento': 'Trentino-Alto Adige/Südtirol', 'Padova': 'Veneto', 'Verona': 'Veneto',
        'Trieste': 'Friuli-Venezia Giulia', 'Udine': 'Friuli-Venezia Giulia', 'Genova': 'Liguria',
        'Bologna': 'Emilia-Romagna', 'Ferrara': 'Emilia-Romagna', 'Modena e Reggio Emilia': 'Emilia-Romagna', 'Parma': 'Emilia-Romagna',
        'Firenze': 'Toscana', 'Pisa': 'Toscana', 'Siena': 'Toscana', 'Perugia': 'Umbria',
        'Camerino': 'Marche', 'Carlo Bo': 'Marche', 'La Sapienza': 'Lazio', 'Tor Vergata': 'Lazio',
        'Tuscia': 'Lazio', 'Teramo': 'Abruzzo', "de L'Aquila": 'Abruzzo',
        'Federico II': 'Campania', 'Vanvitelli': 'Campania', 'Sannio': 'Campania',
        'Bari': 'Puglia', 'Foggia': 'Puglia', 'SALENTO': 'Puglia', 'Basilicata': 'Basilicata',
        'Calabria': 'Calabria', 'Magna Graecia': 'Calabria',
        'Catania': 'Sicilia', 'Palermo': 'Sicilia', 'Messina': 'Sicilia',
        'Cagliari': 'Sardegna', 'Sassari': 'Sardegna',
    }
    def get_regione(nome):
        for key, reg in ATENEO_REG_ANVUR.items():
            if key.lower() in str(nome).lower(): return reg
        return None
    df_anvur['regione'] = df_anvur['ateneo_short'].apply(get_regione)
    df_anvur['macro'] = df_anvur['regione'].map({
        'Piemonte': 'Nord', 'Lombardia': 'Nord', 'Veneto': 'Nord', 'Friuli-Venezia Giulia': 'Nord',
        'Liguria': 'Nord', 'Emilia-Romagna': 'Nord', 'Trentino-Alto Adige/Südtirol': 'Nord',
        'Toscana': 'Centro', 'Umbria': 'Centro', 'Marche': 'Centro', 'Lazio': 'Centro', 'Abruzzo': 'Centro',
        'Campania': 'Sud', 'Puglia': 'Sud', 'Basilicata': 'Sud', 'Calabria': 'Sud', 'Molise': 'Sud',
        'Sicilia': 'Isole', 'Sardegna': 'Isole',
    })
    df_ava2 = df_pentaho.copy()
    df_ava2['CODICE'] = df_ava2['ID Indicatore']
    df_ava2['INDICATORE'] = df_ava2['Numeratore']
    df_ava2['ind_float'] = df_ava2['Numeratore']
    df_ava2['NOME_CORSO'] = df_ava2['Nome Corso'].str.split(' - ', n=1).str[1].str.strip()
    df_ava2['CODICIONE'] = df_ava2['Nome Corso'].str.split(' - ', n=1).str[0].str.strip()
    df_ava2['CODE_UN'] = df_ava2['Ateneo']
    df_ava2['ID_ANNO_ACCADEMICO'] = df_ava2['Anno accademico']
    df_ava2['NUMERATORE'] = df_ava2['Numeratore']
    df_ava2['ID_REGIONE_MACRO_ISTAT'] = df_ava2['Ateneo'].map(ATENEO_REG_L8).map(REGIONE_MACRO_L8).map({'Nord':1,'Centro':3,'Sud':4,'Isole':4})
    df_ava2['COMUNE'] = df_ava2['Ateneo']
    df_pentaho = pd.read_csv(BASE + 'PENTAHO(L8).csv', sep=',', encoding='latin-1', quotechar='"', on_bad_lines='skip')
    df_pentaho['Ateneo'] = df_pentaho['Ateneo'].str.encode('latin-1', errors='replace').str.decode('utf-8', errors='replace')
    df_pentaho['Numeratore'] = pd.to_numeric(df_pentaho['Numeratore'].astype(str).str.replace('.000','',regex=False).str.replace(',','.',regex=False), errors='coerce')
    df_avvi = df_pentaho[df_pentaho['ID Indicatore']=='iC00a'].copy()
    df_avvi['corso_nome'] = df_avvi['Nome Corso'].str.split(' - ', n=1).str[1].str.strip()
    df_lau_corso = df_pentaho[df_pentaho['ID Indicatore']=='iC02'].copy()
    df_ic16 = df_pentaho[df_pentaho['ID Indicatore']=='iC16BIS'].copy()
    ateneo_regione = {k: (v, v) for k, v in ATENEO_REG_L8.items()}
    regione_macro = REGIONE_MACRO_L8
    df_avvi['regione'] = df_avvi['Ateneo'].map(lambda x: ateneo_regione.get(x, (None, None))[0])
    df_avvi['reg_name'] = df_avvi['Ateneo'].map(lambda x: ateneo_regione.get(x, (None, None))[1])
    df_avvi['macro'] = df_avvi['regione'].map(regione_macro)
    df_avvi['ateneo_short'] = df_avvi['Ateneo']
    return (imm_l2, anno1_l2, lau_l2, corso_l2, lau_naz, imm_naz,
            alma_profilo, df_anvur, df_ava2, df_avvi, df_lau_corso, df_ic16, df_pentaho)

with st.spinner("Caricamento dati in corso..."):
    (imm_l2, anno1_l2, lau_l2, corso_l2, lau_naz, imm_naz,
     alma_profilo, df_anvur, df_ava2, df_avvi, df_lau_corso, df_ic16, df_pentaho) = load_data()

GEOJSON_URL = "https://raw.githubusercontent.com/openpolis/geojson-italy/master/geojson/limits_IT_regions.geojson"
GRIGIO_SCURO = ["Valle d'Aosta/Vallée d'Aoste", 'Molise', 'Basilicata']
COLORI_MACRO = {'Nord': '#22C55E', 'Centro': '#4ADE80', 'Sud': '#F59E0B', 'Isole': '#A3E635'}
BG_PLOT = '#0A2010'
BG_PAPER = '#0A2010'
PLOT_LAYOUT = dict(font=dict(family='Inter', size=12), plot_bgcolor=BG_PLOT, paper_bgcolor=BG_PAPER, title_font=dict(size=18, color='white', family='Inter'))

def fonte_annotation(testo):
    return dict(x=0.99, y=-0.13, xref='paper', yref='paper', text=testo, showarrow=False,
                font=dict(size=10, color='#6BAA7A'), align='right', xanchor='right')

def chart_header(titolo, descrizione, istruzioni):
    st.markdown(f"### {titolo}")
    st.markdown(f'<p class="chart-description">{descrizione}</p>', unsafe_allow_html=True)
    if istruzioni:
        st.markdown(f'<div class="chart-instructions">{istruzioni}</div>', unsafe_allow_html=True)


with st.sidebar:
    st.markdown("""
    <div style='padding: 1.5rem 0 1rem 0;'>
        <div style='font-size:1.1rem; font-weight:600; color:#F5F5F7; letter-spacing:-0.02em;'>L-8 Ingegneria</div>
        <div style='font-size:0.75rem; color:#A7F3D0; margin-top:0.25rem; font-weight:400;'>dell'Informazione</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">Sezioni</div>', unsafe_allow_html=True)
    sezione = st.radio(label="", options=[
        "Panoramica", "Iscritti",
        "Profilo Studenti", "Percorso Accademico",
        "Varianti del Corso", "Tasse e Contributi", "Analisi Avanzata", "Sintesi",
    ], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("""<div style='font-size:0.72rem; color:#4D7A5A; line-height:1.6;'>
        Fonti: MUR-USTAT, ANVUR,<br>AlmaLaurea · Dati 2010–2025</div>""", unsafe_allow_html=True)


# ─── PANORAMICA ───────────────────────────────────────────────────────────────
if sezione == "Panoramica":
    st.markdown("# Analisi Nazionale\nL-8 Ingegneria")
    st.markdown("---")
    st.markdown("""<p>Questa analisi documenta il panorama nazionale del Corso di Laurea in Biotecnologie (Classe L-2)
    attraverso dati ufficiali MUR-USTAT, ANVUR e AlmaLaurea. I dati coprono il periodo 2010–2025
    e includono avvii di carriera al primo anno, iscritti, laureati, distribuzione geografica,
    profilo degli studenti e indicatori di qualità della didattica.</p>""", unsafe_allow_html=True)
    st.markdown("### Indicatori chiave")
    kpi = [
        {'label': 'Avvii di carriera 2025', 'value': 'N/D', 'delta': '↑ trend crescita', 'color': '#22C55E'},
        {'label': 'Atenei attivi L-8', 'value': '53', 'delta': 'incluse telematiche', 'color': '#34D399'},
        {'label': 'Soddisfatti del corso', 'value': '82.7%', 'delta': 'AlmaLaurea 2025', 'color': '#F59E0B'},
        {'label': 'Prosegue magistrale', 'value': '82.7%', 'delta': 'AlmaLaurea 2025', 'color': '#34D399'},
    ]
    cols = st.columns(4)
    for col, k in zip(cols, kpi):
        with col:
            st.markdown(f"""<div class="section-card" style="border-top: 3px solid {k['color']}; padding: 1.25rem;">
                <div style="font-size:0.75rem; color:#A7F3D0; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:0.5rem;">{k['label']}</div>
                <div style="font-size:2rem; font-weight:700; color:{k['color']}; letter-spacing:-0.03em;">{k['value']}</div>
                <div style="font-size:0.78rem; color:#A7F3D0; margin-top:0.25rem;">{k['delta']}</div>
            </div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### Struttura dell'analisi")
    sezioni_info = [
        ("Iscritti", "Avvii di carriera al primo anno, distribuzione geografica, top atenei, focus sul Lazio e totale iscritti.", "#22C55E"),
        
        ("Profilo Studenti", "Soddisfazione, riiscrizione e destinazione alla magistrale.", "#34D399"),
        ("Percorso Accademico", "Laureati, laureati in corso e tasso di prosecuzione al II anno.", "#EF4444"),
        ("Varianti del Corso", "Distribuzione delle varianti di denominazione L-2.", "#34D399"),
        ("Tasse e Contributi", "Confronto contributo massimo annuo tra atenei statali (campione) e non statali.", "#EF4444"),
        ("Analisi Avanzata", "iC16bis e correlazione tra dimensione del corso e prosecuzione.", "#4ADE80"),
        ("Sintesi", "Riepilogo dei risultati principali dell'analisi.", "#F59E0B"),
    ]
    for nome, desc, col in sezioni_info:
        st.markdown(f"""<div class="section-card" style="display:flex; align-items:flex-start; gap:1rem; padding:1.25rem;">
            <div style="width:3px; background:{col}; border-radius:2px; min-height:40px; flex-shrink:0;"></div>
            <div>
                <div style="font-size:0.9rem; font-weight:600; color:#F5F5F7; margin-bottom:0.25rem;">{nome}</div>
                <div style="font-size:0.82rem; color:#A7F3D0; font-weight:300;">{desc}</div>
            </div></div>""", unsafe_allow_html=True)


# ─── AVVII DI CARRIERA ───────────────────────────────────────────────────────
elif sezione == "Iscritti":
    st.markdown("## Iscritti")
    st.markdown("---")

    # G14 — Avvii bar chart
    chart_header("Avvii di Carriera al Primo Anno — L-8 Ingegneria",
        "Numero totale nazionale di avvii di carriera al primo anno per anno accademico. Le variazioni percentuali rispetto all'anno precedente sono indicate all'interno delle barre. Il 2025 è evidenziato in azzurro chiaro.",
        "Passa il cursore sulle barre per vedere il valore esatto.")
    avvi_naz = df_avvi.groupby('Anno accademico')['Numeratore'].sum().reset_index()
    avvi_naz.columns = ['anno', 'avvii']
    media_avvi = avvi_naz['avvii'].mean()
    colori_avvi = ['#22C55E' if a != avvi_naz['anno'].max() else '#4ADE80' for a in avvi_naz['anno']]
    fig_avvi = go.Figure()
    fig_avvi.add_trace(go.Scatter(x=[avvi_naz['anno'].min()-0.5, avvi_naz['anno'].max()+0.5], y=[media_avvi, media_avvi],
        mode='lines', line=dict(color='#F59E0B', width=2, dash='dash'),
        name=f'Media avvii di carriera: {media_avvi:,.0f}', hoverinfo='skip'))
    fig_avvi.add_trace(go.Bar(x=avvi_naz['anno'], y=avvi_naz['avvii'],
        marker=dict(color=colori_avvi, line=dict(color='rgba(0,0,0,0)', width=0), cornerradius=6),
        text=avvi_naz['avvii'].apply(lambda x: f'{x:,.0f}'), textposition='outside',
        textfont=dict(color='#D1FAE5', size=13, family='Inter'),
        hovertemplate='<b>%{x}</b><br>Avvii di carriera: <b>%{y:,.0f}</b><extra></extra>', name='Avvii di carriera'))
    for i, row in avvi_naz.iterrows():
        if i == 0: continue
        var = (row['avvii'] - avvi_naz.loc[i-1, 'avvii']) / avvi_naz.loc[i-1, 'avvii'] * 100
        colore = '#34D399' if var >= 0 else '#F87171'
        simbolo = '▲' if var >= 0 else '▼'
        fig_avvi.add_annotation(x=row['anno'], y=row['avvii']*0.5, text=f"{simbolo} {abs(var):.1f}%",
            showarrow=False, font=dict(size=11, color=colore, family='Inter'))
    fig_avvi.update_layout(**PLOT_LAYOUT, title='', showlegend=True,
        legend=dict(font=dict(color='#D1FAE5', size=11), bgcolor='rgba(0,0,0,0)', orientation='h', x=0.5, xanchor='center', y=1.08),
        margin=dict(t=100, b=80, l=70, r=30), height=520,
        annotations=[dict(x=0.99, y=-0.13, xref='paper', yref='paper',
            text='Fonte: ANVUR Cruscotto PENTAHO — Avvii di carriera al primo anno (iC00a)',
            showarrow=False, font=dict(size=10, color='#6BAA7A'), xanchor='right', align='right')])
    fig_avvi.update_xaxes(showgrid=False, tickfont=dict(color='#86EFAC', size=13), linecolor='#A7F3D0', tickmode='linear', dtick=1)
    fig_avvi.update_yaxes(gridcolor='#14532D', tickfont=dict(color='#86EFAC'), linecolor='#A7F3D0', rangemode='tozero',
        title=dict(text='N° avvii di carriera', font=dict(color='#86EFAC')), range=[0, avvi_naz['avvii'].max()*1.2])
    st.plotly_chart(fig_avvi, use_container_width=True)
    st.markdown("---")

    # Treemap avvii per variante
    chart_header("Avvii di Carriera per Variante di Denominazione L-2",
        "Il treemap mostra la distribuzione degli avvii di carriera per variante di denominazione, con dimensione proporzionale agli avvii e colore che indica il numero di atenei.",
        "Seleziona l'anno con i pulsanti.")
    df_avvi['corso_norm'] = df_avvi['Nome Corso'].str.split(' - ').str[1].str.strip().str.title()
    df_avvi['corso_norm'] = df_avvi['corso_norm'].str.replace('Biotecnologia$', 'Biotecnologie', regex=True)
    anni_tree_avvi = sorted(df_avvi['Anno accademico'].unique())
    fig_tree_avvi = go.Figure()
    for i, anno in enumerate(anni_tree_avvi):
        subset = df_avvi[df_avvi['Anno accademico'] == anno].groupby('corso_norm').agg(
            avvii=('Numeratore', 'sum'), n_atenei=('Ateneo', 'nunique')).reset_index()
        fig_tree_avvi.add_trace(go.Treemap(
            labels=subset['corso_norm'], parents=['L-8 Ingegneria (Varianti)']*len(subset),
            values=subset['avvii'], customdata=subset[['n_atenei', 'avvii']],
            hovertemplate='<b>%{label}</b><br>Avvii di carriera: <b>%{customdata[1]:,.0f}</b><br>N° atenei: <b>%{customdata[0]}</b><extra></extra>',
            marker=dict(colorscale=[[0,'#14532D'],[0.4,'#16A34A'],[0.7,'#4ADE80'],[1,'#BBF7D0']],
                colors=subset['n_atenei'], colorbar=dict(title=dict(text='N° atenei', font=dict(color='#86EFAC')), tickfont=dict(color='#86EFAC')),
                showscale=True, line=dict(color='#052E16', width=2)),
            textfont=dict(size=13, color='white', family='Inter'), visible=(i==0)))
    buttons_tree_avvi = []
    for i, anno in enumerate(anni_tree_avvi):
        vis = [j==i for j in range(len(anni_tree_avvi))]
        buttons_tree_avvi.append(dict(label=str(anno), method='update',
            args=[{'visible': vis}, {'title': dict(text=f'Avvii di Carriera per Variante L-2 — {anno}', font=dict(size=18, color='white', family='Inter'), x=0.5, xanchor='center')}]))
    fig_tree_avvi.update_layout(
        title=dict(text=f'Avvii di Carriera per Variante L-2 — {anni_tree_avvi[0]}', font=dict(size=18, color='white', family='Inter'), x=0.5, xanchor='center'),
        updatemenus=[dict(type='buttons', direction='right', x=0.5, xanchor='center', y=1.10, yanchor='top',
            buttons=buttons_tree_avvi, bgcolor='#14532D', bordercolor='#22C55E', borderwidth=1,
            font=dict(size=12, family='Inter', color='white'), active=0, pad=dict(r=6,l=6,t=6,b=6))],
        annotations=[fonte_annotation('Fonte: ANVUR Cruscotto PENTAHO — Avvii di carriera per variante di denominazione')],
        height=580, margin=dict(t=120, b=60, l=20, r=20), font=dict(family='Inter', size=12), paper_bgcolor=BG_PAPER)
    st.plotly_chart(fig_tree_avvi, use_container_width=True)
    st.markdown("---")

    # G17 — Mappa avvii
    chart_header("Avvii di carriera L-2 per regione",
        "La mappa mostra la distribuzione degli avvii di carriera al primo anno per regione, dal 2020 al 2025. Le regioni in grigio scuro non ospitano atenei con corsi L-2 attivi.",
        "Seleziona l'anno con i pulsanti. Passa il cursore sulla regione per il dettaglio per ateneo e corso.")
    df_mappa_avvi = df_avvi.groupby(['Anno accademico', 'reg_name'])['Numeratore'].sum().reset_index().rename(columns={'Numeratore': 'avvii'})
    df_hover_avvi2 = df_avvi.groupby(['Anno accademico', 'reg_name', 'Ateneo', 'Nome Corso'])['Numeratore'].sum().reset_index()
    def crea_hover_avvi2(regione, anno):
        subset = df_hover_avvi2[(df_hover_avvi2['reg_name']==regione) & (df_hover_avvi2['Anno accademico']==anno)].sort_values(['Ateneo','Numeratore'], ascending=[True,False])
        totale = int(subset['Numeratore'].sum())
        testo = f"<b>{regione}</b><br>Anno: {anno}<br>Avvii di carriera: <b>{totale:,}</b><br><br>"
        ateneo_corrente = None
        for _, row in subset.iterrows():
            corso = row['Nome Corso'].split(' - ')[1].strip() if ' - ' in row['Nome Corso'] else row['Nome Corso']
            if row['Ateneo'] != ateneo_corrente:
                ateneo_corrente = row['Ateneo']
                testo += f"<b>{ateneo_corrente}</b><br>"
            testo += f"&nbsp;&nbsp;{corso}: {int(row['Numeratore']):,}<br>"
        return testo
    df_mappa_avvi['hover'] = df_mappa_avvi.apply(lambda r: crea_hover_avvi2(r['reg_name'], r['Anno accademico']), axis=1)
    anni_avvi_map = sorted(df_mappa_avvi['Anno accademico'].unique())
    fig_avvi_map = go.Figure()
    for i, anno in enumerate(anni_avvi_map):
        subset = df_mappa_avvi[df_mappa_avvi['Anno accademico']==anno]
        fig_avvi_map.add_trace(go.Choropleth(geojson=GEOJSON_URL, locations=subset['reg_name'],
            featureidkey='properties.reg_name', z=subset['avvii'],
            colorscale=[[0,'#14532D'],[0.3,'#16A34A'],[0.6,'#4ADE80'],[1,'#BBF7D0']],
            zmin=df_mappa_avvi['avvii'].min(), zmax=df_mappa_avvi['avvii'].max(),
            colorbar=dict(title=dict(text='Avvii di<br>carriera', font=dict(color='#86EFAC')), tickfont=dict(color='#86EFAC'), x=1.0, thickness=15),
            marker_line_color='#052E16', marker_line_width=1.5,
            text=subset['hover'], hovertemplate='%{text}<extra></extra>', name=str(anno), visible=(i==0)))
        fig_avvi_map.add_trace(go.Choropleth(geojson=GEOJSON_URL, locations=GRIGIO_SCURO,
            featureidkey='properties.reg_name', z=[0,0], colorscale=[[0,'#A7F3D0'],[1,'#A7F3D0']], showscale=False,
            marker_line_color='#052E16', marker_line_width=1.5,
            hovertemplate='<b>%{location}</b><br>Nessun corso L-2 attivo<extra></extra>', visible=(i==0), showlegend=False))
    n_layers_avvi = len(fig_avvi_map.data) // len(anni_avvi_map)
    buttons_avvi_map = []
    for i, anno in enumerate(anni_avvi_map):
        vis = []
        for j in range(len(anni_avvi_map)):
            for _ in range(n_layers_avvi): vis.append(j==i)
        buttons_avvi_map.append(dict(label=str(anno), method='update',
            args=[{'visible': vis}, {'title': dict(text=f'Avvii di Carriera L-2 per Regione — {anno}', font=dict(size=18, color='white', family='Inter'), x=0.5, xanchor='center')}]))
    fig_avvi_map.update_layout(
        title=dict(text=f'Avvii di Carriera L-2 per Regione — {anni_avvi_map[0]}', font=dict(size=18, color='white', family='Inter'), x=0.5, xanchor='center'),
        updatemenus=[dict(type='buttons', direction='right', x=0.5, xanchor='center', y=1.08, yanchor='top',
            buttons=buttons_avvi_map, bgcolor='#14532D', bordercolor='#22C55E', borderwidth=1,
            font=dict(size=12, family='Inter', color='white'), active=0, pad=dict(r=6,l=6,t=6,b=6))],
        annotations=[
            dict(x=0.01, y=-0.02, xref='paper', yref='paper', text="Grigio scuro: Molise e Valle d'Aosta — nessun corso L-2 attivo",
                 showarrow=False, font=dict(size=10, color='#6BAA7A'), align='left'),
            dict(x=0.99, y=-0.02, xref='paper', yref='paper', text='Fonte: ANVUR Cruscotto PENTAHO — Avvii di carriera al primo anno (iC00a)',
                 showarrow=False, font=dict(size=10, color='#6BAA7A'), xanchor='right', align='right')],
        margin=dict(r=20, t=110, l=0, b=40), height=650,
        font=dict(family='Inter', size=12), paper_bgcolor=BG_PAPER, geo=dict(bgcolor=BG_PAPER))
    fig_avvi_map.update_geos(fitbounds='locations', visible=False)
    st.plotly_chart(fig_avvi_map, use_container_width=True)
    st.markdown("---")

    # G18 — Top 15 atenei avvii
    chart_header("Top 15 atenei per avvii di carriera",
        "I 15 atenei con il maggior numero di avvii di carriera al primo anno per anno accademico.",
        "Seleziona l'anno con i pulsanti. Passa il cursore sulle barre per il dettaglio per corso.")
    g_avvi4_corsi = df_avvi.groupby(['Anno accademico', 'Ateneo']).apply(
        lambda x: '<br>'.join([f"&nbsp;&nbsp;• {row['Nome Corso'].split(' - ')[1].strip() if ' - ' in row['Nome Corso'] else row['Nome Corso']}: <b>{int(row['Numeratore']):,}</b>"
            for _, row in x.sort_values('Numeratore', ascending=False).iterrows()])
    ).reset_index().rename(columns={0: 'lista_corsi'})
    g_avvi4_corsi_n = df_avvi.groupby(['Anno accademico', 'Ateneo'])['Nome Corso'].nunique().reset_index().rename(columns={'Nome Corso': 'n_corsi'})
    g_avvi4 = df_avvi.groupby(['Anno accademico', 'Ateneo', 'regione', 'macro'])['Numeratore'].sum().reset_index()
    g_avvi4 = g_avvi4.merge(g_avvi4_corsi_n, on=['Anno accademico', 'Ateneo'], how='left')
    g_avvi4 = g_avvi4.merge(g_avvi4_corsi, on=['Anno accademico', 'Ateneo'], how='left')
    anni_avvi4 = sorted(g_avvi4['Anno accademico'].unique())
    fig_avvi4 = go.Figure()
    for i, anno in enumerate(anni_avvi4):
        subset = g_avvi4[g_avvi4['Anno accademico']==anno].sort_values('Numeratore', ascending=False).head(15).sort_values('Numeratore', ascending=True).reset_index(drop=True)
        fig_avvi4.add_trace(go.Bar(x=subset['Numeratore'], y=subset['Ateneo'], orientation='h',
            marker=dict(color=[COLORI_MACRO.get(m, '#6B7280') for m in subset['macro']], line=dict(width=0), opacity=0.9),
            text=subset['Numeratore'].astype(int).apply(lambda x: f'{x:,}'),
            textposition='outside', textfont=dict(size=11, color='#86EFAC'),
            customdata=subset[['macro', 'n_corsi', 'lista_corsi']].values,
            hovertemplate='<b>%{y}</b><br>Avvii di carriera: <b>%{x:,}</b><br>Macro area: %{customdata[0]}<br>N° corsi L-2: <b>%{customdata[1]}</b><br>%{customdata[2]}<extra></extra>',
            visible=(i==0), showlegend=False))
    for macro, colore in COLORI_MACRO.items():
        fig_avvi4.add_trace(go.Bar(x=[None], y=[None], orientation='h', marker_color=colore, name=macro, visible=True))
    buttons_avvi4 = []
    for i, anno in enumerate(anni_avvi4):
        vis = [j==i for j in range(len(anni_avvi4))] + [True]*len(COLORI_MACRO)
        buttons_avvi4.append(dict(label=str(anno), method='update',
            args=[{'visible': vis}, {'title': dict(text=f'Top 15 Atenei per Avvii di Carriera L-2 — {anno}', font=dict(size=18, color='white', family='Inter'), x=0.5, xanchor='center')}]))
    fig_avvi4.update_layout(**PLOT_LAYOUT, title='',
        updatemenus=[dict(type='buttons', direction='right', x=0.5, xanchor='center', y=1.10, yanchor='top',
            buttons=buttons_avvi4, bgcolor='#14532D', bordercolor='#22C55E', borderwidth=1,
            font=dict(size=12, family='Inter', color='white'), active=len(anni_avvi4)-1, pad=dict(r=6,l=6,t=6,b=6))],
        annotations=[fonte_annotation('Fonte: ANVUR Cruscotto PENTAHO — Avvii di carriera al primo anno (iC00a)')],
        legend=dict(title=dict(text='Macro area', font=dict(color='#86EFAC')), font=dict(color='#D1FAE5'), bgcolor='rgba(0,0,0,0)', x=0.75, y=0.05),
        margin=dict(t=120, b=60, l=200, r=80), height=560, barmode='overlay')
    fig_avvi4.update_xaxes(title=dict(text='N° avvii di carriera', font=dict(color='#86EFAC')), showgrid=False, tickfont=dict(color='#86EFAC'), linecolor='#A7F3D0')
    fig_avvi4.update_yaxes(showgrid=False, tickfont=dict(size=12, color='#D1FAE5'), linecolor='#A7F3D0')
    st.plotly_chart(fig_avvi4, use_container_width=True)
    st.markdown("---")

    # G19 — Trend Lazio avvii
    chart_header("Avvii di carriera L-2 nel Lazio — per ateneo e corso",
        "Andamento degli avvii di carriera nei tre atenei laziali: La Sapienza, Tor Vergata e Tuscia.",
        "Passa il cursore sulle linee per vedere i valori anno per anno.")
    lazio_avvi = df_avvi[df_avvi['regione']=='Lazio'].copy()
    lazio_avvi['label'] = lazio_avvi.apply(lambda r: f"{r['Ateneo']} — {r['Nome Corso'].split(' - ')[1].strip()}", axis=1)
    lazio_avvi = lazio_avvi.groupby(['Anno accademico', 'Ateneo', 'label'])['Numeratore'].sum().reset_index().sort_values('Anno accademico')
    ordine_lazio = lazio_avvi.groupby('label')['Numeratore'].sum().sort_values(ascending=False).index.tolist()
    palette_lazio = {'La Sapienza': ['#F59E0B','#FCD34D','#F97316'], 'Tor Vergata': ['#22C55E'], 'Università della Tuscia': ['#34D399']}
    colori_label_avvi = {}
    contatori_avvi = {k: 0 for k in palette_lazio}
    for label in ordine_lazio:
        ateneo = label.split(' — ')[0]
        idx = contatori_avvi.get(ateneo, 0)
        colori_label_avvi[label] = palette_lazio.get(ateneo, ['#34D399'])[idx % len(palette_lazio.get(ateneo, ['#34D399']))]
        contatori_avvi[ateneo] = idx + 1
    fig_avvi9 = go.Figure()
    for label in ordine_lazio:
        df_lab = lazio_avvi[lazio_avvi['label']==label].sort_values('Anno accademico')
        colore = colori_label_avvi[label]
        ateneo = label.split(' — ')[0]
        corso = label.split(' — ')[1]
        dash = 'dot' if ateneo=='La Sapienza' and corso=='Biotecnologie' else 'solid' if ateneo!='La Sapienza' else 'dash'
        fig_avvi9.add_trace(go.Scatter(x=df_lab['Anno accademico'].astype(str), y=df_lab['Numeratore'],
            mode='lines+markers', name=label, line=dict(color=colore, width=2.5, dash=dash),
            marker=dict(size=8, color=colore, line=dict(color='#052E16', width=1.5)),
            hovertemplate=f'<b>{label}</b><br>Anno: %{{x}}<br>Avvii di carriera: <b>%{{y:,.0f}}</b><extra></extra>'))
        ultimo = df_lab.iloc[-1]
        fig_avvi9.add_annotation(x=str(int(ultimo['Anno accademico'])), y=ultimo['Numeratore'],
            text=f"<b>{int(ultimo['Numeratore'])}</b>", showarrow=False, font=dict(size=10, color=colore), xanchor='left', xshift=8)
    fig_avvi9.update_layout(**PLOT_LAYOUT, title='',
        annotations=[fonte_annotation('Fonte: ANVUR Cruscotto PENTAHO — Avvii di carriera al primo anno (iC00a)')],
        legend=dict(font=dict(color='#D1FAE5'), bgcolor='rgba(0,0,0,0)', x=0.99, y=0.99, xanchor='right', yanchor='top'),
        height=650, margin=dict(t=80, b=80, l=60, r=200))
    fig_avvi9.update_xaxes(title=dict(text='Anno accademico', font=dict(color='#86EFAC')), showgrid=False, tickfont=dict(color='#86EFAC'), linecolor='#A7F3D0')
    fig_avvi9.update_yaxes(title=dict(text='N° avvii di carriera', font=dict(color='#86EFAC')), gridcolor='#14532D', tickfont=dict(color='#86EFAC'), linecolor='#A7F3D0', rangemode='tozero')
    st.plotly_chart(fig_avvi9, use_container_width=True)
    st.markdown("---")

    # G20 — Bubble macro aree avvii
    chart_header("Quota avvii di carriera per macro area — trend 2020–2025",
        "Ogni bolla rappresenta la quota percentuale di avvii di carriera per macro area. La dimensione della bolla è proporzionale al numero assoluto di avvii.",
        "Passa il cursore sulle bolle per vedere quota e numero assoluto.")
    macro_avvi = df_avvi.groupby(['Anno accademico', 'macro'])['Numeratore'].sum().reset_index().dropna(subset=['macro'])
    totale_avvi_anno = macro_avvi.groupby('Anno accademico')['Numeratore'].sum().reset_index()
    totale_avvi_anno.columns = ['Anno accademico', 'totale']
    macro_avvi_pct = macro_avvi.merge(totale_avvi_anno, on='Anno accademico')
    macro_avvi_pct['pct'] = (macro_avvi_pct['Numeratore'] / macro_avvi_pct['totale'] * 100).round(1)
    OFFSET_AVVI = {'Nord': 2, 'Centro': 1, 'Sud': -1, 'Isole': -2}
    fig_avvi10 = go.Figure()
    for macro in ['Nord', 'Centro', 'Sud', 'Isole']:
        subset = macro_avvi_pct[macro_avvi_pct['macro']==macro].sort_values('Anno accademico').copy()
        subset['pct_offset'] = subset['pct'] + OFFSET_AVVI.get(macro, 0)
        fig_avvi10.add_trace(go.Scatter(x=subset['Anno accademico'].astype(str), y=subset['pct_offset'],
            mode='markers+text', name=macro,
            marker=dict(size=subset['Numeratore']/macro_avvi_pct['Numeratore'].max()*80+20,
                        color=COLORI_MACRO[macro], opacity=0.85, line=dict(color='#052E16', width=2)),
            text=subset['pct'].apply(lambda x: f'{x:.1f}%'), textposition='middle center',
            textfont=dict(size=10, color='white', family='Inter'),
            hovertemplate=f'<b>{macro}</b><br>Anno: %{{x}}<br>Quota: <b>%{{customdata[0]:.1f}}%</b><br>Avvii di carriera: <b>%{{customdata[1]:,}}</b><extra></extra>',
            customdata=list(zip(subset['pct'], subset['Numeratore'].astype(int)))))
    fig_avvi10.update_layout(**PLOT_LAYOUT, title='',
        annotations=[fonte_annotation('Fonte: ANVUR Cruscotto PENTAHO — Dimensione bolla = avvii assoluti')],
        legend=dict(font=dict(color='#D1FAE5'), bgcolor='rgba(0,0,0,0)', x=0.01, y=0.99),
        height=520, margin=dict(t=80, b=80, l=60, r=30))
    fig_avvi10.update_xaxes(title=dict(text='Anno accademico', font=dict(color='#86EFAC')), showgrid=False, tickfont=dict(color='#86EFAC'), linecolor='#A7F3D0')
    fig_avvi10.update_yaxes(title=dict(text='Quota (%)', font=dict(color='#86EFAC')), gridcolor='#14532D', ticksuffix='%', tickfont=dict(color='#86EFAC'), linecolor='#A7F3D0', range=[0, 70])
    st.plotly_chart(fig_avvi10, use_container_width=True)



    st.markdown("---")

    # Iscritti L-2
    chart_header("Iscritti L-8 Ingegneria — Italia (2020–2025)",
        "Numero totale di studenti iscritti a corsi L-8 Ingegneria in Italia per anno accademico.",
        "Passa il cursore sui pallini per vedere il valore esatto.")
    isc_naz = corso_l2.groupby('AnnoA')['Isc'].sum().reset_index()
    isc_naz = isc_naz[isc_naz['AnnoA'].str[:4].astype(int) >= 2020].copy()
    isc_naz['anno_short'] = isc_naz['AnnoA'].str[:4] + '/' + isc_naz['AnnoA'].str[7:9]
    chart_header("Iscritti L-8 Ingegneria — Italia (2020–2025)",
        "Numero totale di studenti iscritti a corsi L-8 Ingegneria in Italia per anno accademico.",
        "Passa il cursore sui pallini per vedere il valore esatto.")
    fig_isc = go.Figure()
    for _, row in isc_naz.iterrows():
        fig_isc.add_shape(type='line', x0=row['anno_short'], x1=row['anno_short'],
            y0=0, y1=row['Isc'], line=dict(color='#22C55E', width=3))
    fig_isc.add_trace(go.Scatter(x=isc_naz['anno_short'], y=isc_naz['Isc'], mode='markers+text',
        marker=dict(size=20, color=['#4ADE80' if a == '2024/25' else '#22C55E' for a in isc_naz['anno_short']], line=dict(color='white', width=2)),
        text=isc_naz['Isc'].apply(lambda x: f'{x:,.0f}'), textposition='top center',
        textfont=dict(color='#A7F3D0', size=12, family='Inter'),
        hovertemplate='<b>%{x}</b><br>Iscritti: <b>%{y:,.0f}</b><extra></extra>', name='Iscritti L-2'))
    fig_isc.add_hline(y=isc_naz['Isc'].mean(), line=dict(color='#F59E0B', width=2, dash='dash'),
        annotation_text=f'Media: {isc_naz["Isc"].mean():,.0f}', annotation_position='right',
        annotation_font=dict(color='#F59E0B', size=11))
    fig_isc.add_trace(go.Scatter(x=[None], y=[None], mode='lines',
        line=dict(color='#F59E0B', width=2, dash='dash'),
        name=f'Media periodo: {isc_naz["Isc"].mean():,.0f}', showlegend=True))
    fig_isc.update_layout(font=dict(family='Inter', size=12), plot_bgcolor=BG_PLOT, paper_bgcolor=BG_PAPER,
        title=dict(text='Iscritti L-8 Ingegneria — Italia (2020–2025)', font=dict(size=18, color='white', family='Inter'), x=0.5, xanchor='center'),
        showlegend=True, legend=dict(font=dict(color='#A7F3D0', size=11), bgcolor='rgba(0,0,0,0)', orientation='h', x=0.5, xanchor='center', y=1.08),
        margin=dict(t=100, b=80, l=70, r=100), height=520,
        annotations=[dict(x=0.99, y=-0.13, xref='paper', yref='paper',
            text='Fonte: MUR-USTAT — Iscritti L-8 Ingegneria per anno accademico',
            showarrow=False, font=dict(size=10, color='#6BAA7A'), xanchor='right', align='right')])
    fig_isc.update_xaxes(showgrid=False, tickfont=dict(color='#A7F3D0', size=13), linecolor='#1A3A1A')
    fig_isc.update_yaxes(gridcolor='#14532D', tickfont=dict(color='#A7F3D0'), linecolor='#1A3A1A', rangemode='tozero',
        title=dict(text='N° iscritti', font=dict(color='#A7F3D0')), range=[0, isc_naz['Isc'].max() * 1.2])
    st.plotly_chart(fig_isc, use_container_width=True)

# ─── PROFILO STUDENTI ─────────────────────────────────────────────────────────
elif sezione == "Profilo Studenti":
    st.markdown("## Profilo Studenti")
    st.markdown("---")
    chart_header("Indicatori chiave del profilo laureati L-2",
        "I tre indicatori riportano i valori del 2025 confrontati con un anno di riferimento selezionabile. I dati provengono dall'indagine AlmaLaurea sul Profilo dei Laureati.",
        "Seleziona l'anno di riferimento per il confronto con i pulsanti in alto.")
    anni_ref = [2020, 2021, 2022, 2023, 2024]
    indicatori_g5 = [('pct_soddisfatti','Soddisfatti del corso','#22C55E'),('pct_riiscrizione','Si reiscriverebbero','#34D399'),('pct_magistrale','Prosegue magistrale','#34D399')]
    val_2025 = {'pct_soddisfatti': 88.7, 'pct_riiscrizione': 73.1, 'pct_magistrale': 82.7}
    fig5 = go.Figure()
    for anno_ref in anni_ref:
        visible = (anno_ref == 2024)
        for col_idx, (col, titolo, colore) in enumerate(indicatori_g5):
            val_ref = float(alma_profilo[alma_profilo['anno']==anno_ref][col].values[0])
            fig5.add_trace(go.Indicator(mode='gauge+number+delta', value=val_2025[col],
                delta={'reference': val_ref, 'suffix': '%', 'relative': False, 'increasing': {'color': '#34D399'}, 'decreasing': {'color': '#F87171'}},
                number={'suffix': '%', 'font': {'size': 40, 'color': colore}},
                title={'text': f"<b style='color:#D1FAE5'>{titolo}</b><br><span style='font-size:11px;color:#6B7280'>2025 vs {anno_ref}</span>"},
                gauge={'axis': {'range': [0,100], 'ticksuffix': '%', 'tickfont': {'color': '#6B7280'}, 'tickcolor': '#A7F3D0'},
                    'bar': {'color': colore, 'thickness': 0.25}, 'bgcolor': '#14532D', 'borderwidth': 0,
                    'steps': [{'range': [0,50], 'color': '#14532D'}, {'range': [50,75], 'color': '#1A3D1A'}, {'range': [75,100], 'color': '#14532D'}],
                    'threshold': {'line': {'color': '#F59E0B', 'width': 3}, 'thickness': 0.75, 'value': val_ref}},
                domain={'x': [col_idx*0.34, col_idx*0.34+0.30], 'y': [0, 1]}, visible=visible))
    n_per_anno = len(indicatori_g5)
    buttons_g5 = []
    for i, anno_ref in enumerate(anni_ref):
        vis = []
        for j in range(len(anni_ref)): vis += [j==i]*n_per_anno
        buttons_g5.append(dict(label=f'vs {anno_ref}', method='update',
            args=[{'visible': vis}, {'title': dict(text=f'Profilo laureati L-2 — 2025 vs {anno_ref}', font=dict(size=20, color='white', family='Arial'), x=0.5, xanchor='center')}]))
    fig5.update_layout(
        title=dict(text='Profilo laureati L-8 Ingegneria — 2025 vs 2024', font=dict(size=20, color='white', family='Arial'), x=0.5, xanchor='center'),
        updatemenus=[dict(type='buttons', direction='right', x=0.5, xanchor='center', y=1.55, yanchor='top',
            buttons=buttons_g5, bgcolor='#14532D', bordercolor='#22C55E', borderwidth=1,
            font=dict(size=12, family='Arial', color='white'), active=len(anni_ref)-1, pad=dict(r=6,l=6,t=6,b=6))],
        height=420, margin=dict(t=195, b=60, l=30, r=30), font=dict(family='Arial', size=12), paper_bgcolor=BG_PAPER,
        annotations=[dict(x=0.5, y=-0.12, xref='paper', yref='paper',
            text="La linea arancione indica il valore dell'anno di riferimento selezionato",
            showarrow=False, font=dict(size=11, color='#6BAA7A'), align='center'),
            fonte_annotation('Fonte: AlmaLaurea — Profilo dei Laureati')])
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown("---")

    chart_header("Destinazione alla magistrale — dove proseguono gli studi",
        "Distribuzione percentuale degli studenti L-2 che si iscrivono alla laurea magistrale per destinazione geografica.",
        "Passa il cursore sulle barre per vedere la percentuale esatta di ciascun segmento.")
    g6 = alma_profilo[alma_profilo['anno']<=2025][['anno','pct_stesso_ateneo_magistrale','pct_magistrale_nord','pct_magistrale_centro']].copy()
    g6 = g6.dropna()
    g6['anno'] = g6['anno'].astype(str)
    g6['pct_altro'] = 100 - g6['pct_stesso_ateneo_magistrale'] - g6['pct_magistrale_nord'] - g6['pct_magistrale_centro']
    DEST = {'pct_stesso_ateneo_magistrale': ('Stesso ateneo','#22C55E'), 'pct_magistrale_nord': ('Altro Nord','#34D399'), 'pct_magistrale_centro': ('Centro Italia','#F59E0B'), 'pct_altro': ('Estero / Altro','#A7F3D0')}
    fig6 = go.Figure()
    for col, (label, color) in DEST.items():
        fig6.add_trace(go.Bar(x=g6['anno'], y=g6[col], name=label, marker=dict(color=color, line=dict(width=0), opacity=0.92),
            hovertemplate=f'<b>{label}</b><br>Anno %{{x}}<br><b>%{{y:.1f}}%</b><extra></extra>'))
    media_stesso = g6['pct_stesso_ateneo_magistrale'].mean()
    media_centro = g6['pct_magistrale_centro'].mean()
    fig6.update_layout(barmode='stack', **PLOT_LAYOUT, title='',
        legend=dict(orientation='h', y=1.08, x=0.5, xanchor='center', bgcolor='rgba(0,0,0,0)', font=dict(color='#D1FAE5', size=11)),
        annotations=[
            dict(x=0.5, y=-0.18, xref='paper', yref='paper',
                 text=f"<b style='color:white'>{media_stesso:.1f}%</b><span style='color:#86EFAC'> resta nello stesso ateneo · </span><b style='color:#F59E0B'>{media_centro:.1f}%</b><span style='color:#86EFAC'> sceglie un ateneo del Centro Italia</span>",
                 showarrow=False, font=dict(size=12, family='Inter'), align='center'),
            fonte_annotation('Fonte: AlmaLaurea — Profilo dei Laureati')],
        height=540, margin=dict(t=80, b=100, l=60, r=30))
    fig6.update_xaxes(title=dict(text='Anno di laurea', font=dict(color='#86EFAC')), showgrid=False, tickfont=dict(color='#86EFAC'), linecolor='#A7F3D0')
    fig6.update_yaxes(title=dict(text='%', font=dict(color='#86EFAC')), range=[0,100], ticksuffix='%', gridcolor='#14532D', tickfont=dict(color='#86EFAC'), linecolor='#A7F3D0')
    st.plotly_chart(fig6, use_container_width=True)

# ─── PERCORSO ACCADEMICO ──────────────────────────────────────────────────────
elif sezione == "Percorso Accademico":
    st.markdown("## Percorso Accademico")
    st.markdown("---")

    # G2 — Laureati
    chart_header("Laureati L-8 Ingegneria — Italia (2010–2024)",
        "Numero totale di laureati per anno solare. Le barre rosse corrispondono agli anni 2020 e 2021, durante i quali le sessioni di laurea hanno subito variazioni legate all'emergenza sanitaria.",
        "Passa il cursore sulle barre per vedere il valore esatto.")
    fig2 = px.bar(lau_naz, x='AnnoS', y='Lau', color='COVID', color_discrete_map={True:'#EF4444', False:'#22C55E'}, labels={'Lau':'N° Laureati','AnnoS':'Anno'}, text='Lau')
    fig2.update_traces(texttemplate='%{text:,}', textposition='outside', textfont=dict(size=9, color='#86EFAC'), marker_line_width=0, opacity=0.9)
    fig2.add_annotation(fonte_annotation('Fonte: MUR-USTAT · Laureati L-2 per anno solare'))
    fig2.update_layout(**PLOT_LAYOUT, title='', showlegend=False, margin=dict(t=80, b=60, l=60, r=30), height=500)
    fig2.update_xaxes(tickangle=-45, showgrid=False, tickfont=dict(color='#86EFAC'), tickmode='linear', dtick=1, linecolor='#A7F3D0')
    fig2.update_yaxes(gridcolor='#14532D', tickfont=dict(color='#86EFAC'), rangemode='tozero', linecolor='#A7F3D0')
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("---")

    # G11 — Donut
    chart_header("Cosa succede dopo il primo anno — L-8 Ingegneria",
        "Il grafico mostra la distribuzione degli avvii di carriera L-2 al termine del primo anno: chi prosegue nello stesso corso (iC14 ANVUR), chi cambia corso o ateneo ma resta nel sistema universitario (differenza iC21-iC14), e chi lascia l'università (complemento a 1 di iC21). La distinzione è importante: la maggior parte di chi non prosegue nello stesso corso non abbandona l'università, ma si trasferisce altrove.",
        "Seleziona l'anno con i pulsanti.")
    ic14 = df_ava2[df_ava2['CODICE']=='iC14'].copy()
    ic21 = df_ava2[df_ava2['CODICE']=='iC21'].copy()
    for df_ind in [ic14, ic21]:
        df_ind['ind_float'] = (df_ind['INDICATORE'].astype(str).str.strip().str.replace(',','.').str.replace(' ','').apply(lambda x: float(x) if x not in ['','nan','None'] else None))
    ic14_naz = ic14.groupby('ID_ANNO_ACCADEMICO')['ind_float'].mean().reset_index()
    ic14_naz.columns = ['anno','ic14']
    ic21_naz = ic21.groupby('ID_ANNO_ACCADEMICO')['ind_float'].mean().reset_index()
    ic21_naz.columns = ['anno','ic21']
    df_destino = ic14_naz.merge(ic21_naz, on='anno')
    df_destino['prosegue_stesso'] = (df_destino['ic14']*100).round(1)
    df_destino['cambia_corso'] = ((df_destino['ic21']-df_destino['ic14'])*100).round(1)
    df_destino['abbandona'] = ((1-df_destino['ic21'])*100).round(1)
    df_destino['anno'] = df_destino['anno'].astype(str)
    anni_g11 = sorted(df_destino['anno'].unique())
    fig11 = go.Figure()
    for i, anno in enumerate(anni_g11):
        row = df_destino[df_destino['anno']==anno].iloc[0]
        fig11.add_trace(go.Pie(
            labels=['Proseguono nello stesso corso','Cambiano corso o ateneo',"Lasciano l'università"],
            values=[row['prosegue_stesso'],row['cambia_corso'],row['abbandona']],
            hole=0.60, marker=dict(colors=['#22C55E','#F59E0B','#EF4444'], line=dict(color='#052E16', width=3)),
            textinfo='percent', textposition='outside', textfont=dict(size=13, color='white', family='Inter'),
            hovertemplate='<b>%{label}</b><br><b>%{value:.1f}%</b> degli avvii di carriera<extra></extra>',
            visible=(i==0), sort=False, pull=[0.03,0.03,0.03]))
    buttons_g11 = []
    for i, anno in enumerate(anni_g11):
        row = df_destino[df_destino['anno']==anno].iloc[0]
        vis = [j==i for j in range(len(anni_g11))]
        buttons_g11.append(dict(label=anno, method='update', args=[{'visible': vis}, {
            'title': dict(text=f"Cosa succede dopo il primo anno — {anno}", font=dict(size=18, color='white', family='Inter'), x=0.5, xanchor='center'),
            'annotations': [
                dict(text=f"<b>{row['prosegue_stesso']:.1f}%</b><br><span style='color:#86EFAC;font-size:11px'>resta nello<br>stesso corso</span>",
                     x=0.5, y=0.5, xref='paper', yref='paper', showarrow=False, font=dict(size=24, color='white', family='Inter'), align='center'),
                dict(x=0.99, y=-0.12, xref='paper', yref='paper', text='Fonte: ANVUR iC14 + iC21 · Media nazionale corsi L-2',
                     showarrow=False, font=dict(size=10, color='#6BAA7A'), align='right', xanchor='right')]}]))
    row0 = df_destino[df_destino['anno']==anni_g11[0]].iloc[0]
    fig11.update_layout(
        title=dict(text=f"Cosa succede dopo il primo anno — {anni_g11[0]}", font=dict(size=18, color='white', family='Inter'), x=0.5, xanchor='center'),
        updatemenus=[dict(type='buttons', direction='right', x=0.5, xanchor='center', y=1.12, yanchor='top',
            buttons=buttons_g11, bgcolor='#14532D', bordercolor='#22C55E', borderwidth=1,
            font=dict(size=12, family='Inter', color='white'), active=0, pad=dict(r=6,l=6,t=6,b=6))],
        annotations=[
            dict(text=f"<b>{row0['prosegue_stesso']:.1f}%</b><br><span style='color:#86EFAC;font-size:11px'>resta nello<br>stesso corso</span>",
                 x=0.5, y=0.5, xref='paper', yref='paper', showarrow=False, font=dict(size=24, color='white', family='Inter'), align='center'),
            dict(x=0.99, y=-0.12, xref='paper', yref='paper', text='Fonte: ANVUR iC14 + iC21 · Media nazionale corsi L-2',
                 showarrow=False, font=dict(size=10, color='#6BAA7A'), align='right', xanchor='right')],
        height=580, margin=dict(t=120, b=80, l=80, r=80), font=dict(family='Inter', size=12), paper_bgcolor=BG_PAPER,
        showlegend=True, legend=dict(font=dict(color='#D1FAE5', size=12), bgcolor='rgba(0,0,0,0)', orientation='h', x=0.5, xanchor='center', y=-0.08))
    st.plotly_chart(fig11, use_container_width=True)
    st.markdown("---")

    # G15 — iC02
    chart_header("% Laureati entro la Durata Normale del Corso — iC02",
        "Percentuale media nazionale di studenti L-2 che si laureano entro i 3 anni previsti dal corso. Il 2025 è evidenziato in giallo come dato più recente.",
        "Passa il cursore sulle barre per vedere il valore.")
    lau_naz_corso = df_lau_corso.groupby('Anno accademico')['Numeratore'].mean().reset_index()
    lau_naz_corso.columns = ['anno','pct']
    lau_naz_corso['pct'] = lau_naz_corso['pct'].round(1)
    media_lau_corso = lau_naz_corso['pct'].mean()
    fig_lau = go.Figure()
    for i, row in lau_naz_corso.iterrows():
        colore = '#F59E0B' if row['anno']==2025 else '#4ADE80'
        fig_lau.add_trace(go.Bar(x=[row['pct']], y=[str(int(row['anno']))], orientation='h',
            marker=dict(color=colore, cornerradius=4), text=f"{row['pct']:.1f}%", textposition='outside',
            textfont=dict(color='#D1FAE5', size=13),
            hovertemplate=f"<b>{int(row['anno'])}</b><br>Laureati in corso: <b>{row['pct']:.1f}%</b><extra></extra>",
            showlegend=False, width=0.5))
    fig_lau.add_trace(go.Scatter(x=[media_lau_corso, media_lau_corso],
        y=[str(int(lau_naz_corso['anno'].min())), str(int(lau_naz_corso['anno'].max()))],
        mode='lines', line=dict(color='#F59E0B', width=2, dash='dash'),
        name=f'Media periodo: {media_lau_corso:.1f}%', hoverinfo='skip'))
    fig_lau.update_layout(**PLOT_LAYOUT, title='', showlegend=True,
        legend=dict(font=dict(color='#D1FAE5', size=11), bgcolor='rgba(0,0,0,0)', orientation='h', x=0.5, xanchor='center', y=1.08),
        barmode='overlay', margin=dict(t=100, b=80, l=80, r=100), height=450,
        annotations=[dict(x=0.99, y=-0.13, xref='paper', yref='paper',
            text='Fonte: ANVUR Cruscotto PENTAHO — % laureati entro durata normale (iC02)',
            showarrow=False, font=dict(size=10, color='#6BAA7A'), xanchor='right', align='right')])
    fig_lau.update_xaxes(showgrid=False, tickfont=dict(color='#86EFAC'), linecolor='#A7F3D0', ticksuffix='%', range=[0,100])
    fig_lau.update_yaxes(tickfont=dict(color='#86EFAC', size=13), linecolor='#A7F3D0')
    st.plotly_chart(fig_lau, use_container_width=True)

# ─── VARIANTI DEL CORSO ───────────────────────────────────────────────────────
elif sezione == "Varianti del Corso":
    st.markdown("## Varianti del Corso")
    st.markdown("---")
    chart_header("Distribuzione immatricolati per variante di denominazione L-2",
        "Il treemap mostra le varianti di denominazione dei corsi L-2 in Italia, con dimensione proporzionale al numero di immatricolati e colore che indica il numero di atenei che offrono ciascuna variante.",
        "Seleziona l'anno con i pulsanti. Passa il cursore sui rettangoli per vedere immatricolati e numero di atenei.")
    df_var = df_anvur[df_anvur['Anno accademico']>=2020].copy()
    df_var['corso_nome'] = df_var['corso_nome'].str.title().str.strip()
    anni_tree = sorted(df_var['Anno accademico'].unique())
    fig8b = go.Figure()
    for i, anno in enumerate(anni_tree):
        subset = df_var[df_var['Anno accademico']==anno].groupby('corso_nome').agg(imm=('imm','sum'), n_atenei=('ateneo_short','nunique')).reset_index()
        fig8b.add_trace(go.Treemap(labels=subset['corso_nome'], parents=['L-8 Ingegneria (Varianti)']*len(subset),
            values=subset['imm'], customdata=subset[['n_atenei','imm']],
            hovertemplate='<b>%{label}</b><br>Immatricolati: <b>%{customdata[1]:,.0f}</b><br>N° atenei: <b>%{customdata[0]}</b><extra></extra>',
            marker=dict(colorscale=[[0,'#14532D'],[0.4,'#16A34A'],[0.7,'#4ADE80'],[1,'#BBF7D0']], colors=subset['n_atenei'],
                colorbar=dict(title=dict(text='N° atenei', font=dict(color='#86EFAC')), tickfont=dict(color='#86EFAC')),
                showscale=True, line=dict(color='#052E16', width=2)),
            textfont=dict(size=13, color='white', family='Inter'), visible=(i==0)))
    buttons_g8 = []
    for i, anno in enumerate(anni_tree):
        vis = [j==i for j in range(len(anni_tree))]
        buttons_g8.append(dict(label=str(anno), method='update',
            args=[{'visible': vis}, {'title': dict(text=f'Varianti L-2 per immatricolati — {anno}', font=dict(size=18, color='white', family='Inter'), x=0.5, xanchor='center')}]))
    fig8b.update_layout(title=dict(text=f'Varianti L-2 per immatricolati — {anni_tree[0]}', font=dict(size=18, color='white', family='Inter'), x=0.5, xanchor='center'),
        updatemenus=[dict(type='buttons', direction='right', x=0.5, xanchor='center', y=1.10, yanchor='top',
            buttons=buttons_g8, bgcolor='#14532D', bordercolor='#22C55E', borderwidth=1,
            font=dict(size=12, family='Inter', color='white'), active=0, pad=dict(r=6,l=6,t=6,b=6))],
        annotations=[fonte_annotation('Fonte: ANVUR Cruscotto · Colore = n° atenei che offrono la variante')],
        height=580, margin=dict(t=120, b=60, l=20, r=20), font=dict(family='Inter', size=12), paper_bgcolor=BG_PAPER)
    st.plotly_chart(fig8b, use_container_width=True)
    st.markdown("---")

    chart_header("Tasso di prosecuzione al II anno per variante",
        "Confronto del tasso medio di prosecuzione al II anno (iC14 ANVUR) per ciascuna variante di denominazione L-2, usando 'Biotecnologie' come baseline. Verde = superiore alla baseline, rosso = inferiore.",
        "Passa il cursore sulle barre per vedere il tasso di abbandono e il numero di atenei.")
    ic14_g12 = df_ava2[df_ava2['CODICE']=='iC14'].copy()
    ic14_g12['ind_float'] = (ic14_g12['INDICATORE'].astype(str).str.strip().str.replace(',','.').str.replace(' ','').apply(lambda x: float(x) if x not in ['','nan','None'] else None))
    ic14_g12['corso_norm'] = ic14_g12['NOME_CORSO'].str.title().str.strip()
    ic14_g12['corso_norm'] = ic14_g12['corso_norm'].str.replace('Biotecnologia$','Biotecnologie',regex=True)
    ic14_var = ic14_g12.groupby('corso_norm')['ind_float'].mean().reset_index()
    ic14_var.columns = ['corso','prosecuzione']
    ic14_var['prosecuzione_pct'] = (ic14_var['prosecuzione']*100).round(1)
    ic14_var['abbandono'] = (100-ic14_var['prosecuzione_pct']).round(1)
    ic14_atenei = ic14_g12.groupby('corso_norm')['CODE_UN'].nunique().reset_index()
    ic14_atenei.columns = ['corso','n_atenei']
    ic14_var = ic14_var.merge(ic14_atenei, on='corso')
    baseline = ic14_var[ic14_var['corso']=='Biotecnologie']['prosecuzione_pct'].values[0]
    ic14_var_sorted = ic14_var.sort_values('prosecuzione_pct', ascending=True).reset_index(drop=True)
    def get_colore_g12(row):
        if row['corso']=='Biotecnologie': return '#6B7280'
        elif row['prosecuzione_pct']>baseline: return '#34D399'
        else: return '#EF4444'
    ic14_var_sorted['colore'] = ic14_var_sorted.apply(get_colore_g12, axis=1)
    fig12 = go.Figure()
    fig12.add_trace(go.Bar(x=ic14_var_sorted['prosecuzione_pct'], y=ic14_var_sorted['corso'], orientation='h',
        marker=dict(color=ic14_var_sorted['colore'], line=dict(width=0), opacity=0.9),
        text=ic14_var_sorted.apply(lambda r: f"{r['prosecuzione_pct']:.1f}%  ({r['n_atenei']} aten{'eo' if r['n_atenei']==1 else 'ei'})", axis=1),
        textposition='outside', textfont=dict(size=10, color='#D1FAE5'),
        hovertemplate='<b>%{y}</b><br>Prosecuzione: <b>%{x:.1f}%</b><br>Abbandono: <b>%{customdata[0]:.1f}%</b><br>N° atenei: <b>%{customdata[1]}</b><extra></extra>',
        customdata=list(zip(ic14_var_sorted['abbandono'], ic14_var_sorted['n_atenei']))))
    fig12.add_vline(x=baseline, line=dict(color='#6BAA7A', width=2, dash='dash'))
    fig12.update_layout(**PLOT_LAYOUT, title='',
        annotations=[dict(x=baseline, y=1.02, xref='x', yref='paper', text=f'Baseline: {baseline:.1f}%', showarrow=False, font=dict(size=10, color='#86EFAC'), align='center'),
            fonte_annotation('Fonte: ANVUR iC14 · Verde = prosecuzione maggiore · Rosso = minore')],
        height=580, margin=dict(t=80, b=80, l=300, r=120))
    fig12.update_xaxes(title=dict(text='% prosecuzione al II anno', font=dict(color='#86EFAC')), showgrid=False, ticksuffix='%', tickfont=dict(color='#86EFAC'), linecolor='#A7F3D0', range=[0,110])
    fig12.update_yaxes(showgrid=False, tickfont=dict(size=10, color='#D1FAE5'), linecolor='#A7F3D0')
    st.plotly_chart(fig12, use_container_width=True)


# ─── TASSE E CONTRIBUTI ──────────────────────────────────────────────────────
elif sezione == "Tasse e Contributi":
    st.markdown("## Tasse e Contributi")
    st.markdown("---")
    chart_header("Contributo massimo annuo — L-8 Ingegneria",
        "Il grafico confronta il contributo onnicomprensivo massimo annuo per 10 atenei statali (campione) e l'unico ateneo non statale che offre L-8 Ingegneria in Italia (San Raffaele). I colori indicano la macro area geografica. La linea tratteggiata rossa rappresenta la tassa fissa del San Raffaele; la linea punteggiata grigia la media degli statali del campione.",
        "")

    dati_tasse = [
        ('San Raffaele',            'Non statale', 'Nord',   6640),
        ('Università di Pavia',     'Statale',     'Nord',   4538),
        ('Università di Milano',    'Statale',     'Nord',   4101),
        ('Bicocca',                 'Statale',     'Nord',   3736),
        ('Università di Trieste',   'Statale',     'Nord',   3281),
        ('Università di Padova',    'Statale',     'Nord',   3105),
        ('La Sapienza',             'Statale',     'Centro', 2924),
        ('Università di Pisa',      'Statale',     'Centro', 2900),
        ('Politecnico di Torino',   'Statale',     'Nord',   2601),
        ('Federico II Napoli',      'Statale',     'Sud',    2400),
        ('Politecnico di Bari',     'Statale',     'Sud',    2100),
    ]

    BG_PAPER_T = '#051A0A'
    BG_PLOT_T  = '#0F2D16'
    BG_CARD_T  = '#0A2010'
    COLORI_MACRO_T = {'Nord': '#22C55E', 'Centro': '#4ADE80', 'Sud': '#F59E0B'}
    C_NONST_T  = '#EF4444'
    C_GRIGIO_T = '#6B7280'
    C_TESTO_T  = '#A7F3D0'
    C_TESTO2_T = '#D1FAE5'

    df_t = pd.DataFrame(dati_tasse, columns=['Ateneo','Tipo','Macro','Contributo'])
    statali_t     = df_t[df_t['Tipo']=='Statale'].sort_values('Contributo', ascending=False).reset_index(drop=True)
    non_statali_t = df_t[df_t['Tipo']=='Non statale']
    media_statali_t = statali_t['Contributo'].mean()
    max_row_t = statali_t.loc[statali_t['Contributo'].idxmax()]
    min_row_t = statali_t.loc[statali_t['Contributo'].idxmin()]
    san_val_t = non_statali_t['Contributo'].values[0]
    n_t = len(statali_t)

    fig_tasse = make_subplots(
        rows=2, cols=1,
        row_heights=[0.28, 0.72],
        vertical_spacing=0.04,
        specs=[[{"type": "xy"}], [{"type": "xy"}]]
    )

    fig_tasse.add_trace(go.Scatter(
        x=[0], y=[0], mode='markers',
        marker=dict(opacity=0), showlegend=False, hoverinfo='skip'
    ), row=1, col=1)

    cards_t = [
        {'titolo': 'STATALE PIÙ CARO',
         'valore': f"€{max_row_t['Contributo']:,.0f}".replace(',','.'),
         'sub1': max_row_t['Ateneo'],
         'sub2': f"Macro area: {max_row_t['Macro']}",
         'colore': COLORI_MACRO_T[max_row_t['Macro']]},
        {'titolo': 'MEDIA STATALI',
         'valore': f"€{media_statali_t:,.0f}".replace(',','.'),
         'sub1': '10 atenei a campione',
         'sub2': 'su 42 statali totali',
         'colore': C_GRIGIO_T},
        {'titolo': 'STATALE MENO CARO',
         'valore': f"€{min_row_t['Contributo']:,.0f}".replace(',','.'),
         'sub1': min_row_t['Ateneo'],
         'sub2': f"Macro area: {min_row_t['Macro']}",
         'colore': COLORI_MACRO_T[min_row_t['Macro']]},
    ]

    shapes_t = []
    annotations_t = []
    card_y0_t = 0.76; card_y1_t = 0.99
    gaps_t = [0.01, 0.34, 0.67]; card_w_t = 0.31

    for i_t, card_t in enumerate(cards_t):
        x0_t = gaps_t[i_t]; x1_t = x0_t + card_w_t
        cx_t = (x0_t + x1_t) / 2
        cy_t = (card_y0_t + card_y1_t) / 2
        shapes_t.append(dict(type='rect', xref='paper', yref='paper',
                             x0=x0_t, x1=x1_t, y0=card_y0_t, y1=card_y1_t,
                             fillcolor=BG_CARD_T, line=dict(color=card_t['colore'], width=2.5),
                             layer='below', opacity=1))
        shapes_t.append(dict(type='rect', xref='paper', yref='paper',
                             x0=x0_t, x1=x1_t, y0=card_y1_t-0.032, y1=card_y1_t,
                             fillcolor=card_t['colore'], line=dict(width=0),
                             layer='above', opacity=1))
        annotations_t.append(dict(x=cx_t, y=card_y1_t-0.02, xref='paper', yref='paper',
                                   text=f"<b>{card_t['titolo']}</b>",
                                   font=dict(size=13, color='white', family='Inter'),
                                   showarrow=False, xanchor='center', yanchor='middle'))
        annotations_t.append(dict(x=cx_t, y=cy_t+0.055, xref='paper', yref='paper',
                                   text=f"<b>{card_t['valore']}</b>",
                                   font=dict(size=36, color=card_t['colore'], family='Inter'),
                                   showarrow=False, xanchor='center', yanchor='middle'))
        annotations_t.append(dict(x=cx_t, y=cy_t-0.04, xref='paper', yref='paper',
                                   text=f"<b>{card_t['sub1']}</b>",
                                   font=dict(size=13, color='#F5F5F7', family='Inter'),
                                   showarrow=False, xanchor='center', yanchor='middle'))
        annotations_t.append(dict(x=cx_t, y=card_y0_t+0.025, xref='paper', yref='paper',
                                   text=card_t['sub2'],
                                   font=dict(size=13, color=C_TESTO2_T, family='Inter'),
                                   showarrow=False, xanchor='center', yanchor='bottom'))

    for macro_t in ['Nord', 'Centro', 'Sud']:
        sub_t = statali_t[statali_t['Macro']==macro_t]
        fig_tasse.add_trace(go.Bar(
            x=sub_t['Ateneo'], y=sub_t['Contributo'],
            name=macro_t,
            marker=dict(color=COLORI_MACRO_T[macro_t], line=dict(width=0), opacity=0.9, cornerradius=4),
            text=sub_t['Contributo'].apply(lambda v: f'€{v:,.0f}'.replace(',','.')),
            textposition='outside',
            textfont=dict(color=C_TESTO_T, size=11, family='Inter'),
            hovertemplate='<b>%{x}</b><br>Contributo max: <b>€%{y:,.0f}</b><extra></extra>',
        ), row=2, col=1)

    fig_tasse.add_trace(go.Scatter(
        x=[-0.5, n_t-0.5], y=[san_val_t, san_val_t],
        mode='lines', name='Non statale (San Raffaele)',
        line=dict(color=C_NONST_T, width=2.5, dash='dash'),
        showlegend=True, xaxis='x3', yaxis='y2',
        hovertemplate=f'<b>San Raffaele: €{san_val_t:,.0f}</b><extra></extra>',
    ))
    fig_tasse.add_trace(go.Scatter(
        x=[-0.5, n_t-0.5], y=[media_statali_t, media_statali_t],
        mode='lines', name='Media statali',
        line=dict(color=C_TESTO2_T, width=2, dash='dot'),
        showlegend=False, xaxis='x3', yaxis='y2', hoverinfo='skip',
    ))

    annotations_t.append(dict(
        x=0.5, y=san_val_t, xref='paper', yref='y2',
        text=f"<b>San Raffaele (non statale): €{san_val_t:,.0f}</b>".replace(',','.'),
        showarrow=False, font=dict(size=13, color=C_NONST_T, family='Inter'),
        xanchor='center', yanchor='bottom', yshift=10,
        bgcolor='rgba(13,27,46,0.92)', bordercolor=C_NONST_T, borderwidth=1.5, borderpad=17,
    ))
    annotations_t.append(dict(
        x=0.99, y=media_statali_t, xref='paper', yref='y2',
        text=f"<b>Media statali: €{media_statali_t:,.0f}</b>".replace(',','.'),
        showarrow=False, font=dict(size=13, color=C_TESTO2_T, family='Inter'),
        xanchor='right', yanchor='bottom', yshift=8,
        bgcolor='rgba(13,27,46,0.9)', borderpad=8,
    ))
    annotations_t.append(dict(
        x=0.99, y=-0.08, xref='paper', yref='paper',
        text='⚠️ Dati su campione di 10 atenei statali su 42 totali · Fonte: siti ufficiali atenei a.a. 2024/25',
        showarrow=False, font=dict(size=10, color='#6BAA7A', family='Inter'),
        align='right', xanchor='right'
    ))

    fig_tasse.update_layout(
        title=dict(text='Contributo massimo annuo — L-8 Ingegneria',
                   font=dict(size=20, color='white', family='Inter'),
                   x=0.5, xanchor='center'),
        shapes=shapes_t, annotations=annotations_t,
        barmode='group',
        plot_bgcolor=BG_PLOT_T, paper_bgcolor=BG_PAPER_T,
        font=dict(family='Inter', size=12),
        legend=dict(font=dict(color=C_TESTO_T, size=12), bgcolor='rgba(0,0,0,0)',
                    orientation='h', x=0.5, xanchor='center', y=0.73),
        height=880,
        margin=dict(t=80, b=80, l=60, r=180),
        xaxis3=dict(overlaying='x2', range=[-0.5, n_t-0.5], visible=False, anchor='y2'),
    )
    fig_tasse.update_xaxes(visible=False, row=1, col=1)
    fig_tasse.update_yaxes(visible=False, row=1, col=1)
    fig_tasse.update_xaxes(showgrid=False, tickfont=dict(color=C_TESTO_T, size=11),
                            linecolor='#1A3A1A', tickangle=-20, row=2, col=1)
    fig_tasse.update_yaxes(showgrid=True, gridcolor='#14532D', tickfont=dict(color=C_TESTO2_T),
                            linecolor='#1A3A1A', tickprefix='€', range=[0, 8800], row=2, col=1)
    st.plotly_chart(fig_tasse, use_container_width=True)


# ─── ANALISI AVANZATA ─────────────────────────────────────────────────────────
elif sezione == "Analisi Avanzata":
    st.markdown("## Analisi Avanzata")
    st.markdown("---")
    chart_header("Studenti al II Anno con ≥ 2/3 CFU — iC16bis",
        "Grafico radiale che mostra la percentuale media nazionale di studenti che al II anno hanno acquisito almeno 2/3 dei CFU previsti (indicatore iC16bis ANVUR). Ogni arco rappresenta un anno.",
        "Passa il cursore sugli archi per vedere il valore per anno.")
    ic16_naz = df_ic16.groupby('Anno accademico')['Numeratore'].mean().reset_index()
    ic16_naz.columns = ['anno','pct']
    ic16_naz['pct'] = ic16_naz['pct'].round(1)
    media_ic16 = ic16_naz['pct'].mean()
    anni_ic16 = ic16_naz['anno'].tolist()
    valori_ic16 = ic16_naz['pct'].tolist()
    colori_radial = ['#22C55E','#10B981','#059669','#A78BFA','#C4B5FD','#4ADE80','#93C5FD']
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
        fig_radial.add_trace(go.Scatter(x=np.concatenate([x_outer,x_inner]), y=np.concatenate([y_outer,y_inner]),
            fill='toself', fillcolor=c, line=dict(color=c, width=0), name=f'{anno}: {val:.1f}%',
            hovertemplate=f'<b>{anno}</b><br>iC16bis: <b>{val:.1f}%</b><extra></extra>', mode='lines'))
        angolo_label = np.radians(val/100*360+3)
        r_label = raggio_esterno + 0.04
        fig_radial.add_annotation(x=r_label*np.cos(angolo_label), y=r_label*np.sin(angolo_label),
            text=f'{val:.1f}%', showarrow=False, font=dict(size=10, color=c, family='Inter'))
    fig_radial.update_layout(font=dict(family='Inter', size=12), plot_bgcolor=BG_PAPER, paper_bgcolor=BG_PAPER,
        title=dict(text='Studenti al II Anno con ≥ 2/3 CFU — iC16bis L-8 Ingegneria', font=dict(size=16, color='white', family='Inter'), x=0.5, xanchor='center'),
        showlegend=True, legend=dict(font=dict(color='#D1FAE5', size=11), bgcolor='rgba(0,0,0,0)', orientation='v', x=1.02, y=0.5, xanchor='left'),
        xaxis=dict(visible=False, range=[-1.3,1.5]), yaxis=dict(visible=False, range=[-1.3,1.3]),
        margin=dict(t=100, b=60, l=60, r=150), height=520,
        annotations=[dict(x=0, y=0.05, text=f'<b>{media_ic16:.1f}%</b>', showarrow=False, font=dict(size=26, color='white', family='Inter')),
            dict(x=0, y=-0.12, text='media nazionale', showarrow=False, font=dict(size=11, color='#86EFAC', family='Inter')),
            dict(x=0.99, y=-0.08, xref='paper', yref='paper', text='Fonte: ANVUR Cruscotto PENTAHO — iC16bis',
                 showarrow=False, font=dict(size=10, color='#6BAA7A'), xanchor='right', align='right')])
    st.plotly_chart(fig_radial, use_container_width=True)
    st.markdown("---")

    chart_header("Correlazione tra dimensione del corso e tasso di prosecuzione",
        "L'analisi mette in relazione il numero medio di immatricolati puri per corso (2020–2023) con il tasso di prosecuzione al II anno (iC14 ANVUR). Una correlazione negativa (r = -0.32) indica che i corsi più grandi tendono ad avere tassi di prosecuzione leggermente inferiori.",
        "Passa il cursore sui punti per vedere il nome del corso e dell'ateneo.")
    df_anvur_c = df_anvur.copy()
    df_anvur_c['CODICIONE'] = df_anvur_c['Nome Corso'].str.split(' - ').str[0].str.strip()
    lookup_c = df_anvur_c[['CODICIONE','ateneo_short']].drop_duplicates('CODICIONE')
    lookup_c['CODICIONE'] = lookup_c['CODICIONE'].astype(str)
    ic14_c = df_ava2[df_ava2['CODICE']=='iC14'].copy()
    ic14_c['ind_float'] = (ic14_c['INDICATORE'].astype(str).str.strip().str.replace(',','.').str.replace(' ','').apply(lambda x: float(x) if x not in ['','nan','None'] else None))
    imm_corso_c = df_ava2[(df_ava2['CODICE']=='iC00b')&(df_ava2['ID_ANNO_ACCADEMICO']>=2020)].copy()
    imm_corso_c['imm_val'] = (imm_corso_c['NUMERATORE'].astype(str).str.strip().str.replace(',','').str.replace('.000','').apply(lambda x: float(x) if x not in ['','nan','None'] else None))
    imm_media_c = imm_corso_c.groupby('CODICIONE')['imm_val'].mean().reset_index().rename(columns={'imm_val':'imm_media'})
    imm_media_c['CODICIONE'] = imm_media_c['CODICIONE'].astype(str)
    ic14_corso_c = ic14_c.groupby('CODICIONE')['ind_float'].mean().reset_index()
    ic14_corso_c.columns = ['CODICIONE','prosecuzione']
    ic14_corso_c['prosecuzione_pct'] = (ic14_corso_c['prosecuzione']*100).round(1)
    ic14_corso_c['CODICIONE'] = ic14_corso_c['CODICIONE'].astype(str)
    df_corr_c = imm_media_c.merge(ic14_corso_c, on='CODICIONE', how='inner')
    df_ava2_meta = df_ava2[['CODICIONE','NOME_CORSO','ID_REGIONE_MACRO_ISTAT','COMUNE']].drop_duplicates('CODICIONE').copy()
    df_ava2_meta['CODICIONE'] = df_ava2_meta['CODICIONE'].astype(str)
    df_corr_c = df_corr_c.merge(df_ava2_meta, on='CODICIONE', how='left').merge(lookup_c, on='CODICIONE', how='left')
    df_corr_c['macro'] = df_corr_c['ID_REGIONE_MACRO_ISTAT'].map({1:'Nord',2:'Nord',3:'Centro',4:'Sud e Isole'})
    df_corr_c['nome_display'] = df_corr_c['NOME_CORSO'].str.title().str.strip() + ' — ' + df_corr_c['ateneo_short'].fillna(df_corr_c['COMUNE'].str.title())
    df_plot_c = df_corr_c.dropna(subset=['imm_media','prosecuzione_pct','macro']).copy()
    slope, intercept, r, p, se = stats.linregress(df_plot_c['imm_media'], df_plot_c['prosecuzione_pct'])
    x_line = [df_plot_c['imm_media'].min(), df_plot_c['imm_media'].max()]
    y_line = [slope*x+intercept for x in x_line]
    COLORI_MACRO4 = {'Nord':'#22C55E','Centro':'#F59E0B','Sud e Isole':'#34D399'}
    fig_corr = go.Figure()
    for macro, colore in COLORI_MACRO4.items():
        sub = df_plot_c[df_plot_c['macro']==macro]
        fig_corr.add_trace(go.Scatter(x=sub['imm_media'], y=sub['prosecuzione_pct'], mode='markers', name=macro,
            marker=dict(color=colore, size=10, opacity=0.85, line=dict(color='#052E16', width=1.5)),
            hovertemplate='<b>%{customdata}</b><br>Immatricolati medi: <b>%{x:.0f}</b><br>Prosecuzione: <b>%{y:.1f}%</b><extra></extra>',
            customdata=sub['nome_display'].values))
    fig_corr.add_trace(go.Scatter(x=x_line, y=y_line, mode='lines', name='Trend',
        line=dict(color='#86EFAC', width=1.5, dash='dash'), hoverinfo='skip'))
    fig_corr.update_layout(**PLOT_LAYOUT, title='',
        annotations=[
            dict(x=0.98, y=0.98, xref='paper', yref='paper', text=f'r = {r:.3f} · p = {p:.3f} · n = {len(df_plot_c)}',
                 showarrow=False, font=dict(size=12, color='#86EFAC'), align='right', xanchor='right', bgcolor='#14532D', bordercolor='#A7F3D0', borderwidth=1),
            fonte_annotation('Fonte: ANVUR iC00b + iC14 · Ogni punto = un corso presso un ateneo')],
        legend=dict(font=dict(color='#D1FAE5'), bgcolor='rgba(0,0,0,0)', x=0.01, y=0.01),
        height=540, margin=dict(t=80, b=80, l=70, r=30))
    fig_corr.update_xaxes(title=dict(text='Immatricolati medi per anno (2020–2023)', font=dict(color='#86EFAC')), showgrid=True, gridcolor='#14532D', tickfont=dict(color='#86EFAC'), linecolor='#A7F3D0')
    fig_corr.update_yaxes(title=dict(text='Tasso prosecuzione al II anno (%)', font=dict(color='#86EFAC')), showgrid=True, gridcolor='#14532D', ticksuffix='%', tickfont=dict(color='#86EFAC'), linecolor='#A7F3D0')
    st.plotly_chart(fig_corr, use_container_width=True)


# ─── SINTESI ──────────────────────────────────────────────────────────────────
elif sezione == "Sintesi":
    st.markdown("# Sintesi dell'Analisi")
    st.markdown("---")
    chart_header("Scorecard — indicatori chiave per il sistema L-2", "", "")
    kpi_full = [
        {'label':'Avvii di carriera 2025','value':'N/D','delta':'trend crescita 2020-2025','color':'#4ADE80','bg':'#14532D'},
        {'label':'Crescita laureati','value':'+85%','delta':'2010 → 2024','color':'#4ADE80','bg':'#14532D'},
        {'label':'Soddisfatti del corso','value':'88.7%','delta':'AlmaLaurea 2025','color':'#34D399','bg':'#064E3B'},
        {'label':'Prosegue magistrale','value':'82.7%','delta':'AlmaLaurea 2025','color':'#34D399','bg':'#064E3B'},
        {'label':'Retribuzione media 2025','value':'€1.327','delta':'+17% vs 2020','color':'#34D399','bg':'#064E3B'},
        {'label':'Occupazione a 1 anno','value':'36.1%','delta':'82.7% fa magistrale','color':'#FCD34D','bg':'#78350F'},
        {'label':'Atenei telematici L-8','value':'6','delta':'su 53 atenei totali','color':'#FCD34D','bg':'#78350F'},
        {'label':'Politecnici attivi','value':'3','delta':'Milano, Torino, Bari','color':'#34D399','bg':'#064E3B'},
    ]
    fig7 = go.Figure()
    col_positions = [0.01,0.26,0.51,0.76]
    row_positions = [0.52,0.02]
    shapes = []
    annotations = []
    for idx, k in enumerate(kpi_full):
        r = idx // 4; c = idx % 4
        x0=col_positions[c]; x1=x0+0.23; y0=row_positions[r]; y1=y0+0.44; cx=(x0+x1)/2
        shapes.append(dict(type='rect',xref='paper',yref='paper',x0=x0,x1=x1,y0=y0,y1=y1,fillcolor=k['bg'],line=dict(color=k['color'],width=1.5),layer='below'))
        shapes.append(dict(type='rect',xref='paper',yref='paper',x0=x0,x1=x1,y0=y1-0.025,y1=y1,fillcolor=k['color'],line=dict(width=0),layer='above'))
        annotations.append(dict(x=cx,y=y1-0.048,xref='paper',yref='paper',text=f"<b>{k['label']}</b>",showarrow=False,font=dict(size=11,color='white',family='Inter'),align='center',xanchor='center'))
        annotations.append(dict(x=cx,y=(y0+y1)/2+0.04,xref='paper',yref='paper',text=f"<b>{k['value']}</b>",showarrow=False,font=dict(size=30,color=k['color'],family='Inter'),align='center',xanchor='center'))
        annotations.append(dict(x=cx,y=y0+0.055,xref='paper',yref='paper',text=k['delta'],showarrow=False,font=dict(size=10,color='#86EFAC',family='Inter'),align='center',xanchor='center'))
    fig7.update_layout(title=dict(text='Scorecard L-8 Ingegneria',font=dict(size=18,color='white',family='Inter'),x=0.5,xanchor='center'),
        shapes=shapes,annotations=annotations,height=600,margin=dict(t=80,b=40,l=20,r=20),
        paper_bgcolor=BG_PAPER,plot_bgcolor=BG_PAPER,xaxis=dict(visible=False,range=[0,1]),yaxis=dict(visible=False,range=[0,1]))
    st.plotly_chart(fig7, use_container_width=True)
    st.markdown("---")
    st.markdown("## Considerazioni principali")
    st.markdown("""<div class="section-card"><p><b style="color:#F5F5F7">Domanda e offerta formativa.</b> In Italia sono <b style="color:#22C55E">53 gli atenei</b> che offrono corsi L-8 Ingegneria, senza alcun ateneo telematico. L'offerta formativa è molto variegata, con corsi che spaziano dall'informatica pura all'elettronica, dalla biomedica all'automazione nell'anno accademico 2024/25, stabile dopo il calo post-pandemia.</p></div>""", unsafe_allow_html=True)
    st.markdown("""<div class="section-card"><p><b style="color:#F5F5F7">Distribuzione geografica.</b> Il <b style="color:#22C55E">Nord Italia</b> concentra il 50–55% degli avvii di carriera. Il <b style="color:#4ADE80">Centro Italia</b> conta 11 atenei attivi con circa il 27% degli avvii. Molise e Valle d'Aosta non ospitano atenei con corsi L-2 attivi.</p></div>""", unsafe_allow_html=True)
    st.markdown("""<div class="section-card"><p><b style="color:#F5F5F7">Profilo e soddisfazione.</b> L'<b style="color:#34D399">88.7%</b> dei laureati si dichiara soddisfatto del corso (AlmaLaurea 2025), con il <b style="color:#34D399">73.1%</b> che si reiscriverebbe allo stesso corso. La prosecuzione alla magistrale è alta: <b style="color:#F5F5F7">82.7%</b>. La retribuzione media netta mensile è di <b style="color:#22C55E">€1.327</b>.</p></div>""", unsafe_allow_html=True)
    st.markdown("""<div class="section-card"><p><b style="color:#F5F5F7">Tassazione.</b> Il contributo massimo annuo per gli <b style="color:#22C55E">atenei statali</b> varia da <b style="color:#F5F5F7">€2.100</b> (Politecnico di Bari) a <b style="color:#F5F5F7">€4.538</b> (Università di Pavia), con una media di circa <b style="color:#F5F5F7">€3.065</b> su un campione di 10 atenei statali. L'unico ateneo <b style="color:#EF4444">non statale</b> presente nell'offerta L-2 — il San Raffaele — applica una retta fissa di <b style="color:#EF4444">€6.640</b>, più del doppio della media degli statali.</p></div>""", unsafe_allow_html=True)
    st.markdown("""<div class="section-card"><p><b style="color:#F5F5F7">Percorso accademico.</b> In media circa il <b style="color:#22C55E">65-70%</b> degli immatricolati prosegue nello stesso corso al secondo anno (iC14), con variazioni tra famiglie di corso. Le <b style="color:#F59E0B">università telematiche</b> mostrano tassi di prosecuzione strutturalmente inferiori rispetto alle tradizionali.</p></div>""", unsafe_allow_html=True)
    st.markdown("""<div class="section-card" style="border-top: 3px solid #22C55E;">
    <p><b style="color:#F5F5F7">Il sistema L-8 Ingegneria</b> mostra un quadro articolato: domanda sostanzialmente stabile nel quinquennio 2020–2025, elevata soddisfazione dei laureati e forte propensione alla prosecuzione magistrale. Un aspetto da monitorare è il divario tra atenei tradizionali e telematici, sia in termini di prosecuzione che di sbocchi lavorativi.</p>
    <p style="color:#A7F3D0; font-size:0.82rem; margin-top:1.5rem;">Analisi basata su dati MUR-USTAT, ANVUR e AlmaLaurea · Periodo di riferimento: 2020–2025 · Centro Studi</p>
    </div>""", unsafe_allow_html=True)
