"""
AI Study Buddy - Main Application
Premium exam preparation assistant with RAG, web search, and specialized study tools
"""

import streamlit as st
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Import custom modules
from study_buddy_agent import StudyBuddyAgent
from document_processor import DocumentProcessor
from exam_tools import ExamTools
from styles import get_custom_css

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Study Buddy - Your Exam Preparation Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent" not in st.session_state:
    st.session_state.agent = None
if "doc_processor" not in st.session_state:
    st.session_state.doc_processor = DocumentProcessor()
if "study_time" not in st.session_state:
    st.session_state.study_time = 0
if "topics_covered" not in st.session_state:
    st.session_state.topics_covered = []
if "exam_date" not in st.session_state:
    st.session_state.exam_date = str((datetime.now() + timedelta(days=30)).date())


def initialize_agent():
    """Initialize the Study Buddy Agent"""
    if st.session_state.agent is None:
        try:
            st.session_state.agent = StudyBuddyAgent()
            return True
        except Exception as e:
            st.error(f"Error initializing agent: {e}")
            return False
    return True


def sidebar():
    """Render sidebar with document management and stats"""
    with st.sidebar:
        st.markdown("# 🎓 AI Study Buddy")
        st.markdown("*Your Personal Exam Preparation Assistant*")
        st.divider()
        
        # Document Upload Section
        st.markdown("### 📚 Knowledge Base")
        
        uploaded_files = st.file_uploader(
            "Upload your study materials",
            type=["pdf", "txt", "md"],
            accept_multiple_files=True,
            help="Upload PDFs, text files, or markdown documents"
        )
        
        if uploaded_files:
            if st.button("📥 Process Documents", use_container_width=True):
                with st.spinner("Processing documents..."):
                    try:
                        file_paths = st.session_state.doc_processor.save_uploaded_files(uploaded_files)
                        documents = st.session_state.doc_processor.load_documents(file_paths)
                        st.session_state.doc_processor.create_or_update_vectorstore(documents)
                        st.success(f"✅ Processed {len(uploaded_files)} documents!")
                        st.balloons()
                    except Exception as e:
                        st.error(f"Error processing documents: {e}")
        
        # Document List
        docs = st.session_state.doc_processor.list_documents()
        if docs:
            with st.expander(f"📄 Documents ({len(docs)})", expanded=False):
                for doc in docs:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.text(f"📄 {doc['name'][:25]}...")
                        st.caption(f"Modified: {doc['modified']}")
                    with col2:
                        if st.button("🗑️", key=f"del_{doc['name']}"):
                            st.session_state.doc_processor.delete_document(doc['path'])
                            st.rerun()
        
        st.divider()
        
        # Study Stats
        st.markdown("### 📊 Study Stats")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Documents", len(docs), delta=None)
        with col2:
            st.metric("Topics", len(st.session_state.topics_covered), delta=None)
        
        # Exam Date
        st.markdown("### 📅 Exam Info")
        exam_date = st.date_input(
            "Exam Date",
            value=datetime.fromisoformat(st.session_state.exam_date).date(),
            min_value=datetime.now().date()
        )
        st.session_state.exam_date = str(exam_date)
        
        days_left = (exam_date - datetime.now().date()).days
        if days_left > 0:
            st.info(f"⏰ {days_left} days until exam!")
        
        st.divider()
        
        # Quick Actions
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("📝 Generate Study Plan", use_container_width=True):
            st.session_state.messages.append({
                "role": "user",
                "content": f"Create a study plan for my exam on {exam_date}"
            })
            st.rerun()
        
        if st.button("❓ Get Important Questions", use_container_width=True):
            st.session_state.messages.append({
                "role": "user",
                "content": "Generate important questions from my study materials"
            })
            st.rerun()
        
        if st.button("📚 Create Flashcards", use_container_width=True):
            st.session_state.messages.append({
                "role": "user",
                "content": "Create flashcards from my documents"
            })
            st.rerun()
        
        st.divider()
        
        # About
        with st.expander("ℹ️ About", expanded=False):
            st.markdown("""
            **AI Study Buddy Features:**
            - 📖 Multi-document RAG
            - 🌐 Web search (Tavily)
            - 📝 16-mark answers
            - 📅 Study plans
            - 🎯 Quiz generation
            - 🃏 Flashcards
            - 💡 Concept explanations
            
            **Powered by:**
            - LangGraph
            - GROQ (Llama 3.3)
            - ChromaDB
            """)
        
        # Clear button
        if st.session_state.messages:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.messages = []
                st.rerun()


def chat_interface():
    """Main chat interface"""
    # Header
    st.markdown("## 💬 Study Assistant")
    st.markdown("*Ask anything about your studies - I'm here to help you ace your exams!*")
    st.divider()
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Show sources if available (in expander to keep it clean)
            if "sources" in message and message["sources"]:
                with st.expander("📚 View Sources", expanded=False):
                    for source in message["sources"]:
                        st.caption(f"• {source}")
    
    # Check if there's a pending message from quick actions
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        # If the last message is from user and we haven't generated a response yet
        # This happens when a quick action button is clicked
        if len(st.session_state.messages) == 1 or st.session_state.messages[-2]["role"] != "user":
            prompt = st.session_state.messages[-1]["content"]
            
            with st.chat_message("assistant"):
                with st.spinner("Thinking... 🤔"):
                    try:
                        if not initialize_agent():
                            st.error("⚠️ Please check your API keys in the .env file")
                            return
                        
                        result = st.session_state.agent.query(prompt)
                        answer = result.get("answer", "I apologize, I couldn't generate an answer. Please try again.")
                        documents = result.get("documents", [])
                        
                        st.markdown(answer)
                        
                        if documents:
                            sources = []
                            for doc in documents:
                                if "source" in doc.metadata:
                                    sources.append(doc.metadata["source"])
                            
                            if sources:
                                sources = list(set(sources))
                                with st.expander("📚 View Sources", expanded=False):
                                    for source in sources:
                                        st.caption(f"• {source}")
                                
                                st.session_state.messages.append({
                                    "role": "assistant",
                                    "content": answer,
                                    "sources": sources
                                })
                            else:
                                st.session_state.messages.append({
                                    "role": "assistant",
                                    "content": answer
                                })
                        else:
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": answer
                            })
                    except Exception as e:
                        error_msg = f"❌ **Error:** {str(e)}\n\n💡 **Tip:** Make sure your API keys are set in the `.env` file"
                        st.error(error_msg)
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": error_msg
                        })
    
    # Chat input
    if prompt := st.chat_input("💬 Type your question here..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking... 🤔"):
                try:
                    if not initialize_agent():
                        st.error("⚠️ Please check your API keys in the .env file")
                        return
                    
                    result = st.session_state.agent.query(prompt)
                    answer = result.get("answer", "I apologize, I couldn't generate an answer. Please try again.")
                    documents = result.get("documents", [])
                    
                    st.markdown(answer)
                    
                    if documents:
                        sources = []
                        for doc in documents:
                            if "source" in doc.metadata:
                                sources.append(doc.metadata["source"])
                        
                        if sources:
                            sources = list(set(sources))
                            with st.expander("📚 View Sources", expanded=False):
                                for source in sources:
                                    st.caption(f"• {source}")
                            
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": answer,
                                "sources": sources
                            })
                        else:
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": answer
                            })
                    else:
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": answer
                        })
                except Exception as e:
                    error_msg = f"❌ **Error:** {str(e)}\n\n💡 **Tip:** Make sure your API keys are set in the `.env` file"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })




def exam_mode_tab():
    """Exam simulation mode"""
    st.markdown("## 📝 Exam Mode")
    st.markdown("Practice with timed exams and instant feedback!")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        num_questions = st.number_input("Number of Questions", min_value=5, max_value=20, value=10)
    
    with col2:
        difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
    
    with col3:
        time_limit = st.number_input("Time Limit (minutes)", min_value=15, max_value=180, value=60)
    
    topic = st.text_input("Topic/Subject", placeholder="e.g., Machine Learning, Physics, History")
    
    if st.button("🚀 Start Exam", use_container_width=True):
        with st.spinner("Generating exam..."):
            try:
                if not initialize_agent():
                    st.error("Failed to initialize agent. Please check your API keys.")
                    return
                
                result = st.session_state.agent.exam_tools.generate_quiz(
                    topic, 
                    num_questions=num_questions, 
                    difficulty=difficulty.lower()
                )
                
                st.markdown("### Your Exam:")
                st.markdown(result["quiz"])
                
                st.info(f"⏰ Time Limit: {time_limit} minutes")
                
            except Exception as e:
                st.error(f"Error generating exam: {e}")


def study_planner_tab():
    """Study plan generator"""
    st.markdown("## 📅 Study Planner")
    st.markdown("Get a personalized study schedule!")
    
    topics_input = st.text_area(
        "Topics to Cover (one per line)",
        placeholder="Machine Learning\nDeep Learning\nNatural Language Processing",
        height=150
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        exam_date = st.date_input(
            "Exam Date",
            value=datetime.fromisoformat(st.session_state.exam_date).date(),
            min_value=datetime.now().date()
        )
    
    with col2:
        hours_per_day = st.slider("Study Hours Per Day", min_value=1, max_value=12, value=3)
    
    if st.button("📊 Generate Study Plan", use_container_width=True):
        with st.spinner("Creating your personalized study plan..."):
            try:
                if not initialize_agent():
                    st.error("Failed to initialize agent. Please check your API keys.")
                    return
                
                topics = [t.strip() for t in topics_input.split("\n") if t.strip()]
                
                if not topics:
                    st.warning("Please enter at least one topic!")
                    return
                
                result = st.session_state.agent.exam_tools.generate_study_plan(
                    topics,
                    str(exam_date),
                    hours_per_day
                )
                
                st.markdown("### Your Personalized Study Plan:")
                st.markdown(result["plan"])
                
                st.success("✅ Study plan generated! Follow this to ace your exam!")
                
            except Exception as e:
                st.error(f"Error generating study plan: {e}")


def help_tab():
    """Help and examples"""
    st.markdown("## 🆘 Help & Examples")
    
    st.markdown("""
    ### How to Use AI Study Buddy
    
    #### 1. Upload Documents
    - Click **Browse files** in the sidebar
    - Upload your PDFs, notes, textbooks
    - Click **Process Documents**
    
    #### 2. Ask Questions
    The AI understands various question types:
    
    **📝 For 16-Mark Answers:**
    - "Give me a 16-mark answer on Machine Learning"
    - "Explain Neural Networks in exam format"
    
    **📅 For Study Plans:**
    - "Create a study plan for my exam"
    - "How should I prepare for the next 30 days?"
    
    **🎯 For Quizzes:**
    - "Generate a quiz on Deep Learning"
    - "Test me on Python programming"
    
    **🃏 For Flashcards:**
    - "Create flashcards on Data Structures"
    - "Make flashcards from my uploaded notes"
    
    **💡 For Explanations:**
    - "Explain gradient descent"
    - "What is quantum computing?"
    
    **❓ For Important Questions:**
    - "What are important questions on AI?"
    - "Give me likely exam questions"
    
    #### 3. Explore Different Modes
    - **Chat**: Natural conversation with your study buddy
    - **Exam Mode**: Practice with timed tests
    - **Study Planner**: Get organized schedules
    
    ### Features That Make This Better Than ChatGPT
    
    ✅ **Document-Aware**: Answers based on YOUR study materials
    ✅ **Exam-Focused**: Structured 16-mark answers, not generic responses
    ✅ **Study Planning**: Personalized schedules based on your exam date
    ✅ **Progress Tracking**: Track topics covered and study time
    ✅ **Multiple Tools**: Quiz, flashcards, important questions in one place
    ✅ **Web Search**: Combines your docs + latest info from internet
    
    ### Tips for Best Results
    
    1. **Upload comprehensive materials** - The more context, the better answers
    2. **Be specific** - "16-mark answer on Neural Networks" vs "Tell me about NN"
    3. **Set your exam date** - For accurate study plans
    4. **Use different modes** - Variety helps learning
    5. **Review sources** - Check what documents were used for answers
    
    ### Example Questions to Try
    
    ```
    "Give me a 16-mark answer on the French Revolution"
    
    "Create a 2-week study plan covering these topics: Statistics, Probability, Linear Algebra"
    
    "Generate a medium difficulty quiz with 5 questions on Thermodynamics"
    
    "Explain backpropagation in neural networks with examples"
    
    "What are the top 10 important questions for my Biology exam?"
    
    "Create flashcards covering the key concepts in my uploaded notes"
    ```
    
    ### Need Help?
    
    - Make sure you've added your API keys to the `.env` file
    - Check that documents are uploaded and processed
    - Try different phrasings if the AI doesn't understand
    - Use the sidebar quick actions for common tasks
    """)


def main():
    """Main application"""
    # Render sidebar
    sidebar()
    
    # Main content area with tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "💬 Chat", 
        "📝 Exam Mode", 
        "📅 Study Planner", 
        "🆘 Help"
    ])
    
    with tab1:
        chat_interface()
    
    with tab2:
        exam_mode_tab()
    
    with tab3:
        study_planner_tab()
    
    with tab4:
        help_tab()
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #b8b8d1; padding: 1rem;'>
        <p>🎓 <strong>AI Study Buddy</strong> - Your Personal Exam Preparation Assistant</p>
        <p style='font-size: 0.9rem;'>Powered by LangGraph • GROQ • Tavily • ChromaDB</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
