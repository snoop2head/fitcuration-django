#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import datetime

LOCAL = bool(os.environ.get("LOCAL"))


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if LOCAL:
    import dotenv

    if __name__ == "__main__":
        dotenv.read_dotenv()
        main()

else:
    if __name__ == "__main__":
        # logging format with Korean time 2020-04-04 21:59:27.989535
        datetime_object = datetime.datetime.now()
        print(datetime_object)

        main()
