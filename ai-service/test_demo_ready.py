# test_demo_ready.py
# Tests all prompts with 30 demo records
# All outputs must be demo-ready
# Run: python test_demo_ready.py

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.groq_client import (
    classify_data,
    recommend_actions,
    generate_report
)

# 30 realistic demo records
DEMO_RECORDS = [
    {
        "dataset_name": "Customer_DB",
        "description": "Customer personal information database",
        "fields": ["customer_id", "full_name", "email", "phone", "address"]
    },
    {
        "dataset_name": "Payment_Records",
        "description": "Financial transaction records",
        "fields": ["transaction_id", "credit_card", "amount", "cvv"]
    },
    {
        "dataset_name": "Employee_Health",
        "description": "Employee medical records",
        "fields": ["employee_id", "diagnosis", "prescription", "doctor"]
    },
    {
        "dataset_name": "Product_Catalog",
        "description": "Public product listing",
        "fields": ["product_id", "name", "price", "category"]
    },
    {
        "dataset_name": "Server_Logs",
        "description": "Application server logs",
        "fields": ["timestamp", "ip_address", "request_url", "status"]
    },
    {
        "dataset_name": "HR_Records",
        "description": "Human resources employee data",
        "fields": ["employee_id", "salary", "performance", "manager"]
    },
    {
        "dataset_name": "Sales_Data",
        "description": "Sales transaction records",
        "fields": ["sale_id", "customer_id", "amount", "date"]
    },
    {
        "dataset_name": "Marketing_DB",
        "description": "Marketing campaign data",
        "fields": ["campaign_id", "target_audience", "budget", "roi"]
    },
    {
        "dataset_name": "Student_Records",
        "description": "Student academic records",
        "fields": ["student_id", "name", "grades", "attendance"]
    },
    {
        "dataset_name": "Patient_DB",
        "description": "Hospital patient records",
        "fields": ["patient_id", "name", "diagnosis", "treatment"]
    },
    {
        "dataset_name": "Insurance_Claims",
        "description": "Insurance claim records",
        "fields": ["claim_id", "policy_number", "amount", "status"]
    },
    {
        "dataset_name": "Legal_Documents",
        "description": "Legal case documents",
        "fields": ["case_id", "client_name", "case_type", "attorney"]
    },
    {
        "dataset_name": "Tax_Records",
        "description": "Tax filing records",
        "fields": ["tax_id", "income", "deductions", "tax_paid"]
    },
    {
        "dataset_name": "Bank_Accounts",
        "description": "Bank account information",
        "fields": ["account_id", "balance", "transactions", "owner"]
    },
    {
        "dataset_name": "Social_Media",
        "description": "Social media user data",
        "fields": ["user_id", "username", "posts", "followers"]
    },
    {
        "dataset_name": "IoT_Sensors",
        "description": "IoT device sensor data",
        "fields": ["device_id", "temperature", "location", "timestamp"]
    },
    {
        "dataset_name": "Email_Archive",
        "description": "Corporate email archive",
        "fields": ["email_id", "sender", "recipient", "subject"]
    },
    {
        "dataset_name": "Research_Data",
        "description": "Scientific research data",
        "fields": ["study_id", "participant_id", "results", "date"]
    },
    {
        "dataset_name": "Inventory_DB",
        "description": "Product inventory records",
        "fields": ["item_id", "quantity", "location", "supplier"]
    },
    {
        "dataset_name": "Access_Logs",
        "description": "System access logs",
        "fields": ["user_id", "action", "timestamp", "ip_address"]
    },
    {
        "dataset_name": "Contract_DB",
        "description": "Business contract database",
        "fields": ["contract_id", "parties", "value", "expiry"]
    },
    {
        "dataset_name": "Supplier_Data",
        "description": "Supplier information database",
        "fields": ["supplier_id", "name", "contact", "products"]
    },
    {
        "dataset_name": "Audit_Logs",
        "description": "System audit trail",
        "fields": ["audit_id", "action", "user", "timestamp"]
    },
    {
        "dataset_name": "CRM_Data",
        "description": "Customer relationship management data",
        "fields": ["contact_id", "name", "email", "interactions"]
    },
    {
        "dataset_name": "Compliance_Records",
        "description": "Regulatory compliance records",
        "fields": ["record_id", "regulation", "status", "date"]
    },
    {
        "dataset_name": "Biometric_Data",
        "description": "Employee biometric records",
        "fields": ["employee_id", "fingerprint", "face_scan", "access"]
    },
    {
        "dataset_name": "Vehicle_Records",
        "description": "Company vehicle tracking data",
        "fields": ["vehicle_id", "driver", "location", "speed"]
    },
    {
        "dataset_name": "Training_Data",
        "description": "Employee training records",
        "fields": ["employee_id", "course", "score", "completion"]
    },
    {
        "dataset_name": "Network_Logs",
        "description": "Network traffic logs",
        "fields": ["packet_id", "source_ip", "destination", "protocol"]
    },
    {
        "dataset_name": "Backup_Records",
        "description": "System backup records",
        "fields": ["backup_id", "size", "timestamp", "status"]
    }
]


def check_describe_output(result, record_name):
    """Check if describe output is demo ready"""
    required = [
        'classification',
        'sensitivity_level',
        'description',
        'data_types',
        'compliance_requirements',
        'risks',
        'recommended_handling',
        'generated_at',
        'is_fallback'
    ]
    missing = [f for f in required if f not in result]
    if missing:
        return False, f"Missing fields: {missing}"
    return True, "OK"


def run_tests():
    print("\n" + "="*60)
    print("  Tool-134 — Demo Ready Test")
    print("  Testing 30 records")
    print("="*60)

    passed = 0
    failed = 0
    fallback = 0

    # Test first 10 records with /describe
    print("\n📊 Testing /describe with 10 records...")
    for record in DEMO_RECORDS[:10]:
        try:
            result = classify_data(
                dataset_name=record['dataset_name'],
                description=record['description'],
                fields=record['fields']
            )

            ok, msg = check_describe_output(
                result,
                record['dataset_name']
            )

            if ok:
                if result.get('is_fallback'):
                    print(f"  ⚠️  {record['dataset_name']} — FALLBACK")
                    fallback += 1
                else:
                    print(f"  ✅ {record['dataset_name']} — {result.get('classification')} / {result.get('sensitivity_level')}")
                passed += 1
            else:
                print(f"  ❌ {record['dataset_name']} — {msg}")
                failed += 1

        except Exception as e:
            print(f"  ❌ {record['dataset_name']} — ERROR: {str(e)}")
            failed += 1

    # Test next 10 records with /recommend
    print("\n📊 Testing /recommend with 10 records...")
    for record in DEMO_RECORDS[10:20]:
        try:
            result = recommend_actions(
                dataset_name=record['dataset_name'],
                classification="Confidential",
                sensitivity_level="HIGH",
                description=record['description']
            )

            if 'recommendations' in result:
                recs = result['recommendations']
                if len(recs) == 3:
                    print(f"  ✅ {record['dataset_name']} — 3 recommendations")
                    passed += 1
                else:
                    print(f"  ❌ {record['dataset_name']} — {len(recs)} recommendations")
                    failed += 1
            else:
                print(f"  ❌ {record['dataset_name']} — No recommendations")
                failed += 1

        except Exception as e:
            print(f"  ❌ {record['dataset_name']} — ERROR: {str(e)}")
            failed += 1

    # Test last 10 records with /generate-report
    print("\n📊 Testing /generate-report with 10 records...")
    for record in DEMO_RECORDS[20:30]:
        try:
            result = generate_report(
                dataset_name=record['dataset_name'],
                classification="Confidential",
                sensitivity_level="HIGH",
                description=record['description'],
                fields=record['fields']
            )

            required = ['title', 'summary', 'overview',
                       'key_items', 'recommendations']
            missing = [f for f in required if f not in result]

            if not missing:
                print(f"  ✅ {record['dataset_name']} — Report complete")
                passed += 1
            else:
                print(f"  ❌ {record['dataset_name']} — Missing: {missing}")
                failed += 1

        except Exception as e:
            print(f"  ❌ {record['dataset_name']} — ERROR: {str(e)}")
            failed += 1

    print("\n" + "="*60)
    print(f"  Results: {passed} passed | {failed} failed | {fallback} fallback")
    print("="*60)

    if failed == 0:
        print("\n🎉 All 30 records are demo ready!")
    else:
        print(f"\n⚠️  {failed} records need attention.")

    print()


if __name__ == '__main__':
    run_tests()