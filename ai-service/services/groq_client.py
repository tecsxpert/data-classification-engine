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


def load_prompt_template(template_name):
    """
    Loads prompt template from prompts/ folder
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompts_dir = os.path.join(current_dir, '..', 'prompts')
    template_path = os.path.join(prompts_dir, f"{template_name}.txt")
    with open(template_path, 'r') as f:
        return f.read()


def call_groq_with_retry(prompt, max_retries=3):
    """
    Calls Groq API with automatic retry
    Tries 3 times before giving up
    """
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    for attempt in range(max_retries):
        try:
            logger.info(f"Calling Groq API attempt {attempt + 1}")

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a data classification expert. Always respond with valid JSON only."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=1000
            )

            result = response.choices[0].message.content
            logger.info("Groq API call successful!")
            return result

        except Exception as e:
            logger.error(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                logger.info(f"Waiting {wait_time}s before retry...")
                time.sleep(wait_time)

    logger.error("All retries failed")
    return None


def classify_data(dataset_name, description, fields):
    """
    Main function to classify data using AI
    """
    try:
        # Load prompt template
        template = load_prompt_template('classify_prompt')

        # Replace placeholders with real values
        prompt = template.format(
            dataset_name=dataset_name,
            description=description,
            fields=', '.join(fields),
            generated_at=datetime.utcnow().isoformat()
        )

        # Call Groq API
        response_text = call_groq_with_retry(prompt)

        # If API failed return fallback
        if response_text is None:
            return get_fallback_response(dataset_name)

        # Parse JSON response
        result = json.loads(response_text)
        result['is_fallback'] = False
        return result

    except json.JSONDecodeError as e:
        logger.error(f"JSON parse failed: {str(e)}")
        return get_fallback_response(dataset_name)

    except Exception as e:
        logger.error(f"classify_data error: {str(e)}")
        return get_fallback_response(dataset_name)


def get_fallback_response(dataset_name):
    """
    Returns safe response when AI is unavailable
    PDF requires is_fallback: true
    """
    logger.warning(f"Returning fallback for: {dataset_name}")
    return {
        "classification": "Confidential",
        "sensitivity_level": "HIGH",
        "description": f"Manual classification required for {dataset_name}.",
        "data_types": ["Unknown"],
        "compliance_requirements": ["Manual Review Required"],
        "risks": ["Classification pending manual review"],
        "recommended_handling": "Please review manually.",
        "generated_at": datetime.utcnow().isoformat(),
        "is_fallback": True
    }