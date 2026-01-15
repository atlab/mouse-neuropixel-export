from enty import Schema
from . import dataclass, PickleAdapter, NumpyAdapter

schema = Schema(
    prefix='stim',
    base_dir='/mnt/at-export01/mouse_neuropixel_export/schemas/stimulus',
    make_dir=True,
    append_class_sub_dir=True
)

@schema
class EphysSync(PickleAdapter):
    @dataclass
    class Key():
        animal_id: int
        session: int
        scan_idx: int


@schema
class Trial(PickleAdapter):
    @dataclass
    class Key(EphysSync.Key):
        pass


@schema
class TargetAlbumNpx(PickleAdapter):
    @dataclass
    class Key():
        collection_id: int
        image_class: str


@schema
class ImageOracleInfo(PickleAdapter):
    @dataclass
    class Key(TargetAlbumNpx.Key):
        pass


@schema
class ImageInfo(PickleAdapter):
    @dataclass
    class Key(TargetAlbumNpx.Key):
        pass


@schema
class ImageOracleFrameInfo(PickleAdapter):
    @dataclass
    class Key(TargetAlbumNpx.Key):
        pass


@schema
class ImageFrameInfo(PickleAdapter):
    @dataclass
    class Key(TargetAlbumNpx.Key):
        pass


@schema
class Image(NumpyAdapter):
    @dataclass
    class Key():
        image_class: str
        image_id: int