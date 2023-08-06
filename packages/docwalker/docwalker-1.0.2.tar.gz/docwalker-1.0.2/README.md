![docwalker_windows_screenshot](./doc/windows_screenshot.png)

# docwalker

[![PyPI version](https://badge.fury.io/py/docwalker.svg)](https://badge.fury.io/py/docwalker)

Quickly view documentation in source code in a language-agnostic way.

Docwalker processes custom characters in both inline and block comments to
quickly extract and present documentation comments in source code.

For completeness, docwalker will also open entire Markdown files.

## Installation

```shell
$> pip install docwalker

$> docwalker --help
# usage: docwalker [-h] [-f FILE] src_dir

# DocWalker is a quick documentation filter/viewer for examining source code
# documentation. By default, DocWalker creates a local config file, .dwconf, which
# hosts the project-specific configuration.

# positional arguments:
#   src_dir               The source directory to examine.

# options:
#   -h, --help            show this help message and exit
#   -f FILE, --file FILE  The config file to reference for custom parsing [default: '<src_dir>/.dwconf']
```

## Usage

```shell
$> docwalker . # walks the current working directory.
```

## Configuration

### Default

The default configuration supports Python-esque syntax:

```ini
[parser.inline]
syntax = #@

[parser.block]
syntax_start = """@
syntax_end = @"""

[parser.listing]
syntax_start = #<<
syntax_end = #>>
```

* **inline:** `#@ inline documentation here`
* **block:** `"""@ block documentation here @"""`
* **listings:** `#<< code goes here #>>`

When `docwalker` first runs in a directory, a config file by the name `.dwconf`
is generated with these default values. Simply edit this file to change what
characters should be processed.