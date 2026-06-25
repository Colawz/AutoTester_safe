function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n-1) + fibonacci(n-2);
}

const SERVER_PORT = 8080;
const DEBUG_MODE = true;

module.exports = { fibonacci, SERVER_PORT, DEBUG_MODE };
