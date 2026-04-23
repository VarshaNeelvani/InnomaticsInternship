from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph
from typing import TypedDict, List

loader = PyPDFLoader("data.pdf")
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = splitter.split_documents(docs)

embedding = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embedding,
    persist_directory="./db"
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

llm = ChatGroq(
    model="llama-3.1-8b-instant"
)

def get_answer(query, docs):
    context = "\n".join([d.page_content for d in docs])

    prompt = f"""
    You are a customer support assistant.
    Answer ONLY from the context.
    If unsure, say "I don’t know".
    
    Context:
    {context}
    
    Question:
    {query}
    """

    response = llm.invoke(prompt)
    return response.content


class State(TypedDict):
    query: str
    docs: List
    answer: str
    confidence: float
    escalate: bool


def process_node(state):
    query = state.get("query", "")

    docs = retriever.invoke(query)
    answer = get_answer(query, docs)

    state["docs"] = docs
    state["answer"] = answer

    state["confidence"] = 0.9 if docs else 0.2

    return {
    "query": query,
    "docs": docs,
    "answer": answer,
    "confidence": 0.9 if docs else 0.2
}


def decision_node(state):
    escalate = False

    if state["confidence"] < 0.5 or "I don’t know" in state["answer"]:
        escalate = True

    return {**state, "escalate": escalate}


def output_node(state):
    print("\nAnswer:", state["answer"])
    return state


def hitl_node(state):
    print("\nEscalating to human...")
    human = input("Enter human response: ")
    print("\nFinal Answer:", human)
    return state


graph = StateGraph(State)

graph.add_node("process", process_node)
graph.add_node("decision", decision_node)
graph.add_node("output", output_node)
graph.add_node("hitl", hitl_node)

graph.set_entry_point("process")
graph.add_edge("process", "decision")

def route(state):
    return "hitl" if state["escalate"] else "output"

graph.add_conditional_edges("decision", route)

app = graph.compile()


while True:
    query = input("\nAsk something (type 'exit' to quit): ")

    if query.lower() == "exit":
        break

    app.invoke({"query": query})