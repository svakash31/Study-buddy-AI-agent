"""
LangGraph Agent for AI Study Buddy
Orchestrates multiple tools: RAG, Web Search, Exam Tools
"""

from typing import List, Literal
from typing_extensions import TypedDict
from langchain_core.documents import Document
from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langchain_community.document_loaders import WebBaseLoader
from langgraph.graph import START, END, StateGraph
import streamlit as st

from document_processor import DocumentProcessor
from exam_tools import ExamTools


# Graph State Definition
class AgentState(TypedDict):
    question: str
    documents: List[Document]
    context: str
    answer: str
    tool_used: str
    metadata: dict


class StudyBuddyAgent:
    """LangGraph agent for AI Study Buddy"""
    
    def __init__(self, llm_model: str = "llama-3.3-70b-versatile"):
        self.llm = ChatGroq(temperature=0.3, model_name=llm_model)
        self.doc_processor = DocumentProcessor()
        self.exam_tools = ExamTools(llm_model=llm_model)
        self.tavily_search = TavilySearch(max_results=3, search_depth="advanced")
        self.graph = self._build_graph()
    
    def _router_node(self, state: AgentState) -> Literal["rag_tool", "web_search", "exam_answer", "study_plan", "quiz", "flashcards", "explain", "important_questions"]:
        """Route to appropriate tool based on question"""
        question = state["question"].lower()
        
        routing_prompt = f"""You are an intelligent router for a study assistant. Analyze the user's question and decide which tool to use.

AVAILABLE TOOLS:
- **rag_tool**: Search uploaded study documents (PDFs, notes)
- **web_search**: Search internet for current/latest information
- **exam_answer**: Generate structured 16-mark exam answer
- **study_plan**: Create study schedule and plan
- **quiz**: Generate quiz questions on a topic
- **flashcards**: Create flashcard deck for memorization
- **explain**: Explain a concept in detail with examples
- **important_questions**: Generate likely important exam questions

USER QUESTION: "{state["question"]}"

ROUTING LOGIC:
- If asking for "16 mark answer" or "exam answer" → exam_answer
- If asking for "study plan" or "schedule" or "how to prepare" → study_plan
- If asking for "quiz" or "test" or "practice questions" → quiz
- If asking for "flashcards" → flashcards
- If asking "explain" or "what is" → explain
- If asking for "important questions" → important_questions
- If asking about general knowledge or current events → web_search
- Otherwise → rag_tool (search uploaded documents)

Respond with ONLY the tool name, nothing else."""

        response = self.llm.invoke(routing_prompt)
        decision = response.content.strip().lower()
        
        # Map decision to actual tool names
        tool_map = {
            "exam_answer": "exam_answer",
            "study_plan": "study_plan",
            "quiz": "quiz",
            "flashcards": "flashcards",
            "explain": "explain",
            "important_questions": "important_questions",
            "web_search": "web_search",
            "rag_tool": "rag_tool"
        }
        
        for key, value in tool_map.items():
            if key in decision:
                return value
        
        return "rag_tool"  # default
    
    def _rag_tool_node(self, state: AgentState) -> AgentState:
        """Retrieve from vector store"""
        retriever = self.doc_processor.get_retriever(k=5)
        
        if retriever is None:
            return {
                "documents": [],
                "context": "No documents found in knowledge base. Please upload study materials first.",
                "tool_used": "rag_tool"
            }
        
        docs = retriever.invoke(state["question"])
        context = "\n\n".join([doc.page_content for doc in docs])
        
        return {
            "documents": docs,
            "context": context,
            "tool_used": "rag_tool"
        }
    
    def _web_search_node(self, state: AgentState) -> AgentState:
        """Search web and scrape content"""
        try:
            search_results = self.tavily_search.invoke(state["question"])
            
            scraped_docs = []
            if search_results and "results" in search_results:
                urls = [r.get("url") for r in search_results["results"] if r.get("url")]
                
                for url in urls[:2]:  # Limit to 2 URLs
                    try:
                        loader = WebBaseLoader(url)
                        docs = loader.load()
                        for doc in docs:
                            doc.metadata["source"] = url
                        scraped_docs.extend(docs)
                    except:
                        continue
            
            context = "\n\n".join([doc.page_content[:1000] for doc in scraped_docs])
            
            return {
                "documents": scraped_docs,
                "context": context if context else "No relevant web results found.",
                "tool_used": "web_search"
            }
        except Exception as e:
            return {
                "documents": [],
                "context": f"Web search error: {str(e)}",
                "tool_used": "web_search"
            }
    
    def _exam_answer_node(self, state: AgentState) -> AgentState:
        """Generate 16-mark answer"""
        # First get context from RAG
        retriever = self.doc_processor.get_retriever(k=5)
        context = ""
        docs = []
        
        if retriever:
            docs = retriever.invoke(state["question"])
            context = "\n\n".join([doc.page_content for doc in docs])
        
        # Generate answer
        result = self.exam_tools.generate_16_mark_answer(state["question"], context)
        
        return {
            "documents": docs,
            "context": context,
            "answer": result["answer"],
            "tool_used": "exam_answer",
            "metadata": result
        }
    
    def _study_plan_node(self, state: AgentState) -> AgentState:
        """Generate study plan"""
        # Extract topics and dates from question using LLM
        extract_prompt = f"""Extract study plan parameters from this question: "{state["question"]}"

Provide in this format:
TOPICS: [comma-separated list]
EXAM_DATE: [YYYY-MM-DD or 'not specified']
HOURS_PER_DAY: [number or 'not specified']

If information is missing, use reasonable defaults."""

        response = self.llm.invoke(extract_prompt)
        info = response.content
        
        # Parse (simplified - in production use better parsing)
        topics = ["General Topics"]  # default
        exam_date = (st.session_state.get("exam_date") if hasattr(st, "session_state") else 
                    str((datetime.now() + timedelta(days=30)).date()))
        hours_per_day = 3
        
        result = self.exam_tools.generate_study_plan(topics, exam_date, hours_per_day)
        
        return {
            "documents": [],
            "context": "",
            "answer": result["plan"],
            "tool_used": "study_plan",
            "metadata": result
        }
    
    def _quiz_node(self, state: AgentState) -> AgentState:
        """Generate quiz"""
        # Get context from RAG
        retriever = self.doc_processor.get_retriever(k=3)
        context = ""
        docs = []
        
        if retriever:
            docs = retriever.invoke(state["question"])
            context = "\n\n".join([doc.page_content for doc in docs])
        
        # Extract topic from question
        topic = state["question"].replace("quiz", "").replace("on", "").strip()
        
        result = self.exam_tools.generate_quiz(topic, num_questions=5, context=context)
        
        return {
            "documents": docs,
            "context": context,
            "answer": result["quiz"],
            "tool_used": "quiz",
            "metadata": result
        }
    
    def _flashcards_node(self, state: AgentState) -> AgentState:
        """Generate flashcards"""
        # Get context from RAG
        retriever = self.doc_processor.get_retriever(k=5)
        context = ""
        docs = []
        
        if retriever:
            docs = retriever.invoke(state["question"])
            context = "\n\n".join([doc.page_content for doc in docs])
        
        topic = state["question"].replace("flashcards", "").replace("on", "").strip()
        
        result = self.exam_tools.generate_flashcards(topic, context=context)
        
        return {
            "documents": docs,
            "context": context,
            "answer": result["flashcards"],
            "tool_used": "flashcards",
            "metadata": result
        }
    
    def _explain_node(self, state: AgentState) -> AgentState:
        """Explain a concept"""
        # Get context from RAG
        retriever = self.doc_processor.get_retriever(k=5)
        context = ""
        docs = []
        
        if retriever:
            docs = retriever.invoke(state["question"])
            context = "\n\n".join([doc.page_content for doc in docs])
        
        concept = state["question"].replace("explain", "").replace("what is", "").strip()
        
        result = self.exam_tools.explain_concept(concept, context=context)
        
        return {
            "documents": docs,
            "context": context,
            "answer": result["explanation"],
            "tool_used": "explain",
            "metadata": result
        }
    
    def _important_questions_node(self, state: AgentState) -> AgentState:
        """Generate important questions"""
        # Get context from RAG
        retriever = self.doc_processor.get_retriever(k=5)
        context = ""
        docs = []
        
        if retriever:
            docs = retriever.invoke(state["question"])
            context = "\n\n".join([doc.page_content for doc in docs])
        
        # Extract topic - handle generic requests
        topic = state["question"].replace("important questions", "").replace("from my study materials", "").replace("on", "").replace("generate", "").strip()
        
        # If no specific topic, use a general approach
        if not topic or len(topic) < 3:
            topic = "the topics covered in the study materials"
        
        result = self.exam_tools.generate_important_questions(topic, context=context)
        
        return {
            "documents": docs,
            "context": context,
            "answer": result["questions"],
            "tool_used": "important_questions",
            "metadata": result
        }
    
    def _generate_node(self, state: AgentState) -> AgentState:
        """Generate final answer using context"""
        # Only used for rag_tool and web_search
        question = state["question"]
        context = state.get("context", "")
        
        prompt = f"""You are an expert study assistant and tutor. Answer the student's question using the provided context.

CONTEXT:
{context}

QUESTION:
{question}

INSTRUCTIONS:
- Provide a clear, comprehensive answer
- Use the context when available
- If context doesn't have the answer, use your knowledge but mention this
- Format your answer well with headings, bullet points
- Include examples where helpful
- Be encouraging and supportive

ANSWER:"""

        response = self.llm.invoke(prompt)
        
        return {
            "answer": response.content,
            "tool_used": state.get("tool_used", "generate")
        }
    
    def _build_graph(self):
        """Build the LangGraph workflow"""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("rag_tool", self._rag_tool_node)
        workflow.add_node("web_search", self._web_search_node)
        workflow.add_node("exam_answer", self._exam_answer_node)
        workflow.add_node("study_plan", self._study_plan_node)
        workflow.add_node("quiz", self._quiz_node)
        workflow.add_node("flashcards", self._flashcards_node)
        workflow.add_node("explain", self._explain_node)
        workflow.add_node("important_questions", self._important_questions_node)
        workflow.add_node("generate", self._generate_node)
        
        # Add conditional routing from START
        workflow.add_conditional_edges(
            START,
            self._router_node,
            {
                "rag_tool": "rag_tool",
                "web_search": "web_search",
                "exam_answer": "exam_answer",
                "study_plan": "study_plan",
                "quiz": "quiz",
                "flashcards": "flashcards",
                "explain": "explain",
                "important_questions": "important_questions"
            }
        )
        
        # Tools that need generate node
        workflow.add_edge("rag_tool", "generate")
        workflow.add_edge("web_search", "generate")
        
        # Tools that go directly to END
        workflow.add_edge("exam_answer", END)
        workflow.add_edge("study_plan", END)
        workflow.add_edge("quiz", END)
        workflow.add_edge("flashcards", END)
        workflow.add_edge("explain", END)
        workflow.add_edge("important_questions", END)
        workflow.add_edge("generate", END)
        
        return workflow.compile()
    
    def query(self, question: str) -> dict:
        """Main query method"""
        inputs = {"question": question}
        
        result = None
        for output in self.graph.stream(inputs, stream_mode="values"):
            result = output
        
        return result if result else {"answer": "Error processing query", "tool_used": "error"}


# Import datetime for study_plan_node
from datetime import datetime, timedelta
