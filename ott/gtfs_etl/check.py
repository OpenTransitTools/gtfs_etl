import os
import csv
import zipfile
from ott.utils import file_utils
from ott.utils.config_util import ConfigUtil
from .utils import gtfs_cmdline

import logging
log = logging.getLogger(__file__)


def read_zip_file(zip_path, named_file=None, output_path=None):
    """
    open a zipfile
    optionally read a named file from that zip into memory
    optionally write that named file to a separate file outside the zip
    """
    ret_val = None

    with zipfile.ZipFile(zip_path, 'r') as zf:
        ret_val = zf.namelist()

        # find (optional) named_file in zip and return that data 
        if named_file:
            ret_val = None
            if named_file in zf.namelist():
                # read a specific named_file's contents
                with zf.open(named_file) as f:
                    ret_val = f.read().decode('utf-8')
                    # optionally write named_file to a file
                    if ret_val and output_path:
                        # with file.open(output_path):
                        # TODO: write file
                        pass

    return ret_val


def gtfs_fare_category():
    args = gtfs_cmdline()
    zips = file_utils.find_files(args.path, ext="gtfs.zip")
    gtfs = ConfigUtil.factory(section="gtfs")
    feeds = gtfs.get_json('feeds')
    categories = gtfs.get_list('fare_categories')

    for z in zips:
        c = read_zip_file(z, "rider_categories.txt")
        f = os.path.basename(z)
        u = next((i.get('url') for i in feeds if i.get("name") == f), None)
        print(f"\n{f}: {u}\n{c}\n\n")
