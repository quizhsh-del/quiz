def detect_intent(question):
    q = question.lower().strip()

    if q.startswith("what"):
        return "define"
    if q.startswith("which"):
        return "choose"
    if q.startswith("why"):
        return "reason"
    if q.startswith("how"):
        return "process"
    return "general"
import re

STOPWORDS = {
    "what","which","why","how","is","are","the","of",
    "following","correct","option","does"
}

def extract_topic(question):
    words = re.findall(r"[a-zA-Z]{3,}", question.lower())
    topic_words = [w for w in words if w not in STOPWORDS]
    return " ".join(topic_words[:4])
STEM_TEMPLATES = {
    "define": [
        "What is {topic}?",
        "{topic} is defined as:",
        "Identify the correct definition of {topic}."
    ],
    "choose": [
        "Which of the following is related to {topic}?",
        "Select the correct option for {topic}.",
        "Identify {topic} from the options below."
    ],
    "reason": [
        "Why is {topic} important?",
        "State the reason for {topic}.",
    ],
    "process": [
        "How does {topic} work?",
        "Describe the working of {topic}.",
    ],
    "general": [
        "Choose the correct answer related to {topic}."
    ]
}
import random

def rebuild_mcq_stem(question):
    intent = detect_intent(question)
    topic = extract_topic(question)

    templates = STEM_TEMPLATES[intent]
    return random.choice(templates).format(topic=topic)
text= "SIdentify cloud computing advantage from the options below."
clear_output= rebuild_mcq_stem(text)
clear_output