import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="AI Turinio Generatorius (MVP)", layout="wide")
st.title("AI Turinio Generatorius (MVP)")

# Inicijuojame sesijos kintamuosius
if 'output' not in st.session_state:
    st.session_state['output'] = ""
if 'tema' not in st.session_state:
    st.session_state['tema'] = ""

# AI generatorius
generator = pipeline(
    "text-generation",
    model="gpt2"
)

# Teksto įvedimo laukas
st.session_state['tema'] = st.text_area(
    "Įveskite savo temą čia:", 
    st.session_state['tema'], 
    height=100
)

# Turinio tipas
tipas = st.selectbox(
    "Pasirinkite turinio tipą:", 
    ["Social post", "Email", "Reklama"]
)

# Mygtukai
col1, col2, col3 = st.columns(3)
with col1:
    generate = st.button("Generuoti")
with col2:
    clear = st.button("Išvalyti")
with col3:
    copy = st.button("Kopijuoti")

# Išvalymas
if clear:
    st.session_state['tema'] = ""
    st.session_state['output'] = ""

# Generavimas
if generate:
    if st.session_state['tema'].strip() != "":
        with st.spinner("Generuojama..."):
            prompt = f"Sukurk 3 {tipas} šiai temai: {st.session_state['tema']}, tonas: profesionalus."
            resu
