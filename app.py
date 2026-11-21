import streamlit as st
import random
import time
import json
import base64
from datetime import datetime

from database import (
    save_session,
    get_all_sessions,
    get_session_answers,
    get_stats,
    delete_session,
)

# -----------------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------------

st.set_page_config(
    page_title="AI Interview Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------
# THEME — CSS
# -----------------------------------------------------------

DARK_CSS = """
<style>
    .stApp {
        background-color: #0f172a;
        color: #e2e8f0;
    }
    .main-header {
        text-align: center;
        padding: 2rem 0 1rem 0;
    }
    .main-header h1 {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #60a5fa, #a78bfa, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.25rem;
    }
    .main-header p {
        color: #94a3b8;
        font-size: 1.1rem;
    }
    .card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .question-card {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        border: 1px solid #475569;
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
    }
    .question-card h2 {
        color: #60a5fa;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem;
    }
    .question-card h3 {
        color: #f1f5f9;
        font-size: 1.4rem;
        font-weight: 600;
        line-height: 1.4;
    }
    .feedback-card {
        background: linear-gradient(135deg, #064e3b, #065f46);
        border: 1px solid #10b981;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .feedback-card h3 {
        color: #6ee7b7;
    }
    .score-display {
        text-align: center;
        padding: 2rem;
    }
    .score-display h1 {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #60a5fa, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .score-display h2 {
        color: #94a3b8;
        font-size: 1.5rem;
    }
    .stat-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
    }
    .stat-card h3 {
        color: #60a5fa;
        font-size: 2rem;
        font-weight: 700;
    }
    .stat-card p {
        color: #94a3b8;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .timer {
        text-align: center;
        font-size: 1.5rem;
        font-weight: 700;
        color: #f59e0b;
        padding: 0.5rem;
    }
    .timer.warning {
        color: #ef4444;
    }
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        padding: 0.6rem 1.5rem;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    .sidebar .stSelectbox>div>div {
        background-color: #1e293b;
    }
    .progress-container {
        margin: 1rem 0;
    }
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .badge-easy { background-color: #064e3b; color: #6ee7b7; }
    .badge-medium { background-color: #78350f; color: #fcd34d; }
    .badge-hard { background-color: #7f1d1d; color: #fca5a5; }
    .history-item {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.5rem;
    }
    .stTextArea>div>textarea {
        background-color: #1e293b;
        border: 1px solid #475569;
        border-radius: 10px;
        color: #e2e8f0;
    }
    .stTextInput>div>input {
        background-color: #1e293b;
        border: 1px solid #475569;
        border-radius: 10px;
        color: #e2e8f0;
    }
</style>
"""

LIGHT_CSS = """
<style>
    .stApp {
        background-color: #f8fafc;
        color: #1e293b;
    }
    .main-header {
        text-align: center;
        padding: 2rem 0 1rem 0;
    }
    .main-header h1 {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #2563eb, #7c3aed, #db2777);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.25rem;
    }
    .main-header p {
        color: #64748b;
        font-size: 1.1rem;
    }
    .card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .question-card {
        background: linear-gradient(135deg, #ffffff, #f1f5f9);
        border: 1px solid #cbd5e1;
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
    }
    .question-card h2 {
        color: #2563eb;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem;
    }
    .question-card h3 {
        color: #0f172a;
        font-size: 1.4rem;
        font-weight: 600;
        line-height: 1.4;
    }
    .feedback-card {
        background: linear-gradient(135deg, #ecfdf5, #d1fae5);
        border: 1px solid #6ee7b7;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .feedback-card h3 {
        color: #059669;
    }
    .score-display {
        text-align: center;
        padding: 2rem;
    }
    .score-display h1 {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #2563eb, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .score-display h2 {
        color: #64748b;
        font-size: 1.5rem;
    }
    .stat-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .stat-card h3 {
        color: #2563eb;
        font-size: 2rem;
        font-weight: 700;
    }
    .stat-card p {
        color: #64748b;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .timer {
        text-align: center;
        font-size: 1.5rem;
        font-weight: 700;
        color: #d97706;
        padding: 0.5rem;
    }
    .timer.warning {
        color: #dc2626;
    }
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        padding: 0.6rem 1.5rem;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .progress-container {
        margin: 1rem 0;
    }
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .badge-easy { background-color: #d1fae5; color: #059669; }
    .badge-medium { background-color: #fef3c7; color: #d97706; }
    .badge-hard { background-color: #fee2e2; color: #dc2626; }
    .history-item {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.5rem;
    }
</style>
"""

# -----------------------------------------------------------
# QUESTION BANK
# -----------------------------------------------------------

QUESTIONS = {
    "General Interview": {
        "easy": [
            "Tell me about yourself.",
            "What are your strengths?",
            "What are your weaknesses?",
            "Why should we hire you?",
            "Where do you see yourself in five years?",
            "What motivates you?",
            "How do you handle pressure?",
            "What is your greatest achievement?",
            "Describe your ideal work environment.",
            "How do you manage your time?",
        ],
        "medium": [
            "Why do you want to join our company?",
            "Tell me about a difficult problem you solved.",
            "How do you handle conflict in the workplace?",
            "Describe a time you failed and what you learned.",
            "How do you prioritize tasks when everything is urgent?",
            "Tell me about a time you had to learn something quickly.",
            "Describe a situation where you showed leadership.",
            "How do you handle constructive criticism?",
            "Tell me about a time you went above and beyond.",
            "How do you build relationships with coworkers?",
        ],
        "hard": [
            "Describe a time you had to influence without authority.",
            "Tell me about a decision you made that was unpopular.",
            "How would you handle a situation where you disagree with your manager?",
            "Describe a time you had to manage a project with limited resources.",
            "How do you approach mentoring junior team members?",
            "Tell me about a time you had to pivot strategy mid-project.",
            "How do you balance innovation with risk management?",
            "Describe a situation where you had to deliver bad news to a stakeholder.",
        ],
    },
    "Python": {
        "easy": [
            "What is Python?",
            "What is the difference between a list and a tuple?",
            "What is a dictionary in Python?",
            "What is a function?",
            "What is a virtual environment?",
            "What is the difference between == and is?",
            "What is a lambda function?",
            "What is exception handling?",
            "What is a module in Python?",
            "What is PEP 8?",
        ],
        "medium": [
            "Explain inheritance in Python.",
            "What is object-oriented programming?",
            "What are decorators in Python?",
            "Explain the difference between shallow copy and deep copy.",
            "What are generators in Python?",
            "Explain the GIL in Python.",
            "What is the difference between append and extend?",
            "How does garbage collection work in Python?",
            "What are *args and **kwargs?",
            "Explain the difference between a class method and a static method.",
        ],
        "hard": [
            "Explain the Python descriptor protocol.",
            "How does the Python memory manager work?",
            "What is the difference between __new__ and __init__?",
            "Explain metaclasses in Python.",
            "How would you implement a thread-safe singleton in Python?",
            "Explain the difference between asyncio and threading.",
            "How does Python's import system work internally?",
            "What is the difference between __str__ and __repr__?",
            "Explain how you would profile and optimize a slow Python application.",
            "What are context managers and how would you implement one from scratch?",
        ],
    },
    "Data Science": {
        "easy": [
            "What is machine learning?",
            "What is supervised learning?",
            "What is unsupervised learning?",
            "What is a confusion matrix?",
            "What is precision?",
            "What is recall?",
            "What is a database?",
            "What is SQL?",
            "What is feature engineering?",
            "What is cross-validation?",
        ],
        "medium": [
            "What is overfitting?",
            "What is underfitting?",
            "What is the bias-variance tradeoff?",
            "Explain the difference between bagging and boosting.",
            "What is regularization?",
            "How do you handle missing data?",
            "What is the difference between L1 and L2 regularization?",
            "Explain the ROC curve and AUC.",
            "What is the curse of dimensionality?",
            "How do you evaluate a regression model?",
        ],
        "hard": [
            "Explain the math behind gradient descent.",
            "How does XGBoost differ from standard gradient boosting?",
            "What is the difference between a generative and discriminative model?",
            "Explain the attention mechanism in transformers.",
            "How would you design an A/B test for a recommendation system?",
            "What is the difference between MAP and MRR?",
            "Explain how you would handle class imbalance in a classification problem.",
            "What is the difference between batch gradient descent and stochastic gradient descent?",
            "Explain the EM algorithm.",
            "How does a variational autoencoder work?",
        ],
    },
    "Web Development": {
        "easy": [
            "What is HTML?",
            "What is CSS?",
            "What is JavaScript?",
            "What is frontend development?",
            "What is backend development?",
            "What is an API?",
            "What is responsive web design?",
            "What is a database?",
            "What is SQL?",
            "What is a web server?",
        ],
        "medium": [
            "What is REST API?",
            "Explain the difference between GET and POST.",
            "What is CORS?",
            "What is the difference between localStorage and sessionStorage?",
            "Explain the box model in CSS.",
            "What is the virtual DOM?",
            "What is the difference between let, const, and var?",
            "What is a promise in JavaScript?",
            "What is the difference between SQL and NoSQL databases?",
            "Explain the concept of middleware in web frameworks.",
        ],
        "hard": [
            "How does the browser rendering engine work?",
            "Explain the event loop in JavaScript.",
            "What is the difference between SSR and CSR?",
            "How would you optimize a web application for performance?",
            "Explain the concept of microservices architecture.",
            "What is the difference between OAuth and JWT?",
            "How does HTTPS work?",
            "Explain the concept of serverless architecture.",
            "What is the difference between a monolith and microservices?",
            "How would you design a URL shortening service?",
        ],
    },
    "HR Interview": {
        "easy": [
            "Tell me about yourself.",
            "Why do you want this job?",
            "What are your career goals?",
            "What are your strengths?",
            "What are your weaknesses?",
            "How do you handle criticism?",
            "Do you have any questions for us?",
            "What is your expected salary?",
            "Are you willing to relocate?",
            "How did you hear about this position?",
        ],
        "medium": [
            "How do you handle conflicts?",
            "Tell me about your biggest achievement.",
            "Tell me about a failure and what you learned.",
            "Describe your leadership style.",
            "How do you handle stress?",
            "What is your approach to teamwork?",
            "Describe a time you had to deal with a difficult coworker.",
            "How do you handle multiple deadlines?",
            "What are your salary expectations?",
            "Why are you leaving your current job?",
        ],
        "hard": [
            "Describe a time you had to fire someone or give difficult feedback.",
            "How would you handle a situation where your team is underperforming?",
            "Tell me about a time you had to manage a conflict between two senior team members.",
            "How do you approach building a team culture?",
            "Describe a time you had to make a decision with incomplete information.",
            "How do you handle a situation where you don't know the answer?",
            "Tell me about a time you had to push back on a request from leadership.",
            "How do you measure success in your role?",
            "Describe a time you had to manage a remote team.",
            "How do you stay current with industry trends?",
        ],
    },
    "System Design": {
        "easy": [
            "What is a load balancer?",
            "What is caching?",
            "What is a CDN?",
            "What is the difference between horizontal and vertical scaling?",
            "What is a message queue?",
            "What is the CAP theorem?",
            "What is database indexing?",
            "What is the difference between TCP and UDP?",
            "What is DNS?",
            "What is a reverse proxy?",
        ],
        "medium": [
            "How would you design a URL shortener?",
            "How would you design a chat application?",
            "How would you design a rate limiter?",
            "How would you design a notification system?",
            "How would you design a search autocomplete system?",
            "How would you design a file storage system like Dropbox?",
            "How would you design a web crawler?",
            "How would you design a social media feed?",
            "How would you design a ride-sharing app?",
            "How would you design a video streaming platform?",
        ],
        "hard": [
            "How would you design a distributed cache?",
            "How would you design a system to handle millions of concurrent connections?",
            "How would you design a globally distributed database?",
            "How would you design a real-time collaborative editing system?",
            "How would you design a fraud detection system?",
            "How would you design a recommendation system for a large e-commerce platform?",
            "How would you design a payment processing system?",
            "How would you design a system to handle flash sales?",
            "How would you design a distributed task scheduler?",
            "How would you design a system to detect and prevent DDoS attacks?",
        ],
    },
}

# -----------------------------------------------------------
# KEYWORDS FOR SMART EVALUATION
#-----------------------------------------------------------

CATEGORY_KEYWORDS = {
    "Python": [
        "python", "list", "tuple", "dictionary", "function", "class", "object",
        "inheritance", "decorator", "generator", "lambda", "module", "package",
        "exception", "error", "loop", "variable", "string", "integer", "float",
        "boolean", "none", "true", "false", "import", "pep", "gil", "async",
        "thread", "memory", "garbage", "copy", "append", "extend", "args",
        "kwargs", "method", "static", "descriptor", "metaclass", "context",
    ],
    "Data Science": [
        "machine", "learning", "supervised", "unsupervised", "model", "data",
        "training", "testing", "validation", "feature", "label", "classification",
        "regression", "clustering", "overfitting", "underfitting", "bias",
        "variance", "precision", "recall", "accuracy", "f1", "roc", "auc",
        "confusion", "matrix", "cross", "validation", "regularization", "l1",
        "l2", "gradient", "descent", "boosting", "bagging", "random", "forest",
        "neural", "network", "deep", "learning", "dimensionality", "pca",
    ],
    "Web Development": [
        "html", "css", "javascript", "frontend", "backend", "api", "rest",
        "http", "https", "server", "client", "database", "sql", "nosql",
        "responsive", "dom", "browser", "cache", "cookie", "session",
        "authentication", "authorization", "oauth", "jwt", "cors", "cdn",
        "load", "balancer", "microservice", "monolith", "middleware", "route",
        "endpoint", "json", "xml", "websocket", "graphql",
    ],
    "General Interview": [
        "team", "leadership", "communication", "problem", "solution", "experience",
        "skill", "goal", "motivation", "strength", "weakness", "challenge",
        "success", "failure", "learn", "improve", "collaboration", "adapt",
        "time", "manage", "priority", "pressure", "conflict", "feedback",
    ],
    "HR Interview": [
        "team", "leadership", "communication", "problem", "solution", "experience",
        "skill", "goal", "motivation", "strength", "weakness", "challenge",
        "success", "failure", "learn", "improve", "collaboration", "adapt",
        "time", "manage", "priority", "pressure", "conflict", "feedback",
        "salary", "expectation", "culture", "value", "growth", "development",
    ],
    "System Design": [
        "scalability", "availability", "reliability", "latency", "throughput",
        "load", "balancer", "cache", "database", "replication", "sharding",
        "partition", "consistency", "partition", "cap", "theorem", "message",
        "queue", "microservice", "monolith", "cdn", "dns", "proxy", "tcp",
        "udp", "http", "websocket", "distributed", "system", "architecture",
    ],
}

# -----------------------------------------------------------
# SESSION STATE INIT
# -----------------------------------------------------------

defaults = {
    "page": "home",
    "started": False,
    "questions": [],
    "current_question": 0,
    "submitted": False,
    "current_answer": "",
    "scores": [],
    "feedback_list": [],
    "answers": [],
    "question_times": [],
    "finished": False,
    "start_time": None,
    "question_start_time": None,
    "category": "General Interview",
    "difficulty": "easy",
    "number_of_questions": 5,
    "theme": "dark",
    "timer_enabled": True,
    "time_limit": 120,
}

for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# -----------------------------------------------------------
# FUNCTIONS
#-----------------------------------------------------------

def get_difficulty_badge(difficulty):
    cls = f"badge-{difficulty}"
    label = difficulty.capitalize()
    return f'<span class="badge {cls}">{label}</span>'


def evaluate_answer(answer, category):
    """Smart evaluation based on length, keywords, and structure."""
    answer = answer.strip()
    words = answer.split()
    word_count = len(words)

    # Base score from length
    if word_count >= 100:
        base_score = 9
    elif word_count >= 70:
        base_score = 8
    elif word_count >= 50:
        base_score = 7
    elif word_count >= 30:
        base_score = 6
    elif word_count >= 15:
        base_score = 5
    elif word_count >= 5:
        base_score = 3
    else:
        base_score = 1

    # Keyword bonus
    keywords = CATEGORY_KEYWORDS.get(category, [])
    answer_lower = answer.lower()
    keyword_matches = sum(1 for kw in keywords if kw in answer_lower)
    keyword_bonus = min(keyword_matches * 0.3, 1.5)

    # Structure bonus (sentences, examples)
    sentence_count = answer.count(". ") + answer.count("! ") + answer.count("? ") + 1
    structure_bonus = 0
    if sentence_count >= 3:
        structure_bonus += 0.3
    if "example" in answer_lower or "for instance" in answer_lower or "such as" in answer_lower:
        structure_bonus += 0.3
    if "because" in answer_lower or "therefore" in answer_lower or "however" in answer_lower:
        structure_bonus += 0.2
    if "i " in answer_lower or "my " in answer_lower or "me " in answer_lower:
        structure_bonus += 0.2

    # First-person bonus (interview answers should be personal)
    first_person = sum(1 for w in ["i", "my", "me", "myself"] if w in answer_lower.split())
    if first_person >= 3:
        structure_bonus += 0.3

    raw_score = base_score + keyword_bonus + structure_bonus
    score = min(int(round(raw_score)), 10)
    score = max(score, 1)

    # Generate feedback
    feedback_parts = []

    if word_count < 20:
        feedback_parts.append("Your answer is quite short. Aim for at least 3-5 sentences.")
    elif word_count < 50:
        feedback_parts.append("Good length, but you could elaborate more with specific details.")
    else:
        feedback_parts.append("Great length and detail in your answer.")

    if keyword_matches >= 3:
        feedback_parts.append(f"Excellent use of relevant terminology ({keyword_matches} keywords found).")
    elif keyword_matches >= 1:
        feedback_parts.append("Good use of some relevant terms. Try to incorporate more specific vocabulary.")
    else:
        feedback_parts.append("Try to include more relevant technical terms and keywords.")

    if "example" in answer_lower or "for instance" in answer_lower or "such as" in answer_lower:
        feedback_parts.append("Nice inclusion of examples — this strengthens your answer.")
    else:
        feedback_parts.append("Consider adding a specific example to illustrate your point.")

    if "i " in answer_lower or "my " in answer_lower:
        feedback_parts.append("Good use of personal experience.")
    else:
        feedback_parts.append("Try to personalize your answer with your own experiences.")

    if score >= 8:
        feedback_parts.append("Overall, this is a strong answer. Keep up the great work!")
    elif score >= 6:
        feedback_parts.append("This is a solid answer. With a bit more detail and structure, it could be excellent.")
    elif score >= 4:
        feedback_parts.append("Your answer has potential but needs more depth and structure.")
    else:
        feedback_parts.append("Focus on providing more detailed, structured answers with specific examples.")

    feedback = " ".join(feedback_parts)
    return score, feedback


def start_interview():
    category = st.session_state.category
    difficulty = st.session_state.difficulty
    num = st.session_state.number_of_questions

    questions = QUESTIONS[category][difficulty].copy()
    random.shuffle(questions)
    st.session_state.questions = questions[:num]
    st.session_state.current_question = 0
    st.session_state.started = True
    st.session_state.submitted = False
    st.session_state.finished = False
    st.session_state.scores = []
    st.session_state.feedback_list = []
    st.session_state.answers = []
    st.session_state.question_times = []
    st.session_state.current_answer = ""
    st.session_state.start_time = time.time()
    st.session_state.question_start_time = time.time()
    st.session_state.page = "interview"
    st.rerun()


def reset_interview():
    st.session_state.started = False
    st.session_state.questions = []
    st.session_state.current_question = 0
    st.session_state.submitted = False
    st.session_state.current_answer = ""
    st.session_state.scores = []
    st.session_state.feedback_list = []
    st.session_state.answers = []
    st.session_state.question_times = []
    st.session_state.finished = False
    st.session_state.start_time = None
    st.session_state.question_start_time = None
    st.session_state.page = "home"
    st.rerun()


def next_question():
    elapsed = int(time.time() - st.session_state.question_start_time)
    st.session_state.question_times.append(elapsed)
    st.session_state.current_question += 1
    st.session_state.submitted = False
    st.session_state.current_answer = ""
    st.session_state.question_start_time = time.time()
    st.rerun()


def finish_interview():
    elapsed = int(time.time() - st.session_state.question_start_time)
    st.session_state.question_times.append(elapsed)
    st.session_state.finished = True
    st.session_state.page = "results"

    # Save to database
    total_time = int(time.time() - st.session_state.start_time)
    total_score = sum(st.session_state.scores)
    max_score = len(st.session_state.scores) * 10
    percentage = (total_score / max_score) * 100 if max_score > 0 else 0

    qa_list = []
    for i in range(len(st.session_state.questions)):
        qa_list.append({
            "number": i + 1,
            "question": st.session_state.questions[i],
            "answer": st.session_state.answers[i],
            "score": st.session_state.scores[i],
            "feedback": st.session_state.feedback_list[i],
            "time_taken": st.session_state.question_times[i] if i < len(st.session_state.question_times) else 0,
        })

    save_session(
        category=st.session_state.category,
        difficulty=st.session_state.difficulty,
        total_questions=len(st.session_state.questions),
        total_score=total_score,
        max_score=max_score,
        percentage=percentage,
        time_taken=total_time,
        qa_list=qa_list,
    )
    st.rerun()


def format_time(seconds):
    m, s = divmod(seconds, 60)
    return f"{m}:{s:02d}"


def get_score_color(score):
    if score >= 8:
        return "#10b981"
    elif score >= 6:
        return "#f59e0b"
    elif score >= 4:
        return "#f97316"
    else:
        return "#ef4444"


def get_performance_message(percentage):
    if percentage >= 90:
        return "Outstanding! You're interview-ready!"
    elif percentage >= 80:
        return "Excellent performance! Keep it up!"
    elif percentage >= 70:
        return "Great job! You're on the right track."
    elif percentage >= 60:
        return "Good performance. Keep practicing!"
    elif percentage >= 50:
        return "Not bad! Focus on more detailed answers."
    elif percentage >= 40:
        return "You have a good starting point. Keep practicing!"
    else:
        return "Keep practicing! You'll improve with time."


# -----------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------

with st.sidebar:
    st.markdown("## ⚙️ Settings")

    # Theme toggle
    theme = st.selectbox("🎨 Theme", ["dark", "light"], index=0 if st.session_state.theme == "dark" else 1)
    if theme != st.session_state.theme:
        st.session_state.theme = theme
        st.rerun()

    st.divider()

    # Navigation
    page_options = ["Home", "Interview", "History", "Statistics"]
    page_keys = ["home", "interview", "history", "statistics"]
    current_page = st.session_state.page if st.session_state.page in page_keys else "home"
    page = st.radio(
        "📄 Page",
        page_options,
        index=page_keys.index(current_page),
        label_visibility="collapsed",
    )
    page_map = {"Home": "home", "Interview": "interview", "History": "history", "Statistics": "statistics"}
    if page_map[page] != st.session_state.page:
        st.session_state.page = page_map[page]
        st.rerun()

    st.divider()

    if st.session_state.page == "home":
        st.markdown("### 🎯 Interview Setup")

        st.session_state.category = st.selectbox(
            "Category",
            list(QUESTIONS.keys()),
            index=list(QUESTIONS.keys()).index(st.session_state.category),
        )

        st.session_state.difficulty = st.selectbox(
            "Difficulty",
            ["easy", "medium", "hard"],
            index=["easy", "medium", "hard"].index(st.session_state.difficulty),
        )

        st.session_state.number_of_questions = st.slider(
            "Questions",
            3,
            10,
            st.session_state.number_of_questions,
        )

        st.session_state.timer_enabled = st.checkbox("Enable Timer", value=st.session_state.timer_enabled)

        if st.session_state.timer_enabled:
            st.session_state.time_limit = st.slider(
                "Time per question (seconds)",
                30,
                300,
                st.session_state.time_limit,
                step=30,
            )

        st.divider()

        if st.button("🚀 Start Interview", type="primary", use_container_width=True):
            start_interview()

    if st.session_state.page == "interview" and st.session_state.started:
        st.divider()
        if st.button("🔄 Restart", use_container_width=True):
            reset_interview()

    if st.session_state.page == "history":
        st.divider()
        if st.button("🗑️ Clear All History", use_container_width=True):
            sessions = get_all_sessions()
            for s in sessions:
                delete_session(s["id"])
            st.success("History cleared!")
            st.rerun()

# -----------------------------------------------------------
# APPLY THEME
# -----------------------------------------------------------

if st.session_state.theme == "dark":
    st.markdown(DARK_CSS, unsafe_allow_html=True)
else:
    st.markdown(LIGHT_CSS, unsafe_allow_html=True)

# -----------------------------------------------------------
# HEADER
# -----------------------------------------------------------

st.markdown(
    '<div class="main-header"><h1>🤖 AI Interview Chatbot</h1>'
    '<p>Practice interviews with AI-powered feedback</p></div>',
    unsafe_allow_html=True,
)

# -----------------------------------------------------------
# PAGE: HOME
# -----------------------------------------------------------

if st.session_state.page == "home":
    col1, col2, col3 = st.columns(3)

    stats = get_stats()

    with col1:
        st.markdown(
            f'<div class="stat-card"><h3>{stats["total_sessions"]}</h3>'
            '<p>Total Sessions</p></div>',
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f'<div class="stat-card"><h3>{stats["avg_percentage"]}%</h3>'
            '<p>Avg Score</p></div>',
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f'<div class="stat-card"><h3>{len(QUESTIONS)}</h3>'
            '<p>Categories</p></div>',
            unsafe_allow_html=True,
        )

    st.markdown("")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 👋 Welcome!")
    st.markdown(
        """
        This AI-powered interview chatbot helps you practice answering interview questions
        with instant feedback and scoring.

        **How it works:**
        1. Choose a category and difficulty level
        2. Answer each question as you would in a real interview
        3. Get instant AI feedback and a score out of 10
        4. Review your performance at the end

        **Tips for best results:**
        - Speak naturally and be specific
        - Use the STAR method (Situation, Task, Action, Result)
        - Include relevant keywords and examples
        - Aim for 3-5 sentences per answer
        """
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # Category overview
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 📚 Available Categories")
    cat_cols = st.columns(3)
    for i, (cat, diffs) in enumerate(QUESTIONS.items()):
        with cat_cols[i % 3]:
            total_q = sum(len(qs) for qs in diffs.values())
            st.markdown(f"**{cat}**")
            st.caption(f"{total_q} questions across {len(diffs)} difficulty levels")
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------
# PAGE: INTERVIEW
# -----------------------------------------------------------

elif st.session_state.page == "interview":
    if not st.session_state.started:
        st.info("👈 Configure your interview in the sidebar and click **Start Interview**!")
    elif not st.session_state.finished:
        current = st.session_state.current_question
        total = len(st.session_state.questions)

        # Progress bar
        progress = (current + 1) / total
        st.progress(progress)
        st.caption(f"Question {current + 1} of {total}")

        # Timer
        if st.session_state.timer_enabled and st.session_state.question_start_time:
            elapsed = int(time.time() - st.session_state.question_start_time)
            remaining = max(0, st.session_state.time_limit - elapsed)
            timer_class = "timer warning" if remaining <= 15 else "timer"
            st.markdown(
                f'<div class="{timer_class}">⏱️ {format_time(remaining)}</div>',
                unsafe_allow_html=True,
            )

        # Question card
        question = st.session_state.questions[current]
        st.markdown(
            f'<div class="question-card"><h2>🎤 Interviewer</h2>'
            f'<h3>{question}</h3></div>',
            unsafe_allow_html=True,
        )

        # Answer section
        if not st.session_state.submitted:
            answer = st.text_area(
                "✍️ Your Answer",
                height=180,
                placeholder="Type your answer here... Be specific and include examples.",
                key=f"answer_{current}",
            )

            col1, col2 = st.columns([1, 3])
            with col1:
                if st.button("✅ Submit Answer", type="primary", use_container_width=True):
                    if not answer.strip():
                        st.error("Please type an answer before submitting.")
                    else:
                        score, feedback = evaluate_answer(answer, st.session_state.category)
                        st.session_state.current_answer = answer
                        st.session_state.answers.append(answer)
                        st.session_state.scores.append(score)
                        st.session_state.feedback_list.append(feedback)
                        st.session_state.submitted = True
                        st.rerun()

        else:
            # Show answer and feedback
            st.markdown("### 📝 Your Answer")
            st.info(st.session_state.current_answer)

            score = st.session_state.scores[-1]
            feedback = st.session_state.feedback_list[-1]
            score_color = get_score_color(score)

            st.markdown(
                f'<div class="feedback-card">'
                f'<h3>🤖 AI Feedback</h3>'
                f'<p>{feedback}</p>'
                f'<h2 style="color: {score_color};">⭐ Score: {score}/10</h2>'
                f'</div>',
                unsafe_allow_html=True,
            )

            st.markdown("")

            if current + 1 < total:
                if st.button("➡️ Next Question", type="primary", use_container_width=True):
                    next_question()
            else:
                if st.button("🏆 Finish Interview", type="primary", use_container_width=True):
                    finish_interview()

# -----------------------------------------------------------
# PAGE: RESULTS
# -----------------------------------------------------------

elif st.session_state.page == "results" and st.session_state.finished:
    scores = st.session_state.scores
    total_score = sum(scores)
    max_score = len(scores) * 10
    percentage = (total_score / max_score) * 100 if max_score > 0 else 0
    total_time = int(time.time() - st.session_state.start_time) if st.session_state.start_time else 0

    # Score display
    st.markdown(
        f'<div class="score-display">'
        f'<h1>{percentage:.0f}%</h1>'
        f'<h2>{total_score} / {max_score} points</h2>'
        f'<p>⏱️ Total time: {format_time(total_time)}</p>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Performance message
    msg = get_performance_message(percentage)
    if percentage >= 80:
        st.success(f"🎉 {msg}")
    elif percentage >= 60:
        st.info(f"💪 {msg}")
    else:
        st.warning(f"📈 {msg}")

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📊 Score Breakdown")
        chart_data = {
            "Question": [f"Q{i+1}" for i in range(len(scores))],
            "Score": scores,
        }
        st.bar_chart(chart_data.set_index("Question"))
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📈 Performance Metrics")
        avg_score = total_score / len(scores) if scores else 0
        best_score = max(scores) if scores else 0
        worst_score = min(scores) if scores else 0

        mcol1, mcol2, mcol3 = st.columns(3)
        with mcol1:
            st.metric("Average", f"{avg_score:.1f}")
        with mcol2:
            st.metric("Best", f"{best_score}")
        with mcol3:
            st.metric("Worst", f"{worst_score}")

        st.markdown("")
        st.metric("Questions Answered", f"{len(scores)}")
        st.metric("Avg Time per Question", f"{format_time(total_time // len(scores)) if scores else '0:00'}")
        st.markdown("</div>", unsafe_allow_html=True)

    # Detailed review
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 📋 Detailed Review")

    for i in range(len(st.session_state.questions)):
        score = st.session_state.scores[i]
        score_color = get_score_color(score)
        with st.expander(f"**Q{i+1}:** {st.session_state.questions[i]} — **{score}/10**"):
            st.markdown(f'<span style="color:{score_color};font-weight:700;">Score: {score}/10</span>', unsafe_allow_html=True)
            st.markdown("**Your Answer:**")
            st.write(st.session_state.answers[i])
            st.markdown("**AI Feedback:**")
            st.write(st.session_state.feedback_list[i])
            if i < len(st.session_state.question_times):
                st.caption(f"Time taken: {format_time(st.session_state.question_times[i])}")

    st.markdown("</div>", unsafe_allow_html=True)

    # Export
    st.markdown("### 📤 Export Results")
    export_data = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "category": st.session_state.category,
        "difficulty": st.session_state.difficulty,
        "total_score": total_score,
        "max_score": max_score,
        "percentage": round(percentage, 1),
        "time_taken": format_time(total_time),
        "questions": [],
    }
    for i in range(len(st.session_state.questions)):
        export_data["questions"].append({
            "number": i + 1,
            "question": st.session_state.questions[i],
            "answer": st.session_state.answers[i],
            "score": st.session_state.scores[i],
            "feedback": st.session_state.feedback_list[i],
        })

    json_str = json.dumps(export_data, indent=2)
    b64 = base64.b64encode(json_str.encode()).decode()
    href = f'<a href="data:application/json;base64,{b64}" download="interview_results.json">📥 Download JSON</a>'
    st.markdown(href, unsafe_allow_html=True)

    st.markdown("")

    if st.button("🔄 Start New Interview", type="primary", use_container_width=True):
        reset_interview()

# -----------------------------------------------------------
# PAGE: HISTORY
# -----------------------------------------------------------

elif st.session_state.page == "history":
    st.markdown("## 📜 Interview History")

    sessions = get_all_sessions()

    if not sessions:
        st.info("No interview history yet. Complete an interview to see your history!")
    else:
        for s in sessions:
            col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
            with col1:
                st.markdown(f"**{s['category']}** {get_difficulty_badge(s['difficulty'])}")
                st.caption(f"📅 {s['created_at']}")
            with col2:
                st.metric("Score", f"{s['total_score']}/{s['max_score']}")
            with col3:
                st.metric("Percentage", f"{s['percentage']:.0f}%")
            with col4:
                st.metric("Questions", s['total_questions'])
            with col5:
                st.metric("Time", format_time(s['time_taken']))

            with st.expander("View Details"):
                answers = get_session_answers(s["id"])
                for a in answers:
                    st.markdown(f"**Q{a['question_number']}: {a['question']}**")
                    st.caption(f"Score: {a['score']}/10 | Time: {format_time(a['time_taken'])}")
                    st.write(f"**Answer:** {a['answer']}")
                    st.write(f"**Feedback:** {a['feedback']}")
                    st.divider()

            if st.button(f"🗑️ Delete", key=f"del_{s['id']}"):
                delete_session(s["id"])
                st.rerun()

            st.markdown("---")

# -----------------------------------------------------------
# PAGE: STATISTICS
# -----------------------------------------------------------

elif st.session_state.page == "statistics":
    st.markdown("## 📊 Statistics Dashboard")

    stats = get_stats()

    if stats["total_sessions"] == 0:
        st.info("No data yet. Complete some interviews to see statistics!")
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(
                f'<div class="stat-card"><h3>{stats["total_sessions"]}</h3>'
                '<p>Total Sessions</p></div>',
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                f'<div class="stat-card"><h3>{stats["avg_percentage"]}%</h3>'
                '<p>Average Score</p></div>',
                unsafe_allow_html=True,
            )
        with col3:
            st.markdown(
                f'<div class="stat-card"><h3>{stats["avg_ratio"]:.0%}</h3>'
                '<p>Success Rate</p></div>',
                unsafe_allow_html=True,
            )

        st.markdown("")

        # Category breakdown
        sessions = get_all_sessions()
        if sessions:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 📚 Performance by Category")

            cat_stats = {}
            for s in sessions:
                cat = s["category"]
                if cat not in cat_stats:
                    cat_stats[cat] = {"total": 0, "count": 0, "scores": []}
                cat_stats[cat]["total"] += s["percentage"]
                cat_stats[cat]["count"] += 1
                cat_stats[cat]["scores"].append(s["percentage"])

            for cat, data in cat_stats.items():
                avg = data["total"] / data["count"]
                st.markdown(f"**{cat}** — {data['count']} sessions, avg: {avg:.0f}%")
                st.progress(min(avg / 100, 1.0))

            st.markdown("</div>", unsafe_allow_html=True)

            # Difficulty breakdown
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 🎯 Performance by Difficulty")

            diff_stats = {}
            for s in sessions:
                diff = s["difficulty"]
                if diff not in diff_stats:
                    diff_stats[diff] = {"total": 0, "count": 0}
                diff_stats[diff]["total"] += s["percentage"]
                diff_stats[diff]["count"] += 1

            for diff, data in diff_stats.items():
                avg = data["total"] / data["count"]
                st.markdown(f"**{diff.capitalize()}** — {data['count']} sessions, avg: {avg:.0f}%")
                st.progress(min(avg / 100, 1.0))

            st.markdown("</div>", unsafe_allow_html=True)

            # Recent trend
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 📈 Recent Performance Trend")

            recent = sessions[:10]
            trend_data = {
                "Session": [f"#{s['id']}" for s in recent],
                "Score": [s["percentage"] for s in recent],
            }
            st.line_chart(trend_data.set_index("Session"))

            st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------
# FOOTER
# -----------------------------------------------------------

st.divider()
st.caption("🤖 AI Interview Chatbot | Built with Streamlit | Practice makes perfect!")

# -----------------------------------------------------------
# PRINT URL & OPEN BROWSER
# -----------------------------------------------------------

def _print_url_and_open_browser():
    import os
    # Streamlit reruns this script on every interaction — only print/open once.
    if os.environ.get("_AIC_BANNER_SHOWN"):
        return
    os.environ["_AIC_BANNER_SHOWN"] = "1"

    import threading
    import webbrowser
    import sys

    # Windows consoles (cp1252) can't encode emoji — force UTF-8 output.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    url = "http://localhost:8502"
    print("\n" + "=" * 60)
    print("  🤖 AI Interview Chatbot is running!")
    print(f"  👉 Open this URL in your browser: {url}")
    print("=" * 60 + "\n")

    def _open():
        import time as _time
        _time.sleep(2)
        webbrowser.open(url)

    threading.Thread(target=_open, daemon=True).start()


_print_url_and_open_browser()
