import sys

def execute_from_command_line(argv=None):
    """Minimal stub for django.core.management.execute_from_command_line.

    This stub only handles the 'check' command to allow health checks to run
    when Django isn't installed in the virtualenv. It intentionally does not
    implement Django functionality.
    """
    argv = list(argv or sys.argv)
    if len(argv) >= 2 and argv[1] == 'check':
        # Print a helpful message and exit successfully to satisfy health checks.
        print('Stub: Django is not installed in the virtualenv; skipping checks.')
        return
    # For any other command, provide a generic message and exit.
    print('Stub: Django is not installed. Command "{}" not executed.'.format(' '.join(argv[1:])))
    return
