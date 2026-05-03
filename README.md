<p align="center">
<img src="design/orbpondering.png" width="300">
</p>


# Orbpondering [![Version][version-badge]][version-link]

**Orbpondering** generates daily tarot readings based on astrological calculations. It uses your location and the current date to compute planetary positions and generate a deterministic tarot spread.

## Features

- **Daily Tarot Draws**: Receive a tarot reading based on current planetary positions
- **Educational Mode**: Walk through the astrological calculations step by step
- **Natal Chart Support**: Personalize readings with your birth chart
- **Multiple Spreads**: Choose from different tarot spread types
- **Deterministic**: Same date/location always produces same reading

## Installation

Install the package with pip:

```bash
pip install orbpondering
```

Or install with the optional CLI dependencies for enhanced display:

```bash
pip install orbpondering[cli]
```

## Quick Start

### Basic Daily Tarot Reading

```bash
orbpondering
```

By default, this draws for today's date and location (0° latitude/longitude).

### Custom Date and Location

```bash
orbpondering 2025-06-15 --lat 40.7128 --lon -74.0060
```

### Educational Mode

```bash
orbpondering --education
```

This shows step-by-step calculations of planetary positions, house cusps, and the seed generation.

## Natal Chart Mode

### With Birth Data

```bash
orbpondering \
  --birth-date 1990-05-15 \
  --birth-time 14:30 \
  --birth-zone "America/New_York" \
  --birth-lat 41.8781 \
  --birth-lon -87.6298 \
  --spread three_card
```

This enables natal chart mode, incorporating your birth chart into the tarot reading.

## Available Spreads

- **Daily** (default): Single card for the day's theme
- **Three Card**: Past, Present, Future
- **Celtic Cross**: Detailed 10-card spread

## Command Line Options

```
usage: orbpondering [-h] [--lat LAT] [--lon LON]
                   [--house {whole_sign,equal,porphyry,placidus}]
                   [--spread {daily,three_card,celtic_cross}] [--education]
                   [--verbose] [--birth-date BIRTH_DATE]
                   [--birth-time BIRTH_TIME] [--birth-zone BIRTH_ZONE]
                   [--birth-lat BIRTH_LAT] [--birth-lon BIRTH_LON]
                   [date]

Daily tarot draw seeded by astrological chart

positional arguments:
  date                  ISO date (YYYY-MM-DD). Default: today

options:
  -h, --help            show this help message and exit
  --lat LAT             Observer latitude
  --lon LON             Observer longitude
  --house {whole_sign,equal,porphyry,placidus}
                        House system
  --spread {daily,three_card,celtic_cross}
                        Spread name
  --education, -e       Educational mode: walk through calculations step by
                        step
  --verbose, -v         Verbose educational output
  --birth-date BIRTH_DATE
                        Birth date (YYYY-MM-DD) to enable natal chart mode
  --birth-time BIRTH_TIME
                        Birth time (HH:MM) - optional, defaults to noon UTC
  --birth-zone BIRTH_ZONE
                        Birth timezone (IANA format) - optional, defaults to
                        UTC
  --birth-lat BIRTH_LAT
                        Birth latitude
  --birth-lon BIRTH_LON
                        Birth longitude
```

## Development

To develop orbpondering, clone the repository and install in development mode:

```bash
git clone https://github.com/phildini/orbpondering.git
cd orbpondering
uv sync --all-extras  # Install all dependencies including dev
uv run pytest         # Run tests
uv run ruff check     # Lint code
uv run mypy src/      # Type check
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

[version-badge]:   https://img.shields.io/pypi/v/orbpondering.svg?label=version
[version-link]:    https://pypi.python.org/pypi/orbpondering/