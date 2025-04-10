import streamlit as st
import requests

# Configuration de la page
st.set_page_config(
    page_title="Prédiction du Stade de l'IRC",
    layout="wide",
    initial_sidebar_state="auto"
)

# CSS pour style arrondi et fond bleu
st.markdown("""
    <style>
        .blue-container {
            background-color: #eaf2f8;
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 20px;
        }
        .stButton>button {
            background-color: #2E86C1;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 0.5em 1em;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown(
    "<h1 style='text-align: center; color: #2E86C1;'>🩺 Prédiction du Stade de l'Insuffisance Rénale Chronique (IRC)</h1><hr>",
    unsafe_allow_html=True
)

# --- Motifs d'admission ---
st.markdown("<div class='blue-container'>", unsafe_allow_html=True)
st.markdown("## 🧾 Motifs d'admission")
col1, col2 = st.columns(2)
with col1:
    input_data = {
        "motif_admission_asthenie": 1 if st.radio("Asthénie", ["Non", "Oui"]) == "Oui" else 0,
        "motif_admission_alt_fonction": 1 if st.radio("Altération fonction rénale", ["Non", "Oui"]) == "Oui" else 0,
        "motif_admission_hta": 1 if st.radio("HTA", ["Non", "Oui"]) == "Oui" else 0,
    }
with col2:
    input_data["motif_admission_oedeme"] = 1 if st.radio("Œdème", ["Non", "Oui"]) == "Oui" else 0
    input_data["motif_admission_diabete"] = 1 if st.radio("Diabète", ["Non", "Oui"]) == "Oui" else 0
st.markdown("</div>", unsafe_allow_html=True)

# --- Antécédents médicaux ---
st.markdown("<div class='blue-container'>", unsafe_allow_html=True)
st.markdown("## 🧬 Antécédents médicaux")
col3, col4 = st.columns(2)
with col3:
    input_data["pm_hta"] = 1 if st.radio("HTA", ["Non", "Oui"], key="pm_hta") == "Oui" else 0
    input_data["pm_diabete1"] = 1 if st.radio("Diabète Type 1", ["Non", "Oui"], key="pm_diab1") == "Oui" else 0
    input_data["pm_diabete2"] = 1 if st.radio("Diabète Type 2", ["Non", "Oui"], key="pm_diab2") == "Oui" else 0
with col4:
    input_data["pm_cardiovasculaire"] = 1 if st.radio("Maladies cardiovasculaires", ["Non", "Oui"]) == "Oui" else 0
    input_data["pm_pathologies_virales"] = 1 if st.radio("Pathologies virales", ["Non", "Oui"]) == "Oui" else 0
st.markdown("</div>", unsafe_allow_html=True)

# --- Symptômes ---
st.markdown("<div class='blue-container'>", unsafe_allow_html=True)
st.markdown("## 🤒 Symptômes")
cols = st.columns(3)
symptomes = [
    "symptome_anemie", "symptome_nausees", "symptome_hta",
    "symptome_flou_visuel", "symptome_asthenie", "symptome_vomissements",
    "symptome_insomnie", "symptome_perte_poids", "symptome_omi"
]
for i, field in enumerate(symptomes):
    label = field.replace("symptome_", "").replace("_", " ").capitalize()
    input_data[field] = 1 if cols[i % 3].radio(label, ["Non", "Oui"], key=field) == "Oui" else 0
st.markdown("</div>", unsafe_allow_html=True)

# --- Examens biologiques ---
st.markdown("<div class='blue-container'>", unsafe_allow_html=True)
st.markdown("## 🧪 Examens biologiques et état général")

col_urea, col_creatinine, col_etat = st.columns([1, 1, 2])
with col_urea:
    input_data['uree'] = st.number_input("Urée (g/L)", 0.0, 5.0, 0.5)
with col_creatinine:
    input_data['creatinine'] = st.number_input("Créatinine (mg/L)", 0.0, 50.0, 1.0)
with col_etat:
    etat = st.selectbox("État Général à l'Admission", ["Bon", "Acceptable", "Altéré"])
    input_data['etat_general_admission'] = {"Bon": 1, "Acceptable": 2, "Altéré": 3}[etat]

input_data['anemie'] = 1 if st.radio("Anémie (confirmée)", ["Non", "Oui"], key="anemie_finale") == "Oui" else 0
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# --- Prédiction ---
st.markdown("## 🎯 Résultat de la prédiction")
if st.button("🔍 Prédire le Stade de l'IRC"):
    try:
        response = requests.post("https://backend-ta25.onrender.com/predict", json=input_data)
        result = response.json().get("result", "Erreur dans la réponse du modèle.")
        st.success(f"✅ {result}")
    except Exception as e:
        st.error(f"❌ Erreur lors de la requête : {e}")
