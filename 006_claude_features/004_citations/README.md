# Citations — Streamlit demo

This folder contains a small Streamlit demo that mirrors the examples in
`citations.ipynb`. The app lets you upload a document (PDF or plain text),
provide a prompt, and send the document + prompt to the Anthropic API as a
document block with optional citation metadata.

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
streamlit run 006_claude_features/004_citations/streamlit_app.py
```

Notes
- The app encodes uploaded files as base64 and sends them as `document` blocks.
- Enable `Citations` to include the `"citations": {"enabled": true}` field
  in the document metadata (used in `citations.ipynb`).
- The demo also includes the same `thinking` toggle and ensures `max_tokens`
  is larger than the thinking budget when thinking is enabled.
