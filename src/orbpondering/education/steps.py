"""Individual educational steps."""

from __future__ import annotations

from rich.console import Console

from orbpondering.utils import PLANET_SYMBOLS, zodiac_sign_for_degree


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


def step_birth_data(console: Console, ctx: dict, verbose: bool) -> None:

    birth_data = ctx["birth_data"]

    console.print("\n[bold cyan]STEP 0: Birth Data[/]")
    console.print(
        "[dim]Your birth information entered for natal chart calculations[/]"
    )
    console.print(f"[dim]for {birth_data.date.strftime('%B %d, %Y')}[/]")

    if birth_data.time:
        console.print(f"  Birth Time: {birth_data.time.strftime('%H:%M')} UTC")
    else:
        console.print("  Birth Time: Noon UTC (approximate)")
    console.print(f"  Birth Place: {birth_data.lat:.2f}° N, {birth_data.lon:.2f}° E")
    if birth_data.tz:
        console.print(f"  Timezone: {birth_data.tz}")


def step_natal_positions(console: Console, ctx: dict, verbose: bool) -> None:
    from orbpondering.draw import compute_natal_chart

    birth_data = ctx["birth_data"]
    natal_chart = compute_natal_chart(birth_data)
    ctx["natal_positions"] = natal_chart.planetary_positions

    console.print("\n[bold cyan]STEP 1: Natal Planetary Positions[/]")
    console.print("[dim]Where each planet was positioned at your birth[/]")
    console.print(f"[dim]for {birth_data.date.strftime('%B %d, %Y')}[/]\n")

    for body, deg in ctx["natal_positions"].items():
        symbol = PLANET_SYMBOLS.get(body, body[0].upper())
        sign = zodiac_sign_for_degree(deg)
        console.print(
            f"  {symbol}  {body:>9s} \u2192 {deg:>6.1f}\u00b0  \u2192  "
            f"{sign.symbol} {sign.full_name} ({deg % 30:.1f}\u00b0)"
        )


def step_natal_houses(console: Console, ctx: dict, verbose: bool) -> None:
    from orbpondering.draw import compute_natal_chart

    birth_data = ctx["birth_data"]
    natal_chart = compute_natal_chart(birth_data)
    ctx["natal_house_cusps"] = natal_chart.house_cusps

    console.print("\n[bold cyan]STEP 2: Natal House Cusps[/]")
    console.print("[dim]12 house boundaries based on your birth chart[/]\n")

    for house_system, cusps in natal_chart.house_cusps.items():
        console.print(f"  {house_system.value.replace('_', ' ').title()}:")
        house_titles = [
            "Self",
            "Resources",
            "Communication",
            "Home",
            "Creativity",
            "Health",
            "Partnerships",
            "Transformation",
            "Philosophy",
            "Career",
            "Friendships",
            "Subconscious",
        ]
        for idx, cusp in enumerate(cusps, 1):
            sign = zodiac_sign_for_degree(cusp)
            console.print(
                f"    H{idx:<2d}  {cusp:>6.1f}\u00b0  \u2192  "
                f"{sign.symbol} {sign.full_name}  [{house_titles[idx - 1]}]"
            )
        console.print()


def step_planetary_positions(console: Console, ctx: dict, verbose: bool) -> None:
    from orbpondering.astronomy import planetary_positions

    ctx["planetary_positions"] = planetary_positions(ctx["date"])

    console.print("\n[bold cyan]STEP 3: Planetary Positions[/]")
    console.print("[dim]Looking up where each planet sits in the sky at noon UTC[/]")
    console.print(f"[dim]for {ctx['date'].strftime('%B %d, %Y')}...[/]\n")

    for body, deg in ctx["planetary_positions"].items():
        symbol = PLANET_SYMBOLS.get(body, body[0].upper())
        sign = zodiac_sign_for_degree(deg)
        console.print(
            f"  {symbol}  {body:>9s} \u2192 {deg:>6.1f}\u00b0  \u2192  "
            f"{sign.symbol} {sign.full_name} ({deg % 30:.1f}\u00b0)"
        )

    if not verbose:
        _print_synthesis(ctx["planetary_positions"], console)


def step_sidereal_time(console: Console, ctx: dict, verbose: bool) -> None:
    from orbpondering.astronomy import ascendant, midheaven, sidereal_time

    lst = sidereal_time(ctx["date"], ctx["lon"])
    asc = ascendant(ctx["date"], ctx["lat"], ctx["lon"])
    mc = midheaven(ctx["date"], ctx["lat"], ctx["lon"])

    ctx["ascendant"] = asc
    ctx["midheaven"] = mc

    console.print("\n[bold cyan]STEP 4: Sidereal Time & Angles[/]")
    console.print("[dim]The Sidereal Time tells us which part of the zodiac[/]")
    console.print("[dim]is rising at your location.[/]\n")
    console.print(f"  Local Sidereal Time: {lst:.1f}\u00b0")
    console.print(
        f"  Ascendant (rising):  {asc:.1f}\u00b0 \u2192 "
        f"{zodiac_sign_for_degree(asc).symbol} {zodiac_sign_for_degree(asc).full_name}"
    )
    console.print(
        f"  Midheaven (zenith):  {mc:.1f}\u00b0 \u2192 "
        f"{zodiac_sign_for_degree(mc).symbol} {zodiac_sign_for_degree(mc).full_name}"
    )


def step_house_cusps(console: Console, ctx: dict, verbose: bool) -> None:
    from orbpondering.houses import house_cusps

    cusps = house_cusps(ctx["date"], ctx["lat"], ctx["lon"], ctx["house_system"])
    ctx["house_cusps"] = cusps

    console.print(
        f"\n[bold cyan]STEP 5: {ctx['house_system'].value.replace('_', ' ').title()} House Cusps[/]"
    )
    console.print(
        "[dim]Dividing the sky into 12 houses based on the "
        "Ascendant and Midheaven.[/]\n"
    )

    house_titles = [
        "Self",
        "Resources",
        "Communication",
        "Home",
        "Creativity",
        "Health",
        "Partnerships",
        "Transformation",
        "Philosophy",
        "Career",
        "Friendships",
        "Subconscious",
    ]
    for idx, cusp in enumerate(cusps, 1):
        sign = zodiac_sign_for_degree(cusp)
        console.print(
            f"  H{idx:<2d}  {cusp:>6.1f}\u00b0  \u2192  "
            f"{sign.symbol} {sign.full_name}  [{house_titles[idx - 1]}]"
        )


def step_planets_in_houses(console: Console, ctx: dict, verbose: bool) -> None:
    cusps = ctx.get("house_cusps", [])
    planets_in_houses = {}

    for planet, deg in ctx["planetary_positions"].items():
        house_num = 0
        for idx, cusp in enumerate(cusps):
            if deg >= cusp and (idx + 1 == len(cusps) or deg < cusps[idx + 1]):
                house_num = idx + 1
                break
        planets_in_houses[planet] = house_num if house_num else 1

    ctx["planets_in_houses"] = planets_in_houses

    console.print("\n[bold cyan]STEP 6: Planets in Houses[/]")
    console.print("[dim]Mapping each planet to its corresponding house.[/]\n")

    for planet, house_num in planets_in_houses.items():
        planet_deg = ctx["planetary_positions"][planet]
        sign = zodiac_sign_for_degree(planet_deg)
        symbol = PLANET_SYMBOLS.get(planet, planet[0].upper())
        console.print(
            f"  {symbol}  {planet:>9s} in H{house_num:<2d} \u2192 "
            f"{sign.symbol} {sign.full_name}"
        )


def step_aspects(console: Console, ctx: dict, verbose: bool) -> None:
    from orbpondering.aspects import find_aspects
    from orbpondering.draw import compute_chart, compute_natal_chart

    birth_data = ctx["birth_data"]

    transit_chart = compute_chart(
        ctx["date"], ctx["lat"], ctx["lon"], ctx["house_system"]
    )
    natal_chart = compute_natal_chart(birth_data)
    aspects = find_aspects(natal_chart, transit_chart)
    ctx["aspects"] = aspects

    console.print("\n[bold cyan]STEP 7: Natal-Transit Aspects[/]")
    console.print(
        "[dim]Angular relationships between your natal chart and today's transits[/]\n"
    )

    if aspects:
        for aspect in aspects:
            console.print(
                f"  {aspect.natal_body} {aspect.transit_body}: "
                f"{aspect.separation:.1f}\u00b0 separation "
                f"({aspect.aspect_type.name.lower()}, orb: {aspect.orb:.1f}\u00b0)"
            )
    else:
        console.print("  No significant aspects detected.")


def step_seed_generation(console: Console, ctx: dict, verbose: bool) -> None:
    from orbpondering.draw import compute_natal_chart
    from orbpondering.seed import chart_seed

    birth_data = ctx.get("birth_data")
    aspects = ctx.get("aspects", ())

    seed = chart_seed(
        ctx["date"],
        ctx["lat"],
        ctx["lon"],
        ctx["house_system"],
        natal_chart=compute_natal_chart(birth_data) if birth_data else None,
        aspects=aspects,
        tz=birth_data.tz if birth_data else None,
    )
    ctx["seed"] = seed

    console.print("\n[bold cyan]STEP 8: Generating the Seed[/]")
    console.print("[dim]Combining all chart data into a single SHA-256 hash[/]\n")
    console.print(
        "  Planetary positions + house cusps + natal planets + aspects \u2192 JSON \u2192 SHA-256"
    )
    console.print(f"  Seed: {seed:016x}")
    console.print(
        "  [dim]This uniquely identifies today's astrological configuration.[/dim]"
    )


def step_card_draw(console: Console, ctx: dict, verbose: bool) -> None:
    from orbpondering.draw import birth_tarot_draw, daily_tarot_draw
    from orbpondering.spreads import get_spread

    spread = get_spread(ctx["spread_name"])

    if "birth_data" in ctx:
        # Natal mode

        birth_data = ctx["birth_data"]
        ctx["card_draw"] = birth_tarot_draw(
            ctx["date"],
            ctx["lat"],
            ctx["lon"],
            birth_data,
            ctx["house_system"],
            spread,
        )
    else:
        # Regular mode
        ctx["card_draw"] = daily_tarot_draw(
            ctx["date"],
            ctx["lat"],
            ctx["lon"],
            ctx["house_system"],
            spread,
        )

    console.print("\n[bold cyan]STEP 9: Drawing the Cards[/]")
    console.print(
        "[dim]Using the astrological seed to deterministically draw cards.[/]\n"
    )
    console.print(f"  Spread: {spread.name}")
    console.print(f"  Cards to draw: {len(spread.positions)}")
    console.print()

    for pos in ctx["card_draw"].positions:
        _render_card_with_context(pos, ctx, console)


def _print_synthesis(positions: dict[str, float], console: Console) -> None:
    elements = {"fire": 0, "earth": 0, "air": 0, "water": 0}
    for deg in positions.values():
        sign = zodiac_sign_for_degree(deg)
        elements[sign.element] += 1

    dominant = max(elements, key=elements.get)
    console.print(
        f"\n[italic]Today's chart is dominated by {dominant} energy "
        f"({elements[dominant]} planets). "
        f"Fire: {elements['fire']}, Earth: {elements['earth']}, "
        f"Air: {elements['air']}, Water: {elements['water']}[/italic]"
    )


def _render_card_with_context(pos: object, ctx: dict, console: Console) -> None:
    card = pos.card
    position_label = pos.position_label
    arrow = "\u2191" if getattr(card, "upright", True) else "\u2193"

    if card.arcana.value == "major":
        console.print(
            f"  \u2726 [bold white]{position_label}:[/] "
            f"[bold red]{card.name}[/] "
            f"{arrow}"
        )
    else:
        suit_symbol = getattr(card.suit, "symbol", "")
        console.print(
            f"  \u2727 [bold white]{position_label}:[/] "
            f"[_get_suit_color(card.suit)]{suit_symbol}[/] {card.name} "
            f"{arrow}"
        )

    keywords = ", ".join(card.keywords) if card.keywords else "No keywords"
    console.print(f"      [italic dim]{keywords}[/italic dim]")

    if ctx.get("planetary_positions") and card.arcana.value == "minor" and card.suit:
        for planet, deg in ctx["planetary_positions"].items():
            planet_sign = zodiac_sign_for_degree(deg)
            if planet_sign.element == card.suit.element:
                console.print(
                    f"      [dim]Resonates with {planet} in {planet_sign.full_name}[/dim]"
                )
                break
