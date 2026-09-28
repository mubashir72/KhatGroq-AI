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

## Deploy on Streamlit Community Cloud

1. Push `app.py`, `requirements.txt`, and `.streamlit/config.toml` to GitHub.
2. Create the app in Streamlit Community Cloud and choose `app.py` as the entrypoint.
3. In **Advanced settings**, select **Python 3.12**.
4. Add the following in the **Secrets** field:

   ```toml
   GROQ_API_KEY = "gsk_your_key_here"
   ```

5. Deploy or reboot the app.

If the app was originally created with a different Python version, delete and redeploy it to change the Python version.
