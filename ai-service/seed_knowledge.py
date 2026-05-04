# seed_knowledge.py
# Seeds ChromaDB with 10 domain knowledge documents
# Run once: python seed_knowledge.py

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.chroma_service import initialize_chromadb
import chromadb
from chromadb.utils import embedding_functions
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 10 domain knowledge documents
KNOWLEDGE_DOCUMENTS = [
    {
        "id": "doc_001",
        "content": "PII (Personally Identifiable Information) includes any data that can identify a specific individual. Examples include full name, email address, phone number, home address, date of birth, social security number, passport number, and biometric data. PII requires strict protection under GDPR, CCPA, and other privacy regulations.",
        "category": "PII Classification"
    },
    {
        "id": "doc_002",
        "content": "Financial data classification includes credit card numbers, bank account details, transaction records, salary information, and tax identification numbers. Financial data is governed by PCI-DSS for payment data and SOX for financial reporting. HIGH or CRITICAL sensitivity level required.",
        "category": "Financial Classification"
    },
    {
        "id": "doc_003",
        "content": "Health data or PHI (Protected Health Information) includes medical records, diagnoses, prescriptions, insurance information, and treatment history. Health data is governed by HIPAA in the US and requires CRITICAL sensitivity classification. Strict access controls and encryption mandatory.",
        "category": "Health Classification"
    },
    {
        "id": "doc_004",
        "content": "Public data is information that can be freely shared without risk. Examples include publicly available product catalogs, press releases, public website content, and general company information. Public data has LOW sensitivity and minimal compliance requirements.",
        "category": "Public Classification"
    },
    {
        "id": "doc_005",
        "content": "Confidential data includes business strategies, trade secrets, internal financial reports, merger plans, and proprietary algorithms. Confidential data has HIGH sensitivity and requires access controls, encryption, and non-disclosure agreements.",
        "category": "Confidential Classification"
    },
    {
        "id": "doc_006",
        "content": "Internal data includes employee directories, internal policies, procedures, meeting notes, and internal communications. Internal data has MEDIUM sensitivity and should be restricted to employees only. Not for public disclosure.",
        "category": "Internal Classification"
    },
    {
        "id": "doc_007",
        "content": "Data encryption best practices: Use AES-256 for data at rest, TLS 1.3 for data in transit. Implement key rotation every 90 days. Never store encryption keys with encrypted data. Use envelope encryption for large datasets.",
        "category": "Security Best Practices"
    },
    {
        "id": "doc_008",
        "content": "GDPR compliance requirements: Lawful basis for processing, data minimization, purpose limitation, storage limitation, data subject rights (access, rectification, erasure), data breach notification within 72 hours, Data Protection Officer appointment for large scale processing.",
        "category": "Compliance GDPR"
    },
    {
        "id": "doc_009",
        "content": "Access control best practices: Implement role-based access control (RBAC), principle of least privilege, multi-factor authentication for sensitive data, regular access reviews, immediate revocation on employee termination, audit logging of all access attempts.",
        "category": "Access Control"
    },
    {
        "id": "doc_010",
        "content": "Data retention policies: Define retention periods for each data type. PII should be deleted when no longer needed. Financial records typically kept 7 years. Health records kept as per local regulations. Implement automated deletion workflows. Document retention schedules.",
        "category": "Data Retention"
    }
]


def seed_chromadb():
    """Seeds ChromaDB with domain knowledge documents"""

    print("\n" + "="*60)
    print("  Tool-134 — ChromaDB Knowledge Seeder")
    print("="*60)

    # Initialize ChromaDB
    print("\n  Initializing ChromaDB...")

    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    client = chromadb.PersistentClient(path="./chroma_data")

    # Delete existing collection if exists
    try:
        client.delete_collection("domain_knowledge")
        print("  Deleted existing collection")
    except Exception:
        pass

    # Create fresh collection
    collection = client.get_or_create_collection(
        name="domain_knowledge",
        embedding_function=embedding_fn
    )

    print(f"\n  Seeding {len(KNOWLEDGE_DOCUMENTS)} documents...")

    # Add documents one by one
    for doc in KNOWLEDGE_DOCUMENTS:
        try:
            collection.add(
                ids=[doc['id']],
                documents=[doc['content']],
                metadatas=[{"category": doc['category']}]
            )
            print(f"  ✅ Added: {doc['category']}")
        except Exception as e:
            print(f"  ❌ Failed: {doc['category']} — {str(e)}")

    print(f"\n  Total documents: {collection.count()}")
    print("\n" + "="*60)
    print("  ChromaDB seeding complete!")
    print("="*60 + "\n")


if __name__ == '__main__':
    seed_chromadb()