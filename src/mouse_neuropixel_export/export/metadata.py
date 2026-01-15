from ..utils.logging import Logger
from ..schemas import metadata as dst

logger = Logger(__name__)

def export_metadata(scan_key, stim_key=None):
    if stim_key is not None:
        logger.info(f"Starting metadata export for scan_key: {scan_key} with stim_key: {stim_key}.")
    else:
        logger.info(f"Starting metadata export for scan_key: {scan_key}.")
    
    dst.ScanKey(**scan_key).put(scan_key)
    
    if stim_key is not None:
        dst.StimKey(**stim_key).put(stim_key)
        dst.ScanStimKey(**scan_key, **stim_key).put({**scan_key, **stim_key})