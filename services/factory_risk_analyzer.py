from tools.production_tool import get_production_analysis
from tools.quality_tool import get_quality_analysis
from tools.maintenance_tool import get_maintenance_analysis
from llm_service import ask_llm


def get_factory_risk_analysis():

    production = get_production_analysis()
    quality = get_quality_analysis()
    maintenance = get_maintenance_analysis()

    prompt = f"""
You are a senior manufacturing consultant.

IMPORTANT:
Only use the facts provided.
Do not invent data.
Do not assume downtime unless explicitly stated.

Identify:

1. Biggest Operational Risk
2. Root Cause
3. Business Impact
4. Recommended Action

Production Facts

Target Production: {production['target']}
Projected Output: {production['projected_output']}
Production Gap: {production['gap']}

Quality Facts

Defect Rate: {quality['defect_rate']}%
Scrap Rate: {quality['scrap_rate']}%
Rework Rate: {quality['rework_rate']}%

Maintenance Facts

Machine: {maintenance['machine']}
Temperature: {maintenance['temperature']}
Vibration: {maintenance['vibration']}
Runtime Hours: {maintenance['runtime']}
Days Since Last Maintenance:
{maintenance['days_since_maintenance']}

Look for relationships between the facts.

Keep response under 200 words.
"""

    return ask_llm(prompt)