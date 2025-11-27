import os
import inspect
from ott.utils import file_utils


def fix(dir_path):
    """
    adjust the gtfs files located in dir_path
    for SMART, we do two things:
     1) copy the *.txt V2 files located in this folder
     2) a new column network_id is appended to the existing table routes.txt
        rows with route_id=1X is assigned network_id=1X
        other rows (except route_id=1X) is assigned network_id=SMART
    """
    
    # step 1: copy *.txt files into the folder with SMARTS other gtfs .txt files
    this_module_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    file_utils.cp_files(this_module_dir, dir_path)

    # step 2: add network_id to routes.txt
    