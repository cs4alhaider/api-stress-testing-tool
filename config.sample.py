def get_config():
    return {
        "total_requests": 100,  # Total number of requests to make
        "concurrent_requests": 10,  # Number of concurrent requests
        "headers": {
            "User-Agent": "API-Stress-Tester/1.0",
            "Accept": "application/json"
        },
        "params": {
            # Add any query parameters here
            # "page": 1,
            # "limit": 10
        },
        "method": "GET",
        "log_file": "logs/api_stress_test.jsonl",
        "timeout": 30.0  # Timeout in seconds
    }