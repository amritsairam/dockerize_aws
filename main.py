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
    '''
    this function will return a list of documents read from the uploaded pdf file
    '''
    loader = PyPDFLoader(document)
    docs = loader.load()
    return docs

def document_splitter(docs):
    '''
    this function will return list of documents with approximate chunk size of mentioned chunk_size
    '''
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    list_documents=text_splitter.split_documents(docs)
    return list_documents

def retrieve_similar_documents(docs):
    '''
    this creates a chroma client to store embeddings of documents and retrieves similar documents related to the query provided by the user
    '''
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key=google_api_key)
    db=Chroma.from_documents(docs,embeddings)
    # results=db.similarity_search(query,k=3)
    return db

# def answer(documents):
#     llm = GoogleGenerativeAI(model="models/text-bison-001", google_api_key=google_api_key)
#     prompt = ChatPromptTemplate.from_template(""" Answer the following question based only on the provided context.  Think step by step before providing a detailed answer. I will tip you $1000 if the user finds the answer helpful.
#                                                <context> {context} </context>
#                                               Question: {input}""")
#     document_chain=create_stuff_documents_chain(llm,prompt)
#     retriever=vectorstore.as_retriever()
    

from langchain.chains import RetrievalQAWithSourcesChain

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

def rag(pdf_path,query):
    initial_docs=document_loader(pdf_path)
    chunk_docs=document_splitter(initial_docs)
    vectorstore=retrieve_similar_documents(chunk_docs)
    answer=get_answer(query,vectorstore)
    return answer
    

if __name__=='__main__':
    rag()





