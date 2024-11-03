import sys
import random
from functools import partial
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFrame, QSlider, QComboBox, QVBoxLayout, QGridLayout, QLabel, QWidget
from ui import Ui_Dialog  # Importing the UI class from ui.py

class GameOfLife(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()  # Create an instance of the UI class
        self.ui.setupUi(self)  # Set up the UI
        self.setWindowTitle("Game of Life")
        
        # Initialize grid parameters
        self.rows = 20
        self.cols = 20
        self.grid = [[0] * self.cols for _ in range(self.rows)]
        
        # Create the grid layout and buttons
        self.grid_layout = QGridLayout()
        self.cells = [[QPushButton() for _ in range(self.cols)] for _ in range(self.rows)]
        self.setup_grid()

        # Add the grid layout to the GridFrame
        self.ui.GridFrame.setLayout(self.grid_layout)

        # Connect UI buttons to methods
        self.ui.Start.clicked.connect(self.start_game)
        self.ui.Stop.clicked.connect(self.stop_game)
        self.ui.Clear.clicked.connect(self.clear_grid)
        self.ui.AddPattern.clicked.connect(self.add_pattern)
        self.ui.Evolutionary_Computation.clicked.connect(self.add_evolutionary_pattern)

        # Timer for updating the grid
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_grid)

        # Configure the slider for speed control
        self.ui.SpeedSlider.setMinimum(200)  # Set minimum speed to 200 ms
        self.ui.SpeedSlider.setMaximum(2000)  # Set maximum speed to 2000 ms
        self.ui.SpeedSlider.setValue(1000)  # Set default speed to 1000 ms
        self.ui.SpeedSlider.valueChanged.connect(self.update_speed)

        # Set the initial speed
        self.update_speed()

        # Add items to the combo box with new patterns
        self.ui.comboBox.addItems(["Glider", "Blinker", "Toad", "Beacon", "Pulsar", "Glider Gun"])

    def setup_grid(self):
        """Sets up the grid buttons."""
        for i in range(self.rows):
            for j in range(self.cols):
                cell_button = self.cells[i][j]
                cell_button.setFixedSize(20, 20)  # Adjust size if needed
                cell_button.setStyleSheet("background-color: white;")
                cell_button.clicked.connect(partial(self.toggle_cell, i, j))
                self.grid_layout.addWidget(cell_button, i, j)

    def toggle_cell(self, x, y):
        """Toggles the state of a cell when clicked."""
        self.grid[x][y] = 1 - self.grid[x][y]  # Toggle the cell state
        self.update_button_style(x, y)

    def update_button_style(self, x, y):
        """Updates the button color based on the cell state."""
        if self.grid[x][y] == 1:
            self.cells[x][y].setStyleSheet("background-color: black;")  # Alive
        else:
            self.cells[x][y].setStyleSheet("background-color: white;")  # Dead

    def start_game(self):
        """Starts the game by starting the timer."""
        self.timer.start(self.ui.SpeedSlider.value())

    def stop_game(self):
        """Stops the game by stopping the timer."""
        self.timer.stop()

    def clear_grid(self):
        """Clears the grid."""
        self.grid = [[0] * self.cols for _ in range(self.rows)]
        self.update_buttons()

    def add_pattern(self):
        """Adds a pattern to the grid based on the selected combo box item."""
        pattern = self.ui.comboBox.currentText()
        if pattern == "Glider":
            self.add_glider()
        elif pattern == "Blinker":
            self.add_blinker()
        elif pattern == "Toad":
            self.add_toad()
        elif pattern == "Beacon":
            self.add_beacon()
        elif pattern == "Pulsar":
            self.add_pulsar()
        elif pattern == "Glider Gun":
            self.add_glider_gun()
        self.update_buttons()

    def add_glider(self):
        """Adds a glider pattern to the grid."""
        glider = [(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)]
        self.add_pattern_to_grid(glider)

    def add_blinker(self):
        """Adds a blinker pattern to the grid."""
        blinker = [(1, 0), (1, 1), (1, 2)]
        self.add_pattern_to_grid(blinker)

    def add_toad(self):
        """Adds a toad pattern to the grid."""
        toad = [(1, 0), (1, 1), (1, 2), (0, 2), (0, 3), (0, 4)]
        self.add_pattern_to_grid(toad)

    def add_beacon(self):
        """Adds a beacon pattern to the grid."""
        beacon = [(1, 1), (1, 2), (2, 1), (2, 2), (0, 0), (0, 1), (1, 0), (2, 0)]
        self.add_pattern_to_grid(beacon)

    def add_pulsar(self):
        """Adds a pulsar pattern to the grid."""
        pulsar = [
            (2, 1), (2, 2), (2, 3),
            (3, 1), (3, 2), (3, 3),
            (4, 1), (4, 2), (4, 3),
            (1, 4), (2, 4), (3, 4),
            (4, 4), (5, 1), (5, 2),
            (5, 3), (1, 2), (1, 3)
        ]
        self.add_pattern_to_grid(pulsar)

    def add_glider_gun(self):
        """Adds a glider gun pattern to the grid."""
        glider_gun = [
            (5, 1), (5, 2), (6, 1), (6, 2),
            (5, 11), (6, 11), (7, 11), (4, 12),
            (5, 12), (6, 12), (5, 13), (6, 13),
            (7, 12), (7, 13), (8, 12), (8, 13),
            (9, 11), (10, 11), (9, 12), (10, 12),
            (11, 11), (11, 12), (12, 11), (12, 12)
        ]
        self.add_pattern_to_grid(glider_gun)

    def add_pattern_to_grid(self, pattern):
        """Adds a specified pattern to the grid."""
        for x, y in pattern:
            if 0 <= x < self.rows and 0 <= y < self.cols:
                self.grid[x][y] = 1  # Set cell to alive
                self.cells[x][y].setStyleSheet("background-color: black;")  # Update button color

    def add_evolutionary_pattern(self):
        """Adds random evolution cells to the grid."""
        for _ in range(random.randint(5, 20)):  # Randomly add between 5 and 20 cells
            x = random.randint(0, self.rows - 1)
            y = random.randint(0, self.cols - 1)
            if self.grid[x][y] == 0:  # Only add if the cell is currently dead
                self.add_pattern_to_grid([(x, y)])

    def update_grid(self):
        """Updates the grid according to Game of Life rules."""
        new_grid = [[0] * self.cols for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                alive_neighbors = self.count_alive_neighbors(i, j)
                if self.grid[i][j] == 1:  # Alive cell
                    if alive_neighbors in (2, 3):
                        new_grid[i][j] = 1  # Stay alive
                else:  # Dead cell
                    if alive_neighbors == 3:
                        new_grid[i][j] = 1  # Become alive
        self.grid = new_grid
        self.update_buttons()

    def count_alive_neighbors(self, x, y):
        """Counts the number of alive neighbors for a given cell."""
        count = 0
        for i in range(max(0, x - 1), min(self.rows, x + 2)):
            for j in range(max(0, y - 1), min(self.cols, y + 2)):
                if (i == x and j == y):
                    continue
                count += self.grid[i][j]
        return count

    def update_buttons(self):
        """Updates the button styles based on the current grid state."""
        for i in range(self.rows):
            for j in range(self.cols):
                self.update_button_style(i, j)

    def update_speed(self):
        """Updates the speed of the timer based on the slider value."""
        self.timer.setInterval(self.ui.SpeedSlider.value())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameOfLife()
    window.show()
    sys.exit(app.exec_())
