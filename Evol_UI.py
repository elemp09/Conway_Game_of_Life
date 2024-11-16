import sys
import random
from functools import partial
from PyQt5 import QtCore 
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QSizePolicy, QTextEdit, QMainWindow, QPushButton, QFrame, QSlider, QComboBox, QVBoxLayout, QGridLayout, QLabel, QWidget
from PyQt5.QtGui import QPalette, QColor, QTextCursor
from PyQt5.QtCore import QTimer, Qt, QRect
from ui import Ui_Dialog  
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class Logs:
    @staticmethod
    def app_msg(message):
        print(f"LOG: {message}")

class GameOfLife(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)  
        self.setWindowTitle("Game of Life")

        self.logs = Logs()  # Initialize logging system

        print(f"self.ui.logger is: {self.ui.logger}") 
        self.logger_layout = QVBoxLayout(self.ui.logger)
        self.ui.Logger_QText.setReadOnly(True) 
        self.ui.Logger_QText.setGeometry(QRect(0, 0, 600, 400)) 
        self.ui.Logger_QText.setMinimumHeight(400)  
        
        self.logger_layout.addWidget(self.ui.Logger_QText)
        
        self.ui.Logger_QText.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  
        self.ui.Logger_QText.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.set_white_palette()  

        self.logs.app_msg("Game of Life initialized")  

        # Initialize grid settings
        self.rows = 20
        self.cols = 20
        self.grid = [[0] * self.cols for _ in range(self.rows)]

        self.grid_layout = QGridLayout()
        self.cells = [[QPushButton() for _ in range(self.cols)] for _ in range(self.rows)]
        self.setup_grid()  # Set up grid of buttons

        self.ui.GridFrame.setLayout(self.grid_layout)

        # Connect UI buttons to methods
        self.ui.Start.clicked.connect(self.start_game)
        self.ui.Stop.clicked.connect(self.stop_game)
        self.ui.Clear.clicked.connect(self.clear_grid)
        self.ui.AddPattern.clicked.connect(self.add_pattern)
        self.ui.Evolutionary_Computation.clicked.connect(self.run_evolutionary_algorithm)

        # Set up timers for grid and plot updates
        self.grid_timer = QTimer()
        self.grid_timer.timeout.connect(self.update_grid)

        self.plot_update_timer = QTimer(self)
        self.plot_update_timer.timeout.connect(self.update_plot)

        # Set up speed control slider
        self.ui.SpeedSlider.setMinimum(200)
        self.ui.SpeedSlider.setMaximum(2000)
        self.ui.SpeedSlider.setValue(1000)  
        self.ui.SpeedSlider.valueChanged.connect(self.update_speed)

        self.update_speed()  # Set initial speed

        self.game_running = False  # Game state flag

        # Add patterns to combo box
        self.ui.comboBox.addItems(["Glider", "Blinker", "Toad", "Beacon", "Pulsar", "Glider Gun"])

        # Initialize plot tracking
        self.fitness_history = []  
        self.current_generation = 0

        # Set up the fitness plot
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.ax.set_title("Fitness over Generations")
        self.ax.set_xlabel("Generation")
        self.ax.set_ylabel("Fitness")
        self.line, = self.ax.plot([], [], marker='o')  

        # Add canvas to plot frame layout if not already set
        if not self.ui.PlotFrame.layout():
            plot_layout = QVBoxLayout(self.ui.PlotFrame)
            self.ui.PlotFrame.setLayout(plot_layout)

        self.canvas = FigureCanvas(self.fig)
        self.ui.PlotFrame.layout().addWidget(self.canvas)

        # Ensure canvas resizes with window
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvas.updateGeometry()

        # Enable real-time updates on plot
        plt.ion()
        self.canvas.draw()  

    def log_message(self, message):
        """Appends a message to the Logger_QText widget."""
        print(f"Logging message: {message}")  # Print to console
        self.ui.Logger_QText.append(message)  # Append message to the widget
        self.ui.Logger_QText.ensureCursorVisible()  # Ensure cursor stays at the bottom

    def resizeEvent(self, event):
        # Resize canvas when window size changes
        self.canvas.resize(self.ui.PlotFrame.width(), self.ui.PlotFrame.height())
        event.accept()

    def update_plot(self):
        """Update the plot with new data if the game is running and there are alive cells."""
        if not self.game_running:
            return  # No update if game is stopped

        # Check for any live cells
        any_alive = any(any(cell == 1 for cell in row) for row in self.grid)

        if any_alive:  # Only update if there are alive cells
            self.current_generation += 1
            fitness_value = random.uniform(0, 100)  # Random fitness value
            self.fitness_history.append(fitness_value)

            # Log the fitness data
            self.logs.app_msg(f"Generation {self.current_generation}: Fitness = {fitness_value:.2f}")
            self.log_message(f"Generation {self.current_generation}: Fitness = {fitness_value:.2f}")
            
            # Update the plot
            self.line.set_data(range(self.current_generation), self.fitness_history)

            # Redraw the canvas with updated data
            self.ax.relim()  # Recalculate axis limits
            self.ax.autoscale_view()  # Adjust to fit data
            self.canvas.draw()  # Redraw canvas

    def set_white_palette(self):
        white_palette = QPalette()

        # Set up basic white theme colors
        white_palette.setColor(QPalette.Window, QColor(255, 255, 255))
        white_palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
        white_palette.setColor(QPalette.Base, QColor(255, 255, 255))
        white_palette.setColor(QPalette.AlternateBase, QColor(240, 240, 240))
        white_palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        white_palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
        white_palette.setColor(QPalette.Text, QColor(0, 0, 0))
        white_palette.setColor(QPalette.Button, QColor(240, 240, 240))
        white_palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))

        # Apply the white palette to the app
        QApplication.setPalette(white_palette)

    def setup_grid(self):
        for i in range(self.rows):
            for j in range(self.cols):
                cell_button = self.cells[i][j]
                cell_button.setFixedSize(30, 30) 
                cell_button.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc;")
                cell_button.clicked.connect(partial(self.toggle_cell, i, j))  
                self.grid_layout.addWidget(cell_button, i, j)

    def toggle_cell(self, x, y):
        """Toggles the state of a cell when clicked."""
        self.grid[x][y] = 1 - self.grid[x][y]  # Switch between alive (1) and dead (0)
        self.update_button_style(x, y) 

    def update_button_style(self, x, y):
        """Updates the button color based on the cell state."""
        if self.grid[x][y] == 1:
            self.cells[x][y].setStyleSheet("background-color: #21c362; border: 2px solid #ccc; border-radius: 5px;")  # Green for alive
        else:
            self.cells[x][y].setStyleSheet("background-color: #f0f0f0; border: 2px solid #ccc; border-radius: 5px;")  # Light color for dead


    def start_game(self):
        """Start the game and initialize the grid."""
        self.game_running = True
        self.grid_timer.start(self.ui.SpeedSlider.value())  # Start grid update timer
        self.plot_update_timer.start(1000)  # Start plot update timer
        self.logs.app_msg("Game started!")

    def stop_game(self):
        """Stop the game and stop all timers."""
        self.game_running = False
        self.grid_timer.stop()  # Stop grid update timer
        self.plot_update_timer.stop()  # Stop plot update timer

    def clear_grid(self):
        """Clears the grid."""
        self.grid = [[0] * self.cols for _ in range(self.rows)]  # Reset grid to all dead cells
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
            (5, 12), (6, 12), (3, 13), (7, 13),
            (4, 14), (8, 14), (5, 15), (6, 15),
            (5, 16), (6, 16), (5, 17), (4, 18),
            (5, 18), (6, 18), (6, 19), (7, 19),
            (5, 21), (6, 21), (7, 21), (5, 22),
            (6, 22), (7, 22), (6, 23)
        ]
        self.add_pattern_to_grid(glider_gun)
        
    def add_pattern_to_grid(self, pattern):
        """Adds a specified pattern to the grid."""
        for x, y in pattern:
            if 0 <= x < self.rows and 0 <= y < self.cols:
                self.grid[x][y] = 1  # Set cell to alive
                self.cells[x][y].setStyleSheet("background-color: black;") 


    def update_grid(self):
        """Updates the grid based on the Game of Life rules."""
        
        if not self.game_running:
            return  # Exit early if the game is not running
        
        new_grid = [[0] * self.cols for _ in range(self.rows)]  # Create a new grid for the next generation

        # Iterate over each cell to apply Game of Life rules
        for x in range(self.rows):
            for y in range(self.cols):
                alive_neighbors = self.count_alive_neighbors(x, y)  # Count alive neighbors

                # Apply Game of Life rules
                if self.grid[x][y] == 1:  # Cell is alive
                    if alive_neighbors in [2, 3]:  # Stay alive with 2 or 3 neighbors
                        new_grid[x][y] = 1
                    else:  # Die if not 2 or 3 neighbors
                        new_grid[x][y] = 0
                else:  # Cell is dead
                    if alive_neighbors == 3:  # Become alive if exactly 3 neighbors
                        new_grid[x][y] = 1
                    else:
                        new_grid[x][y] = 0

        self.grid = new_grid  # Update the grid with the new generation
        self.update_buttons() 

    def plot_update(self):
        """Update the plot with the current grid state."""
        
        if not self.game_running:
            return  # Skip plot update if the game is not running

        self.plot_grid(self.grid) 

    def count_alive_neighbors(self, x, y):
        """Counts the number of alive neighbors of a given cell (x, y)."""
        neighbors = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        count = 0
        for dx, dy in neighbors:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.rows and 0 <= ny < self.cols:  # Check for boundary conditions
                count += self.grid[nx][ny]
        return count

    def update_buttons(self):
        """Updates the button styles based on the current grid state."""
        for i in range(self.rows):
            for j in range(self.cols):
                self.update_button_style(i, j) 

    def update_speed(self):
        """Updates the speed of the game based on slider value."""
        self.grid_timer.setInterval(self.ui.SpeedSlider.value())  # Set the grid update timer interval

    def display_pattern(self, pattern):
        """Displays a given pattern on the grid."""
        for x in range(self.rows):
            for y in range(self.cols):
                self.grid[x][y] = pattern[x][y]  # Set grid cell to the pattern value
        self.update_buttons()
        
    def run_evolutionary_algorithm(self, generations=10, population_size=20):
        """Runs an evolutionary algorithm to find an optimal starting pattern."""
        # Initialize population with random patterns
        population = [self.generate_random_pattern() for _ in range(population_size)]
        
        best_pattern = None  # Initialize the best pattern variable

        print(f"self.logs is: {self.logs}") 
        self.logs.app_msg("Starting evolutionary computation...") 
        
        self.log_message("Starting evolutionary computation...")

        for generation in range(generations):
            # Step 1: Evaluate fitness of each pattern in the population
            fitness_scores = [self.evaluate_fitness(pattern) for pattern in population]
            
            # Track the best fitness of this generation
            best_fitness = max(fitness_scores)
            self.fitness_history.append(best_fitness)
            self.current_generation = generation + 1

            # Log the progress for the current generation
            self.logs.app_msg(f"Generation {generation + 1}/{generations}: Best Fitness = {best_fitness}")
            try:
                self.log_message(f"Generation {generation + 1}/{generations}: Best Fitness = {best_fitness}")
            except Exception as e:
                print(f"Error in logging: {e}")

            # Step 2: Selection - keep top 50% of the population
            selected_population = [population[i] for i in sorted(range(len(fitness_scores)), key=lambda i: fitness_scores[i], reverse=True)[:population_size // 2]]
            
            # Step 3: Crossover and mutation to create new patterns
            new_population = selected_population[:]
            while len(new_population) < population_size:
                parent1, parent2 = random.sample(selected_population, 2)  # Select two parents
                child = self.crossover(parent1, parent2)  # Create child pattern from parents
                self.mutate(child)  # Apply mutation to the child pattern
                new_population.append(child)
            
            # Update population for the next generation
            population = new_population

            # Update plot with the best fitness so far
            self.update_plot()

            # Refresh the plot display
            self.canvas.draw()

        # Step 4: Find the best pattern from the population and update the grid
        best_pattern = max(population, key=self.evaluate_fitness)  # Find the best pattern based on fitness
        
        # Log the completion of evolutionary process
        self.logs.app_msg("Evolution completed. Setting grid to the best pattern.")
        self.log_message("Evolution completed. Setting grid to the best pattern.")
        
        # Update the grid with the best pattern found
        for x in range(self.rows):
            for y in range(self.cols):
                self.grid[x][y] = best_pattern[x][y]  # Set the grid cells to the best pattern
        
        self.update_buttons()

    def generate_random_pattern(self):

        """Generates a random pattern for the grid."""
        return [[random.choice([0, 1]) for _ in range(self.cols)] for _ in range(self.rows)]

    def evaluate_fitness(self, pattern):
        """Evaluates the fitness of a pattern based on how many cells are alive after 10 generations."""
        
        # Set the grid to the given pattern
        self.grid = pattern
        
        # Simulate the grid for 10 generations
        for _ in range(10):
            self.update_grid()  # Update the grid based on Game of Life rules
        
        # Count the number of alive cells after 10 generations
        alive_cells = sum([sum(row) for row in self.grid])

        return alive_cells


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
        """Performs crossover between two patterns."""
        # Simple crossover logic: mix the first half of one parent and the second half of the other
        return [
            [parent1[x][y] if x < self.rows // 2 else parent2[x][y] for y in range(self.cols)]
            for x in range(self.rows)
        ]

    def mutate(self, pattern):
        """Mutates the given pattern by flipping a random cell."""
        x = random.randint(0, self.rows - 1)
        y = random.randint(0, self.cols - 1)
        pattern[x][y] = 1 - pattern[x][y]  # Flip the cell state                
                    
def main():
    app = QApplication(sys.argv)
    game = GameOfLife()
    game.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()