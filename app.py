import streamlit as st
import google.generativeai as genai
import re
import csv
import uuid
import os

# Configure Gemini API
API_KEY = "YOUR_API_KEY"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

# App Title
st.title("🤖 TalentScout: AI Hiring Assistant")

# Exit
exit_keywords = ["exit", "quit", "bye"]
user_input = st.text_input("Type 'exit' to end at any time:")
if any(word in user_input.lower() for word in exit_keywords):
    st.success("Thank you! Your details have been recorded.")
    st.stop()

# Session state initialization
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.candidate_info = {
        "user_id": str(uuid.uuid4()),  # Generate unique user ID
        "name": "", "email": "", "phone": "",
        "experience": 0, "position": "", "location": "",
        "languages": "", "frameworks": "", "databases": "", "tools": ""
    }
    st.session_state.questions = []
    st.session_state.current_q = 0
    st.session_state.answers = []

# ------------------ STEP 0: Basic Info ------------------
if st.session_state.step == 0:
    st.subheader("Step 1: Basic Details")
    with st.form("basic_info_form"):
        st.session_state.candidate_info["name"] = st.text_input("Full Name *")
        st.session_state.candidate_info["email"] = st.text_input("Email Address *")
        st.session_state.candidate_info["phone"] = st.text_input("Phone Number *")
        st.session_state.candidate_info["experience"] = st.number_input("Years of Experience *", min_value=0)
        st.session_state.candidate_info["position"] = st.text_input("Desired Position(s) *")
        st.session_state.candidate_info["location"] = st.text_input("Current Location *")
        submitted = st.form_submit_button("Next")

        if submitted:
            info = st.session_state.candidate_info
            if not all([info["name"].strip(), info["email"].strip(), info["phone"].strip(), info["position"].strip(), info["location"].strip()]):
                st.warning("Please fill in all required fields.")
            elif not re.match(r"[^@]+@[^@]+\.[^@]+", info["email"]):
                st.warning("Invalid email format.")
            elif not re.match(r"^\+?\d{10,15}$", info["phone"].strip()):
                st.warning("Enter a valid phone number.")
            else:
                # ✅ Save candidate info to CSV
                candidate_file = "candidates.csv"
                file_exists = os.path.exists(candidate_file)
                with open(candidate_file, mode="a", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=st.session_state.candidate_info.keys())
                    if not file_exists:
                        writer.writeheader()
                    writer.writerow(st.session_state.candidate_info)

                st.session_state.step = 1

# ------------------ STEP 1: Tech Stack ------------------
elif st.session_state.step == 1:
    st.subheader("Step 2: Your Tech Stack")
    with st.form("tech_stack_form"):
        st.session_state.candidate_info["languages"] = st.text_input("Programming Languages (comma separated)")
        st.session_state.candidate_info["frameworks"] = st.text_input("Frameworks (comma separated)")
        st.session_state.candidate_info["databases"] = st.text_input("Databases (comma separated)")
        st.session_state.candidate_info["tools"] = st.text_input("Other Tools/Technologies (comma separated)")
        submitted = st.form_submit_button("Generate Questions")

        if submitted:
            if not st.session_state.candidate_info["languages"].strip():
                st.warning("Please enter at least one language.")
            else:
                # Generate questions with Gemini
                tech_string = (
                    f"Languages: {st.session_state.candidate_info['languages']}, "
                    f"Frameworks: {st.session_state.candidate_info['frameworks']}, "
                    f"Databases: {st.session_state.candidate_info['databases']}, "
                    f"Tools: {st.session_state.candidate_info['tools']}"
                )
                prompt = f"Generate 3 to 5 concise technical interview questions to assess skills in: {tech_string}"

                try:
                    response = model.generate_content(prompt)
                    text = response.text.strip()
                    lines = text.splitlines()
                    while lines and not re.match(r'^\d+\.', lines[0].strip()):
                        lines.pop(0)

                    cleaned_text = "\n".join(lines)
                    questions = re.split(r'\n\d+\.\s', cleaned_text)
                    questions = [q.strip(" -\n\r\t1234567890.") for q in questions if q.strip()]


                    filtered_questions = []
                    for q in questions:
                        if len(q.split()) < 3:
                            continue  # Skip very short entries
                        if "encourage candidates" in q.lower() or "explain their reasoning" in q.lower():
                            continue  # Remove explanations or general comments
                        filtered_questions.append(q)

                    st.session_state.questions = filtered_questions[:5]

                    if len(questions) < 3:
                        questions = [text]

                    st.session_state.questions = questions[:5]
                    st.session_state.answers = [""] * len(st.session_state.questions)
                    st.session_state.current_q = 0
                    st.session_state.step = 2

                except Exception as e:
                    st.error(f"Failed to generate questions: {e}")

# ------------------ STEP 2: Show Questions ------------------
elif st.session_state.step == 2:
    q_idx = st.session_state.current_q
    total = len(st.session_state.questions)

    st.subheader(f"Step 3: Technical Questions ({q_idx + 1}/{total})")
    st.markdown(f"**Q{q_idx + 1}:** {st.session_state.questions[q_idx]}")
    answer = st.text_area("Your Answer:", value=st.session_state.answers[q_idx], height=150)
    st.session_state.answers[q_idx] = answer

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Previous") and q_idx > 0:
            st.session_state.current_q -= 1
    with col2:
        if st.button("Next"):
            if answer.strip() == "":
                st.warning("Please answer before moving on.")
            elif q_idx < total - 1:
                st.session_state.current_q += 1
    with col3:
        if st.button("Submit"):
            if answer.strip() == "":
                st.warning("Please answer before submitting.")
            elif q_idx == total - 1:
                st.session_state.step = 3

# ------------------ STEP 3: Summary and Save QA ------------------
elif st.session_state.step == 3:
    st.success("✅ Thank you for completing the screening!")
    st.write("Here are your submitted answers:")
    for i, (q, a) in enumerate(zip(st.session_state.questions, st.session_state.answers), start=1):
        st.markdown(f"**Q{i}:** {q}")
        st.markdown(f"**Your Answer:** {a}")
        st.markdown("---")
    st.info("Our team will review your answers and get back to you.")

    # ✅ Save QA to CSV
    qa_file = "qa_pairs.csv"
    file_exists = os.path.exists(qa_file)
    with open(qa_file, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["user_id", "question", "answer"])
        if not file_exists:
            writer.writeheader()
        for q, a in zip(st.session_state.questions, st.session_state.answers):
            writer.writerow({"user_id": st.session_state.candidate_info["user_id"], "question": q, "answer": a})