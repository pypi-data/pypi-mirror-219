# MIT License
#
# Copyright (c) 2023 Clivern
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import uuid
import click
import logging, json, sys

from pavio import __version__
from pavio.model.environment import Environment
from pavio.command.configs import Configs
from pavio.command.environments import Environments


@click.group(help="🐺 A Minimalist Python Environment Manager")
@click.version_option(version=__version__, help="Show the current version")
def main():
    pass


# Environments command
@click.group(help="Manage environments")
def environment():
    pass


# Delete environment sub command
@environment.command(help="Delete a environment")
@click.argument("name")
def delete(name):
    return Environments().init().delete(name)


# Manage configs command
@click.group(help="Manage configs")
def config():
    pass


# Init configs sub command
@config.command(help="Init configurations")
def init():
    return Configs().init()


# Edit configs sub command
@config.command(help="Edit configurations")
def edit():
    return Configs().edit()


# Show configs sub command
@config.command(help="Show configurations")
def dump():
    return Configs().dump()


# Register Commands
main.add_command(environment)
main.add_command(config)


if __name__ == "__main__":
    main()
