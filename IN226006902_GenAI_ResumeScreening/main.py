import os
from dotenv import load_dotenv

load_dotenv()

from chains.pipeline import evaluate_resume
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq


def load_file(path):
    with open(path, "r") as f:
        return f.read()


job = load_file("data/job.txt")

resumes = {
    "Strong": load_file("data/strong.txt"),
    "Average": load_file("data/average.txt"),
    "Weak": load_file("data/weak.txt"),
}


for name, resume in resumes.items():
    print("\n" + "="*50)
    print(f"--- {name} Candidate ---")

    result = evaluate_resume(resume, job)

    print("\n🔹 Extracted Info:\n")
    print(result["extracted"])

    print("\n🔹 Match Analysis:\n")
    print(result["match"])

    print("\n🔹 Score & Explanation:\n")
    print(result["score"])


#DEBUG EXAMPLE 
print("\n" + "="*50)
print("\n--- Debug Example (Bad Prompt) ---")

llm = ChatGroq(model="llama-3.1-8b-instant")

# Bad prompt 
bad_prompt = PromptTemplate.from_template("Analyze resume")

bad_chain = bad_prompt | llm

debug_output = bad_chain.invoke({"resume": resumes["Weak"]}).content

print("\nBad Output:\n")
print(debug_output)

print("\nExplanation:")
print("The above output is vague and lacks structure because the prompt is unclear.")
print("Improved prompts with explicit instructions were used in the pipeline to fix this.")