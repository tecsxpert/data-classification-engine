import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from services.groq_client import classify_data

test_cases = [
    {
        "name": "Test 1 — Customer Database",
        "dataset_name": "Customer_DB",
        "description": "Customer personal information",
        "fields": ["customer_id", "full_name", "email", "phone"]
    },
    {
        "name": "Test 2 — Payment Records",
        "dataset_name": "Payment_Records",
        "description": "Financial transaction records",
        "fields": ["transaction_id", "credit_card_number", "amount"]
    },
    {
        "name": "Test 3 — Health Records",
        "dataset_name": "Employee_Health",
        "description": "Employee medical records",
        "fields": ["employee_id", "medical_condition", "prescription"]
    },
    {
        "name": "Test 4 — Product Catalog",
        "dataset_name": "Product_Catalog",
        "description": "Public product listing",
        "fields": ["product_id", "product_name", "price"]
    },
    {
        "name": "Test 5 — Server Logs",
        "dataset_name": "Server_Logs",
        "description": "Application server logs",
        "fields": ["timestamp", "ip_address", "request_url"]
    }
]


def run_tests():
    print("\n" + "="*60)
    print("  Tool-134 Prompt Template Test")
    print("  Testing 5 real inputs")
    print("="*60)

    passed = 0
    failed = 0

    for test in test_cases:
        print(f"\n🧪 {test['name']}")
        print(f"   Calling AI... please wait...")

        try:
            result = classify_data(
                dataset_name=test['dataset_name'],
                description=test['description'],
                fields=test['fields']
            )

            required = [
                'classification',
                'sensitivity_level',
                'description',
                'is_fallback'
            ]
            missing = [f for f in required if f not in result]

            if missing:
                print(f"   ❌ FAILED — Missing: {missing}")
                failed += 1
            else:
                print(f"   ✅ PASSED")
                print(f"   Classification: {result['classification']}")
                print(f"   Sensitivity:    {result['sensitivity_level']}")
                print(f"   Fallback:       {result['is_fallback']}")
                passed += 1

        except Exception as e:
            print(f"   ❌ ERROR: {str(e)}")
            failed += 1

    print("\n" + "="*60)
    print(f"  Results: {passed} passed | {failed} failed")
    print("="*60 + "\n")

    if failed == 0:
        print("🎉 All 5 tests passed!")
    else:
        print("⚠️  Fix failing tests before Day 3.")


if __name__ == '__main__':
    run_tests()