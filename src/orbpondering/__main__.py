"""CLI entry point for daily tarot draws."""

from __future__ import annotations

import argparse
import datetime
import sys

from orbpondering.constants import HouseSystem
from orbpondering.display import display_reading
from orbpondering.draw import tarot_draw_for_date
from orbpondering.spreads import SPREADS


def _try_import_rich():
    try:
        from rich.console import Console
        from rich.progress import Progress, SpinnerColumn, TextColumn

        return Console, Progress, SpinnerColumn, TextColumn
    except ImportError:
        return None, None, None, None


def main(argv: list[str] | None = None) -> int:
    Console, Progress, SpinnerColumn, TextColumn = _try_import_rich()
    
    parser = argparse.ArgumentParser(
        description="Daily tarot draw seeded by astrological chart"
    )
    parser.add_argument(
        "date",
        nargs="?",
        default=str(datetime.date.today()),
        help="ISO date (YYYY-MM-DD). Default: today",
    )
    parser.add_argument("--lat", type=float, default=0.0, help="Observer latitude")
    parser.add_argument("--lon", type=float, default=0.0, help="Observer longitude")
    parser.add_argument(
        "--house",
        type=str,
        default=HouseSystem.WHOLE_SIGN.value,
        choices=[h.value for h in HouseSystem],
        help="House system",
    )
    parser.add_argument(
        "--spread",
        type=str,
        default="daily",
        choices=list(SPREADS),
        help="Spread name",
    )
    parser.add_argument(
        "--education",
        "-e",
        action="store_true",
        help="Educational mode: walk through calculations step by step",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Verbose educational output",
    )
    args = parser.parse_args(argv)

    try:
        dt = datetime.date.fromisoformat(args.date)
    except ValueError as exc:
        print(f"Error: Invalid date format '{args.date}'. Use YYYY-MM-DD.", file=sys.stderr)
        return 1

    house = HouseSystem(args.house)

    if Console and args.education:
        from orbpondering.education.engine import run_education

        console = Console()
        console.print("[bold blue]✦ ORBPONDERING EDUCATION MODE ✦[/]\n")
        result = run_education(
            d=dt,
            lat=args.lat,
            lon=args.lon,
            house_system=house,
            spread_name=args.spread,
            console=console,
            verbose=args.verbose,
        )
        display_reading(result)
    elif Progress:
        console = Console()
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
        ) as progress:
            task1 = progress.add_task("[cyan]Calculating planetary positions...", total=100)
            task2 = progress.add_task("[green]Computing house cusps...", total=100)
            task3 = progress.add_task("[blue]Determining chart data...", total=100)
            task4 = progress.add_task("[magenta]Drawing tarot cards...", total=100)

            reading = tarot_draw_for_date(
                d=dt,
                lat=args.lat,
                lon=args.lon,
                house_system=house,
                spread_name=args.spread,
            )

            progress.update(task1, completed=100)
            progress.update(task2, completed=100)
            progress.update(task3, completed=100)
            progress.update(task4, completed=100)

        display_reading(reading)
    else:
        print("Rich is not installed. Install with: pip install rich", file=sys.stderr)
        reading = tarot_draw_for_date(
            d=dt,
            lat=args.lat,
            lon=args.lon,
            house_system=house,
            spread_name=args.spread,
        )
        for pos in reading.positions:
            print(f"{pos.position_label}: {pos.card.name}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
