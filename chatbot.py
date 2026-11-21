questions = {

    "Python Developer": [
        "What is Python?",
        "What is a list in Python?",
        "What is a dictionary in Python?",
        "What is a function in Python?",
        "What is object-oriented programming?"
    ],

    "AI/ML Engineer": [
        "What is Artificial Intelligence?",
        "What is Machine Learning?",
        "What is supervised learning?",
        "What is deep learning?",
        "What is a neural network?"
    ],

    "Software Engineer": [
        "What is a programming language?",
        "What is an algorithm?",
        "What is a database?",
        "What is an API?",
        "What is Git?"
    ]
}


def get_question(role, question_number):

    role_questions = questions.get(role, [])

    if question_number >= len(role_questions):
        return None

    return role_questions[question_number]


def evaluate_answer(answer, role, question):

    answer_lower = answer.lower()

    keywords = {
        "Python Developer": [
            "python",
            "list",
            "dictionary",
            "function",
            "object"
        ],

        "AI/ML Engineer": [
            "artificial",
            "machine",
            "supervised",
            "deep",
            "neural"
        ],

        "Software Engineer": [
            "program",
            "algorithm",
            "database",
            "api",
            "git"
        ]
    }

    role_keywords = keywords.get(role, [])

    matched = False

    for word in role_keywords:
        if word in answer_lower:
            matched = True
            break

    if matched:

        feedback = (
            "Your answer contains relevant information. "
            "Try to explain the concept with a simple example "
            "to make your answer stronger."
        )

        return 1, feedback

    else:

        feedback = (
            "Your answer needs improvement. "
            "Try to include the definition, key points, "
            "and a simple example."
        )

        return 0, feedback