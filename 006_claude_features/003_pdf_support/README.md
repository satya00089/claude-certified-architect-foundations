# PDF Support — Streamlit demo

This folder contains a small Streamlit demo that mirrors the PDF examples in
`pdf.ipynb`. The app lets you upload a PDF, provide a prompt, and send the
document + prompt to the Anthropic API (encoded as a base64 document block).

Quick start

1. Create a `.env` file with your Anthropic API key:

```
ANTHROPIC_API_KEY=sk-...
```

2. (Optional) activate your project's virtualenv.

3. Install the required packages:

```powershell
pip install streamlit python-dotenv anthropic
```

4. Run the demo:

```powershell
streamlit run 006_claude_features/003_pdf_support/streamlit_app.py
```

Notes
- The app encodes uploaded PDFs as base64 and sends them as `document` blocks.
- Use the `Trigger magic thinking test` button to exercise the redacted-thinking
  demo (same magic string as the Extended Thinking demo).
- The demo ensures `max_tokens` is larger than the thinking budget when
  thinking is enabled.
