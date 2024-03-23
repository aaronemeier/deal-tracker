#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "deal_tracker_config.settings.production")

    try:
        from django.core.management import execute_from_command_line

    except ImportError as e:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from e

    # This allows easy placement of apps within the interior deal_tracker directory
    current_path = Path(__file__).parent.resolve()
    sys.path.append(str(current_path / "deal_tracker"))

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
