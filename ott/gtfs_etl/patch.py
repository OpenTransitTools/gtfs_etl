import importlib
from ott.utils import gtfs_utils

import logging 
log = logging.getLogger(__file__)


def fix_agency(feed_id, file_dir):
    """
    dynamically load the agency.{feed_id} patch.py, if it exists
    note: most agencies won't have a patch, so this method will get a lot of exceptions
    """
    agency_patch = f"ott.gtfs_etl.agency.{feed_id}.patch"    
    try:
        i = importlib.import_module(agency_patch)
        i.fix(file_dir)
    except:
        log.info(f"feed_id {feed_id} has no patch (e.g., {agency_patch}.py doesn't exist), which is okay since most feeds don't need a patch")


def main():
    tmpdir = gtfs_utils.tmpdir()
    gtfs_utils.unzip("/Users/fpurcell/java/DEV/rtp/gtfs_etl/ott/gtfs_etl/cache/SMART.gtfs.zip", tmpdir)
    fix_agency("SMART", tmpdir)
    gtfs_utils.zip("./gtfs/BLA.gtfs.zip", tmpdir)

