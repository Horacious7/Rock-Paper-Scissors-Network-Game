import socket
import threading
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

class ServerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Player 1 - Server") # You can change this to any name you would like
        self.setGeometry(600, 200, 300, 300)

        # Server setup
        self.HOST = '127.0.0.1'     # Be sure to change this to the correct IP address
        self.PORT = 7777            # Be sure to change this to the correct port number
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.HOST, self.PORT))
        self.server_socket.listen(1)
        self.client_socket, addr = self.server_socket.accept()

        self.server_choice = None
        self.client_choice = None
        self.server_ready = False
        self.client_ready = False
        self.server_score = 0
        self.client_score = 0

        # UI setup
        self.layout = QVBoxLayout()
        self.label = QLabel("Choose your move:", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label)

        # Rock, Paper, Scissors buttons
        self.rock_button = QPushButton("Rock", self)
        self.rock_button.clicked.connect(lambda: self.make_choice("Rock"))
        self.layout.addWidget(self.rock_button)

        self.paper_button = QPushButton("Paper", self)
        self.paper_button.clicked.connect(lambda: self.make_choice("Paper"))
        self.layout.addWidget(self.paper_button)

        self.scissors_button = QPushButton("Scissors", self)
        self.scissors_button.clicked.connect(lambda: self.make_choice("Scissors"))
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

        threading.Thread(target=self.receive_client_choice, daemon=True).start()

    def make_choice(self, choice):
        self.server_choice = choice
        self.disable_buttons()
        self.check_winner()

    def receive_client_choice(self):
        while True:
            try:
                data = self.client_socket.recv(1024).decode()
                if data == "ready":
                    self.client_ready = True
                    if self.server_ready:
                        self.reset_game_state()
                else:
                    self.client_choice = data
                    self.check_winner()
            except Exception as e:
                print(f"Connection error: {e}")
                break

    def check_winner(self):
        if self.server_choice and self.client_choice:
            if self.server_choice == self.client_choice:
                result = "It's a tie!"
            elif (self.server_choice == "Rock" and self.client_choice == "Scissors") or \
                    (self.server_choice == "Paper" and self.client_choice == "Rock") or \
                    (self.server_choice == "Scissors" and self.client_choice == "Paper"):
                result = "Server wins!"
            else:
                result = "Client wins!"

            self.result_label.setText(result)
            self.client_socket.sendall(result.encode())
            self.update_score(result)  # Actualizăm scorul
            self.play_again_button.setVisible(True)

    def update_score(self, result):
        if result == "Server wins!":
            self.server_score += 1
        elif result == "Client wins!":
            self.client_score += 1

        # This updates the score labels
        self.server_score_label.setText(f"Server Score: {self.server_score}")
        self.client_score_label.setText(f"Client Score: {self.client_score}")

    def prepare_for_next_game(self):
        self.server_ready = True
        self.play_again_button.setEnabled(False)
        self.client_socket.sendall("ready".encode())
        if self.client_ready:
            self.reset_game_state()

    def reset_game_state(self):
        self.server_choice = None
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
        self.client_socket.close()
        self.server_socket.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    server = ServerApp()
    server.show()
    sys.exit(app.exec())
