# Image Support — Streamlit demo

This folder contains a small Streamlit demo that mirrors the image examples in
`images.ipynb`. The app lets you upload an image, provide a prompt, and send
the image + prompt to the Anthropic API (encoded as base64 image blocks).

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
streamlit run 006_claude_features/002_image_support/streamlit_app.py
```

Notes
- The app encodes uploaded images as base64 and sends them as image blocks.
- Use the `Trigger magic thinking test` button to exercise the redacted-thinking
  demo (same magic string as the Extended Thinking demo).
- The demo tries to keep `max_tokens` larger than the thinking budget when
  thinking is enabled.
