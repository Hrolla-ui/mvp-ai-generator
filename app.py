import streamlit as st
from transformers import pipeline

st.title("AI Turinio Generatorius (MVP)")

generator = pipeline(
    "text-generation",
    model="bigscience/bloom-560m",
    use_auth_token=st.secrets["HUGGINGFACE_API_TOKEN"]
)

tema = st.text_input("Įveskite temą:")
tipas = st.selectbox("Pasirinkite turinio tipą:", ["Social post", "Email", "Reklama"])

if st.button("Generuoti"):
    if tema:
        with st.spinner("Generuojama..."):
            prompt = f"Sukurk 3 {tipas} šiai temai: {tema}, tonas: profesionalus."
            result = generator(
                prompt,
                max_new_tokens=50,  # mažiau ir saugiau CPU
                do_sample=True,
                temperature=0.7
            )
            st.text_area("Sugeneruotas tekstas:", result[0]['generated_text'], height=200)
    else:
        st.warning("Įveskite temą!")
