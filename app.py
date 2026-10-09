import os
from groq import Groq
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Emily Baskins AI Assistant - The Newsletter Crew",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 Emily Baskins AI Assistant (The Newsletter Crew)")
st.write(
    "Aapka apna Crowdfunding Email Marketing AI assistant tayyar hai! Néeche"
    " diye gaye box mein sawal puchein."
)

# Initialize Groq Client directly with your key
api_key = "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"

if not api_key:
    st.error(
        "⚠️ Groq API Key nahi mili! Baraye meharbani apni key check karein."
    )
else:
    client = Groq(api_key=api_key)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Apna message yahan type karein..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate assistant response
        with st.chat_message("assistant"):
            try:
                # Updated System Prompt with strict email instruction & no dummy links
                system_prompt = {
                    "role": "system",
                    "content": (
                        "You are Emily Baskins, the official customer-support and chat"
                        " agent exclusively for The Newsletter Crew"
                        " (https://thenewslettercrew.com/)[cite: 10].\n\n"
                        "CRITICAL INSTRUCTION - NO DUMMY LINKS & OFFICIAL EMAIL"
                        " REDIRECTION:\n"
                        "- You must ONLY answer questions using the exact facts,"
                        " pricing, rules, and details provided in your official"
                        " knowledge base[cite: 10].\n"
                        "- DO NOT invent, assume, or bring in any outside"
                        " knowledge, generic facts, or fabricated pricing/terms"
                        ".\n"
                        "- STRICTLY DO NOT generate any dummy URLs, fake"
                        " contract links, or placeholder websites.\n"
                        "- If a customer indicates they are ready to buy, book,"
                        " or proceed with a package, DO NOT provide links. "
                        "Instead, instruct them to send an email directly to"
                        " the official company email address:"
                        " info@thenewslettercrew.com with their details, and"
                        " inform them that the team will reply with further"
                        " instructions, agreement, and payment details (Wise or"
                        " bank wire transfer)[cite: 13].\n\n"
                        "Company & Services Summary (from Knowledge Base):\n"
                        "- Official email: info@thenewslettercrew.com | Address:"
                        " 1002 S MAIN ST STE 501, Kalispell, Montana 59901,"
                        " United States.\n"
                        "- Core Service: Crowdfunding email marketing service"
                        " promoting Kickstarter, Indiegogo, and equity"
                        " crowdfunding (Wefunder, StartEngine, Honeycomb)"
                        " campaigns[cite: 10].\n"
                        "- Audience: 230,000+ active crowdfunding backers and"
                        " enthusiasts (57% US-based, core age 26-44) [cite: 10,"
                        " 16, 21].\n"
                        "- Offerings: Shared newsletter placements (starting at"
                        " $400), dedicated newsletter placements ($800 with"
                        " potential 2x ROI guarantee under signed agreement),"
                        " investor newsletter marketing, and Meta Ads [cite: 11,"
                        " 12, 20, 21].\n"
                        "- Payment Methods: Wise and bank wire transfer only."
                        " PayPal, Stripe, and standard cards are NOT accepted"
                        "[cite: 13].\n"
                    ),
                }

                # Combine system prompt with user messages
                messages_payload = [system_prompt] + [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]

                stream = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=messages_payload,
                    stream=True,
                )

                response = st.write_stream(
                    chunk.choices[0].delta.content
                    for chunk in stream
                    if chunk.choices[0].delta.content is not None
                )
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )
            except Exception as e:
                st.error(f"Koi kharabi ho gayi hai: {e}")
