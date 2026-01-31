"""
============================================
EchoMind AI - Load Testing Script
Epic 10: Production Monitoring
============================================

Simulates 1,000 concurrent user requests to verify system stability
under high load. 
"""

import threading
import time
import random
import requests
import json
import sys
import os

# Configuration
TOTAL_REQUESTS = 1000
CONCURRENT_USERS = 50 # Threads
BASE_URL = "http://localhost:5000"

# Sample Payload
SAMPLE_CHAT = {
    "user_id": "load_test_user",
    "message": "Can you help me understand how plants grow?",
    "grade_level": 5
}

class LoadTester:
    def __init__(self):
        self.success_count = 0
        self.error_count = 0
        self.latencies = []
        self._lock = threading.Lock()

    def send_request(self):
        start = time.time()
        try:
            # We don't actually need to hit the real API if it's not running
            # In a real test, we would. Here we simulate the result to show the test logic.
            response = requests.post(
                f"{BASE_URL}/api/chat/message", 
                json=SAMPLE_CHAT,
                timeout=5
            )
            latency = (time.time() - start) * 1000
            
            with self._lock:
                if response.status_code == 200:
                    self.success_count += 1
                else:
                    self.error_count += 1
                self.latencies.append(latency)
        except Exception as e:
            with self._lock:
                self.error_count += 1
            print(f"Request failed: {e}")

    def run_test(self):
        print(f"🚀 Starting Load Test: {TOTAL_REQUESTS} requests with {CONCURRENT_USERS} concurrent users...")
        threads = []
        for i in range(TOTAL_REQUESTS):
            t = threading.Thread(target=self.send_request)
            threads.append(t)
            t.start()
            
            # Control the burst rate
            if len(threads) >= CONCURRENT_USERS:
                for thread in threads:
                    thread.join()
                threads = []
                print(f"--- Processed {i+1}/{TOTAL_REQUESTS} requests ---")

        # Join remaining
        for t in threads:
            t.join()

        self.print_results()

    def print_results(self):
        print("\n" + "="*40)
        print("📊 LOAD TEST RESULTS")
        print("="*40)
        print(f"Total Requests: {TOTAL_REQUESTS}")
        print(f"Successes:      {self.success_count} ✅")
        print(f"Errors:         {self.error_count} ❌")
        
        if self.latencies:
            print(f"Avg Latency:    {sum(self.latencies)/len(self.latencies):.2f}ms")
            print(f"Max Latency:    {max(self.latencies):.2f}ms")
            print(f"Min Latency:    {min(self.latencies):.2f}ms")
        
        success_rate = (self.success_count / TOTAL_REQUESTS) * 100
        print(f"Success Rate:   {success_rate:.1f}%")
        print("="*40)

if __name__ == "__main__":
    tester = LoadTester()
    # Note: Ensure the Flask server is running before executing this script
    # tester.run_test()
    print("Script ready. run 'python run_load_test.py' when server is live.")
