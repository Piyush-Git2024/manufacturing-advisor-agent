import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
from services.advisor_service import get_advisor_response

question = input("Ask a question: ")

response = get_advisor_response(question)

print("\n")
print(response)