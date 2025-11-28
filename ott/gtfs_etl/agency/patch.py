import importlib
from ott.utils import file_utils

import logging 
log = logging.getLogger(__file__)


def fix_agency(feed_path, feed_id, new_feed_path=None, file_dir=None):
    """
    dynamically load the agency.{feed_id} patch.py, if it exists
    note: most agencies won't have a patch, so this method will get a lot of exceptions
    """
    agency_patch = f"ott.gtfs_etl.agency.{feed_id}.patch"    
    try:
        if new_feed_path is None:
            new_feed_path = feed_path
        if file_dir is None:
            file_dir = file_utils.tmpdir()

        i = importlib.import_module(agency_patch)
        file_utils.unzip(feed_path, file_dir)
        i.fix(file_dir)
        file_utils.dozip(new_feed_path, file_dir)
    except ImportError:
        log.info(f"feed_id {feed_id} has no patch (e.g., {agency_patch}.py doesn't exist), which is okay since most feeds don't need a patch")
    except Exception as e:
        log.warning(e)
    return file_dir


def main():
    d = fix_agency("/Users/fpurcell/java/DEV/rtp/gtfs_etl/ott/gtfs_etl/cache/SMART.gtfs.zip", "SMART", "BLA.zip", file_dir="/tmp")
    print(d)

