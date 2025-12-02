"""
Document Processor for AI Study Buddy
Handles multi-format document upload, processing, and vector store management
"""

import os
from typing import List, Dict, Optional
from datetime import datetime
import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document


class DocumentProcessor:
    """Handles document processing and vector store management"""
    
    def __init__(self, persist_directory: str = "chroma_db", knowledge_base_dir: str = "knowledge-base"):
        self.persist_directory = persist_directory
        self.knowledge_base_dir = knowledge_base_dir
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        
        # Create knowledge base directory if it doesn't exist
        os.makedirs(knowledge_base_dir, exist_ok=True)
    
    def save_uploaded_files(self, uploaded_files, subject: str = "General") -> List[str]:
        """Save uploaded files to knowledge base directory"""
        saved_files = []
        
        for uploaded_file in uploaded_files:
            file_path = os.path.join(self.knowledge_base_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            saved_files.append(file_path)
        
        return saved_files
    
    def load_documents(self, file_paths: Optional[List[str]] = None, subject: str = "General") -> List[Document]:
        """Load documents from file paths or entire knowledge base"""
        documents = []
        
        # If no specific files, load all from knowledge base
        if file_paths is None:
            if not os.path.exists(self.knowledge_base_dir):
                return []
            
            file_paths = []
            for file_name in os.listdir(self.knowledge_base_dir):
                file_paths.append(os.path.join(self.knowledge_base_dir, file_name))
        
        # Load each file
        for file_path in file_paths:
            try:
                if file_path.lower().endswith(".pdf"):
                    loader = PyPDFLoader(file_path)
                    docs = loader.load()
                elif file_path.lower().endswith(".txt") or file_path.lower().endswith(".md"):
                    loader = TextLoader(file_path, encoding='utf-8')
                    docs = loader.load()
                else:
                    continue
                
                # Add metadata
                for doc in docs:
                    doc.metadata.update({
                        "source": os.path.basename(file_path),
                        "subject": subject,
                        "upload_date": datetime.now().isoformat(),
                        "file_path": file_path
                    })
                
                documents.extend(docs)
                
            except Exception as e:
                st.warning(f"Error loading {file_path}: {e}")
        
        return documents
    
    def chunk_documents(self, documents: List[Document], chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
        """Split documents into chunks"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        return text_splitter.split_documents(documents)
    
    def create_or_update_vectorstore(self, documents: List[Document]) -> Chroma:
        """Create or update the vector store"""
        chunks = self.chunk_documents(documents)
        
        if os.path.exists(self.persist_directory):
            # Update existing vector store
            vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
            vectorstore.add_documents(chunks)
        else:
            # Create new vector store
            vectorstore = Chroma.from_documents(
                chunks,
                self.embeddings,
                persist_directory=self.persist_directory
            )
        
        vectorstore.persist()
        return vectorstore
    
    def get_vectorstore(self) -> Optional[Chroma]:
        """Get existing vector store"""
        if not os.path.exists(self.persist_directory):
            return None
        
        return Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )
    
    def get_retriever(self, k: int = 5):
        """Get retriever from vector store"""
        vectorstore = self.get_vectorstore()
        if vectorstore is None:
            return None
        return vectorstore.as_retriever(search_kwargs={"k": k})
    
    def list_documents(self) -> List[Dict]:
        """List all documents in knowledge base"""
        if not os.path.exists(self.knowledge_base_dir):
            return []
        
        docs = []
        for file_name in os.listdir(self.knowledge_base_dir):
            file_path = os.path.join(self.knowledge_base_dir, file_name)
            if os.path.isfile(file_path):
                stat = os.stat(file_path)
                docs.append({
                    "name": file_name,
                    "path": file_path,
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
                })
        
        return sorted(docs, key=lambda x: x["modified"], reverse=True)
    
    def delete_document(self, file_path: str) -> bool:
        """Delete a document from knowledge base"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
        except Exception as e:
            st.error(f"Error deleting file: {e}")
        return False
    
    def clear_vectorstore(self):
        """Clear the entire vector store"""
        if os.path.exists(self.persist_directory):
            import shutil
            shutil.rmtree(self.persist_directory)
