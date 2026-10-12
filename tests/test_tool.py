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

print(
    get_production_analysis()
)