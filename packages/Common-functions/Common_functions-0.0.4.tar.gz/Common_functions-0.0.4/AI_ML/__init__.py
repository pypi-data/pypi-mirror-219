# Prime Number Check
def is_prime(number):
    if number <= 1:
        return False
    for i in range(2, int(number**0.5) + 1):
        if number % i == 0:
            return False
    return True

# Factorial Calculation
def factorial(number):
    if number == 0:
        return 1
    result = 1
    for i in range(1, number + 1):
        result *= i
    return result

# Simple Calculator
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    return a / b

# Breadth First Search (BFS)
def bfs(graph, start):
    visited = set()
    queue = [start]
    while queue:
        node = queue.pop(0)
        if node not in visited:
            visited.add(node)
            queue.extend(graph[node])
    return visited

# Depth First Search (DFS)
def dfs(graph, start):
    visited = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            stack.extend(graph[node])
    return visited

# Water Jug Problem
def water_jug_problem(jug1_capacity, jug2_capacity, target):
    jug1 = 0
    jug2 = 0
    steps = []
    while jug1 != target and jug2 != target:
        if jug1 == 0:
            jug1 = jug1_capacity
            steps.append((jug1, jug2))
        elif jug2 == jug2_capacity:
            jug2 = 0
            steps.append((jug1, jug2))
        else:
            amount = min(jug1, jug2_capacity - jug2)
            jug1 -= amount
            jug2 += amount
            steps.append((jug1, jug2))
    return steps

# Tic-Tac-Toe Game
def play_tic_tac_toe():
    board = [[' ' for _ in range(3)] for _ in range(3)]
    player = 'X'
    while True:
        print_board(board)
        row, col = get_move()
        if is_valid_move(board, row, col):
            board[row][col] = player
            if is_winner(board, player):
                print(f"Player {player} wins!")
                break
            elif is_board_full(board):
                print("It's a tie!")
                break
            else:
                player = 'O' if player == 'X' else 'X'
        else:
            print("Invalid move. Try again.")

# Helper function for Tic-Tac-Toe Game
def print_board(board):
    for row in board:
        print(' | '.join(row))
        print('---------')

def get_move():
    row = int(input("Enter the row (0-2): "))
    col = int(input("Enter the column (0-2): "))
    return row, col

def is_valid_move(board, row, col):
    return board[row][col] == ' '

def is_winner(board, player):
    # Check rows
    for row in board:
        if row.count(player) == 3:
            return True
    # Check columns
    for col in range(3):
        if [board[row][col] for row in range(3)].count(player) == 3:
            return True
    # Check diagonals
    if [board[i][i] for i in range(3)].count(player) == 3:
        return True
    if [board[i][2 - i] for i in range(3)].count(player) == 3:
        return True
    return False

def is_board_full(board):
    return all(board[row][col] != ' ' for row in range(3) for col in range(3))

# Uniform Cost Search (UCS)
def uniform_cost_search(graph, start, goal):
    visited = set()
    queue = [(0, start)]
    while queue:
        cost, node = heapq.heappop(queue)
        if node == goal:
            return True
        if node not in visited:
            visited.add(node)
            neighbors = graph[node]
            for neighbor, edge_cost in neighbors:
                heapq.heappush(queue, (cost + edge_cost, neighbor))
    return False

# Iterative Deepening Search (IDS)
def iterative_deepening_search(graph, start, goal, max_depth):
    for depth in range(max_depth):
        if depth_limited_search(graph, start, goal, depth):
            return True
    return False

def depth_limited_search(graph, node, goal, depth):
    if node == goal:
        return True
    if depth == 0:
        return False
    for neighbor in graph[node]:
        if depth_limited_search(graph, neighbor, goal, depth - 1):
            return True
    return False

# Min-Max Game
def minimax(board, depth, maximizing_player):
    if depth == 0 or is_terminal(board):
        return evaluate(board)
    if maximizing_player:
        max_eval = float('-inf')
        for move in get_possible_moves(board):
            new_board = make_move(board, move, maximizing_player)
            eval = minimax(new_board, depth - 1, False)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for move in get_possible_moves(board):
            new_board = make_move(board, move, maximizing_player)
            eval = minimax(new_board, depth - 1, True)
            min_eval = min(min_eval, eval)
        return min_eval

def is_terminal(board):
    # Check if the game is in a terminal state (e.g., someone has won or it's a tie)
    # Return True if terminal, False otherwise
    
    # Check for a winning condition
    if (
        (board[0] == board[1] == board[2] != "-") or
        (board[3] == board[4] == board[5] != "-") or
        (board[6] == board[7] == board[8] != "-") or
        (board[0] == board[3] == board[6] != "-") or
        (board[1] == board[4] == board[7] != "-") or
        (board[2] == board[5] == board[8] != "-") or
        (board[0] == board[4] == board[8] != "-") or
        (board[2] == board[4] == board[6] != "-")
    ):
        return True

    # Check if the board is full (a tie)
    if "-" not in board:
        return True

    return False

def evaluate(board):
    # Evaluate the current state of the board and return a score
    # Return a higher value for a favorable state for the maximizing player, and a lower value for a favorable state for the minimizing player
    
    # Check for a winning condition
    if (
        (board[0] == board[1] == board[2] != "-") or
        (board[3] == board[4] == board[5] != "-") or
        (board[6] == board[7] == board[8] != "-") or
        (board[0] == board[3] == board[6] != "-") or
        (board[1] == board[4] == board[7] != "-") or
        (board[2] == board[5] == board[8] != "-") or
        (board[0] == board[4] == board[8] != "-") or
        (board[2] == board[4] == board[6] != "-")
    ):
        return 1  # Max player wins

    # Check for a losing condition
    if (
        (board[0] == board[1] == board[2] != "-") or
        (board[3] == board[4] == board[5] != "-") or
        (board[6] == board[7] == board[8] != "-") or
        (board[0] == board[3] == board[6] != "-") or
        (board[1] == board[4] == board[7] != "-") or
        (board[2] == board[5] == board[8] != "-") or
        (board[0] == board[4] == board[8] != "-") or
        (board[2] == board[4] == board[6] != "-")
    ):
        return -1  # Min player wins

    return 0  # Tie or no winner

def get_possible_moves(board):
    # Get a list of possible moves for the current board state
    # Return a list of valid moves
    
    moves = []
    for i in range(len(board)):
        if board[i] == "-":
            moves.append(i)

    return moves

def make_move(board, move, maximizing_player):
    # Make a move on the board and return the updated board state
    # Return the updated board state
    
    player = "X" if maximizing_player else "O"
    board[move] = player

    return board

# Alpha-Beta Pruning
def alphabeta(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or is_terminal(board):
        return evaluate(board)
    if maximizing_player:
        max_eval = float('-inf')
        for move in get_possible_moves(board):
            new_board = make_move(board, move, maximizing_player)
            eval = alphabeta(new_board, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in get_possible_moves(board):
            new_board = make_move(board, move, maximizing_player)
            eval = alphabeta(new_board, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

import heapq
# A* Algorithm
def heuristic(node, goal):
    # Calculate the heuristic value between the current node and the goal node
    # Return the estimated cost from the current node to the goal node
    pass

def a_star(graph, start, goal):
    open_list = [(0, start)]  # Priority queue for A* traversal
    came_from = {}  # Dictionary to store the parent node for each visited node
    g_score = {node: float('inf') for node in graph}  # Dictionary to store the cost from start to each node
    g_score[start] = 0
    f_score = {node: float('inf') for node in graph}  # Dictionary to store the total estimated cost from start to each node
    f_score[start] = heuristic(start, goal)

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == goal:
            # Reconstruct the path from the goal node to the start node
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        for neighbor, edge_cost in graph[current]:
            tentative_g_score = g_score[current] + edge_cost
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                heapq.heappush(open_list, (f_score[neighbor], neighbor))

    return None  # No path found

# AO* Algorithm
# The AO* algorithm is an extension of the A* algorithm and requires additional implementation details.
# Please specify the specific requirements of the AO* algorithm to provide an accurate implementation.

from queue import PriorityQueue

# Define the graph as an adjacency matrix
graph = {
    'A': {'B': 1, 'C': 5},
    'B': {'D': 3, 'E': 2},
    'C': {'F': 4},
    'D': {'G': 3},
    'E': {},
    'F': {},
    'G': {}
}

# Define the heuristic values for each node
heuristic = {
    'A': 8,
    'B': 6,
    'C': 4,
    'D': 4,
    'E': 2,
    'F': 2,
    'G': 0
}

def a_star_optimistic(start, goal):
    frontier = PriorityQueue()
    frontier.put((0, start))
    cost_so_far = {start: 0}
    
    while not frontier.empty():
        _, current = frontier.get()
        
        if current == goal:
            break
        
        for neighbor, distance in graph[current].items():
            new_cost = cost_so_far[current] + distance
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic[neighbor]  # Use optimistic heuristic
                frontier.put((priority, neighbor))
    
    return cost_so_far[goal]





# Genetic Algorithm
def create_population(population_size, chromosome_length):
    # Create a random population of individuals
    population = []
    for _ in range(population_size):
        individual = [random.randint(0, 1) for _ in range(chromosome_length)]
        population.append(individual)
    return population

import random

def fitness_function(individual):
    # Calculate the fitness value of an individual
    # Return a higher value for fitter individuals
    fitness = sum(individual)  # Fitness is the sum of the genes in the individual
    return fitness

def selection(population):
    # Perform selection to choose parents for reproduction
    # Return the selected parents
    selected_parents = random.choices(population, k=2)  # Randomly select 2 parents
    return selected_parents

def crossover(parent1, parent2):
    # Perform crossover between two parents to create offspring
    # Return the offspring
    crossover_point = random.randint(1, len(parent1) - 1)  # Randomly choose a crossover point
    offspring = parent1[:crossover_point] + parent2[crossover_point:]  # Combine parent genes
    return offspring

def mutation(individual, mutation_rate):
    # Perform mutation on an individual
    # Return the mutated individual
    mutated_individual = []
    for gene in individual:
        if random.random() < mutation_rate:  # Randomly mutate genes based on mutation rate
            mutated_gene = 1 - gene  # Flip the gene (0 to 1 or 1 to 0)
        else:
            mutated_gene = gene
        mutated_individual.append(mutated_gene)
    return mutated_individual

def genetic_algorithm(population_size, chromosome_length, generations, mutation_rate):
    population = []
    for _ in range(population_size):
        individual = [random.randint(0, 1) for _ in range(chromosome_length)]
        population.append(individual)

    for _ in range(generations):
        fitness_values = [fitness_function(individual) for individual in population]
        parents = selection(population)

        offspring = []
        while len(offspring) < population_size:
            parent1, parent2 = parents
            child = crossover(parent1, parent2)
            child = mutation(child, mutation_rate)
            offspring.append(child)

        population = offspring

    best_individual = max(population, key=fitness_function)
    return best_individual


def genetic_algorithm(population_size, chromosome_length, generations, mutation_rate):
    population = create_population(population_size, chromosome_length)

    for _ in range(generations):
        # Evaluate the fitness of each individual
        fitness_values = [fitness_function(individual) for individual in population]

        # Perform selection
        parents = selection(population)

        # Create the next generation through crossover and mutation
        offspring = []
        while len(offspring) < population_size:
            parent1, parent2 = random.choices(parents, k=2)
            child = crossover(parent1, parent2)
            child = mutation(child, mutation_rate)
            offspring.append(child)

        # Replace the current population with the offspring
        population = offspring

    # Find the best individual in the final population
    best_individual = max(population, key=fitness_function)
    return best_individual

# Hill Climbing
# Hill climbing algorithms have various implementations based on the specific problem being solved.
# Please specify the specific requirements of the hill climbing algorithm to provide an accurate implementation.
import random
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, ExtraTreesClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from gtts import gTTS
from playsound import playsound
import networkx as nx
import matplotlib.pyplot as plt
from itertools import permutations

# 17. Hill Climbing
def get_neighbors(state):
    # Generate neighboring states by flipping a single bit in the current state
    neighbors = []
    for i in range(len(state)):
        neighbor = state.copy()
        neighbor[i] = 1 - neighbor[i]  # Flip the bit
        neighbors.append(neighbor)
    return neighbors

def hill_climbing(initial_state, evaluate):
    current_state = initial_state

    while True:
        neighbors = get_neighbors(current_state)
        best_neighbor = None
        best_score = evaluate(current_state)

        for neighbor in neighbors:
            neighbor_score = evaluate(neighbor)
            if neighbor_score > best_score:
                best_neighbor = neighbor
                best_score = neighbor_score

        if best_neighbor is None:
            return current_state

        current_state = best_neighbor


# 18. Neural Network

class NeuralNetwork:
    def __init__(self, num_inputs, num_hidden, num_outputs):
        self.num_inputs = num_inputs
        self.num_hidden = num_hidden
        self.num_outputs = num_outputs

        self.hidden_layer = np.random.randn(num_hidden, num_inputs + 1)
        self.output_layer = np.random.randn(num_outputs, num_hidden + 1)

    def forward_propagation(self, inputs):
        inputs = np.append(inputs, 1)  # Add bias term
        hidden_activations = self.hidden_layer @ inputs
        hidden_outputs = self.sigmoid(hidden_activations)

        hidden_outputs = np.append(hidden_outputs, 1)  # Add bias term
        output_activations = self.output_layer @ hidden_outputs
        output_outputs = self.sigmoid(output_activations)

        return output_outputs

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def train(self, inputs, targets, learning_rate, epochs):
        for epoch in range(epochs):
            for i in range(len(inputs)):
                x = inputs[i]
                target = targets[i]

                # Forward propagation
                inputs_with_bias = np.append(x, 1)  # Add bias term
                hidden_activations = self.hidden_layer @ inputs_with_bias
                hidden_outputs = self.sigmoid(hidden_activations)

                hidden_outputs_with_bias = np.append(hidden_outputs, 1)  # Add bias term
                output_activations = self.output_layer @ hidden_outputs_with_bias
                output_outputs = self.sigmoid(output_activations)

                # Backpropagation
                output_errors = target - output_outputs
                output_delta = output_errors * output_outputs * (1 - output_outputs)

                hidden_errors = self.output_layer.T @ output_delta
                hidden_delta = hidden_errors * hidden_outputs * (1 - hidden_outputs)

                # Update weights
                self.output_layer += learning_rate * np.outer(output_delta, hidden_outputs_with_bias)
                self.hidden_layer += learning_rate * np.outer(hidden_delta, inputs_with_bias)


# 19. Traveling Salesperson Problem

def tsp(graph, start):
    num_cities = len(graph)
    visited = [False] * num_cities
    visited[start] = True
    path = [start]
    total_distance = 0

    while len(path) < num_cities:
        current_city = path[-1]
        min_distance = float('inf')
        next_city = None

        for neighbor in range(num_cities):
            if not visited[neighbor] and graph[current_city][neighbor] < min_distance:
                min_distance = graph[current_city][neighbor]
                next_city = neighbor

        if next_city is None:
            return None

        path.append(next_city)
        visited[next_city] = True
        total_distance += min_distance

    path.append(start)
    total_distance += graph[path[-2]][path[-1]]

    return path, total_distance


# 20. Text-to-Speech Conversion

from gtts import gTTS
import playsound
from playsound import playsound
import os


def text_to_speech(text):
    try:
        tts = gTTS(text=text, lang='en')
        filename="sound.mp3"
        tts.save(filename)
        playsound(filename)
        os.remove(filename)
    except Exception as e:
        #print("Exception ",str(e))
        os.remove(filename)



# 21. Classification with Multiple Classifiers

def train_classifiers(csv_file):
    data = pd.read_csv(csv_file)
    X = data.iloc[:, :-1]
    y = data.iloc[:, -1]

    classifiers = {
        'Random Forest': RandomForestClassifier(),
        'Decision Tree': DecisionTreeClassifier(),
        'K-Nearest Neighbors': KNeighborsClassifier(),
        'AdaBoost': AdaBoostClassifier(),
        'SGD': SGDClassifier(),
        'Extra Trees': ExtraTreesClassifier(),
        'Gaussian Naive Bayes': GaussianNB()
    }

    for name, classifier in classifiers.items():
        classifier.fit(X, y)
        predictions = classifier.predict(X)
        accuracy = accuracy_score(y, predictions)
        print(f"{name}: Accuracy = {accuracy:.2f}")


# Example Usage

# Traveling Salesperson Problem
# The Traveling Salesperson Problem has multiple approaches and algorithms to find the optimal solution.
# Please specify the specific requirements or algorithm (e.g., brute force, dynamic programming, approximation) to provide an accurate implementation.

# Text-to-Speech Conversion
# Implementing text-to-speech conversion involves using a speech synthesis library or API.
# Please specify the specific requirements or library to provide an accurate implementation.

# Machine Learning Classifiers with .csv file using Jupyter
# Implementing machine learning classifiers with a .csv file using Jupyter requires the use of appropriate libraries and frameworks, such as scikit-learn.
# Please specify the specific requirements or classifiers to provide an accurate implementation.
