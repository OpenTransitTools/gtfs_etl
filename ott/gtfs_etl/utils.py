import os
import argparse

HOME_DIR = os.path.expanduser("~")
GTFS_DIR = os.path.join(HOME_DIR, "gtfs")


def gtfs_cmdline(gtfs_dir=GTFS_DIR, do_parse=True):
    parser = argparse.ArgumentParser(description="Get a GTFS feed's info.")
    parser.add_argument("--path", "-p", default=gtfs_dir, help="File path to the GTFS zip.")
    if do_parse:
        args = parser.parse_args()
        parser = args
    return parser

