import smtplib
from email.mime.text import MIMEText

import streamlit as st
from google import genai
from google.genai import types

from prompts import SUMMARY_REQUEST_PROMPT, SYSTEM_PROMPT


MODEL_NAME = "gemini-3.5-flash"

st.set_page_config(
    page_title="Snap & Study",
    page_icon="📚"
)


# ---------------------------------------------------------
# Secrets
# ---------------------------------------------------------

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
GMAIL_ADDRESS = st.secrets["GMAIL_ADDRESS"]
GMAIL_APP_PASSWORD = st.secrets["GMAIL_APP_PASSWORD"]


# ---------------------------------------------------------
# Clients
# ---------------------------------------------------------

@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key=GEMINI_API_KEY)


gemini_client = get_gemini_client()


# ---------------------------------------------------------
# Message functions
# ---------------------------------------------------------

def render_message(message):
    with st.chat_message(message["role"]):

        if message["kind"] == "text":
            st.write(message["content"])

        elif message["kind"] == "image":
            st.image(message["content"])


def add_message(role, kind, content):
    st.session_state.messages.append(
        {
            "role": role,
            "kind": kind,
            "content": content,
        }
    )

    render_message(st.session_state.messages[-1])


# ---------------------------------------------------------
# Gemini function
# ---------------------------------------------------------

def ask_gemini(parts):
    try:
        response = st.session_state.chat.send_message(parts)
        return response.text

    except Exception as error:
        return f"Sorry, something went wrong: {error}"


# ---------------------------------------------------------
# Gmail SMTP function
# ---------------------------------------------------------

def send_email(to_address, subject, body):
    try:
        message = MIMEText(body)

        message["Subject"] = subject
        message["From"] = GMAIL_ADDRESS
        message["To"] = to_address

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(
                GMAIL_ADDRESS,
                GMAIL_APP_PASSWORD
            )

            server.send_message(message)

        return True, "Email sent successfully."

    except Exception as error:
        return False, str(error)


# =========================================================
# STEP 1: ONBOARDING
# =========================================================

if "onboarded" not in st.session_state:

    st.title("📚 Snap & Study")

    st.caption(
        "Snap it. Understand it. Save the explanation."
    )

    with st.form("onboarding_form"):

        name = st.text_input(
            "Your name"
        )

        email = st.text_input(
            "Email address",
            placeholder="you@example.com",
            help="The study summary will be sent to this email address."
        )

        submitted = st.form_submit_button(
            "Let's study 🚀"
        )

    if submitted:

        if not name.strip() or not email.strip():

            st.warning(
                "Please fill in both your name and email address."
            )

        else:

            st.session_state.name = name.strip()
            st.session_state.email = email.strip()

            st.session_state.chat = gemini_client.chats.create(
                model=MODEL_NAME,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT
                ),
            )

            st.session_state.messages = []

            st.session_state.onboarded = True

            st.rerun()

    st.stop()


# =========================================================
# STEP 2: MAKE SURE SESSION STATE EXISTS
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================================================
# STEP 3: CHAT INTERFACE
# =========================================================

header_col, button_col = st.columns(
    [5, 2],
    vertical_alignment="center"
)


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

with header_col:

    st.title("📚 Snap & Study")


# ---------------------------------------------------------
# Send to Email button
# ---------------------------------------------------------

with button_col:

    send_disabled = len(st.session_state.messages) <= 1

    if st.button(
        "📧 Send to Email",
        disabled=send_disabled,
        use_container_width=True
    ):

        with st.spinner(
            "Preparing your study summary..."
        ):

            summary = ask_gemini(
                [SUMMARY_REQUEST_PROMPT]
            )

        success, info = send_email(
            st.session_state.email,
            "Your Snap & Study Summary 📚",
            summary
        )

        if success:

            st.success(
                "Sent! Check your email 📧"
            )

        else:

            st.error(
                f"Couldn't send the email: {info}"
            )


# ---------------------------------------------------------
# User information
# ---------------------------------------------------------

st.caption(
    f"Logged in as {st.session_state.name} "
    f"• Explanations will be sent to "
    f"{st.session_state.email}"
)


# =========================================================
# STEP 4: SHOW PREVIOUS MESSAGES
# =========================================================

for message in st.session_state.messages:

    render_message(message)


# =========================================================
# STEP 5: CHAT INPUT
# =========================================================

user_input = st.chat_input(
    "Ask a question, or attach a study image",
    accept_file=True,
    file_type=["jpg", "jpeg", "png"],
)


# =========================================================
# STEP 6: PROCESS USER INPUT
# =========================================================

if user_input:

    photo = (
        user_input.files[0]
        if user_input.files
        else None
    )

    text = user_input.text

    parts = []


    # -----------------------------------------------------
    # Image
    # -----------------------------------------------------

    if photo is not None:

        photo_bytes = photo.getvalue()

        add_message(
            "user",
            "image",
            photo_bytes
        )

        parts.append(
            types.Part.from_bytes(
                data=photo_bytes,
                mime_type=photo.type
            )
        )


    # -----------------------------------------------------
    # Text
    # -----------------------------------------------------

    if text:

        add_message(
            "user",
            "text",
            text
        )

        parts.append(text)


    # -----------------------------------------------------
    # Image without text
    # -----------------------------------------------------

    elif photo is not None:

        parts.append(
            "Explain this study material clearly. "
            "Break it down step by step."
        )


    # -----------------------------------------------------
    # Send to Gemini
    # -----------------------------------------------------

    with st.spinner(
        "Understanding your study material..."
    ):

        answer = ask_gemini(parts)


    # -----------------------------------------------------
    # Display Gemini response
    # -----------------------------------------------------

    add_message(
        "assistant",
        "text",
        answer
    )
