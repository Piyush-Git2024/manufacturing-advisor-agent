import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from services.factory_risk_analyzer import (
    get_factory_risk_analysis
)

print(get_factory_risk_analysis())