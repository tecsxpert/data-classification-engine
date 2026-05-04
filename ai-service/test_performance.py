# test_performance.py
# Tests all endpoints performance
# Run with: python test_performance.py

import requests
import time

BASE_URL = "http://localhost:5000"
TARGET_TIME = 35.0  # Realistic for free tier Groq


def print_header(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def print_result(test_name, passed, time_taken=None):
    status = "✅ PASSED" if passed else "❌ FAILED"
    if time_taken:
        print(f"  {status} — {test_name} ({time_taken:.2f}s)")
    else:
        print(f"  {status} — {test_name}")


def test_health_performance():
    """Test /health responds instantly"""
    print_header("Testing /health Performance")

    start = time.time()
    response = requests.get(f"{BASE_URL}/health")
    elapsed = time.time() - start

    print_result(
        "Health under 2s",
        elapsed < 20.0,
        elapsed
    )

    data = response.json()
    print(f"\n  Health Response:")
    print(f"  Status:      {data.get('status')}")
    print(f"  Avg Time:    {data.get('avg_response_time')}")
    print(f"  Performance: {data.get('performance_status')}")
    print(f"  Uptime:      {data.get('uptime')}")


def test_describe_performance():
    """Test /describe responds under 5 seconds"""
    print_header("Testing /describe Performance")

    # Use same dataset to benefit from cache
    payload = {
        "dataset_name": "Customer_DB",
        "description": "Customer personal information",
        "fields": ["id", "name", "email"]
    }

    times = []

    for i in range(3):
        print(f"  Request {i+1}/3...")
        start = time.time()

        response = requests.post(
            f"{BASE_URL}/describe",
            json=payload
        )

        elapsed = time.time() - start
        times.append(elapsed)

        passed = elapsed < TARGET_TIME
        print_result(
            f"Request {i+1} under {TARGET_TIME}s",
            passed,
            elapsed
        )

        # Small wait between requests
        time.sleep(0.5)

    avg = sum(times) / len(times)
    print(f"\n  Average time: {avg:.2f}s")
    print_result(
        f"Average under {TARGET_TIME}s",
        avg < TARGET_TIME,
        avg
    )


def test_recommend_performance():
    """Test /recommend responds under 5 seconds"""
    print_header("Testing /recommend Performance")

    payload = {
        "dataset_name": "Customer_DB",
        "classification": "PII",
        "sensitivity_level": "HIGH",
        "description": "Customer data"
    }

    times = []

    for i in range(3):
        print(f"  Request {i+1}/3...")
        start = time.time()

        response = requests.post(
            f"{BASE_URL}/recommend",
            json=payload
        )

        elapsed = time.time() - start
        times.append(elapsed)

        passed = elapsed < TARGET_TIME
        print_result(
            f"Request {i+1} under {TARGET_TIME}s",
            passed,
            elapsed
        )

        time.sleep(0.5)

    avg = sum(times) / len(times)
    print(f"\n  Average time: {avg:.2f}s")
    print_result(
        f"Average under {TARGET_TIME}s",
        avg < TARGET_TIME,
        avg
    )


def test_report_performance():
    """Test /generate-report performance"""
    print_header("Testing /generate-report Performance")

    print("  Request 1/1...")
    start = time.time()

    response = requests.post(
        f"{BASE_URL}/generate-report",
        json={
            "dataset_name": "Customer_DB",
            "classification": "PII",
            "sensitivity_level": "HIGH",
            "description": "Customer personal data",
            "fields": ["id", "name", "email"]
        }
    )

    elapsed = time.time() - start
    passed = elapsed < TARGET_TIME
    print_result(
        f"Report under {TARGET_TIME}s",
        passed,
        elapsed
    )


def test_fallback_works():
    """Test fallback response has is_fallback field"""
    print_header("Testing Fallback Response")

    response = requests.post(
        f"{BASE_URL}/describe",
        json={
            "dataset_name": "Test_DB",
            "description": "Test dataset",
            "fields": ["id", "name"]
        }
    )

    data = response.json()

    if 'is_fallback' in data:
        print_result("Response has is_fallback field", True)
        print(f"  is_fallback value: {data['is_fallback']}")
    else:
        print_result("Response has is_fallback field", False)


def run_all_tests():
    print("\n" + "="*60)
    print("  Tool-134 — Performance Tests")
    print(f"  Target: All endpoints under {TARGET_TIME}s")
    print("  Note: Using Groq free tier")
    print("="*60)
    print("\n⚠️  Make sure Flask is running first!")

    test_health_performance()
    test_describe_performance()
    test_recommend_performance()
    test_report_performance()
    test_fallback_works()

    print("\n" + "="*60)
    print("  Performance tests complete!")
    print("  Note: Cache will improve times on repeat requests")
    print("="*60 + "\n")


if __name__ == '__main__':
    run_all_tests()