# Orbpondering Natal Chart Personalization Implementation Plan

## Overview
This document outlines the implementation plan for adding natal chart support to orbpondering, enabling personalized tarot readings based on the user's birth chart and current transits.

## Key Design Decisions
- **Option A**: Aspects influence the seed hash (not card weighting)
- **Birth time**: Optional; falls back to noon UTC with warning
- **Classic 5 aspects**: conjunction 0°, sextile 60°, square 90°, trine 120°, opposition 180°
- **CLI**: Optional `--birth-*` parameters; presence of `--birth-date` auto-enables natal mode
- **Education mode**: Factual only — raw data, no interpretive claims
- **House cusps**: All 4 systems, computed lazily
- **Aspects**: All transit planets vs all natal planets (not just matching bodies), but purely descriptive

## Implementation Phases

### Phase 1: Constants & Models
Files to modify/create:
- `src/orbpondering/constants.py` - Add `AspectType` enum
- `src/orbpondering/models.py` - Add `BirthData`, `Aspect`, `NatalChart` models; update `TarotReading`

### Phase 2: Astronomy Refinements
File to modify:
- `src/orbpondering/astronomy.py` - Add `_to_time`, datetime support, timezone conversion

### Phase 3: Aspect Detection Engine
File to create:
- `src/orbpondering/aspects.py` - Aspect detection engine

### Phase 4: Seed Generation
File to modify:
- `src/orbpondering/seed.py` - Modify `chart_seed()` to accept natal data and aspects

### Phase 5: Draw Pipeline
File to modify:
- `src/orbpondering/draw.py` - Add `birth_tarot_draw()` function

### Phase 6: CLI Updates
File to modify:
- `src/orbpondering/__main__.py` - Add `--birth-*` arguments, natal mode detection

### Phase 7: Education Mode
Files to modify:
- `src/orbpondering/education/steps.py` - Add natal/aspect education steps
- `src/orbpondering/education/engine.py` - Conditional natal steps

### Phase 8: Tests
Files to create/update:
- `tests/test_aspects.py` - Aspect detection tests
- `tests/test_natal.py` - Natal chart & draw tests
- `tests/test_cli.py` - CLI birth data handling tests
- Update `tests/test_seed.py` - Add natal seed tests

## Detailed Implementation Details

### 1. Constants & Models
**`src/orbpondering/constants.py`:**
```python
class AspectType(Enum):
    CONJUNCTION = (0, 8)
    SEXTILE = (60, 6)
    SQUARE = (90, 8)
    TRINE = (120, 8)
    OPPOSITION = (180, 8)
```

**`src/orbpondering/models.py`:**
```python
@dataclass(frozen=True)
class BirthData:
    date: date
    time: datetime.time | None
    lat: float
    lon: float
    tz: str | None

@dataclass(frozen=True)
class Aspect:
    natal_body: str
    transit_body: str
    separation: float
    aspect_type: AspectType
    orb: float

@dataclass(frozen=True)
class NatalChart:
    birth_data: BirthData
    planetary_positions: dict[str, float]

    @cached_property
    def house_cusps(self) -> dict[HouseSystem, list[float]]:
        """Compute all 4 house systems on first access."""
        from orbpondering.houses import house_cusps
        when: date | datetime = self.birth_data.date
        if self.birth_data.time:
            # Convert to datetime with timezone
            ...
        return {
            hs: house_cusps(when, self.birth_data.lat, self.birth_data.lon, hs)
            for hs in HouseSystem
        }

@dataclass(frozen=True)
class TarotReading:
    # ... existing fields ...
    natal_chart: NatalChart | None = None
    aspects: tuple[Aspect, ...] = ()
```

### 2. Astronomy Refinements
**`src/orbpondering/astronomy.py`:**
- Add `_to_time(d: date | datetime) -> Time`
- Modify `planetary_positions`, `ascendant`, `midheaven`, `sidereal_time` to accept `date | datetime`
- Add timezone conversion using `zoneinfo`
- Handle both noon fallback and exact time scenarios

### 3. Aspect Detection Engine
**`src/orbpondering/aspects.py`:**
```python
def _angular_separation(lon1: float, lon2: float) -> float:
    """Shortest angular distance between two longitudes."""

def find_aspects(natal: NatalChart, transit: Chart) -> tuple[Aspect, ...]:
    """Detect classical aspects between all natal and transit planets."""
```

### 4. Seed Generation
**`src/orbpondering/seed.py`:**
```python
def chart_seed(
    d: date, lat: float, lon: float,
    house_system: HouseSystem,
    natal_chart: NatalChart | None = None,
    aspects: tuple[Aspect, ...] = (),
) -> int:
    # Build raw dict with natal + aspects if present
    # Same SHA256 → int(...[:16], 16) pattern
```

### 5. Draw Pipeline
**`src/orbpondering/draw.py`:**
```python
def birth_tarot_draw(
    d: date, lat: float, lon: float,
    birth_data: BirthData,
    house_system: HouseSystem,
    spread: Spread,
) -> TarotReading:
    # 1. Compute natal chart
    # 2. Compute transit chart
    # 3. Find aspects
    # 4. Generate seed (natal + transit + aspects)
    # 5. Shuffle & deal
    # 6. Return TarotReading with natal_chart and aspects
```

### 6. CLI Updates
**`src/orbpondering/__main__.py`:**
New arguments:
```
--birth-date YYYY-MM-DD   # Triggers natal mode
--birth-time HH:MM        # Optional; defaults to noon UTC
--birth-zone IANA_TZ      # Optional; defaults to UTC
--birth-lat FLOAT         # Required with --birth-date
--birth-lon FLOAT         # Required with --birth-date
```

Behavior:
- When `--birth-date` present → parse `BirthData` → call `birth_tarot_draw()`
- If `--birth-time` missing → print warning to stderr
- Display natal summary before spread

### 7. Education Mode
**New education steps in `src/orbpondering/education/steps.py`:**
1. `step_birth_data` — display birth parameters, warn about missing time
2. `step_natal_positions` — show natal planetary positions
3. `step_natal_houses` — show house cusps (all 4 systems)
4. `step_aspects` — list detected aspects
5. `step_seed_with_aspects` — show how aspects contribute to seed hash

### 8. Tests
Create new test files and update existing ones:
- `tests/test_aspects.py` - 9 tests
- `tests/test_natal.py` - 8 tests  
- `tests/test_cli.py` - 7 tests
- Update `tests/test_seed.py` - 6 tests

## Dependencies
- No new pip dependencies — `zoneinfo` is Python 3.9+ stdlib, already on 3.12

## Key Integration Points
1. **Seed Generation**: Aspects are added to the hash input
2. **Education Mode**: New steps added conditionally when natal mode is active
3. **CLI Interface**: New arguments to trigger natal mode
4. **Models**: Structured data to hold natal chart and aspects