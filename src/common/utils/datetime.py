from datetime import datetime, UTC


def now() -> datetime:
    """Returns the current datetime in UTC."""
    return datetime.now(UTC)


def parse_date(date_value) -> datetime:
    if isinstance(date_value, (int, float)):
        # If timestamp, convert to datetime
        return datetime.fromtimestamp(date_value)
    if isinstance(date_value, str):
        try:
            return datetime.fromisoformat(date_value)
        except ValueError:
            # If not ISO, try parsing as timestamp string
            try:
                return datetime.fromtimestamp(float(date_value))
            except Exception:
                raise Exception(f"Invalid date format: {date_value}")
    return date_value  # Already a datetime
