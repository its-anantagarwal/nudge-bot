import sys
import random
import re

from PySide6.QtWidgets import(
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QPushButton,
    QLabel
)
from PySide6.QtCore import Qt


INTENTS = {
    "GREETING": [
        "hello",
        "hi",
        "hey",
        "yo",
        "good morning",
        "good afternoon",
        "good evening",
        "sup"
    ],

    "SAD": [
        "sad",
        "unhappy",
        "upset",
        "miserable",
        "down",
        "lonely"
    ],

    "TIRED": [
        "tired",
        "exhausted",
        "sleepy",
        "drained",
        "fatigued"
    ],

    "HAPPY": [
        "happy",
        "excited",
        "great",
        "amazing",
        "awesome",
        "good"
    ],

    "STUDYING": [
        "studying",
        "study",
        "homework",
        "revision",
        "revising",
        "schoolwork"
    ],
}

TOPICS = {
    "physics": ["physics", "phy"],
    "chemistry": ["chemistry", "chem"],
    "mathematics": ["math", "maths", "mathematics"],
    "computer science": ["computer science", "cs", "coding", "programming"],
    "school": ["school", "classes", "class"],
}

DIFFICULTY_PHRASES = [
    "difficult",
    "hard",
    "confusing",
    "struggling",
    "don't understand",
    "do not understand",
    "can't understand",
    "cannot understand",
]

class NudgeBot(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Nudge Bot")
        self.resize(700,600)
        self.setup_ui()
        self.last_intent = None
        self.last_question = None
        self.current_topic = None
        self.waiting_for = None

    def setup_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        title = QLabel("NudgeBot")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            padding: 10px;
        """)

        main_layout.addWidget(title)

        self.chat = QTextEdit()
        self.chat.setReadOnly(True)
        self.chat.setStyleSheet("""
            QTextEdit{
                background-color:#121212;
                color:white;
                border:1px solid #333333;
                border-radius:10px;
                padding:12px;
                font-size:16px;
            }
        """)

        main_layout.addWidget(self.chat)

        input_layout = QHBoxLayout()

        self.input_box = QTextEdit()

        self.input_box.setPlaceholderText("Type a message...")
        self.input_box.setFixedHeight(60)
        self.input_box.setStyleSheet("""
            QTextEdit{
                background-color:#1e1e1e;
                color:white;
                border:1px solid #444444;
                border-radius:10px;
                padding:10px;
                font-size:16px;
            }
        """)

        input_layout.addWidget(self.input_box)

        send_button = QPushButton("Send")

        send_button.setFixedWidth(90)
        send_button.clicked.connect(self.send_message)
        send_button.setStyleSheet("""
            QPushButton{
                background-color:#6c4cff;
                color:white;
                border:none;
                border-radius:10px;
                font-size:16px;
                padding:10px;
            }
            QPushButton:hover{
                background-color:#8066ff;
            }
        """)

        input_layout.addWidget(send_button)
        main_layout.addLayout(input_layout)

        self.add_bot_message("Hey! I am Nudge Bot. How are you feeling today?")

    def send_message(self):
        message = self.input_box.toPlainText().strip()

        if not message:
            return

        self.add_user_message(message)
        self.input_box.clear()

        response = self.generate_response(message)
        self.add_bot_message(response)

    def generate_response(self, message):
        intent = self.detect_intent(message)
        topic = self.detect_topic(message)

        if topic:
            self.current_topic = topic

        if self.waiting_for == "tired_reason":
            self.waiting_for = None
            return f"Got it. So you've been {message.lower().strip()}."

        if self.waiting_for == "study_subject":
            self.waiting_for = None

            detected_topic = self.detect_topic(message)

            if detected_topic:
                self.current_topic = detected_topic
            else:
                self.current_topic = message.strip()

            return f"Nice. You're working on {self.current_topic}. How's it going?"

        if self.waiting_for == "sad_reason":
            self.waiting_for = None
            return "I see. Thanks for telling me."


        if self.current_topic:
            message_lower = message.lower()

            for phrase in DIFFICULTY_PHRASES:
                if phrase in message_lower:
                    return f"What part of {self.current_topic} are you finding difficult?"

        if intent == "STUDYING" and self.last_intent == "TIRED":
            self.last_intent = intent
            self.waiting_for = "study_subject"

            return random.choice([
                "Studying? What subject?",
                "Ah, that's probably why you're tired. What subject?",
                "Study session, huh? What are you working on?"
            ])

        self.last_intent = intent

        responses = {

            "GREETING": [
                "Hey! What's up?",
                "Hey there! How are you doing?",
                "Hi! Good to see you.",
                "Hey! What's going on?"
            ],

            "SAD": [
                "I'm sorry you're feeling down. Want to talk about it?",
                "That doesn't sound great. What happened?",
                "I'm here if you want to talk about it.",
                "Sounds like something's bothering you."
            ],

            "TIRED": [
                "Sounds like you've had a long day. What have you been doing?",
                "You sound exhausted. What happened?",
                "Running low on battery? What's been keeping you busy?",
                "Sounds like you could use a break. What have you been up to?"
            ],

            "HAPPY": [
                "That's great! What's making you happy?",
                "Nice! What's going so well?",
                "I like the sound of that :)",
                "That's awesome! Tell me about it."
            ],

            "UNKNOWN": [
                "Hmm... tell me more about that.",
                "Interesting. What makes you say that?",
                "I see. Can you tell me more?",
                "I'm listening."
            ],

            "STUDYING": [
                "What are you studying?",
                "What subject are you working on?",
                "Study session, huh? What are you working on?",
                "What's the topic?"
            ],
        }

        response = random.choice(responses[intent])

        if intent == "TIRED":
            self.waiting_for = "tired_reason"

        elif intent == "STUDYING":
            self.waiting_for = "study_subject"

        elif intent == "SAD":
            self.waiting_for = "sad_reason"

        return response

    def handle_confirmation(self, message):
        message = message.lower().strip()

        if message in ["yes", "yeah", "yep", "yup"]:
            return "Got it. Tell me more."

        if message in ["no", "nope", "nah"]:
            return "Alright. So what's going on?"

        return "Okay. Tell me more."
    
    def add_user_message(self, message):
        self.chat.append(
            f'<p style ="color:#9b8cff;"><b>You:<b> {message}</p>'
        )

    def add_bot_message(self, message):
        self.chat.append(
            f'<p style="color:#ffffff;"><b>Nudge Bot:</b> {message}</p>'
        )

    def detect_intent(self, message):
        message = message.lower()
        for intent, keywords in INTENTS.items():
            for keyword in keywords:
                if keyword in message:
                    return intent

        return "UNKNOWN"

    def detect_topic(self, message):
        message = message.lower()

        for topic, keywords in TOPICS.items():
            for keyword in keywords:
                pattern = r"\b" + re.escape(keyword) + r"\b"

                if re.search(pattern, message):
                    return topic

        return None

    def is_question(self, message):
        question_words = [
            "what",
            "why",
            "how",
            "when",
            "where",
            "who",
            "which",
            "do you",
            "are you",
            "have you",
            "can you"
        ]

        message = message.lower().strip()

        if message.endswith("?"):
            return True

        for word in question_words:
            if message.startswith(word):
                return True

        return False

app = QApplication(sys.argv)

window = NudgeBot()
window.show()

sys.exit(app.exec())