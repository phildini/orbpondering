from orbpondering.houses import house_cusps
from orbpondering.constants import HouseSystem
from datetime import date

d = date(2025, 6, 15)
print("Testing different house systems:")

for hs in HouseSystem:
    cusps = house_cusps(d, 40.7, -74.0, hs)
    print(f"{hs.value:12s}: {[round(c, 2) for c in cusps]}")
