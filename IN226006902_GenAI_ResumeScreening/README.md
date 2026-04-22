# 🧠 AI Resume Screening System (LangChain + LangSmith)

This project implements an AI-powered Resume Screening System using **LangChain** and **LangSmith**.  
It evaluates candidates based on a given job description and provides a **fit score with explanation**.

---

## 🚀 Objective

The goal of this project is to:
- Build an LLM-based resume evaluation system
- Extract skills, experience, and tools from resumes
- Match resumes with job requirements
- Assign a score (0–100)
- Provide explainable reasoning
- Enable tracing using LangSmith

---

## ⚙️ Tech Stack

- Python  
- LangChain (LCEL)  
- LangSmith (Tracing)  
- Groq API (LLM)  

---

## 📂 Project Structure
resume-screening/
│
├── prompts/ # Prompt templates
├── chains/ # Pipeline logic
├── data/ # Sample resumes + job description
├── main.py # Entry point
├── requirements.txt
└── README.md

---

## 🔄 Pipeline Flow
Resume → Skill Extraction → Matching → Scoring → Explanation


---

## 🧠 Features

✔ Skill extraction (skills, experience, tools)  
✔ Resume-job matching analysis  
✔ Score generation (0–100)  
✔ Clear explanation for score  
✔ Debug example (prompt improvement)  
✔ LangSmith tracing for monitoring  

---

## 📥 Input

- 1 Job Description (Data Scientist role)  
- 3 Resumes:
  - Strong candidate  
  - Average candidate  
  - Weak candidate  

---

## 📤 Output

For each candidate:

- Extracted information  
- Matching analysis  
- Score (0–100)  
- Explanation  

---

## 🧪 Debugging

A bad prompt example is included to demonstrate:
- Incorrect output  
- Improvement using better prompt engineering  

---

## 📊 LangSmith Tracing

Tracing is enabled using:
LANGCHAIN_TRACING_V2=true

This allows:
- Monitoring pipeline steps  
- Debugging outputs  
- Viewing execution flow  

---