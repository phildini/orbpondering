"""CLI entry point for daily tarot draws."""

from __future__ import annotations

import argparse
import datetime
import sys

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from orbpondering.constants import HouseSystem
from orbpondering.draw import tarot_draw_for_date
from orbpondering.display import display_spread


def main(argv: list[str] | None = None) -> int:
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
        help="Spread name (daily, three_card, celtic_cross)",
    )
    parser.add_argument(
        "--education", "-e",
        action="store_true",
        help="Educational mode: walk through calculations step by step",
    )
    args = parser.parse_args(argv)

    dt = datetime.date.fromisoformat(args.date)
    house = HouseSystem(args.house)

    if args.education:
        # Run in educational mode
        from orbpondering.education.engine import run_education
        console = Console()
        console.print("[bold blue]✦ ORBPONDERING EDUCATION MODE ✦[/]\n")
        result = run_education(
            dt, args.lat, args.lon, house, args.spread, console
        )
        # Display final result
        display_spread(result)
    else:
        # Standard mode with progress bar
        console = Console()
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
        ) as progress:
            task1 = progress.add_task("[cyan]Calculating planetary positions...", total=100)
            task2 = progress.add_task("[green]Computing house cusps...", total=100)
            task3 = progress.add_task("[blue]Determining chart data...", total=100)
            task4 = progress.add_task("[magenta]Drawing tarot cards...", total=100)
            
            # Actually perform the computation
            draw = tarot_draw_for_date(
                dt, lat=args.lat, lon=args.lon, house_system=house, spread_name=args.spread
            )
            
            # Complete all tasks
            progress.update(task1, completed=100)
            progress.update(task2, completed=100)
            progress.update(task3, completed=100)
            progress.update(task4, completed=100)
        
        # Display final result
        display_spread(draw)

    return 0


if __name__ == "__main__":
    sys.exit(main())