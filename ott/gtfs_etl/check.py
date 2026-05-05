import csv
from ott.utils import file_utils
from .utils import gtfs_cmdline

import logging
log = logging.getLogger(__file__)


def gtfs_fare_category():
    args = gtfs_cmdline()
    zips = file_utils.find_files(args.path, ext="gtfs.zip")
    print(zips)
