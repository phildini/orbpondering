"""Individual educational steps."""

from __future__ import annotations

from rich.console import Console


def _get_zodiac_sign(deg: float):
    """Map ecliptic longitude to zodiac sign."""
    from orbpondering.constants import ZodiacSign
    
    normalized = deg % 360.0
    for sign in ZodiacSign:
        if sign.start_deg <= normalized < sign.end_deg:
            return sign
    return ZodiacSign.PISCES


def step_planetary_positions(console: Console, ctx: dict, verbose: bool) -> None:
    """Calculate and display where each planet is today."""
    from orbpondering.astronomy import planetary_positions
    
    ctx["planetary_positions"] = planetary_positions(ctx["date"])
    
    console.print(f"\n[bold cyan]STEP 1: Planetary Positions[/]")
    console.print(f"[dim]Looking up where each planet sits in the sky at noon UTC[/]")
    console.print(f"[dim]for {ctx['date'].strftime('%B %d, %Y')}...[/]\n")
    
    planet_symbols = {
        "sun": "\u2609",
        "moon": "\u263D", 
        "mercury": "\u263F",
        "venus": "\u2640",
        "mars": "\u2642",
        "jupiter": "\u2643",
        "saturn": "\u2644",
        "uranus": "\u2645",
        "neptune": "\u2646",
        "pluto": "\u2647",
    }
    
    for body, deg in ctx["planetary_positions"].items():
        symbol = planet_symbols.get(body, body[0].upper())
        sign = _get_zodiac_sign(deg)
        console.print(f"  {symbol}  {body:>9s} \u2192 {deg:>6.1f}\u00b0  \u2192  {sign.symbol} {sign.full_name} ({deg % 30:.1f}\u00b0)")
    
    if not verbose:
        _print_synthesis(ctx["planetary_positions"], console)


def step_sidereal_time(console: Console, ctx: dict, verbose: bool) -> None:
    """Calculate and display sidereal time and angles."""
    from orbpondering.astronomy import sidereal_time, ascendant, midheaven
    
    lst = sidereal_time(ctx["date"], ctx["lon"])
    asc = ascendant(ctx["date"], ctx["lat"], ctx["lon"])
    mc = midheaven(ctx["date"], ctx["lat"], ctx["lon"])
    
    ctx["ascendant"] = asc
    ctx["midheaven"] = mc
    
    console.print(f"\n[bold cyan]STEP 2: Sidereal Time & Angles[/]")
    console.print(f"[dim]The Sidereal Time tells us which part of the zodiac[/]")
    console.print(f"[dim]is rising at your location.[/]\n")
    console.print(f"  Local Sidereal Time: {lst:.1f}\u00b0")
    console.print(f"  Ascendant (rising):  {asc:.1f}\u00b0 \u2192 {_get_zodiac_sign(asc).symbol} {_get_zodiac_sign(asc).full_name}")
    console.print(f"  Midheaven (zenith):  {mc:.1f}\u00b0 \u2192 {_get_zodiac_sign(mc).symbol} {_get_zodiac_sign(mc).full_name}")


def step_house_cusps(console: Console, ctx: dict, verbose: bool) -> None:
    """Calculate and display house cusps."""
    from orbpondering.houses import house_cusps
    
    cusps = house_cusps(ctx["date"], ctx["lat"], ctx["lon"], ctx["house_system"])
    ctx["house_cusps"] = cusps
    
    console.print(f"\n[bold cyan]STEP 3: {ctx['house_system'].value.replace('_', ' ').title()} House Cusps[/]")
    console.print(f"[dim]Dividing the sky into 12 houses based on the Ascendant and Midheaven.[/]\n")
    
    house_titles = [
        "Self", "Resources", "Communication", "Home",
        "Creativity", "Health", "Partnerships", "Transformation",
        "Philosophy", "Career", "Friendships", "Subconscious"
    ]
    for i, cusp in enumerate(cusps, 1):
        sign = _get_zodiac_sign(cusp)
        console.print(f"  H{i:<2d}  {cusp:>6.1f}\u00b0  \u2192  {sign.symbol} {sign.full_name}  [{house_titles[i-1]}]")


def step_planets_in_houses(console: Console, ctx: dict, verbose: bool) -> None:
    """Map planets to houses."""
    from orbpondering.houses import house_cusps
    
    cusps = house_cusps(ctx["date"], ctx["lat"], ctx["lon"], ctx["house_system"])
    
    planets_in_houses = {}
    for planet, deg in ctx["planetary_positions"].items():
        house_num = int(deg // 30) + 1
        planets_in_houses[planet] = house_num
    
    ctx["planets_in_houses"] = planets_in_houses
    
    console.print(f"\n[bold cyan]STEP 4: Planets in Houses[/]")
    console.print(f"[dim]Mapping each planet to its corresponding house.[/]\n")
    
    planet_symbols = {
        "sun": "\u2609",
        "moon": "\u263D", 
        "mercury": "\u263F",
        "venus": "\u2640",
        "mars": "\u2642",
        "jupiter": "\u2643",
        "saturn": "\u2644",
        "uranus": "\u2645",
        "neptune": "\u2646",
        "pluto": "\u2647",
    }
    
    for planet, house_num in planets_in_houses.items():
        planet_deg = ctx["planetary_positions"][planet]
        sign = _get_zodiac_sign(planet_deg)
        symbol = planet_symbols.get(planet, planet[0].upper())
        console.print(f"  {symbol}  {planet:>9s} in H{house_num:<2d} \u2192 {sign.symbol} {sign.full_name}")


def step_seed_generation(console: Console, ctx: dict, verbose: bool) -> None:
    """Show how the deterministic seed is generated."""
    from orbpondering.seed import chart_seed
    
    seed = chart_seed(ctx["date"], ctx["lat"], ctx["lon"], ctx["house_system"])
    ctx["seed"] = seed
    
    console.print(f"\n[bold cyan]STEP 5: Generating the Seed[/]")
    console.print(f"[dim]Combining all chart data into a single SHA-256 hash.[/]\n")
    console.print(f"  Planetary positions + house cusps \u2192 JSON \u2192 SHA-256")
    console.print(f"  Seed: {seed:016x}")
    console.print(f"  [dim]This uniquely identifies today's astrological configuration.[/dim]")


def step_card_draw(console: Console, ctx: dict, verbose: bool) -> None:
    """Draw cards and display with education context."""
    from orbpondering.draw import daily_tarot_draw, get_spread
    from orbpondering.education.content import SPREAD_POSITIONS
    
    spread = get_spread(ctx["spread_name"])
    ctx["card_draw"] = daily_tarot_draw(
        ctx["date"], ctx["lat"], ctx["lon"], ctx["house_system"], spread
    )
    
    console.print(f"\n[bold cyan]STEP 6: Drawing the Cards[/]")
    console.print(f"[dim]Using the astrological seed to deterministically draw cards.[/]\n")
    console.print(f"  Spread: {spread.name}")
    console.print(f"  Cards to draw: {len(spread.positions)}")
    console.print()
    
    for pos in ctx["card_draw"]["positions"]:
        _render_card_with_context(pos, ctx, console)


def _print_synthesis(positions: dict[str, float], console: Console) -> None:
    """Print a brief synthesis of the planetary positions."""
    elements = {"fire": 0, "earth": 0, "air": 0, "water": 0}
    for deg in positions.values():
        sign = _get_zodiac_sign(deg)
        elements[sign.element] += 1
    
    dominant = max(elements, key=elements.get)
    console.print(f"\n[italic]Today's chart is dominated by {dominant} energy ({elements[dominant]} planets). "
                  f"Fire: {elements['fire']}, Earth: {elements['earth']}, "
                  f"Air: {elements['air']}, Water: {elements['water']}[/italic]")


def _render_card_with_context(pos: dict, ctx: dict, console: Console) -> None:
    """Render a card with contextual astrological information."""
    card = pos["card"]
    position_label = pos["position_label"]
    
    if card.arcana.value == "major":
        console.print(f"  \u2726 [bold white]{position_label}:[/] [bold red]{card.name}[/] { '\u2191' if card.upright else '\u2193'}")
    else:
        suit_symbol = card.suit.symbol if card.suit else ""
        console.print(f"  \u2727 [bold white]{position_label}:[/] [{_get_suit_color(card.suit)}]{suit_symbol}[/] {card.name} { '\u2191' if card.upright else '\u2193'}")
    
    keywords = ", ".join(card.keywords) if card.keywords else "No keywords"
    console.print(f"      [italic dim]{keywords}[/italic dim]")
    
    if ctx.get("planetary_positions") and card.arcana.value == "minor" and card.suit:
        for planet, deg in ctx["planetary_positions"].items():
            planet_sign = _get_zodiac_sign(deg)
            if planet_sign.element == card.suit.element:
                console.print(f"      [dim]Resonates with {planet} in {planet_sign.full_name}[/dim]")
                break


def _get_suit_color(suit) -> str:
    """Get Rich color for suit."""
    if not suit:
        return "white"
    colors = {
        "wands": "bright_red",
        "cups": "bright_blue",
        "swords": "bright_white",
        "pentacles": "bright_yellow",
    }
    return colors.get(suit.full_name.lower(), "white")
