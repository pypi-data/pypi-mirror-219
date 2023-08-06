import subprocess
import os

root=os.path.dirname(__file__)
os.chdir(root)
def factorial_of_numbers(numbers):
    result = subprocess.run(["java", "FactorialOfNumbers",str(numbers)]  , capture_output=True, text=True)
    print(result.stdout if result.stdout else result.stderr)


def prime_series(n):
    result = subprocess.run(["java", "PrimeSeries", str(n)], capture_output=True, text=True)
    print(result.stdout if result.stdout else result.stderr)

def rhombus_pattern():
    subprocess.run(["java", "RhombusPattern"])

def string_operations():
    subprocess.run(["java", "StringOperations"])

def average_of_numbers(numbers):
    result = subprocess.run(["java", "AverageOfNumbers"] + numbers, capture_output=True, text=True)
    print(result.stdout if result.stdout else result.stderr)

def distance_between_points(points):
    result = subprocess.run(["java", "DistanceBetweenPoints"] + points, capture_output=True, text=True)
    print(result.stdout if result.stdout else result.stderr)

def average_marks(marks):
    result = subprocess.run(["java", "AverageMarks"] + marks, capture_output=True, text=True)
    print(result.stdout if result.stdout else result.stderr)

def sum_of_numbers(numbers):
    result = subprocess.run(["java", "SumOfNumbers"] + numbers, capture_output=True, text=True)
    print(result.stdout if result.stdout else result.stderr)

def linear_search(numbers, target):
    result = subprocess.run(["java", "LinearSearch"] + numbers, capture_output=True, text=True, input=target)
    print(result.stdout if result.stdout else result.stderr)

def mouse_events():
    subprocess.run(["java", "MouseEvents"])

