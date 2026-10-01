import sys

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
    ]
}

class NudgeBot(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Nudge Bot")
        self.resize(700,600)
        self.setup_ui()

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
        if intent == "GREETING":
            return "Hey! What's up?"

        if intent == "SAD":
            return "I'm sorry you're feeling down. Want to talk about it?"

        if intent == "TIRED":
            return "Sounds like you've had a long day."

        if intent == "HAPPY":
            return "That's great! What's making you happy?"

        return "Hmm... tell me more about that."

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

        return "Unknown"

app = QApplication(sys.argv)

window = NudgeBot()
window.show()

sys.exit(app.exec())