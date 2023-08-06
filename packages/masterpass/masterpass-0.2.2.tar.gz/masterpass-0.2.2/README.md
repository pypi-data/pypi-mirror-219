# Master

[![Deploy pages](https://github.com/jpedro/master/actions/workflows/pages.yaml/badge.svg)](https://github.com/jpedro/master/actions/workflows/pages.yaml)

Generates deterministic passwords

Inspired by [spectre.app](https://spectre.app/) but simpler.


![Pictutre](https://raw.githubusercontent.com/jpedro/master/master/docs/strong.jpg)
<!-- ![Strong password](https://raw.githubusercontent.com/jpedro/master/master/docs/blink.gif) -->

This uses a sha256 hashed combination of `username + password + service`
to generate the same password, thus eliminating the need to store,
maintain and back up other generated passwords.

The used service name list is kept under the file
`~/.config/master/list.txt` (or whatever `MASTER_LIST` points to)
*purely for autocompletion*, which will be added later.


## Install

    pip install masterpass

Yes, yes. The package is called `masterpass` but the binary is called
`master`. To be fixed after [#2582](https://github.com/pypi/support/issues/2582)
is resolved.


## Usage

```
$ master --help

NAME
    master -- Generates deterministic passwords for services

USAGE
    master NAME                 Gets the password for service NAME
    master -l, --list           Lists all stored services
    master -r, --remove NAME    Removes service NAME from the stored list
    master -v, --version        Shows the version
    master -h, --help           Shows this help

```


## Environment variables

| Name                | Default                       |
| ------------------- | ----------------------------- |
| `MASTER_LIST`       | `~/.config/master/list.txt`   |
| `MASTER_USERNAME`   | (None) [1]                    |
| `MASTER_PASSWORD`   | (None) [1]                    |
| `MASTER_SEPARATOR`  | `-`                           |
| `MASTER_LENGTH`     | `6`                           |
| `MASTER_CHUNKS`     | `6`                           |

**Note [1]:** If you don't set the `MASTER_USERNAME` or the
`MASTER_PASSWORD` you will be prompted for them.


## Online

[jpedro.github.io/master](https://jpedro.github.io/master/) has the
browser experience.
