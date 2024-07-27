import uuid
import os
import faiss
import cloudpickle
import torch
import requests
import bs4
from operator import itemgetter
from langchain.document_loaders import HuggingFaceDatasetLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, TokenTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore.in_memory import InMemoryDocstore
from langchain.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA
from langchain.prompt import PromptTemplate
from langchain.schema.runnable import RunnableMap, RunnablePassthrough, StrOutputParser
from langchain.schema import Document
from transformers import (
    AutoTokenizer,
    AutoModelForQuestionAnswering,
    pipeline,
    AutoModelForCausalLM,
    BitsAndBytesConfig,
)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex, VectorIndexRetriever, RetrieverQueryEngine, SimilarityPostprocessor
import pandas as pd
def load_data(lang):
    if(lang == 'c++'):
        return pd.read_csv('codescpp.csv')
    elif(lang == 'java'):
        return pd.read_csv('codesjava.csv')
    elif(lang=='python'):
        return pd.read_csv('codespy.csv')
def mod():
    modelPath = "sentence-transformers/all-MiniLM-l6-v2"
    model_kwargs = {'device':'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    embeddings = HuggingFaceEmbeddings(
        model_name=modelPath,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    return embeddings
def retriever(embeddings,data):
    documents = [Document(page_content=text) for text in data]
    db = FAISS.from_documents(documents, embeddings)
    return db
def recommenderL(question,db):
    searchDocs = db.similarity_search(question,5)
    return searchDocs
def leetcode(question,db):
    searchDocs = db.similarity_search(question,1)
    return searchDocs[0].page_content
def new_question(question,db):
    searchDocs = db.similarity_search(question,1)
    return searchDocs
