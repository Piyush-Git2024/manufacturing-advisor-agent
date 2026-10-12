from tools.production_tool import get_production_analysis
from tools.quality_tool import get_quality_analysis
from tools.maintenance_tool import get_maintenance_analysis

from services.factory_risk_analyzer import get_factory_risk_analysis
from llm_service import ask_llm


def get_production_response():

    data = get_production_analysis()

    prompt = f"""
You are a manufacturing operations expert.

Target Production: {data['target']}
Current Production: {data['current']}
Projected Output: {data['projected_output']}
Production Gap: {data['gap']}

Provide:

1. Status
2. Risk
3. Recommendation

Keep response under 150 words.
"""

    return ask_llm(prompt)


def get_quality_response():

    data = get_quality_analysis()

    prompt = f"""
You are a quality management expert.

Defect Rate: {data['defect_rate']}%
Scrap Rate: {data['scrap_rate']}%
Rework Rate: {data['rework_rate']}%

Provide:

1. Quality Status
2. Key Concern
3. Recommendation

Keep response under 150 words.
"""

    return ask_llm(prompt)


def get_maintenance_response():

    data = get_maintenance_analysis()

    prompt = f"""
You are a maintenance expert.

Machine: {data['machine']}
Temperature: {data['temperature']}
Vibration: {data['vibration']}
Runtime Hours: {data['runtime']}
Days Since Maintenance:
{data['days_since_maintenance']}

Provide:

1. Machine Health
2. Failure Risk
3. Recommended Action

Keep response under 150 words.
"""

    return ask_llm(prompt)


def get_advisor_response(question):

    question = question.lower()

    if "production" in question:
        return get_production_response()

    elif "quality" in question:
        return get_quality_response()

    elif "maintenance" in question:
        return get_maintenance_response()

    elif "risk" in question:
        return get_factory_risk_analysis()

    else:
        return """
I can assist with:

• Production Analysis
• Quality Analysis
• Maintenance Analysis
• Factory Risk Assessment

Try asking:
'What is the biggest operational risk today?'
"""