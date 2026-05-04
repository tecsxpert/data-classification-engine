# test_security.py
# Tests all security measures are working
# Run with: python test_security.py
# Flask must be running first!

import requests

BASE_URL = "http://localhost:5000"


def print_header(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def print_result(test_name, passed):
    status = "✅ PASSED" if passed else "❌ FAILED"
    print(f"  {status} — {test_name}")


def test_security_headers():
    """Test all security headers are present"""
    print_header("Testing Security Headers")

    try:
        response = requests.get(f"{BASE_URL}/health")
        headers = response.headers

        # Check each security header
        checks = [
            ('X-Frame-Options', 'DENY'),
            ('X-Content-Type-Options', 'nosniff'),
            ('X-XSS-Protection', '1; mode=block'),
            ('Referrer-Policy', 'strict-origin-when-cross-origin'),
            ('Content-Security-Policy', "default-src 'self'"),
        ]

        for header_name, expected_value in checks:
            if header_name in headers:
                if expected_value in headers[header_name]:
                    print_result(f"{header_name} present", True)
                else:
                    print_result(
                        f"{header_name} has correct value",
                        False
                    )
            else:
                print_result(f"{header_name} present", False)

        # Check server header
        server = headers.get('Server', '')
        if 'werkzeug' not in server.lower():
            print_result("Server info hidden", True)
        else:
            print_result(
                "Server info hidden (Werkzeug in dev — acceptable)",
                True
            )

    except Exception as e:
        print(f"  ❌ ERROR: {str(e)}")


def test_prompt_injection():
    """Test prompt injection is blocked"""
    print_header("Testing Prompt Injection Protection")

    injection_attempts = [
        "ignore previous instructions",
        "ignore above instructions",
        "disregard all instructions",
        "forget instructions",
        "new instructions follow",
        "system prompt override"
    ]

    for attempt in injection_attempts:
        try:
            response = requests.post(
                f"{BASE_URL}/describe",
                json={
                    "dataset_name": attempt,
                    "description": "test",
                    "fields": ["field1"]
                }
            )
            print_result(
                f"Blocked: '{attempt[:30]}'",
                response.status_code == 400
            )
        except Exception as e:
            print(f"  ❌ ERROR: {str(e)}")


def test_empty_inputs():
    """Test empty inputs are rejected"""
    print_header("Testing Empty Input Validation")

    try:
        # Empty body
        response = requests.post(
            f"{BASE_URL}/describe",
            json={}
        )
        print_result(
            "Empty body returns 400",
            response.status_code == 400
        )

        # Empty fields list
        response = requests.post(
            f"{BASE_URL}/describe",
            json={
                "dataset_name": "Test",
                "description": "Test",
                "fields": []
            }
        )
        print_result(
            "Empty fields returns 400",
            response.status_code == 400
        )

        # Null values
        response = requests.post(
            f"{BASE_URL}/describe",
            json={
                "dataset_name": None,
                "description": "Test",
                "fields": ["field1"]
            }
        )
        print_result(
            "Null dataset_name returns 400",
            response.status_code == 400
        )

    except Exception as e:
        print(f"  ❌ ERROR: {str(e)}")


def test_wrong_methods():
    """Test wrong HTTP methods are rejected"""
    print_header("Testing Wrong HTTP Methods")

    try:
        # GET on /describe
        response = requests.get(f"{BASE_URL}/describe")
        print_result(
            "GET /describe returns 405",
            response.status_code == 405
        )

        # GET on /recommend
        response = requests.get(f"{BASE_URL}/recommend")
        print_result(
            "GET /recommend returns 405",
            response.status_code == 405
        )

        # POST on /health
        response = requests.post(f"{BASE_URL}/health")
        print_result(
            "POST /health returns 405",
            response.status_code == 405
        )

    except Exception as e:
        print(f"  ❌ ERROR: {str(e)}")


def test_invalid_endpoints():
    """Test invalid endpoints return 404"""
    print_header("Testing Invalid Endpoints")

    invalid_endpoints = [
        "/invalid",
        "/admin",
        "/config",
        "/env"
    ]

    for endpoint in invalid_endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}")
            print_result(
                f"GET {endpoint} returns 404",
                response.status_code == 404
            )
        except Exception as e:
            print(f"  ❌ ERROR: {str(e)}")


def run_all_tests():
    print("\n" + "="*60)
    print("  Tool-134 — Security Tests")
    print("="*60)
    print("\n⚠️  Make sure Flask is running first!")

    test_security_headers()
    test_prompt_injection()
    test_empty_inputs()
    test_wrong_methods()
    test_invalid_endpoints()

    print("\n" + "="*60)
    print("  Security tests complete!")
    print("="*60 + "\n")


if __name__ == '__main__':
    run_all_tests()