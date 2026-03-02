# 🎙️ Job Description → Interview Prep Podcast Agent

A GenAI-powered agent that converts job descriptions into **audio-based interview preparation** with interview questions, answer guidance, and skill gap alerts.

---

## What This Agent Does

1. Takes a **Job Description** as input
2. Analyzes role requirements using an LLM
3. Generates:

   * Role overview
   * Likely interview questions
   * High-level answer guidance
   * Skill gap alerts
4. Converts the output into a **podcast-style audio**
5. Plays and allows download of the audio

---

## Tech Stack

* Python
* Streamlit
* Groq API (LLM – LLaMA 3.1)
* Google gTTS (Free Text-to-Speech)
* ElevenLabs (Optional – better voice quality)

---

## Local Setup (Step by Step)

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/jd-interview-podcast-agent.git
cd jd-interview-podcast-agent
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**macOS / Linux**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the App

```bash
streamlit run jd_interview_podcast_agent.py
```

Open in browser:

```
http://localhost:8501
```

---

## API Keys

### Required

* **Groq API Key**
  Get it from: [https://console.groq.com](https://console.groq.com)

### Optional

* **ElevenLabs API Key** (for better audio quality)

If ElevenLabs is not provided, the app automatically uses **free Google gTTS**.

---

## Deployment (Streamlit Cloud)

### 1. Push Code to GitHub

```bash
git add .
git commit -m "Deploy JD Interview Prep Podcast Agent"
git push origin main
```

### 2. Deploy on Streamlit Cloud

1. Go to [https://share.streamlit.io](https://share.streamlit.io)
2. Click **New app**
3. Select your GitHub repository
4. Choose branch: `main`
5. File: `jd_interview_podcast_agent.py`
6. Click **Deploy**

---

## How to Use

1. Paste **Groq API key**
2. Paste **Job Description**
3. Select interview round and experience level
4. Click **Generate Interview Podcast**
5. Listen or download the audio 🎧

---

## License

MIT License

---

## Author

Archana Parmar
