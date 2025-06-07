# 🤖 TalentScout: AI Hiring Assistant Chatbot

TalentScout is a Streamlit-based intelligent hiring assistant that uses Google Gemini (via `google.generativeai`) to screen candidates. It collects candidate information, generates technical questions based on their tech stack, captures their answers, and stores the data in CSV format.

---

## 🛠️ Features

- Collect candidate details (name, email, phone, etc.)
- Accept tech stack input (languages, frameworks, databases, tools)
- Use Gemini API to generate 3–5 custom interview questions
- Interactive Q&A interface
- Save candidate responses to CSV files
- Exit the form at any time using keywords like `exit`, `bye`, `quit`

---

## 📁 Project Structure

<pre>
hiring_assistant_chatbot_5/
├── app.py                     # Streamlit application
├── requirements.txt           # Required Python packages
├── candidates.csv             # Stores candidate basic information
├── qa_pairs.csv               # Stores question-answer pairs
├── .gitignore                 # Git ignored files
</pre>

---

## ▶️ How to Run the Project

<pre>
1. Clone the repository:
   git clone https://github.com/varshithaga/hiring_assistant_chatbot_5.git
   cd hiring_assistant_chatbot_5

2. Create a virtual environment:
   python -m venv venv

3. Activate the virtual environment:
   - Windows: .\venv\Scripts\activate
   - Linux/Mac: source venv/bin/activate

4. Install dependencies:
   pip install -r requirements.txt

5. Add your Gemini API key:
   - Open <code>app.py</code>
   - Replace <code>API_KEY = "YOUR_API_KEY"</code> with your actual API key

6. Run the Streamlit app:
   streamlit run app.py
</pre>

---

## 💾 CSV Output Files

- <code>candidates.csv</code><br>
  Stores the following fields:
  <pre>
  user_id, name, email, phone, experience, position, location,
  languages, frameworks, databases, tools
  </pre>

- <code>qa_pairs.csv</code><br>
  Stores:
  <pre>
  user_id, question, answer
  </pre>

---

## 🔐 API Key Info

You need a **Google Gemini API key**. Create one at:
[https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)

---

## 📌 Example Question Generation Prompt

<pre>
"Generate 3 to 5 concise technical interview questions to assess skills in:
Languages: Python, Java; Frameworks: React, Spring Boot; Databases: MySQL;
Tools: Git, Docker"
</pre>

---

## ✅ Exit Keyword Support

At any step, typing `exit`, `bye`, or `quit` will end the session gracefully.

---
