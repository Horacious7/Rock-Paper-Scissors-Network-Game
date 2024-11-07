import threading
import socket
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

class ClientApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Player 2 - Client") # You can change this to any name you would like
        self.setGeometry(600, 200, 300, 300)

        self.HOST = '127.0.0.1' # Be sure to change this to the correct IP address
        self.PORT = 7777 # Be sure to change this to the correct port number
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.HOST, self.PORT))

        self.client_choice = None
        self.server_ready = False
        self.client_ready = False
        self.client_score = 0
        self.server_score = 0

        # UI setup
        self.layout = QVBoxLayout()
        self.label = QLabel("Choose your move:", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label)

        # Rock, Paper, Scissors buttons
        self.rock_button = QPushButton("Rock", self)
        self.rock_button.clicked.connect(lambda: self.send_choice("Rock"))
        self.layout.addWidget(self.rock_button)

        self.paper_button = QPushButton("Paper", self)
        self.paper_button.clicked.connect(lambda: self.send_choice("Paper"))
        self.layout.addWidget(self.paper_button)

        self.scissors_button = QPushButton("Scissors", self)
        self.scissors_button.clicked.connect(lambda: self.send_choice("Scissors"))
        self.layout.addWidget(self.scissors_button)

        # Result label
        self.result_label = QLabel("", self)
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.result_label)

        # Score labels
        self.server_score_label = QLabel(f"Server Score: {self.server_score}", self)
        self.server_score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.server_score_label)

        self.client_score_label = QLabel(f"Client Score: {self.client_score}", self)
        self.client_score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.client_score_label)

        # Play again button
        self.play_again_button = QPushButton("Play again?", self)
        self.play_again_button.clicked.connect(self.prepare_for_next_game)
        self.play_again_button.setVisible(False)  # Initially hidden
        self.layout.addWidget(self.play_again_button)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        threading.Thread(target=self.receive_result, daemon=True).start()

    def send_choice(self, choice):
        self.client_choice = choice
        self.s.sendall(choice.encode())
        self.disable_buttons()

    def receive_result(self):
        while True:
            try:
                data = self.s.recv(1024).decode()
                if data == "ready":
                    self.server_ready = True
                    if self.client_ready:
                        self.reset_game_state()
                else:
                    self.result_label.setText(data)
                    self.update_score(data)
                    self.play_again_button.setVisible(True)
            except Exception as e:
                print(f"Connection error: {e}")
                break

    def update_score(self, result):
        if result == "Server wins!":
            self.server_score += 1
        elif result == "Client wins!":
            self.client_score += 1

        # Update score labels
        self.server_score_label.setText(f"Server Score: {self.server_score}")
        self.client_score_label.setText(f"Client Score: {self.client_score}")

    def prepare_for_next_game(self):
        self.client_ready = True
        self.play_again_button.setEnabled(False)
        self.s.sendall("ready".encode())
        if self.server_ready:
            self.reset_game_state()

    def reset_game_state(self):
        self.client_choice = None
        self.server_ready = False
        self.client_ready = False
        self.result_label.setText("")
        self.enable_buttons()
        self.play_again_button.setEnabled(True)
        self.play_again_button.setVisible(False)

    def enable_buttons(self):
        self.rock_button.setEnabled(True)
        self.paper_button.setEnabled(True)
        self.scissors_button.setEnabled(True)

    def disable_buttons(self):
        self.rock_button.setEnabled(False)
        self.paper_button.setEnabled(False)
        self.scissors_button.setEnabled(False)

    def closeEvent(self, event):
        self.s.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = ClientApp()
    client.show()
    sys.exit(app.exec())
