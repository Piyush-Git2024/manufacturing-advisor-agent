import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

#from services.factory_summary_service import get_factory_summary  # type: ignore[reportMissingImports]

#print("\nFACTORY SUMMARY\n")
#print(get_factory_summary())

from services.factory_summary_service import (
    get_factory_summary,
    get_executive_risk_summary,
    get_plant_risk_ranking
)

print("\n")
print(get_executive_risk_summary())
print()
print(get_plant_risk_ranking())