import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
from tools.maintenance_tool import get_maintenance_analysis
from llm_service import ask_llm

data = get_maintenance_analysis()

prompt = f"""
You are a manufacturing maintenance expert.

Machine: {data['machine']}
Temperature: {data['temperature']} C
Vibration: {data['vibration']}
Runtime Hours: {data['runtime']}
Days Since Maintenance: {data['days_since_maintenance']}

Provide:

1. Machine Health
2. Failure Risk
3. Recommended Action

Limit response to 150 words.
"""

response = ask_llm(prompt)

print(response)