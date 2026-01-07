import os
import streamlit as st
from google import genai

# ---------------- Gemini client ----------------
# Set GEMINI_API_KEY in environment or Streamlit secrets.
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

SYSTEM_PROMPT = """You generate BDD test scenarios in Gherkin.
- Use: Feature / Scenario / Given-When-Then
- Include at least one positive and one negative scenario.
- Domain: generic sample web app with login and dashboard.
Return ONLY valid Gherkin text, no explanations."""

HAPPY_KEYWORDS = ["login", "submit", "approve"]


# ---------------- LLM + BDD helpers ----------------
def call_llm(requirements_text: str) -> str:
    prompt = f"{SYSTEM_PROMPT}\n\nUser requirements:\n{requirements_text}"
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text.strip()


def split_scenarios(gherkin_text: str):
    blocks = []
    current = []
    for line in gherkin_text.splitlines():
        if line.strip().startswith("Scenario:"):
            if current:
                blocks.append("\n".join(current).strip())
                current = []
        current.append(line)
    if current:
        blocks.append("\n".join(current).strip())
    return blocks


def is_valid_scenario(text: str) -> bool:
    needed = ["Given", "When", "Then"]
    return all(k in text for k in needed)


def is_happy_path(text: str) -> bool:
    lower = text.lower()
    return ("happy path" in lower) or ("success" in lower and "valid" in lower)


def contains_known_actions(text: str) -> bool:
    lower = text.lower()
    return any(k in lower for k in HAPPY_KEYWORDS)


def validate_and_select_happy(gherkin_text: str):
    all_scenarios = split_scenarios(gherkin_text)
    valid = [s for s in all_scenarios if is_valid_scenario(s)]
    happy = [
        s for s in valid
        if contains_known_actions(s) and is_happy_path(s)
    ]
    return {
        "all": all_scenarios,
        "valid": valid,
        "happy": happy,
        "summary": {
            "total": len(all_scenarios),
            "valid": len(valid),
            "happy": len(happy),
            "has_required_actions": all(contains_known_actions(s) for s in happy),
        },
    }


# ---------------- Streamlit UI ----------------
st.title("LLM‑Assisted BDD Scenario Generator (Gemini)")

st.write(
    "Enter plain‑English business requirements for a sample web app. "
    "The app will generate Gherkin scenarios and select happy‑path ones for automation."
)

default_reqs = """The system must allow a registered user to log in with a valid email and password
and redirect to a dashboard on success. If credentials are invalid, an error message
must be displayed and the user must remain on the login page.
"""

requirements_text = st.text_area(
    "Business requirements",
    value=default_reqs,
    height=200,
)

if st.button("Generate Gherkin scenarios"):
    if not requirements_text.strip():
        st.error("Please enter some requirements.")
    else:
        with st.spinner("Calling Gemini and generating scenarios..."):
            gherkin_text = call_llm(requirements_text)
            result = validate_and_select_happy(gherkin_text)

        st.subheader("Raw Gherkin from Gemini")
        st.code(gherkin_text, language="gherkin")

        st.subheader("Validation summary")
        st.json(result["summary"])

        st.subheader("All scenarios")
        for i, s in enumerate(result["all"], start=1):
            st.markdown(f"**Scenario {i}**")
            st.code(s, language="gherkin")

        st.subheader("Selected happy‑path scenarios for automation")
        if result["happy"]:
            for i, s in enumerate(result["happy"], start=1):
                st.markdown(f"**Happy path {i}**")
                st.code(s, language="gherkin")
        else:
            st.warning("No happy‑path scenarios matched the selection rules.")

        # Downloadable feature file for BDD framework
        feature_header = (
            "Feature: LLM generated login flows\n"
            "  As a user of the sample web app\n"
            "  I want to login and access the dashboard\n"
            "  So that I can use the application features\n\n"
        )
        feature_body = ""
        for s in result["happy"]:
            lines = ["  " + line if line.strip() else "" for line in s.splitlines()]
            feature_body += "\n".join(lines) + "\n\n"

        feature_content = feature_header + feature_body
        st.download_button(
            label="Download happy‑path feature file",
            data=feature_content,
            file_name="login_happy.feature",
            mime="text/plain",
        )
