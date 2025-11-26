import os
from .fares import convert_fares

#
# NOTE: convert.py depends on https://github.com/ibi-group/gtfs-fares-converter for converting Fares V1 -> V2
#   I couldn't get poetry to properly recognize that package when installed as a dependency, with the following:
#   gtfs-fares-converter = {git = "https://github.com/ibi-group/gtfs-fares-converter.git"}
#   so punted and and simply put Arcadis' convert.py file here via curl.
#
#   curl https://raw.githubusercontent.com/ibi-group/gtfs-fares-converter/refs/heads/main/convert.py > fares.py
#


def fares_to_v2(feeds, cache_dir):
    for f in feeds:
        if f.get('faresV1'):
            path = os.path.join(cache_dir, f.get('name'))
            convert_fares(path, path)


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Converts a GTFS feed's Fares V1 info to Fares V2 info."
    )
    parser.add_argument(
        "input_zip",
        help="Path to the current GTFS zip file."
    )
    parser.add_argument(
        "output_zip",
        help="Path to the output zip file."
    )
    args = parser.parse_args()
    convert_fares(args.input_zip, args.output_zip)
