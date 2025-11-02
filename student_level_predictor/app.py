# app.py

import streamlit as st
import pandas as pd
import json
from model.classifier import predict_level

# --------------------------
# Streamlit Page Setup
# --------------------------
st.set_page_config(page_title="🎓 Student Skill Level Analyzer", layout="centered")
st.title("🤖 Student Skill Level Analyzer")

# --------------------------
# Input: Student Details
# --------------------------
student_name = st.text_input("👤 Enter your name")

course = st.selectbox("📚 Choose your course:", ["python", "genai", "datascience", "fullstack"])

# --------------------------
# Load Questions from JSON
# --------------------------
try:
    with open("questions.json", "r") as f:
        all_questions = json.load(f)
    questions = all_questions.get(course, [])
except Exception as e:
    st.error(f"⚠️ Failed to load questions: {e}")
    questions = []

# --------------------------
# Display Questions & Inputs
# --------------------------
st.markdown("---")
st.subheader(f"📝 Questions for {course.upper()}")

answers = []
for i, q in enumerate(questions):
    ans = st.text_input(f"{i+1}. {q}")
    answers.append(ans)

# --------------------------
# Predict Button
# --------------------------
if st.button("🧠 Analyze My Skill Level"):
    # Validation
    if not student_name.strip():
        st.error("Please enter your name.")
    elif any(not a.strip() for a in answers):
        st.error("Please answer all questions.")
    else:
        # Combine responses
        combined_response = " ".join(answers)
        level = predict_level(course, combined_response)

        # Level description
        level_desc = {
            1: "🟢 **Beginner** – Start with foundational concepts and hands-on projects.",
            2: "🟡 **Intermediate** – You're progressing well. Try more real-world applications.",
            3: "🔴 **Advanced** – Great job! Consider contributing to open source or mentoring."
        }

        # Show result
        st.success(f"Hi **{student_name}**, your skill level in **{course.upper()}** is: **Level {level}**")
        st.info(level_desc[level])

        # Save to CSV
        df = pd.DataFrame({
            "name": [student_name],
            "course": [course],
            "level": [level],
            **{f"answer{i+1}": [ans] for i, ans in enumerate(answers)}
        })

        try:
            df.to_csv("student_responses.csv", mode="a", header=not pd.io.common.file_exists("student_responses.csv"), index=False)
            st.success("📁 Your responses have been saved successfully!")
        except Exception as e:
            st.error(f"Error saving data: {e}")
