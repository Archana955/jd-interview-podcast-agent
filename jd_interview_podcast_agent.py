import os
import streamlit as st
from groq import Groq
from gtts import gTTS
from elevenlabs import ElevenLabs
import tempfile

# ------------------ Streamlit Setup ------------------

st.set_page_config(
    page_title="🎙️ JD → Interview Prep Podcast Agent",
    page_icon="🎧",
    layout="centered"
)

st.title("🎙️ Job Description → Interview Prep Podcast Agent")
st.write(
    "Convert job descriptions into audio-based interview preparation "
    "with questions, answer guidance, and skill gap alerts."
)

# ------------------ Sidebar: API Keys ------------------

st.sidebar.header("🔑 API Keys")

groq_api_key = st.sidebar.text_input("Groq API Key", type="password")
elevenlabs_key = st.sidebar.text_input(
    "ElevenLabs API Key (optional)", type="password"
)

# ------------------ Inputs ------------------

jd_text = st.text_area(
    "📄 Paste Job Description",
    height=250,
    placeholder="Paste the full job description here..."
)

round_type = st.selectbox(
    "🎯 Interview Round Type",
    ["HR Round", "Technical Round", "Managerial Round"]
)

experience_level = st.selectbox(
    "🧑‍💻 Experience Level",
    ["Fresher", "Mid-Level", "Senior"]
)

audio_length = st.selectbox(
    "⏱️ Audio Length",
    ["2 minutes", "5 minutes", "8 minutes"]
)

generate_btn = st.button(
    "🎧 Generate Interview Podcast",
    disabled=not all([groq_api_key, jd_text.strip()])
)

# ------------------ Main Logic ------------------

if generate_btn:
    with st.spinner("Generating interview podcast..."):
        try:
            # ---------- Groq LLM ----------
            client = Groq(api_key=groq_api_key)

            prompt = f"""
You are an expert interview coach.

Analyze the following job description and generate spoken interview preparation.

Job Description:
{jd_text}

Interview Round: {round_type}
Experience Level: {experience_level}
Preferred Audio Length: {audio_length}

Include:
1. Brief role overview
2. Five likely interview questions
3. High-level answer guidance
4. Skill gap alerts (commonly expected but missing skills)

Use simple conversational language suitable for audio.
Do not use markdown, bullets, or emojis.
"""

            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
                max_tokens=900,
            )

            interview_script = response.choices[0].message.content

            # ---------- TTS ----------
            audio_bytes = None
            tts_used = None

            # Try ElevenLabs first (optional)
            if elevenlabs_key:
                try:
                    eleven = ElevenLabs(api_key=elevenlabs_key)
                    audio_stream = eleven.text_to_speech.convert(
                        text=interview_script,
                        voice_id="JBFqnCBsd6RMkjVDRZzb",
                        model_id="eleven_multilingual_v2"
                    )

                    chunks = []
                    for chunk in audio_stream:
                        if chunk:
                            chunks.append(chunk)
                    audio_bytes = b"".join(chunks)
                    tts_used = "ElevenLabs"

                except Exception:
                    audio_bytes = None

            # Fallback: Google gTTS (FREE)
            if audio_bytes is None:
                tts = gTTS(text=interview_script)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                    tts.save(fp.name)
                    with open(fp.name, "rb") as f:
                        audio_bytes = f.read()
                tts_used = "Google gTTS (Free)"

            # ---------- Output ----------
            st.success(f"🎉 Podcast generated using {tts_used}")
            st.audio(audio_bytes, format="audio/mp3")

            st.download_button(
                "⬇️ Download Podcast",
                audio_bytes,
                "interview_prep_podcast.mp3",
                "audio/mp3"
            )

            with st.expander("📄 Generated Interview Script"):
                st.write(interview_script)

        except Exception as e:
            st.error(f"Error: {e}")