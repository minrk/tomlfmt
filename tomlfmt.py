"""autoformat one or more toml files"""
import argparse
import sys
from unittest import mock

import pytoml as toml

__version__ = "0.1.0"

def _format_list(v):
    """override pytoml's format_list to split items onto lines

    rather than one big line
    """
    lines = ["["]
    for obj in v:
        lines.append("    %s," % toml.writer._format_value(obj))
    lines.append("]")
    return "\n".join(lines)


def format(*files, inplace=False):
    """Automatically format one or more toml files"""

    if not files:
        raise ValueError("Please specify one or more files to format")
    for path in files:
        with open(path) as f:
            toml_text = f.read()
        try:
            data = toml.loads(toml_text)
        except Exception as e:
            print(f"- ❌ Error parsing {path}: {e}", file=sys.stderr)
            continue
        # serialize with patched export of lists
        # so that they are split across lines
        with mock.patch.object(toml.writer, '_format_list', _format_list):
            assert toml.writer._format_list is _format_list
            reformatted = toml.dumps(data).rstrip() + "\n"
            # verify that we are producing valid, parseable toml
            toverify = toml.loads(reformatted)
            assert toverify == data

        if inplace:
            if reformatted == toml_text:
                print(f"- 🎉 {path} already looking good", file=sys.stderr)
            else:
                with open(path, "w") as f:
                    f.write(reformatted)
                print(f"- ✅ {path} reformatted", file=sys.stderr)
        else:
            print(reformatted, end='')


def main(argv=None):
    """Run the autoformatter"""
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", type=str, help="toml files to format")
    parser.add_argument("-i", "--inplace", action="store_true", help="reformat ")
    opts = parser.parse_args(argv)
    format(*opts.files, inplace=opts.inplace)


if __name__ == "__main__":
    main()
