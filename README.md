Copyright © 2026 Arnav Tikole. All rights reserved.

# PianoCoach AI 🎹

PianoCoach AI is a piano practice app that uses AI to help students understand how they played a piece.

You upload your **sheet music** and a **recording of your performance**, and the app compares them and gives you feedback.

## Why I Made This

I made PianoCoach AI because practicing piano can sometimes be difficult without a teacher there to give immediate feedback.

I wanted to build something that could listen to a student's performance, compare it with the sheet music, and explain what they could improve.

## What It Can Do

* Upload sheet music as a PDF
* Upload a piano recording as a WAV file
* Read the sheet music and turn it into note data
* Analyze the recorded performance
* Compare the expected and played notes
* Find:
  * Wrong notes
  * Wrong octaves
  * Missed notes
  * Extra notes
  * Timing mistakes
* Analyze performance by measure
* Give AI-generated feedback
* Give suggestions for improving
* View your sheet music and recording

## How It Works

The app has a few main steps:

**1. Sheet Music**

Audiveris converts the PDF sheet music into MusicXML. The Python code then reads the MusicXML and turns it into structured note data.

**2. Recording**

Basic Pitch and librosa analyze the recording and determine which notes were played and when they were played.

**3. Comparison**

The comparison system compares the expected notes from the sheet music with the notes detected from the recording.

It looks for things like wrong notes, missed notes, extra notes, wrong octaves, and timing mistakes.

**4. AI Feedback**

The structured comparison results are sent to an AI model. The AI explains the results in simple language and gives suggestions for improving.

The AI does not independently re-analyze the recording. It uses the results produced by the comparison system.

## Technologies

* Python
* Streamlit
* OpenAI API
* Audiveris
* Basic Pitch
* librosa
* MusicXML

## Requirements

You need:

* Python 3.11+
* Audiveris
* The packages in `requirements.txt`
* An OpenAI API key

### Audiveris

Audiveris is used to convert sheet music PDFs into MusicXML.

It is a separate program, so it **does not get installed with `requirements.txt`**.

You need to install Audiveris separately before running the app.

## Installation

Clone the repository:

    git clone <YOUR_GITHUB_REPOSITORY_URL>
    cd AI_Piano_Coach

Create a virtual environment:

    python -m venv .venv

On Windows, activate it with:

    .venv\Scripts\activate

Install the Python packages:

    pip install -r requirements.txt

## OpenAI API Key

PianoCoach AI uses the OpenAI API to generate AI feedback.

You will need your own OpenAI API key to use the AI feedback features.

### Create the Secrets File

Inside the project folder, create a folder called:

    .streamlit

Inside `.streamlit`, create a file called:

    secrets.toml

Your project should look like this:

    AI_Piano_Coach/
    ├── .streamlit/
    │   └── secrets.toml
    ├── ai/
    ├── audio/
    ├── comparison/
    ├── pages/
    ├── parser/
    ├── tests/
    ├── utils/
    ├── app.py
    ├── requirements.txt
    └── README.md

Open `secrets.toml` and add:

    OPENAI_API_KEY = "your-api-key-here"

Replace `"your-api-key-here"` with your own OpenAI API key.

**Do not share or upload your API key to GitHub.**

Make sure `.streamlit/secrets.toml` is included in your `.gitignore` file so your API key is not accidentally uploaded to GitHub.

## Running the App

Run:

    python -m streamlit run app.py

Then open the local URL that Streamlit gives you.

## Project Structure

    AI_Piano_Coach/
    ├── .streamlit/
    │   └── secrets.toml
    ├── ai/
    ├── audio/
    ├── comparison/
    ├── pages/
    ├── parser/
    ├── tests/
    ├── utils/
    ├── app.py
    ├── requirements.txt
    └── README.md

## Demo

A live version of PianoCoach AI will be available here:

**[Try PianoCoach AI](YOUR_APP_URL)**

🎹 **Thanks for checking out PianoCoach AI!**