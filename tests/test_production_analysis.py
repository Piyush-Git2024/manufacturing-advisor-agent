import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
from tools.production_tool import get_production_analysis
from llm_service import ask_llm

data = get_production_analysis()

prompt = f"""
You are a manufacturing operations expert.

Target Production: {data['target']}
Current Production: {data['current']}
Projected Production: {data['projected_output']}
Production Gap: {data['gap']}

Provide:

1. Status
2. Key Risk
3. Recommendation

Limit response to 150 words.
"""

result = ask_llm(prompt)

print(result)