# from google import genai
# from langsmith import wrappers
from dotenv import load_dotenv
import os
import pyperclip

load_dotenv()

# DEFAULT_MODEL = "gemini-2.5-flash"


# def main():
#     if not os.getenv("GOOGLE_API_KEY") and not os.getenv("GEMINI_API_KEY"):
#         raise RuntimeError("Set GOOGLE_API_KEY or GEMINI_API_KEY in your environment.")

#     # genai.Client() reads GOOGLE_API_KEY / GEMINI_API_KEY from the environment
#     gemini_client = genai.Client()

#     # Wrap the Gemini client to enable LangSmith tracing
#     client = wrappers.wrap_gemini(
#         gemini_client,
#         tracing_extra={
#             "tags": ["gemini", "python"],
#             "metadata": {
#                 "integration": "google-genai",
#             },
#         },
#     )

#     # Make a traced Gemini call
#     response = client.models.generate_content(
#         model=os.getenv("GEMINI_MODEL", DEFAULT_MODEL),
#         contents="Explain quantum computing in simple terms.",
#     )

#     print(response.text)


# if __name__ == "__main__":
#     main()


from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore


 
file_path = Path(__file__).resolve().parent / "yash_resume.pdf"

loader = PyPDFLoader(file_path)

docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)
all_splits = text_splitter.split_documents(docs)

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
vector_store = InMemoryVectorStore(embeddings)

vector_store.add_documents(all_splits)

for chunk in all_splits:
    embedding = embeddings.embed_query(chunk.page_content)


results = vector_store.similarity_search(
    "What work did Yash do at BharatPe?"
)

print(results[0].page_content)
