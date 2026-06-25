def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n-1)

SERVER_PORT = 8080
DEBUG_MODE = True
