import os
import io
import re
import csv
import zipfile
from ott.utils import file_utils
from ott.utils.config_util import ConfigUtil
from .utils import gtfs_cmdline

import logging
log = logging.getLogger(__file__)


def str_to_csv(data):
    """ turn a string (expected to be in .csv form, w/a header line) into a list of dicts """
    ret_val = []
    if data:
        ret_val = csv.DictReader(io.StringIO(data))
    return ret_val


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
                    # hack: decode/encode/decode the zip's file, which gets rid of weird control chars from the zipfile
                    #       (ala "\xef\xbb\xbfrider_category_id,rider...") junk in C-TRAN feed
                    v = f.read()                              # open GTFS .zip file (e.g., 'rider_categories.txt')
                    t = v.decode('utf-8')                     # convert that binary data to str via decode (note: C-TRAN has ""\xef\xbb\xbf" junk in that data)
                    t = t.encode('ascii', errors='ignore')    # force 'ascii' encoding to get rid of strange ctl chars by coverting str back to binary
                    t = t.decode()                            # now decode ascii binary data back to string, thus string is just ascii (no more strange ctl chars)
                    t = t.strip()                             # remove spaces 
                    ret_val = t

                    # optionally write the zip's named_file data to a new file
                    if ret_val and output_path:
                        # with file.open(output_path):
                        # TODO: write file
                        pass

    return ret_val


def feed_has_unexpected_categories(gtfs_feed_path, gtfs_rider_categories, known_categories):
    """ 
    iterate thru the lines in the GTFS.rider_categories.txt, looking at the 'rider_category_id' element
    return a string of any 'unknown' rider categories seen in the given .gtfs.zip rider_categories.txt file
    note: for the most part, there should not be any unknown categories .. want to be alerted if there are unknowns
    """
    #import pdb; pdb.set_trace()
    ret_val = ""
    for d in gtfs_rider_categories:
        rc = d.get('rider_category_id')
        if not rc:
            log.warning(f"{gtfs_feed_path} 'rider_categories.txt' is missing the 'rider_category_id' field.")
        else:
            rc = rc.strip()
            if rc not in known_categories:
                ret_val = f"{rc}, {ret_val}"
            else:
                log.info(f"\n\t{rc:15} in {known_categories} = {gtfs_feed_path}")
    ret_val = ret_val.strip().strip(',')
    return ret_val


def gtfs_fare_category():
    """
    cmdline app that reads a directory of GTFS .zip files
    open each feed's "rider_categories.txt" file, making sure that
    there are no unexpected catoriges (as configured in app.ini data)
    """
    ret_val = 0
    args = gtfs_cmdline()
    zips = file_utils.find_files(args.path, ext="gtfs.zip")
    gtfs = ConfigUtil.factory(section="gtfs")
    feeds = gtfs.get_json('feeds')
    categories = gtfs.get_list('fare_categories')

    #import pdb; pdb.set_trace()
    if categories is None or len(categories) < 1:
        print(f"ERROR: {gtfs.ini_file_path} config lacks a 'gtfs.fare_categories: [ADULT,...]' element")
    else:
        print("Checking fare rider categories:")
        for z in zips:
            c = read_zip_file(z, "rider_categories.txt")
            v = str_to_csv(c)
            nc = feed_has_unexpected_categories(z, v, categories)
            if nc:
                print(f" **FAIL**: {z}", end="")
                f = os.path.basename(z)
                u = next((i.get('url') for i in feeds if i.get("name") == f), None)
                print(f" ({u}) has UNKNOWN rider category(s): '{nc}'")
                ret_val += 1
            else:
                print(f" PASS: {z}")
        print("done")

    return ret_val
