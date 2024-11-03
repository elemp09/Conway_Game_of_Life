import sys
import random
from functools import partial
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFrame, QSlider, QComboBox, QVBoxLayout, QGridLayout, QLabel, QWidget
from PyQt5.QtGui import QPalette, QColor
from ui import Ui_Dialog  # Importing the UI class from ui.py

class GameOfLife(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()  # Create an instance of the UI class
        self.ui.setupUi(self)  # Set up the UI
        self.setWindowTitle("Game of Life")
        
        # Set a modern color palette for the application
        self.set_dark_palette()

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
        self.ui.Evolutionary_Computation.clicked.connect(self.run_evolutionary_algorithm)

        # Timer for updating the grid
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_grid)

        # Configure the slider for speed control
        self.ui.SpeedSlider.setMinimum(200)
        self.ui.SpeedSlider.setMaximum(2000)
        self.ui.SpeedSlider.setValue(1000)
        self.ui.SpeedSlider.valueChanged.connect(self.update_speed)

        # Set the initial speed
        self.update_speed()

        # Add items to the combo box with new patterns
        self.ui.comboBox.addItems(["Glider", "Blinker", "Toad", "Beacon", "Pulsar", "Glider Gun"])

    def set_dark_palette(self):
        """Sets a dark theme palette for the application."""
        dark_palette = QPalette()

        # Basic dark theme colors
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
        dark_palette.setColor(QPalette.Text, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))

        # Set the palette for the application
        QApplication.setPalette(dark_palette)

    def setup_grid(self):
        """Sets up the grid buttons with a modern style."""
        for i in range(self.rows):
            for j in range(self.cols):
                cell_button = self.cells[i][j]
                cell_button.setFixedSize(20, 20)
                cell_button.setStyleSheet("background-color: #2d2d2d; border: 1px solid #444;")  # Dark cell background
                cell_button.clicked.connect(partial(self.toggle_cell, i, j))
                self.grid_layout.addWidget(cell_button, i, j)

    def toggle_cell(self, x, y):
        """Toggles the state of a cell when clicked."""
        self.grid[x][y] = 1 - self.grid[x][y]
        self.update_button_style(x, y)

    def update_button_style(self, x, y):
        """Updates the button color based on the cell state."""
        if self.grid[x][y] == 1:
            self.cells[x][y].setStyleSheet("background-color: #21c362; border: 1px solid #444;")  # Alive cell in green
        else:
            self.cells[x][y].setStyleSheet("background-color: #2d2d2d; border: 1px solid #444;")  # Dead cell in dark color


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

    # Pattern Methods
    # (omitted here for brevity, but they should be included as in the previous response)

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
        """Updates the colors of the buttons based on the current grid state."""
        for i in range(self.rows):
            for j in range(self.cols):
                self.update_button_style(i, j)

    def update_speed(self):
        """Updates the speed of the timer based on the slider value."""
        self.timer.setInterval(self.ui.SpeedSlider.value())

    # Evolutionary Algorithm
    def run_evolutionary_algorithm(self, generations=10, population_size=20):
        """Runs an evolutionary algorithm to find an optimal starting pattern."""
        population = [self.generate_random_pattern() for _ in range(population_size)]
        
        for generation in range(generations):
            # Evaluate fitness of each pattern
            fitness_scores = [self.evaluate_fitness(pattern) for pattern in population]
            
            # Selection: keep top 50% of the population
            selected_population = [population[i] for i in sorted(range(len(fitness_scores)), key=lambda i: fitness_scores[i], reverse=True)[:population_size // 2]]
            
            # Crossover and mutation to create new patterns
            new_population = selected_population[:]
            while len(new_population) < population_size:
                parent1, parent2 = random.sample(selected_population, 2)
                child = self.crossover(parent1, parent2)
                self.mutate(child)
                new_population.append(child)
            
            # Update population for the next generation
            population = new_population
        
        # Set the grid to the best pattern found
        best_pattern = max(population, key=self.evaluate_fitness)
        self.grid = best_pattern
        self.update_buttons()

    def generate_random_pattern(self):
        """Generates a random pattern for the grid."""
        return [[random.choice([0, 1]) for _ in range(self.cols)] for _ in range(self.rows)]

    def evaluate_fitness(self, pattern):
        """Evaluates the fitness of a pattern based on live cells after several generations."""
        test_grid = [row[:] for row in pattern]
        for _ in range(10):  # Run the game for 10 steps
            new_grid = [[0] * self.cols for _ in range(self.rows)]
            for i in range(self.rows):
                for j in range(self.cols):
                    alive_neighbors = self.count_alive_neighbors_in_grid(test_grid, i, j)
                    if test_grid[i][j] == 1:  # Alive cell
                        if alive_neighbors in (2, 3):
                            new_grid[i][j] = 1  # Stay alive
                    else:  # Dead cell
                        if alive_neighbors == 3:
                            new_grid[i][j] = 1  # Become alive
            test_grid = new_grid
        return sum(sum(row) for row in test_grid)  # Fitness: total number of alive cells

    def count_alive_neighbors_in_grid(self, grid, x, y):
        """Counts the number of alive neighbors for a given cell in a specific grid."""
        count = 0
        for i in range(max(0, x - 1), min(self.rows, x + 2)):
            for j in range(max(0, y - 1), min(self.cols, y + 2)):
                if (i == x and j == y):
                    continue
                count += grid[i][j]
        return count

    def crossover(self, parent1, parent2):
        """Creates a new pattern by crossing over two parent patterns."""
        child = [[0] * self.cols for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                child[i][j] = random.choice([parent1[i][j], parent2[i][j]])
        return child

    def mutate(self, pattern, mutation_rate=0.01):
        """Mutates a pattern with a given mutation rate."""
        for i in range(self.rows):
            for j in range(self.cols):
                if random.random() < mutation_rate:
                    pattern[i][j] = 1 - pattern[i][j]  # Toggle cell state

def main():
    app = QApplication(sys.argv)
    game = GameOfLife()
    game.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
