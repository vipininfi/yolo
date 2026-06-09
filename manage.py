#!/usr/bin/env python
import os
import sys
from typing import List

from django.core.management import execute_from_command_line


def main(argv: List[str] | None = None) -> None:
    """Django's command-line utility for administrative tasks with a main entrypoint."""
    if argv is None:
        argv = sys.argv
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    execute_from_command_line(argv)


if __name__ == '__main__':
    main()
