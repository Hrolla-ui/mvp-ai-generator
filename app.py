import streamlit as st
from transformers import pipeline
import streamlit.components.v1 as components

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
            result = generator(
                prompt,
                max_new_tokens=150,
                do_sample=True,
                temperature=0.7
            )
            st.session_state['output'] = result[0]['generated_text']
    else:
        st.warning("Įveskite temą!")

# Rezultato blokas su scroll
if st.session_state['output']:
    st.text_area("Sugeneruotas tekstas:", st.session_state['output'], height=200)

# Automatinis kopijavimas į clipboard per JS
if copy and st.session_state['output']:
    # HTML + JS mygtukas
    components.html(f"""
        <button onclick="navigator.clipboard.writeText(`{st.session_state['output']}`)">
            Tekstas nukopijuotas į clipboard!
        </button>
    """, height=50)
