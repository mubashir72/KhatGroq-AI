# KhatGroq AI

A glass-style AI email generator built with Streamlit and Groq.

## Run locally

1. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Add your Groq API key as an environment variable:

   ```powershell
   $env:GROQ_API_KEY="gsk_your_key_here"
   ```

   You can also copy `.env.example` to `.env` and place your key there. The app loads `.env` automatically.

4. Start the app:

   ```powershell
   streamlit run app.py
   ```

You can also create `.streamlit/secrets.toml` with:

```toml
GROQ_API_KEY = "gsk_your_key_here"
```

Do not commit API keys or `secrets.toml`.
