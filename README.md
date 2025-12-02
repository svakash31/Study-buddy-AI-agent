# 🎓 AI Study Buddy - Your Personal Exam Preparation Assistant

An intelligent AI-powered study companion that goes beyond traditional chatbots! Built with LangGraph, this application combines RAG (Retrieval Augmented Generation), web search, and specialized exam preparation tools to help you ace your exams.

## ✨ Features

### 🚀 Core Capabilities
- **📚 Multi-Document RAG**: Upload PDFs, text files, and markdown documents to create your personalized knowledge base
- **🌐 Web Search Integration**: Powered by Tavily to fetch the latest information from the internet
- **🤖 Intelligent Agent**: LangGraph-based agent that routes to the right tool automatically

### 🎯 Specialized Exam Tools
- **📝 16-Mark Answer Generator**: Get structured, comprehensive exam-style answers
- **📅 Study Plan Generator**: Personalized study schedules based on your exam date
- **🎯 Quiz Generator**: Practice with auto-generated quizzes from your materials
- **🃏 Flashcard Creator**: Auto-extract key concepts for quick revision
- **💡 Concept Explainer**: Detailed explanations with examples and exam tips
- **❓ Important Questions**: AI-predicted likely exam questions

### 🎨 Premium UI
- **Modern Dark Theme**: Beautiful gradient backgrounds with glassmorphism effects
- **Smooth Animations**: Engaging micro-interactions and transitions
- **Responsive Design**: Works seamlessly on desktop and mobile
- **Multiple Modes**: Chat, Exam, Study Planner tabs for different workflows

## 🏗️ Why Better Than ChatGPT?

✅ **Document-Aware**: Answers grounded in YOUR study materials, not generic Knowledge  
✅ **Exam-Focused**: Structured 16-mark answers, not generic explanations  
✅ **Personalized Study Plans**: Based on your exam date and topics  
✅ **All-in-One**: Quiz, flashcards, important questions in one place  
✅ **Progress Tracking**: Monitor topics covered and study time  
✅ **Hybrid Intelligence**: Combines your documents + web search  

## 📋 Prerequisites

- Python 3.11 or higher
- GROQ API Key (get from [console.groq.com](https://console.groq.com/keys))
- Tavily API Key (get from [tavily.com](https://tavily.com))

## 🚀 Installation & Setup

### 1. Install Dependencies

```bash
cd d:\LangGraph\src
uv sync
```

Or if you don't use `uv`:

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

Create a `.env` file in the `src` directory:

```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

**How to get API keys:**
- **GROQ**: Sign up at [console.groq.com](https://console.groq.com) → Go to API Keys → Create New Key
- **Tavily**: Sign up at [tavily.com](https://tavily.com) → Get API Key (free tier available)

### 3. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 Usage Guide

### Quick Start

1. **Upload Documents**
   - Click "Browse files" in the sidebar
   - Select your study materials (PDFs, TXT, MD files)
   - Click "📥 Process Documents"

2. **Ask Questions**
   - Type naturally in the chat: "Give me a 16-mark answer on Machine Learning"
   - The AI automatically routes to the right tool

3. **Explore Different Modes**
   - **💬 Chat**: Natural conversation with context from your docs
   - **📝 Exam Mode**: Generate timed practice tests
   - **📅 Study Planner**: Get personalized study schedules

### Example Questions

```
"Give me a 16-mark answer on Neural Networks"

"Create a 2-week study plan for my Physics exam"

"Generate a quiz with 10 questions on Data Structures"

"Explain gradient descent with examples"

"What are important questions for my exam on Algorithms?"

"Create flashcards from my uploaded notes on Chemistry"
```

## 🏗️ Architecture

```
┌─────────────┐
│   User      │
└──────┬──────┘
       │
       v
┌─────────────────────────┐
│   Streamlit UI          │
│   (app.py + styles.py)  │
└──────────┬──────────────┘
           │
           v
┌─────────────────────────┐
│  LangGraph Agent        │
│  (study_buddy_agent.py) │
└──────┬──────────────────┘
       │
       ├──> RAG Tool (ChromaDB + HuggingFace Embeddings)
       ├──> Web Search Tool (Tavily)
       ├──> Exam Answer Generator
       ├──> Study Plan Generator
       ├──> Quiz Generator
       ├──> Flashcard Creator
       └──> Concept Explainer
```

## 📁 Project Structure

```
d:\LangGraph\src\
├── app.py                      # Main Streamlit application
├── study_buddy_agent.py        # LangGraph agent with tool routing
├── document_processor.py       # Document upload & vector store management
├── exam_tools.py               # Specialized exam preparation tools
├── styles.py                   # Custom CSS for premium UI
├── .env                        # API keys (you create this)
├── .env.example                # Template for environment variables
├── pyproject.toml              # Dependencies
├── knowledge-base/             # Uploaded documents go here
└── chroma_db/                  # Vector database storage
```

## 🎨 UI Features

- **Dark Theme**: Modern gradient backgrounds (purple-blue-teal)
- **Glassmorphism**: Frosted glass effect on cards and panels
- **Smooth Animations**: Hover effects, slide-ins, and micro-interactions
- **Custom Components**: Styled metrics, buttons, chat messages
- **Responsive Layout**: Works on all screen sizes

## 🛠️ Technologies Used

- **LangGraph**: Agent orchestration and workflow
- **LangChain**: Document processing and RAG pipeline
- **GROQ (Llama 3.3 70B)**: Fast LLM inference
- **Tavily**: Web search API
- **ChromaDB**: Vector database for semantic search
- **HuggingFace Embeddings**: Document embeddings
- **Streamlit**: Web application framework

## 💡 Tips for Best Results

1. **Upload comprehensive materials** - More context = better answers
2. **Be specific in questions** - "16-mark answer on..." works better than generic questions
3. **Set accurate exam date** - For realistic study plans
4. **Use different tools** - Try quizzes, flashcards for variety
5. **Check sources** - Review which documents were used

## 🐛 Troubleshooting

**Agent won't initialize:**
- Check that your `.env` file exists with valid API keys
- Verify GROQ and Tavily keys are correct

**No documents found:**
- Make sure you clicked "📥 Process Documents" after uploading
- Check that files are PDF, TXT, or MD format

**Slow responses:**
- First query loads models (HuggingFace embeddings) - subsequent queries are faster
- Large documents take longer to process

**Import errors:**
- Run `uv sync` or `pip install -r requirements.txt`
- Ensure Python 3.11+ is installed

## 📝 License

This project is for educational purposes.

## 🙏 Acknowledgments

- Built with ❤️ using LangGraph and Streamlit
- Powered by GROQ's blazing-fast inference
- Search capabilities by Tavily

---

**Happy Studying! 🎓 Ace those exams! 🚀**
