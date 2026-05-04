import os
import json
import time
import logging
from groq import Groq
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Track response times globally
ai_response_times = []


def get_average_response_time():
    """Returns average AI response time in seconds"""
    if not ai_response_times:
        return 0
    return sum(ai_response_times) / len(ai_response_times)


def load_prompt_template(template_name):
    """Loads prompt template from prompts/ folder"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompts_dir = os.path.join(current_dir, '..', 'prompts')
    template_path = os.path.join(
        prompts_dir, f"{template_name}.txt"
    )
    with open(template_path, 'r') as f:
        return f.read()


def call_groq_with_retry(prompt, max_retries=3):
    """
    Calls Groq API with automatic retry.
    Tracks response time for performance monitoring.
    """
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    for attempt in range(max_retries):
        try:
            logger.info(f"Calling Groq API attempt {attempt + 1}")

            # Track start time
            start_time = time.time()

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a data governance expert. Always respond with valid JSON only. Be concise."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=1000
            )

            # Calculate response time
            response_time = time.time() - start_time

            # Track response time
            ai_response_times.append(response_time)
            if len(ai_response_times) > 100:
                ai_response_times.pop(0)

            logger.info(
                f"Groq API success! Time: {response_time:.2f}s"
            )

            result = response.choices[0].message.content
            return result

        except Exception as e:
            logger.error(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                logger.info(f"Waiting {wait_time}s before retry...")
                time.sleep(wait_time)

    logger.error("All retries failed — returning fallback")
    return None


def classify_data(dataset_name, description, fields):
    """Classifies data using AI — used by /describe"""
    try:
        template = load_prompt_template('classify_prompt')
        prompt = template.format(
            dataset_name=dataset_name,
            description=description,
            fields=', '.join(fields),
            generated_at=datetime.utcnow().isoformat()
        )
        response_text = call_groq_with_retry(prompt)
        if response_text is None:
            return get_fallback_response(dataset_name)
        result = json.loads(response_text)
        result['is_fallback'] = False
        return result
    except Exception as e:
        logger.error(f"classify_data error: {str(e)}")
        return get_fallback_response(dataset_name)


def recommend_actions(dataset_name, classification,
                      sensitivity_level, description):
    """Generates recommendations — used by /recommend"""
    try:
        template = load_prompt_template('recommend_prompt')
        prompt = template.format(
            dataset_name=dataset_name,
            classification=classification,
            sensitivity_level=sensitivity_level,
            description=description,
            generated_at=datetime.utcnow().isoformat()
        )
        response_text = call_groq_with_retry(prompt)
        if response_text is None:
            return get_fallback_recommendations(dataset_name)
        result = json.loads(response_text)
        result['is_fallback'] = False
        return result
    except Exception as e:
        logger.error(f"recommend_actions error: {str(e)}")
        return get_fallback_recommendations(dataset_name)


def generate_report(dataset_name, classification,
                    sensitivity_level, description, fields):
    """Generates full report — used by /generate-report"""
    try:
        template = load_prompt_template('report_prompt')
        prompt = template.format(
            dataset_name=dataset_name,
            classification=classification,
            sensitivity_level=sensitivity_level,
            description=description,
            fields=', '.join(fields),
            generated_at=datetime.utcnow().isoformat()
        )
        response_text = call_groq_with_retry(prompt)
        if response_text is None:
            return get_fallback_report(dataset_name)
        result = json.loads(response_text)
        result['is_fallback'] = False
        return result
    except Exception as e:
        logger.error(f"generate_report error: {str(e)}")
        return get_fallback_report(dataset_name)


def get_fallback_response(dataset_name):
    """
    Returns safe fallback when AI unavailable.
    PDF requires is_fallback: true
    """
    logger.warning(f"Returning fallback for: {dataset_name}")
    return {
        "classification": "Confidential",
        "sensitivity_level": "HIGH",
        "description": f"Manual classification required for {dataset_name}. AI service temporarily unavailable.",
        "data_types": ["Unknown"],
        "compliance_requirements": ["Manual Review Required"],
        "risks": ["Classification pending manual review"],
        "recommended_handling": "Please review manually.",
        "generated_at": datetime.utcnow().isoformat(),
        "is_fallback": True
    }


def get_fallback_recommendations(dataset_name):
    """Returns safe fallback recommendations"""
    logger.warning(
        f"Returning fallback recommendations for: {dataset_name}"
    )
    return {
        "recommendations": [
            {
                "action_type": "ENCRYPT",
                "description": "Encrypt all sensitive data fields.",
                "priority": "HIGH"
            },
            {
                "action_type": "ACCESS_CONTROL",
                "description": "Restrict access to authorized personnel.",
                "priority": "HIGH"
            },
            {
                "action_type": "AUDIT",
                "description": "Enable audit logging for all access.",
                "priority": "MEDIUM"
            }
        ],
        "generated_at": datetime.utcnow().isoformat(),
        "is_fallback": True
    }


def get_fallback_report(dataset_name):
    """Returns safe fallback report"""
    logger.warning(
        f"Returning fallback report for: {dataset_name}"
    )
    return {
        "title": f"Data Classification Report — {dataset_name}",
        "summary": f"Manual review required for {dataset_name}.",
        "overview": "AI service temporarily unavailable.",
        "key_items": [
            {
                "category": "Data Type",
                "value": "Unknown — manual review required"
            },
            {
                "category": "Compliance",
                "value": "Manual review required"
            },
            {
                "category": "Risk Level",
                "value": "Unknown — manual review required"
            },
            {
                "category": "Data Sensitivity",
                "value": "Unknown — manual review required"
            }
        ],
        "recommendations": [
            {
                "action_type": "ENCRYPT",
                "description": "Encrypt all sensitive data fields.",
                "priority": "HIGH"
            },
            {
                "action_type": "ACCESS_CONTROL",
                "description": "Restrict access to authorized personnel.",
                "priority": "HIGH"
            },
            {
                "action_type": "AUDIT",
                "description": "Enable audit logging.",
                "priority": "MEDIUM"
            }
        ],
        "generated_at": datetime.utcnow().isoformat(),
        "is_fallback": True
    }