import streamlit as st
st.set_page_config(page_title="My Performance",page_icon="🎼",layout="wide",)

st.title("My Performance")
st.write("View your sheet music and listen back to your performance.")

sheet_music = st.session_state.get("sheet_music")
audio_file = st.session_state.get("audio_file")


if sheet_music is None or audio_file is None:
    st.warning("Upload your sheet music and recording on the main page first.")

else:
    st.subheader("Your Sheet Music")
    st.pdf(sheet_music,height=800,)
    st.divider()
    st.subheader("Your Recording")
    st.audio(audio_file,format="audio/wav",)

