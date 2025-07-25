import streamlit as st
from simplifier import simplify_text
import pyttsx3
import pdfplumber
import pytesseract
from PIL import Image
from fpdf import FPDF
import base64
import os

st.set_page_config(page_title="AI Reading Assistant", layout="wide")

# --- Text-to-speech engine ---
engine = pyttsx3.init()

def speak_text(text, rate, pitch):
    engine.setProperty('rate', rate)
    engine.setProperty('pitch', pitch)
    engine.say(text)
    engine.runAndWait()

# --- Export functions ---
def export_text(text):
    st.download_button("⬇ Export Text", text, file_name="simplified_text.txt")

def export_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in text.split('\n'):
        pdf.multi_cell(190, 10, txt=line)
    pdf_output_path = "simplified_text.pdf"
    pdf.output(pdf_output_path)
    with open(pdf_output_path, "rb") as f:
        st.download_button("⬇ Export PDF", f.read(), file_name=pdf_output_path)

def export_audio(text):
    audio_path = "simplified_audio.mp3"
    engine.save_to_file(text, audio_path)
    engine.runAndWait()
    with open(audio_path, "rb") as f:
        st.download_button("⬇ Export Audio", f.read(), file_name=audio_path)

# --- Sidebar Settings ---
st.sidebar.header("⚙️ Settings")

with st.sidebar.expander("🖋 Font Settings", expanded=True):
    font_size = st.slider("Font Size", 14, 40, 20)
    use_dyslexic_font = st.checkbox("Use Dyslexic-Friendly Font")
    line_spacing = st.slider("Line Spacing", 1.0, 3.0, 1.5)

with st.sidebar.expander("🔊 Speech Settings", expanded=True):
    speech_rate = st.slider("Speech Rate", 100, 300, 180)
    voice_pitch = st.slider("Voice Pitch", 0, 100, 50)
    highlight = st.checkbox("Highlight words while speaking")

with st.sidebar.expander("🧠 AI Settings", expanded=True):
    model_level = st.selectbox("Simplification", ["a", "b", "c"])

# --- Main Layout ---
st.title("🧠 AI Reading Assistant")
st.caption("Supporting dyslexic learners with AI-powered text simplification")

col1, col2 = st.columns([3, 1])

with col1:
    uploaded_file = st.file_uploader("Upload Text/PDF", type=["txt", "pdf"])
    uploaded_img = st.file_uploader("Upload Image (OCR)", type=["png", "jpg", "jpeg"])

    text_input = ""
    if uploaded_file:
        if uploaded_file.name.endswith(".txt"):
            text_input = uploaded_file.read().decode("utf-8")
        elif uploaded_file.name.endswith(".pdf"):
            with pdfplumber.open(uploaded_file) as pdf:
                text_input = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    elif uploaded_img:
        img = Image.open(uploaded_img)
        text_input = pytesseract.image_to_string(img)
    else:
        sample = st.button("📄 Load Sample")
        if sample:
            text_input = """The quick brown fox jumps over the lazy dog. This is a complex sentence that contains various grammatical structures and vocabulary that might be challenging for some readers to understand. Artificial intelligence can help make reading more accessible by simplifying complex text while preserving the original meaning and intent of the author."""

    input_text = st.text_area("✍️ Text Input", text_input, height=250)

    if st.button("🔁 Simplify Text"):
        simplified_text = simplify_text(input_text)
    else:
        simplified_text = ""

    col_btn1, col_btn2, col_btn3 = st.columns(3)
    with col_btn1:
        if st.button("🗣 Speak Original"):
            speak_text(input_text, speech_rate, voice_pitch)
    with col_btn2:
        if st.button("🗣 Speak Simplified"):
            speak_text(simplified_text, speech_rate, voice_pitch)

    st.divider()

    st.subheader("🆚 Text Comparison")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Original Text**")
        st.write(input_text)
    with c2:
        st.markdown("**Simplified Text**")
        st.write(simplified_text)

    st.divider()
    st.subheader("📤 Export Options")
    export_text(simplified_text)
    export_pdf(simplified_text)
    export_audio(simplified_text)

# --- Apply font settings via custom CSS ---
font_family = "Comic Sans MS" if use_dyslexic_font else "Arial"
st.markdown(f"""
    <style>
        textarea, .stTextInput > div > div > input, .stTextArea textarea {{
            font-family: '{font_family}';
            font-size: {font_size}px;
            line-height: {line_spacing} !important;
        }}
    </style>
""", unsafe_allow_html=True)
