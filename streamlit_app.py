import streamlit as st
import requests

st.title("Prédiction du Stade de l'IRC")

# Dictionnaire de mappage pour afficher les labels clairs
field_labels = {
    "motif_admission_asthenie": "Motif(s) d'Admission/Asthénie",
    "motif_admission_alt_fonction": "Motif(s) d'Admission/Altération de la fonction rénale",
    "motif_admission_hta": "Motif(s) d'Admission/HTA",
    "motif_admission_oedeme": "Motif(s) d'Admission/Œdème",
    "motif_admission_diabete": "Motif(s) d'Admission/Diabète",
    "pm_hta": 'Personnels Médicaux/HTA',
    "pm_diabete1": 'Personnels Médicaux/Diabète 1',
    "pm_diabete2": 'Personnels Médicaux/Diabète 2',
    "pm_cardiovasculaire": 'Personnels Médicaux/Maladies Cardiovasculaire(Cardiopathie, AVC, preeclampsie)',
    "pm_pathologies_virales": 'Personnels Médicaux/Pathologies virales (HB, HC, HIV)',
    "symptome_anemie": 'Symptômes/Anémie',
    "symptome_nausees": 'Symptômes/Nausées',
    "symptome_hta": 'Symptômes/HTA',
    "symptome_flou_visuel": 'Symptômes/Flou visuel',
    "symptome_asthenie": 'Symptômes/Asthénie',
    "symptome_vomissements": 'Symptômes/Vomissements',
    "symptome_insomnie": 'Symptômes/Insomnie',
    "symptome_perte_poids": 'Symptômes/Perte de poids',
    "symptome_omi": 'Symptômes/OMI',
}

# Liste des champs booléens
bool_fields = list(field_labels.keys())

# Dictionnaire pour stocker les entrées utilisateur
input_data = {}

# Affichage des champs booléens
for field in bool_fields:
    label = field_labels[field]
    input_data[field] = 1 if st.radio(label, ["Non", "Oui"], key=field) == "Oui" else 0

# Sélection de l'état général à l'admission
etat = st.selectbox("Etat Général (EG) à l'Admission", ["Bon", "Acceptable", "Altéré"])
etat_map = {"Bon": 1, "Acceptable": 2, "Altéré": 3}
input_data['etat_general_admission'] = etat_map[etat]

# Résultats médicaux
input_data['uree'] = st.number_input("Urée (g/L)", 0.0, 5.0, 0.5)
input_data['creatinine'] = st.number_input("Créatinine (mg/L)", 0.0, 50.0, 1.0)

# Champ Anémie (en plus de symptôme anémie)
input_data['anemie'] = 1 if st.radio("Anémie", ["Non", "Oui"], key="anemie_finale") == "Oui" else 0

# Bouton de prédiction
if st.button("Prédire le Stade de l'IRC"):
    try:
        response = requests.post("http://backend:8000/predict", json=input_data)
        result = response.json().get("result", "Erreur dans la réponse du modèle.")
        st.success(result)
    except Exception as e:
        st.error(f"Erreur lors de la requête : {e}")
