import datajoint as dj

from . import fetch_dj_as_pd
from ..schemas import experiment as dst
from ..utils.logging import Logger

logger = Logger(__name__)

src = dj.create_virtual_module('pipeline_experiment', 'pipeline_experiment')

def get_session_table(scan_key):
    return fetch_dj_as_pd(src.Session & scan_key)

def get_scan_table(scan_key):
    return fetch_dj_as_pd(src.Scan & scan_key)

def export_scan_data(scan_key):
    logger.info(f"Exporting experiment data for scan_key: {scan_key}")
    
    logger.info(f"Exporting Session...")
    dst.Session(**scan_key).put(get_session_table(scan_key))

    logger.info(f"Exporting Scan...")
    dst.Scan(**scan_key).put(get_scan_table(scan_key))