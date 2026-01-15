import datajoint as dj
from tqdm import tqdm

from . import fetch_dj_as_pd
from ..schemas import stimulus as dst
from ..utils.logging import Logger

logger = Logger(__name__)

src = dj.create_virtual_module('pipeline_stimulus', 'pipeline_stimulus')
src2 = dj.create_virtual_module('imagenet', 'pipeline_imagenet')

def get_ephys_sync_table(scan_key):
    return fetch_dj_as_pd(src.EphysSync & scan_key)

def get_trial_table(scan_key):
    return fetch_dj_as_pd(src.Trial & scan_key)

def get_target_album_npx_table(stim_key):
    return fetch_dj_as_pd(src2.TargetAlbumNpx & stim_key)

def get_oracle_image_info_table(stim_key):
    return fetch_dj_as_pd((src2.Album.Oracle & stim_key) * src.StaticImage.ImageNet * src.StaticImage)

def get_image_info_table(stim_key):
    return fetch_dj_as_pd((src2.Album.Single & stim_key) * src.StaticImage.ImageNet * src.StaticImage)

def get_oracle_frame_info_table(stim_key):
    return fetch_dj_as_pd((src2.Album.Oracle & stim_key) * src.Frame)

def get_image_frame_info_table(stim_key):
    return fetch_dj_as_pd((src2.Album.Single & stim_key) * src.Frame)

def get_stimulus_image(image_key):
    return (src.StaticImage.Image & image_key).fetch1('image')

def export_scan_data(scan_key):
    logger.info(f"Exporting stimulus data for scan_key: {scan_key}")

    logger.info(f"Exporting EphysSync...")
    dst.EphysSync(**scan_key).put(get_ephys_sync_table(scan_key))

    logger.info(f"Exporting Trial...")
    dst.Trial(**scan_key).put(get_trial_table(scan_key))

def export_stimulus_data(stim_key):
    logger.info(f"Exporting stimulus data for stim_key: {stim_key}")
    logger.info(f"Exporting TargetAlbumNpx...")
    dst.TargetAlbumNpx(**stim_key).put(get_target_album_npx_table(stim_key))

    logger.info(f"Exporting stimulus oracle image information...")
    dst.ImageOracleInfo(**stim_key).put(get_oracle_image_info_table(stim_key))

    logger.info(f"Exporting stimulus image information...")
    dst.ImageInfo(**stim_key).put(get_image_info_table(stim_key))

    logger.info(f"Exporting stimulus oracle frame image information...")
    dst.ImageOracleFrameInfo(**stim_key).put(get_oracle_frame_info_table(stim_key))

    logger.info(f"Exporting stimulus frame image information...")
    dst.ImageFrameInfo(**stim_key).put(get_image_frame_info_table(stim_key))

def export_stimulus_images(stim_key):
    logger.info(f"Exporting stimulus oracle images...")
    oracle_df = get_oracle_image_info_table(stim_key)
    for _, row in tqdm(oracle_df.iterrows(), total=len(oracle_df)):
        dst.Image(**row).put(get_stimulus_image(dict(row)))

    logger.info(f"Exporting stimulus images...")
    stim_df = get_image_info_table(stim_key)
    for _, row in tqdm(stim_df.iterrows(), total=len(stim_df)):
        dst.Image(**row).put(get_stimulus_image(dict(row)))