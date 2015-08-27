import functools
import sys

import click

from sriovlib import exceptions


def check_common_errors(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            ret = function(*args, **kwargs)
            return ret
        except exceptions.SriovDeviceNotFound as e:
            click.echo("Error: %s" % e.msg)
            sys.exit(1)
        except IOError as e:
            click.echo("Error: %s" % e)
            sys.exit(1)
    return wrapper
