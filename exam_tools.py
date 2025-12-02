"""
Exam-Focused Tools for AI Study Buddy
Specialized tools for exam preparation: 16-mark answers, study plans, quizzes, flashcards
"""

from typing import List, Dict, Optional
from datetime import datetime, timedelta
from langchain_groq import ChatGroq
from langchain_core.documents import Document
import json


class ExamTools:
    """Collection of exam preparation tools"""
    
    def __init__(self, llm_model: str = "llama-3.3-70b-versatile"):
        self.llm = ChatGroq(temperature=0.3, model_name=llm_model)
    
    def generate_16_mark_answer(self, question: str, context: str = "") -> Dict:
        """
        Generate a structured 16-mark answer
        Returns: dict with sections and formatted answer
        """
        prompt = f"""You are an expert exam preparation tutor. Generate a COMPREHENSIVE 16-mark answer for the following question.

QUESTION: {question}

CONTEXT FROM STUDY MATERIALS:
{context if context else "No specific context provided. Use general knowledge."}

STRUCTURE YOUR ANSWER AS FOLLOWS:

**INTRODUCTION** (2 marks):
- Brief overview of the topic
- Scope of the answer

**MAIN BODY** (10-12 marks):
Provide 4-5 major points, each worth 2-3 marks:
1. **Point 1**: [Detailed explanation with examples]
2. **Point 2**: [Detailed explanation with examples]
3. **Point 3**: [Detailed explanation with examples]
4. **Point 4**: [Detailed explanation with examples]
5. **Point 5** (if applicable): [Detailed explanation]

**EXAMPLES/CASE STUDIES** (2 marks):
- Real-world examples or case studies
- Relevant diagrams or flowcharts (describe them)

**CONCLUSION** (2 marks):
- Summary of key points
- Future implications or significance

IMPORTANT:
- Each point should be well-elaborated (3-4 sentences minimum)
- Include technical terms and definitions
- Cite specific facts, figures, or theories
- Make it comprehensive enough to earn full 16 marks
- Use proper formatting with headings and bullet points

Generate the answer now:"""

        response = self.llm.invoke(prompt)
        return {
            "question": question,
            "answer": response.content,
            "marks": 16,
            "generated_at": datetime.now().isoformat()
        }
    
    def generate_study_plan(self, topics: List[str], exam_date: str, hours_per_day: int = 3) -> Dict:
        """
        Generate a personalized study plan
        Args:
            topics: List of topics to cover
            exam_date: Exam date in YYYY-MM-DD format
            hours_per_day: Available study hours per day
        """
        # Smart date handling
        try:
            # Try to parse the provided date
            if not exam_date or "202" not in exam_date:  # Basic check for valid year
                raise ValueError("Invalid date")
            exam_datetime = datetime.fromisoformat(exam_date)
            days_available = (exam_datetime - datetime.now()).days
        except:
            # Default to 30 days from now if date is invalid or missing
            exam_datetime = datetime.now() + timedelta(days=30)
            days_available = 30
            exam_date = exam_datetime.strftime("%Y-%m-%d")
        
        # Ensure positive days
        if days_available < 1:
            days_available = 30
            exam_datetime = datetime.now() + timedelta(days=30)
            exam_date = exam_datetime.strftime("%Y-%m-%d")
        
        topics_str = "\n".join([f"- {topic}" for topic in topics])
        
        prompt = f"""You are an expert study planner. Create a DETAILED day-by-day study schedule.
        
        IMPORTANT: The exam is on {exam_date} ({days_available} days from now).
        
        INPUTS:
        - Topics to cover: 
        {topics_str}
        - Days until exam: {days_available} days
        - Study hours per day: {hours_per_day} hours
        
        CREATE A STUDY PLAN WITH:
        
        1. **Week-by-week breakdown**:
           - Divide topics strategically across weeks
           - Include revision cycles (20% of time)
           - Build in buffer days for unexpected delays
        
        2. **Daily schedule format**:
           ```
           DAY X (Date):
           - Morning (1.5 hrs): [Topic/Activity]
           - Evening (1.5 hrs): [Topic/Activity]
           - Quick revision: [Previous topics]
           ```
        
        3. **Milestones**:
           - Weekly targets
           - Mock exams/practice tests schedule
           - Final revision week plan
        
        4. **Study techniques**:
           - Recommend active recall, spaced repetition
           - Suggest breaks and rest days
        
        Generate a COMPLETE study plan now:"""
        
        response = self.llm.invoke(prompt)
        return {
            "topics": topics,
            "exam_date": exam_date,
            "days_available": days_available,
            "hours_per_day": hours_per_day,
            "plan": response.content,
            "generated_at": datetime.now().isoformat()
        }
    
    def generate_quiz(self, topic: str, num_questions: int = 5, difficulty: str = "medium", context: str = "") -> Dict:
        """
        Generate quiz questions
        Args:
            topic: Topic for quiz
            num_questions: Number of questions
            difficulty: easy, medium, or hard
            context: Context from documents
        """
        prompt = f"""Generate a quiz on the topic: {topic}

NUMBER OF QUESTIONS: {num_questions}
DIFFICULTY LEVEL: {difficulty}

CONTEXT FROM STUDY MATERIALS:
{context if context else "Use general knowledge on this topic."}

For each question, provide:

**MCQ Questions** (Format):
1. Question text
   A) Option A
   B) Option B
   C) Option C
   D) Option D
   
   **Correct Answer**: [Letter]
   **Explanation**: [Why this is correct and others are wrong]

Include a mix of:
- Conceptual understanding questions
- Application-based questions
- Fact-recall questions (for {difficulty} difficulty)

Generate {num_questions} high-quality questions now:"""

        response = self.llm.invoke(prompt)
        return {
            "topic": topic,
            "num_questions": num_questions,
            "difficulty": difficulty,
            "quiz": response.content,
            "generated_at": datetime.now().isoformat()
        }
    
    def generate_flashcards(self, topic: str, context: str = "", num_cards: int = 10) -> Dict:
        """Generate flashcards for a topic"""
        prompt = f"""Create {num_cards} flashcards for the topic: {topic}

CONTEXT FROM STUDY MATERIALS:
{context if context else "Use general knowledge on this topic."}

FORMAT each flashcard as:

**Card X:**
- **FRONT** (Question/Term): [Question or key term]
- **BACK** (Answer/Definition): [Concise answer or definition]
- **Hint**: [Memory aid or mnemonic]

GUIDELINES:
- Focus on key concepts, definitions, formulas
- Keep answers concise but complete
- Include memory aids where helpful
- Mix different types: definitions, processes, comparisons

Generate {num_cards} flashcards now:"""

        response = self.llm.invoke(prompt)
        return {
            "topic": topic,
            "num_cards": num_cards,
            "flashcards": response.content,
            "generated_at": datetime.now().isoformat()
        }
    
    def explain_concept(self, concept: str, context: str = "", difficulty: str = "medium") -> Dict:
        """Explain a concept in detail with examples"""
        prompt = f"""Explain the following concept in detail: {concept}

DIFFICULTY LEVEL: {difficulty}

CONTEXT FROM STUDY MATERIALS:
{context if context else "No specific context. Provide a comprehensive explanation."}

STRUCTURE YOUR EXPLANATION:

**1. SIMPLE DEFINITION** (ELI5):
[Explain like I'm 5 - simple, intuitive explanation]

**2. FORMAL DEFINITION**:
[Academic/technical definition]

**3. KEY COMPONENTS/ASPECTS**:
- Component 1: [Explanation]
- Component 2: [Explanation]
- Component 3: [Explanation]

**4. REAL-WORLD EXAMPLES**:
- Example 1: [Concrete example]
- Example 2: [Another example]

**5. COMMON MISCONCEPTIONS**:
- Misconception 1: [Clarification]
- Misconception 2: [Clarification]

**6. RELATED CONCEPTS**:
- How it connects to other topics

**7. EXAM TIP**:
[How this concept typically appears in exams]

Provide the explanation now:"""

        response = self.llm.invoke(prompt)
        return {
            "concept": concept,
            "difficulty": difficulty,
            "explanation": response.content,
            "generated_at": datetime.now().isoformat()
        }
    
    def generate_important_questions(self, topic: str, context: str = "", num_questions: int = 10) -> Dict:
        """Generate likely important exam questions"""
        prompt = f"""Based on the topic: {topic}

CONTEXT FROM STUDY MATERIALS:
{context}

Generate {num_questions} MOST IMPORTANT questions that are likely to appear in exams.

For each question, provide:

**Question X** ([Marks: 2/5/10/16]):
[Question text]

**Why This is Important**:
[Explain why this question is commonly asked]

**Key Points to Include in Answer**:
- Point 1
- Point 2
- Point 3

Include a variety of question types:
- Short answer (2-5 marks)
- Long answer (10-16 marks)
- Application-based questions
- Conceptual questions

Generate the questions now:"""

        response = self.llm.invoke(prompt)
        return {
            "topic": topic,
            "num_questions": num_questions,
            "questions": response.content,
            "generated_at": datetime.now().isoformat()
        }
