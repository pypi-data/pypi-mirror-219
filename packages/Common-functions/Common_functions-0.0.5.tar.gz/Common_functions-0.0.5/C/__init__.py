import ctypes
import os
root=os.path.dirname(__file__)
# Load the shared libraries
fib_lib = ctypes.CDLL(os.path.join(root,'fibonacci.so'))
reverse_decimal_lib = ctypes.CDLL(os.path.join(root,'reverse_decimal.so'))
binary_to_decimal_lib = ctypes.CDLL(os.path.join(root,'binary_to_decimal.so'))
sin_x_lib = ctypes.CDLL(os.path.join(root,'sin_x.so'))
cos_x_lib = ctypes.CDLL(os.path.join(root,'cos_x.so'))
gcd_lib = ctypes.CDLL(os.path.join(root,'gcd.so'))
calculate_e_lib = ctypes.CDLL(os.path.join(root,'calculate_e.so'))
generate_primes_lib = ctypes.CDLL(os.path.join(root,'generate_primes.so'))
square_root_lib = ctypes.CDLL(os.path.join(root,'square_root.so'))
char_to_ascii_lib = ctypes.CDLL(os.path.join(root,'char_to_ascii.so'))
partition_array_lib = ctypes.CDLL(os.path.join(root,'partition_array.so'))
remove_duplicates_lib = ctypes.CDLL(os.path.join(root,'remove_duplicates.so'))
count_duplicates_lib = ctypes.CDLL(os.path.join(root,'count_duplicates.so'))
prime_factors_lib = ctypes.CDLL(os.path.join(root,'prime_factors.so'))
reverse_array_lib = ctypes.CDLL(os.path.join(root,'reverse_array.so'))
kth_smallest_lib = ctypes.CDLL(os.path.join(root,'kth_smallest.so'))
merge_sort_lib = ctypes.CDLL(os.path.join(root,'merge_sort.so'))
bubble_sort_lib = ctypes.CDLL(os.path.join(root,'bubble_sort.so'))
selection_sort_lib = ctypes.CDLL(os.path.join(root,'selection_sort.so'))
binary_search_lib = ctypes.CDLL(os.path.join(root,'binary_search.so'))

# Define function prototypes
fibonacci = fib_lib.fibonacci
fibonacci.argtypes = [ctypes.c_int]
fibonacci.restype = ctypes.c_int

reverse_decimal = reverse_decimal_lib.reverseDecimal
reverse_decimal.argtypes = [ctypes.c_int]
reverse_decimal.restype = ctypes.c_int

binary_to_decimal = binary_to_decimal_lib.binaryToDecimal
binary_to_decimal.argtypes = [ctypes.c_int]
binary_to_decimal.restype = ctypes.c_int

sin_x = sin_x_lib.calculateSin
sin_x.argtypes = [ctypes.c_double]
sin_x.restype = ctypes.c_double

cos_x = cos_x_lib.calculateCos
cos_x.argtypes = [ctypes.c_double]
cos_x.restype = ctypes.c_double

gcd = gcd_lib.calculateGCD
gcd.argtypes = [ctypes.c_int, ctypes.c_int]
gcd.restype = ctypes.c_int

calculate_e = calculate_e_lib.calculateE
calculate_e.restype = ctypes.c_double

generate_primes = generate_primes_lib.generatePrimes
generate_primes.argtypes = [ctypes.c_int]

square_root = square_root_lib.squareRoot
square_root.argtypes = [ctypes.c_double]
square_root.restype = ctypes.c_double

char_to_ascii = char_to_ascii_lib.charToAscii
char_to_ascii.argtypes = [ctypes.c_char]
char_to_ascii.restype = ctypes.c_int

partition_array = partition_array_lib.partitionArray
partition_array.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_int]
partition_array.restype = ctypes.c_int

remove_duplicates = remove_duplicates_lib.removeDuplicates
remove_duplicates.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]
remove_duplicates.restype = ctypes.c_int

count_duplicates = count_duplicates_lib.countDuplicates
count_duplicates.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]
count_duplicates.restype = ctypes.c_int

prime_factors = prime_factors_lib.calculatePrimeFactors
prime_factors.argtypes = [ctypes.c_int]

reverse_array = reverse_array_lib.reverseArray
reverse_array.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]

kth_smallest = kth_smallest_lib.findKthSmallest
kth_smallest.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_int]
kth_smallest.restype = ctypes.c_int

merge_sort = merge_sort_lib.mergeSort
merge_sort.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]

bubble_sort = bubble_sort_lib.bubbleSort
bubble_sort.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]

selection_sort = selection_sort_lib.selectionSort
selection_sort.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]

binary_search = binary_search_lib.binarySearch
binary_search.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_int]
binary_search.restype = ctypes.c_int


# Fibonacci
def get_fibonacci(n):
    return fibonacci(n)


# Reverse Decimal
def get_reverse_decimal(num):
    return reverse_decimal(num)


# Binary to Decimal
def get_binary_to_decimal(binary):
    return binary_to_decimal(binary)


# Sin(x)
def calculate_sin(x):
    return sin_x(x)


# Cos(x)
def calculate_cos(x):
    return cos_x(x)


# GCD
def calculate_gcd(a, b):
    return gcd(a, b)


# Calculate e
def calculate_e():
    return calculate_e()


# Generate Primes
def get_prime_numbers(n):
    primes = (ctypes.c_int * n)()
    generate_primes(primes, n)
    return list(primes)


# Square Root
def get_square_root(num):
    return square_root(num)


# Char to ASCII
def get_ascii_code(char):
    return char_to_ascii(char)


# Partition Array
def partition_array(arr, low, high):
    size = len(arr)
    c_arr = (ctypes.c_int * size)(*arr)
    return partition_array(c_arr, low, high)


# Remove Duplicates
def remove_duplicates(arr):
    size = len(arr)
    c_arr = (ctypes.c_int * size)(*arr)
    new_size = remove_duplicates(c_arr, size)
    return list(c_arr[:new_size])


# Count Duplicates
def count_duplicates(arr):
    size = len(arr)
    c_arr = (ctypes.c_int * size)(*arr)
    return count_duplicates(c_arr, size)


# Prime Factors
def get_prime_factors(num):
    prime_factors_arr = (ctypes.c_int * num)()
    prime_factors(num, prime_factors_arr)
    return list(prime_factors_arr)


# Reverse Array
def reverse_array(arr):
    size = len(arr)
    c_arr = (ctypes.c_int * size)(*arr)
    reverse_array(c_arr, size)
    return list(c_arr)


# Kth Smallest
def get_kth_smallest(arr, k):
    size = len(arr)
    c_arr = (ctypes.c_int * size)(*arr)
    return kth_smallest(c_arr, size, k)


# Merge Sort
def merge_sort_array(arr):
    size = len(arr)
    c_arr = (ctypes.c_int * size)(*arr)
    merge_sort(c_arr, size)
    return list(c_arr)


# Bubble Sort
def bubble_sort_array(arr):
    size = len(arr)
    c_arr = (ctypes.c_int * size)(*arr)
    bubble_sort(c_arr, size)
    return list(c_arr)


# Selection Sort
def selection_sort_array(arr):
    size = len(arr)
    c_arr = (ctypes.c_int * size)(*arr)
    selection_sort(c_arr, size)
    return list(c_arr)


# Binary Search
def binary_search_array(arr, target):
    size = len(arr)
    c_arr = (ctypes.c_int * size)(*arr)
    return binary_search(c_arr, size, target)


