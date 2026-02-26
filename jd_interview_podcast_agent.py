import os
import streamlit as st
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.run.agent import RunOutput
from elevenlabs import ElevenLabs

# ------------------ Streamlit UI Setup ------------------

st.set_page_config(
    page_title="🎙️ JD → Interview Prep Podcast Agent",
    page_icon="🎧",
    layout="centered"
)

st.title("🎙️ Job Description → Interview Prep Podcast Agent")
st.write(
    "Convert any job description into **audio-based interview preparation**, "
    "including likely questions, answer guidance, and skill gap alerts."
)

# ------------------ Sidebar: API Keys ------------------

st.sidebar.header("🔑 API Keys")

openai_key = st.sidebar.text_input("OpenAI API Key", type="password")
elevenlabs_key = st.sidebar.text_input("ElevenLabs API Key", type="password")

# ------------------ User Inputs ------------------

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
    disabled=not all([openai_key, elevenlabs_key, jd_text.strip()])
)

# ------------------ Main Logic ------------------

if generate_btn:
    with st.spinner("Analyzing JD and generating interview podcast..."):
        try:
            # Set environment variables
            os.environ["OPENAI_API_KEY"] = openai_key

            # ------------------ Agent Setup ------------------

            agent = Agent(
                name="JD Interview Prep Agent",
                model=OpenAIChat(id="gpt-4o"),
                instructions=[
                    "You are an expert interview coach.",
                    "Analyze the given job description carefully.",
                    "Extract key skills, tools, and responsibilities.",
                    "Generate likely interview questions based on the interview round.",
                    "Provide high-level answer guidance in simple spoken language.",
                    "Identify missing or weak skills and report them as skill gaps.",
                    "The output must be conversational and suitable for audio.",
                    "Do NOT use markdown, bullet symbols, or emojis in the response."
                ],
            )

            # ------------------ Agent Prompt ------------------

            prompt = f"""
Job Description:
{jd_text}

Interview Round: {round_type}
Experience Level: {experience_level}
Preferred Audio Length: {audio_length}

Generate:
1. A short role overview
2. 5 likely interview questions
3. High-level answer guidance for each question
4. Skill gap alert: skills that candidates often miss for this role
"""

            response: RunOutput = agent.run(prompt)
            interview_script = response.content

            if not interview_script:
                st.error("Failed to generate interview content.")
                st.stop()

            # ------------------ ElevenLabs Audio Generation ------------------

            eleven_client = ElevenLabs(api_key=elevenlabs_key)

            audio_stream = eleven_client.text_to_speech.convert(
                text=interview_script,
                voice_id="JBFqnCBsd6RMkjVDRZzb",
                model_id="eleven_multilingual_v2"
            )

            audio_chunks = []
            for chunk in audio_stream:
                if chunk:
                    audio_chunks.append(chunk)

            audio_bytes = b"".join(audio_chunks)

            # ------------------ Output ------------------

            st.success("🎉 Interview Prep Podcast Generated!")
            st.audio(audio_bytes, format="audio/mp3")

            st.download_button(
                label="⬇️ Download Podcast",
                data=audio_bytes,
                file_name="interview_prep_podcast.mp3",
                mime="audio/mp3"
            )

            with st.expander("📄 Generated Interview Script"):
                st.write(interview_script)

        except Exception as e:
            st.error(f"Something went wrong: {e}")