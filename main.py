import httpx
import asyncio
import json
import time
from datetime import datetime
from typing import Any
import logging
from pathlib import Path

class APIStressTester:
    """
    A class for performing stress testing on APIs by making concurrent HTTP requests.
    
    This class allows you to test an API endpoint by sending multiple requests concurrently
    and collecting detailed metrics about the responses including status codes, response times,
    and any errors encountered.
    """

    def __init__(
        self,
        base_url: str,
        total_requests: int = 100,
        concurrent_requests: int = 10,
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
        method: str = "GET",
        log_file: str = "api_stress_test.jsonl",
        timeout: float = 60.0
    ):
        """
        Initialize the API stress tester.

        Args:
            base_url (str): The target API endpoint URL
            total_requests (int): Total number of requests to make
            concurrent_requests (int): Number of requests to make concurrently
            headers (dict): Optional HTTP headers to include with each request
            params (dict): Optional query parameters to include with each request
            method (str): HTTP method to use (GET, POST, etc.)
            log_file (str): Path to the log file where results will be stored
            timeout (float): Request timeout in seconds
        """
        self.base_url = base_url
        self.total_requests = total_requests
        self.concurrent_requests = concurrent_requests
        self.headers = headers or {}
        self.params = params or {}
        self.method = method.upper()
        self.log_file = log_file
        self.timeout = timeout
        self.results = []

    async def make_request(self, client: httpx.AsyncClient, request_id: int) -> dict[str, Any]:
        """
        Make a single HTTP request and record the results.

        Args:
            client (httpx.AsyncClient): The HTTP client to use for making requests
            request_id (int): Unique identifier for this request

        Returns:
            dict: A dictionary containing detailed information about the request and response
        """
        start_time = time.time()
        result = {
            "request_id": request_id,
            "timestamp": datetime.now().isoformat(),
            "url": self.base_url,
            "method": self.method,
            "headers": self.headers,
            "params": self.params,
        }

        try:
            # Make the HTTP request
            response = await client.request(
                method=self.method,
                url=self.base_url,
                headers=self.headers,
                params=self.params,
            )
            end_time = time.time()
            response_time = (end_time - start_time) * 1000  # Convert to milliseconds

            # Record successful response details
            result.update({
                "status_code": response.status_code,
                "response_time_ms": round(response_time, 2),
                "success": 200 <= response.status_code < 300,
                "response_headers": dict(response.headers),
                "content_length": len(response.content),
            })

            # Try to parse response as JSON, fall back to text if not possible
            try:
                result["response_body"] = response.json()
            except:
                result["response_body"] = response.text

        except Exception as e:
            # Record error details if request fails
            end_time = time.time()
            response_time = (end_time - start_time) * 1000
            result.update({
                "status_code": None,
                "response_time_ms": round(response_time, 2),
                "success": False,
                "error": str(e),
            })

        self._log_result(result)
        return result

    def _log_result(self, result: dict[str, Any]):
        """
        Log a single request result to the log file in JSONL format.

        Args:
            result (dict): The request result to log
        """
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(result) + '\n')

    async def run(self):
        """
        Execute the stress test by running multiple concurrent requests.
        
        This method creates a connection pool and manages concurrent requests
        according to the specified parameters.
        """
        # Configure connection pooling limits
        limits = httpx.Limits(max_keepalive_connections=self.concurrent_requests, max_connections=self.concurrent_requests)
        async with httpx.AsyncClient(timeout=self.timeout, limits=limits) as client:
            tasks = []
            for i in range(self.total_requests):
                task = asyncio.create_task(self.make_request(client, i + 1))
                tasks.append(task)
                
                # Execute batch of concurrent requests
                if len(tasks) >= self.concurrent_requests:
                    await asyncio.gather(*tasks)
                    tasks = []
            
            # Execute any remaining tasks
            if tasks:
                await asyncio.gather(*tasks)

def run_stress_test(
    url: str,
    total_requests: int = 100,
    concurrent_requests: int = 10,
    headers: dict[str, str] | None = None,
    params: dict[str, Any] | None = None,
    method: str = "GET",
    log_file: str = "api_stress_test.jsonl",
    timeout: float = 60.0
):
    """
    Convenience function to run an API stress test.

    Args:
        url (str): The target API endpoint URL
        total_requests (int): Total number of requests to make
        concurrent_requests (int): Number of requests to make concurrently
        headers (dict): Optional HTTP headers to include with each request
        params (dict): Optional query parameters to include with each request
        method (str): HTTP method to use (GET, POST, etc.)
        log_file (str): Path to the log file where results will be stored
        timeout (float): Request timeout in seconds
    """
    # Create log file directory if it doesn't exist
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    
    # Clear previous log file
    with open(log_file, 'w') as f:
        pass

    # Initialize and run the stress tester
    tester = APIStressTester(
        base_url=url,
        total_requests=total_requests,
        concurrent_requests=concurrent_requests,
        headers=headers,
        params=params,
        method=method,
        log_file=log_file,
        timeout=timeout
    )

    asyncio.run(tester.run())

if __name__ == "__main__":
    # Example usage
    api_url = "https://jsonplaceholder.typicode.com/todos"
    
    # Example configuration
    config = {
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

    # Run the stress test with the specified configuration
    run_stress_test(
        url=api_url,
        **config
    )
