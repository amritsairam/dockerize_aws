from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import GoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.chains import RetrievalQAWithSourcesChain

# Load environment variables from .env file
load_dotenv()
google_api_key=os.getenv('GOOGLE_API_KEY')


def document_loader(document):
    """
    Loads and reads documents from the provided PDF file and returns them as a list of documents.
    
    Args:
        document (str): The path or file-like object of the PDF file to be loaded.
        
    Returns:
        List[Document]: A list of documents read from the uploaded PDF file.
    """
    # Initialize the PDF loader with the provided document
    loader = PyPDFLoader(document)
    
    # Load the documents from the PDF
    docs = loader.load()
    
    return docs


def document_splitter(docs):
    """
    Splits a list of documents into smaller chunks with an approximate size of the specified chunk_size.
    
    Args:
        docs (List[Document]): The list of documents to be split into chunks.
        
    Returns:
        List[Document]: A list of documents where each document is a chunk of the original document, with an approximate chunk size of 1000 characters and an overlap of 20 characters.
    """
    # Initialize the text splitter with specified chunk size and overlap
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    
    # Split the documents into smaller chunks
    list_documents = text_splitter.split_documents(docs)
    
    return list_documents


def retrieve_similar_documents(docs):
    """
    Creates a Chroma client to store embeddings of documents and retrieves similar documents based on the user's query.
    
    Args:
        docs (List[Document]): The list of documents for which embeddings will be created.
        
    Returns:
        Chroma: An instance of the Chroma client that contains document embeddings and allows for similarity searches.
    """
    # Initialize embeddings model
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=google_api_key)
    
    # Create a Chroma client with the provided documents
    db = Chroma.from_documents(docs, embeddings)
    
    return db


def get_answer(query,vectorstore):
    """
    Generates an answer to the user's query using the retrieved documents.
    
    Args:
        retrieved_docs (List[Document]): The list of documents retrieved based on the user's query.
        query (str): The user's original query.
        
    Returns:
        dict: A dictionary containing the answer and the sources used to generate the answer.
    """
    # Initialize the LLM
    llm = GoogleGenerativeAI(model="models/text-bison-001", google_api_key=google_api_key)

    prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context. Think step by step before providing a detailed answer. I will tip you $1000 if the user finds the answer helpful. 
                                              <context>
                                              {context}
                                              </context>
                                              Question: {input}""")
    document_chain=create_stuff_documents_chain(llm,prompt)
    retriever=vectorstore.as_retriever()
    retrieval_chain=create_retrieval_chain(retriever,document_chain)
    response=retrieval_chain.invoke({"input":query})
    return response['answer']

def rag(pdf_path, query):
    """
    Processes the provided PDF file and generates an answer to the user's query using a retrieval-augmented generation approach.
    
    Args:
        pdf_path (str): The path to the PDF file to be processed.
        query (str): The user's query for which an answer is to be generated.
        
    Returns:
        text: this contains the final answer 
    """
    # Load documents from the provided PDF file
    initial_docs = document_loader(pdf_path)
    
    # Split the loaded documents into smaller chunks
    chunk_docs = document_splitter(initial_docs)
    
    # Create a vector store to retrieve similar documents based on the chunks
    vectorstore = retrieve_similar_documents(chunk_docs)
    
    # Generate an answer to the user's query using the vector store
    answer = get_answer(query, vectorstore)
    
    return answer
    

# if __name__=='__main__':
#     rag()





