# utils.py
import re
import random

# -------------------------------
# Detect intent of question
# -------------------------------
def detect_intent(question):
    q = question.lower().strip()

    if q.startswith(("what", "define", "explain")):
        return "define"
    if q.startswith(("which", "identify", "select", "choose")):
        return "choose"
    if q.startswith("where"):
        return "location"
    if q.startswith("why"):
        return "reason"
    if q.startswith("how"):
        return "process"

    return "general"


# -------------------------------
# Stopwords
# -------------------------------
STOPWORDS = {
    "what", "which", "why", "how", "where",
    "is", "are", "was", "were", "the", "of",
    "from", "below", "following",
    "correct", "option", "options",
    "identify", "select", "choose",
    "does", "do", "did"
}


# -------------------------------
# Extract topic
# -------------------------------
def extract_topic(question):
    words = re.findall(r"[a-zA-Z]{3,}", question.lower())
    topic_words = [w for w in words if w not in STOPWORDS]
    return " ".join(topic_words[:5])


# -------------------------------
# Stem templates
# -------------------------------
STEM_TEMPLATES = {
    "define": [
        "What is {topic}?",
        "Define {topic}.",
        "Which statement best describes {topic}?"
    ],
    "choose": [
        "Which of the following best represents {topic}?",
        "Select the correct option related to {topic}.",
        "Identify the correct answer for {topic}."
    ],
    "location": [
        "Where is {topic} located?",
        "Identify the location of {topic}."
    ],
    "reason": [
        "Why is {topic} important?",
        "State the reason for {topic}."
    ],
    "process": [
        "How does {topic} work?",
        "Explain the working of {topic}."
    ],
    "general": [
        "Choose the correct answer related to {topic}.",
        "Which option is correct for {topic}?"
    ]
}


# -------------------------------
# Main NLP regeneration function
# -------------------------------
def rebuild_mcq_stem(question):
    if not question:
        return ""

    intent = detect_intent(question)
    topic = extract_topic(question)

    if not topic:
        return question  # fallback

    templates = STEM_TEMPLATES.get(intent, STEM_TEMPLATES["general"])
    return random.choice(templates).format(topic=topic)
