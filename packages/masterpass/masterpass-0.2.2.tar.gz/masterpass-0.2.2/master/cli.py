#!/usr/bin/env python3
"""
NAME
    master -- Deterministic password generator.

USAGE
    master                      With no arguments, prompt for service NAME
    master NAME                 Gets the password for service NAME
    master -l, --list           Lists all stored services
    master -r, --remove NAME    Removes service NAME from the stored list
    master -v, --version        Shows the version
    master -h, --help           Shows this help
"""
import os
import sys
import getpass

from . import VERSION
from .master import Master
from .logger import Logger


USER_HOME        = os.path.expanduser("~")
MASTER_LIST      = f"{USER_HOME}/.config/master/list.txt"
MASTER_LIST      = os.environ.get("MASTER_LIST", MASTER_LIST)
MASTER_DEBUG     = bool(os.environ.get("MASTER_DEBUG"))
MASTER_USERNAME  = os.environ.get("MASTER_USERNAME")
MASTER_PASSWORD  = os.environ.get("MASTER_PASSWORD")
MASTER_SEPARATOR = os.environ.get("MASTER_SEPARATOR", "-")
MASTER_LENGTH    = int(os.environ.get("MASTER_LENGTH", "6"))
MASTER_CHUNKS    = int(os.environ.get("MASTER_CHUNKS", "6"))

class Cli:

    def ask(self) -> (str, str):
        if len(MASTER_USERNAME) > 0:
            username = MASTER_USERNAME
        else:
            prompt = "Enter your master username: "
            username = getpass.getpass(prompt=prompt)

        # if len(self.PASSWORD) > 0:
        if len(MASTER_PASSWORD) > 0:
            password = MASTER_PASSWORD
        else:
            prompt = "Enter your master password: "
            password = getpass.getpass(prompt=prompt)

        return (username, password)


    @Logger.trace()
    def get(self, service: str, counter: int = 0):
        """Gets the deterministic password for SERVICE."""
        username, password = self.ask()

        master = Master(MASTER_LIST)
        master.add(service)
        master.save()

        master.username = username
        master.password = password
        random = master.generate(service, counter)
        print(random)

    @Logger.trace()
    def start(self):
        """Asks input for a new SERVICE."""
        username, password = self.ask()
        service = input("Enter your service name: ")

        master = Master(MASTER_LIST)
        master.add(service)
        master.save()

        master.username = username
        master.password = password
        random = master.generate(service)
        print(random)

    @Logger.trace()
    def ls(self):
        """Lists all stored services."""
        master = Master(MASTER_LIST)
        master.load()
        for service in master.services:
            print(service)


    @Logger.trace()
    def version(self):
        """Prints the version."""
        print(f"v{VERSION}")


    @Logger.trace()
    def remove(self, service: str):
        """Removes SERVICE from the stored list."""
        master = Master(MASTER_LIST)
        master.remove(service)
        master.save()


def main():
    cli = Cli()
    cmd = sys.argv[1] if len(sys.argv) > 1 else None
    args = sys.argv[1:]

    if cmd is None:
        cli.start()
        return

    if cmd in ["-h", "--help", "help"]:
        print(__doc__)
        return

    if cmd in ["-v", "--version", "version"]:
        print(f"v{VERSION}")
        return

    if cmd in ["-l","-ls", "--ls", "--list"]:
        cli.ls()
        return

    if cmd in ["-r", "--rm", "--remove", "-d", "--delete"]:
        name = args[1]
        if name is None:
            print("Usage: master --rm NAME")
            return 1

        return cli.remove(args[1])

    cli.get(cmd)


if __name__ == "__main__":
    exit(main())
