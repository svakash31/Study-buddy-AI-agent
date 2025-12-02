# 🎓 AI Study Buddy - Quick Setup Instructions

## Step 1: Add Your API Keys ⚙️

1. Open the file: `d:\LangGraph\src\.env.example`
2. You'll see:
   ```
   GROQ_API_KEY=
   TAVILY_API_KEY=
   ```
3. Add your actual API keys after the `=` sign
4. Save the file as `.env` (remove `.example`)

**Example:**
```env
GROQ_API_KEY=gsk_abc123xyz...
TAVILY_API_KEY=tvly-xyz789...
```

## Step 2: Install Dependencies 📦

Open your terminal in `d:\LangGraph\src\` and run:

```bash
uv sync
```

This will install all required packages.

## Step 3: Run the Application 🚀

In the same directory, run:

```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

## Step 4: Start Using! 🎉

1. **Upload Documents**: Click "Browse files" in sidebar → Select PDFs → Click "Process Documents"
2. **Ask Questions**: Type in chat: "Give me a 16-mark answer on [topic]"
3. **Explore Tabs**: Try Exam Mode and Study Planner tabs

## Quick Test Questions 🧪

Try these to see different features:

```
"Give me a 16-mark answer on Machine Learning"
"Create a study plan for my exam in 30 days"
"Generate a quiz on Python programming"
"Create flashcards from my notes"
"Explain neural networks with examples"
```

## Troubleshooting 🔧

**If you see "Failed to initialize agent":**
- Check that your API keys are correctly added to `.env`
- Make sure there are no extra spaces in the `.env` file

**If app won't start:**
- Make sure you're in the `d:\LangGraph\src\` directory
- Run `uv sync` again to ensure all packages are installed

---

**That's it! You're ready to ace your exams! 🎓**
