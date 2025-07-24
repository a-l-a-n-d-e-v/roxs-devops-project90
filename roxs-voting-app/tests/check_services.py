#!/usr/bin/env python3
"""
Service Health Check Script

This script checks the health/status of all services defined in the docker-compose file
by making HTTP requests to their respective endpoints.
"""
import requests
import time
from typing import Dict, List, Tuple

# Service endpoints configuration
SERVICES = {
    'vote': {
        'url': 'http://localhost:80',
        'method': 'GET',
        'expected_status': 200
    },
    'result': {
        'url': 'http://localhost:3000/healthz',
        'method': 'GET',
        'expected_status': 200
    },
    'prometheus': {
        'url': 'http://localhost:9090',
        'method': 'GET',
        'expected_status': 200
    },
    'grafana': {
        'url': 'http://localhost:3001',
        'method': 'GET',
        'expected_status': 200
    },
}

def check_http_service(service_name: str, config: Dict) -> Tuple[bool, str]:
    """Check the status of an HTTP service."""
    try:
        response = requests.request(
            method=config['method'],
            url=config['url'],
            timeout=5
        )
        if response.status_code == config['expected_status']:
            return True, f"Status: {response.status_code}"
        return False, f"Unexpected status: {response.status_code}"
    except requests.RequestException as e:
        return False, f"Error: {str(e)}"

def check_all_services() -> Dict[str, Dict[str, str]]:
    """Check the status of all services."""
    results = {}
    
    for service_name, config in SERVICES.items():
        status = {
            'status': 'UNKNOWN',
            'message': 'Not checked',
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        try:
            is_ok, message = check_http_service(service_name, config)
            status['status'] = 'HEALTHY' if is_ok else 'UNHEALTHY'
            status['message'] = message
        except Exception as e:
            status['status'] = 'ERROR'
            status['message'] = f"Unexpected error: {str(e)}"
        
        results[service_name] = status
    
    return results

def print_results(results: Dict[str, Dict[str, str]]) -> None:
    """Print the results in a formatted way."""
    print("\n" + "="*60)
    print("SERVICE STATUS CHECK")
    print("="*60)
    print(f"{'Service':<15} | {'Status':<15} | Message")
    print("-"*60)
    
    for service, data in results.items():
        status = data['status']
        # Add color to status
        if status in ['HEALTHY', 'RUNNING']:
            status = f"\033[92m{status}\033[0m"  # Green
        elif status in ['UNHEALTHY', 'DOWN']:
            status = f"\033[91m{status}\033[0m"  # Red
        else:
            status = f"\033[93m{status}\033[0m"  # Yellow
            
        print(f"{service:<15} | {status:<15} | {data['message']}")
    
    print("\nLast checked:", time.strftime('%Y-%m-%d %H:%M:%S'))
    print("="*60 + "\n")

if __name__ == "__main__":
    print("Checking service statuses...")
    results = check_all_services()
    print_results(results)
    # Exit with non-zero code if any service is not healthy
    if any(
        status['status'] in ['UNHEALTHY', 'DOWN', 'ERROR'] 
        for status in results.values()
    ):
        exit(1)
    exit(0)
