import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
from tools.quality_tool import get_quality_analysis
from llm_service import ask_llm

data = get_quality_analysis()

prompt = f"""
You are a manufacturing quality expert.

Line: {data['line']}

Defect Rate: {data['defect_rate']}%
Scrap Rate: {data['scrap_rate']}%
Rework Rate: {data['rework_rate']}%

Provide:

1. Quality Status
2. Key Concern
3. Recommendation

Limit response to 150 words.
"""

response = ask_llm(prompt)

print(response)