"""CLI entry point for Orbpondering."""

import argparse
import sys
from datetime import date, datetime

import click

from orbpondering.constants import HouseSystem
from orbpondering.display import display_reading
from orbpondering.draw import (
    birth_tarot_draw,
    tarot_draw_for_date,
)
from orbpondering.models import BirthData


@click.command()
@click.version_option()
@click.argument("date", required=False)
@click.option(
    "--lat",
    type=float,
    default=0.0,
    help="Latitude for astrological calculations (default: 0.0)",
)
@click.option(
    "--lon",
    type=float,
    default=0.0,
    help="Longitude for astrological calculations (default: 0.0)",
)
@click.option(
    "--house",
    type=click.Choice([hs.value for hs in HouseSystem], case_sensitive=False),
    default=HouseSystem.WHOLE_SIGN.value,
    help="House system to use for astrological calculations (default: whole_sign)",
)
@click.option(
    "--spread",
    type=str,
    default="daily",
    help="Name of the tarot spread to use (default: daily)",
)
@click.option(
    "--reversed",
    "-r",
    is_flag=True,
    help="Show cards as reversed (30-50% of cards)",
)
@click.option(
    "--birth-date",
    type=str,
    help="Birth date for natal chart mode (YYYY-MM-DD)",
)
@click.option(
    "--birth-time",
    type=str,
    help="Birth time for natal chart mode (HH:MM, 24-hour format)",
)
@click.option(
    "--birth-lat",
    type=float,
    default=0.0,
    help="Birth latitude for natal chart mode (default: 0.0)",
)
@click.option(
    "--birth-lon",
    type=float,
    default=0.0,
    help="Birth longitude for natal chart mode (default: 0.0)",
)
@click.option(
    "--birth-zone",
    type=str,
    default=None,
    help="Birth time zone for natal chart mode (e.g., 'America/New_York')",
)
@click.option(
    "--config",
    type=str,
    help="Path to config file (default: ~/.config/orbpondering/config.toml)",
)
# @click.option(
#     "--tui",
#     is_flag=True,
#     help="Launch the Textual TUI interface",
# )
def cli(
    date: str | None,
    lat: float,
    lon: float,
    house: str,
    spread: str,
    reversed: bool,
    birth_date: str | None,
    birth_time: str | None,
    birth_lat: float,
    birth_lon: float,
    birth_zone: str | None,
    config: str | None,
    tui: bool = False,
):
    """Tarot spreads seeded by daily astrological calculations."""
    if tui:
        # Launch TUI
        from orbpondering.tui import TUIApp

        app = TUIApp()
        app.run()
    else:
        # Handle CLI mode
        args = argparse.Namespace(
            date=date,
            lat=lat,
            lon=lon,
            house=house,
            spread=spread,
            reversed=reversed,
            birth_date=birth_date,
            birth_time=birth_time,
            birth_lat=birth_lat,
            birth_lon=birth_lon,
            birth_zone=birth_zone,
            config=config,
        )
        main(args)


def main(args: argparse.Namespace) -> None:
    """Handle CLI mode."""
    # Set defaults
    lat = getattr(args, "lat", 0.0)
    lon = getattr(args, "lon", 0.0)
    house_system = getattr(args, "house", HouseSystem.WHOLE_SIGN)
    spread_name = getattr(args, "spread", "daily")
    reversed_cards = getattr(args, "reversed", False)

    # Handle date argument (if provided)
    if hasattr(args, "date") and args.date:
        try:
            d = datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            sys.exit(1)
    else:
        d = date.today()

    # Handle birth data for natal chart mode
    if (
        hasattr(args, "birth_date")
        and args.birth_date
        and hasattr(args, "birth_time")
        and args.birth_time
    ):
        try:
            birth_date = datetime.strptime(args.birth_date, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid birth date format. Please use YYYY-MM-DD.")
            sys.exit(1)

        birth_time = None
        if hasattr(args, "birth_time") and args.birth_time:
            try:
                time_obj = datetime.strptime(args.birth_time, "%H:%M").time()
                birth_time = time_obj
            except ValueError:
                print("Invalid birth time format. Please use HH:MM.")
                sys.exit(1)

        birth_lat = getattr(args, "birth_lat", 0.0)
        birth_lon = getattr(args, "birth_lon", 0.0)
        birth_tz = getattr(args, "birth_zone", None)

        birth_data = BirthData(
            date=birth_date, time=birth_time, lat=birth_lat, lon=birth_lon, tz=birth_tz
        )

        # Generate natal chart reading
        reading = birth_tarot_draw(
            d=d,
            lat=lat,
            lon=lon,
            birth_data=birth_data,
            house_system=house_system,
            spread_name=spread_name,
            reversed_cards=reversed_cards,
        )
    else:
        # Generate standard daily reading
        reading = tarot_draw_for_date(
            d=d,
            lat=lat,
            lon=lon,
            house_system=house_system,
            spread_name=spread_name,
            reversed_cards=reversed_cards,
        )

    # Display the reading
    display_reading(reading)
