from __future__ import annotations

import argparse
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence
from uuid import uuid4

import getorg
from geopy import Nominatim
from geopy.exc import GeocoderServiceError, GeocoderTimedOut
from geopy.extra.rate_limiter import RateLimiter


LOGGER_NAME = "talkmap"
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_TALKS_DIR = Path(__file__).resolve().parent / "_talks"
DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parent / "talkmap"
ENV_USER_AGENT = "TALKMAP_USER_AGENT"


@dataclass(frozen=True)
class TalkRecord:
    """Minimal metadata captured from a talk markdown file."""

    path: Path
    location: str


def extract_location_from_markdown(markdown_path: Path) -> Optional[str]:
    """Return the normalized location string from the file's front matter."""
    in_front_matter = False
    try:
        with markdown_path.open("r", encoding="utf-8") as handle:
            for raw_line in handle:
                line = raw_line.strip()
                if line == "---":
                    if not in_front_matter:
                        in_front_matter = True
                        continue
                    break
                if not in_front_matter:
                    continue
                if line.startswith("location:"):
                    value = line.split(":", 1)[1].strip()
                    return value.strip().strip("\"'")
    except OSError as exc:  # Bubble up for calling code to log context.
        raise RuntimeError(f"Failed to read markdown file {markdown_path}") from exc
    return None


def collect_talk_records(
    talks_dir: Path,
    *,
    logger: logging.LoggerAdapter,
) -> Sequence[TalkRecord]:
    """Collect talk metadata for markdown files under the provided directory."""
    records: List[TalkRecord] = []
    for path in sorted(talks_dir.glob("*.md")):
        try:
            location = extract_location_from_markdown(path)
        except RuntimeError as exc:
            logger.warning("Failed to parse talk metadata", extra={"path": str(path), "error": str(exc)})
            continue
        if not location:
            logger.debug("Skipping talk without location", extra={"path": str(path)})
            continue
        normalized = " ".join(location.split())
        if not normalized:
            logger.debug("Skipping talk with empty normalized location", extra={"path": str(path)})
            continue
        records.append(TalkRecord(path=path, location=normalized))
    return records


def geocode_locations(
    locations: Iterable[str],
    *,
    user_agent: str,
    logger: logging.LoggerAdapter,
) -> Dict[str, object]:
    """Geocode each unique location string and return mapping used by getorg."""
    geocoder = Nominatim(user_agent=user_agent, timeout=10)
    rate_limited_geocode = RateLimiter(
        geocoder.geocode,
        min_delay_seconds=1,
        max_retries=2,
        error_wait_seconds=2,
        swallow_exceptions=False,
    )
    location_map: Dict[str, object] = {}
    for location in sorted(set(locations)):
        try:
            result = rate_limited_geocode(location)
        except (GeocoderServiceError, GeocoderTimedOut) as exc:
            logger.warning(
                "Geocoding failed for location",
                extra={"location": location, "error": str(exc)},
            )
            continue
        if result is None:
            logger.warning("No geocode match for location", extra={"location": location})
            continue
        location_map[location] = result
        logger.debug(
            "Geocoded location",
            extra={"location": location, "latitude": result.latitude, "longitude": result.longitude},
        )
    return location_map


def ensure_directory(path: Path) -> None:
    """Create the directory if it is missing, ensuring parents exist."""
    try:
        path.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise RuntimeError(f"Unable to create output directory {path}") from exc


def build_logger(level_name: str, trace_id: str) -> logging.LoggerAdapter:
    """Configure a logger for the script and return an adapter with trace context."""
    logger = logging.getLogger(LOGGER_NAME)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s %(levelname)s %(name)s trace_id=%(trace_id)s %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(level_name.upper())
    return logging.LoggerAdapter(logger, extra={"trace_id": trace_id})


def generate_talk_map(
    *,
    talks_dir: Path,
    output_dir: Path,
    user_agent: str,
    logger: logging.LoggerAdapter,
) -> None:
    """Primary workflow for generating the talk location map artifacts."""
    talks_dir = talks_dir.resolve(strict=True)
    output_dir = output_dir.resolve()

    logger.info(
        "Starting talk map generation",
        extra={"talks_dir": str(talks_dir), "output_dir": str(output_dir)},
    )

    records = collect_talk_records(talks_dir, logger=logger)
    if not records:
        logger.error("No talks with valid locations found; aborting map generation")
        raise RuntimeError("No talks with valid locations.")

    unique_locations = [record.location for record in records]
    location_map = geocode_locations(unique_locations, user_agent=user_agent, logger=logger)
    if not location_map:
        logger.error("Geocoding produced no results; aborting map generation")
        raise RuntimeError("Geocoding produced no results.")

    ensure_directory(output_dir)
    getorg.orgmap.create_map_obj()
    getorg.orgmap.output_html_cluster_map(
        location_map,
        folder_name=str(output_dir),
        hashed_usernames=False,
    )
    logger.info(
        "Talk map artifacts written",
        extra={
            "output_dir": str(output_dir),
            "locations_count": len(location_map),
            "talks_processed": len(records),
        },
    )


def parse_args() -> argparse.Namespace:
    """Parse command line arguments for the talk map generator."""
    parser = argparse.ArgumentParser(
        description="Generate clustered talk map artifacts from talk markdown files."
    )
    parser.add_argument(
        "--talks-dir",
        type=Path,
        default=DEFAULT_TALKS_DIR,
        help=f"Directory containing talk markdown files (default: {DEFAULT_TALKS_DIR})",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory where map artifacts will be written (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--user-agent",
        type=str,
        default=None,
        help="User agent string for Nominatim. "
        f"Can also be provided via the {ENV_USER_AGENT} environment variable.",
    )
    parser.add_argument(
        "--trace-id",
        type=str,
        default=None,
        help="Optional trace identifier used to correlate logs.",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default=DEFAULT_LOG_LEVEL,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level for the script.",
    )
    return parser.parse_args()


def main() -> None:
    """Script entrypoint."""
    args = parse_args()
    user_agent = args.user_agent or os.getenv(ENV_USER_AGENT)
    if not user_agent:
        raise SystemExit(
            "A Nominatim user agent must be supplied via --user-agent or TALKMAP_USER_AGENT."
        )
    trace_id = args.trace_id or str(uuid4())
    logger = build_logger(args.log_level, trace_id)
    try:
        generate_talk_map(
            talks_dir=args.talks_dir,
            output_dir=args.output_dir,
            user_agent=user_agent,
            logger=logger,
        )
    except Exception as exc:  # noqa: BLE001 - top-level guard for clean exit.
        logger.error("Talk map generation failed", extra={"error": str(exc)})
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
