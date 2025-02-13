# API Stress Testing Tool

A powerful and configurable API stress testing tool built with Python, using HTTPX for efficient concurrent requests. This tool helps you evaluate API performance, reliability, and behavior under load by simulating multiple concurrent requests.

## Features

- Concurrent request execution using async/await
- Detailed request/response logging in JSONLINEs format
- Configurable request parameters (headers, query params, etc.)
- Connection pooling and timeout management
- Support for different HTTP methods
- Comprehensive metrics collection (response time, status codes, etc.)

## Installation

### Prerequisites

- Python 3.13 or higher
- Poetry (Python package manager)

### Installing Poetry

#### On macOS/Linux:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

#### On Windows:
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

After installation, make sure to add Poetry to your system's PATH:
- **Windows**: `%APPDATA%\Python\Scripts`
- **macOS/Linux**: `$HOME/.local/bin`

### Project Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Activate the virtual environment:
```bash
poetry shell
```

## Usage

### Basic Usage

```python
from main import run_stress_test

run_stress_test(
    url="https://api.example.com/endpoint",
    total_requests=100,
    concurrent_requests=10
)
```

### Advanced Configuration

```python
config = {
    "total_requests": 100,
    "concurrent_requests": 10,
    "headers": {
        "Authorization": "Bearer your-token",
        "Accept": "application/json"
    },
    "params": {
        "page": 1,
        "limit": 10
    },
    "method": "POST",
    "log_file": "logs/custom_test.jsonl",
    "timeout": 30.0
}

run_stress_test(
    url="https://api.example.com/endpoint",
    **config
)
```

### Configuration Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `url` | Target API endpoint URL | Required |
| `total_requests` | Total number of requests to make | 100 |
| `concurrent_requests` | Number of concurrent requests | 10 |
| `headers` | HTTP headers for requests | None |
| `params` | Query parameters for requests | None |
| `method` | HTTP method (GET, POST, etc.) | "GET" |
| `log_file` | Path to log file | "api_stress_test.jsonl" |
| `timeout` | Request timeout in seconds | 60.0 |

### Log File Format

The tool generates a JSONL (JSON Lines) file containing detailed information about each request:

```json
{
    "request_id": 1,
    "timestamp": "2024-01-01T12:00:00.000000",
    "url": "https://api.example.com/endpoint",
    "method": "GET",
    "headers": {},
    "params": {},
    "status_code": 200,
    "response_time_ms": 150.45,
    "success": true,
    "response_headers": {},
    "content_length": 1234,
    "response_body": {}
}
```

## Development

### Project Structure

```
.
├── main.py              # Main implementation
├── pyproject.toml       # Poetry configuration and dependencies
├── README.md           # Documentation
└── logs/               # Directory for log files
    └── api_stress_test.jsonl
```

### Running Tests

```bash
poetry run pytest
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
