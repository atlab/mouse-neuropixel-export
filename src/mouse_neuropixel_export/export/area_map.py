import datajoint as dj

from . import fetch_dj_as_pd
from ..schemas import area_map as dst
from ..utils.logging import Logger

logger = Logger(__name__)

src = dj.create_virtual_module('mdiamantaki_area_mapping', 'mdiamantaki_area_mapping')

def export_scan_data(scan_key):
    logger.info(f"Exporting area data for scan_key: {scan_key}")

    logger.info(f"Exporting AreaPerUnit...")
    dst.AreaPerUnit(**scan_key).put(fetch_dj_as_pd(src.AreaPerUnit & scan_key))