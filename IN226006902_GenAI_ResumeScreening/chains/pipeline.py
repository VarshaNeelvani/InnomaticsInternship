from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq


# Initialize LLM
def get_llm():
    return ChatGroq(model="llama-3.1-8b-instant")


# Load prompts
def load_prompt(path):
    with open(path, "r") as f:
        return f.read()


# Load prompt templates
extract_prompt = PromptTemplate.from_template(load_prompt("prompts/extract_prompt.txt"))
match_prompt = PromptTemplate.from_template(load_prompt("prompts/match_prompt.txt"))
score_prompt = PromptTemplate.from_template(load_prompt("prompts/score_prompt.txt"))


# Main pipeline
def evaluate_resume(resume, job):

    llm = get_llm()   # ✅ LLM initialized here

    # Chains (LCEL)
    extract_chain = extract_prompt | llm
    match_chain = match_prompt | llm
    score_chain = score_prompt | llm

    extracted = extract_chain.invoke({"resume": resume}).content

    match = match_chain.invoke({
        "job": job,
        "resume": resume
    }).content

    score = score_chain.invoke({
        "job": job,
        "resume": resume,
        "match": match
    }).content

    return {
        "extracted": extracted,
        "match": match,
        "score": score
    }