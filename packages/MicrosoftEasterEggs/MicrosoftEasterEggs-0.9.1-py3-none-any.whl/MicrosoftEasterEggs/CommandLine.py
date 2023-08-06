#!/usr/local/bin/python3

## Exports the assets for the credits easter egg of a Windows 3.1x SHELL.DLL.
## Currently, only read-only support is planned. But eventually, modding
## will be possible!

import argparse
import os 
import json

def main():
    # DEFINE THE COMMAND-LINE ARGUMENT PARSERS.
    argument_parser = argparse.ArgumentParser(
        formatter_class = argparse.RawTextHelpFormatter,
        description = "Extracts assets from Microsoft easter eggs")
    subparsers = argument_parser.add_subparsers(
        required = True,
        title = 'Easter eggs',
        description = 'Choose one of the following supported Microsoft easter eggs to export. You must have access to the required original file(s) from the original Microsoft products.',
        help = 'WINDOWS\SYSTEM\SHELL.DLL')

    # Windows 3.1 Credits.
    windows31_credits_argument_parser = subparsers.add_parser(
        name = 'windows31-credits',
        description = "Extracts assets from the Windows 3.1x Credits easter egg in SHELL.DLL.")
    input_argument_help = "The filepath to SHELL.DLL (Windows 3.1x version)."
    windows31_credits_argument_parser.add_argument('input', help = input_argument_help)
    export_argument_help = "Specify the directory location for exporting assets."
    windows31_credits_argument_parser.add_argument('export', help = export_argument_help)
    def extract_windows31_credits_argument_parser(command_line_args):
        from .windows31.credits import Windows31Credits
        windows31_credits = Windows31Credits(command_line_args.input)
        windows31_credits.export(command_line_args.export)
    windows31_credits_argument_parser.set_defaults(func = extract_windows31_credits_argument_parser)

    # EXTRACT THE ASSETS.
    command_line_args = argument_parser.parse_args()
    command_line_args.func(command_line_args)

if __name__ == "__main__":
    main()