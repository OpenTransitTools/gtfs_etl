import partridge as ptg
from ott.utils import gtfs_utils


def main():
    td = gtfs_utils.tmpdir()
    gtfs_utils.unzip("/Users/fpurcell/java/DEV/rtp/gtfs_etl/ott/gtfs_etl/cache/SMART.gtfs.zip", td)
    gtfs_utils.zip("./gtfs/BLA.gtfs.zip", td)