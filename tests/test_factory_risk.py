import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
from services.factory_risk_analyzer import get_factory_risk_analysis

print(
    get_factory_risk_analysis()
)