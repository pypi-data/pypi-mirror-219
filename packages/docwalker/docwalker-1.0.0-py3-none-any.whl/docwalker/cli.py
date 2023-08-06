import os

from argparse import ArgumentParser
from configparser import ConfigParser

_description = """
DocWalker is a quick documentation filter/viewer for examining source code
documentation.

By default, DocWalker creates a local config file, .dwconf, which hosts the
project-specific configuration.
"""

_default_inline_syntax = "#@"
_default_block_syntax_start = "/*@"
_default_block_syntax_end = "@*/"
_default_listing_syntax_start = "<<<"
_default_listing_syntax_end = ">>>"

_default_config = f"""
[parser.inline]
syntax = {_default_inline_syntax}

[parser.block]
syntax_start = {_default_block_syntax_start}
synax_end = {_default_block_syntax_end}

[parser.listing]
syntax_start = {_default_listing_syntax_start}
syntax_end = {_default_listing_syntax_end}

"""

PARSER = ArgumentParser(prog="docwalker", description=_description)
PARSER.add_argument("src_dir", type=str, help="The source directory to examine.")
PARSER.add_argument(
    "-f",
    "--file",
    type=str,
    help="The config file to reference for custom parsing [default: '<src_dir>/.dwconf']",
)


def generate_config(path: str = ".dwconf") -> dict:
    output = {}
    if not os.path.exists(path):
        with open(path, "w+") as file:
            file.write(_default_config)

    config = ConfigParser()
    config.read(path)
    output["inline_syntax"] = config.get(
        "parser.inline", "syntax", fallback=_default_inline_syntax
    )
    output["block_syntax_start"] = config.get(
        "parser.block", "syntax_start", fallback=_default_block_syntax_start
    )
    output["block_syntax_end"] = config.get(
        "parser.block", "syntax_end", fallback=_default_block_syntax_end
    )
    output["listing_syntax_start"] = config.get(
        "parser.listing", "syntax_start", fallback=_default_listing_syntax_start
    )
    output["listing_syntax_end"] = config.get(
        "parser.listing", "syntax_end", fallback=_default_listing_syntax_end
    )

    return output
