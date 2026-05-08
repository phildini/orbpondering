"""CLI entry point for daily tarot draws."""

from __future__ import annotations

import argparse
import datetime
import sys
from datetime import date, time

from orbpondering.constants import HouseSystem
from orbpondering.display import display_reading
from orbpondering.draw import birth_tarot_draw, daily_tarot_draw, tarot_draw_for_date
from orbpondering.models import BirthData
from orbpondering.spreads import SPREADS


def _try_import_rich():
    try:
        from rich.console import Console
        from rich.progress import Progress, SpinnerColumn, TextColumn

        return Console, Progress, SpinnerColumn, TextColumn
    except ImportError:
        return None, None, None, None


def _parse_time(time_str: str | None) -> time | None:
    """Parse time string in HH:MM format."""
    if not time_str:
        return None
    try:
        h, m = map(int, time_str.split(":"))
        return time(h, m)
    except (ValueError, TypeError):
        raise argparse.ArgumentTypeError(f"Invalid time format: {time_str}. Use HH:MM")


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
    parser.add_argument(
        "--reversed",
        "-r",
        action="store_true",
        help="Draw cards in reversed position",
    )
    # Birth data arguments
    parser.add_argument(
        "--birth-date",
        type=str,
        help="Birth date (YYYY-MM-DD) to enable natal chart mode",
    )
    parser.add_argument(
        "--birth-time",
        type=str,
        help="Birth time (HH:MM) - optional, defaults to noon UTC",
    )
    parser.add_argument(
        "--birth-zone",
        type=str,
        help="Birth timezone (IANA format) - optional, defaults to UTC",
    )
    parser.add_argument(
        "--birth-lat",
        type=float,
        help="Birth latitude",
    )
    parser.add_argument(
        "--birth-lon",
        type=float,
        help="Birth longitude",
    )
    args = parser.parse_args(argv)

    try:
        dt = datetime.date.fromisoformat(args.date)
    except ValueError as exc:
        print(f"Error: Invalid date format '{args.date}'. Use YYYY-MM-DD.", file=sys.stderr)
        return 1

    house = HouseSystem(args.house)

    # Check for natal chart arguments
    if args.birth_date:
        # Validate required birth arguments
        if args.birth_lat is None or args.birth_lon is None:
            print("Error: --birth-lat and --birth-lon are required when using --birth-date", file=sys.stderr)
            return 1
        
        try:
            birth_date = datetime.date.fromisoformat(args.birth_date)
        except ValueError as exc:
            print(f"Error: Invalid birth date format '{args.birth_date}'. Use YYYY-MM-DD.", file=sys.stderr)
            return 1
            
        birth_time = _parse_time(args.birth_time)
        birth_tz = args.birth_zone
        
        birth_data = BirthData(
            date=birth_date,
            time=birth_time,
            lat=args.birth_lat,
            lon=args.birth_lon,
            tz=birth_tz,
        )
        
        # Use birth tarot draw
        spread = SPREADS[args.spread]
        if Console and args.education:
            from orbpondering.education.engine import run_education_with_natal
            
            console = Console()
            console.print("[bold blue]✦ ORBPONDERING EDUCATION MODE ✦[/]\n")
            result = run_education_with_natal(
                d=dt,
                lat=args.lat,
                lon=args.lon,
                house_system=house,
                spread_name=args.spread,
                birth_data=birth_data,
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

                reading = birth_tarot_draw(
                    d=dt,
                    lat=args.lat,
                    lon=args.lon,
                    birth_data=birth_data,
                    house_system=house,
                    spread_name=args.spread,
                    reversed_cards=args.reversed,
                )

                progress.update(task1, completed=100)
                progress.update(task2, completed=100)
                progress.update(task3, completed=100)
                progress.update(task4, completed=100)

            display_reading(reading)
        else:
            print("Rich is not installed. Install with: pip install rich", file=sys.stderr)
            reading = birth_tarot_draw(
                d=dt,
                lat=args.lat,
                lon=args.lon,
                birth_data=birth_data,
                house_system=house,
                spread_name=args.spread,
                reversed_cards=args.reversed,
            )
            for pos in reading.positions:
                print(f"{pos.position_label}: {pos.card.name}")
    else:
        # Regular daily mode
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
                    reversed_cards=args.reversed,
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
                reversed_cards=args.reversed,
            )
            for pos in reading.positions:
                print(f"{pos.position_label}: {pos.card.name}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
