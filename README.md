# Multiplayer Rock-Paper-Scissors Game

This is a two-player Rock-Paper-Scissors game implemented in Python using socket programming and PyQt for the graphical interface. The game allows a server and client to connect over a local network  and play multiple rounds, with scores tracked automatically.

## Features

- **Local Network Multiplayer**: Play Rock-Paper-Scissors with a friend on the same network.
- **Graphical Interface**: A PyQt-based interface with easy-to-use buttons and score display.
- **Score Tracking**: The game keeps track of each player's score until one decides to quit.

## Requirements

- Python 3.7 or higher
- PyQt6 library

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/rock-paper-scissors-game.git
    cd rock-paper-scissors-game
    ```

2. Run the game by starting the server and client as described below.

## Usage

1. **Run the Game**:
   - Open two terminals to run the server and client scripts.
   - Ensure that both terminals are on the same network.
   - Replace `SERVER_IP` with the server's IP address in `client.py`.
   
2. **Start the Server**:
   - Run `server.py` to start the server (Player 1).
   ```bash
   python server.py

3. **Start the Client**:
   - On a different terminal, run `client.py` to start the client (Player 2).
   ```bash
   python client.py

4. **Play the Game**:

## Project Structure

- `server.py`: The main server script, handles Player 1's gameplay and communicates with the client.
- `client.py`: The client script, connects to the server for Player 2's gameplay.
- `README.md`: Project documentation.

## Future Improvements

- **Network Play**: Extend to allow play across the internet.
- **Additional Rounds**: Implement more gameplay modes or variations.
- **Leaderboard**: Add persistent storage for scores across sessions.

## License

This project is licensed under the Apache License 2.0. See the `LICENSE` file for more details.
