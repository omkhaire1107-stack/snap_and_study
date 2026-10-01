# 📚 Snap & Study

Snap & Study is an AI-powered study assistant built with **Streamlit** and **Google Gemini**.

Students can ask questions or upload images of study material such as textbook pages, diagrams, notes, and programming problems. Gemini analyzes the material and provides clear, student-friendly explanations.

The app can also generate a concise study summary from the conversation and send it directly to the student's email using **Gmail SMTP**.

## ✨ Features

- 💬 Ask study-related questions
- 📷 Upload images of study material
- 🤖 AI-powered explanations using Google Gemini
- 📝 Step-by-step explanations
- 📚 Generate a concise study summary
- 📧 Send study summaries through Gmail
- 🔐 Secure API credentials using Streamlit Secrets

## 🛠️ Technologies Used

- **Python**
- **Streamlit**
- **Google Gemini API**
- **Gmail SMTP**
- **google-genai**
- **smtplib**

## 📁 Project Structure

```text
snap-and-study/
│
├── app.py
├── prompts.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── .streamlit/
    └── secrets.toml.example

The actual .streamlit/secrets.toml file is kept locally and is not committed to GitHub.

⚙️ Local Setup
1. Clone the repository
git clone https://github.com/omkhaire1107-stack/snap_and_study
cd snap-and-study
2. Create a virtual environment
python -m venv venv

On Windows:

venv\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
4. Configure Streamlit Secrets

Create the following file:

.streamlit/secrets.toml

Add:

GEMINI_API_KEY = "your_gemini_api_key"
GMAIL_ADDRESS = "your_gmail_address"
GMAIL_APP_PASSWORD = "your_gmail_app_password"

Replace the placeholder values with your actual credentials.

5. Run the application
streamlit run app.py

The application will open in your browser.

📧 Gmail Setup

Snap & Study uses Gmail SMTP to send study summaries.

A Google App Password is required. Your normal Gmail password should not be used.

To configure Gmail:

Enable 2-Step Verification on your Google account.
Create a Google App Password.
Add the App Password to .streamlit/secrets.toml.
Keep .streamlit/secrets.toml private.
🔑 Required Secrets
Secret	Purpose
GEMINI_API_KEY	Authenticates requests to Google Gemini
GMAIL_ADDRESS	Gmail account used to send summaries
GMAIL_APP_PASSWORD	App Password used for Gmail SMTP authentication
🚀 How Snap & Study Works
        Student
           │
           ▼
   Enter Name + Email
           │
           ▼
 Ask Question / Upload Image
           │
           ▼
      Google Gemini
           │
           ▼
     AI Explanation
           │
           ▼
   Send to Email 📧
           │
           ▼
   Generate Study Summary
           │
           ▼
      Gmail SMTP
           │
           ▼
      Student Inbox
🧠 AI Assistance

The application uses Google Gemini to understand questions and uploaded study material and generate explanations that are structured for students.

The prompts are maintained separately in prompts.py to keep the AI instructions organized and easier to modify.

🔐 Security

Sensitive credentials are stored using Streamlit Secrets.

The following file must never be committed to GitHub:

.streamlit/secrets.toml

The repository contains:

.streamlit/secrets.toml.example

as a template for the required configuration.

📌 Project Goal

Snap & Study aims to make studying more interactive by allowing students to snap or upload study material, understand it with AI, and save the explanation through email.

👨‍💻 Author

Omkar Khaire
