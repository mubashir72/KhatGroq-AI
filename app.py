import os
import re
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv


load_dotenv()


st.set_page_config(
    page_title="KhatGroq AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


GLASS_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');

    :root {
        --ink: #17203d;
        --muted: #6d7390;
        --violet: #7257f5;
        --purple: #9a66f7;
        --pink: #ef78ac;
        --line: rgba(107, 93, 190, 0.16);
        --glass: rgba(255, 255, 255, 0.60);
    }

    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    .stApp {
        color: var(--ink);
        background:
            radial-gradient(circle at 8% 8%, rgba(181, 152, 255, .42), transparent 27%),
            radial-gradient(circle at 88% 15%, rgba(255, 176, 210, .40), transparent 27%),
            radial-gradient(circle at 78% 84%, rgba(160, 220, 255, .32), transparent 30%),
            linear-gradient(135deg, #f8f6ff 0%, #fff8fc 46%, #f4f9ff 100%);
        background-attachment: fixed;
    }
    .stApp::before, .stApp::after {
        content: "";
        position: fixed;
        z-index: 0;
        border-radius: 999px;
        filter: blur(2px);
        pointer-events: none;
    }
    .stApp::before {
        width: 280px; height: 280px; right: -80px; top: 32%;
        background: linear-gradient(135deg, rgba(119,87,245,.14), rgba(239,120,172,.12));
    }
    .stApp::after {
        width: 220px; height: 220px; left: 19%; bottom: -90px;
        background: rgba(113, 204, 255, .15);
    }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stToolbar"] { right: 1rem; }
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, .48);
        border-right: 1px solid rgba(255,255,255,.74);
        backdrop-filter: blur(24px);
    }
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] { gap: .65rem; }
    [data-testid="stMainBlockContainer"] {
        max-width: 1180px;
        padding-top: 2.2rem;
        padding-bottom: 4rem;
    }
    h1, h2, h3 { font-family: 'Manrope', sans-serif !important; letter-spacing: -.035em; }
    .brand {
        display: flex; align-items: center; gap: .75rem; margin-bottom: 1.55rem;
    }
    .brand-mark {
        display: grid; place-items: center; width: 42px; height: 42px;
        color: white; font-size: 1.25rem; font-weight: 800;
        border-radius: 14px;
        background: linear-gradient(135deg, var(--violet), var(--pink));
        box-shadow: 0 10px 28px rgba(114, 87, 245, .28), inset 0 1px 0 rgba(255,255,255,.45);
    }
    .brand-name { font: 800 1.12rem 'Manrope', sans-serif; letter-spacing: -.03em; }
    .brand-sub { color: var(--muted); font-size: .76rem; margin-top: .08rem; }
    .hero { padding: 1rem .2rem 1.25rem; }
    .eyebrow {
        display: inline-flex; align-items: center; gap: .45rem;
        padding: .36rem .7rem; border: 1px solid rgba(114,87,245,.18);
        border-radius: 999px; background: rgba(255,255,255,.55);
        color: #6550ce; font-size: .77rem; font-weight: 700; letter-spacing: .02em;
        box-shadow: inset 0 1px 0 rgba(255,255,255,.85);
    }
    .hero h1 { font-size: clamp(2.1rem, 5vw, 3.75rem); line-height: 1.04; margin: .75rem 0 .75rem; }
    .gradient-text {
        background: linear-gradient(105deg, #6047df 10%, #a351de 55%, #e567a4 95%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .hero p { max-width: 710px; color: var(--muted); font-size: 1.03rem; line-height: 1.65; }
    .glass-card {
        border: 1px solid rgba(255,255,255,.82);
        border-radius: 24px;
        background: rgba(255,255,255,.52);
        box-shadow: 0 20px 55px rgba(72, 54, 139, .10), inset 0 1px 0 rgba(255,255,255,.95);
        backdrop-filter: blur(24px);
        padding: 1.2rem 1.3rem .35rem;
        margin-bottom: 1rem;
    }
    .section-kicker { color: var(--violet); font-weight: 800; font-size: .72rem; letter-spacing: .12em; text-transform: uppercase; }
    .section-title { font: 700 1.12rem 'Manrope', sans-serif; margin: .2rem 0 .15rem; }
    .section-note { color: var(--muted); font-size: .83rem; margin-bottom: .65rem; }
    .privacy-note {
        color: var(--muted); font-size: .78rem; line-height: 1.5;
        padding: .8rem .9rem; border-radius: 14px;
        border: 1px solid rgba(114,87,245,.12); background: rgba(255,255,255,.42);
    }
    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea,
    div[data-baseweb="select"] > div {
        border-color: rgba(99, 82, 175, .16) !important;
        background: rgba(255,255,255,.58) !important;
        box-shadow: inset 0 1px 0 rgba(255,255,255,.75) !important;
    }
    div[data-testid="stTextInput"] input:focus,
    div[data-testid="stTextArea"] textarea:focus {
        border-color: rgba(114,87,245,.50) !important;
        box-shadow: 0 0 0 3px rgba(114,87,245,.10) !important;
    }
    .stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primary"] {
        border: 0; color: white; font-weight: 700;
        background: linear-gradient(105deg, #6750e7, #9b58e6 58%, #df6da8);
        box-shadow: 0 10px 24px rgba(114,87,245,.24), inset 0 1px 0 rgba(255,255,255,.34);
        transition: transform .18s ease, box-shadow .18s ease;
    }
    .stButton > button[kind="primary"]:hover, .stFormSubmitButton > button[kind="primary"]:hover {
        transform: translateY(-1px); box-shadow: 0 14px 30px rgba(114,87,245,.30);
    }
    .stDownloadButton > button, .stButton > button[kind="secondary"] {
        background: rgba(255,255,255,.55); border-color: rgba(99,82,175,.16); color: var(--ink);
    }
    [data-testid="stExpander"] {
        border: 1px solid rgba(255,255,255,.82) !important;
        background: rgba(255,255,255,.42); border-radius: 16px !important;
    }
    .output-head {
        display: flex; align-items: center; justify-content: space-between;
        margin: .2rem 0 .75rem;
    }
    .status-pill {
        display: inline-flex; align-items: center; gap: .35rem; color: #267a5b;
        font-size: .73rem; font-weight: 700; padding: .32rem .62rem;
        border-radius: 999px; background: rgba(91, 202, 153, .13); border: 1px solid rgba(49,166,119,.16);
    }
    .email-subject {
        padding: .85rem 1rem; border-radius: 14px; margin-bottom: .8rem;
        background: rgba(255,255,255,.56); border: 1px solid rgba(99,82,175,.12);
    }
    .email-subject span { color: var(--muted); font-size: .78rem; font-weight: 700; text-transform: uppercase; letter-spacing: .08em; }
    .email-subject strong { display: block; margin-top: .2rem; }
    .mini-stat { color: var(--muted); font-size: .78rem; text-align: right; margin-top: .35rem; }
    #MainMenu, footer { visibility: hidden; }
</style>
"""


@st.cache_resource(show_spinner=False)
def groq_client(api_key: str):
    from groq import Groq

    return Groq(api_key=api_key)


def build_prompt(data: dict) -> str:
    details = [
        f"Purpose: {data['purpose']}",
        f"Recipient: {data['recipient_name'] or 'Not specified'}",
        f"Recipient role/company: {data['recipient_context'] or 'Not specified'}",
        f"Tone: {data['tone']}",
        f"Length: {data['length']}",
        f"Language: {data['language']}",
        f"Sender name: {data['sender_name'] or 'Not specified'}",
        f"Key message and context:\n{data['context']}",
    ]
    if data["call_to_action"]:
        details.append(f"Desired call to action: {data['call_to_action']}")
    if data["extra_instructions"]:
        details.append(f"Additional instructions: {data['extra_instructions']}")

    return """You are an expert business email writer. Draft one polished, natural email from the brief below.

Rules:
- Be specific, human, and direct. Avoid clichés, filler, and exaggerated claims.
- Never invent facts, dates, offers, relationships, or contact details.
- Match the requested tone, language, and approximate length.
- Include an appropriate greeting and sign-off.
- Return exactly this structure, with no markdown fences or commentary:
SUBJECT: <one concise subject line>
BODY:
<email body>

BRIEF
""" + "\n".join(details)


def parse_email(raw: str) -> tuple[str, str]:
    cleaned = raw.strip().strip("`").strip()
    match = re.search(r"SUBJECT:\s*(.*?)\s*\nBODY:\s*(.*)", cleaned, flags=re.I | re.S)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    lines = cleaned.splitlines()
    if lines and lines[0].lower().startswith("subject:"):
        return lines[0].split(":", 1)[1].strip(), "\n".join(lines[1:]).strip()
    return "Your email draft", cleaned


def generate_email(api_key: str, model: str, temperature: float, brief: dict) -> tuple[str, str]:
    client = groq_client(api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You write clear, credible emails that sound like a thoughtful human wrote them.",
            },
            {"role": "user", "content": build_prompt(brief)},
        ],
        temperature=temperature,
        max_tokens=1200,
    )
    content = response.choices[0].message.content or ""
    return parse_email(content)


def reset_draft() -> None:
    st.session_state.pop("draft", None)
    st.session_state.pop("brief", None)
    st.session_state.pop("draft_subject", None)
    st.session_state.pop("draft_body", None)


st.markdown(GLASS_CSS, unsafe_allow_html=True)

with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-mark">✦</div>
            <div><div class="brand-name">KhatGroq AI</div><div class="brand-sub">AI email studio</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("#### AI settings")
    api_key = os.getenv("GROQ_API_KEY", "")
    key_status = (
        "✅ Groq API is configured"
        if api_key
        else "⚠️ GROQ_API_KEY is missing from the environment"
    )
    st.markdown(
        f"""<div class="privacy-note">{key_status}</div>""",
        unsafe_allow_html=True,
    )
    model = st.selectbox(
        "Model",
        ["openai/gpt-oss-20b", "openai/gpt-oss-120b", "qwen/qwen3.8-27b"],
        help="Available models can vary by Groq account.",
    )
    creativity = st.slider("Creativity", 0.0, 1.0, 0.45, 0.05)
    st.markdown(
        """<div class="privacy-note">🔒 The API key is managed securely by the app environment and is never shown to visitors.</div>""",
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.caption("Tip: lower creativity for formal or sensitive emails; raise it for outreach and campaigns.")

st.markdown(
    """
    <section class="hero">
        <div class="eyebrow">✦ GROQ-POWERED WRITING</div>
        <h1>Write emails people<br><span class="gradient-text">actually want to read.</span></h1>
        <p>Turn a rough thought into a polished, purposeful email in seconds—without losing your voice.</p>
    </section>
    """,
    unsafe_allow_html=True,
)

input_col, output_col = st.columns([1.05, 0.95], gap="large")

with input_col:
    st.markdown(
        """<div class="glass-card"><div class="section-kicker">01 · The brief</div><div class="section-title">What are we writing?</div><div class="section-note">Give the AI enough context to sound informed, not generic.</div></div>""",
        unsafe_allow_html=True,
    )
    with st.form("email_form", clear_on_submit=False):
        purpose = st.selectbox(
            "Email purpose",
            [
                "Professional outreach",
                "Follow-up",
                "Meeting request",
                "Sales introduction",
                "Thank you",
                "Job application",
                "Customer support",
                "Announcement",
                "Apology",
                "Other",
            ],
        )
        name_col, sender_col = st.columns(2)
        with name_col:
            recipient_name = st.text_input("Recipient name", placeholder="e.g. Maya")
        with sender_col:
            sender_name = st.text_input("Your name", placeholder="e.g. Alex")
        recipient_context = st.text_input(
            "Who are they?",
            placeholder="e.g. Product lead at Northstar Labs",
        )
        context = st.text_area(
            "Key message and context *",
            placeholder="Explain what happened, what matters, and any details the email must include…",
            height=150,
        )
        call_to_action = st.text_input(
            "Desired next step",
            placeholder="e.g. Ask for a 20-minute call next week",
        )
        tone_col, length_col, language_col = st.columns(3)
        with tone_col:
            tone = st.selectbox("Tone", ["Warm", "Professional", "Friendly", "Persuasive", "Concise", "Empathetic"])
        with length_col:
            length = st.selectbox("Length", ["Short", "Medium", "Detailed"])
        with language_col:
            language = st.selectbox("Language", ["English", "Spanish", "French", "German", "Portuguese", "Urdu"])
        with st.expander("Fine-tune the result"):
            extra_instructions = st.text_area(
                "Extra instructions",
                placeholder="e.g. Avoid buzzwords, mention the attached proposal, use a confident closing…",
                height=90,
            )
        submitted = st.form_submit_button("✦  Generate email", type="primary", use_container_width=True)

    if submitted:
        if not api_key:
            st.error("GROQ_API_KEY is not configured in the app environment. Contact the app administrator.")
        elif not context.strip():
            st.warning("Add a key message or some context before generating.")
        else:
            brief = {
                "purpose": purpose,
                "recipient_name": recipient_name.strip(),
                "sender_name": sender_name.strip(),
                "recipient_context": recipient_context.strip(),
                "context": context.strip(),
                "call_to_action": call_to_action.strip(),
                "tone": tone,
                "length": length,
                "language": language,
                "extra_instructions": extra_instructions.strip(),
            }
            try:
                with st.spinner("Crafting your email…"):
                    subject, body = generate_email(api_key, model, creativity, brief)
                st.session_state.draft = {"subject": subject, "body": body, "created_at": datetime.now()}
                st.session_state.brief = brief
                st.session_state.draft_subject = subject
                st.session_state.draft_body = body
            except ImportError:
                st.error("The Groq package is not installed. Run `pip install -r requirements.txt` and restart the app.")
            except Exception as exc:
                message = str(exc)
                if "401" in message or "authentication" in message.lower():
                    st.error("Groq rejected the API key. Check the key and try again.")
                elif "429" in message or "rate" in message.lower():
                    st.error("Groq's rate limit was reached. Wait a moment and try again.")
                elif "connection" in message.lower():
                    st.error("The app could not reach Groq. Check your internet connection and try again.")
                else:
                    st.error(f"Generation failed: {message}")

with output_col:
    st.markdown(
        """<div class="glass-card"><div class="section-kicker">02 · Your draft</div><div class="section-title">Ready to review</div><div class="section-note">Edit, copy, or download the result when it feels right.</div></div>""",
        unsafe_allow_html=True,
    )
    if "draft" not in st.session_state:
        st.info("Your generated email will appear here. Add a brief and click **Generate email** to begin.", icon="💌")
        st.markdown(
            """
            <div class="glass-card" style="margin-top:1rem; padding-bottom:1.2rem; opacity:.82">
                <div class="section-kicker">A stronger draft starts with</div>
                <div style="margin-top:.7rem; color:#6d7390; line-height:1.9; font-size:.88rem">
                    ✓ A clear outcome or next step<br>
                    ✓ Specific facts the recipient needs<br>
                    ✓ The relationship and tone you want
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        draft = st.session_state.draft
        st.markdown(
            """<div class="output-head"><div class="status-pill">● Draft ready</div></div>""",
            unsafe_allow_html=True,
        )
        edited_subject = st.text_input("Subject", key="draft_subject")
        edited_body = st.text_area("Email body", height=390, key="draft_body")
        word_count = len(edited_body.split())
        reading_time = max(1, round(word_count / 200))
        st.markdown(
            f"<div class='mini-stat'>{word_count} words · {reading_time} min read</div>",
            unsafe_allow_html=True,
        )
        full_email = f"Subject: {edited_subject}\n\n{edited_body}"
        download_col, clear_col = st.columns([1, 1])
        with download_col:
            st.download_button(
                "↓  Download .txt",
                data=full_email,
                file_name="email-draft.txt",
                mime="text/plain",
                use_container_width=True,
            )
        with clear_col:
            st.button("Clear draft", on_click=reset_draft, use_container_width=True)
        with st.expander("Copy-ready version"):
            st.code(full_email, language=None, wrap_lines=True)

st.caption("KhatGroq AI can make mistakes. Review names, dates, commitments, and sensitive details before sending.")
