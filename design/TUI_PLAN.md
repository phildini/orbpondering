# Orbponding Textual TUI Plan

## Overview

Transform orbponding from a one-shot CLI into an interactive terminal dashboard using Textual. The TUI will display tarot card layouts visually, show astrological charts, and allow users to navigate through readings interactively.

TUI mode is **optional** — the CLI remains the default entry point. The TUI is activated via `orbpondering --tui`. Education mode is **incompatible** with TUI mode; use CLI for education.

---

## Architecture

### Core Widget Classes

#### 1. `CardWidget` (extends `Static`)

Renders a single tarot card with:
- ASCII art card frame
- Card name + arcana type
- Suit symbol (for minor arcana: ⚡ Wands, ☌ Cups, ⚔ Swords, ⭐ Pentacles)
- Orientation indicator (↑ upright / ↓ reversed) — **only shown when `--reversed` CLI flag is enabled** (default: off)
- Element color coding:
  - Fire/Wands → red
  - Water/Cups → blue
  - Air/Swords → yellow
  - Earth/Pentacles → green

Supports click/tap to expand details.

**Reactive state:**
- `card` – the Card data object
- `is_flipped` – whether card is face-down or face-up
- `is_selected` – whether this card is highlighted

**Future work (not in scope for v1):**
- `CardPosition.resonant_sign` and `resonant_planet` fields
- `_infer_house_index()` improvement (current exact-match float comparison left as-is)

#### 2. `SpreadLayout` (extends `Static`)

Visual layout of the spread with positioned card slots. Supports three layouts:

- **Daily** – Single centered card
- **Three Card** – Three cards horizontal (Past → Present → Future)
- **Celtic Cross** – Traditional 10-card layout using a **2D grid with empty spacer widgets** for gaps. Overlapping positions (e.g., crossing card) displayed as separate stacked rows rather than true overlap.

Each slot can be:
- Empty (waiting for reveal)
- Face-down (card drawn but not yet read)
- Face-up (revealed with animation)
- Highlighted (currently selected)

**Reactive state:**
- `spread` – the Spread configuration
- `positions` – list of card slot data
- `current_position` – index of selected slot

#### 3. `PlanetaryPanel` (extends `Static`)

Shows current planetary positions in a formatted table:

```
☉ Sun      17°13' Taurus     ♉
☽ Moon     03°42' Libra      ♎
☿ Mercury  28°50' Aries      ♈
♀ Venus    05°18' Gemini     ♊
♂ Mars     12°30' Leo        ♌
♃ Jupiter  22°45' Virgo      ♍
♄ Saturn   15°20' Capricorn  ♑
♅ Uranus   25°33' Taurus     ♉
♆ Neptune  01°08' Pisces     ♓
♇ Pluto    01°15' Aquarius   ♒
```

Color-coded by element. Can toggle between:
- Transit positions (current date)
- Natal positions (birth date if provided)
- Aspect table showing angular relationships

**Requires:** Proper `PlanetaryPosition` dataclass usage (see Pre-work).

#### 4. `ZodiacRing` (extends `Static`)

**PNG image widget** generated via `matplotlib` + `pillow`, rendered in-terminal via `textual-media` (`PILImage`). Shows:
- Zodiac sign glyphs arranged in a circle
- Planetary glyphs at their computed positions within the ring
- House cusps marked with degree indicators
- Ascendant (Asc) and Midheaven (MC) labeled on the horizontal/vertical axes
- Toggleable house system boundaries

If `textual-media` is unavailable or terminal doesn't support inline images, falls back to a **simplified tabular planetary list** (same data, no ring).

#### 5. `StatusBar` (extends `Static`)

Bottom bar with:
- Key bindings (F1:F5)
- Current mode indicator
- Seed hash (truncated)
- Timestamp

---

## Screens

### 1. `MainScreen` (primary dashboard)

Layout structure:

```
┌───────────────────────────────────────────────────────────────────┐
│ ╔═ ORBPONDERING ══════════════════════════════════ [Help] ≡ ╕   ║
│ ┃                                                                ┃ │
│ ┃ ┌─ Settings ────────────┐ ┌─ Spread View ───────────────────┐ ┃ │
│ ┃ │ Date:      2026-05-08 │ │                                 │ ┃ │
│ ┃ │ Lat:       40.7128    │ │        Three Card Spread        │ ┃ │
│ ┃ │ Lon:      -74.0060    │ │                                 │ ┃ │
│ ┃ │ Spread: three_card ▼ │ │   ┌─────┐ ┌─────┐ ┌─────┐      │ ┃ │
│ ┃ │ House: whole_sign  ▼ │ │   │  1  │ │  2  │ │  3  │      │ ┃ │
│ ┃ │                      │ │   │Past │ │Present│ │Future│      │ ┃ │
│ ┃ │ [Calculate Reading]  │ │   └─────┘ └─────┘ └─────┘      │ ┃ │
│ ┃ │                      │ │                                 │ ┃ │
│ ┃ │ [Toggle Natal Mode]  │ └─────────────────────────────────┘ ┃ │
│ ┃ └──────────────────────┘                                       ┃ │
│ ┃ ┌─ Chart Details ─────────┐ ┌─ Card Info ───────────────────┐ ┃ │
│ ┃ │ ☉ Sun: 17° Taurus ♉     │ │ The Sun ☉                     │ ┃ │
│ ┃ │ ☽ Moon: 3° Libra ♎      │ │ Position: Future              │ ┃ │
│ ┃ │ ☿ Mercury: 28° Aries ♈  │ │ Keywords: positivity, fun     │ ┃ │
│ ┃ │ ♀ Venus: 5° Gemini ♊    │ │ Orientation: Upright ↑        │ ┃ │
│ ┃ │ ...                      │ │ Element: 🔥 Fire              │ ┃ │
│ ┃ │ ♅ Asc: 12° Leo           │ │                               │ ┃ │
│ ┃ │ ♆ MC: 25° Cancer         │ │ [Interpretation...]           │ ┃ │
│ ┃ └─────────────────────────┘ └───────────────────────────────┘ ┃ │
│ ┃                                                                ┃ │
│ ╚══════════════════════════════════════════════════════════════╝ │
│ [F1:Help] [F2:Settings] [F3:Spread] [F4:Chart] [F5:Save] ESC:Quit
└───────────────────────────────────────────────────────────────────┘
```

Tab navigation between views:
- **Spread View** (default) – Visual card layout
- **Chart View** – Planetary positions table (ZodiacRing as optional enhancement)
- **Reading View** – Full interpretation and details
- **History** – Previously generated readings (if saved)

### 2. `SettingsScreen` (modal)

Modal form for inputting:

**Date/Time:**
- Reading date (default: today)
- Reading time (default: 12:00)

**Location:**
- Latitude
- Longitude
- ~~City lookup (optional, with autocomplete)~~ — **Moved to future work**

**Astrology:**
- House system (Whole Sign, Equal, Porphyry, Placidus)
- Spread type (Daily, Three Card, Celtic Cross)

**Natal Chart:**
- Enable natal chart mode (checkbox)
- Birth date
- Birth time
- Birth location (lat/lon)

**Display:**
- Color theme (default, dark, astro)
- Show seed hash (toggle)
- ~~Show educational steps (toggle)~~ — Education mode is CLI-only, incompatible with TUI

Buttons: `[Calculate]` `[Save Defaults]` `[Cancel]`

**Keybinding handling:** Input fields use `prevent = {"key"}` to suppress global bindings when focused. SettingsScreen has its own scoped BINDINGS (Tab, Enter, Esc).

### 3. `CardDetailView` (modal)

Expanded view when clicking/selecting a card:

```
┌─ The Tower ───────────────────────────────────┐
│                                               │
│   ┌─────────────────────────────────────┐   │
│   │         ASCII ART FRAME             │   │
│   │         (card image)                │   │
│   └─────────────────────────────────────┘   │
│                                               │
│ Arcana: Major                                 │
│ Position: Outcome                             │
│ Orientation: Reversed ↓                       │
│                                               │
│ Keywords:                                     │
│   sudden_change, upheaval, chaos              │
│                                               │
│ Element: 🔥 Fire                              │
│                                               │
│ [Interpretation...]                           │
│                                               │
│ [Close]  [Previous Card]  [Next Card]         │
└───────────────────────────────────────────────┘
```

**Resonant sign/planet fields removed** — moved to future work.

### 4. ~~`EducationScreen`~~ — **Moved to CLI-only, future work**

Education mode is not part of the TUI. Use `orbpondering --education` from CLI instead. TUI is incompatible with education mode for v1.

### 5. `ReadingHistoryScreen`

View past readings (persisted to file):
- List of readings by date
- Filter by spread type
- Filter by date range
- Click to replay full reading

**Requires:** Persistence layer (see Pre-work).

---

## Keyboard Navigation

Bindings are **scoped per screen** to avoid conflicts with SettingsScreen input fields:

```python
# Global (all screens)
BINDINGS = [
    ("q", "quit", "Quit"),
    ("f1", "help", "Help"),
    ("f2", "settings", "Settings"),
    ("f5", "save_reading", "Save Reading"),
]

# MainScreen only
MAIN_BINDINGS = [
    ("c", "calculate", "Calculate Reading"),
    ("tab", "cycle_views", "Cycle Between Views"),
    ("f3", "spread_view", "Spread View"),
    ("f4", "chart_view", "Chart View"),
    ("h", "history", "Reading History"),
    ("f6", "natal_toggle", "Toggle Natal Mode"),
]

# SpreadView (when focused)
SPREAD_BINDINGS = [
    ("n", "next_card", "Next Card in Spread"),
    ("p", "prev_card", "Previous Card in Spread"),
    ("r", "reveal_card", "Reveal/Flip Selected Card"),
]

# SettingsScreen (modal, isolated keymap)
SETTINGS_BINDINGS = [
    ("tab", "next_field", "Next Input"),
    ("shift+tab", "prev_field", "Prev Input"),
    ("enter", "submit", "Calculate / Save"),
    ("escape", "cancel", "Cancel"),
]
```

**SettingsScreen Input fields** use `prevent = {"key"}` to suppress all global bindings when typed into, preventing key collisions (e.g., typing "n" for latitude doesn't trigger "next_card").

---

## Animation Sequence (Card Reveal)

*(Simplified for v1 — full animations deferred to polish phase)*

1. Brief loading spinner while calculating
2. Card appears face-up (no flip animation in v1)
3. Position highlights
4. Card details appear in info panel

---

## Color Themes

### Default Theme

```css
MainScreen {
    background: $surface;
    layout: grid;
    grid-size: 2 4;
    grid-columns: 25% 1fr;
    grid-rows: 10% 1fr 15% 8%;
}

SettingsPanel {
    dock: left;
    background: $boost;
    padding: 1 2;
    border: tall $primary;
}

SpreadLayout {
    background: $surface;
    align: center middle;
}

CardWidget {
    border: heavy $primary;
    background: $surface-darken-1;
}

CardWidget:hover {
    border: heavy $accent;
    background: $surface-darken-2;
}

CardWidget.selected {
    border: double $warning;
}

CardWidget.reversed {
    opacity: 0.8;
}

PlanetaryPanel {
    border: tall $primary;
    padding: 1 2;
}

StatusBar {
    dock: bottom;
    background: $boost;
    color: $text-muted;
    padding: 0 2;
}
```

### Astro Theme (Dark Cosmic)

```python
ASTRO_THEME = {
    "background": "#0a0a1a",
    "surface": "#1a1a2e",
    "boost": "#16213e",
    "primary": "#6a5acd",
    "accent": "#ffd700",
    "warning": "#ff6b6b",
    "success": "#4ecdc4",
    "fire": "#ff6b6b",
    "water": "#4ecdc4", 
    "air": "#ffd93d",
    "earth": "#6bff6b",
}
```

---

## Data Flow & Integration

```
┌─────────────────────────────────────────────────────────────┐
│ Textual Event Loop                                           │
├───────────┬───────────────┬───────────────────────────────────┤
│ Settings  │ Calculate     │ Display                          │
│ Screen    │ Button Press  │                                  │
│           │               │                                  │
│ Collect   │ ┌───────────┐ │ ┌──────────────────────────────┐ │
│ Inputs ──▶│ draw.py     │─▶│ Screen Updates                 │ │
│           │             │ │ • SpreadLayout.populate()        │ │
│ - Date    │ daily_tarot │ │ • PlanetaryPanel.update()        │ │
│ - Loc     │ birth_tarot │ │ • CardWidget.reveal()            │ │
│ - Spread  │ seed -> cards│ │ • StatusBar.set_seed()           │ │
│ - House   │             │ │                                  │ │
│ - Natal   │ Returns     │ └────────────────────────────────┘ │
│           │ TarotReading│                                  │
│           └───────────┘                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## Dependencies to Add

```toml
textual = ">=0.47.0"
rich = ">=13.0"  # Keep for fallback
textual-dev = ">=1.2.0"  # For development
textual-media = ">=0.2.0"  # For inline image display (zodiac ring)
matplotlib = ">=3.8.0"  # For zodiac ring image generation
pillow = ">=10.0"  # Image processing for matplotlib/textual-media
```

---

## Pre-work (Phase 0)

Before any TUI widget code, these foundational fixes are required:

### 0.1 Fix `compute_chart()` to use proper `PlanetaryPosition` dataclass

- **File:** `src/orbpondering/draw.py:68-70`
- **Problem:** Currently creates ad-hoc objects via `type()` instead of using the `PlanetaryPosition` dataclass from `models.py:17`. These objects lack `zodiac_sign: ZodiacSign` which the TUI needs.
- **Fix:** Replace the `type()` construct with proper `PlanetaryPosition(...)` instantiation.

### 0.2 Add card reversal logic to the draw pipeline

- **File:** `src/orbpondering/draw.py` and `src/orbpondering/cards.py`
- **Problem:** `Card.upright` field always defaults to `True` — no code randomizes it.
- **Fix:** Add an `--reversed` CLI flag (default: off). When enabled, randomly assign `upright` to ~30-50% of drawn cards during `_shuffle_and_deal()`. TUI only displays orientation indicator when reversal is enabled.

### 0.3 Build persistence layer for reading history

- **Storage:** JSON files in `~/.config/orbpondering/readings/`
- **Serialization:** Add `to_dict()` / `from_dict()` methods to `TarotReading` and `CardPosition` dataclasses
- **Features:**
  - Save a reading to file
  - List readings by date
  - Load a reading by date
  - Delete readings

### 0.4 Build settings/config persistence

- **Storage:** TOML/JSON file at `~/.config/orbpondering/config.toml`
- **Features:**
  - Save user defaults (lat/lon, house system, spread type, theme)
  - Load defaults on app start
  - "Save Defaults" button in SettingsScreen writes to this file
  - CLI `--config` flag to override path

### 0.5 Ephemeris caching

- **Problem:** `jplephem` downloads ~hundreds of MB on first run
- **Fix:** Cache ephemeris data in `~/.config/orbpondering/cache/ephemeris/`. Detect cached data on startup and skip download if available. Show loading indicator during first-run download.

### 0.6 Add service/validation layer

- **Problem:** TUI needs input validation, error handling, and partial results — `draw.py` is tightly coupled to `datetime` inputs
- **Fix:** Add `src/orbpondering/service.py`:
  - Validate lat ([-90, 90]), lon ([-180, 180]), dates
  - Handle ephemeris errors gracefully (date out of range)
  - Wraps `compute_chart()` with try/except, returns structured error objects
  - Supports cancellation signaling

---

## Implementation Phases

0. **Phase 0: Foundation** (Pre-work)
   - Fix `PlanetaryPosition` dataclass usage in `compute_chart()`
   - Add `--reversed` CLI flag and reversal logic to draw pipeline
   - Build persistence layer (JSON file storage for readings)
   - Build config persistence (TOML settings file)
   - Ephemeris caching in `~/.config/orbpondering/cache/`
   - Add service/validation layer (`service.py`)

1. **Phase 1: Core TUI Skeleton**
   - Textual `App` class with screen routing (MainScreen, SettingsScreen, CardDetailView, ReadingHistoryScreen)
   - Basic `CardWidget` displaying name, arcana, suit, orientation (when `--reversed` active)
   - Settings modal with `Input` widgets for date/lat/lon/house system/spread type
   - Keyboard navigation with scoped bindings
   - Calculate reading button wired to `service.py` → `draw.py`

2. **Phase 2: Spread Visualization**
   - `SpreadLayout` widget with Daily and Three Card layouts
   - Grid-based `CardWidget` positioning
   - Card reveal flow (spinner → card appears → detail panel updates)
   - `PlanetaryPanel` widget showing transit positions

3. **Phase 3: Celtic Cross + Zodiac Ring**
   - Celtic Cross layout in `SpreadLayout` using 2D grid with empty spacer widgets
   - `ZodiacRing` widget generating PNG via `matplotlib` + `pillow`, rendered via `textual-media`
   - `CardDetailView` modal with full card details
   - Tab navigation between Spread/Chart/Reading/History views

4. **Phase 4: Natal Mode + History**
   - Toggle between transit-only and natal+transit modes
   - `ReadingHistoryScreen` with list, filter, load, delete
   - `Save Defaults` button in SettingsScreen writing to config file
   - Aspect table in PlanetaryPanel

5. **Phase 5: Polish**
   - Color themes (Default, Astro)
   - Loading indicators for ephemeris download and chart computation
   - Error dialogs for invalid inputs
   - Responsive layout for narrow terminals (min 60 cols for Daily/Three-card, min 100 cols for Celtic Cross)
   - Animation enhancements (card flip, fade-in)

---

## What This Transforms

The Textual TUI will complement the current Rich console output with:
- Full interactive terminal UI (vs. one-shot print)
- Visual spread layouts (vs. tables)
- Organized astrological chart panels
- Keyboard/mouse navigation through readings
- Persistent settings and reading history
- Multiple visual themes

The CLI remains the primary entry point. TUI is activated via `orbpondering --tui`. Education mode remains CLI-only (incompatible with TUI for v1).

---

## Future Work (Not in Scope for v1)

- City lookup with autocomplete for geocoding
- `CardPosition.resonant_sign` and `resonant_planet` population
- `_infer_house_index()` improvement (floating point comparison fix)
- Education mode step-through within TUI
- Full card flip animations
- Advanced accessibility features (screen reader optimization)
