import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="AI Turinio Generatorius (MVP)", layout="wide")
st.title("AI Turinio Generatorius (MVP)")

# Inicijuojame sesijos kintamuosius
if 'output' not in st.session_state:
    st.session_state['output'] = ""
if 'tema' not in st.session_state:
    st.session_state['tema'] = ""
if 'model_choice' not in st.session_state:
    st.session_state['model_choice'] = "gpt2"

# Teksto įvedimo laukas
st.session_state['tema'] = st.text_area(
    "Įveskite savo temą čia:", 
    st.session_state['tema'], 
    height=100
)

# AI modelių pasirinkimas (alternatyvos)
st.session_state['model_choice'] = st.selectbox(
    "Pasirinkite AI modelį:",
    ["gpt2", "bigscience/bloom-560m", "meta-llama/Llama-2-7b-hf"],
    index=["gpt2", "bigscience/bloom-560m", "meta-llama/Llama-2-7b-hf"].index(st.session_state['model_choice'])
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

# Saugumo patikra: tekstas per ilgas
MAX_CHARS = 300
if len(st.session_state['tema']) > MAX_CHARS:
    st.warning(f"Tekstas per ilgas! Prašome ne daugiau nei {MAX_CHARS} simbolių.")
    st.stop()

# Hugging Face Inference API generatorius
def get_generator(model_name):
    return pipeline(
        "text-generation",
        model=model_name,
        use_auth_token=st.secrets["HUGGINGFACE_TOKEN"]
    )

# Generavimas
if generate:
    if st.session_state['tema'].strip() != "":
        with st.spinner("Generuojama..."):
            prompt = f"Sukurk 3 {tipas} šiai temai: {st.session_state['tema']}, tonas: profesionalus."
            try:
                generator = get_generator(st.session_state['model_choice'])
                result = generator(
                    prompt,
                    max_new_tokens=150,
                    do_sample=True,
                    temperature=0.7
                )
                st.session_state['output'] = result[0]['generated_text']
            except Exception as e:
                st.error(f"Klaida generuojant tekstą: {e}")
    else:
        st.warning("Įveskite temą!")

# Rezultato blokas su scroll
if st.session_state['output']:
    st.text_area("Sugeneruotas tekstas:", st.session_state['output'], height=200)

# Modernus copy mygtukas su Tailwind stiliaus efektais
if copy and st.session_state['output']:
    safe_text = st.session_state['output'].replace("`", "\\`").replace("\n", "\\n")
    import streamlit.components.v1 as components
    components.html(f"""
        <div style="margin-top:10px;">
            <button 
                onclick="navigator.clipboard.writeText(`{safe_text}`); 
                         this.innerText='Tekstas nukopijuotas!'; 
                         setTimeout(()=>{{this.innerText='Kopijuoti';}}, 2000);" 
                style="
                    background-color: #4F46E5;
                    color: white;
                    font-weight: bold;
                    padding: 10px 20px;
                    border-radius: 8px;
                    border: none;
                    cursor: pointer;
                    transition: all 0.2s;
                "
                onmouseover="this.style.backgroundColor='#4338CA';"
                onmouseout="this.style.backgroundColor='#4F46E5';"
            >
                Kopijuoti
            </button>
        </div>
    """, height=70)
