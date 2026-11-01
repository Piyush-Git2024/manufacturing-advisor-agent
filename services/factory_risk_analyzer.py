from services.factory_summary_service import (
    get_management_dashboard
)

from llm_service import ask_llm


def get_factory_risk_analysis():

    dashboard = get_management_dashboard()

    prompt = f"""
You are a Manufacturing Operations Consultant.

Review the management dashboard below.

{dashboard}

IMPORTANT:

Use ONLY information explicitly present in the dashboard.

Do NOT assume:
- operator training issues
- staffing issues
- planning issues
- supply chain problems
- quality process issues

unless they are directly stated.

If the root cause cannot be proven from the dashboard,
state:

"Additional operational data is required to determine
the root cause with confidence."


Provide:

1. Executive Summary

2. Biggest Operational Risk

3. Root Cause Analysis

4. Business Impact

5. Priority Actions

6. Recommended Leadership Focus

Keep the response under 300 words.

Use a professional management-consulting style.
"""

    return ask_llm(prompt)