import datajoint as dj

from . import fetch_dj_as_pd
from ..schemas import ephys as dst
from ..utils.logging import Logger

logger = Logger(__name__)

src = dj.create_virtual_module('neuropixel_ephys', 'neuropixel_ephys')

def get_probe_insertion_table(scan_key):
    table = src.ProbeInsertion * src.ProbeInsertion.Location * src.ProbeInsertion.Probe & scan_key
    return fetch_dj_as_pd(table)

def get_session_table(scan_key):
    return fetch_dj_as_pd(src.Session & scan_key)

def get_ephys_file_metadata_table(scan_key):
    return fetch_dj_as_pd(src.EphysFile * src.EphysFile.Metadata & (src.Session & scan_key))

def get_ephys_recording_table(scan_key):
    return fetch_dj_as_pd(src.EphysRecording & (src.Session & scan_key))

def get_clustering_table(scan_key):
    return fetch_dj_as_pd(src.ClusteringMethod * src.ClusteringParamSet * src.ClusteringTask * src.Clustering & (src.Session & scan_key))

def get_curation_table(scan_key):
    return fetch_dj_as_pd(src.Curation* src.CurationType & (src.Session & scan_key))

def get_curated_clustering_table(scan_key):
    return fetch_dj_as_pd(src.CuratedClustering.Unit & (src.Session & scan_key))

def get_peak_waveform_table(scan_key):
    return fetch_dj_as_pd(src.WaveformSet.PeakWaveform & (src.Session & scan_key))

def get_waveform_table(scan_key):
    return fetch_dj_as_pd(src.WaveformSet.Waveform & (src.Session & scan_key))

def get_quality_metrics_table(scan_key):
    return fetch_dj_as_pd(src.QualityMetrics.Cluster & (src.Session & scan_key))

def export_scan_data(scan_key):
    logger.info(f"Exporting ephys data for scan_key: {scan_key}")

    logger.info(f"Exporting ProbeInsertion...")
    dst.ProbeInsertion(**scan_key).put(get_probe_insertion_table(scan_key))
    
    logger.info(f"Exporting Session...")
    dst.Session(**scan_key).put(get_session_table(scan_key))
    
    logger.info(f"Exporting EphysFileMetadata...")
    dst.EphysFileMetadata(**scan_key).put(get_ephys_file_metadata_table(scan_key))
    
    logger.info(f"Exporting EphysRecording...")
    dst.EphysRecording(**scan_key).put(get_ephys_recording_table(scan_key))
    
    logger.info(f"Exporting Clustering...")
    dst.Clustering(**scan_key).put(get_clustering_table(scan_key))
    
    logger.info(f"Exporting Curation...")
    dst.Curation(**scan_key).put(get_curation_table(scan_key))
    
    logger.info(f"Exporting CuratedClustering...")
    dst.CuratedClustering(**scan_key).put(get_curated_clustering_table(scan_key))
    
    logger.info(f"Exporting PeakWaveForm...")
    dst.PeakWaveForm(**scan_key).put(get_peak_waveform_table(scan_key))
    
    logger.info(f"Exporting WaveForm...")
    dst.WaveForm(**scan_key).put(get_waveform_table(scan_key))
    
    logger.info(f"Exporting QualityMetrics...")
    dst.QualityMetrics(**scan_key).put(get_quality_metrics_table(scan_key))