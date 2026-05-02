#!/usr/bin/env python3

# Debug script to understand how aspect detection works
from orbpondering.aspects import _angular_separation, find_aspects
from orbpondering.constants import AspectType
from orbpondering.models import Aspect, BirthData, NatalChart

# Test the angular separation
print("Angular separation tests:")
print(f"0.0 to 0.0 = {_angular_separation(0.0, 0.0)}")
print(f"0.0 to 30.0 = {_angular_separation(0.0, 30.0)}")
print(f"0.0 to 90.0 = {_angular_separation(0.0, 90.0)}")
print(f"0.0 to 180.0 = {_angular_separation(0.0, 180.0)}")
print(f"0.0 to 270.0 = {_angular_separation(0.0, 270.0)}")
print(f"30.0 to 60.0 = {_angular_separation(30.0, 60.0)}")
print(f"350.0 to 10.0 = {_angular_separation(350.0, 10.0)}")

# Test aspect classification
print("\nAspect classification tests:")
for aspect in AspectType:
    print(f"{aspect.name}: ideal={aspect.value[0]}, max_orb={aspect.value[1]}")

print("\nTesting _classify_aspect:")
print(f"_classify_aspect(0.0) = {AspectType.CONJUNCTION} with orb 0.0")
print(f"_classify_aspect(2.0) = {AspectType.CONJUNCTION} with orb 2.0")
print(f"_classify_aspect(7.0) = {AspectType.CONJUNCTION} with orb 7.0")
print(f"_classify_aspect(9.0) = None with orb 0.0 (outside orb)")

# Test the actual find_aspects logic
print("\nTesting find_aspects:")

natal_positions = {
    "sun": 0.0,
    "moon": 100.0,
}
transit_positions = {
    "sun": 2.0,  # close to natal sun
    "moon": 100.0,  # same as natal moon
}

natal = NatalChart(
    birth_data=BirthData(date="2025-01-01", time=None, lat=0.0, lon=0.0, tz=None),
    planetary_positions=natal_positions,
)
transit = type("Chart", (), {
    "planetary_positions": transit_positions,
})()

result = find_aspects(natal, transit)
print(f"Result: {result}")
for a in result:
    print(f"  {a}")