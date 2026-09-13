import streamlit as st
import random
from parser.parser import parse_score
from audio.pipeline import run_audio_pipeline
from comparison.engine import run_comparison
from ai.feedback import generate_feedback
from utils.temp_files import save_uploaded_file
from parser.utils import get_all_notes
from parser.convert_to_musicxml import convert_pdf_to_musicxml
from comparison.timing_utils import assign_score_beat_times

language = st.selectbox(
    "Feedback Language",
    [
        "English",
        "Spanish",
        "French",
        "German",
        "Italian",
        "Portuguese",
        "Chinese",
        "Japanese",
        "Korean"
    ]
)

PIANO_FACTS = [
    "🎹 The piano is both a string instrument and a percussion instrument. Its strings make the sound, but hammers strike those strings to produce it.",

    "🇮🇹 The first piano was invented in Italy around 1709 by Bartolomeo Cristofori.",

    "🎼 The original name for the piano was 'gravicèmbalo col piano e forte,' which means something like 'harpsichord with soft and loud.'",

    "🔑 A standard piano has 88 keys, but some modern pianos have more. In 2018, Stuart & Sons introduced a piano with 108 keys.",

    "🎵 The colors of piano keys weren't always arranged the way they are today. In the 18th century, some keyboard instruments had the colors reversed!",

    "🎶 A standard 88-key piano covers seven octaves, giving it an enormous range of notes.",

    "⚡ A concert grand piano can repeat a note extremely quickly — its action can allow repetitions of around 14 times per second.",

    "🦶 The three traditional piano pedals have different jobs. The sustain pedal lets notes continue ringing, while the other pedals can change the sound or which strings are struck.",

    "🔧 Pianos need regular tuning because their strings can change pitch over time as the instrument settles and responds to its environment.",

    "🎹 A piano produces sound differently from a harpsichord. A piano's hammers strike the strings, while a harpsichord plucks them.",

    "📜 Before radios and recorded music became common, player pianos could play music automatically using rolls of paper with holes that controlled which notes were played.",

    "🎬 The piano has played important roles in movies, including films such as The Pianist and The Piano.",

    "💪 A piano's steel strings are under enormous tension. An acoustic piano can have more than 200 strings, each under substantial tension.",

    "🎹 Grand pianos generally allow faster note repetition than upright pianos because their hammers can return to their resting position more quickly.",

    "🎵 Some older pianos had ivory key coverings. Modern piano keys are generally made from plastic or other synthetic materials.",

    "🏛️ The piano became especially prominent during the Classical and Romantic periods, with composers such as Beethoven and Chopin writing extensively for it."
]

st.set_page_config(page_title="PianoCoach AI",page_icon="🎹",layout="wide")

st.markdown("""
<style>

    /* Main page spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1100px;
    }

    /* Title */
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        font-size: 1.15rem;
        opacity: 0.75;
        margin-bottom: 1.5rem;
    }

    /* Upload section */
    .upload-description {
        font-size: 0.9rem;
        opacity: 0.7;
        margin-top: -0.5rem;
        margin-bottom: 1rem;
    }

    /* Step labels */
    .step-number {
        font-size: 0.8rem;
        font-weight: 700;
        opacity: 0.6;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    /* Analyze button */
    .stButton > button {
        height: 3.2rem;
        font-size: 1.05rem;
        font-weight: 600;
        border-radius: 10px;
    }

    /* Result section */
    .feedback-header {
        font-size: 1.5rem;
        font-weight: 650;
        margin-bottom: 0.5rem;
    }

    /* Footer */
    .footer {
        text-align: center;
        opacity: 0.55;
        font-size: 0.85rem;
        margin-top: 2rem;
    }

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🎹 PianoCoach AI</div>',unsafe_allow_html=True)

st.markdown(
    '<div class="subtitle">'
    'Your personal AI piano instructor — practice, analyze, and improve.'
    '</div>',
    unsafe_allow_html=True
)

st.write(
    "Upload your sheet music and a recording of your performance. "
    "PianoCoach AI compares what you played with the music and gives you "
    "personalized feedback."
)

st.divider()

st.subheader("How it works")

step1, step2, step3 = st.columns(3)

with step1:
    st.markdown("**① Upload your music**")
    st.caption("Provide the sheet music for the piece you're practicing.")

with step2:
    st.markdown("**② Upload your recording**")
    st.caption("Upload a WAV recording of yourself playing the piece.")

with step3:
    st.markdown("**③ Get feedback**")
    st.caption("Your performance is analyzed and explained by your AI coach.")

st.write("")
st.divider()

st.subheader("🎼 Your Practice Session")

left_col, right_col = st.columns(2, gap="large")

with left_col:
    st.markdown('<div class="step-number">Step 1</div>',unsafe_allow_html=True)

    st.markdown("### 📄 Sheet Music")

    st.markdown(
        '<div class="upload-description">'
        'Upload the PDF sheet music for the piece you played.'
        '</div>',
        unsafe_allow_html=True
    )

    sheet_music = st.file_uploader("Choose your sheet music",type=["pdf"],label_visibility="collapsed")

    if sheet_music:
        st.success(f"✓ {sheet_music.name}")


with right_col:

    st.markdown('<div class="step-number">Step 2</div>',unsafe_allow_html=True)

    st.markdown("### 🎙️ Performance Recording")

    st.markdown(
        '<div class="upload-description">'
        'Upload a WAV audio recording of your performance.'
        '</div>',
        unsafe_allow_html=True
    )

    audio_file = st.file_uploader("Choose your recording",type=["wav"],label_visibility="collapsed")

    if audio_file:
        st.success(f"✓ {audio_file.name}")


if sheet_music is not None:
    st.session_state["sheet_music"] = sheet_music.getvalue()

if audio_file is not None:
    st.session_state["audio_file"] = audio_file.getvalue()


st.write("")
st.divider()


st.subheader("🎯 Ready to Analyze?")

if sheet_music and audio_file:
    st.success("Both files are ready! Click below to analyze your performance.")

else:
    st.info("Upload both your sheet music and recording to begin your analysis.")


analyze = st.button("🎹 Analyze My Performance",use_container_width=True)

if analyze:

    if not sheet_music or not audio_file:

        st.warning("⚠️ Please upload both your sheet music and recording before analyzing.")

    else:

        st.divider()

        st.header("📊 Analysis Results")

        with st.status("Analyzing your performance...",expanded=True) as status:
            fun_fact = random.choice(PIANO_FACTS)
            st.info(f"🎹 **Here's a fun piano fact while you wait:**\n\n{fun_fact}")
            st.write("📄 Processing sheet music...")

            sheet_music_path = save_uploaded_file(sheet_music)
            st.write("🎵 Reading musical notes...")
            musicxml_path = convert_pdf_to_musicxml(sheet_music_path)
            score = parse_score(musicxml_path)
            sheet_notes = get_all_notes(score)

            st.write("🎙️ Analyzing your recording...")
            audio_path = save_uploaded_file(audio_file)
            played_notes, _detected_tempo = run_audio_pipeline(audio_path)

            st.write("🔍 Comparing your performance...")
            assign_score_beat_times(sheet_notes)

            comparison_report = run_comparison(expected_notes=sheet_notes,played_notes=played_notes)
            status.update(label="Analysis complete!",state="complete",expanded=False)


        st.subheader("🤖 Your AI Piano Coach")

        with st.spinner("Generating your personalized feedback..."):

            feedback = generate_feedback(comparison_report,language)

        st.markdown('<div class="feedback-header">💬 Feedback</div>',unsafe_allow_html=True)

        st.write(feedback)


else:

    st.divider()

    st.info(
        "🎹 Your analysis will appear here after you upload your files "
        "and click **Analyze My Performance**."
    )


st.divider()

st.markdown(
    '<div class="footer">'
    'PianoCoach AI · Built with Streamlit 🎹<br>'
    'AI-generated feedback may contain mistakes. '
    'Use feedback as a practice guide, not a replacement for a piano teacher.'
    '</div>',
    unsafe_allow_html=True
)

######python -m streamlit run app.py
