"""Streamlit demo for the Image Support notebook.

Usage:
    streamlit run streamlit_app.py

Requires a working Anthropic SDK and API key in a .env file.
"""

import base64
from dotenv import load_dotenv
import streamlit as st
from anthropic import Anthropic

load_dotenv()


# Default model (same as notebook)
MODEL = "claude-sonnet-4-5"


client = Anthropic()


def add_user_message(messages, message):
    """Helper to add a user message to the conversation history."""
    messages.append({"role": "user", "content": message})


def add_assistant_message(messages, message):
    """Helper to add an assistant message to the conversation history."""
    messages.append({"role": "assistant", "content": message})


def chat(
    messages,
    system=None,
    temperature=1.0,
    stop_sequences=None,
    tools=None,
    thinking=False,
    thinking_budget=1024,
):
    """Helper to call the Anthropic SDK with the right parameters for this demo."""
    if stop_sequences is None:
        stop_sequences = []

    params = {
        "model": MODEL,
        "max_tokens": 4000,
        "messages": messages,
        "temperature": temperature,
        "stop_sequences": stop_sequences,
    }

    if thinking:
        # ensure max_tokens is strictly greater than the thinking budget (follow thinking.py)
        current_max = params.get("max_tokens") or 0
        if thinking_budget >= current_max:
            params["max_tokens"] = int(thinking_budget * 1.5)
        params["thinking"] = {"type": "enabled", "budget_tokens": thinking_budget}

    if tools:
        params["tools"] = tools
    if system:
        params["system"] = system

    return client.messages.create(**params)


def text_from_message(message):
    """Helper to extract text from the SDK response. Fall back to string repr."""
    try:
        if hasattr(message, "content"):
            content = message.content
            # content may be a list of blocks
            if isinstance(content, list):
                parts = [
                    getattr(block, "text", None) or block.get("text", "")
                    for block in content
                ]
                return "\n".join([p for p in parts if p])
            if isinstance(content, str):
                return content
        if isinstance(message, dict):
            c = message.get("content")
            if isinstance(c, str):
                return c
            if isinstance(c, list):
                return "\n".join(
                    [b.get("text", "") for b in c if b.get("type") == "text"]
                )
    except Exception:
        pass
    return str(message)


def main():
    """Main Streamlit app function."""
    st.title("Image Support — demo")

    st.markdown("Small demo that mirrors `images.ipynb` (use `.env` for keys).")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    with st.form(key="send_form"):
        uploaded_file = st.file_uploader(
            "Upload image",
            type=["png", "jpg", "jpeg"],
            help="Upload a PNG or JPEG image",
            key="image_uploader",
        )

        file_bytes = None
        if uploaded_file is not None:
            try:
                file_bytes = uploaded_file.getvalue()
                st.image(file_bytes, caption=uploaded_file.name)
            except Exception:
                st.write("(preview not available)")

        prompt_default = (
            "Analyze the attached satellite image of a property and provide a short,"
            " structured assessment (residence location, tree overhang, fire risk, and a"
            " concise risk rating)."
        )
        prompt = st.text_area("Prompt", value=prompt_default, height=200)
        temperature = st.slider("Temperature", 0.0, 2.0, 1.0, 0.1)
        submit = st.form_submit_button("Send")

    # Trigger magic thinking test removed (reserved for Extended Thinking demo)

    if submit:
        if file_bytes is None:
            st.warning("Please upload an image before sending.")
        else:
            try:
                # detect media type from filename
                fname = uploaded_file.name.lower() if uploaded_file is not None else "image.png"
                media_type = "image/png"
                if fname.endswith(".jpg") or fname.endswith(".jpeg"):
                    media_type = "image/jpeg"

                image_block = {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": media_type,
                        "data": base64.standard_b64encode(file_bytes).decode("utf-8"),
                    },
                }

                text_block = {"type": "text", "text": prompt}

                add_user_message(st.session_state.messages, [image_block, text_block])
                try:
                    resp = chat(
                        st.session_state.messages,
                        temperature=temperature,
                        thinking=False,
                        thinking_budget=0,
                    )
                    assistant_text = text_from_message(resp)
                    add_assistant_message(st.session_state.messages, assistant_text)
                    st.success("Response received")
                    st.write(assistant_text)
                    try:
                        st.json(getattr(resp, "__dict__", resp))
                    except Exception:
                        st.write(repr(resp))
                except Exception as e:
                    st.error(f"API call failed: {e}")
            except Exception as e:
                st.error(f"Failed to prepare image: {e}")

    st.subheader("Conversation history")
    for m in st.session_state.messages:
        role = m.get("role")
        content = m.get("content")
        if role == "user":
            st.markdown(f"**User:** {content}")
        else:
            st.markdown(f"**Assistant:** {content}")


if __name__ == "__main__":
    main()
