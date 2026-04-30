"""CLI entry point for daily tarot draws."""

from __future__ import annotations

import argparse
import datetime
import sys

from orbpondering.constants import HouseSystem
from orbpondering.draw import tarot_draw_for_date


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
    args = parser.parse_args(argv)

    dt = datetime.date.fromisoformat(args.date)
    house = HouseSystem(args.house)

    draw = tarot_draw_for_date(
        dt, lat=args.lat, lon=args.lon, house_system=house, spread_name=args.spread
    )

    print(f"Date:     {dt}")
    print(f"Location: {args.lat}{chr(176)}, {args.lon}{chr(176)}")
    print(f"House:    {args.house}")
    print(f"Spread:   {args.spread}")
    print(f"Seed:     {draw['seed']:016x}")
    print()
    for pos in draw["positions"]:
        print(f"  {pos['position_label']:>14}: {pos['card'].name}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
